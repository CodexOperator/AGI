---
id: experiment:a00-71ee7ec5-423ae5
mint_id: 9e2ef8c6f8de470a9fdc8fc6593591d3
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.8
edited_by: a00-325f2fa0
evidence_runs:
  - experiment:a00-71ee7ec5-423ae5
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 889ae3b71d17eff0
season: 2
title: A00 71ee7ec5 423ae5
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-71ee7ec5-423ae5

FIX-ONLY round L4.312, KID A of 4 — `cli.py branch-reshuffle` region ONLY
(plus `tests/test_branch_reshuffle.py`). Target
`hypothesis:l4-branches-follow-the-season-grammar` clause 3, the one
migration script. The claim is a BUILD order (g15), so I measured the
pre-fix state, implemented, then proved on the built bytes (hermetic fixture
+ real-tree dry-run).

## Experiment

### Pre-fix state (mur-44, re-verified on this checkout)

1. `--delete-old` only printed `git push origin --delete <old>` via
   `_post_rename_print(..., True)` and never executed anything -> returned 0
   after printing.
2. `--apply` not resumable — re-running after a partial apply hit a failing
   `git branch -m`; no origin-moved check, and no persisted dry-run plan.
3. `git branch -m` never re-points the upstream; nothing set `-u`.
4. `--kinds towns` matched NOTHING on the live tree: the job builder used a
   SECOND grammar `_RS_TOWN_RE = ^town/(.+?)/season/s(\d+)$` which does not
   match the live legacy spellings `town/streaming-suite@s2` /
   `town/web-app-suite@s2` (`branches.parse` returns kind 'alias', canonical
   `season2/<t>/season1/main`; the regex returned None).
5. post-rename (`post/<name>@s<N>`) and branch-reshuffle (canonical
   `season<N>/posts/<name>`) disagreed on the seat-branch target.

### What I implemented (in-region)

`extensions/agi/bin/cli.py` branch-reshuffle region:

* **Grammar**: deleted the second grammar (`_RS_SEASON/TOWN/LOOP/SEAT/LEGACY`
  regexes). `_reshuffle_canonical` now routes an ALIAS through
  `branches.parse(b)["canonical"]` (branches.py is the sole grammar owner),
  plus the single escape hatch `_RS_POST_RE` `^post/(.+?)@s(\d+)$` for
  post-rename's intermediate seat target, finished via `post_branch` so
  post-rename THEN branch-reshuffle COMPOSE. `_RS_TOKEN_RE` only DETECTS
  legacy-looking tokens in prime-owned cell prose; the rewrite DECISION still
  goes through `branches.parse`.
* **defect 1**: `--delete-old` now EXECUTES each listed delete
  (`git push origin --delete <old>`) after the `sessions/verified.stamp`
  refusal (exit 3 preserved, separate step, never implied by `--apply`),
  one branch per `[APPLY]` line printed.
* **defect 2**: new plan file `sessions/branch-reshuffle-plan.json` (mirrors
  `post-rename-plan.json` shape) records each old branch's `origin_sha` at
  dry-run; `--apply` re-runs load it and REFUSE BY NAME when origin's tip of
  a source branch has moved (`ERR: --apply REFUSES <old>: origin tip moved
  since the plan was taken`) and SKIP already-renamed branches (old absent,
  new present) instead of failing the `git branch -m`.
* **defect 3**: after the push, `git branch --set-upstream-to origin/<new>
  <new>` re-points the upstream to the NEW remote name.
* **defect 5/contract**: make the shared seat-target handling in
  `_reshuffle_canonical` (post-rename side is the sibling's region, so only
  the branch-reshuffle half is wired here). Last line of `--dry-run` is the
  one-line runbook note owed to the crons region (KID D).

### Tests (hermetic, tmp fixture repo — bare origin + MAIN + 2 worktrees)

Extended `_build_repo` with a `.gitignore` for `.agi/sessions/` (so the plan
file is the same gitignored scratch post-rename already treats as such) and
added six tests in `test_branch_reshuffle.py`:
* `test_delete_old_executes_deletes_when_stamp_present` (defect 1)
* `test_apply_sets_upstream_and_is_resumable` (defects 2+3)
* `test_apply_refuses_origin_moved_by_name` (defect 2)
* `test_dry_run_plans_live_legacy_town_at_alias` (defect 4 — town/<t>@s2)
* `test_post_rename_output_post_at_composes` (defect 5)
* `test_dry_run_last_line_is_runbook_note` (KID D contract)

Pytest last line:
```
11 passed in 3.32s
```
Merged-relevant suite (`test_branch_reshuffle.py` + `test_cli.py`):
```
30 passed in 3.90s
```

## Evidence

Real-tree `--dry-run --kinds main,posts,towns` from this worktree — defect 4
now plans BOTH legacy town mains (7 jobs: 2 main + 3 post + 2 town):
```
branch-reshuffle (season=2): 7 legacy branch(es)
[DRY ] branch rename (local): git branch -m season/s2 season2/main
[DRY ] branch rename (local): git branch -m seat/sanctuary-director@s2 season2/posts/sanctuary-director
[DRY ] branch rename (local): git branch -m seat/sanctuary-helper@s2 season2/posts/sanctuary-helper
[DRY ] branch rename (local): git branch -m seat/sensei-director@s2 season2/posts/sensei-director
[DRY ] branch rename (local): git branch -m town/streaming-suite@s2 season2/streaming-suite/season1/main
[DRY ] branch rename (local): git branch -m town/web-app-suite@s2 season2/web-app-suite/season1/main
...
  nodes/.geometry/ladder.md:62: town/web-app-suite@s2 -> season2/web-app-suite/season1/main
  nodes/.geometry/ladder.md:155: season/s2 -> season2/main
  nodes/.geometry/rotations.md:170: seat/x@s2 -> season2/posts/x
NOTE: remote delete is NOT implied by --apply; run --delete-old separately, and only after the suite is green.
dry-run: nothing changed
runbook: a rename needs one `crons.py apply` within the 5-min grid_sync window, else `branch_push` keeps pushing the old name
```
The last line is the runbook note (KID D contract), kept to one line.

## Caveats

* Defect 5 (composition) could only be wired on the branch-reshuffle half —
  post-rename is a sibling's region and was not edited; the end-to-end
  post-rename-then-branch-reshuffle run and the wrong-order refusal are
  therefore not proven here. Proven only that `post/<name>@s<N>` is
  canonicalised to `season<N>/posts/<name>`.
* `print("  -- already renamed")` line is correct behavior, not noise: after
  a full `--apply`, origin still lists the legacy names (delete-old is
  separate), so a re-run reports each as skipped BY NAME.

## Agent Notes
KID A branch-reshuffle region: grammar now branches.parse-only (+_RS_POST_RE escape for post-rename output), --delete-old executes, --apply resumable+refuses origin moves by name, upstream set to new remote, --kinds towns matches live @s2 town branches (7 jobs on real tree), runbook note last line of dry-run. 11+30 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID (parent brief L4.312, KID A of 4): the five mur-44 defects in the cli.py branch-reshuffle region -- --delete-old executes nothing, --apply is not resumable and has no origin-moved check, renamed branches keep the OLD upstream, --kinds towns matches nothing because a SECOND regex parser builds the jobs, and post-rename/branch-reshuffle do not compose.
WHAT THE MACHINE ACTUALLY DOES, measured by the parent on the kid staged bytes: `pytest test_branch_reshuffle.py` -> 11 passed; `+ test_cli.py` -> 30 passed; the real-tree dry-run from the kid worktree now plans SEVEN legacy branches, including `master -> season1/main` and both live town mains `town/streaming-suite@s2`/`town/web-app-suite@s2` -> `season2/<t>/season1/main`; the last line of --dry-run is the one-line crons runbook note. `--delete-old` runs `git push origin --delete <old>` after the verified.stamp refusal (exit 3 kept).
THE NEAR MISS: adding one more regex for `town/<t>@s2` satisfies "make --kinds towns match the live town spelling" and LOSES the mechanism -- the cell-proposal detector `_RS_LEGACY_RE` would stay blind to the same spelling and the ladder/rotations proposals would keep missing the town cells. The kid deleted the whole `_RS_*` family and routes every rename decision through `branches.parse`, keeping exactly one escape hatch (`post/<n>@s<N>`, which branches.py does not know because post-rename is a sibling migration) finished via `post_branch`, so post-rename THEN branch-reshuffle compose.
DEVIATION FROM A STANDING RULE: --dry-run now WRITES `sessions/branch-reshuffle-plan.json`; the claim says dry-run "touches nothing". The file is gitignored scratch and is the resumption + origin-moved baseline defect 2 requires; recorded here rather than left silent.
PARENT REVIEW: accepted at inconclusive_lean_proved:80. Defect 5 is only half-wired (post-rename is KID-independent and was not edited), which is why this is a lean and not a proved. FLAG FOR THE PRIME: --apply --kinds main,posts,towns now INCLUDES `master -> season1/main`, and a later --delete-old would delete origin/master; that is in the Prime verbatim grammar but is NOT in the pre-fix 4-job plan, so it is a new consequence to read before the live run.
<!-- THOUGHT:END -->
