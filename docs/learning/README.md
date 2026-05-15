# Learning Path

This folder is a beginner-friendly learning track for someone who has little or no background in:
- biology
- molecular simulation
- Python workflow tooling
- this specific repo

The goal is not just to define terms. The goal is to connect the dots in the right order so the repo makes sense.

## Best Reading Order

Read these files in order:

1. `01_big_picture.md`
2. `bio_01_dna_proteins_helicases.md`
3. `bio_02_twinkle_and_this_project.md`
4. `bio_03_structure_representation.md`
5. `sim_01_molecular_simulation_basics.md`
6. `sim_02_coarse_graining_and_martini.md`
7. `sim_03_force_fields_topology_and_solvent.md`
8. `code_01_repo_and_python_workflow.md`
9. `workflow_01_this_repo_end_to_end.md`
10. `glossary.md`

## Why It Is Split This Way

The material is separated into three tracks:

- **Biology**
  This explains what DNA is, what proteins are, what helicases do, and why Twinkle matters here.

- **Simulation**
  This explains what molecular simulation is, what “coarse-grained” means, how force fields and topology work, why solvent and ions matter, why Martini is used, and why the final delivery is a practical fallback rather than a perfect theoretical target.

- **Code and workflow**
  This explains how the repo is organized, what the scripts do, and how the one-command workflow maps to the scientific idea.

## What This Learning Material Assumes

Almost nothing.

It assumes only that the reader is willing to learn step by step and may not already know:
- what DNA looks like
- what a PDB file is
- what a topology is
- what a force field is
- what Python scripts are
- what `uv` is doing

## What This Material Is Trying To Achieve

By the end, a novice should be able to answer:

- What biological system is this repo modeling?
- Why is Twinkle shown as a ring around DNA?
- What is the difference between structure files, topology files, and rendered images?
- Why is the repo using a Martini 2 rescue branch instead of claiming a clean Martini 3 result?
- What exactly happens when `uv run --locked twinkle-delivery` is executed?
