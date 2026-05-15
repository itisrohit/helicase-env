# ruff: noqa: E402

import os
import tempfile
from pathlib import Path

CACHE_DIR = Path(tempfile.gettempdir()) / "twinkle-sim-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(CACHE_DIR / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_DIR / "xdg-cache"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import MDAnalysis as mda
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
CG_DIR = ROOT / "cg"
DELIVERABLES_DIR = ROOT / "deliverables"
COMPLEX_PDB = CG_DIR / "complex_cg.pdb"
ENV_PDB = CG_DIR / "solvated_inspection_system.pdb"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scatter_projection(ax, points: np.ndarray, color: str, label: str, size: float, alpha: float) -> None:
    if len(points) == 0:
        return
    ax.scatter(points[:, 0], points[:, 1], s=size, c=color, alpha=alpha, linewidths=0, label=label)


def projection(points: np.ndarray, axes: tuple[int, int]) -> np.ndarray:
    return points[:, list(axes)]


def style_axis(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(False)


def bounds(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return points.min(axis=0), points.max(axis=0)


def add_box_outline(ax, mins: np.ndarray, maxs: np.ndarray, dims: tuple[int, int], color: str = "#555555") -> None:
    i, j = dims
    rect = Rectangle(
        (mins[i], mins[j]),
        maxs[i] - mins[i],
        maxs[j] - mins[j],
        fill=False,
        linewidth=1.2,
        linestyle="--",
        edgecolor=color,
        alpha=0.8,
    )
    ax.add_patch(rect)


def set_limits(ax, points: np.ndarray, dims: tuple[int, int], pad: float) -> None:
    projected = projection(points, dims)
    mins = projected.min(axis=0) - pad
    maxs = projected.max(axis=0) + pad
    ax.set_xlim(mins[0], maxs[0])
    ax.set_ylim(mins[1], maxs[1])


def render_complex() -> Path:
    u = mda.Universe(str(COMPLEX_PDB))
    protein = u.select_atoms("protein").positions
    dna = u.select_atoms("resname DA* DC* DG* DT*").positions

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    views = [((0, 2), "X", "Z", "Side View (X-Z)"), ((1, 2), "Y", "Z", "Front View (Y-Z)")]
    for ax, (dims, xlabel, ylabel, title) in zip(axes, views, strict=True):
        scatter_projection(ax, projection(protein, dims), "#7fb3d5", "Twinkle", 12, 0.55)
        scatter_projection(ax, projection(dna, dims), "#f28e2b", "dsDNA", 36, 0.98)
        style_axis(ax, title, xlabel, ylabel)
        set_limits(ax, np.vstack([protein, dna]), dims, pad=12.0)
    axes[0].legend(loc="upper right", frameon=False, markerscale=1.2)
    fig.suptitle("Twinkle + dsDNA Merged Complex", fontsize=14)

    out = DELIVERABLES_DIR / "twinkle_dsDNA_complex_overview.png"
    fig.savefig(out, dpi=220, facecolor="white")
    plt.close(fig)
    return out


def render_environment_overview_and_zoom() -> tuple[Path, Path]:
    env = mda.Universe(str(ENV_PDB))
    complex_u = mda.Universe(str(COMPLEX_PDB))
    protein = complex_u.select_atoms("protein").positions
    dna = complex_u.select_atoms("resname DA* DC* DG* DT*").positions
    waters = env.select_atoms("resname W").positions
    ions = {
        "NA": ("#d62728", env.select_atoms("resname NA").positions),
        "CL": ("#2ca02c", env.select_atoms("resname CL").positions),
        "MG": ("#9467bd", env.select_atoms("resname MG").positions),
    }
    solute = np.vstack([protein, dna])
    box_mins, box_maxs = bounds(env.atoms.positions)
    solute_center = solute.mean(axis=0)

    # Overview: keep only a light solvent background so the solute remains visible.
    water_step = max(1, len(waters) // 22000)
    waters_overview = waters[::water_step]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    views = [((0, 2), "X", "Z", "Environment Side View (X-Z)"), ((1, 2), "Y", "Z", "Environment Front View (Y-Z)")]
    for ax, (dims, xlabel, ylabel, title) in zip(axes, views, strict=True):
        scatter_projection(ax, projection(waters_overview, dims), "#d9d9d9", "Water (light subsample)", 1.0, 0.09)
        for label, (color, positions) in ions.items():
            scatter_projection(ax, projection(positions, dims), color, label, 14, 0.72)
        scatter_projection(ax, projection(protein, dims), "#1f77b4", "Twinkle", 16, 0.78)
        scatter_projection(ax, projection(dna, dims), "#ff7f0e", "dsDNA", 42, 0.98)
        add_box_outline(ax, box_mins, box_maxs, dims)
        style_axis(ax, title, xlabel, ylabel)
        i, j = dims
        ax.scatter([solute_center[i]], [solute_center[j]], s=90, c="black", marker="x", alpha=0.8)
    axes[0].legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, markerscale=1.5)
    fig.suptitle("Twinkle + dsDNA Local Solvated Environment", fontsize=14)

    overview_out = DELIVERABLES_DIR / "twinkle_dsDNA_environment_overview.png"
    fig.savefig(overview_out, dpi=220, facecolor="white", bbox_inches="tight")
    plt.close(fig)

    # Zoom: show the solute neighborhood clearly.
    shell_radius = 34.0
    ion_radius = 45.0
    water_dist = np.linalg.norm(waters - solute_center, axis=1)
    waters_zoom = waters[water_dist <= shell_radius]
    ions_zoom = {
        label: (color, positions[np.linalg.norm(positions - solute_center, axis=1) <= ion_radius])
        for label, (color, positions) in ions.items()
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    views = [((0, 2), "X", "Z", "Zoomed Side View (X-Z)"), ((1, 2), "Y", "Z", "Zoomed Front View (Y-Z)")]
    for ax, (dims, xlabel, ylabel, title) in zip(axes, views, strict=True):
        scatter_projection(ax, projection(waters_zoom, dims), "#cfcfcf", "Nearby water", 6, 0.18)
        for label, (color, positions) in ions_zoom.items():
            scatter_projection(ax, projection(positions, dims), color, label, 26, 0.9)
        scatter_projection(ax, projection(protein, dims), "#1f77b4", "Twinkle", 22, 0.82)
        scatter_projection(ax, projection(dna, dims), "#ff7f0e", "dsDNA", 56, 0.98)
        style_axis(ax, title, xlabel, ylabel)
        set_limits(ax, solute, dims, pad=18.0)
    axes[0].legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, markerscale=1.2)
    fig.suptitle("Twinkle + dsDNA Solute Neighborhood", fontsize=14)

    zoom_out = DELIVERABLES_DIR / "twinkle_dsDNA_environment_zoom.png"
    fig.savefig(zoom_out, dpi=220, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    return overview_out, zoom_out


def main() -> None:
    DELIVERABLES_DIR.mkdir(exist_ok=True)
    complex_png = render_complex()
    overview_png, zoom_png = render_environment_overview_and_zoom()
    print(rel(complex_png))
    print(rel(overview_png))
    print(rel(zoom_png))


if __name__ == "__main__":
    main()
