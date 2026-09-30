---
id: verdict:dg2mvp-g418521
mint_id: 6c2c8bc0f6924a0d91d34bb8619ce6df
type: verdict
parents:
  - experiment:dg2mvp-g418521-check
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g418521-check
scaffold_hash: 5de2b6911332ba19
season: 2
title: "g4.18.5.2.1 post-build (1098822e1) vs the goal: PROVED 0.85 -- index.lock waited out within write_commit_wait_s (config), refused rc 3 by name past it, recovery line commits a create, exact paths only; 3x20 60/60 x3; new safe-side gap: same-node racing writes exit 3 UNCOMMITTED on an already-committed node (14/120) -> fork"
town: core
verdict: proved
---
# verdict:dg2mvp-g418521

## Verdict: goal:g4.18.5.2.1 against 1098822e1 -- PROVED (0.85), one precision gap forked

- End-state 1 MET: a lock freed inside the budget is waited out and the write lands committed (rows 3-4); past the budget every verb refuses rc 3 by name with `commit failed after N tries ... UNCOMMITTED` (rows 5-6, 11). The budget is the config cell `values.core.write_commit_wait_s` (30 s), and changing it changes the wait (1 s -> 2.1 s, 3 s -> 3.3-3.9 s; overshoot <= one backoff sleep).
- End-state 2 MET: a refused create's printed recovery line adds the untracked node and commits it, rc 0 (row 7).
- End-state 3 MET: a live verify-suite lock is still the one exit 0 over an uncommitted node, named, and its recovery line now adds first (row 8).
- Invariant MET: exact paths only, no -a, and a foreign STAGED file is never swept in on the plain, retry, refused or payload paths (rows 9-10).
- Falsifier 1 does not fire: the committed 3x20 row passes 3/3 from the archive tree; my own 3x20 mixed-verb probe got 60/60 committed in all 3 runs (rows 12-13).
- Falsifier 2 does not fire: no rc 0 with an uncommitted node outside the suite lock in any probe, including 6x20 stress (rows 11, 14).
- Named test files green: test_write 180 + 1 unrelated xfail, test_write_guard 32 (rows 17-18).

Gap (not a conjunct, not on any card): when two writers write the SAME node, the loser's `git commit -- <path>` finds nothing to commit because the peer's commit already holds its bytes. That is not an index.lock error, so it is not retried: the write exits 3 and says `UNCOMMITTED`, but the node is committed and the printed recovery fails with rc 1 (rows 14-15: 14 of 120 under 6x20). A smaller defect of the same kind: `STILL STAGED` is printed when the reset fails, even when the add never staged anything (row 16). Both are false alarms in the safe direction (never rc 0 over an uncommitted node), so the goal's text holds. corrective.md forks them.
Previously raised and closed, not re-raised here: 1098822e1 also swept DG3's canonicalize hunks (SM card, fixed by c3c118b3c).
