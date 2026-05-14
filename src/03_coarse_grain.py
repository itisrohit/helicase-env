import glob
import math
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import MDAnalysis as mda
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CG_DIR = ROOT / "cg"
MARTINIZE = ROOT / ".venv" / "bin" / "martinize2"
POLYPLY = ROOT / ".venv" / "bin" / "polyply"
VENDORED_VERMOUTH = (
    ROOT / "vendor" / "martini-forcefields" / "regular" / "v3.0.0" / "vermouth_files"
)
EXTRA_FF_DIR = VENDORED_VERMOUTH / "force_fields"
EXTRA_MAP_DIR = VENDORED_VERMOUTH / "mappings"
VENDORED_NUCLEOBASE_ITP = (
    ROOT
    / "vendor"
    / "martini-forcefields"
    / "regular"
    / "v3.0.0"
    / "gmx_files"
    / "martini_v3.0.0_nucleobases_v1.itp"
)
LEGACY_DNA_DIR = ROOT / "vendor" / "legacy-martini2-dna"
LEGACY_DNA_SCRIPT = LEGACY_DNA_DIR / "martinize-dna.py"
OFFICIAL_M2_DIR = ROOT / "vendor" / "martini2-official"
OFFICIAL_M2_TUTORIAL_TAR = OFFICIAL_M2_DIR / "na-tutorials_20170815.tar"
DNA_FALLBACK_NAME = "dna_fallback_m2"
PROTEIN_FALLBACK_NAME = "twinkle_m2"

ONE_TO_RES = {"A": "DA", "C": "DC", "G": "DG", "T": "DT"}
RES_TO_ONE = {value: key for key, value in ONE_TO_RES.items()}
DNA_COMPLEMENT = {"A": "T", "C": "G", "G": "C", "T": "A"}


def residue_chain_id(residue) -> str:
    chain_id = getattr(residue, "chainID", "") or ""
    segid = getattr(residue, "segid", "") or ""
    return chain_id.strip() or segid.strip() or "A"


def base_cmd() -> list[str]:
    cmd = [str(MARTINIZE)]
    # The vendored upstream vermouth files are kept for reference, but they are
    # not enabled by default because their format is newer than the installed
    # vermouth parser in this environment.
    use_vendored = os.environ.get("USE_VENDORED_MARTINI_VERMOUTH") == "1"
    if use_vendored and EXTRA_FF_DIR.exists():
        cmd.extend(["-ff-dir", str(EXTRA_FF_DIR)])
    if use_vendored and EXTRA_MAP_DIR.exists():
        cmd.extend(["-map-dir", str(EXTRA_MAP_DIR)])
    return cmd


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)


def print_process_output(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print(result.stderr)


def explain_dna_blocker(result: subprocess.CompletedProcess[str]) -> None:
    print("DNA coarse-graining is still blocked.")
    print("Verified state:")
    print(
        "- Standard vermouth/martinize2 does not recognize atomistic DNA residues DA/DC/DG/DT here."
    )
    print(
        "- The vendored official Martini 3 vermouth bundle is pinned locally for reference, but it is not parser-compatible with the installed vermouth release here."
    )
    print(
        "- Even upstream official Martini 3 assets do not provide a complete martinize2-ready dsDNA polymer path in this workspace."
    )
    print(
        "- The official Martini repository currently provides nucleobase .itp parameters, not a full martinize2-ready dsDNA pipeline."
    )
    print(
        "- Official Martini legacy documentation still points dsDNA users to the Martini 2 `martinize-dna.py` workflow."
    )
    if VENDORED_NUCLEOBASE_ITP.exists():
        print(f"- Vendored reference nucleobase parameters: {VENDORED_NUCLEOBASE_ITP}")
    if LEGACY_DNA_SCRIPT.exists():
        print(f"- Legacy fallback script is available locally: {LEGACY_DNA_SCRIPT}")
    else:
        print(
            "- Legacy fallback script is not present locally. Drop the official Martini 2 DNA package into vendor/legacy-martini2-dna/ to enable that path."
        )
    print("Raw martinize2 output:")
    print_process_output(result)


def extract_tar_member(archive: Path, member: str, destination: Path) -> bool:
    if not archive.exists():
        return False
    with tarfile.open(archive, "r") as handle:
        try:
            extracted = handle.extractfile(member)
        except KeyError:
            return False
        if extracted is None:
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(extracted.read())
    return True


def ensure_legacy_dna_assets() -> None:
    assets = {
        "./na-tutorials/dna-tutorial/martini-dna/martinize-dna.py": LEGACY_DNA_SCRIPT,
        "./na-tutorials/dna-tutorial/martini-dna/martini_v2.1-dna.itp": LEGACY_DNA_DIR
        / "martini_v2.1-dna.itp",
        "./na-tutorials/dna-tutorial/martini-dna/martini_v2.1P-dna.itp": LEGACY_DNA_DIR
        / "martini_v2.1P-dna.itp",
    }
    for member, destination in assets.items():
        if destination.exists():
            continue
        if extract_tar_member(OFFICIAL_M2_TUTORIAL_TAR, member, destination):
            print(f"Bootstrapped legacy Martini 2 DNA asset: {destination.relative_to(ROOT)}")


def run_legacy_dna_martinize(dna_pdb: Path, dna_out: Path, dna_itp: Path) -> bool:
    ensure_legacy_dna_assets()
    if not LEGACY_DNA_SCRIPT.exists():
        return False

    print("Trying official legacy Martini 2 DNA fallback...")
    cmd = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(LEGACY_DNA_SCRIPT),
        "-dnatype",
        "ds-stiff",
        "-f",
        str(dna_pdb),
        "-o",
        str(dna_itp),
        "-x",
        str(dna_out),
    ]
    result = run_cmd(cmd)
    if result.returncode != 0:
        print("Legacy Martini 2 DNA fallback failed:")
        print_process_output(result)
        return False

    print("Legacy Martini 2 DNA fallback completed.")
    return True


def residue_name_sequence(sequence: str) -> list[str]:
    residues = [ONE_TO_RES[base] for base in sequence]
    residues[0] += "5"
    residues[-1] += "3"
    return residues


def bead_names(resname: str) -> list[str]:
    base = resname[:2]
    names = ["BB1", "BB2", "BB3", "SC1", "SC2", "SC3"]
    if resname.endswith("5"):
        names.remove("BB1")
    if base in {"DA", "DG"}:
        names.append("SC4")
    return names


def local_bead_positions(
    angle_deg: float, z_angstrom: float, resname: str
) -> dict[str, np.ndarray]:
    theta = math.radians(angle_deg)
    radial = np.array([math.cos(theta), math.sin(theta), 0.0])
    tangent = np.array([-math.sin(theta), math.cos(theta), 0.0])
    zhat = np.array([0.0, 0.0, 1.0])
    center = np.array([0.0, 0.0, z_angstrom])

    positions = {
        "BB1": center + 10.5 * radial + 1.6 * tangent - 1.2 * zhat,
        "BB2": center + 9.0 * radial + 0.8 * tangent - 0.2 * zhat,
        "BB3": center + 7.2 * radial + 0.2 * tangent + 0.6 * zhat,
        "SC1": center + 5.0 * radial - 0.4 * tangent,
        "SC2": center + 3.7 * radial + 1.6 * tangent + 0.3 * zhat,
        "SC3": center + 3.5 * radial - 1.4 * tangent - 0.3 * zhat,
    }
    if resname[:2] in {"DA", "DG"}:
        positions["SC4"] = center + 4.4 * radial - 0.2 * tangent + 1.0 * zhat
    return {name: positions[name] for name in bead_names(resname)}


def write_cg_pdb(sequence: str, out_pdb: Path) -> None:
    first_strand = residue_name_sequence(sequence)
    second_sequence = "".join(DNA_COMPLEMENT[base] for base in reversed(sequence))
    second_strand = residue_name_sequence(second_sequence)

    rise = 3.4
    twist = 36.0
    half_span = rise * (len(sequence) - 1) / 2.0
    serial = 1
    lines = ["REMARK    Generated idealized coarse-grained dsDNA fallback\n"]

    for chain_id, residues in (("A", first_strand), ("B", second_strand)):
        for resid, resname in enumerate(residues, start=1):
            if chain_id == "A":
                pair_index = resid - 1
                angle = pair_index * twist
            else:
                pair_index = len(sequence) - resid
                angle = pair_index * twist + 180.0
            z_pos = pair_index * rise - half_span
            for atom_name, position in local_bead_positions(angle, z_pos, resname).items():
                x, y, z = position
                lines.append(
                    f"ATOM  {serial:5d} {atom_name:>4s} {resname:>3s} {chain_id}{resid:4d}"
                    f"    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n"
                )
                serial += 1
        lines.append("TER\n")
    lines.append("END\n")
    out_pdb.write_text("".join(lines))


def first_dna_sequence(dna_pdb: Path) -> tuple[str, str]:
    universe = mda.Universe(str(dna_pdb))
    chain_ids = []
    for residue in universe.residues:
        chain_id = residue_chain_id(residue)
        if chain_id and chain_id not in chain_ids:
            chain_ids.append(chain_id)
    if not chain_ids:
        chain_ids = ["A"]
    chain_id = chain_ids[0]
    residues = universe.select_atoms(f"chainID {chain_id} or segid {chain_id}").residues
    sequence = "".join(RES_TO_ONE.get(res.resname.strip(), "N") for res in residues)
    return chain_id, sequence


def inspect_dna_input(dna_pdb: Path) -> bool:
    universe = mda.Universe(str(dna_pdb))
    chain_sequences: dict[str, str] = {}
    for residue in universe.residues:
        chain_id = residue_chain_id(residue)
        chain_sequences.setdefault(chain_id, "")
        chain_sequences[chain_id] += RES_TO_ONE.get(residue.resname.strip(), "N")
    if len(chain_sequences) >= 2:
        chains = list(chain_sequences.items())[:2]
        if chains[0][1] == chains[1][1]:
            print("Input DNA warning:")
            print(f"- {dna_pdb.name} contains at least two strands with the same 5'->3' sequence.")
            print("- This is not a chemically valid duplex template for direct coarse-graining.")
            print("- Falling back to sequence-driven dsDNA generation from the first strand.")
            return False
    return True


def run_polyply_dna_fallback(dna_pdb: Path, dna_out: Path, dna_itp: Path) -> bool:
    if not POLYPLY.exists():
        print("Polyply fallback is unavailable because `.venv/bin/polyply` is missing.")
        return False

    chain_id, sequence = first_dna_sequence(dna_pdb)
    if "N" in sequence or not sequence:
        print("Could not derive a clean DNA sequence from the atomistic PDB.")
        return False

    fasta_path = CG_DIR / "dna_30bp_sequence.fasta"
    fasta_path.write_text(f">DNA extracted from chain {chain_id}\n{sequence}\n")

    print("Trying official polyply Martini 2 DNA fallback...")
    print(f"- Using chain {chain_id} sequence: {sequence}")
    cmd = [
        str(POLYPLY),
        "gen_params",
        "-lib",
        "martini2",
        "-seqf",
        str(fasta_path),
        "-name",
        DNA_FALLBACK_NAME,
        "-o",
        str(dna_itp),
        "-dsdna",
    ]
    result = run_cmd(cmd)
    if result.returncode != 0:
        print("Polyply DNA fallback failed:")
        print_process_output(result)
        return False

    write_cg_pdb(sequence, dna_out)
    print(f"Polyply DNA fallback completed: {dna_itp.name}, {dna_out.name}")
    print("Note: this fallback is Martini 2 DNA, not Martini 3 DNA.")
    return True


def repair_nan_sidechains(input_pdb: Path, output_pdb: Path) -> int:
    defaults = {"LYS": 3.095, "ARG": 3.503}
    records: list[dict[str, object]] = []
    residue_atoms: dict[tuple[str, str, int], dict[str, np.ndarray]] = {}
    residue_order: list[tuple[str, str, int]] = []

    for line in input_pdb.read_text().splitlines():
        if not line.startswith("ATOM"):
            records.append({"kind": "raw", "line": line})
            continue
        atom_name = line[12:16].strip()
        resname = line[17:20].strip()
        chain = line[21].strip() or "A"
        resid = int(line[22:26])
        try:
            position = np.array(
                [float(line[30:38]), float(line[38:46]), float(line[46:54])],
                dtype=float,
            )
        except ValueError:
            position = np.array([np.nan, np.nan, np.nan], dtype=float)
        key = (resname, chain, resid)
        residue_atoms.setdefault(key, {})
        if key not in residue_order:
            residue_order.append(key)
        residue_atoms[key][atom_name] = position
        records.append(
            {
                "kind": "atom",
                "line": line,
                "atom_name": atom_name,
                "resname": resname,
                "chain": chain,
                "resid": resid,
                "position": position,
            }
        )

    sc1_sc2_lengths: dict[str, list[float]] = {}
    for (resname, _, _), atoms in residue_atoms.items():
        if {"BB", "SC1", "SC2"} <= atoms.keys() and np.isfinite(atoms["SC2"]).all():
            sc1_sc2_lengths.setdefault(resname, []).append(
                np.linalg.norm(atoms["SC2"] - atoms["SC1"])
            )

    repaired = 0
    for key in residue_order:
        resname, _, _ = key
        atoms = residue_atoms[key]
        if resname not in {"LYS", "ARG"}:
            continue
        if "SC2" not in atoms or np.isfinite(atoms["SC2"]).all():
            continue
        if not {"BB", "SC1"} <= atoms.keys():
            continue
        if not np.isfinite(atoms["BB"]).all() or not np.isfinite(atoms["SC1"]).all():
            continue
        direction = atoms["SC1"] - atoms["BB"]
        norm = np.linalg.norm(direction)
        if norm == 0:
            continue
        length = float(np.mean(sc1_sc2_lengths.get(resname, [defaults[resname]])))
        atoms["SC2"] = atoms["SC1"] + direction / norm * length
        repaired += 1

    out_lines: list[str] = []
    for record in records:
        if record["kind"] != "atom":
            out_lines.append(str(record["line"]))
            continue
        key = (str(record["resname"]), str(record["chain"]), int(record["resid"]))
        atom_name = str(record["atom_name"])
        position = residue_atoms[key][atom_name]
        line = str(record["line"])
        out_lines.append(
            f"{line[:30]}{position[0]:8.3f}{position[1]:8.3f}{position[2]:8.3f}{line[54:]}"
        )

    output_pdb.write_text("\n".join(out_lines) + "\n")
    return repaired


def run_protein_m2_fallback(input_pdb: Path) -> bool:
    raw_pdb = CG_DIR / f"{PROTEIN_FALLBACK_NAME}_raw.pdb"
    top_path = CG_DIR / f"{PROTEIN_FALLBACK_NAME}.top"
    final_pdb = CG_DIR / f"{PROTEIN_FALLBACK_NAME}_cg.pdb"

    print("Building consistent Martini 2 protein fallback...")
    cmd = base_cmd() + [
        "-f",
        str(input_pdb),
        "-x",
        str(raw_pdb),
        "-o",
        str(top_path),
        "-ff",
        "martini22",
        "-elastic",
        "-ef",
        "500",
        "-el",
        "0.5",
        "-eu",
        "0.9",
        "-ss",
        "C",
        "-noscfix",
    ]
    result = run_cmd(cmd)
    if result.returncode != 0:
        print("Martini 2 protein fallback failed:")
        print_process_output(result)
        return False

    repaired = repair_nan_sidechains(raw_pdb, final_pdb)
    print(f"Martini 2 protein fallback completed. Repaired {repaired} sidechain beads.")
    return True


def run_martinize():
    input_pdb = ROOT / "structures" / "twinkle_hex.pdb"
    output_pdb = CG_DIR / "twinkle_cg.pdb"
    output_top = CG_DIR / "twinkle_cg.top"

    CG_DIR.mkdir(exist_ok=True)
    ensure_legacy_dna_assets()

    print(f"Running martinize2 for {input_pdb}...")

    # Run martinize2
    # We use -maxwarn 1 because we don't have DSSP installed in this environment yet
    cmd = base_cmd() + [
        "-f",
        str(input_pdb),
        "-x",
        str(output_pdb),
        "-o",
        str(output_top),
        "-ff",
        "martini3001",
        "-elastic",
        "-ef",
        "500",
        "-el",
        "0.5",
        "-eu",
        "0.9",
        "-maxwarn",
        "1",
    ]

    result = run_cmd(cmd)

    if result.returncode != 0:
        print("Error running martinize2:")
        print_process_output(result)
        return

    print("martinize2 completed successfully for protein.")

    # --- DNA -> MARTINI 3 CG ---
    dna_pdb = ROOT / "structures" / "dna_30bp.pdb"
    dna_out = CG_DIR / "dna_fallback_m2_cg.pdb"
    dna_itp = CG_DIR / "dna_fallback_m2_cg.itp"

    if not inspect_dna_input(dna_pdb):
        if run_polyply_dna_fallback(dna_pdb, dna_out, dna_itp):
            run_protein_m2_fallback(input_pdb)
    else:
        print(f"Running martinize2 for {dna_pdb}...")
        cmd_dna = base_cmd() + [
            "-f",
            str(dna_pdb),
            "-x",
            str(dna_out),
            "-o",
            str(dna_itp),
            "-ff",
            "martini3001",
            "-maxwarn",
            "1",
        ]

        result_dna = run_cmd(cmd_dna)
        if result_dna.returncode != 0:
            explain_dna_blocker(result_dna)
            if not run_legacy_dna_martinize(dna_pdb, dna_out, dna_itp):
                if run_polyply_dna_fallback(dna_pdb, dna_out, dna_itp):
                    run_protein_m2_fallback(input_pdb)
        else:
            print("DNA coarse-graining completed.")

    # Move molecule_*.itp files to cg/
    itp_files = glob.glob("molecule_*.itp")
    for f in itp_files:
        shutil.move(f, CG_DIR / f)
        print(f"Moved {f} to cg/")

    # Clean up backups
    backups = glob.glob("#*#")
    for f in backups:
        os.remove(f)
        print(f"Removed backup {f}")


if __name__ == "__main__":
    run_martinize()
