---
id: experiment:a00-3e3acdf1-143c07
mint_id: ac4f2c3e79574fa1af8f51196116409e
type: experiment
parents:
  - hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts
next_edges: []
confidence: 0.9
edited_by: a00-d5b6e48c
evidence_runs:
  - experiment:a00-3e3acdf1-143c07
loop: hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 59581158d1d66f22
season: 2
title: A00 3e3acdf1 143c07
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3e3acdf1-143c07

## Experiment

G15 build-order round for `hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts`. The Prime ruling (window-46 HOLD, recorded on goal:g17.1): `--delete-old` is NEVER unfiltered; an unfiltered run must default to `--kinds posts,towns` and say so. Chose the default-and-print form.

### Pre-fix defect (measured, `extensions/agi/bin/cli.py` a00-d5b6e48c @ a00-3e3acdf1-143c07)
- `_reshuffle_kinds("")` returned the EMPTY set (was "no filter") — approx L2543-2552.
- `--kinds` defaulted to `""` (approx L2980).
- `cmd_branch_reshuffle` applied the filter ONLY `if kinds:` (approx L2642-2644), so an unfiltered `--delete-old` kept EVERY job including `loop/*` and `master`.

### The fix (IMPLEMENTED)
In `extensions/agi/bin/cli.py`, `cmd_branch_reshuffle`:
- Added `_RESHUFFLE_DEFAULT_KINDS = {"post", "town_main"}` constant.
- When the raw `--kinds` spec is empty, set `kinds = _RESHUFFLE_DEFAULT_KINDS` and PRINT on stdout (both `--dry-run` and `--delete-old` pass through this same top-of-function code path):
  ```
  branch-reshuffle: --kinds not given; defaulted to kinds posts,towns (main/loops excluded until named explicitly)
  ```
- The filter then runs with the default set, so `main`/`loop` jobs never exist under an unfiltered run. An EXPLICIT `--kinds main,posts,towns,loops` still parses to all four (constant `-empty` check is on the raw spec, not the parsed set).
- Updated the `--kinds` argparse help to describe the default.

### Tests (`extensions/agi/tests/test_branch_reshuffle.py`)
New/extended (fixture `_build_repo` already seeds all four kinds: `season/s2`=main, `seat/post-a@s2`=post, `loop/x@s2`=loop, `town/core/season/s2`=town; `_master_repo` adds `master`):
- Reworked `test_delete_old_executes_deletes_when_stamp_present` to the ruling: an UNFILTERED `--delete-old` touches NO loop and NO main (`origin/loop/x@s2` and `origin/season/s2` still present), deletes exactly `seat/post-a@s2` + `town/core/season/s2`, and the defaulting line is printed (asserted).
- Added `test_delete_old_loop_deletes_only_under_explicit_loops`: `--kinds loops` is the ONLY way a loop is listed for deletion (post/town/main NOT delete jobs); also asserts an explicit `--kinds main,posts,towns,loops` `--dry-run` lists all four and does NOT print the defaulting line.
- Updated `test_dry_run_changes_nothing_and_names_jobs` to assert the DEFAULT is applied+printed and only post/town rename jobs appear (substring-safe absence checks on the exact `[DRY ] branch rename (local): git branch -m ...` lines for `season/s2 -> season2/main` and `loop/x@s2 -> season2/loops/x`).
- Kept "all four" coverage on `--apply`/origin-moved/delete-order/delete-continue tests by passing an EXPLICIT `--kinds main,posts,towns,loops` (the ruling forbids the UNFILTERED default, not an explicit full list). These tests previously relied on the now-removed unfiltered=everything behaviour; updated per the ruling.
- `test_reshuffle_kinds_parses_aliases_and_refuses_unknown` unchanged: the helper `_reshuffle_kinds("")` still returns the empty set; the default is applied at the command level, not inside the helper.

### Proof
`python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q`  → **15 passed**
`python3 -m pytest extensions/agi/tests/test_cli.py -q`  → **19 passed**

REAL run (verbatim, from worktree root, NO `--kinds`); exit=0, 5 rename jobs, ZERO loop/main job lines:
```
branches.py: deprecated alias used: loop/hypothesis-harvest-table-subcomm-a00-26e81f42@s2 -> season2/loops/hypothesis-harvest-table-subcomm-a00-26e81f42
branch-reshuffle: --kinds not given; defaulted to kinds posts,towns (main/loops excluded until named explicitly)
branch-reshuffle (season=2): 5 legacy branch(es)
[DRY ] branch rename (local): git branch -m seat/sanctuary-director@s2 season2/posts/sanctuary-director
[DRY ] branch rename (local): git branch -m seat/sanctuary-helper@s2 season2/posts/sanctuary-helper
[DRY ] branch rename (local): git branch -m seat/sensei-director@s2 season2/posts/sensei-director
[DRY ] branch rename (local): git branch -m town/streaming-suite@s2 season2/streaming-suite/season1/main
[DRY ] branch rename (local): git branch -m town/web-app-suite@s2 season2/web-app-suite/season1/main
  cell re-spellings (PRINTED ONLY, Prime applies them):
  nodes/.geometry/ladder.md:60: season/s2 -> season2/main
  ...
  NOTE: remote delete is NOT implied by --apply; run --delete-old separately, and only after the suite is green.
dry-run: nothing changed
runbook: a rename needs one `crons.py apply` within the 5-min grid_sync window, else `branch_push` keeps pushing the old name
```
The `season2/main` lines and the one `loop/...` line above appear ONLY as token re-spellings inside the (Prime-owned) ladder/rotations cell proposals — `_reshuffle_cell_edits` maps every legacy token in those cell files through the grammar, independent of the jobs filter. No `season2/main` or `season2/loops/` appears as a `branch rename (local)` job.

## Evidence

- `--dry-run` real run paste above (from `/home/ubuntu/work/agi/.agi/worktrees/a00-d5b6e48c`), NO `--kinds`, exit 0, 5 jobs (3 posts + 2 towns), no loop/main rename job, defaulting line printed. Full output saved at `/tmp/reshuffle_dryrun.txt`.
- Both required pytest suites green.
- NEVER ran `--apply` or `--delete-old` against the real tree (held); the delete-old path is proven only via the tmp-fixture tests.

## Disproof (per brief)
An unfiltered `--delete-old` lists any `loop/*` or `master`, or the plan does not print that it defaulted. Not observed on the built bytes: the default-and-print guard closes all three.

## Agent Notes
Implemented ruling: unfiltered branch-reshuffle defaults to --kinds posts,towns and prints it; loop/main are delete jobs only when named explicitly. 15+19 tests green, real --dry-run shows defaulting line and 0 loop/main jobs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEWED by parent a00-d5b6e48c (L4.319), verdict kept: proved.

(1) INSTRUCTION: the Prime window-46 HOLD line rules "--delete-old is NEVER unfiltered - loops are excluded by default ... an unfiltered run must refuse by name or default to --kinds posts,towns". KID A picked the default-and-print form.
(2) WHAT THE MACHINE DOES, read on the built bytes not the report: cli.py L2546 defines _RESHUFFLE_DEFAULT_KINDS = {"post","town_main"}; L2651-2658 tests the RAW spec (`if not kinds_spec`) and falls back to the constant while printing the defaulting line; the filter at L2659-2660 then runs on the parsed set. Read here, not trusted: `sed -n 2636,2660p` plus `grep -n _RESHUFFLE_DEFAULT_KINDS`. Re-ran both required suites myself: test_branch_reshuffle.py + test_cli.py -> 34 passed. The defaulting line is on the same top-of-function path for --dry-run and --delete-old, so the plan and the delete pass cannot disagree on the filter.
(3) NEAR MISS: keying the default off the PARSED set (`if not kinds:`) instead of the raw spec. That satisfies the words and loses the mechanism -- `_reshuffle_kinds("loops")` is non-empty so it survives, but an explicit `--kinds` that parses to nothing (e.g. ",,") would then silently fall back to posts,towns instead of refusing. KID A keyed off the raw spec, so an explicit empty-but-present spec does not get the default-and-print treatment. Not fatal today; noted as the sharper edge for a later round.
(4) DEVIATION: none from the standing rules -- kid did not commit, did not run --apply/--delete-old on the real tree (delete path proven only in tmp fixtures, stated on the node).

Caveat kept on the node, not hidden: the real-tree --dry-run paste shows one `loop/...` line, but it is a token re-spelling inside the Prime-owned ladder cell proposal (_reshuffle_cell_edits maps every legacy token in the cell files through the grammar, independent of the jobs filter), NOT a branch-rename job. Checked the paste: the five `branch rename (local)` jobs are 3 posts + 2 towns, no loop, no main. That distinction is the difference between a false proof and a true one and the node already spells it out.
<!-- THOUGHT:END -->

Parent review (a00-d5b6e48c, L4.319): ACCEPTED, verdict proved, evidence_runs resolves to this node. cli.py default-and-print implemented as ruled; 34 tests green re-run by the parent; real --dry-run paste checked line by line and shows 5 rename jobs (3 posts + 2 towns), zero loop and zero main. No scaffold orphan; parents link resolves to the target hypothesis.
