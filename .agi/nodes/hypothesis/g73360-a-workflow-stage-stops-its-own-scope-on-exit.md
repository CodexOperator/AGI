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

## CORRECTIVE DH.DG3.75 -- closes SM 07:18Z gate-tree RETURN of 855daaccd (3 range reds: red on the merged tree, green on pure HEAD)
BASE      CUT FROM de-base-DG3.69 tip 855daaccd; local-maxxing/season2/main MERGED IN (94f7dcea5) on branch de-base-DG3.75, worktree /mnt/agi-ram/worktrees/de-base-DG3.75. Never rebase.
1. test_ram_worktrees::test_no_systemd_run_argv_outside_mem_cap -- workflow.py:1909 tests the literal token systemd-run -- ASK mem_cap instead (one small helper there, e.g. is_wrapped(argv) beside wrap_argv), never widen the scan. TRUE WHEN that test passes at the new tip (paste) and git grep -n systemd-run extensions/agi/bin/workflow.py prints nothing.
2. test_workflow_slice_isolation::test_silent_stage_is_killed_at_the_wall + ::test_max_extensions_reached_still_kills_and_names -- the wall path calls proc.poll(), which the injected _FakePopen seam lacks (AttributeError) -- extend the fakes in the SAME commit (poll returns the fake returncode) so the stage path works on the seam exactly as before. TRUE WHEN both pass at the new tip (paste).
3. NO TEST MAY REACH A REAL HARNESS -- after the AttributeError the test FELL THROUGH to a REAL pi -p launch (SM measured) -- find the fall-through path and close it: a seam failure must surface as a test failure, never as a real child. TRUE WHEN a committed assertion (or a guard the tests share) makes a real harness launch under the seam a RED, and a deliberately broken fake in tmp (not committed) shows the guard firing without any real child (paste).
TESTS     at the new tip, env -u TMUX -u TMUX_PANE, --basetemp under /tmp: test_workflow_stage_scope.py test_workflow_stage_seam_cfg.py test_launch_memory_cap.py test_ram_worktrees.py test_workflow_slice_isolation.py test_workflow.py test_bin_help_smoke.py (paste the tail; test_workflow::test_dry_run_credential_line_matches_live_decision is red on the trunk alone -- report it, do not fix it here).
SAFETY    never run a real pi / claude / dispatch / systemd-run from a test or probe; never print a key or an argv carrying one.
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/bin/mem_cap.py · extensions/agi/tests/test_workflow_slice_isolation.py · extensions/agi/tests/test_ram_worktrees.py (only if the guard lives there) · this node.
CEILING   HARD CAP: production NET +12 lines · tests +40 lines · Sonnet 5.5 subagent (owner lanes 02:26Z 10-01) · 0 USD.
DONE      f819a8cd0 (Sonnet 5.5 subagent): mem_cap.is_wrapped, _FakePopen.poll, autouse _no_real_harness; 240 passed 8 skipped (7 files).

## CORRECTIVE DH.DG3.76 -- closes mur-de-base-dg3-75 h60e-code (accept_with_residue, verify upheld 3 residues)
BASE      de-base-DG3.75 tip f819a8cd0, same worktree. Never rebase.
1. The guard is argv-SHAPE, not a launch ban -- test_workflow_slice_isolation.py:67-69 -- a real child of any other shape forks; worst case (verify missed[0]): workflow.py _run_round_stage (~2307-2311) runs [python3, dispatch.py, ... --tier parent ... --detach] through subprocess.run and the guard passes it = a REAL parent dispatch from a test. Make it DENY BY DEFAULT: every real launch under the seam is refused unless the one test that needs a real child (the bash tick row ~395-421) opts in explicitly for that argv. TRUE WHEN a committed row shows a dispatch.py-shaped argv refused, and the bash row still passes.
2. String-shaped argv bypasses every check -- :65-66 -- normalize a str argv (shlex.split) before the checks, or refuse non-list argv outright. TRUE WHEN a committed row shows Popen of a pi-shaped STRING refused.
3. A second home for the no-real-child policy -- the declared home is suite_guards (conftest.py ~641-647 NO_REAL_PROCESSES, suite_guards.py ~340-354) -- fold this file into that home (opt in, with the bash row's real child as the one declared exception), or, if suite_guards cannot carry an exception, extend suite_guards ONCE so it can and delete the per-file guard body. TRUE WHEN the per-file guard body is gone or reduced to an opt-in plus the exception, and `git grep -n 'def _guard' extensions/agi/tests/test_workflow_slice_isolation.py` shows no second policy body.
DEMOTED   UNVERIFIED 3b (the hazardous probe was rightly not run; the code read found no fall-through) · UNVERIFIED F1-F3 (test_workflow_stage_scope.py excluded by the brief; 240 passed reported) · the finally AssertionError note (no test exercises it) · no experiment node (a note; the hypothesis closes at the merge-up).
SAFETY    never run a real pi / claude / dispatch.py / workflow.py run / systemd-run from a test or probe.
FILE SCOPE extensions/agi/tests/test_workflow_slice_isolation.py · extensions/agi/tests/conftest.py · extensions/agi/tests/suite_guards.py (only the exception mechanism) · this node.
CEILING   tests net +40 lines · production 0 · Sonnet 5.5 subagent · 0 USD.
DONE      81f75ae39: the per-file guard deleted; NO_REAL_PROCESSES = True (suite_guards home); 290 passed 8 skipped.

## CORRECTIVE DH.DG3.77 -- closes mur-de-base-dg3-76 h60f-code (accept_with_residue, verify upheld)
BASE      de-base-DG3.75 tip 81f75ae39 + this node commit, same worktree. Never rebase.
1. _REAL_LEAF is a module global (test_workflow_slice_isolation.py:48): scope the one real child to the bash tick row ONLY -- a fixture or a local in that row whose leaf itself refuses any argv but the declared bash tick (assert at the leaf, not the call site). TRUE WHEN no module-level name in the file holds the raw Popen (paste git grep -n _REAL_LEAF) and the bash row passes.
2. Deny-by-default not pinned (verify missed): test_opt_in_refuses_every_real_launch adds a benign NON-harness argv (e.g. ['true']) refused on Popen and run. TRUE WHEN that row would FAIL against a harness-shape-only guard (say why in the commit message).
3. Stale module docstring (:24-27) rewritten to the opt-in truth (one real bash child, everything else refused by suite_guards).
4. _CFG read at import (:74): read the config snapshot inside the fixture (lazily, before the fence engages), never at module import.
DEMOTED   UNVERIFIED other guard files (290 passed reported) · the bash-child kill note (unreachable) · the silent-fallback note (the conftest fence loads for this suite) · the config-frozen note (closed by item 4).
FILE SCOPE extensions/agi/tests/test_workflow_slice_isolation.py · this node.
CEILING   tests net +25 lines · production 0 · Sonnet 5.5 subagent · 0 USD.
DONE      567ca53ab: the real leaf in the _bash_tick_leaf fixture closure; ['true'] pinned; docstring; lazy _cfg_text; 62 passed.

## CORRECTIVE DH.DG3.78 -- closes mur-de-base-dg3-77 h60g-code (accept_with_residue) -- the LAST hygiene round: pin the invariant ONCE, repo-wide
BASE      de-base-DG3.75 tip 567ca53ab + this node commit. Never rebase.
1. The raw-leaf escape hatch is unpinned repo-wide (verify missed[1]): ANY opted-in test file can getattr(_sp.Popen, "__agi_spawn_fence__") and get the raw stdlib Popen. ONE committed test in the suite_guards neighbourhood scans extensions/agi/tests/*.py and allows the fence marker only in a declared allow-list (today: test_workflow_slice_isolation.py's _bash_tick_leaf fixture). TRUE WHEN a scratch file adding a second holder turns that test RED (paste), then removed.
2. The leaf's allow-list is basename-only (:87-88): require the tick path to resolve under the test's tmp root (pass tmp_path into the leaf). TRUE WHEN a tick.sh outside tmp is refused (a row).
3. The ['true'] row (:64) can run a real /usr/bin/true if the fence is absent: use a /nonexistent/ path like its siblings, so a broken fence gives FileNotFoundError, never a child.
DEMOTED   production conjuncts out of range (refuted: by scope) · no verdict (refuted: experiment:a00-d41529a1-5fe419 carries it).
FILE SCOPE extensions/agi/tests/test_workflow_slice_isolation.py · extensions/agi/tests/test_declared_suite_guards.py (or test_conftest_guard.py) for item 1 · this node.
CEILING   tests net +35 · production 0 · Sonnet 5.5 subagent · 0 USD.
DONE      eb31b477a: test_declared_suite_guards::test_the_raw_leaf_escape_hatch_has_a_declared_allow_list scans extensions/agi/tests/*.py (ONE directory, not repo-wide: subdirs and bin/ are outside it -- no holder exists there today, verify h60h) for __agi_spawn_fence__ / FENCE_MARKER, allow-list conftest.py + test_conftest_guard.py + test_declared_suite_guards.py + test_workflow_slice_isolation.py; scratch second holder test_scratch_second_holder.py -> RED "Extra items in the left set" (subagent run, file then removed; verify h60h reproduced it); _bash_tick_leaf(root) tmp-scoped; /nonexistent/true; 63 passed. mur-de-base-dg3-78: review accept_with_residue, verify accept_with_residue -> residues node-prose only (this DONE line), closed by the director without a re-mur (agi-corrective row 1).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG3.78 (the last hygiene round): mur-de-base-dg3-77 h60g-code accept_with_residue: the raw-leaf escape hatch pinned once repo-wide by an allow-list test, the leaf tmp-scoped, the true row on a nonexistent path.
<!-- THOUGHT:END -->
