# Code Part 1: Repo and Python Workflow

This section explains the software side of the project in beginner terms.

## What A Repo Is

A repo is a version-controlled project folder.

It contains:
- code
- data files
- documentation
- generated outputs

In this project, the repo contains both:
- scientific inputs and outputs
- the Python scripts that build those outputs

## Why There Are Multiple Kinds Of Files

A beginner often expects one main file. But scientific repos usually contain several categories:

### Input structures

These are starting molecular structures.

Examples:
- `structures/twinkle_hex.pdb`
- `structures/dna_30bp.pdb`

### Intermediate coarse-grained files

These are generated during the pipeline.

Examples:
- `cg/twinkle_m2_cg.pdb`
- `cg/dna_fallback_m2_cg.pdb`
- `cg/complex_cg.pdb`

### Final delivery artifacts

These are intended for handoff or presentation.

Examples:
- `cg/handoff_m2_mg_proxy/`
- `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`
- `deliverables/*.png`

### Documentation

These explain what the repo is doing.

Examples:
- `README.md`
- `docs/plan.md`
- `docs/journal.md`
- `docs/visual_guide.md`

## What The Python Scripts Are Doing

Each script handles one stage of the workflow.

- `src/01_clean.py`
  Downloads and cleans the Twinkle source structure when needed.

- `src/02_build_dna.py`
  Validates the provided DNA input instead of regenerating it.

- `src/03_coarse_grain.py`
  Builds the coarse-grained protein and DNA outputs, including the fallback path.

- `src/04_merge.py`
  Combines protein and DNA into one merged complex.

- `src/05_solvate.py`
  Builds the local water-and-ion inspection environment.

- `src/06_simulate.py`
  Builds the HPC handoff bundle.

- `src/07_render_delivery_views.py`
  Generates the presentation PNGs.

## What `uv` Is Doing

`uv` is the project tool used to:
- manage the Python environment
- install dependencies
- run commands reproducibly

That is why the main usage pattern is:

```bash
uv run --locked twinkle-delivery
```

This means:
- use the repo’s locked dependency setup
- run the project’s defined entrypoint

## Why One Command Matters

Without a single entrypoint, users must remember the exact order of many scripts.

With the one-command runner:
- the workflow is easier to reproduce
- the order is preserved
- the docs can point to one stable command

## The Important Beginner Takeaway

The code side of this repo is not separate from the science. The code is the mechanism that turns:
- structures
- modeling choices
- and workflow decisions

into the final handoff files and visuals.
