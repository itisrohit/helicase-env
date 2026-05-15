# Simulation Part 1: Molecular Simulation Basics

This section explains the computational ideas behind the repo without assuming prior simulation knowledge.

## What Molecular Simulation Is

Molecular simulation is a way of representing molecules in a computer so that we can:
- inspect their structures
- place them relative to one another
- prepare environments around them
- sometimes simulate how they move over time

This repo is mainly about the **preparation** stage.

## Why A Structure File Is Not Enough

A structure file gives coordinates. In simple terms, it tells you where particles are in space.

But a simulation also needs rules describing:
- what the particles are
- how they interact
- what bonds or connections exist
- what force model is being used

That is why simulation workflows often produce more than just one coordinate file.

## Structure vs Topology

This distinction is very important.

### Structure file

A structure file mainly answers:
- where are the beads or atoms?

Examples in this repo:
- `cg/complex_cg.pdb`
- `cg/solvated_inspection_system.pdb`

### Topology file

A topology file mainly answers:
- what are the molecule types?
- how are they connected?
- what supporting force-field files are needed?

Examples in this repo:
- `cg/handoff_m2_mg_proxy/system.top`
- `cg/dna_fallback_m2_cg.itp`

## What A Force Field Is

A **force field** is a set of rules and parameters used to model molecular interactions.

For a beginner, it helps to think of it as:
- the instruction set that tells the simulation how particles behave

Different force fields make different modeling choices. That is why saying “Martini 2” versus “Martini 3” is not a minor naming detail. It affects compatibility and interpretation.

## Why Water and Ions Are Added

Biological molecules do not normally exist in empty space.

They are surrounded by:
- water
- salts
- charged species

So if we want a realistic starting environment, we need more than just protein + DNA coordinates.

We also need:
- a local solvent environment
- ions at the intended concentration

## What This Repo Delivers At The Simulation Level

The repo delivers:

- a merged solute
  Twinkle + dsDNA

- a local solvated inspection environment
  water + ions around the solute

- an HPC handoff bundle
  files that can be taken forward for later simulation work

## The Important Beginner Takeaway

In molecular simulation, “build the system” means much more than “download a structure.”

It usually means:
- get the biomolecular parts
- choose a representation
- choose a force model
- combine the parts
- add solvent and ions
- produce the files needed for later computation
