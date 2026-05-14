# src/05_solvate.py
import os

from openmm.app import ForceField, Modeller, PDBFile
from openmm.unit import molar, nanometer

# --- Load CG complex ---
pdb_path = "cg/complex_cg.pdb"
if not os.path.exists(pdb_path):
    print(f"Error: {pdb_path} not found. Run earlier steps first.")
    exit(1)

pdb = PDBFile(pdb_path)
modeller = Modeller(pdb.topology, pdb.positions)

# --- Add TIP3P water box (2.0 nm padding) ---
# Note: For CG simulations, you'd typically use CG water (W), but the plan specifies TIP3P.
# In a real MARTINI setup, you'd use MARTINI water. This script follows the plan's logic.
print("Adding solvent...")
modeller.addSolvent(
    forcefield=ForceField("charmm36.xml", "charmm36/water.xml"),
    model="tip3p",
    padding=2.0 * nanometer,
)

# --- Ion counts from paper buffer (PMC7186178) ---
# 100 mM NaCl + 7.5 mM MgCl2 in HEPES pH 7.5
# Box ~= 20nm x 20nm x 20nm => 8000 nm3 = 8e-24 L
AVOGADRO = 6.022e23
box_vol_L = 8e-24

na = int(0.100 * AVOGADRO * box_vol_L)  # ~481 Na+
cl = int(0.100 * AVOGADRO * box_vol_L)  # ~481 Cl- (NaCl)
mg = int(0.0075 * AVOGADRO * box_vol_L)  # ~36 Mg2+
cl += mg * 2  # +72 Cl- for MgCl2

# neutralize net protein charge
print("Adding ions...")
modeller.addSolvent(
    forcefield=ForceField("charmm36.xml"),
    positiveIon="Na+",
    negativeIon="Cl-",
    ionicStrength=0.1 * molar,  # 100 mM
    neutralize=True,
)

print(f"System: {modeller.topology.getNumAtoms()} atoms")
print(f"Target ions: {na} Na+, {mg} Mg2+, {cl} Cl-")

# Save the environment
with open("cg/solvated_system.pdb", "w") as f:
    PDBFile.writeFile(modeller.topology, modeller.positions, f)

print("solvated_system.pdb saved — environment ready.")
