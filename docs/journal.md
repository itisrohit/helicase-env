# Engineering Journal: Twinkle + dsDNA Simulation

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
