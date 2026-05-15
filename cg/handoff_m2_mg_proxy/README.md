# Martini 2 fallback HPC handoff

This directory is the delivered handoff bundle for the local environment request.

Contents:
- `system.top`
- `solvated_m2_mg_proxy.pdb`
- `mg_proxy.itp`
- `em.mdp`
- `equil.mdp`
- `mdrun.mdp`
- official Martini 2 support files bundled for handoff

Scope:
- this is the delivered Martini 2 rescue branch
- this is meant for later HPC-side GROMACS preparation
- this is not a claim of a solved Martini 3 dsDNA workflow

Model tradeoff:
- the bundle uses a documented local `MG2` proxy because the official Martini 2 ion file available here does not define Mg
- the `37` requested divalent ions are therefore represented by that local proxy
