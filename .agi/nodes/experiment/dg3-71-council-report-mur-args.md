---
id: experiment:dg3-71-council-report-mur-args
mint_id: 72b8f31d3ece424e92f2a388d4c744df
type: experiment
parents:
  - hypothesis:council-report-reads-the-mur-args-shape-per-round
next_edges: []
confidence: 0.85
edited_by: director-general-3
link_ref: extensions/agi/tests/test_council_report.py
scaffold_hash: 7d6394ec96c67647
season: 2
testable_claim: with a rounds[] args file of two rounds, council_report.py add writes each round its own old..new and routes each round residues to the owner resolved from that round hypothesis; an unmatched label or unknown tip is rc 2, never a ?..? row
title: "DG3.71: council_report.py reads the mur rounds[] args per round (own tips, own owner, rc 2 on unmatched/unknown)"
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:dg3-71-council-report-mur-args

## Experiment
Round DG3.71 against hypothesis:council-report-reads-the-mur-args-shape-per-round, cut from 1b1b50c003, landed 967ab4fb99.

**Dispatch line answered:** config-max none (the only cell is `council.residue_leaves`, the Prime's, untouched; tips/hypothesis come from the mur args file itself) · template-max none · code: `council_report.py` `round_args()` + the `add()` plan, one test file.

**Mechanism:** `round_args(root, label, args, cell)` -- a `rounds[]` args file is matched per label (key == label or its LONGEST prefix), returns that round's `old_tip..new_tip` (both checked by ONE `git show -s --format=%s --end-of-options old new`, rc != 0 = unknown) and the owner leaf from the round hypothesis's `goal:` parents' `(assigned: <post>)`, else new_tip's commit subject `(<post>)`, else director-engine (Prime never). `add()` builds the whole plan BEFORE any write, so an unmatched label / absent or unknown tip is rc 2 naming the label with nothing written. No `rounds` key = the flat per-run dict, unchanged.

## Measured
| falsifier | row | fails on 1b1b50c003 |
|---|---|---|
| F1 own old..new + own owner leaf per round | `test_mur_f1_each_round_writes_its_own_tips_and_routes_to_its_own_owner` | yes (FAILED) |
| F2 unmatched label / unknown tip = rc 2 naming the label, no `?..?` | `test_mur_f2_..._never_a_qq_row[bad0..2]` (key zz · old_tip deadbeef0 · new_tip "") | yes (3 FAILED) |
| F3 flat shape stays | existing 19 rows + one assert `aaa..bbb` in `test_f1_one_row_per_round...` | no -- a regression guard, green on base by nature |

Base check: base `council_report.py` copied over the worktree file, new test file run: 4 failed, 19 passed; file restored.
Suite (test_council_report · test_write · test_commands_manifest · test_bin_help_smoke; test_merge_gate.py absent on this trunk): **483 passed, 8 skipped, 1 xfailed** in 108.89 s. test_council_report.py alone: 23 passed.
NET: council_report.py +22 (29+/7-, ceiling +25) · tests +40 (41+/1-, ceiling +40).

## Residue
The CLAIM's "a row whose old or new is unknown is refused" holds for the rounds[] shape only: the flat shape with no old/new still writes `?..?` because F3 pins the existing flat tests (they pass `{"parent": ...}` without tips). Closing it = refuse in the flat branch too and give those tests tips -- a separate round.
