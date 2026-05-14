# src/04_merge.py
# Place DNA through center of Twinkle ring (along Z-axis)
from pathlib import Path

import MDAnalysis as mda
import numpy as np

Path("cg").mkdir(exist_ok=True)

try:
    protein_path = Path("cg/twinkle_m2_cg.pdb")
    if not protein_path.exists():
        protein_path = Path("cg/twinkle_cg.pdb")
    protein = mda.Universe(str(protein_path))

    dna_path = Path("cg/dna_fallback_m2_cg.pdb")
    if not dna_path.exists():
        dna_path = Path("cg/dna_cg.pdb")
    dna = mda.Universe(str(dna_path))

    protein_finite = protein.atoms[np.isfinite(protein.atoms.positions).all(axis=1)]
    dna_finite = dna.atoms[np.isfinite(dna.atoms.positions).all(axis=1)]
    removed = len(protein.atoms) - len(protein_finite)
    if removed:
        print(f"Removed {removed} protein beads with non-finite coordinates before merge.")

    # Center protein at origin
    protein_finite.translate(-protein_finite.center_of_geometry())

    # Center DNA, align along Z through ring channel
    dna_finite.translate(-dna_finite.center_of_geometry())

    merged = mda.Merge(protein_finite, dna_finite)
    merged.atoms.write("cg/complex_cg.pdb")
    print(f"complex_cg.pdb saved using {protein_path.name} + {dna_path.name}.")
except FileNotFoundError:
    print("Error: cg/twinkle_cg.pdb or a DNA CG PDB was not found. Run earlier steps first.")
