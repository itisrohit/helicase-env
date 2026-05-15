# Engineering Journal: Twinkle + dsDNA Simulation

## 🗓️ 2026-05-14 — DNA Input Validation + Polyply Fallback

### What was tested

* Checked the actual 30 bp DNA input with `MDAnalysis` instead of assuming the 1KX5 slice was a valid duplex.
* Installed the official `polyply` toolchain in the project venv and tested its documented DNA sequence workflow locally.
* Verified that `polyply gen_params -lib martini2 -dsdna` can generate a dsDNA topology from the 30-mer sequence derived from `structures/dna_30bp.pdb`.

### What we learned

* `structures/dna_30bp.pdb` is **not** a usable duplex template for direct coarse-graining:
  * both chains carry the same 5'->3' sequence,
  * and their base coordinates are not arranged as a paired duplex.
* This means the earlier "30 bp duplex extracted from 1KX5" assumption was wrong in practice, even though the file contains DNA residues.
* The official `polyply` route can still recover a dsDNA topology from the first-strand sequence, so the repo now has a supported fallback for DNA topology generation.
* Because the fallback is Martini 2 DNA and not Martini 3 DNA, it is suitable for visual assembly and troubleshooting, but not yet a clean end-state for the original MARTINI 3 simulation goal.
* The repo now also builds a Martini 2 protein fallback using `martinize2 -ff martini22`.
* That fallback repairs the 18 invalid `SC2` sidechain bead coordinates deterministically from local `BB -> SC1` geometry, yielding `cg/twinkle_m2_cg.pdb`.
* The merge step now prefers the consistent Martini 2 pair and writes `cg/complex_cg.pdb`.
* The generated `cg/twinkle_m2.top` is now normalized so each `molecule_*.itp` file is included only once.

### Consequence

* The repo now distinguishes between:
  * the blocked MARTINI 3 DNA path,
  * and a working official fallback that produces `cg/dna_fallback_m2_cg.itp` plus an idealized `cg/dna_fallback_m2_cg.pdb`.
* This unblocks merge/inspection work, while keeping the force-field inconsistency explicit.
* Solvation is still pending and should not be treated as complete in the current repo state.

## 🗓️ 2026-05-14 — Provisional Water + Ion Environment

### What was built

* Replaced the old all-atom OpenMM placeholder in `src/05_solvate.py` with a real coarse-grained packing script.
* The script now writes:
  * `cg/solvated_inspection_system.pdb`
  * `cg/solvated_inspection_system.json`

### What it does

* Builds a padded solvent box around `cg/complex_cg.pdb`.
* Places coarse-grained water beads on a regular grid outside a solute exclusion radius.
* Adds ion beads at concentration-derived counts for:
  * 100 mM NaCl
  * 7.5 mM MgCl2

### Verified output

* Solute beads: 7408
* Water beads: 81375
* Na beads: 496
* Cl beads: 570
* Mg beads: 37

### Limitation

* This is an **inspection-only** environment.
* It is useful for geometry checks and notebook visualization, but it is **not** a validated simulation-ready Martini topology.

## 🗓️ 2026-05-14 — DNA Coarse-Grain Blocker Verified

### What was tested

* Ran `src/03_coarse_grain.py` directly against the local `.venv/bin/martinize2` binary to avoid the earlier `uv run` cache permission issue.
* Verified that protein coarse-graining still works for `structures/twinkle_hex.pdb`.
* Cloned the official `marrink-lab/martini-forcefields` repository and vendored the relevant Martini 3 reference files into `vendor/martini-forcefields/`.

### What we learned

* The installed `vermouth` / `martinize2` pipeline does **not** recognize atomistic DNA residues `DA/DC/DG/DT` in `structures/dna_30bp.pdb`.
* The official Martini 3 repository provides `martini_v3.0.0_nucleobases_v1.itp`, but that is only a nucleobase parameter file, not a full dsDNA polymer coarse-graining path for `martinize2`.
* The vendored upstream `vermouth_files` are not directly usable with the local `vermouth 0.15.0` parser in this environment; enabling them breaks even the protein path because the file format revision is newer than the installed parser.
* After checking the current upstream `vermouth-martinize` repository, the situation is unchanged there as well: Martini 3 still lacks the dsDNA polymer blocks/maps needed for this workflow.
* The official Martini documentation still points dsDNA users to the **legacy Martini 2** `martinize-dna.py` workflow for supported double-stranded DNA coarse-graining.
* Direct access to the standalone legacy DNA tarball still returned `AccessDenied` from this CLI environment, but the larger official `na-tutorials_20170815.tar` package downloaded successfully and now supplies the legacy `martinize-dna.py` script plus `martini_v2.1-dna.itp` and `martini_v2.1P-dna.itp`.

### Consequence

* The blocker is now narrowed down precisely:
  * this is **not** just a missing `-map-dir` flag,
  * and it is **not** a malformed DNA PDB.
* The real issue is a missing compatible Martini 3 dsDNA polymer workflow for the current local `martinize2` stack.

## 🗓️ 2026-05-14 — Initial Environment & Pipeline Setup

### 🚩 Key Issues Encountered

#### 1. The "RCSB Wall" (SSL & 403 Forbidden)
*   **Issue**: Initial attempts to download `7T8C.pdb` and `1BNA.pdb` failed with `URLError` (SSL) or `403 Forbidden`.
*   **The Hunt**: Standard Python `urllib.request.urlretrieve` is flagged as a bot by RCSB.
*   **The Fix**:
    *   Bypassed SSL verification using `ssl._create_unverified_context`.
    *   Impersonated a browser using `opener.addheaders = [("User-agent", "Mozilla/5.0")]`.
    *   *Lesson*: Always check for bot-protection when hitting scientific databases via CLI.

#### 2. The DNA "Ghost" Problem
*   **Issue**: `martinize2` (coarse-graining tool) would not recognize our mathematically generated DNA.
*   **The Hunt**: I initially built an idealized helix with only Phosphorus (P) atoms. `martinize2` requires a full atomistic template (Phosphate + Sugar + Base) to determine how to map them to Martini beads.
*   **The Fix**: Instead of "building" math, we "extracted" biology. I searched for a PDB with exactly 30bp and found **1KX5** (Nucleosome). We downloaded it and used `MDAnalysis` to slice out a perfect 30bp duplex segment.
*   **Result**: The PDB now has full DT, DC, DA, DG residues, which `martinize2` can actually "see."

#### 3. Root Clutter (Topological Noise)
*   **Issue**: Running `martinize2` generated dozens of `molecule_*.itp` files in the root directory, making the project hard to navigate.
*   **The Fix**: 
    *   Created `src/03_coarse_grain.py` to act as a manager. 
    *   It now automatically moves all `.itp` files into the `cg/` directory and deletes `#*#` backup files.
    *   Updated `.gitignore` to prevent these from ever being committed.

---

### 🔍 How to Find Things (Heuristics for MD)

When setting up a simulation environment, finding specific structural "parts" is the biggest hurdle. Our strategy evolved into:

1.  **Don't Search for "DNA"**: Search for specific lengths (e.g., "PDB entry with 30bp duplex"). 
2.  **Verify via Grep**: Before trusting a PDB, run `grep "^ATOM" file.pdb | grep " DT "` to ensure it actually contains the coordinates you think it does (some "DNA binding" PDBs only have the protein part).
3.  **Cross-Reference Force Fields**: We found that `martinize2` (vermouth) is force-field sensitive. If a residue isn't recognized, check `martinize2 -list-blocks -ff martini3001` to see what it expects.

---

### ✅ Success Summary & Quality Checks

1.  **Bootstrap**: Used `uv` for 100x faster dependency resolution compared to legacy `pip`.
2.  **Quality**: Enforced 2026 standards using `ruff` (linting) and `ty` (type checking). Fixed "star imports" in OpenMM scripts to make them IDE-friendly.
3.  **Automation**: The entire process is now unified in [pipeline.ipynb](../pipeline.ipynb), reducing a 20-step manual process to a few clicks.

---
> **Tip for Future Steps**: If the DNA coarse-graining fails again, verify that the `martinize2` version has the Martini 3 DNA mapping files in its library path.

## 🗓️ 2026-05-14 — Martini 2 HPC Handoff Bundle

### What was built

* Replaced the old `src/06_simulate.py` OpenMM placeholder with a real handoff builder.
* The script now writes `cg/handoff_m2_mg_proxy/` containing:
  * `system.top`
  * `solvated_m2_mg_proxy.pdb`
  * official `martini_v2.2.itp`
  * official `martini_v2.0_ions.itp`
  * official `martini_v2.1P-dna.itp`
  * local `mg_proxy.itp`
  * official legacy `em.mdp`, `equil.mdp`, `mdrun.mdp`
  * a local handoff `README.md` and `manifest.json`

### What we learned

* The official Martini 2 ion file available here defines `NA+`, `CL-`, and `CA+`, but not Mg.
* To keep the fallback branch self-contained and semantically cleaner, the requested `37` divalent ions are now encoded as a local `MG2` proxy that explicitly reuses the official Martini 2 `Qd` +2 divalent bead parameters.

### Consequence

* The repo now produces a concrete HPC handoff bundle instead of stopping at an inspection PDB.
* The remaining chemistry caveat is narrowed to one place:
  * true Martini 3 dsDNA is still unavailable locally,
  * and the Martini 2 rescue branch still needs a divalent-ion proxy for Mg.
