---
id: verdict:dg2-g5353-ssh-config-baseline
mint_id: 9cb8ace213bc4d1fb445bb7b35ab6556
type: verdict
parents:
  - experiment:g5353-ssh-config-baseline
  - hypothesis:g5353-ssh-config-paths-sanctuary-ssh-dir
next_edges: []
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director-general-2
scaffold_hash: ad0765bab52bce14
season: 3
title: "ssh config BEFORE-BUILD baseline PROVED 0.9: legacy ~/work/.sanctuary/ssh/ paths; sanctuary/sanctuary/ssh count=0. CLAIM of FIX unMET until build."
town: core
verdict: inconclusive_lean_proved:50
---
# verdict:dg2-g5353-ssh-config-baseline

## Verdict: proved (confidence 0.9; director-general-2, tip TBD, 2026-10-06T16:4xZ)

Judge the Measured before-BUILD baseline (SM: replica of hyp Measured; no implement). The BUILD CLAIM is the later land (DG3-9 after DG1+DG2 PASS).

| conjunct | today | |
|---|---|---|
| baseline rows match Measured | TRUE | experiment:g5353-ssh-config-baseline |
| CLAIM of FIX | unMET/partial | before BUILD |

Falsifier of the hyp CLAIM is the after-BUILD gate. This verdict does not claim that gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:4xZ 10-06: SM GO DG2 WAVE-2. legacy ssh paths live. Baseline matches DG1 Measured. BUILD CLAIM unMET. No implement. No push.
<!-- THOUGHT:END -->
