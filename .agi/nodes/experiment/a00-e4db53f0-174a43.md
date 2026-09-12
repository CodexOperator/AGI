---
id: experiment:a00-e4db53f0-174a43
mint_id: e8e2f2c525c3446d85b86108b86a7430
type: experiment
parents:
  - hypothesis:l4-the-button-down-legal-hint-consults-is-legal-branch
next_edges: []
confidence: 0.95
edited_by: sensei-director
evidence_runs:
  - experiment:a00-e4db53f0-174a43
loop: hypothesis:l4-the-button-down-legal-hint-consults-is-legal-branch@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ca01e488a81d5eb6
season: 2
title: "_button_down_legal_hint consults branches.is_legal_branch: post/loop/town branches read NOT legal (grid commit would be SKIPPED), season main and master read legal"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e4db53f0-174a43

## Experiment

FIX-ONLY (goal:g15): `_button_down_legal_hint` must consult
`branches.is_legal_branch` (the ONE legality rule, L4.311) instead of
trusting any non-empty `git rev-parse` output.

**Before** (`extensions/agi/bin/rotate.py:6462-6478`): the hint returned
`f"legal on {out.stdout.strip()!r}"` for ANY non-empty branch — a worktree
on `season2/posts/x` (or any loop/town branch) printed `legal on
'season2/posts/x'` while the real `grid.py commit --all` refused.

**After** (same def, `rotate.py:6462-6481`): reads the branch, calls
`branches.is_legal_branch(branch)` (already imported at rotate.py:68), and
- returns `legal on <branch>` when True;
- returns `NOT legal on <branch> (grid commit would be SKIPPED — season
  main or master only)` when False;
- keeps the existing `no repo / unknown branch (grid commit would be
  SKIPPED)` line for empty/failed rev-parse.

No change to `branches.py` or `grid.py` — one rule, one module.

**Tests** — new file `extensions/agi/tests/test_rotate_legal_hint.py`
faking `git rev-parse` (monkeypatch `rotate.subprocess.run`):
post/loop/town branches each assert the exact `NOT legal on …` line;
`season2/main`, `season/s2`, `master` each assert the exact `legal on …`
line; empty output and non-zero return keep the exact SKIPPED no-repo line.

## Evidence

Command:

```
python3 -m pytest extensions/agi/tests/test_rotate_legal_hint.py -q
```

→ `8 passed in 0.20s` (tier-gate phantom-record notice only).

No-regression (existing dry-run tests intact):

```
python3 -m pytest extensions/agi/tests/test_rotate_tail.py extensions/agi/tests/test_rotate_legal_hint.py -q
```

→ `34 passed in 5.45s`.

Wider rotate suite (all `test_rotate_*.py` glob): `516 passed, 1 xfailed,
1 failed`. The single failure
`test_rotate_recover.py::test_detection_only_record_still_respawns_next_pass`
is a pre-existing timing flake (watch seat-dead respawn loop with real
sleeps) — it passes in isolation and is unrelated to this change
(`_button_down_legal_hint` is called only from the dry-run print at
rotate.py:11473; the recover test never reaches it).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
g15 fix round: _button_down_legal_hint previously echoed any non-empty branch as "legal on" promising a grid commit the real run skips on a post/loop/town branch. Deferred to branches.is_legal_branch (L4.311, the ONE rule) — no rule duplicated in rotate.py. Test file added driving the hint via faked git rev-parse on all six spellings plus the two SKIPPED edge lines. Existing dry-run tests untouched (verified 34 passed on test_rotate_tail + the new file). The one wider-suite failure is a pre-existing recover-suite timing flake, unrelated to this def.
<!-- THOUGHT:END -->

## Agent Notes
Implemented _button_down_legal_hint consulting branches.is_legal_branch; post/loop/town -> NOT legal line, season2/main|season/s2|master -> legal; 8 new tests pass, existing dry-run tests intact (34 passed)

Parent review SL7.36: ACCEPTED proved. Artifact read, not just the report: rotate.py _button_down_legal_hint now reads the branch and defers to branches.is_legal_branch (the ONE legality rule), returning legal only on True and the NOT legal (grid commit would be SKIPPED - season main or master only) line on False; the no-repo line is unchanged. Reproduced independently: python3 -m pytest extensions/agi/tests/test_rotate_legal_hint.py -q -> 8 passed, and is_legal_branch returns True only for season2/main, season/s2, master while post/loop/town spellings are False. Fix is implemented in the target file, satisfying the g15 build-order demand. Existing dry-run tests untouched.
