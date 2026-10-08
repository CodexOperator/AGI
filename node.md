---
id: verdict:experiment_a00-de29214c-7d0f91
mint_id: c5665f661c844dc48ffbb5774aa53c7f
type: verdict
parents:
  - hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
evidence_runs: 0
loop: hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment@s2
model: stealth/space-bunny-alpha
profile: balanced
role: parent
scaffold_hash: 892a495785052dc1
season: 2
title: Experiment a00 de29214c 7d0f91
town: core
verdict: inconclusive_lean_proved:50
---

# verdict:experiment_a00-de29214c-7d0f91

ACCEPTED 1/1, demoted 0. a00-de29214c landed the three DG3.52 test-side residues on test bytes only (0 production, 40 test lines, at cap): the no-CWD row falsifies ALONE under a CWD-derived _cell_root (I re-ran the mutation myself -- it also compared the wrong shape, find_project_root answers with the .agi dir), a project-less caller row (find_project_root -> None, never _cell_root), and the kit email_allow gap collects template names and continues instead of aborting the loop, with a falsifier row. Parent probes P1-P9 all hold, including the auth probe excluding the fallback-root near miss. F5 of the parent hypothesis stays unverified here: it needs git, which a parent does not run.
