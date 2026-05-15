# Martini 2 fallback HPC handoff

This directory is the strongest force-field-consistent rescue branch available in this repo today.

- Protein: Martini 2 fallback generated from `twinkle_hex.pdb`
- DNA: official `polyply` Martini 2 dsDNA topology + idealized CG coordinates
- Solvent coordinates: provisional grid-packed inspection coordinates
- Divalent ion caveat: the official `martini_v2.0_ions.itp` bundled here does not provide Mg. The `37` requested divalent ions are therefore encoded through a local `MG2` proxy with the same `Qd` +2 parameters as the official `CA+` bead.

Files:
- `system.top`: combined topology for the fallback system
- `solvated_m2_mg_proxy.pdb`: coordinate file rewritten to use Martini 2 ion names
- `mg_proxy.itp`: local Mg proxy include using the official divalent `Qd` +2 bead class
- `em.mdp`, `equil.mdp`, `mdrun.mdp`: official legacy tutorial starting points
- `water.gro`: official legacy Martini water box from the DNA tutorial package

Suggested HPC sequence:
1. `gmx grompp -f em.mdp -c solvated_m2_mg_proxy.pdb -p system.top -o 01-em.tpr -maxwarn 1`
2. `gmx mdrun -v -deffnm 01-em`
3. `gmx grompp -f equil.mdp -c 01-em.gro -p system.top -o 02-eq -maxwarn 1`
4. `gmx mdrun -v -deffnm 02-eq -rdd 2.0`
5. `gmx grompp -f mdrun.mdp -c 02-eq.gro -p system.top -o 03-run -maxwarn 1`
6. `gmx mdrun -v -deffnm 03-run -rdd 2.0`

This is still a rescue path, not a validated production-grade Martini 3 setup.
