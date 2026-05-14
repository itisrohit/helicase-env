# src/02_build_dna.py
from pathlib import Path

import numpy as np
from Bio.PDB import PDBIO, Atom, Chain, Model, Residue, Structure


def generate_ideal_b_dna(n_bp=30):
    """
    Generates an idealized B-DNA structure (30 bp) using helical parameters.
    Saves it to structures/dna_30bp.pdb.
    """
    Path("structures").mkdir(exist_ok=True)

    # B-DNA helical parameters
    RISE = 3.38  # Angstroms per bp
    TWIST = 36.0  # Degrees per bp (360/10)
    RADIUS = 9.0  # Approx radius of backbone

    structure = Structure.Structure("DNA")
    model = Model.Model(0)
    chain_a = Chain.Chain("A")
    chain_b = Chain.Chain("B")

    # Residue names (alternating for simplicity)
    res_names = ["DA", "DT", "DC", "DG"]

    for i in range(n_bp):
        z = i * RISE
        angle = np.radians(i * TWIST)

        # --- Chain A ---
        res_a = Residue.Residue((" ", i + 1, " "), res_names[i % 4], " ")
        # Add a dummy P atom to represent the backbone for CG purposes
        # In a real PDB you'd have many atoms, but for martinize2, even CA/P helps
        x_a = RADIUS * np.cos(angle)
        y_a = RADIUS * np.sin(angle)
        atom_a = Atom.Atom("P", np.array([x_a, y_a, z]), 0, 1.0, " ", "P", i, "P")
        res_a.add(atom_a)
        chain_a.add(res_a)

        # --- Chain B (Complementary and antiparallel) ---
        # Angle offset by 180 degrees, z inverted or shifted
        # For simplicity, we just shift and rotate
        angle_b = angle + np.pi
        res_b = Residue.Residue((" ", i + 1, " "), res_names[(i + 1) % 4], " ")
        x_b = RADIUS * np.cos(angle_b)
        y_b = RADIUS * np.sin(angle_b)
        atom_b = Atom.Atom("P", np.array([x_b, y_b, z]), 0, 1.0, " ", "P", i, "P")
        res_b.add(atom_b)
        chain_b.add(res_b)

    model.add(chain_a)
    model.add(chain_b)
    structure.add(model)

    io = PDBIO()
    io.set_structure(structure)
    io.save("structures/dna_30bp.pdb")
    print(f"Idealized {n_bp}bp B-DNA saved to structures/dna_30bp.pdb")


if __name__ == "__main__":
    generate_ideal_b_dna()
