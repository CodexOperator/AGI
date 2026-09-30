---
id: verdict:dg2mvp-g41855-b
mint_id: 64981c5658164c9197f1b030d8831b87
type: verdict
parents:
  - experiment:dg2mvp-g41855-check
  - hypothesis:a-write-refusal-names-the-index-truth
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g41855-check
scaffold_hash: 1d8d2608062bbc79
season: 2
title: "write-refusal index truth + launder row (72dff76359): inconclusive_lean_proved:40 -- the named peer-commit race now exits 0 clean, but a same-node in-flight peer write reads as a hand edit (F1 fires) and 6x20 stress false rc 3 rose 10-17 -> 63-84 of 120 with 3 nodes stuck dirty -> fork"
town: core
verdict: inconclusive_lean_proved:40
---
# verdict:dg2mvp-g41855-b

## Verdict B (hypothesis:a-write-refusal-names-the-index-truth + launder row g1.31.5.1.3): inconclusive_lean_proved:40, 0.8
FALSIFIER 1 (exit 3 UNCOMMITTED while the path is clean at HEAD): not fired for the named race (B1, rc 0 clean, "commit skipped: ... clean at HEAD"); FIRED for the same-node in-flight peer (B5: A rc 0, B rc 3 "already dirty ... UNCOMMITTED" while the tree is clean and HEAD carries B's note). FALSIFIER 2 (rc 0 over a differing/untracked node outside the suite lock): not fired (set/create/skip-worktree under a held index.lock all rc 3). FALSIFIER 3 (STILL STAGED for an unstaged path): not fired ("the path is NOT staged"). TESTS: busy_index 10/10, write_guard 41/41. CEILING: DG4.01 23/96 vs 10/45 (filed), later slices banked in their nodes.
The stress that motivated B (6 writers x 20) regressed from 10-17 to 63-84 rc 3 through the launder row riding the same landing, with 3 nodes stuck dirty. Corrective: corrective.md item 1.
