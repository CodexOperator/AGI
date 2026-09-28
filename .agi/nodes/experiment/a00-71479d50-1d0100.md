---
id: experiment:a00-71479d50-1d0100
mint_id: 9d2ef7d83f4e4b5b9c6af79c2fcb2ca6
type: experiment
parents:
  - hypothesis:context-budget-never-floors-to-zero-and-is-pinned
next_edges: []
confidence: 0.95
edited_by: a00-57bf9540
evidence_runs:
  - experiment:a00-71479d50-1d0100
loop: hypothesis:context-budget-never-floors-to-zero-and-is-pinned@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 gate (S1 fraction): 0.001/0.5/0.999999 context -> exactly 1; load-scaled sites (lf .2-.5, load 0-8) -> exactly 1; pre-fix temp copy returned 0 (RED confirmed). P2 wire (S1 live): stubbed run_workflow with context_timeout_s=0.5 saw timeout=[1,1] on viewport+brief; 0 never reached a subprocess. P3 gate (S2 precedence): stage 300 beats manifest 60; stage-declared 0 wins by PRESENCE and is refused by name (no fallback to 300); stage None falls through to 7. P4 gate (S3 bool+refusal): 0/-1/-0.5/True/'300' each refused by name; absent -> 60. P5 gate (S4+S5 dry-run/zero-dispatch): dry-run ct=0 -> rc 5, no [dispatch]; ct=0.5 -> rc 0 with [dispatch]. P6 wire (S6): pre-fix workflow.py returns 0 for 0.5, so the fraction test is RED pre-fix. P7 wire (S7): test_workflow*.py 146 passed on the tip."
production_lines: 19
profile: balanced
role: kid
scaffold_hash: af0483667ca33ac7
season: 2
title: Fractional context budget floors at 1s not 0; stage/bool/dry-run pinned
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-71479d50-1d0100

## Experiment

Build round for `hypothesis:context-budget-never-floors-to-zero-and-is-pinned`
(leaf `goal:g15.29.20`). Test-first, then fix `workflow.py`, then prove on the
built bytes. FILE SCOPE only: `workflow.py` · `test_workflow_review_under_load.py`.

### Defect (measured, pre-fix)

`_resolve_context_timeout` accepted `0<v<1` (a positive number, so it cleared
the refusal) and then truncated with `int(raw)` — `int(0.5) == 0` — so the
context subprocess was handed `timeout=0`, which `subprocess.run` treats as an
immediate `TimeoutExpired`. The load-scaled sites truncated the same way
(`int(min(0.5*(1+0), 1.0)) == 0`). Same silent-kill shape the refusal exists
to prevent, reached through the ONE path that was not refused.

### Fix

New `_whole_seconds(value) -> max(1, int(value))` and used at all four
truncation sites: the stage wall with and without `load_factor`, and the
context build with and without `load_factor`. A fractional budget now floors at
ONE second, never zero. Semantics otherwise unchanged: `int` floors whole
values exactly as before, and the refusal (0/negative/bool/non-numeric) is
untouched.

### Tests added (`test_workflow_review_under_load.py`)

| Conjunct | Test |
|---|---|
| fraction never floors to 0 | `test_fractional_context_budget_never_floors_to_zero` (RED pre-fix) |
| load-scaled truncation | `test_fractional_budget_under_load_never_floors_to_zero` (RED pre-fix) |
| stage > manifest precedence | `test_stage_context_timeout_beats_manifest` |
| bool refusal + zero dispatch | `test_bool_context_timeout_refused_and_no_stage_dispatched` |
| dry-run rc 5 parity | `test_dry_run_refuses_a_bad_context_timeout_with_rc_5` |

## Evidence

Pre-fix, named test file (before the `workflow.py` edit):
```
FAILED test_fractional_context_budget_never_floors_to_zero
FAILED test_fractional_budget_under_load_never_floors_to_zero
3 failed, 11 passed
```
Both failure messages were the expected assertion (`int(0.5) == 0`). The other
five conjuncts were already green pre-fix, as the hypothesis states.

Post-fix:
```
$ python3 -m pytest extensions/agi/tests/test_workflow_review_under_load.py -q
14 passed in 0.35s

$ python3 -m pytest test_workflow.py test_workflow_review_under_load.py \
    test_workflow_slice_isolation.py test_workflow_result_file.py \
    test_workflow_claude_code_branch_names_itself.py -q
146 passed in 164.04s (0:02:44)
```
All runs under `env -u TMUX -u TMUX_PANE`, files named, never the bare
directory. Production lines: `git diff --numstat` = 19 added / 4 removed in
`workflow.py` (tests excluded), under the ceiling.

HAZARD respected: no real workflow was run; every drive stubs `subprocess.run`
and redirects sessions to tmp, and the dry-run test dispatches nothing.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of commit c4bcffa4ac. Parent brief: read the kid DIFF, run one negative probe per conjunct, never trust its result file. Machine (read from the diff, not the summary): the kid adds _whole_seconds(v)=max(1,int(v)) and routes all four truncation sites through it (workflow.py stage wall with/without load_factor, context build with/without load_factor); the refusal predicate (raw<=0 / bool / non-numeric) stays BEFORE the clamp in both resolvers. I ran 32 independent probes (7 recorded as probes:), all held: fractional budgets return exactly 1 on and off the load path; a live stubbed run passes timeout=[1,1] to viewport+brief; stage-0 wins by presence and is refused rather than falling back to the manifest; dry-run rc 5 with zero [dispatch]; the pre-fix temp copy returns 0 for 0.5 (test RED pre-fix); test_workflow*.py 146 passed on the tip. Near miss: clamping first (return max(1,int(raw)) reachable for raw==0) would satisfy never-floors-to-zero while silently converting a declared 0 into a 1s run and breaking the pinned rc-5/zero-dispatch contract; the diff avoids it and P4 confirms 0/-1/True still refuse. Deviation: none. Accepted; verdict proved.
<!-- THOUGHT:END -->

## Agent Notes
Built the fix: _whole_seconds floors every truncation site at 1s so a 0<v<1 context/stage budget never reaches subprocess timeout=0; added tests pinning fraction (RED pre-fix), stage>manifest, bool refusal with zero dispatch, dry-run rc5; test_workflow*.py 146 passed.

ACCEPTED proved 0.95. Diff within FILE SCOPE (workflow.py, test_workflow_review_under_load.py): _whole_seconds floors every truncation site at 1s so a 0<v<1 budget never becomes subprocess timeout=0. 32/32 parent probes held; fraction test RED on pre-fix bytes; test_workflow*.py 146 passed. No deliverable named by the kid is missing from the diff. Caveat: the stage wall now also floors fractional >=1 values (1.9 -> 1), a widening beyond the context-only claim, defensible and inside the same helper.
