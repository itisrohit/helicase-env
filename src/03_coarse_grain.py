# src/03_coarse_grain.py
import glob
import os
import shutil
import subprocess
from pathlib import Path


def run_martinize():
    input_pdb = "structures/twinkle_hex.pdb"
    output_pdb = "cg/twinkle_cg.pdb"
    output_itp = "cg/twinkle_cg.itp"

    Path("cg").mkdir(exist_ok=True)

    print(f"Running martinize2 for {input_pdb}...")

    # Run martinize2
    # We use -maxwarn 1 because we don't have DSSP installed in this environment yet
    cmd = [
        "uv",
        "run",
        "martinize2",
        "-f",
        input_pdb,
        "-o",
        output_pdb,
        "-x",
        output_itp,
        "-ff",
        "martini3001",
        "-elastic",
        "-ef",
        "500",
        "-el",
        "0.5",
        "-eu",
        "0.9",
        "-maxwarn",
        "1",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running martinize2:")
        print(result.stderr)
        return

    print("martinize2 completed successfully for protein.")

    # --- DNA -> MARTINI 3 CG ---
    dna_pdb = "structures/dna_30bp.pdb"
    dna_out = "cg/dna_cg.pdb"
    dna_itp = "cg/dna_cg.itp"

    print(f"Running martinize2 for {dna_pdb}...")
    cmd_dna = [
        "uv",
        "run",
        "martinize2",
        "-f",
        dna_pdb,
        "-o",
        dna_out,
        "-x",
        dna_itp,
        "-ff",
        "martini3001",
        "-maxwarn",
        "1",
    ]

    result_dna = subprocess.run(cmd_dna, capture_output=True, text=True)
    if result_dna.returncode != 0:
        print("Error running martinize2 for DNA:")
        print(result_dna.stderr)
    else:
        print("DNA coarse-graining completed.")

    # Move molecule_*.itp files to cg/
    itp_files = glob.glob("molecule_*.itp")
    for f in itp_files:
        shutil.move(f, Path("cg") / f)
        print(f"Moved {f} to cg/")

    # Clean up backups
    backups = glob.glob("#*#")
    for f in backups:
        os.remove(f)
        print(f"Removed backup {f}")


if __name__ == "__main__":
    run_martinize()
