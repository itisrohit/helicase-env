# Twinkle + dsDNA Simulation Environment

A modern, high-performance simulation environment for the Twinkle helicase and dsDNA, optimized.

---

## Quick Start

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
| **03** | `uv run python src/03_coarse_grain.py` | Generate MARTINI 3 topologies & move to `cg/` |
| **04** | `uv run python src/04_merge.py` | Assemble the complex (DNA through ring channel) |
| **05** | `uv run python src/05_solvate.py` | Add water, 100mM NaCl, and 7.5mM MgCl₂ |
| **06** | `uv run python src/06_simulate.py` | Run OpenMM simulation |

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
- **Simulation**: [OpenMM 8.5+](https://openmm.org/)
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
- `cg/`: Coarse-grained models and ITP topologies.
- `structures/`: Input atomic structures.
- `notebooks/`: Visualization and analysis.
- `output/`: Trajectories and results.

---

## Project Plan
See [docs/plan.md](docs/plan.md) for the detailed implementation roadmap and status.
