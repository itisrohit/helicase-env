# src/04_merge.py
# Place DNA through center of Twinkle ring (along Z-axis)
from pathlib import Path

import MDAnalysis as mda

Path("cg").mkdir(exist_ok=True)

try:
    protein = mda.Universe("cg/twinkle_cg.pdb")
    dna = mda.Universe("cg/dna_cg.pdb")

    # Center protein at origin
    protein.atoms.translate(-protein.atoms.center_of_mass())

    # Center DNA, align along Z through ring channel
    dna.atoms.translate(-dna.atoms.center_of_mass())

    merged = mda.Merge(protein.atoms, dna.atoms)
    merged.atoms.write("cg/complex_cg.pdb")
    print("complex_cg.pdb saved.")
except FileNotFoundError:
    print("Error: cg/twinkle_cg.pdb or cg/dna_cg.pdb not found. Run earlier steps first.")
