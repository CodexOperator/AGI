---
id: hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
mint_id: f019f4cc65504db2b3e104ca40cf2f63
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-general-3
scaffold_hash: 8a62b56d10e58eb3
season: 2
testable_claim: _run_stage_proc wraps each stage in a named scope (mem_cap.unit_name) and stops that unit in a finally on normal return, the wall kill and an exception; a failing stop is one stderr line; wrap_argv without unit= is byte-unchanged; both merge-up-review stage prompts forbid grep -r / rg / find over .agi/ or the repo root
title: a workflow stage runs in a NAMED scope and stops it on every exit path, so no orphan (a repo-wide grep) outlives its stage; reviewer briefs never grep recursively
town: core
---
# hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit

## Measured
- goal:g7.33.19 row 60 (the Prime's [red] 20:4xZ 09-30, placed by sanctuary-master): a pi-free workflow stage left a repo-wide grep|head pipeline behind in its run-*.scope after the stage exited -- 5 orphans, ppid = the user manager, cwd MAIN, 2.8-6.8 h, grep in D state, 115 GB read, ~3 GB file cache refilled after every reclaim -> 4 memory reliefs + 2 PSI RED spells; the Prime stopped the scopes by systemctl --user stop.
- workflow.py `_run_stage_proc`: the stage argv is wrapped by `mem_cap.wrap_argv` into an ANONYMOUS `systemd-run --user --scope` (no --unit); on the wall it calls `proc.kill()` on the stage process only; on a normal return it touches nothing. A scope lives until its LAST process exits, so any child the stage agent left (a backgrounded or orphaned grep) keeps the scope and its I/O alive with nothing to stop it by name.
- `mem_cap.unit_name(prefix, name)` is THE one spelling of a transient unit name; `mem_cap.scope_argv` already takes `unit=`; `wrap_argv` does not.
- extensions/agi/workflows/merge-up-review.json: the review and verify stage prompts carry "NEVER author and run a probe ... rotate" but no line forbidding a recursive grep / rg / find over .agi/ or the repo root (it reaches the bind-mounted worktrees).

## CLAIM
1. Every workflow stage runs in a NAMED scope (`wrap_argv(argv, cap, cfg, unit=mem_cap.unit_name("agi-stage", <run key>/<stage label>))`), and `_run_stage_proc` stops that unit (`systemctl --user stop <unit>`, quiet, a stop failure is one stderr line, never a raise) in a `finally` on EVERY exit path: normal return, the wall kill, an exception. No stage leaves a live process in its scope.
2. The merge-up-review template (both stage prompts in merge-up-review.json; its derived .js too if it carries prompt text) says: NEVER grep -r / rg / find over .agi/ or the repo root -- diffs and named files only.
3. Callers that pass no unit (dispatch.py, heal.py) are byte-unchanged.

## Dispatch line
config-max: none new (the unit prefix `agi-stage` is a literal beside the existing `agi-` unit prefixes; if a `values.memcap` or `spawn` cell already names unit prefixes, use it) / template-max: CLAIM 2 is a TEMPLATE line in merge-up-review.json, no code / code: the one missing trigger -- stop the stage's own scope on stage exit.

## FALSIFIERS
F1 a fake stage (a tmp script on PATH standing in for pi) that backgrounds a long `sleep` child and exits 0: after `_run_stage_proc` returns, the fake systemctl on PATH never received `stop <that unit>` (must receive it exactly once, with the unit the wrap used).
F2 the same on the wall-kill path (a stage that outlives a tiny budget with no extensions) and on an exception path.
F3 a failing `systemctl stop` raises or changes the stage's return (must be one stderr line, same result).
F4 `wrap_argv` without `unit=` changes its argv for any caller (byte-compare the no-unit argv before/after).
F5 the review or verify prompt in merge-up-review.json still lacks the no-recursive-grep line.

## TESTS
extensions/agi/tests/test_workflow_stage_scope.py (NEW): fakes for systemd-run and systemctl on PATH in tmp dirs ONLY -- never the real user manager, a real unit, sudo or the live RAM dir; `timeout` on every subprocess. Neighbourhood: test_workflow*.py (the ones touching _run_stage_proc), test_ram_write_charge.py, test_bin_help_smoke.py.

## FILE SCOPE
extensions/agi/bin/workflow.py (`_run_stage_proc` and its caller's unit name only) · extensions/agi/bin/mem_cap.py (`wrap_argv` gains `unit=None`) · extensions/agi/workflows/merge-up-review.json (+ agi-merge-up-review.js only if it carries the prompt text) · extensions/agi/tests/test_workflow_stage_scope.py (new). Nothing else.

## CEILING
kids <= the cell spawn.parent_max_kids (one kid) · production NET <= +14 (workflow.py + mem_cap.py) · template +2 lines · test file <= 90 lines · pi-free parent and kid, 0 USD · a byte over a cap = rebrief the director BEFORE, never after · TWO-operand numstat <cut>..<tip before the paste commit>, labelled.
