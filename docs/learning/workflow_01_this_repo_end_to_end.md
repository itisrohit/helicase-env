# Workflow Part 1: This Repo End To End

This section ties the biology and code together.

## The One-Command Workflow

The main command is:

```bash
uv sync --locked
uv run --locked twinkle-delivery
```

That is the easiest way to rebuild the delivered local environment.

## What Happens In Order

### Step 1: DNA input validation

`src/02_build_dna.py` checks the provided DNA input file and confirms the repo is using that input instead of silently generating a different one.

### Step 2: Coarse-graining

`src/03_coarse_grain.py`:
- coarse-grains the protein
- checks the DNA input situation
- uses the documented fallback path when needed

This is where the repo’s practical compromise becomes visible.

### Step 3: Merge

`src/04_merge.py` places the protein and DNA together into:

- `cg/complex_cg.pdb`

This is the core merged structural view.

### Step 4: Solvation and ions

`src/05_solvate.py` creates:

- `cg/solvated_inspection_system.pdb`
- `cg/solvated_inspection_system.json`

This adds the local water and ion environment around the merged complex.

### Step 5: Handoff packaging

`src/06_simulate.py` creates:

- `cg/handoff_m2_mg_proxy/`

This is the practical handoff bundle for later HPC-side work.

### Step 6: Rendering

`src/07_render_delivery_views.py` creates:

- `deliverables/twinkle_dsDNA_complex_overview.png`
- `deliverables/twinkle_dsDNA_environment_overview.png`
- `deliverables/twinkle_dsDNA_environment_zoom.png`

These are the communication-ready visuals.

## How The Outputs Relate To Each Other

Think of the outputs as a ladder:

1. **Input structures**
   Starting molecular data

2. **Coarse-grained pieces**
   Protein and DNA represented in bead form

3. **Merged complex**
   Protein and DNA placed together

4. **Solvated inspection system**
   The merged complex inside local water and ions

5. **Handoff bundle**
   A packaged set of files for the next computational stage

6. **Visual deliverables**
   Human-readable images and notebook inspection

## Why The Workflow Is Honest About Tradeoffs

This repo tries to be explicit about what happened.

It does not say:
- “everything is perfect”
- “the Martini 3 DNA path is solved”

Instead it says:
- here is the deliverable
- here is the fallback path that made it possible
- here are the exact outputs

That is good scientific engineering practice.

## The Important Beginner Takeaway

The workflow is not random scripting. It is a chain where each step answers a specific question:

- what is the input?
- how is it represented?
- how are the parts combined?
- what environment surrounds them?
- what files are handed off?
- what visuals explain the result?
