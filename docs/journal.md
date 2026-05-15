# Engineering Journal

## Summary

This repo ended up as a **delivery-first Martini 2 rescue branch** for the requested local environment handoff.

The main engineering decisions were:
- keep the local deliverable focused on the actual ask
- stop pretending the blocked Martini 3 dsDNA path was solved
- build a coherent fallback branch instead

## Main Findings

### 1. DNA input reality

- `structures/dna_30bp.pdb` is not a chemically valid duplex template for direct CG mapping
- both strands carry the same 5'->3' sequence
- the delivered branch therefore uses sequence-driven Martini 2 DNA fallback generation

### 2. Martini 3 blocker

- local `martinize2/vermouth` does not provide a usable Martini 3 dsDNA polymer workflow here
- official Martini 3 nucleic-acid downloads expose nucleobase parameters, not a complete dsDNA build path for this repo

### 3. Delivered fallback branch

- protein: Martini 2 fallback coarse-graining
- DNA: Martini 2 fallback topology and coordinates
- merged complex: `cg/complex_cg.pdb`
- local environment: `cg/solvated_inspection_system.pdb`
- handoff bundle: `cg/handoff_m2_mg_proxy/`

### 4. Mg handling

- official Martini 2 ion files available here define `NA+`, `CL-`, and `CA+`, but not Mg
- the delivered handoff therefore uses a documented local `MG2` proxy that reuses the official divalent `Qd` +2 behavior

### 5. Visualization

Available now:
- `deliverables/twinkle_dsDNA_complex_overview.png`
- `deliverables/twinkle_dsDNA_environment_overview.png`
- `deliverables/twinkle_dsDNA_environment_zoom.png`
- `notebooks/visualize.ipynb`

## Delivered End State

The cleanest handoff statement is:

- the requested local environment is prepared
- the packaged artifact is `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`
- the repo does not claim a solved Martini 3 dsDNA production workflow
