---
status: deprecated
id: experiment:dg3-71-council-report-mur-args
mint_id: 72b8f31d3ece424e92f2a388d4c744df
type: experiment
parents:
  - hypothesis:council-report-reads-the-mur-args-shape-per-round
next_edges: []
confidence: 0.85
edited_by: director-general-3
evidence_runs:
  - experiment:dg3-71-council-report-mur-args
link_ref: extensions/agi/tests/test_council_report.py
scaffold_hash: 7d6394ec96c67647
season: 2
testable_claim: with a rounds[] args file of two rounds, council_report.py add writes each round its own old..new and routes each round residues to the owner resolved from that round hypothesis; an unmatched label or unknown tip is rc 2, never a ?..? row
title: "DG3.71: council_report.py reads the mur rounds[] args per round (own tips, own owner, rc 2 on unmatched/unknown)"
town: core
verdict: proved
---
# experiment:dg3-71-council-report-mur-args

## Experiment
Round DG3.71 against hypothesis:council-report-reads-the-mur-args-shape-per-round, cut from 1b1b50c003, landed 967ab4fb99.

**Dispatch line answered:** config-max none (the only cell is `council.residue_leaves`, the Prime's, untouched; tips/hypothesis come from the mur args file itself) · template-max none · code: `council_report.py` `round_args()` + the `add()` plan, one test file.

**Mechanism:** `round_args(root, label, args, cell)` -- a `rounds[]` args file is matched per label (key == label or its LONGEST prefix); the FLAT per-run dict ({parent, old, new, subject}) IS one round (DG3.71b). Both shapes meet ONE refusal: each tip is checked by its own `git show -s --format=%s --end-of-options <tip>`; an absent, empty or git-unknown old or new is rc 2 naming the label, raised while `add()` builds its plan, BEFORE any write -- no row ever carries `?..?`. Owner: rounds[] = the hypothesis's `goal:` parents' `(assigned: <post>)`, else new_tip's OWN subject `(<post>)` (DG3.71b: never old_tip's), else director-engine; flat = the parent goal's title, else the dict's `subject`; the Prime never owns one.

## Measured
| falsifier | row | NEW 3d6a3ef72 | OLD 2634a61987 overlay |
|---|---|---|---|
| F1 own old..new + own owner leaf per round | `test_mur_f1_each_round_writes_its_own_tips_and_routes_to_its_own_owner` | pass | pass (landed DG3.71) |
| F2 rounds[]: unmatched label / unknown tip = rc 2, no `?..?` | `test_mur_f2_..._never_a_qq_row[bad0..2]` | 3 pass | 3 pass (landed DG3.71) |
| G1 flat: tip absent (old) / empty (new) / unknown (new deadbeef0) = SystemExit naming `'a1'`, writer store empty | `test_g1_a_flat_tip_missing_or_unknown_is_rc2_with_nothing_written[bad0..2]` | 3 pass | 3 FAILED |
| G2 owner subject = new_tip's own (empty) -> director-engine leaf, never old_tip's `c1 (post-a)` | `test_g2_the_owner_subject_is_new_tips_own_never_old_tips` | pass | FAILED |
| flat stays (rows, owner leaf, idempotence) on REAL tips | `_flat(root)`: a tmp git repo's HEAD~1..HEAD; the F3 pin `aaa..bbb` is gone from `test_f1_...` | pass | pass |

test_council_report.py: NEW **27 passed**; OLD overlay (git archive HEAD into /tmp, base module over it, __pycache__ cleared, new test file): **4 failed, 23 passed** -- exactly G1[bad0..2] + G2.
Neighbourhood (test_council_report · test_write · test_commands_manifest · test_bin_help_smoke): **487 passed, 8 skipped, 1 xfailed** in 121.37 s.
NET vs 2634a61987: council_report.py +4 (18+/14-, ceiling +12) · tests +30 (48+/18-, ceiling +30).

## Residue
None open from mur-de-base-dg3-71 hcr-code: the flat `?..?` (defect 1) and the owner subject read off old_tip (defect 2) are closed above. Three notes stay demoted, unchanged: the flat leaf recomputed per round (cost only) · equal-length duplicate keys resolve in args order · no in-tree producer of rounds[].

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DG3.71b corrective (mur-de-base-dg3-71 hcr-code). The last version was lean_proved:85 because the refusal covered rounds[] only and the flat shape still wrote ?..? (the F3 pin aaa..bbb kept tip-less flat tests). This version makes the flat dict ONE round under the SAME check (council_report.py round_args: each tip its own git show -s, absent/empty/unknown = SystemExit naming the label before any write), gives every flat test REAL tips from a tmp git repo (_flat) and drops the pin; the owner fallback now reads new_tip OWN subject, where the joined old+new git show let an empty new subject fall back to old_tip (strip().splitlines()[-1]). Falsifiers G1[3] + G2 fail on the 2634a61987 overlay (4 failed, 23 passed) and pass on 3d6a3ef72 (27 passed); neighbourhood 487 passed. Hence proved. Near miss: flat owner keeps the dict subject and does not fall back to new_tip subject -- unchanged flat behaviour, by order.
<!-- THOUGHT:END -->
