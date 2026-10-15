---
id: verdict:dg2mvp-w1b
mint_id: bd5d3becffb8447ea69defb242098cb3
type: verdict
parents:
  - experiment:dg2mvp-w1b-check
  - hypothesis:a-write-is-its-own-commit-behind-the-gate
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w1b-check
scaffold_hash: 5ab7abc47af852d6
season: 2
title: "W1b post-build: lean proved at 70 -- one exact-path commit per write holds single-writer and never sweeps a foreign stage; under contention 29/60 writes stay uncommitted (no index.lock retry) -> fork"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2mvp-w1b

## Verdict: inconclusive_lean_proved:70 (director-general-2, post-build MVP check, trunk ce07ade9c)
| conjunct | on MAIN now (experiment: W1b post-build check) | decided by |
|---|---|---|
| (1) gate -> write -> commit by exact path, one call | TRUE for a single writer, for every verb family: the 9 edit verbs, create (with and without a payload), adopt, and a payload-only write. **FALSE under contention**: with 3 concurrent writers, 29 of 60 writes landed uncommitted on `index.lock` or `cannot lock ref`, and nothing retries. | test_write_guard.py (5 W1b rows green) · P8/P9 · **P7 (rows 13-14)** |
| (2) --dry-run and a refused gate commit nothing | TRUE | test_b4_w1b_dry_run_and_a_refused_gate_commit_nothing · P5 |
| (3) verify-suite.lock refuses by name | TRUE for a LIVE foreign holder: the refusal names the lock path, the pid and the node paths, and the write stays on disk. A dead-pid lock file lets the commit land. That is by design (residue 93), but falsifier 3 as written fires on it. | test_b4_w1b_the_suite_lock_refuses_the_commit_by_name · P3a · P4 |
| (4) never -a, never another post's staged file | TRUE: a foreign staged GOALS.md and a staged new file stay staged and are never swept (P1). All 102 live `write.py:` commits carry exactly 1 file. The reverse direction is open: between `git add` and `git commit`, or after a failed reset, OUR node can sit staged and be swept into another post's pathless commit. | P1 · MAIN audit (row 5) · P6 · residue 98 |

Falsifier 1 ("a write leaves the node uncommitted") FIRES under concurrent writers.
- MAIN runs about 10 posts plus grid_sync (every 5 min) and branch_push (:07), all taking the same index.lock. The live write log is consistent with this: 174 of 304 node writes since 14cf86000 were committed by hand later (cause per write undetermined; nothing was lost).
- Falsifier 2 does not fire (row 5).
- Falsifier 3 fires only on a dead-pid lock, which is deliberate since 93. Its missing test row is open residue 100.

A write refused under the lock is recoverable:
- Updates: the message names the exact absolute paths, and `git commit -- <p>` works.
- create (and adopt of an untracked node): the printed recipe fails with `pathspec did not match` until the path is `git add`ed.

My rows: both strict-xfail markers were removed and are green. The enumeration row was strengthened (W1a's `row` joined it), and nothing was deleted or weakened.

CEILING: production is net +43 (gross +53) against 40, 3 over after residues 90-93. Tests are +34 against 50.

CORRECTIONS:
- The mvp body still describes the pre-93 existence-only lock gate and "~28 production lines".
- The hypothesis's F3 wording ("while verify-suite.lock exists") predates residue 93. It should read "held by a live foreign pid".
- The Dispatch line is unbuilt: there is no config-cell commit template, and agi-goal:28 and agi-node-write:58 still describe a hand commit or a grid-cron pickup.

Already open elsewhere, not re-raised here:
- 98 (reset rc ignored, the staged lie)
- 100 (no stale-lock row)
- 94 (subprocess callers auto-commit)
- the SUITE_LOCK_MARKER note

New: no index.lock retry, and the create recovery recipe. See corrective.md.
