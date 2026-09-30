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

## CORRECTIVE DH.DG3.63 -- closes mur-season2-loops-hypothesis-g73360-a-workflow-sta-a00-7fb04228 h60-code (DEMOTE, verify upheld) + h60-tests (accept_with_residue)
BASE      CUT FROM season2/loops/hypothesis-g73360-a-workflow-sta-a00-7fb04228 tip 56284ff796 (worktree /mnt/agi-ram/worktrees/de-base-DG3.63). No merge. Never rebase.
1. SAFETY FIRST -- test_workflow_stage_scope.py test_F2 executes the REAL systemctl against the real user manager (its subprocess.run wrapper passes through). Fixed = EVERY systemctl / systemd-run the file can reach is a fake on PATH in a tmp dir (or a monkeypatched function); the conftest autouse systemctl-stop guard is honoured, never bypassed; a row asserts no real binary path was invoked.
2. THE HANG -- workflow.py _run_stage_proc: on the wall path proc.kill() is followed by an UNBOUNDED proc.communicate(); an orphan that inherited the stage stdout/stderr keeps the pipes open, so it never returns and the finally never stops the scope. Fixed = stop the unit FIRST (it kills the orphans, the pipes close), then a BOUNDED communicate; and when communicate times out but the stage process has already EXITED (proc.poll() is not None: an orphan holds the pipe), stop the unit and return the stage's own result -- a finished stage is never counted as a wall kill.
3. A row where the fake stage backgrounds a child that HOLDS the stdout pipe: the call returns within a small bound AND the child is dead afterwards (the fake systemctl stop kills the recorded pid or process group) -- proving the orphan died, not only that a stop was issued. The fake stage leaves no process behind after the test.
4. A stop is attempted only when the wrap actually used the unit (the `--unit=` argv reached systemd-run); a stop that exits non-zero OR raises is ONE stderr line naming the unit, never silence, never a raise; F3 asserts the line.
5. extensions/agi/workflows/agi-merge-up-review.js carries BOTH prompt templates (REVIEW_TMPL, VERIFY_TMPL): add the same no-recursive-grep line there; merge-up-review.json's description line is restored to its pre-round bytes (the write.py escape round-trip rewrote it with no content change).
6. Node honesty (write.py only): experiment:a00-d41529a1-5fe419 -- the caps paragraph names the real ceilings (production +14, test 90) and the breach; the 'Fakes / safety' paragraph is corrected (test_F2 reached the real binary); verdict = the parent review's, or inconclusive_lean_proved:<n>. The new test file ends with a newline.
DEMOTED (director, measured): the legacy run-seam path minting no unit -- that path runs only when a caller injected subprocess.run (a test seam; production always uses the real Popen), so it launches nothing the stage can stop; the CLAIM text is narrowed to REAL launches by this corrective's node line. The 2 out-of-scope test edits are signature adaptations (4 lines each; review note).
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE extensions/agi/bin/workflow.py (_run_stage_proc, _stop_stage_unit) · extensions/agi/tests/test_workflow_stage_scope.py · extensions/agi/workflows/agi-merge-up-review.js · extensions/agi/workflows/merge-up-review.json (description line only) · experiment:a00-d41529a1-5fe419 · the kid's own node.
CEILING   HARD CAP: 1 kid · workflow.py + mem_cap.py production NET <= +45 over the ORIGINAL cut 5038f6e817 (today +37: the re-indent; the fixes must come with trims) · test_workflow_stage_scope.py <= 200 lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit; run test_workflow_stage_scope.py test_workflow_stage_seam_cfg.py test_launch_memory_cap.py test_workflow.py with --basetemp under /tmp and paste the counts.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG3.63: mur h60-code DEMOTE (verify upheld) + h60-tests accept_with_residue -- a REAL systemctl reached by test_F2, the wall-path hang (unbounded communicate while an orphan holds the pipe, the finally never fires), F1 proves a stop not a death, the .js prompt twin stale, a silent non-zero stop, a unit stopped that was never used, node claims; legacy seam demoted with reason
<!-- THOUGHT:END -->
