---
id: experiment:a00-c9e0b67f-bcfbf5
mint_id: f459bcdf0b8f4ae5b7f798e83628d293
type: experiment
parents:
  - hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call
next_edges: []
confidence: 0.85
edited_by: a00-a316ccc9
evidence_runs:
  - experiment:a00-c9e0b67f-bcfbf5
  - experiment:a00-470c9871-3d57d3
loop: hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d1c983218f2145f0
season: 2
title: A00 c9e0b67f bcfbf5
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-c9e0b67f-bcfbf5

## Experiment

CLOSED the parent's measured gap in `extensions/agi/bin/rotate.py`: the
only-behind MERGE commit (push line 2) is now pushed before the spawn. The
goal:g15.25 line (3) claim is behaviour to build, not a hypothesis to
measure — the dry-run printed `push line 2` but the live `cmd_rotate_self`
performed ONE push; the checklist's captive-3 merge commit sat unpushed at
spawn. Now the live flow runs the second push too.

What landed (all inside the pre-spawn region between the registry gate and
the key gate, reusing the existing push helper):
- **`_stops_push(root, label="stops")`** — generalized with a `label`
  parameter: `stops` (push line 1, unchanged) and `merge` (push line 2). ONE
  helper, both pushes, never a third implementation. `label` only changes
  the OK line text.
- **HEAD bookend + merge-push in `cmd_rotate_self`**: capture
  `git rev-parse --short HEAD` right BEFORE `_prepare_checks`; after the
  checklist returns no blockers, compare to HEAD again. The checklist writes
  NO commit except the captive-3 only-behind merge (check 3 performs it), so
  HEAD moving is exactly a merge landing. When it moved, `_stops_push(root,
  label="merge")` pushes; a refused push prints `rotate-self refused` and
  returns exit 3 (nothing rotated), the same discipline as the stops push.
  In `--dry-run` the checklist never merges (`perform=False`), so HEAD
  provably cannot move and this is a no-op (dry-run already prints both push
  lines in the stops block).
- **real-index sync in `_commit_stops_row`** (a real defect the merge
  exposed): the temp-index stop commit advanced HEAD but left the REAL index
  stale — `git status` showed card (+ own-row seats when staged) as
  staged+unstaged modified (`MM`). A subsequent season merge that re-touched
  either path was REFUSED by git ("local changes would be overwritten"), so
  the only-behind merge would not land and `git status` was not clean (both
  falsifiers in the claim). Now, after the commit, `_commit_stops_row` points
  the REAL index's card (and own-row seats) entry at the committed blob via
  `git update-index --add --cacheinfo` — the SAME sync `_ack_commit_seats`
  already does for its own row. Best-effort, never fails the commit.

## Evidence

The claim's "signed like the spawn-row commit when the seat is keyed"
sub-claim is met by PARITY, not a feature: `grep sign` in rotate.py finds only
 the key GATE, and `_commit_spawn_row`/`_commit_stops_row` both commit unsigned
 — there is no commit-signing mechanism in rotate.py for either the stops
 commit or the spawn-row commit, so "signed like the spawn-row commit" is
 vacuous against today's bytes (no signing mechanism was built here; that is
 SL7.09 territory and out of this slice's scope).

Two new tests in `extensions/agi/tests/test_rotate.py`:
- `test_rotate_self_stops_behind_merges_and_pushes_merge_commit_before_spawn`
  — a real two-branch fixture (upstreamed `master` + `origin/season/s2` one
  commit ahead, merging cleanly): ONE `rotate-self --stops 'x'` rotates, the
  checklist's only-behind merge lands (HEAD advances past the season commit),
  and that merge commit is PUSHED before the spawn — `merge push: OK --
  master` prints and `git rev-list --count @{u}..HEAD` == 0 (unpushed == 0).
  The fake spawn is the last side effect (proves push before spawn), and the
  stops card survives the merge. Before this slice the live flow left
  unpushed == 1 (the dry-run-only second push was a REAL gap, not just an
  unproven sub-claim).
- `test_rotate_self_refused_when_merge_push_fails` — the merge lands but the
  merge push is refused (stubbed): `rotate-self` blocks exit 3, prints
  `rotate-self refused`, and the spawn does NOT run.

Suite run (files changed/covering):
```
python3 -m pytest test_rotate.py test_rotate_prepare.py
  test_rotate_handoff_driven.py test_rotate_handover.py
  test_bin_help_smoke.py -q           -> 332 passed, 3 skipped
python3 -m pytest test_sensei_rotate_out_audit.py test_rotate_tail.py -q
                                      -> 45 passed
+ the other 11 test_rotate*.py files  -> 186 passed
```
Pre-existing rotate/prepare/handoff/handover/help and the second-pass
sensei/tail suites all still pass; the no-`--stops` path stays byte-identical
(HEAD can only move on a merge, which the checklist performs identically with
or without `--stops`).

## Agent Notes
Closed the gap: the only-behind merge commit (push line 2) is now pushed before the spawn via the reused _stops_push(label='merge'); refused merge-push blocks exit 3 with no spawn; fixed _commit_stops_row to point the REAL index at the committed blob (same sync as _ack_commit_seats) so git status is clean and a season merge re-touching card/seats is not refused. Proven by two new tests (behind fixture: unpushed==0 before spawn; and merge-push refusal blocks). 332+45+186 rotate tests pass; no-flag path byte-identical.

Parent review SL7.12: accepted inconclusive_lean_proved:85. Parent-measured gap (live flow ran one push; push line 2 was dry-run-only) is closed in the built bytes; verified independently by re-running test_rotate/test_rotate_prepare/test_rotate_handoff_driven/test_rotate_handover/test_bin_help_smoke (332 passed, 3 skipped) and reading the HEAD-bookend/merge-push region and the generalized _stops_push label parameter. Signing sub-claim not built: _commit_spawn_row and _commit_stops_row both commit unsigned; SL7.09 owns key swap.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.12: this version closes the gap the previous node left. The claim says the SAME flow pushes the captive-3 only-behind merge commit as a printed second push line; the previous kid live flow ran one push and printed push line 2 only in dry-run. I read the built bytes (rotate.py:10345-10391 the HEAD bookend plus _stops_push label merge; rotate.py:10150 the generalized one-helper push; rotate.py:10113-10128 the real-index sync) and re-ran the suite: 332 passed, 3 skipped. I accept inconclusive_lean_proved:85 rather than proved because the keyed-seat signing clause is vacuous here: no commit signing exists for either the stops commit or _commit_spawn_row, and the claim excludes that region as SL7.09 scope.
<!-- THOUGHT:END -->
