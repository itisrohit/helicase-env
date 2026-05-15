# Simulation Part 3: Force Fields, Topology, Solvent, and Ions

This section adds more scientific depth to the simulation side.

## Why Coordinates Alone Are Not Physics

If you only know where particles are, you know geometry but not behavior.

A simulation needs more than coordinates. It needs a model for:
- bonded structure
- nonbonded interactions
- charge-like behavior
- particle identity
- environment composition

That full model is built from **topology** plus a **force field**.

## What A Force Field Means Scientifically

A force field is a simplified mathematical model of how particles interact.

For a beginner, the easiest way to think about it is:
- it tells the computer what particles exist
- how strongly they attract or repel
- which particles are connected
- what energetic rules are used

This is why changing the force field is not cosmetic. It changes the scientific model being used.

## What Topology Means Scientifically

Topology is the structural rulebook for the model.

It tells the simulation things like:
- what molecules are present
- what particle types they contain
- how particles are bonded
- what support parameter files must be included

In practice:
- the coordinate file answers “where?”
- the topology answers “what exactly is this system?”

## Why Protein And DNA Compatibility Matters

If protein and DNA are represented with incompatible modeling assumptions, the result may still be drawable but not scientifically clean as a simulation starting point.

That is why the repo distinguishes between:
- a practical delivered handoff
- and an ideal fully force-field-consistent target

The delivery is useful because it preserves the intended geometry and workflow.
But the repo also documents where the scientific ideal and the practical toolchain diverged.

## Why Water Matters Scientifically

Water is not just “background filler.”

In biomolecular systems, water affects:
- screening of charges
- local packing
- molecular stabilization
- ion distribution
- interaction surfaces

That is why a bare protein + DNA complex is usually not enough for meaningful simulation preparation.

## Why Ions Matter Scientifically

Ions are also not decorative.

They affect:
- electrostatic screening
- local environment around charged biomolecules
- stabilization or destabilization of certain interactions
- solution conditions relevant to experimental setups

That is why the repo specifically tracks:
- sodium-like species
- chloride-like species
- divalent magnesium-like species

## Why Mg Is Called A Proxy Here

This is scientifically important.

The repo uses a documented `MG2` proxy in the final handoff bundle.

That means:
- the intended chemical role is magnesium-like divalent ionic content
- but the exact local available force-field path did not provide a native final Mg definition in the same way the repo needed

So the repo preserves:
- the intended stoichiometric idea
- the practical handoff behavior

while also being explicit that this is a proxy choice.

That honesty matters scientifically.

## Why The Solvated System Is Called “Inspection” Here

The file `cg/solvated_inspection_system.pdb` is named carefully.

It is not called a finished production system because the repo is deliberately not overstating what has been proven.

Scientifically, the file is best treated as:
- a local environment construction
- a geometry-check artifact
- a handoff preparation artifact

not as final proof that all production-simulation assumptions have already been validated.

## The Important Beginner Takeaway

At the scientific level, this repo is not only about drawing molecules.

It is about building a model that answers:
- what particles are in the system?
- what rules describe them?
- what environment surrounds them?
- and how honestly can we claim simulation readiness?
