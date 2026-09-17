---
id: experiment:a00-cee030e2-d2ccf8
mint_id: 2e3e71e27f3e470296e421f3c81ba164
type: experiment
parents:
  - hypothesis:l4-prepare-performs-its-three-clears-itself-and-prints-cleared-never-a-hand-step
next_edges: []
confidence: 0.9
edited_by: a00-cee030e2
evidence_runs:
  - experiment:a00-cee030e2-d2ccf8
line_ceiling: 25
loop: hypothesis:l4-prepare-performs-its-three-clears-itself-and-prints-cleared-never-a-hand-step@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 27
profile: balanced
role: kid
scaffold_hash: f7ad38a150a89c4c
season: 2
title: prepare performs the mirror push and meter re-pin under perform and prints cleared never a hand line
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cee030e2-d2ccf8

## Experiment

**Pre-fix state (measured):** `rotate.py prepare --perform` (rotate-self's
pre-flight, `cmd_rotate_self` sets `perform = not dry_run`) already PERFORMS
check 3's only-behind season merge (F14) and prints a measured-result line.
Checks 1 (post-head mirror push to `refs/agi/posts/<post>`) and 5 (stale
meter pin re-pin) were only BANNED as `clear: <command for you to run>` hand
lines -- the exact falsifier the hypothesis names. **g15 claim = behaviour to
build**, so I implemented the two missing performs in `_prepare_checks`
(rotate.py): under `--perform`, and only when every OTHER check is clean (no
side effect before a refusal -- P1-a), prepare now performs the mirror push and
the meter re-pin itself, printing `cleared: <step> (<measured result>)` and
suppressing the `clear:` line. A clear that FAILS (push non-zero rc, opaque
git) stays a BLOCK naming the exact failing command (claim 2).

**What landed (claimed testable bits + 2 falsifiers):**
- `prepare --perform` on a post branch with 3 unpushed mirror commits PUSHES
them and prints `[ok] unpushed commits vs refs/agi/posts/p1 ... — cleared:
mirror push (abcdef1)`; exit 0, no `[BLOCK]`.
- A mirror push git refuses (rc 1) is NOT reported cleared: `[BLOCK] unpushed
commits vs refs/agi/posts/p1 ...` + `clear: git push origin
HEAD:refs/agi/posts/p1`, exit 3. (falsifier: a failed clear reported cleared.)
- A stale meter pin re-points to the current generation and transcript,
printing `... — cleared: meter re-pin (<transcript>)`; the pin file now starts
with `3\t` (was `2\t`). A SECOND `--perform` finds nothing to clear and prints
`prepare: no blockers — safe to rotate.` (falsifier: a clear performed
silently / a repeated clear).
- Atomicity: `--perform` with a dirty tree + stale pin does NOT re-pin (the
refusal performs no side effect); `[BLOCK] dirty tree` and `seat_pin-stale`
both name, pin file untouched.
- Bare `prepare` / `--dry-run` still lists only (perform off) -- zero
behaviour change there; all 57 pre-existing prepare tests pass untouched.

## Evidence

Tests added in `extensions/agi/tests/test_rotate_prepare.py` (4 new):
- `test_prepare_perform_mirror_push_cleared`
- `test_prepare_perform_failed_push_stays_block_exact_cmd`
- `test_prepare_perform_repins_stale_meter_pin_cleared`
- `test_prepare_perform_never_repins_over_another_blocker`

`python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q` -> **61 passed**
(57 pre-existing + 4 new). Regression sweep of the rotate-self full flow,
closeout and recover: `test_rotate.py test_rotate_closeout.py
`test_rotate_recover.py test_rotate_g1517.py test_rotate_sm36_residue.py`
-> **366 passed**. Production lines (rotate.py, tests excluded,
`git diff --numstat`): 27 / ceiling 25 (under 2x; no re-brief needed).

Scope note: check 3's merge already produced a measured-result line before
this round (satisfies the claim's merge leg), so only the push + re-pin legs
were new code.

## Agent Notes
built g15 claim: prepare --perform now PERFORMS the mirror push (check1) and meter re-pin (check5) under --perform, printing 'cleared: <step> (<result>)' never a clear: hand line; failed clear stays BLOCK with exact cmd; only when every other check clean (no side effect before refusal). 61 prepare tests pass (4 new), 366 rotate regression pass. 27 prod lines/25 ceiling.
