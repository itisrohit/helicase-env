import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURES_DIR = ROOT / "structures"
TWINKLE_INPUT = STRUCTURES_DIR / "twinkle_hex.pdb"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run_step(script_name: str) -> None:
    script_path = ROOT / "src" / script_name
    print(f"\n==> Running {rel(script_path)}", flush=True)
    result = subprocess.run([sys.executable, str(script_path)], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Twinkle + dsDNA local-environment delivery flow from repo inputs to "
            "handoff bundle and static visuals."
        )
    )
    parser.add_argument(
        "--refresh-twinkle",
        action="store_true",
        help="Force a fresh download and cleanup of 7T8C before the rest of the workflow.",
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="Skip static PNG generation at the end.",
    )
    parser.add_argument(
        "--open-notebook",
        action="store_true",
        help="Launch Jupyter Notebook on notebooks/visualize.ipynb after the pipeline finishes.",
    )
    return parser


def maybe_refresh_twinkle(refresh_requested: bool) -> None:
    if refresh_requested or not TWINKLE_INPUT.exists():
        reason = "requested by flag" if refresh_requested else "missing local input"
        print(f"Twinkle structure refresh enabled ({reason}).", flush=True)
        run_step("01_clean.py")
    else:
        print(f"Using existing {rel(TWINKLE_INPUT)}", flush=True)


def maybe_render(skip_render: bool) -> None:
    if skip_render:
        print("Skipping static render generation.", flush=True)
        return
    run_step("07_render_delivery_views.py")


def maybe_open_notebook(open_notebook: bool) -> None:
    if not open_notebook:
        print("\nInteractive notebook is available at `notebooks/visualize.ipynb`.", flush=True)
        print("Launch it with: `uv run jupyter notebook notebooks/visualize.ipynb`")
        return

    notebook_path = ROOT / "notebooks" / "visualize.ipynb"
    print(f"\nLaunching {rel(notebook_path)}", flush=True)
    raise SystemExit(
        subprocess.run(
            [sys.executable, "-m", "notebook", str(notebook_path)],
            cwd=ROOT,
        ).returncode
    )


def main() -> None:
    args = build_parser().parse_args()

    maybe_refresh_twinkle(args.refresh_twinkle)
    for script_name in [
        "02_build_dna.py",
        "03_coarse_grain.py",
        "04_merge.py",
        "05_solvate.py",
        "06_simulate.py",
    ]:
        run_step(script_name)
    maybe_render(args.skip_render)
    maybe_open_notebook(args.open_notebook)


if __name__ == "__main__":
    main()
