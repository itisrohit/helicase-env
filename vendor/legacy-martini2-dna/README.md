Official fallback location for the Martini 2 dsDNA tooling.

Why this exists:
- Current upstream `vermouth/martinize2` does not provide a complete Martini 3 dsDNA polymer coarse-graining path in this repo's environment.
- The official Martini legacy DNA tutorial still documents dsDNA setup through `martinize-dna.py`.

Expected local contents:
- `martinize-dna.py`
- `martini_v2.1-dna.itp` or equivalent DNA force-field files from the same package

Official sources:
- Martini 2 nucleic-acid downloads:
  https://cgmartini.nl/docs/downloads/force-field-parameters/martini2/nucleic_acids.html
- Legacy DNA tutorial:
  https://cgmartini.nl/docs/tutorials/Legacy/martini2/dna.html

Notes:
- The standalone DNA tarball links on the public docs currently point to S3 objects that were not fetchable from this CLI environment due `AccessDenied`.
- This repo now bootstraps `martinize-dna.py`, `martini_v2.1-dna.itp`, and `martini_v2.1P-dna.itp` from the larger official `na-tutorials_20170815.tar` archive when available.
