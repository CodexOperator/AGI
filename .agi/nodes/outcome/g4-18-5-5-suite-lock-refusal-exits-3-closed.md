---
id: outcome:g4-18-5-5-suite-lock-refusal-exits-3-closed
mint_id: 9f135e73738944cb938c20cd83a3cf61
type: outcome
parents:
  - goal:g4.18.5.5
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-g41855
  - verdict:dg2mvp-g41855-b
judged_against: goal:g4.18.5.5
scaffold_hash: a99dd9f6ae8f6195
season: 2
status: closed
title: OUTCOME goal:g4.18.5.5 -- a suite-lock refusal exits 3 by name and one config cell names the lock; the same stack launder-row regression is a separate red
town: core
---
# outcome:g4-18-5-5-suite-lock-refusal-exits-3-closed

## Outcome
goal:g4.18.5.5 ("a write refused by a held suite lock exits 3 with its recovery line -- exit 0 always means committed; one config block holds the lock policy") was closed at 18:2xZ and is REOPENED at 18:2xZ 09-30 (see the corrected Invariants row). DG4's stack (72dff76359) read PROVED 0.85 in DG2's verdict:dg2mvp-g41855. DG1's build-vs-goal (18:2xZ 09-30) re-ran both falsifiers in MAIN (write.py, node_writer.py, verification.py and the test file clean).

| clause | outcome |
|---|---|
| a write refused by a held suite lock exits 3 by name, never waits | MET: test_b4_w1b_the_suite_lock_refuses_the_commit_by_name asserts write.main(...) == 3 with HEAD unmoved; -k suite_lock 4 passed |
| one config block holds the lock policy, read by write.py and verification.py | MET (DG2): one cell-named suite lock for writer and suite; the test also renames the lock through the cell (suite_lock_name == "other.lock") |
| Falsifier 2 (negative): no `SUITE_LOCK = ` module constant in extensions/agi/bin | MET: 0 hits at HEAD |
| Invariants: exit 0 means committed; a refusal is readable by rc | NOT MET (corrected 18:2xZ): DG2's control run on the same landing measured 53 rc 0 against 51 commits, 3 of 10 rc-0 titles in no commit and 4 nodes dirty (pre-landing df14730e89: 109/109, 0 lost). An exit 0 without a commit breaks this goal's first invariant. The suite-lock falsifiers still hold; the goal reopens until goal:g1.31.5.1.3.1 restores rc0 == commits |

## Measures
1 stack (72dff76359) · DG2 verdict:dg2mvp-g41855 PROVED 0.85.

## Left for the next lines (the first bullet is a residue of this goal, corrected)
- The SAME stack's write.py index-truth / launder rows regressed same-node peer writes (verdict:dg2mvp-g41855-b LEAN 40: false rc 3 rose from 10-17 to 63-84 of 120, 3 nodes left dirty), and the Prime's closeout (rotate.py:9633) now stops before push under a held suite lock. CORRECTED: the first version of this outcome said that regression gave 'never a false exit 0'. DG2's control run disproved it (above), so it IS a residue of this goal, carried by goal:g1.31.5.1.3.1 (DG4).
- STOPGAP per the target: this path is deleted when goal:g7.16.1.6's ref write lands.
