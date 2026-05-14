# src/06_simulate.py
import os

from openmm import LangevinMiddleIntegrator
from openmm.app import PME, DCDReporter, ForceField, PDBFile, Simulation, StateDataReporter
from openmm.unit import HBonds, kelvin, nanometer, picosecond, picoseconds

input_pdb = "cg/solvated_system.pdb"
if not os.path.exists(input_pdb):
    print(f"Error: {input_pdb} not found. Run earlier steps first.")
    exit(1)

pdb = PDBFile(input_pdb)
ff = ForceField("charmm36.xml", "charmm36/water.xml")

system = ff.createSystem(
    pdb.topology,
    nonbondedMethod=PME,
    nonbondedCutoff=1.0 * nanometer,
    constraints=HBonds,
)

integrator = LangevinMiddleIntegrator(310 * kelvin, 1 / picosecond, 0.002 * picoseconds)
sim = Simulation(pdb.topology, system, integrator)
sim.context.setPositions(pdb.positions)

print("Minimizing energy...")
sim.minimizeEnergy()

os.makedirs("output", exist_ok=True)
sim.reporters.append(DCDReporter("output/traj.dcd", 1000))
sim.reporters.append(
    StateDataReporter(
        "output/energies.csv",
        1000,
        step=True,
        potentialEnergy=True,
        temperature=True,
        speed=True,
    )
)

print("Running...")
# Note: 500k steps is just a starting point.
sim.step(500_000)  # 10 ns at 20 fs CG timestep (adjust accordingly)
