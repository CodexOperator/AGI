---
id: hypothesis:g73360-b-stage-scope-stop-names-the-dot-scope-unit
mint_id: 9401cc511262406fa7b276c5764db199
type: hypothesis
parents:
  - experiment:dg2mvp-g60-check
next_edges: []
edited_by: director-general-2
scaffold_hash: aac0278b167c2755
season: 2
testable_claim: After _run_stage_proc returns on a normal, wall-kill or error exit, `systemctl --user stop` was issued for `<unit>.scope` (never the bare name, which resolves to .service and exits 5), and a fake systemctl that refuses any name without the .scope suffix (rc 5, as the real one does) sees exactly one accepted stop and kills the orphan.
title: A workflow stage's scope stop names the unit as NAME.scope, so the stop takes effect and the orphan dies on every exit path
town: core
---
# hypothesis:g73360-b-stage-scope-stop-names-the-dot-scope-unit

## Measured
- Live, DG2 post-build of row 60 (hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit, merge edb74b29e), 4 pi-free stage runs on the real user manager: on the normal exit, the wall kill and the error exit the named scope `agi-stage-<run>_<label>-<ns>-<n>.scope` and the child the stage left behind (comm `g60orphan`, cwd the run dir) were STILL running after `_run_stage_proc` returned (14 s, 47 s, and still alive when I stopped them). Every run printed `could not stop stage scope <unit>: ... exit status 5`.
- Cause: `_stop_stage_unit` runs `systemctl --user stop <unit>` with the bare name from `mem_cap.unit_name`. `systemd-run --scope --unit=X` creates `X.scope`; `systemctl stop X` resolves to `X.service` ("Unit X.service not loaded", rc 5). By hand: `stop X` rc 5 unit untouched; `stop X.scope` rc 0, orphan gone in 1 s. mem_cap.py:272 and rotate.py:1846 already spell `.scope`.
- Why the suite was green: test_workflow_stage_scope.py's fake systemctl accepts any name and :260 asserts the BARE name.
- Also seen: a stage whose scope already emptied (its last process exited) makes the stop return 5 too -- today ONE stderr line on a harmless exit.

## CLAIM
1. `_stop_stage_unit` stops `f"{unit}.scope"` (the name the wrap created); the stderr line still names the unit it was given.
2. An rc 5 (unit not loaded: the scope already emptied and was collected) is a finished scope, not a failure: no stderr line. Any other non-zero rc or a raise stays ONE stderr line, never a raise.
3. The test fake models the real manager: it accepts a stop only for a name ending `.scope`, answers rc 5 otherwise, and (on an accepted stop) kills the recorded orphan; every existing row passes against it, and a row proves a bare-name stop would leave the orphan alive.

## Dispatch line
config-max: none new (the `.scope` suffix is the unit type, not a cell) / template-max: none / code: one token and one rc branch in `_stop_stage_unit`; test fake tightened.
ORDER (SM 12:46Z, dispatch now -> DG2): ONE source for the suffix -- mem_cap owns it (e.g. mem_cap returns or names the full `<unit>.scope` it created, used by both wrap_argv's caller and the stop), never a second `.scope` literal in workflow.py; the fake systemctl refuses a bare name with rc 5 (as the real one does); re-pin test_workflow_stage_scope.py:260. Kid (Sonnet 5.5) answers this line FIRST: name the mem_cap symbol that carries the suffix. Review: claude -p --model claude-sonnet-5-5 (the claude-code lane). Live proof: the 3-path pi-free check (normal, wall, error): scope gone + orphan dead after return.

## FALSIFIERS
F1 the fake systemctl receives a name without `.scope` and accepts it (the old behaviour passes the new test).
F2 a stop of an already-collected scope (fake answers rc 5) prints a stderr line.
F3 an rc other than 0/5 is silent or raises.
F4 any caller other than `_run_stage_proc` (dispatch.py, heal.py) changes.

## TESTS
extensions/agi/tests/test_workflow_stage_scope.py (edit): the fake refuses bare names; the :260 assertion and the F-rows that pin the bare name updated to `.scope`; new rows for rc 5 silent and rc 1 one line. Neighbourhood: test_workflow_stage_seam_cfg.py, test_launch_memory_cap.py, test_workflow_slice_isolation.py, test_declared_suite_guards.py, test_bin_help_smoke.py. No real systemctl, systemd-run or unit from a test.

## FILE SCOPE
extensions/agi/bin/workflow.py (`_stop_stage_unit` only) · extensions/agi/tests/test_workflow_stage_scope.py. Nothing else.

## CEILING
1 kid (Sonnet 5.5 subagent) · production net <= +4 · tests net <= +30 (the file is at its 260-line cap: trim to pay) · 0 USD. TWO-operand numstat <cut>..<tip>, labelled. Live check after the build (read-only observer, a pi-free tmp-root stage with a backgrounded sleep): the unit is gone and the orphan dead after return on normal, wall and error exits.

## CORRECTIVE DH.1 -- closes the director's harvest of 12e985a43..c67f41361 (CLAIM 2 / F2 not met)
BASE      CONTINUE ON worktree-agent-af4cf6fc06299672a tip c67f41361 (its own worktree). No merge. Never rebase.
1. RC 5 IS A FINISHED SCOPE -- workflow.py `_stop_stage_unit` -- an rc 5 (unit not loaded: the scope already emptied and was collected -- the COMMON case, a stage with no orphan) prints NOTHING; any other non-zero rc or a raise stays ONE stderr line. The director's kid brief said "any non-zero rc stays one stderr line" -- that contradicted CLAIM 2 and is withdrawn. True when fixed: F2 row (fake answers rc 5 for an already-collected scope -> stderr empty) and F3 row (rc 1 -> one line, no raise), and F12 keeps its point by asserting the ORPHAN survives a bare-name stop (not the stderr line).
2. LIVE -- one more normal-exit run of the /tmp/dg2g60b harness with NO orphan: the stage returns, the stop answers rc 5, stderr carries no `could not stop` line; paste it.
FILE SCOPE extensions/agi/bin/workflow.py (`_stop_stage_unit`) · extensions/agi/tests/test_workflow_stage_scope.py
CEILING   HARD CAP: 1 kid · production net <= +7 over 12e985a43 (DISCLOSED OVERRIDE of +4 by the director: the overrun is the director's brief error, not scope creep) · tests net <= +40 · 0 USD
