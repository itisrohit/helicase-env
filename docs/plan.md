# Twinkle + dsDNA — Complete Plan 
# Including: Message Decoding, Visualization, Modern Tooling

## Project Status (2026-05-14)

| Step | Task | Status | Note |
| :--- | :--- | :--- | :--- |
| 0 | Bootstrap Environment | ✅ Done | uv, ruff, ty, vermouth installed |
| 1 | Get Twinkle structure | ✅ Done | 7T8C.pdb cleaned to twinkle_hex.pdb |
| 2 | Build dsDNA (30 bp) | ⏳ Pending | Awaiting `dna_30bp.pdb` from user |
| 3 | Coarse-grain | 🔄 Partial | Automated via `src/03_coarse_grain.py` |
| 4 | Merge + position | ⏳ Pending | Requires Step 2 & 3 |
| 5 | Solvate + ions | ⏳ Pending | Goal: `solvated_system.pdb` |
| 6 | Simulate | ⏳ Pending | HPC handoff |

---

## What she actually asked (decoded)

Her message had two layers:

**Layer 1 — "the story once we meet"**
She has scientific context (why Twinkle, what research question) that she
will explain in person. Don't read into it further — set it aside.

**Layer 2 — the actual task**
```
"make an environment with water having Twinkle protein and dsDNA strand,
add salt, you can start with what I suggested on your laptop"
```

She is splitting the work deliberately:
- YOU:  prepare the simulation system (water box + protein + DNA + ions) locally
- HER / CLUSTER: run the actual MD simulation on HPC later

"Environment" = the starting configuration file (a .gro or .pdb with everything
placed correctly in a periodic water box). This is something you CAN do on any
laptop — it takes minutes, not days. It does not require running a single
simulation step.

So the deliverable she wants right now is:
  → a solvated, ionized PDB/GRO file with Twinkle + dsDNA + TIP3P water
     + 100 mM NaCl + 7.5 mM MgCl2, ready to simulate.

---

## Do we need visualization? Yes, for two things

### 1. Before simulation — verify the system is correct
You need to SEE that the protein is inside the water box, the DNA is
positioned near the protein channel, ions are distributed. If you skip this
you may waste hours simulating garbage.

### 2. After simulation — analyze what happened
RMSD plots, ion distributions, ring conformations, DNA threading.

---

## Visualization tools (2026, all free, laptop-native)

| Tool | Use | Install |
|---|---|---|
| **NGLview** | Interactive 3D in Jupyter notebook. Best for trajectory playback | `uv add nglview` |
| **PyMOL 3.1** (open-source) | Gold standard for pretty renders, structure inspection | `conda install pymol-bundle` or pymol.org |
| **matplotlib** | 2D plots — RMSD, energy, ion density over time | `uv add matplotlib` |
| **MDAnalysis** | Trajectory analysis + feeds directly into NGLview | `uv add mdanalysis` |

**Recommended workflow:**
- Use **NGLview inside Jupyter** for day-to-day trajectory viewing
- Use **PyMOL** for final renders / screenshots

NGLview is a Jupyter widget that provides interactive molecular graphics
and directly integrates with MDAnalysis — view the trajectory frame by frame
inside your notebook with no external tools.

### NGLview quick start

```python
# In Jupyter notebook
import nglview as nv
import MDAnalysis as mda

# View static structure
view = nv.show_file("structures/twinkle_hex.pdb")
view  # renders interactive 3D in notebook

# View trajectory after simulation
u = mda.Universe("cg/complex_cg.pdb", "output/traj.dcd")
view = nv.show_mdanalysis(u)
view.add_representation("cartoon", selection="protein")
view.add_representation("licorice", selection="nucleic")
view  # play/pause the MD trajectory
```

---

## Full project structure

```
twinkle-sim/
├── pyproject.toml         ← single config for everything
├── uv.lock                ← exact pinned deps (commit this)
├── .python-version        ← "3.12"
├── README.md
│
├── structures/            ← raw inputs
│   ├── 7T8C.pdb           ← Twinkle cryo-EM download
│   ├── twinkle_hex.pdb    ← cleaned 6-chain hexamer
│   └── dna_30bp.pdb       ← B-form dsDNA
│
├── cg/                    ← coarse-grained files
│   ├── twinkle_cg.pdb
│   ├── twinkle_cg.itp
│   ├── dna_cg.pdb
│   ├── complex_cg.pdb     ← merged protein + dna
│   └── system.top         ← MARTINI topology master file
│
├── src/
│   ├── 01_clean.py        ← extract 6 chains from 7T8C
│   ├── 02_build_dna.py    ← build 30bp B-form dsDNA
│   ├── 03_coarse_grain.sh ← martinize2 commands
│   ├── 04_merge.py        ← combine protein + DNA, position DNA in channel
│   ├── 05_solvate.py      ← add water + ions (THE ENVIRONMENT)
│   ├── 06_simulate.py     ← OpenMM production run
│   └── 07_analyze.py      ← RMSD, ion density, plots
│
├── notebooks/
│   └── visualize.ipynb    ← NGLview trajectory viewer
│
└── output/
    ├── traj.dcd
    ├── energies.csv
    └── rmsd.png
```

---

## pyproject.toml (complete)

```toml
[project]
name = "twinkle-sim"
version = "0.1.0"
description = "CG-MD of Twinkle helicase + dsDNA — laptop-friendly"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "openmm>=8.0",
  "mdanalysis>=2.7",
  "numpy>=2.0",
  "matplotlib>=3.9",
  "biopython>=1.84",
  "nglview>=3.1",
  "jupyter>=1.1",
  "ipywidgets>=8.0",
]

[dependency-groups]
dev = [
  "ruff>=0.4",
  "ty>=0.0.1",
  "pytest>=8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP"]

[tool.ruff.format]
quote-style = "double"
```

---

## Step-by-step pipeline

### Step 0 — Bootstrap (once)

```bash
# Install uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init twinkle-sim && cd twinkle-sim

# Add all deps at once
uv add openmm mdanalysis numpy matplotlib biopython nglview jupyter ipywidgets
uv add --dev ruff ty pytest

# Install martinize2 separately (not on PyPI via uv yet)
pip install martinize2
```

---

### Step 1 — Get Twinkle structure

```python
# src/01_clean.py
import urllib.request
from pathlib import Path
from Bio import PDB

Path("structures").mkdir(exist_ok=True)

# Download
urllib.request.urlretrieve(
    "https://files.rcsb.org/download/7T8C.pdb",
    "structures/7T8C.pdb"
)

# Extract 6 chains (A-F) = hexamer, remove HETATM
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("twinkle", "structures/7T8C.pdb")

class HexamerSelect(PDB.Select):
    def accept_chain(self, chain):
        return chain.id in list("ABCDEF")
    def accept_residue(self, res):
        return res.id[0] == " "  # exclude HETATM

io = PDB.PDBIO()
io.set_structure(structure)
io.save("structures/twinkle_hex.pdb", HexamerSelect())
print("twinkle_hex.pdb saved.")
```

```bash
uv run python src/01_clean.py
```

---

### Step 2 — Build dsDNA (30 bp)

Use the web tool — no install needed:
1. Go to http://web.x3dna.org
2. Select "Rebuild" → B-DNA → 30 bp → any sequence → Download PDB
3. Save as `structures/dna_30bp.pdb`

---

### Step 3 — Coarse-grain

```bash
# src/03_coarse_grain.sh

# Protein → MARTINI 3 CG
martinize2 \
  -f structures/twinkle_hex.pdb \
  -o cg/twinkle_cg.pdb \
  -x cg/twinkle_cg.itp \
  -ff martini3001 \
  -elastic -ef 500 -el 0.5 -eu 0.9

# DNA → MARTINI CG (download martinize_dna.py from cgmartini.nl)
python martinize_dna.py \
  -f structures/dna_30bp.pdb \
  -o cg/dna_cg.pdb \
  -x cg/dna_cg.itp
```

---

### Step 4 — Merge + position

```python
# src/04_merge.py
# Place DNA through center of Twinkle ring (along Z-axis)
import MDAnalysis as mda
import numpy as np
from pathlib import Path

Path("cg").mkdir(exist_ok=True)

protein = mda.Universe("cg/twinkle_cg.pdb")
dna = mda.Universe("cg/dna_cg.pdb")

# Center protein at origin
protein.atoms.translate(-protein.atoms.center_of_mass())

# Center DNA, align along Z through ring channel
dna.atoms.translate(-dna.atoms.center_of_mass())

merged = mda.Merge(protein.atoms, dna.atoms)
merged.atoms.write("cg/complex_cg.pdb")
print("complex_cg.pdb saved.")
```

---

### Step 5 — Solvate + add ions (THE ENVIRONMENT she asked for)

This is what she wants you to build on your laptop.
The output of this step is a fully solvated, ionized system ready to run.

```python
# src/05_solvate.py
from openmm.app import *
from openmm import *
from openmm.unit import *

# --- Load CG complex ---
pdb = PDBFile("cg/complex_cg.pdb")
modeller = Modeller(pdb.topology, pdb.positions)

# --- Add TIP3P water box (2.0 nm padding) ---
modeller.addSolvent(
    forcefield=ForceField("charmm36.xml", "charmm36/water.xml"),
    model="tip3p",
    padding=2.0 * nanometer,
)

# --- Ion counts from paper buffer (PMC7186178) ---
# 100 mM NaCl + 7.5 mM MgCl2 in HEPES pH 7.5
# Box ~= 20nm x 20nm x 20nm => 8000 nm3 = 8e-24 L
AVOGADRO = 6.022e23
box_vol_L = 8e-24

na  = int(0.100 * AVOGADRO * box_vol_L)   # ~481 Na+
cl  = int(0.100 * AVOGADRO * box_vol_L)   # ~481 Cl- (NaCl)
mg  = int(0.0075 * AVOGADRO * box_vol_L)  # ~36 Mg2+
cl += mg * 2                               # +72 Cl- for MgCl2

# neutralize net protein charge
modeller.addSolvent(
    forcefield=ForceField("charmm36.xml"),
    positiveIon="Na+",
    negativeIon="Cl-",
    ionicStrength=0.1 * molar,  # 100 mM
    neutralize=True,
)

print(f"System: {modeller.topology.getNumAtoms()} atoms")
print(f"Target ions: {na} Na+, {mg} Mg2+, {cl} Cl-")

# Save the environment
with open("cg/solvated_system.pdb", "w") as f:
    PDBFile.writeFile(modeller.topology, modeller.positions, f)

print("solvated_system.pdb saved — environment ready.")
```

```bash
uv run python src/05_solvate.py
```

**This is the file you hand off. The environment is done.**

---

### Step 6 — Simulate (when ready, any machine)

```python
# src/06_simulate.py
from openmm.app import *
from openmm import *
from openmm.unit import *

pdb = PDBFile("cg/solvated_system.pdb")
ff  = ForceField("charmm36.xml", "charmm36/water.xml")

system = ff.createSystem(
    pdb.topology,
    nonbondedMethod=PME,
    nonbondedCutoff=1.0 * nanometer,
    constraints=HBonds,
)

integrator = LangevinMiddleIntegrator(310*kelvin, 1/picosecond, 0.002*picoseconds)
sim = Simulation(pdb.topology, system, integrator)
sim.context.setPositions(pdb.positions)

print("Minimizing energy...")
sim.minimizeEnergy()

sim.reporters.append(DCDReporter("output/traj.dcd", 1000))
sim.reporters.append(StateDataReporter(
    "output/energies.csv", 1000,
    step=True, potentialEnergy=True, temperature=True, speed=True,
))

print("Running...")
sim.step(500_000)  # 10 ns at 20 fs CG timestep
```

---

### Step 7 — Visualize in Jupyter

```bash
uv run jupyter notebook notebooks/visualize.ipynb
```

```python
# notebooks/visualize.ipynb
import nglview as nv
import MDAnalysis as mda
import matplotlib.pyplot as plt
from MDAnalysis.analysis import rms

# --- 3D trajectory viewer ---
u = mda.Universe("cg/complex_cg.pdb", "output/traj.dcd")
view = nv.show_mdanalysis(u)
view.add_representation("cartoon", selection="protein")
view.add_representation("licorice", selection="nucleic")
view.add_representation("ball+stick", selection="resname NA CL MG")
view  # interactive — play/pause/scrub frames

# --- RMSD plot ---
protein = u.select_atoms("protein")
R = rms.RMSD(protein, select="backbone")
R.run()

plt.figure(figsize=(8, 4))
plt.plot(R.results.rmsd[:, 1], R.results.rmsd[:, 2], color="#7c3aed")
plt.xlabel("Frame")
plt.ylabel("RMSD (Å)")
plt.title("Twinkle hexamer stability over simulation")
plt.tight_layout()
plt.savefig("output/rmsd.png", dpi=150)
plt.show()
```

---

## Daily commands (the only 4 you need)

```bash
uv run python src/01_clean.py       # get + clean structure
uv run python src/04_merge.py       # position complex
uv run python src/05_solvate.py     # build environment ← what she asked for
uv run jupyter notebook             # visualize
```

---

## Tool summary (2026 stack)

| Role | Tool | Why |
|---|---|---|
| Package + env manager | `uv` | 10-100x faster than pip/conda, Rust-based |
| Linting + formatting | `Ruff` | replaces Black + isort + Flake8 |
| Type checker | `Ty` | new from Astral, native uv integration |
| MD engine | `OpenMM` | pure Python, CPU-runnable |
| CG force field | `MARTINI 3` | protein+DNA, 10x less compute than all-atom |
| Protein CG | `martinize2` | standard tool, pip install |
| Analysis | `MDAnalysis` | trajectory RMSD, selection, ion density |
| 3D visualization | `NGLview` | in-Jupyter, integrates with MDAnalysis |
| Static renders | `PyMOL 3.1` | free open-source, updated March 2026 |
| 2D plots | `matplotlib` | RMSD, energy, ion distribution |

---

## References

- Salt buffer: PMC7186178 (100 mM NaCl, 7.5 mM MgCl₂, HEPES pH 7.5)
- Twinkle structure: PDB 7T8C, Ciesielski et al. PNAS 2022
- MARTINI 3: Souza et al. Nature Methods 2021
- OpenMM: docs.openmm.org
- NGLview: Nguyen et al. Bioinformatics 2018
- 2026 Python stack: KDnuggets April 2026 (uv + Ruff + Ty)
- PyMOL 3.1.8: updated March 2026, pymol.org