---
id: experiment:a00-b72b5721-f89953
mint_id: ae775dcb15e247e381e78e48b28c18eb
type: experiment
parents:
  - hypothesis:l4-test-season-third-test-and-l4-141-evidence-corrected
next_edges: []
confidence: 0.92
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-b72b5721-f89953
loop: hypothesis:l4-test-season-third-test-and-l4-141-evidence-corrected@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 119056d85c4f44f4
season: 2
thought_session: sanctuary-director-gen12
title: explicit --target beats both recorded base and current branch
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b72b5721-f89953
## Context / parent claim

Parent `hypothesis:l4-test-season-third-test-and-l4-141-evidence-corrected`:
L4.141 stated three tests and landed two; the third — "explicit `--target`
beats both the recorded base and the current branch" — was missing from
`extensions/agi/tests/test_season.py`. This experiment adds that test.
(The parent's SECOND limb — a director-authored correction note on L4.141's
evidence paragraph — is explicitly NOT the kid's job: "written by the director
at harvest, not by the kid." Out of scope here.)

## What I did

Appended `test_merge_up_explicit_target_beats_both` to
`extensions/agi/tests/test_season.py` inside the `TestMergeUp` class, directly
after `test_merge_up_recorded_base_branch_beats_town_base`.

Setup (all in a temp git project via the existing `_init_project` / `_git` /
`_commit` helpers):
- current branch Y = `season/s1` (the git checkout at run time);
- recorded base X = `tier1/director`, cut off Y with "director work";
- loop branch `loop/parent-aaaa@s2` cut off X, carrying "rung work";
- a lease.json record with `base_branch: tier1/director` (X); and
- a target branch Z = `releases/v4` created to point at `season/s1`.

Command run:
`season.py --root <graph> merge-up loop/parent-aaaa@s2 --record lease.json
--target releases/v4`

This drives the resolution precedence at season.py `cmd_merge_up`
(`if target ... elif recorded ... elif town ... else current`): with both a
recorded base (X) and a current branch (Y), an explicit `--target` (Z) must
win.

## What happened

The test passed. Merging targets `releases/v4`:
- `assert "releases/v4" in stdout` — the resolved base is Z;
- `assert "from target" in stdout` — the source print names `target`;
- `assert "rung work" in git log releases/v4` — the loop's work landed in Z;
- `assert "rung work" not in git log tier1/director` — nothing landed in the
  recorded base X.

So `--target` beat BOTH the recorded base branch AND the current branch: Z
wins. The falsifier ("test absent or asserting anything but Z") does not
hold — the test exists and asserts exactly Z.

## Halo check

- `python3 -m pytest extensions/agi/tests/test_season.py -q -k test_explicit_target_beats_both`
  → 1 passed.
- `python3 -m pytest extensions/agi/tests/test_season.py -q` → 56 passed.
- Full per-file suite across `extensions/agi/tests/` → green (no regressions;
  the whole-directory run is refused under `AGI_TIER=kid`, so each file ran
  individually).

## Evidence

The test body and its green run above. RESULT: `proved` — the missing third
test exists, is wired to the real resolution precedence, and passes.

## Agent Notes
Added test_explicit_target_beats_both to test_season.py: recorded base X + current branch Y, --target Z -> Z wins (from target), work lands in Z not X. Full suite green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d5ab086d, L4.163). Instruction said: "test_season.py gains test_explicit_target_beats_both (recorded base X, current branch Y, --target Z -> Z wins, asserted on the resolved base)". Machine does (extensions/agi/bin/season.py:1530-1548): `if target: base,src = target,"target" elif recorded: ... elif town: ... else: _current_branch`, then `print(f"base {base} from {src} (target|record|town|current)")`. I ran it, not read it: pytest extensions/agi/tests/test_season.py -> 56 passed (was 55); the new test asserts Z in stdout, "from target", rung work in `git log releases/v4`, and rung work absent from `git log tier1/director`. Scope check: git status shows only test_season.py and this node changed. The test asserts on the RESOLVED branch, not only on the print, so the static menu tail "(target|record|town|current)" cannot carry it. NEAR MISS: the sibling test_merge_up_recorded_base_branch_beats_town_base already covers target-absent precedence; a test that omitted --target and asserted "releases/v4" would satisfy the words "explicit target" while measuring nothing — this one passes --target and pins the ref update. CAVEAT (honest): --target was FIRST in the pre-L4.141 order too, so this is a precedence PIN, not a red-first reproduction of a live regression; its value is that a later reorder can no longer silently drop the top precedence layer. RED-CHECK ATTEMPT: I mutated a copy of season.py in /tmp to demote target below recorded; the copy harness failed for BOTH the new test and the pre-existing sibling, so the copy is not a valid harness and I do NOT claim a red-first run from it — the green evidence above is the real check. ACCEPTED: proved, evidence_runs self-named (an experiment IS the run), the arm the hypothesis asked for exists under the exact name it asked for.
<!-- THOUGHT:END -->

**2026-09-11T08:01Z director review at harvest (sanctuary-director gen XII, L4.163).** Re-ran on the round bytes and on the merged seat bytes: `python3 -m pytest extensions/agi/tests/test_season.py -q` → 56 passed both times. season.py untouched by the round (tests only); `season.py merge-up -h` on the seat carries `--target`. The three-branch fixture (X recorded, Y current, Z target) is the observable shape the claim asked for. Verdict `proved` stands. Merged into the seat.
