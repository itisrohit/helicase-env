# Twinkle + dsDNA Delivery Repo

This repo prepares the **local starting environment** requested for a Twinkle hexamer + 30 bp dsDNA system in water with salt, and packages it for later HPC-side simulation.

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
uv sync
uv run python src/02_build_dna.py
uv run python src/03_coarse_grain.py
uv run python src/04_merge.py
uv run python src/05_solvate.py
uv run python src/06_simulate.py
```

Optional:
- `uv run python src/01_clean.py` if you need to re-download `7T8C.pdb`
- `MPLCONFIGDIR=/private/tmp/.mpl .venv/bin/python src/07_render_delivery_views.py` to regenerate static PNGs
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
