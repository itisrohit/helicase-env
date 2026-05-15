import json
from pathlib import Path

import MDAnalysis as mda
import numpy as np
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
CG_DIR = ROOT / "cg"
INPUT_PDB = CG_DIR / "complex_cg.pdb"
OUTPUT_PDB = CG_DIR / "solvated_inspection_system.pdb"
OUTPUT_JSON = CG_DIR / "solvated_inspection_system.json"

GRID_SPACING_A = 4.7
PADDING_A = 28.0
EXCLUSION_A = 4.2
NA_CL_MOLAR = 0.100
MG_CL2_MOLAR = 0.0075
ANGSTROM3_TO_LITER = 1e-27
RNG_SEED = 20260514


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def volume_liters(box_lengths_a: np.ndarray) -> float:
    return float(np.prod(box_lengths_a) * ANGSTROM3_TO_LITER)


def concentration_count(molarity: float, box_lengths_a: np.ndarray) -> int:
    avogadro = 6.02214076e23
    return int(round(molarity * avogadro * volume_liters(box_lengths_a)))


def pdb_atom_line(
    record: str,
    serial: int,
    atom_name: str,
    resname: str,
    chain_id: str,
    resid: int,
    position: np.ndarray,
) -> str:
    x, y, z = position
    return (
        f"{record:<6}{serial:5d} {atom_name:>4s} {resname:>3s} {chain_id}{resid:4d}"
        f"    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n"
    )


def write_system(
    source_pdb: Path,
    solvent_positions: np.ndarray,
    ion_positions: dict[str, np.ndarray],
    box_lengths_a: np.ndarray,
) -> None:
    lines = source_pdb.read_text().splitlines()
    atom_lines = [line for line in lines if line.startswith(("ATOM", "HETATM"))]
    serial = len(atom_lines) + 1
    resid = 1

    with OUTPUT_PDB.open("w") as handle:
        handle.write("TITLE     PROVISIONAL CG SOLVATED INSPECTION SYSTEM\n")
        handle.write(
            "CRYST1"
            f"{box_lengths_a[0]:9.3f}{box_lengths_a[1]:9.3f}{box_lengths_a[2]:9.3f}"
            "  90.00  90.00  90.00 P 1           1\n"
        )
        handle.write(
            "REMARK    Generated for geometric inspection only; not a validated production topology.\n"
        )
        for line in atom_lines:
            handle.write(f"{line}\n")
        for position in solvent_positions:
            handle.write(pdb_atom_line("HETATM", serial, "W", "W", "S", resid, position))
            serial += 1
            resid = 1 if resid == 9999 else resid + 1
        for resname, positions in ion_positions.items():
            for position in positions:
                handle.write(
                    pdb_atom_line("HETATM", serial, resname, resname, "I", resid, position)
                )
                serial += 1
                resid = 1 if resid == 9999 else resid + 1
        handle.write("END\n")


def main() -> None:
    if not INPUT_PDB.exists():
        raise SystemExit(f"Missing {rel(INPUT_PDB)}. Run src/04_merge.py first.")

    universe = mda.Universe(str(INPUT_PDB))
    solute = universe.atoms.positions.astype(float)

    mins = solute.min(axis=0) - PADDING_A
    maxs = solute.max(axis=0) + PADDING_A
    box_lengths = maxs - mins

    xs = np.arange(mins[0], maxs[0] + GRID_SPACING_A, GRID_SPACING_A)
    ys = np.arange(mins[1], maxs[1] + GRID_SPACING_A, GRID_SPACING_A)
    zs = np.arange(mins[2], maxs[2] + GRID_SPACING_A, GRID_SPACING_A)
    grid = np.stack(np.meshgrid(xs, ys, zs, indexing="ij"), axis=-1).reshape(-1, 3)

    tree = cKDTree(solute)
    distances, _ = tree.query(grid, workers=-1)
    free_sites = grid[distances >= EXCLUSION_A]

    na_count = concentration_count(NA_CL_MOLAR, box_lengths)
    cl_count = concentration_count(NA_CL_MOLAR, box_lengths) + 2 * concentration_count(
        MG_CL2_MOLAR, box_lengths
    )
    mg_count = concentration_count(MG_CL2_MOLAR, box_lengths)
    total_ions = na_count + cl_count + mg_count

    if len(free_sites) <= total_ions:
        raise SystemExit(
            "Not enough free solvent sites for ions. Increase the box or reduce spacing."
        )

    rng = np.random.default_rng(RNG_SEED)
    selected = rng.permutation(len(free_sites))
    ion_sites = free_sites[selected[:total_ions]]
    water_sites = free_sites[selected[total_ions:]]

    ion_positions = {
        "NA": ion_sites[:na_count],
        "CL": ion_sites[na_count : na_count + cl_count],
        "MG": ion_sites[na_count + cl_count :],
    }

    write_system(INPUT_PDB, water_sites, ion_positions, box_lengths)

    metadata = {
        "type": "inspection_only",
        "input_complex": str(INPUT_PDB.relative_to(ROOT)),
        "output_pdb": str(OUTPUT_PDB.relative_to(ROOT)),
        "grid_spacing_angstrom": GRID_SPACING_A,
        "padding_angstrom": PADDING_A,
        "exclusion_angstrom": EXCLUSION_A,
        "box_lengths_angstrom": box_lengths.tolist(),
        "counts": {
            "solute_beads": int(len(solute)),
            "water_beads": int(len(water_sites)),
            "na": int(na_count),
            "cl": int(cl_count),
            "mg": int(mg_count),
        },
        "notes": [
            "This file is for geometric inspection and notebook visualization.",
            "It is not a validated simulation-ready Martini topology.",
            "The merged complex may come from the consistent Martini 2 fallback pair when available.",
        ],
    }
    OUTPUT_JSON.write_text(json.dumps(metadata, indent=2))

    print(f"Wrote {rel(OUTPUT_PDB)}")
    print(f"Wrote {rel(OUTPUT_JSON)}")
    print(json.dumps(metadata["counts"], indent=2))


if __name__ == "__main__":
    main()
