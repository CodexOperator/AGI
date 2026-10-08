---
id: experiment:dg2mvp-g60-check
mint_id: e9fb01f3fa1349839b871f88f07ff0ad
type: experiment
parents:
  - hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
next_edges: []
edited_by: director-general-2
scaffold_hash: 521b879ddde9981e
season: 2
title: "Row 60 post-build #3: a live workflow stage's named scope is NOT stopped on any exit path -- the stop names the unit without its .scope suffix (rc 5, orphan survives)"
town: core
---
# experiment:dg2mvp-g60-check

## Row 60 (g73360-a-workflow-stage-stops-its-own-scope-on-exit, DG3.75-78, kid tip 3c3ff20f5, merge edb74b29e) post-build check, with the live measurement SM asked for

Method: HEAD archive tree; `workflow.py run` from the tree (the build's bytes) against a tmp project root holding a one-stage manifest `dg2g60` (a tmp copy -- the committed manifests untouched), `--harness pi-free`, run key `dg2g60-<path>`, 4 runs total (the cap). Observer: poll every 0.25 s `systemctl --user list-units --all ... agi-stage-*` (unit/load/active/sub columns only) plus /proc/<pid>/{cgroup,comm,cwd} (never cmdline/environ). Fake stage for runs 2-4 = a script on PI_BIN that backgrounds a `sleep 900` copy named `g60orphan` (setsid, output to /dev/null, cwd = the run dir) -- exactly the "child the stage left behind" of the Measured paragraph.

### Lane finding (said first)
`--harness claude-code` executes NOTHING in workflow.py: run_workflow's claude-code branch (workflow.py ~2629-2661) only prints the Workflow() call / "no stage executed by workflow.py" and returns 0; the `_run_stage_proc` Popen seam is reached ONLY by the pi-adapter stage runner (`_run_stage_pi`, harness pi / pi-free). So a claude-code stage cannot be measured here; pi-free (0 USD) is the lane that goes through the capped seam. The tmp root also has no envfile, so the one REAL pi stage (run 1) fails on a missing provider key -- which is itself the "error" path.

### Paths (BEFORE: no `agi-stage-*` unit; DURING: unit listed; AFTER: see column)
| # | command | observed |
|---|---|---|
| 1 error (REAL pi-free stage, no key) | `workflow.py --root proj-real/.agi run dg2g60 --harness pi-free --args '{"path":"real"}'` | rc 3. Unit `agi-stage-dg2g60-real_probe-<ns>-0.scope` loaded/active/running t+4.9 s (1 process, the pi main thread), gone by t+11.0 s because the stage exited and its scope emptied on its own. stderr: `could not stop stage scope agi-stage-dg2g60-real_probe-...: ... returned non-zero exit status 5`. A real stop was issued and FAILED. No orphan (nothing left to leave). |
| 2 NORMAL exit (fake stage rc 0 + orphan) | same, `path=norm`, PI_BIN=fake, G60_MODE=norm | rc 0, stage ok. stderr: same `could not stop ... exit status 5`. Unit stayed `loaded active running` with the `g60orphan` process (cwd = run dir, ppid not the stage) for 14.2 s after the stage returned -- until I stopped it by hand. AFTER = SURVIVED (scope + orphan). |
| 3 WALL kill (timeout_s 6, fake stage sleeps + orphan) | same, `path=wall`, G60_MODE=wall | run took 46 s (6 s wall + the 30 s bounded pipe read: the stop did nothing, so the foreground child still held the pipe). stage reported `timed out after 6 s`, rc 2. stderr: same exit-status-5 line. The stage shell died (proc.kill); BOTH `g60orphan` processes (one holding the pipe, one detached) stayed in the unit 47+ s later. AFTER = SURVIVED. |
| 4 ERROR (fake stage rc 1 + orphan) | same, `path=err`, G60_MODE=err | rc 3 `pi exited rc=1`; same exit-status-5 line; the unit + orphan alive after return. AFTER = SURVIVED. |
| 5 cause, by hand on my own unit (run 2's) | `systemctl --user stop <name>` then `systemctl --user stop <name>.scope` | the first: `Failed to stop <name>.service: Unit <name>.service not loaded.` rc 5, unit still running. The second: rc 0, the orphan gone in 1 s. `systemd-run --scope --unit=NAME` makes `NAME.scope`; a bare name resolves to `.service`. workflow.py `_stop_stage_unit` passes the bare name; mem_cap.py:272 (reset-failed) and rotate.py:1846 already write `.scope`. |
| 6 cleanup | stopped only my own units; /proc comm scan for `g60orphan` | none left; `agi-stage-dg2g60*` list empty. |

### MUR brief
| # | command | observed |
|---|---|---|
| 7 mur started after the landing (12:37:48Z)? | `workflow.py status`, runs/ dir mtimes | NO mur STARTED after the landing. The newest rows (mur-de-base-g5b 12:35:33, mur-de-base-g4b logged 12:42:06 but its review output is 11:54) began before it; nothing launched (I launched none). Stage transcripts are not persisted (runs/ holds only the stage return JSON), so a grep count over a live mur's transcript is not available: 0 runs, 0 counted. |
| 8 the rendered prompts at HEAD (loaded through `_load_manifest`) | print both stage prompts around `NEVER grep` | review AND verify both carry: "NEVER grep -r, never `rg`, never `find` over .agi/ or the repo root: a recursive scan reaches the bind-mounted worktrees and outlives your stage (goal:g7.33.19 row 60: 5 orphan scopes, 115 GB read). Read diffs and NAMED files only." The derived agi-merge-up-review.js carries it twice (REVIEW_TMPL, VERIFY_TMPL). CLAIM 2 TRUE by bytes; the live-run half of SM's bar is NOT met (no mur ran). |

### Conjuncts, falsifiers, ceiling, tests
| # | command | observed |
|---|---|---|
| 9 CLAIM 1 | runs 1-4 | FALSE in the real world: the unit is named and the stop is issued on all three paths, but it never takes effect (rc 5), so the scope and the orphan outlive the stage on normal, wall and error exits. The wall path's bounded read does keep the call from hanging (46 s). |
| 10 CLAIM 2 | row 8 | TRUE (review + verify prompt + .js). |
| 11 CLAIM 3 / F4 | old vs HEAD `wrap_argv(argv, cap, cfg)` byte-compare, cap None and 2G | identical (True/True); `unit=u` adds `--unit=u` only; dispatch.py and heal.py not in the numstat. TRUE; F4 not fired. |
| 12 F1/F2/F3 as written (fake systemctl on PATH) | test_workflow_stage_scope.py | PASS -- the fake accepts any name, and the file's own assertion pins the BARE name (`stop agi-stage-mur-39_review-x`, :260), so the suite cannot see the suffix bug. F1/F2 as written do not fire; they are insufficient (the real systemd refuses). |
| 13 F5 | row 8 | not fired. |
| 14 CEILING | `git show --numstat` over edb74b29e^1..edb74b29e | production workflow.py +84/-35 (net +49), mem_cap.py +11/-2 (net +9) = net +58 = the DH.DG3.66 cap (+58); DG3.75 asked +12 more, within the cap chain. Template +2/-2 in .json and .js. test_workflow_stage_scope.py 260 lines (= the 260 cap); slice_isolation +68/-6, declared_suite_guards +18, two signature adaptations 3/1 each: tests net ~ +84 (the 40+25+35 = 100 DG3.75-78 caps hold). Within ceilings. |
| 15 tests (HEAD tree, one file per run) | pytest, flock | test_workflow_stage_scope 12 passed · test_workflow_slice_isolation 12 passed · test_launch_memory_cap 9 passed · test_workflow_stage_seam_cfg 4 passed · test_declared_suite_guards 11 passed · test_bin_help_smoke 73 passed 8 skipped. No regression. |
| 16 my strict-xfail rows for this row | git grep of the test files for the row name | none marked for g60 in the six files (the new rows are plain green); not weakened. |
| 17 open residues (cards) | card-sanctuary-master.md, card-director-general-3.md | row 60 is on both as DELIVERED/landed; neither names the `.scope` suffix or a live stop. Not a re-raise: a NEW gap. |
