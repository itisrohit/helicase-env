# Big Picture

This repo is about preparing a **starting model** for a biological system, not about reporting final scientific results from a completed simulation.

The system has three main pieces:

1. a protein machine called **Twinkle**
2. a short piece of **double-stranded DNA**
3. a surrounding **water + salt environment**

## The Core Idea

In cells, proteins often interact with DNA physically. Some proteins bind DNA, some cut it, some copy it, and some help open or move along it.

Twinkle is one of those DNA-related protein machines. It forms a ring-like assembly, and the DNA is expected to pass through its central region.

That means the modeling problem is not just:
- build a protein
- build a DNA strand

It is also:
- place the DNA correctly relative to the protein
- surround both with a reasonable solvent environment
- prepare files that can be handed off for later simulation work

## What This Repo Produces

At a high level, the repo produces:

- a merged Twinkle + dsDNA coarse-grained complex
- a local solvated environment around that complex
- a simulation handoff bundle
- a set of visuals for inspection and presentation

## What “Coarse-Grained” Means Here

Molecular structures can be represented at different levels of detail.

- **All-atom** means every atom is represented explicitly.
- **Coarse-grained** means multiple atoms are grouped into a smaller number of interaction sites or “beads.”

This repo uses a coarse-grained approach because it is lighter and more practical for the stated delivery goal.

## What Makes This Repo Slightly Tricky

The original intended path was a **Martini 3** coarse-grained setup for both protein and DNA.

That ideal path did not work cleanly here for DNA. So the final delivery became a **practical rescue path**:

- deliver the local environment honestly
- keep the geometry and workflow usable
- document the tradeoffs clearly

That is why this repo is both:
- a scientific preparation repo
- an engineering compromise repo

## The Main Mental Model

You should think of the repo as a pipeline with four layers:

1. **Biology layer**
   What system are we trying to model?

2. **Representation layer**
   How are we representing protein, DNA, water, and ions?

3. **Workflow layer**
   What sequence of scripts builds the deliverable?

4. **Delivery layer**
   What files can be shown or handed off?

The rest of the learning material explains those layers one by one.
