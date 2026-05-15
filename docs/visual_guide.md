# Visual Guide

This note explains the three delivery images in simple terms.

## Background

The project builds a coarse-grained model of:
- the **Twinkle helicase** protein complex
- a **30 base-pair double-stranded DNA (dsDNA)** segment
- a surrounding **local solvent + ion environment**

Twinkle is a ring-shaped helicase. In plain language, it is a protein assembly that forms a central channel, and DNA is expected to pass through that channel during function.

In these images:
- the **blue cloud** is the Twinkle protein
- the **orange vertical structure** is the dsDNA
- the **red / green / purple points** are ions in the solvent environment
- the **light gray points** are a light subsample of water beads

These are **coarse-grained** views, not all-atom views. That means each point represents a grouped interaction site rather than every individual atom. The goal of these figures is to show the overall geometry clearly.

## Why There Are Two Panels In Each Figure

Each image shows the same system from two directions:
- **Side View (X-Z)** on the left
- **Front View (Y-Z)** on the right

This matters because a 3D structure can look misleading from only one angle. Showing two perpendicular views makes it easier to confirm where the DNA sits relative to the protein and solvent box.

## Twinkle + dsDNA Merged Complex

File:
- `deliverables/twinkle_dsDNA_complex_overview.png`

Title:
- `Twinkle + dsDNA Merged Complex`

### What this image shows

This is the simplest structural view. It shows only:
- the Twinkle complex
- the dsDNA

It does **not** show the solvent environment yet.

### How to read it

- The **blue beads** form the coarse-grained protein body of Twinkle.
- The **orange beads** form the DNA duplex.
- The DNA is placed approximately through the middle of the Twinkle assembly.

### What a novice should notice

1. The protein is much wider than the DNA.
2. The DNA is aligned roughly along the vertical direction in the image.
3. The DNA passes through the middle region of the protein rather than sitting completely outside it.
4. The two panels confirm this placement from two different angles.

### Why this image matters

This is the key geometry check for the merged complex. Before adding solvent and ions, the first thing to confirm is:
- do we have both components present?
- is the DNA roughly centered through the Twinkle ring region?

That is what this image is meant to communicate.

## Twinkle + dsDNA Local Solvated Environment

File:
- `deliverables/twinkle_dsDNA_environment_overview.png`

Title:
- `Twinkle + dsDNA Local Solvated Environment`

### What this image shows

This figure adds the **local environment** around the merged complex.

It includes:
- Twinkle protein
- dsDNA
- a local box of coarse-grained water
- sodium-like ions
- chloride-like ions
- magnesium-proxy ions

### Color meaning

- **Blue**: Twinkle
- **Orange**: dsDNA
- **Red**: `NA`
- **Green**: `CL`
- **Purple**: `MG`
- **Light gray**: water subsample
- **Black X**: approximate solute center
- **Dashed rectangle**: approximate solvent box boundary in that projection

### How to read it

- The dashed outline marks the overall local environment box.
- The protein and DNA sit near the center of that box.
- Water and ions fill the surrounding space rather than overlapping the solute core.
- Only a light subset of water beads is shown so the picture remains readable.

### What a novice should notice

1. The environment extends well beyond the protein and DNA.
2. The solute is not pressed against the box edge.
3. Ions are distributed around the system instead of being stacked only in one spot.
4. The DNA remains centered when solvent and ions are included.

### Why this image matters

This is the main “environment prepared” figure.

It answers:
- was solvent added?
- were ions added?
- is the solute sitting inside a sensible local box?

It is not meant to prove physical correctness of a full production simulation by itself. It is meant to show that the local starting environment exists and is geometrically reasonable.

## Twinkle + dsDNA Solute Neighborhood

File:
- `deliverables/twinkle_dsDNA_environment_zoom.png`

Title:
- `Twinkle + dsDNA Solute Neighborhood`

### What this image shows

This is a closer view of the region immediately around the protein and DNA.

Instead of showing the full solvent box, it focuses on the **solute neighborhood**:
- Twinkle
- dsDNA
- nearby water
- nearby ions

### Why this image exists

The full environment overview is useful, but it can look busy. A zoomed view makes it easier to see the local relationship between:
- the DNA
- the protein body
- the nearest solvent and ions

### What a novice should notice

1. The DNA remains visibly inside the central region of the protein assembly.
2. Nearby water and ions surround the complex rather than replacing it.
3. The solvent neighborhood is local and continuous around the solute.
4. The two views again confirm that the visual impression is not just an artifact of one camera angle.

### Why this image matters

This is usually the easiest image to show first during a presentation because it is clearer than the full-box view while still showing that the complex is solvated.

## What These Three Images Mean Together

Taken together, the three figures tell a simple story:

1. **Twinkle + dsDNA Merged Complex** shows that the protein and DNA were successfully merged into one complex.
2. **Twinkle + dsDNA Local Solvated Environment** shows that a local water-and-ion environment was built around that complex.
3. **Twinkle + dsDNA Solute Neighborhood** gives a closer inspection view of the solvated complex so the local geometry is easier to read.

## Important Scope Note

These figures show a **prepared local environment and handoff geometry**.

They do **not** by themselves prove:
- a finished production simulation
- a solved Martini 3 dsDNA workflow
- experimentally validated dynamics

They are best understood as:
- structure-preparation figures
- environment-preparation figures
- handoff-quality inspection figures

## Short Version For Presentation

If you need to explain the images quickly:

- **Twinkle + dsDNA Merged Complex**: merged Twinkle + dsDNA complex
- **Twinkle + dsDNA Local Solvated Environment**: full local solvated environment with ions
- **Twinkle + dsDNA Solute Neighborhood**: zoomed view of the solvated complex neighborhood

If you need one sentence:

These figures show that the Twinkle helicase and dsDNA were assembled into one coarse-grained complex, placed inside a local solvent-and-ion environment, and checked visually from multiple angles.
