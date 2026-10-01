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
testable_claim: _run_stage_proc runs each REAL capped launch (Popen seam, systemd-run usable) in a named scope (mem_cap.unit_name) and stops that unit in a finally on normal return, the wall kill and an exception; on the wall only a stage that ALREADY exited returns its own rc, every other wall path raises TimeoutExpired; the legacy run seam and the prlimit fallback stop nothing (no scope of theirs to stop); a failing stop is one stderr line; wrap_argv without unit= is byte-unchanged; both merge-up-review stage prompts forbid grep -r / rg / find over .agi/ or the repo root
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
1. Every REAL capped stage launch (the Popen seam, systemd-run usable) runs in a NAMED scope (`wrap_argv(argv, cap, cfg, unit=mem_cap.unit_name("agi-stage", <run key>/<stage label>))`), and `_run_stage_proc` stops that unit (`systemctl --user stop <unit>`; a stop that exits non-zero or cannot run is ONE stderr line naming the unit, never a raise) in a `finally` on every exit path: normal return, the wall kill, an exception. On the wall the stop goes FIRST and the pipe read is bounded; a stage that had ALREADY exited (an orphan holding its pipe) returns its own rc, every other wall path raises TimeoutExpired. NARROWED (DH.DG3.66, to the bytes): the legacy run seam (a caller-injected subprocess.run, a test seam) keeps the anonymous wrap and launches nothing this function can stop; the prlimit fallback has no scope, so no stop is attempted.
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

## CORRECTIVE DH.DG3.66 -- closes mur-season2-loops-hypothesis-g73360-a-workflow-sta-a00-3fde9a51 h60b-code + h60b-tests (accept_with_residue, verify upheld)
BASE      CUT FROM season2/loops/hypothesis-g73360-a-workflow-sta-a00-3fde9a51 tip 96a7dd7173 (worktree /mnt/agi-ram/worktrees/de-base-DG3.66). No merge. Never rebase.
1. workflow.py _run_stage_proc wall path (~:1933-1949) -- `proc.poll() is not None` is read AFTER the scope stop + proc.kill() + a 30 s wait, so it is always true: a real wall timeout returns a bare CompletedProcess with a negative rc, SKIPPING the caller's TimeoutExpired handling (~:2033-2042: _result_file_value + 'timed out after N s') and can be named 'killed by memory-cap'. Fixed = whether the stage ALREADY exited is read ONCE, BEFORE the stop and the kill (a done stage whose pipe an orphan holds); only that case returns the stage's own rc + whatever output the bounded read got; every other wall path raises TimeoutExpired. The comment states exactly that. Line-neutral: trim to pay for it.
2. test_workflow_stage_scope.py -- the fake `systemctl stop` kills the WHOLE scope (the stage AND the orphan), as a real stop does. Rows: (a) a stage that exited while an orphan holds the pipe -> the stage's own rc returns, the unit is stopped, nothing left alive; (b) a real wall timeout whose orphan SURVIVES the stop -> TimeoutExpired reaches the caller and the stage reads 'timed out', never memory-cap; (c) a prlimit-fallback launch (cmd[0] != systemd-run) -> NO stop is attempted. Each row FAILS on 96a7dd7173 (say how you checked).
3. test_workflow_stage_scope.py F6 -- deterministic: the fake stage's pids file exists before the budget starts (wait on it), never a 0.5 s race.
4. test_workflow_stage_scope.py:72 -- the spy WRAPS the conftest autouse guard (wrap the subprocess.run that is current when the test starts, never the stdlib original), so the guard stays on the chain; one row proves a real-shaped `systemctl --user stop` from this file still hits the guard.
5. extensions/agi/workflows/merge-up-review.json -- line 4 (description) byte-identical to its bytes at 5038f6e817 (the write.py round-trip 0c7541ffc4 turned its — escapes into literal dashes); paste `diff <(git show 5038f6e817:<file> | sed -n 4p) <(sed -n 4p <file>)` = empty. Both stage prompts keep their no-recursive-grep line.
6. Node honesty (write.py only): this hypothesis's testable_claim (:11) and CLAIM 1 (:24 region) narrowed to what the bytes do (the stage seam stops its own unit; the legacy run seam launches nothing it can stop). experiment:a00-d41529a1-5fe419: F3 row (:41, 'a stop returning 1 is silent') and the 'Fakes / safety' paragraph (:47) restated to the shipped code; the caps paragraph names the real ceilings and the breach (+58 vs +45); the stale cite at :100 fixed.
DEMOTED / NOTED (director): 'the finished-stage return discards output' folds into item 1; the tuned literal _WALL_STOP_GRACE_S beside a per-stage knob and 'the no-grep line lives in four carriers' -> findings rows on goal:g7.33.19, not this round; template_max yes = the line is correctly in the workflow's own templates (verify agreed).
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/tests/test_workflow_stage_scope.py · extensions/agi/workflows/merge-up-review.json (line 4 only) · this hypothesis node (item 6) · experiment:a00-d41529a1-5fe419 · the kid's own node.
CEILING   HARD CAP: 1 kid · workflow.py + mem_cap.py production NET <= +58 over 5038f6e817 (today's breach, findings row 64: item 1 must be line-NEUTRAL) · test_workflow_stage_scope.py <= 260 lines (director disclosed override from 200: three new rows) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after.
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit; run test_workflow_stage_scope.py test_workflow_stage_seam_cfg.py test_launch_memory_cap.py test_workflow.py test_bin_help_smoke.py with --basetemp under /tmp and paste the counts.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG3.75: SM 07:18Z returned 855daaccd with 3 gate-tree reds -- the systemd-run token asked of mem_cap, the Popen fakes gain poll in the same commit, and a seam failure must never fall through to a real harness launch; base = 855daaccd with the trunk merged in.
<!-- THOUGHT:END -->
