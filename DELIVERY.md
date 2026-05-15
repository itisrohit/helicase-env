# Delivery

As of May 15, 2026, the requested **local environment handoff** is prepared.

## Delivered

Recommended one-command rebuild:
- `uv run --locked twinkle-delivery`

Packaged artifact:
- `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`

Expanded handoff directory:
- `cg/handoff_m2_mg_proxy/`

Static visuals:
- `deliverables/twinkle_dsDNA_complex_overview.png`
- `deliverables/twinkle_dsDNA_environment_overview.png`
- `deliverables/twinkle_dsDNA_environment_zoom.png`

Interactive inspection:
- `notebooks/visualize.ipynb`

## Delivered Scope

This handoff includes:
- Twinkle hexamer coarse-grained coordinates
- 30 bp dsDNA coarse-grained coordinates and topology
- a local solvated water + ion environment
- an HPC-side GROMACS handoff bundle

## Not Claimed

This delivery is **not** claiming:
- a true Martini 3 dsDNA production workflow
- a completed production simulation
- an official Martini 2 Mg ion model

The delivered branch is a practical Martini 2 rescue path with a documented `MG2` proxy.
