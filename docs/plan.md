# Plan

## Status (2026-05-15)

| Step | Status | Scope note |
| :--- | :--- | :--- |
| Twinkle structure prepared | ✅ Done | `7T8C.pdb` cleaned to `twinkle_hex.pdb` |
| DNA input prepared | ✅ Done | `structures/dna_30bp.pdb` exists and is used as input |
| Coarse-graining | ✅ Done | delivered branch uses Martini 2 fallback protein + DNA |
| Merge | ✅ Done | `cg/complex_cg.pdb` |
| Local water + ions environment | ✅ Done | `cg/solvated_inspection_system.pdb` |
| HPC handoff bundle | ✅ Done | `cg/handoff_m2_mg_proxy/` and packaged tarball |
| Visualization | ✅ Done | static PNGs + `notebooks/visualize.ipynb` |

## Actual Ask

The practical request was:
- prepare the local starting environment
- include Twinkle, dsDNA, water, and salt
- hand off something usable for later HPC work

That ask is satisfied by:
- `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`
- `cg/handoff_m2_mg_proxy/`

## Delivered Scope

This repo currently delivers:
- a merged Twinkle + dsDNA CG complex
- a local solvated environment for inspection
- a self-contained HPC handoff bundle
- visuals that can be shown directly

## Explicit Non-Goals

This repo is **not** currently delivering:
- a solved Martini 3 dsDNA topology path
- a finished MD trajectory
- a claim that the `MG2` proxy is an official Martini Mg parameter

## Key Artifacts

Core:
- `cg/complex_cg.pdb`
- `cg/solvated_inspection_system.pdb`
- `cg/handoff_m2_mg_proxy/system.top`

Delivery:
- `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`

Visualization:
- `deliverables/twinkle_dsDNA_complex_overview.png`
- `deliverables/twinkle_dsDNA_environment_zoom.png`
- `notebooks/visualize.ipynb`

## Known Tradeoffs

- Martini 3 dsDNA is still upstream-blocked in the local `martinize2/vermouth` path.
- The delivered branch therefore uses Martini 2 fallback components.
- The final handoff bundle uses a documented `MG2` proxy that reuses the official Martini 2 divalent `Qd` +2 behavior.
