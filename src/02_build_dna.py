from pathlib import Path

import MDAnalysis as mda

ROOT = Path(__file__).resolve().parents[1]
DNA_PDB = ROOT / "structures" / "dna_30bp.pdb"


def residue_chain_id(residue) -> str:
    chain_id = getattr(residue, "chainID", "") or ""
    segid = getattr(residue, "segid", "") or ""
    return chain_id.strip() or segid.strip() or "A"


def main() -> None:
    if not DNA_PDB.exists():
        raise SystemExit(
            "Missing structures/dna_30bp.pdb. This repo expects the validated 30 bp DNA input to already be present."
        )

    universe = mda.Universe(str(DNA_PDB))
    chain_counts: dict[str, int] = {}
    chain_resnames: dict[str, list[str]] = {}
    for residue in universe.residues:
        chain_id = residue_chain_id(residue)
        chain_counts[chain_id] = chain_counts.get(chain_id, 0) + 1
        chain_resnames.setdefault(chain_id, []).append(residue.resname.strip())

    print(f"Validated {DNA_PDB.relative_to(ROOT)}")
    for chain_id in sorted(chain_counts):
        preview = "-".join(chain_resnames[chain_id][:6])
        print(f"chain {chain_id}: {chain_counts[chain_id]} residues | preview {preview}")

    print("Step 2 in this repo validates the provided DNA input; it does not regenerate DNA coordinates.")


if __name__ == "__main__":
    main()
