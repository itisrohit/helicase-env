# Biology Part 3: How Biological Structure Is Represented

This section connects the science to the files.

A beginner often understands the words:
- DNA
- protein
- ring

but still does not understand how those ideas become coordinates in a computer.

That is the gap this note fills.

## Biological Molecules Have Shape

The central scientific fact behind this repo is that biological molecules are not just chemical formulas. They have 3D shape.

That shape matters because:
- proteins function through their geometry
- DNA interactions depend on orientation and access
- ring-like assemblies only make sense if the central channel is represented correctly

For this repo, the scientific problem is therefore partly geometric:
- where is the protein?
- where is the DNA?
- how are they oriented relative to one another?

## What A Structure File Represents

A structure file is a list of particles in 3D space.

At higher resolution, those particles are atoms.
At coarse-grained resolution, those particles are beads.

The important idea is:
- a structure file is a snapshot of arrangement
- it tells you what is where

It does not fully explain:
- what forces are active
- what connectivity rules are used
- what simulation model is assumed

That is why structure alone is not enough for simulation.

## Why PDB Files Appear So Often

The repo uses PDB-format files because they are a standard way to store biomolecular coordinates.

For a beginner, a PDB file can be thought of as:
- a table of named particles
- grouped into residues and chains
- with 3D coordinates

Examples in this repo:
- atomistic-style input structures in `structures/`
- coarse-grained coordinate outputs in `cg/`

## What Chains And Residues Mean

Two common words in structural biology are:

### Chain

A chain is one continuous molecular piece in the structure file.

For proteins, a chain often corresponds to one subunit.
For DNA, a chain often corresponds to one strand.

### Residue

A residue is one repeating unit within a biomolecule.

Examples:
- one amino acid in a protein
- one nucleotide in DNA

So when the repo talks about six protein chains or two DNA strands, it is using the structure-file representation of the biological assembly.

## Why The Twinkle Hexamer Matters Structurally

The repo uses a six-chain Twinkle assembly.

That means the biological protein complex is represented as:
- six structural subunits
- arranged together in a ring-like form

This matters because the scientific point is not simply “Twinkle exists.” The point is:
- what does the assembled ring-like geometry look like?
- can DNA be placed through its center?

## Why A Bad DNA Input Is A Scientific Problem

If a DNA file is structurally wrong, the issue is not just a scripting inconvenience.

It becomes a scientific representation problem.

For example, if both DNA strands carry the same 5'->3' sequence in a way that does not represent a proper duplex, then the file is not a clean physical template for direct mapping.

That is why the repo had to treat the DNA issue carefully:
- not because the filename was wrong
- but because the biological structure representation was not trustworthy enough for direct use

## The Important Beginner Takeaway

The core scientific objects in this repo are:
- molecular shape
- molecular identity
- molecular arrangement

The files are not random technical artifacts. They are the computer representation of those scientific ideas.
