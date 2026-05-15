# Delivery

As of May 15, 2026, the requested local environment deliverable is prepared.

Primary handoff artifact:
- [deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz](/Users/RohitKumar/Desktop/GItHubProjects/helicase-env/deliverables/twinkle_dsDNA_environment_m2_mg_proxy.tar.gz)

Expanded handoff directory:
- [cg/handoff_m2_mg_proxy/](</Users/RohitKumar/Desktop/GItHubProjects/helicase-env/cg/handoff_m2_mg_proxy/>)

What it contains:
- Twinkle hexamer coarse-grained protein coordinates
- 30 bp dsDNA coarse-grained coordinates and topology
- solvated coordinate file with water, NaCl, and the requested divalent-ion count
- combined topology and official Martini 2 support files
- starter `em.mdp`, `equil.mdp`, and `mdrun.mdp` files for HPC-side GROMACS preparation

Important scope note:
- This satisfies the practical ask of preparing the local starting environment for later HPC use.
- The delivered branch is the repo's validated Martini 2 rescue path.
- The original Martini 3 dsDNA aspiration remains upstream-blocked and is not required for this handoff.
