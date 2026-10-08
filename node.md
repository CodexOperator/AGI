---
id: experiment:a00-cee030e2-d2ccf8
mint_id: 2e3e71e27f3e470296e421f3c81ba164
type: experiment
parents:
  - hypothesis:l4-prepare-performs-its-three-clears-itself-and-prints-cleared-never-a-hand-step
next_edges: []
confidence: 0.9
edited_by: a00-c245faec
evidence_runs:
  - experiment:a00-cee030e2-d2ccf8
line_ceiling: 25
loop: hypothesis:l4-prepare-performs-its-three-clears-itself-and-prints-cleared-never-a-hand-step@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: A.push-wire:push issued with exact ("push","origin","HEAD:refs/agi/posts/p1") args, cleared printed, no BLOCK (conjunct1 wire). B.failed-push-blocks:push rc1 stays BLOCK with exact clear cmd, never cleared, exit 3 (conjunct2 gate). C.merge-conflict-blocks:conflict stays BLOCK naming path+merge cmd, never cleared (conjunct2 gate). D.second-prepare-idempotent:second --perform re-pushes nothing, re-pins nothing (pin content+mtime stable), no cleared line, exit 0 (conjunct3 wire). All 4 PASS run by parent.
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

Parent review (a00-c245faec): read the delivered bytes (commit b0b808c69, rotate.py +27, tests +102). 4 independent negative probes all PASS: push-wire, failed-push-blocks, merge-conflict-blocks, second-prepare-idempotent. Claim assumes performed under --perform (rotate-self pre-flight default); bare prepare/dry-run still lists, unchanged. Conjunct1 merge leg pre-existing (F14). Caveats: 27/25 prod lines (2 over; under 2x=50 so no re-brief per ceiling clause); the push+re-pin defer until every OTHER check is clean (conservative, no side-effect-first) so a single --perform with a pending merge does not do all three in one pass, completed on the next pass. Accept proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent version: accepted as proved after reviewing the delivered commit b0b808c69, not the result file. The kid implemented both missing performs (mirror push check1, meter re-pin check5) under --perform and printed cleared with a measured result. I ran 4 of my OWN negative probes and all passed, including the two falsifiers that matter most: a failed push reports BLOCK plus exact command not cleared, and a second prepare is idempotent. The guard requires every OTHER check clean before any side effect (P1-a), so a pending merge defers the push and re-pin to the next pass, completed before rotate-self spawns. The merge leg (check3) was already performed (F14); the new bytes scope matched the claim; evidence self-linked; title real; probes recorded. 27 of 25 lines, under the 2x re-brief threshold. No re-brief needed.
<!-- THOUGHT:END -->
