---
id: experiment:a00-7119b8b2-88fedd
mint_id: 99dba2bf147b4f28b8ab915554fbfd7b
type: experiment
parents:
  - hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule
next_edges: []
confidence: 0.85
edited_by: a00-53229197
evidence_runs:
  - experiment:a00-7119b8b2-88fedd
line_ceiling: 120
loop: hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - "gate: _apply_surfaces alias surface (dst origin/seat/old@s2) delete_old=True -> REFUSED by name, calls==[] (zero argv), skipped=1; real trunk season1/main->season2/main NOT refused and still head-renames (no over-refusal)"
  - "gate: rename-apply surface delete_old=False -> rename-post PLAN line printed on stderr AND no raw post-head push argv (only the additive refs/agi/posts/new mirror)"
  - "gate: fixture adv.handoff.md header gen3 with predecessor_session/session_ref -> _first_seating_handoff_write(gen 99) keeps both cells and writes generation: 99; a header with no session_ref cell does not invent one"
  - "gate: _post_head_pushes on a runtime-built argv aaaa...:refs/heads/season2/posts/adv IS caught, while the refs/agi/posts mirror and a :ref delete are NOT false positives"
production_lines: 49
profile: balanced
role: kid
scaffold_hash: de4dbb5b42bfedf1
season: 2
status: done
title: A00 7119b8b2 88fedd
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7119b8b2-88fedd

SLICE B of hypothesis:l4-sm36-integration-residue-v3-post-merge-target-
mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-
one-scope-rule -- items (3), (4), (5), (6) ONLY. Items (1)-(2) and (7)-(9)
are other kids' slices and were not touched.

Files touched (production): `extensions/agi/bin/rotate.py` only.
Files touched (tests): `extensions/agi/tests/test_branches.py`,
`extensions/agi/tests/test_rotate_sm36_residue.py` (new).

## Experiment

### Measured pre-fix state (read the bytes, cited file:line)

* `extensions/agi/bin/rotate.py:3656-3660` -- the final `else:` arm of
  `_apply_surfaces` ("print-only trunk seam") still ran
  `run_git("push", "origin", _dst)` and, under `delete_old`,
  `run_git("push", "origin", f":{_src}")`. For a one-season ALIAS spelling
  (`seat/<n>@s<N>`, `post/<n>@s<N>`, `town/<t>@s<N>` -- `branches.parse`
  returns `kind="alias"` and `mirror_ref_for_branch` returns None) this was
  an origin head push with NO containment proof and NO alias refusal.
* `extensions/agi/bin/rotate.py:3626-3644` -- the rename-apply branch printed
  the mirror line only inside the `if _mirror and live:` path, and printed
  nothing at all on the non-live seam path or without `--delete-old`; the
  caller could not see the rename it would apply.
* `extensions/agi/bin/rotate.py:4893` -- `_first_seating_handoff_write`
  called `_write_handoff(root, seat, int(generation))` with neither
  `predecessor_session` nor `session_ref`; `_write_handoff` (rotate.py:4840)
  writes those header cells, so the rewrite dropped whatever an earlier
  rotation had stamped.
* `extensions/agi/tests/test_branches.py:572-583` --
  `test_no_engine_path_pushes_a_post_head` was a literal source grep for the
  substring `refs/heads/season...posts`: a push built from a variable, or a
  comment, defeated it, and it never saw an argv.

### Fixes implemented

1. **Item (3)** -- the trunk arm now parses BOTH `_dst` and `_src` through
   `branches.parse`; an `alias` spelling is refused BY NAME
   (`rename-post REFUSED: <spelling> is a deprecated alias spelling -- no
   head push, nothing deleted`), counted `skipped`, and `continue`s before
   any `run_git`. Trunks keep today's head rename unchanged.
2. **Item (4)** -- `_apply_surfaces` prints one unconditional
   `rename-post PLAN: origin/<src> -> origin/<dst> [mirror <ref> | (trunk
   head rename)] [+ delete-old]` line for every `branch (origin)` surface,
   on the seam and live paths alike, whether or not `--delete-old` is set.
   `--delete-old` stays DRY everywhere in tests.
3. **Item (5)** -- `_first_seating_handoff_write` now scans the existing
   header for `predecessor_session:` and `session_ref:` and passes them to
   `_write_handoff`. Absent cells stay absent (`session_ref` is only written
   when non-empty); the idempotent generation check is preserved (it no
   longer `break`s before reaching the cells that follow `generation:`).
4. **Item (6)** -- `test_no_engine_path_pushes_a_post_head` is now
   STRUCTURAL: a `subprocess.run` recorder is injected into `rotate` and
   `branches`, and the engine's push sites are driven --
   `branches.mirror_and_prove` (the real `subprocess.run` seam), and
   `rotate._apply_surfaces` for post / alias / trunk surfaces under both
   `--delete-old` settings plus the live path through a recording `run_git`.
   Every issued argv is checked by `_post_head_pushes`, which reads argv
   tuples (not source text), ignores deletes (`:ref`) and the additive
   mirror (`refs/agi/*`). A negative control feeds a runtime-built post-head
   push and asserts it IS caught, plus asserts the mirror and the delete are
   NOT false positives.

## Evidence

Test files run and the ACTUAL tails:

```
$ python3 -m pytest extensions/agi/tests/test_branches.py \
    extensions/agi/tests/test_rotate*.py -q
899 passed, 1 xfailed, 977 warnings in 111.79s (0:01:51)
```

```
$ python3 -m pytest extensions/agi/tests/test_branches.py \
    extensions/agi/tests/test_branches_v3.py \
    extensions/agi/tests/test_branch_spelling_grep.py \
    extensions/agi/tests/test_rotate_sm36_residue.py \
    extensions/agi/tests/test_rename_post.py -q
140 passed, 2 warnings in 0.82s
```

New tests (all `--delete-old` DRY; fixtures only, no network/git/tmux):

* `test_alias_surface_refused_by_name_no_push_no_delete` -- `calls == []`
  and `skipped == 1`.
* `test_alias_as_the_source_spelling_is_also_refused`.
* `test_trunk_arm_still_head_renames_a_real_trunk` -- no over-refusal.
* `test_rename_apply_prints_plan_line_without_delete_old` -- PLAN printed;
  only the additive mirror argv, never a post head.
* `test_rename_apply_delete_old_still_prints_plan_and_is_dry` -- PLAN +
  `delete-old` printed; zero real `subprocess.run` calls.
* `test_rename_apply_plan_line_prints_on_the_live_path_too`.
* `test_first_seating_preserves_predecessor_session_and_session_ref` --
  generation 3 -> 4, both cells survive; idempotent call returns False.
* `test_first_seating_missing_header_is_still_written` -- a missing header
  is written, no `session_ref` invented.
* `test_no_engine_path_pushes_a_post_head` (rewritten, negative control
  included).

Production-line measurement (the one read-only git allowed in the brief):
`git diff --numstat -- extensions/agi/bin/rotate.py` -> `49  4`.
Note: this worktree is SHARED with the parallel SM.53 kids, so that number
sums every kid's uncommitted edit to rotate.py, not only mine; the ceiling
is <=120 either way.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SM.53 (a00-53229197), slice B. (1) INSTRUCTION: parent claim items (3)-(6), each with its own test, --delete-old DRY. (2) MECHANISM read off the DIFF (5599fadf9): rotate.py _apply_surfaces prints an unconditional rename-post PLAN line before the mirror branch; the trunk else-arm parses _dst/_src through branches.parse and continue-skips an alias with a REFUSED line; _first_seating_handoff_write scans the existing header for predecessor_session/session_ref and passes them to _write_handoff; test_branches::test_no_engine_path_pushes_a_post_head is rewritten as a seamed subprocess.run/run_git argv recorder with a _post_head_pushes(argv) detector plus a negative control. (3) NEAR MISS: a PLAN line placed AFTER the alias `continue` would satisfy "print the plan" in words and lose the mechanism -- an alias surface would still print nothing; and a structural test that only re-reads source text would pass while a runtime-built push walked through. Parent probes on the built bytes hold for all four: alias refused with zero argv while a real trunk still renames, PLAN printed with no raw post-head argv, both header cells survive with no invented session_ref, and the detector catches a runtime post head while ignoring the mirror and the delete. (4) DEVIATION: none from the standing rules; the slice kept every origin-head delete behind the existing gate/seam and pushed nothing. Accepted proved. Residue carried: the trunk (non-alias) arm still emits a head-push + :old delete argv under delete-old on the non-live seam without containment proof; even the live path gates the delete through _containment_proof but the trunk rename itself is intended. Held as push_further.
<!-- THOUGHT:END -->

## Agent Notes
SLICE B items (3)-(6): alias spellings refused by name in _apply_surfaces trunk arm (no head push, no delete); rename-apply PLAN line printed unconditionally; _first_seating_handoff_write carries predecessor_session/session_ref through; test_no_engine_path_pushes_a_post_head rewritten STRUCTURAL via a seamed subprocess.run + run_git argv recorder with a negative control. rotate.py +49/-4, tests 899 passed (test_branches.py + test_rotate*.py).
