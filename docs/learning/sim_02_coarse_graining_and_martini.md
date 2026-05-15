# Simulation Part 2: Coarse-Graining and Martini

This section explains the specific modeling style used in the repo.

## What Coarse-Graining Means

In an all-atom model, every atom is represented explicitly.

In a coarse-grained model, several atoms are grouped into one larger interaction site, often called a **bead**.

Why do this?

- fewer particles
- simpler representation
- lower computational cost
- easier large-scale setup and visualization

The cost is reduced detail.

## Why The Images Look Like Clouds Of Dots

The images in this repo do not show every atom.

Instead:
- blue dots represent coarse-grained Twinkle beads
- orange dots represent coarse-grained dsDNA beads
- other colored dots represent coarse-grained solvent or ion beads

That is why the figures look abstract compared with textbook ribbon cartoons or atomic stick models.

## What Martini Is

**Martini** is a well-known family of coarse-grained force fields.

You do not need to know the full literature history to understand this repo. The key beginner point is:

- Martini provides a coarse-grained way to represent biomolecules and their interactions

## Why Martini 2 And Martini 3 Both Appear In This Repo

This is one of the most important practical details.

### The ideal target

The original goal was a Martini 3-style setup for the delivered system.

### The practical blocker

The local toolchain did not provide a clean working dsDNA path for that target in this repo.

### The delivered solution

The repo therefore uses a **Martini 2 rescue branch** for the final practical handoff.

That means the delivery favors:
- completing the local environment honestly
- keeping the files usable
- documenting the limitation clearly

instead of pretending the blocked path was solved.

## What “Fallback” Means Here

Fallback does **not** mean random or fake.

Here it means:
- the originally intended path failed for a specific technical reason
- a supported alternative path was used to complete the practical deliverable

So the delivered branch is a **pragmatic engineering solution**.

## Why Magnesium Is Called A Proxy In This Repo

The final handoff uses a documented `MG2` proxy.

For a beginner, the important point is:
- the repo is preserving the requested divalent-ion idea in the handoff
- but it is also being honest that this is a proxy choice, not an official solved Mg model from the local available Martini 2 files

## The Important Beginner Takeaway

The final delivered system is best understood as:

- coarse-grained
- Martini-based
- practically usable
- clearly documented
- not pretending to be more final or more perfect than it really is
