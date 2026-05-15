import json
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG_DIR = ROOT / "cg"
OFFICIAL_M2_DIR = ROOT / "vendor" / "martini2-official"
OFFICIAL_TUTORIAL_TAR = OFFICIAL_M2_DIR / "na-tutorials_20170815.tar"
HANDOFF_DIR = CG_DIR / "handoff_m2_mg_proxy"

INSPECTION_PDB = CG_DIR / "solvated_inspection_system.pdb"
INSPECTION_JSON = CG_DIR / "solvated_inspection_system.json"
PROTEIN_TOP = CG_DIR / "twinkle_m2.top"
DNA_ITP = CG_DIR / "dna_fallback_m2_cg.itp"


def require(path: Path, message: str) -> None:
    if not path.exists():
        raise SystemExit(message)


def extract_tar_member(archive: Path, member: str, destination: Path) -> None:
    with tarfile.open(archive, "r") as handle:
        extracted = handle.extractfile(member)
        if extracted is None:
            raise SystemExit(f"Could not extract {member} from {archive.name}.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(extracted.read())


def ensure_official_assets() -> dict[str, Path]:
    require(
        OFFICIAL_M2_DIR / "martini_v2.2.itp",
        "Missing official Martini 2 base force field. Download martini_v2.2.itp first.",
    )
    require(
        OFFICIAL_M2_DIR / "martini_v2.0_ions.itp",
        "Missing official Martini 2 ions file. Download martini_v2.0_ions.itp first.",
    )
    require(
        OFFICIAL_TUTORIAL_TAR,
        "Missing official Martini DNA tutorial archive. Download na-tutorials_20170815.tar first.",
    )

    extracted_dir = OFFICIAL_M2_DIR / "extracted"
    assets = {
        "martini_v2.1P-dna.itp": "./na-tutorials/dna-tutorial/martini-dna/martini_v2.1P-dna.itp",
        "water.gro": "./na-tutorials/dna-tutorial/protein_DNA/water.gro",
        "em.mdp": "./na-tutorials/dna-tutorial/martini-dna/em.mdp",
        "equil.mdp": "./na-tutorials/dna-tutorial/martini-dna/equil.mdp",
        "mdrun.mdp": "./na-tutorials/dna-tutorial/martini-dna/mdrun.mdp",
    }
    resolved: dict[str, Path] = {
        "martini_v2.2.itp": OFFICIAL_M2_DIR / "martini_v2.2.itp",
        "martini_v2.0_ions.itp": OFFICIAL_M2_DIR / "martini_v2.0_ions.itp",
    }
    for name, member in assets.items():
        destination = extracted_dir / name
        if not destination.exists():
            extract_tar_member(OFFICIAL_TUTORIAL_TAR, member, destination)
        resolved[name] = destination
    return resolved


def parse_twinkle_topology(path: Path) -> tuple[list[str], list[str]]:
    includes: list[str] = []
    molecules: list[str] = []
    in_molecules = False
    seen_includes: set[str] = set()
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if raw_line.startswith('#include "molecule_'):
            if raw_line not in seen_includes:
                includes.append(raw_line)
                seen_includes.add(raw_line)
        if line.startswith("["):
            in_molecules = line == "[ molecules ]"
            continue
        if in_molecules and line and not line.startswith(";"):
            molecules.append(line)
    if not includes or not molecules:
        raise SystemExit(f"Could not parse molecule includes from {path}.")
    return includes, molecules


def copy_molecule_itps(include_lines: list[str], destination: Path) -> list[str]:
    copied: list[str] = []
    for include_line in include_lines:
        filename = include_line.split('"')[1]
        if filename in copied:
            continue
        source = CG_DIR / filename
        if not source.exists():
            source = ROOT / filename
        require(source, f"Missing {filename}. Re-run src/03_coarse_grain.py.")
        shutil.copy2(source, destination / filename)
        copied.append(filename)
    return copied


def rewrite_proxy_pdb(source: Path, destination: Path) -> None:
    rename_map = {
        "NA": "NA+",
        "CL": "CL-",
        "MG": "MG2",
    }
    lines_out: list[str] = []
    for line in source.read_text().splitlines():
        if line.startswith(("ATOM", "HETATM")):
            atom_name = line[12:16].strip()
            resname = line[17:20].strip()
            replacement = rename_map.get(resname, rename_map.get(atom_name))
            if replacement:
                line = f"{line[:12]}{replacement:>4s}{line[16:17]}{replacement:>3s}{line[20:]}"
        lines_out.append(line)
    destination.write_text("\n".join(lines_out) + "\n")


def write_system_topology(
    destination: Path,
    include_lines: list[str],
    molecule_lines: list[str],
    counts: dict[str, int],
) -> None:
    output = [
        '#include "martini_v2.2.itp"',
        '#include "martini_v2.0_ions.itp"',
        '#include "mg_proxy.itp"',
        '#include "martini_v2.1P-dna.itp"',
    ]
    output.extend(include_lines)
    output.append('#include "dna_fallback_m2_cg.itp"')
    output.extend(
        [
            "",
            "[ system ]",
            "Twinkle hexamer + 30bp dsDNA Martini 2 fallback handoff",
            "",
            "[ molecules ]",
        ]
    )
    output.extend(molecule_lines)
    output.append("dna_fallback_m2    1")
    output.append(f"W                {counts['water_beads']}")
    output.append(f"NA+              {counts['na']}")
    output.append(f"CL-              {counts['cl']}")
    output.append(f"MG2              {counts['mg']}")
    destination.write_text("\n".join(output) + "\n")


def write_mg_proxy_itp(destination: Path) -> None:
    destination.write_text(
        """;;; Local Mg proxy for Martini 2 fallback handoff.
;;; Uses the same Qd divalent bead class and +2 charge as the official CA+ ion.
;;; This preserves the requested MgCl2 stoichiometry in file naming while keeping
;;; the nonbonded behavior explicitly identical to the official divalent ion model.

[ moleculetype ]
; molname  nrexcl
  MG2      1

[ atoms ]
;id  type  resnr  residu  atom  cgnr  charge
 1   Qd    1      ION     MG2   1     2.0
"""
    )


def write_handoff_readme(destination: Path, counts: dict[str, int]) -> None:
    text = f"""# Martini 2 fallback HPC handoff

This directory is the delivered handoff bundle for the local environment request.

Contents:
- `system.top`
- `solvated_m2_mg_proxy.pdb`
- `mg_proxy.itp`
- `em.mdp`
- `equil.mdp`
- `mdrun.mdp`
- official Martini 2 support files bundled for handoff

Scope:
- this is the delivered Martini 2 rescue branch
- this is meant for later HPC-side GROMACS preparation
- this is not a claim of a solved Martini 3 dsDNA workflow

Model tradeoff:
- the bundle uses a documented local `MG2` proxy because the official Martini 2 ion file available here does not define Mg
- the `{counts["mg"]}` requested divalent ions are therefore represented by that local proxy
"""
    destination.write_text(text)


def write_manifest(destination: Path, counts: dict[str, int], molecule_files: list[str]) -> None:
    manifest = {
        "type": "martini2_fallback_handoff",
        "coordinate_source": str(INSPECTION_PDB.relative_to(ROOT)),
        "topology": "system.top",
        "requested_solution": {
            "na_cl_molar": 0.100,
            "mg_cl2_molar": 0.0075,
        },
        "encoded_solution": {
            "na_count": counts["na"],
            "cl_count": counts["cl"],
            "mg_proxy_count": counts["mg"],
        },
        "notes": [
            "The official Martini 2 ion file does not provide Mg.",
            "MG2 is a local proxy that reuses the official CA+ bead type Qd with +2 charge.",
            "The solvent coordinates were packed for inspection and should be relaxed by minimization and equilibration on HPC.",
        ],
        "protein_molecule_itps": molecule_files,
    }
    destination.write_text(json.dumps(manifest, indent=2))


def main() -> None:
    require(
        INSPECTION_PDB, "Missing cg/solvated_inspection_system.pdb. Run src/05_solvate.py first."
    )
    require(
        INSPECTION_JSON, "Missing cg/solvated_inspection_system.json. Run src/05_solvate.py first."
    )
    require(PROTEIN_TOP, "Missing cg/twinkle_m2.top. Run src/03_coarse_grain.py first.")
    require(DNA_ITP, "Missing cg/dna_fallback_m2_cg.itp. Run src/03_coarse_grain.py first.")

    assets = ensure_official_assets()
    include_lines, molecule_lines = parse_twinkle_topology(PROTEIN_TOP)
    counts = json.loads(INSPECTION_JSON.read_text())["counts"]

    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    rewrite_proxy_pdb(INSPECTION_PDB, HANDOFF_DIR / "solvated_m2_mg_proxy.pdb")
    shutil.copy2(CG_DIR / "complex_cg.pdb", HANDOFF_DIR / "complex_cg.pdb")
    shutil.copy2(CG_DIR / "twinkle_m2_cg.pdb", HANDOFF_DIR / "twinkle_m2_cg.pdb")
    shutil.copy2(CG_DIR / "dna_fallback_m2_cg.pdb", HANDOFF_DIR / "dna_fallback_m2_cg.pdb")
    shutil.copy2(DNA_ITP, HANDOFF_DIR / "dna_fallback_m2_cg.itp")

    for asset_name, source in assets.items():
        shutil.copy2(source, HANDOFF_DIR / asset_name)

    molecule_files = copy_molecule_itps(include_lines, HANDOFF_DIR)
    write_mg_proxy_itp(HANDOFF_DIR / "mg_proxy.itp")
    write_system_topology(HANDOFF_DIR / "system.top", include_lines, molecule_lines, counts)
    write_handoff_readme(HANDOFF_DIR / "README.md", counts)
    write_manifest(HANDOFF_DIR / "manifest.json", counts, molecule_files)

    print(f"Wrote {HANDOFF_DIR.relative_to(ROOT)}")
    print("This is an HPC handoff bundle, not a local simulation run.")


if __name__ == "__main__":
    main()
