# Twinkle + dsDNA Simulation Environment

A coarse-grained Twinkle helicase + dsDNA setup workspace.

Current reality:
- The requested local environment handoff is prepared.
- The delivered path in this repo is a consistent Martini 2 rescue branch:
  - `cg/twinkle_m2_cg.pdb`
  - `cg/dna_fallback_m2_cg.pdb`
  - `cg/complex_cg.pdb`
  - `cg/solvated_inspection_system.pdb`
  - `cg/handoff_m2_mg_proxy/`
- Packaged delivery artifact:
  - `deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz`
- The original MARTINI 3 DNA path is still blocked upstream in the local `martinize2` stack, but that does not block the requested handoff deliverable.

---

## Quick Start

### Delivery
The direct handoff artifact is documented in [DELIVERY.md](./DELIVERY.md).

### 1. Initialize Environment
Ensure you have `uv` installed, then sync the project:
```bash
uv sync
```

### 2. Run the Pipeline
The simulation setup is broken down into modular steps:

| Step | Script | Description |
| :--- | :--- | :--- |
| **01** | `uv run python src/01_clean.py` | Fetch & clean Twinkle hexamer from RCSB (7T8C) |
| **02** | *Manual Step* | Place `dna_30bp.pdb` in `structures/` |
| **03** | `uv run python src/03_coarse_grain.py` | Generate Twinkle CG output and DNA fallback artifacts in `cg/` |
| **04** | `uv run python src/04_merge.py` | Assemble an inspection complex using the available CG DNA file |
| **05** | `uv run python src/05_solvate.py` | Build the local CG water/ion environment |
| **06** | `uv run python src/06_simulate.py` | Build the self-contained Martini 2 HPC handoff bundle in `cg/handoff_m2_mg_proxy/` |

### 3. Visualization
Open the interactive 3D viewer in Jupyter:
```bash
uv run jupyter notebook notebooks/visualize.ipynb
```

---

## Toolchain 

This project leverages the **Astral toolchain** for maximum efficiency:

- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Rust-based, 100x faster than pip)
- **Linter & Formatter**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checker**: [Ty](https://github.com/astral-sh/ty) (Modern successor to mypy)
- **Simulation Handoff**: legacy Martini/GROMACS-style HPC bundle generation
- **Coarse-Graining**: [MARTINI 3](https://cgmartini.nl/) via `martinize2`

### Development Commands

```bash
uv run ruff check . --fix  # Lint & Auto-fix
uv run ruff format .       # Format code
uv run ty check .          # Type check (Modern)
uv run pytest              # Run tests
```

---

## Project Structure

- `src/`: Core simulation logic and pipeline scripts.
- `cg/`: Coarse-grained models and topology artifacts.
- `structures/`: Input atomic structures.
- `notebooks/`: Visualization and analysis.
- `output/`: Trajectories and results.

---

## Project Plan
See [docs/plan.md](docs/plan.md) for the detailed implementation roadmap and status.
