# Twinkle + dsDNA Delivery Repo

This repo prepares the **local starting environment** requested for a Twinkle hexamer + 30 bp dsDNA system in water with salt, and packages it for later HPC-side simulation.

## Fastest Run

For the normal local delivery flow, use one command:

```bash
uv run --locked twinkle-delivery
```

This is the command that generates the PNG visuals too. If you use `--skip-render`, the images will not be regenerated.

What it does:
- validates the provided DNA input
- coarse-grains the available protein and DNA inputs
- merges the complex
- builds the local solvated inspection environment
- builds the HPC handoff bundle
- renders the static delivery PNGs

Useful variants:
- `uv run --locked twinkle-delivery --refresh-twinkle`
  Re-download `7T8C` and rebuild `structures/twinkle_hex.pdb`.
- `uv run --locked twinkle-delivery --skip-render`
  Skip PNG generation. Do not use this if you want fresh visuals.
- `uv run --locked twinkle-delivery --open-notebook`
  Launch `notebooks/visualize.ipynb` at the end.

## Prerequisites

Required before running the one-command flow:
- Python `3.12+`
- `uv`
- access to the checked-in repo files, including `uv.lock`

Needed only for optional paths:
- internet access if you use `--refresh-twinkle`
- a browser-capable local Jupyter setup if you use `--open-notebook`

Not required for the local handoff build:
- system-wide GROMACS
- system-wide Martini downloads
- manual virtualenv activation

Reproducibility notes:
- run through `uv run --locked ...` so the command uses the repo lockfile instead of silently changing dependency resolution
- the repo lockfile is cross-platform, and `uv` installs the project environment automatically before running the command
- the workflow now resolves console tools from the active environment and does not hardcode `.venv/bin/...`

## Scope

What this repo **does**:
- prepares a merged Twinkle + dsDNA coarse-grained complex
- prepares a local solvated environment with the requested salt counts
- prepares an HPC handoff bundle
- provides static and notebook-based visualization for inspection

What this repo **does not claim**:
- a finished Martini 3 dsDNA workflow
- a completed production simulation
- validated Mg parameters from an official Martini 2 ion file

## Delivered Artifacts

Primary packaged handoff:
- `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`

Expanded handoff directory:
- `cg/handoff_m2_mg_proxy/`

Key local outputs:
- `cg/complex_cg.pdb`
- `cg/solvated_inspection_system.pdb`
- `cg/solvated_inspection_system.json`

Visualization outputs:
- `deliverables/twinkle_dsDNA_complex_overview.png`
- `deliverables/twinkle_dsDNA_environment_overview.png`
- `deliverables/twinkle_dsDNA_environment_zoom.png`
- `notebooks/visualize.ipynb`

## Delivered Model Choice

The delivered branch is a **Martini 2 rescue path**, because the intended Martini 3 dsDNA path is still upstream-blocked in the local `martinize2/vermouth` workflow.

The final handoff bundle uses:
- Martini 2 protein fallback
- Martini 2 DNA fallback
- a documented local `MG2` proxy that reuses the official Martini 2 divalent `Qd` +2 ion behavior

## End-to-End Run

```bash
uv sync --locked
uv run --locked twinkle-delivery
```

Expected render outputs from the full command:
- `deliverables/twinkle_dsDNA_complex_overview.png`
- `deliverables/twinkle_dsDNA_environment_overview.png`
- `deliverables/twinkle_dsDNA_environment_zoom.png`

Manual equivalent:
- `uv run python src/02_build_dna.py`
- `uv run python src/03_coarse_grain.py`
- `uv run python src/04_merge.py`
- `uv run python src/05_solvate.py`
- `uv run python src/06_simulate.py`
- `uv run python src/07_render_delivery_views.py`

Optional:
- `uv run python src/01_clean.py` if you need to re-download `7T8C.pdb`
- `uv run jupyter notebook notebooks/visualize.ipynb` for interactive inspection

## Files to Show

If you need to show progress quickly:
1. `deliverables/twinkle_dsDNA_complex_overview.png`
2. `deliverables/twinkle_dsDNA_environment_zoom.png`
3. `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`

## Supporting Notes

- `DELIVERY.md`: exact handoff statement
- `docs/plan.md`: concise status and scope
- `docs/journal.md`: engineering decisions and known tradeoffs

## Hardcoded Defaults

The one-command flow is intentionally opinionated so it runs smoothly without manual choices.

- Twinkle source is hardcoded to PDB `7T8C`, and the local hexamer is hardcoded to chains `A-F` in `src/01_clean.py`.
- The DNA input is hardcoded to `structures/dna_30bp.pdb`, and `src/02_build_dna.py` validates that file instead of generating a new duplex.
- If the two DNA strands carry the same `5'->3'` sequence, `src/03_coarse_grain.py` hardcodes a fallback that derives the sequence from the first strand and builds an idealized dsDNA CG model from that sequence.
- The delivery branch is hardcoded to prefer the Martini 2 rescue path when available, including the `MG2` proxy used in the final handoff bundle.
- The local solvent builder in `src/05_solvate.py` is hardcoded to `100 mM` NaCl, `7.5 mM` MgCl2, `4.7 A` grid spacing, `28.0 A` padding, `4.2 A` solute exclusion, and RNG seed `20260514`.
- The render step is hardcoded to write the three PNGs in `deliverables/`.

If you need to change behavior, edit the corresponding script directly:
- `src/01_clean.py`: source PDB and chain selection
- `src/02_build_dna.py`: accepted DNA input contract
- `src/03_coarse_grain.py`: protein/DNA coarse-graining strategy
- `src/05_solvate.py`: salt concentrations, packing constants, RNG seed
- `src/06_simulate.py`: handoff bundle naming and Mg proxy behavior
- `src/07_render_delivery_views.py`: render layout and output filenames
