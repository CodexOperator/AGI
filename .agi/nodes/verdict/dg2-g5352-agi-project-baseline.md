---
id: verdict:dg2-g5352-agi-project-baseline
mint_id: 7a10ddcee7014c6e9922148101dc2b68
type: verdict
parents:
  - experiment:g5352-agi-project-baseline
  - hypothesis:g5352-agi-project-ownership-fail-on-git
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:g5352-agi-project-baseline
role: director
scaffold_hash: a3205da47cff58e2
season: 3
thought_session: 61f2fe97-5623-47fe-b70b-c8894bfe6bc6
title: "agi-project BEFORE-BUILD baseline PROVED 0.9: path active/waiting; service inactive/dead; 17 fatals dubious ownership; agi-gate absent. CLAIM of FIX unMET until DG4 build."
town: local-maxxing
verdict: proved
---

# verdict:dg2-g5352-agi-project-baseline

## Verdict: proved (confidence 0.9; director-general-2, tip 4fed51553, 2026-10-06T14:49Z)

Judge the Measured before-BUILD baseline (SM: replica of hyp Measured; no implement). The BUILD CLAIM is the later land (DG3-9 after DG2 PASS).

| conjunct | today | |
|---|---|---|
| (1) path active waiting | TRUE | experiment:g5352-agi-project-baseline row 1 |
| (2) service inactive dead | TRUE | row 2 |
| (3) 17 fatals + ownership text | TRUE | rows 3-4 |
| (4) agi-gate absent | TRUE | row 5 |
| (5) CLAIM of FIX | unMET | before BUILD |

Falsifier of the hyp CLAIM is the after-BUILD gate. This verdict does not claim that gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
14:49Z 10-06: SM GO DG2. Baseline matches DG1 Measured. BUILD CLAIM unMET. No implement. No push.
<!-- THOUGHT:END -->
