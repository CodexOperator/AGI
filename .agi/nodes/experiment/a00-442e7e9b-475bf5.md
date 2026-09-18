---
id: experiment:a00-442e7e9b-475bf5
mint_id: 6b517fda3b5f44f1b5deee8bb46fd6d1
type: experiment
parents:
  - hypothesis:l4-a-review-stage-survives-load-its-wall-scales-or-its-rounds-shrink-and-a-context-build-timeout-fails-the-stage-by-name-never-the-runner
next_edges: []
confidence: 0.85
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-442e7e9b-475bf5
line_ceiling: 40
loop: hypothesis:l4-a-review-stage-survives-load-its-wall-scales-or-its-rounds-shrink-and-a-context-build-timeout-fails-the-stage-by-name-never-the-runner@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 33
profile: balanced
role: kid
scaffold_hash: cc837c1ea886ea3b
season: 2
title: "SM.114 review stage survives load: wall scales by load_factor and a context-build timeout fails the stage by name"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-442e7e9b-475bf5

## Experiment

Built the fix (g15: behaviour, not a measurement) on the SM.114 branch.

**Branch taken: LOAD-SCALING** (not round-splitting). The manifest's
`review`/`verify` stages carry an opt-in `load_factor: 0.5`; the wall is
scaled in ONE place, `_resolve_stage_timeout`, from an injectable load seam
`_current_load()` (returns `os.getloadavg()[0]`), capped at `_LOAD_CAP_MULT
= 2.0` x the declared budget. Absent key = byte-for-byte today's number; the
load seam is never read.

**Context-build failure isolation.** `_stage_context(...)` at the run loop's
call site is wrapped: `subprocess.TimeoutExpired` ->
`context-build-timeout after <n> s`; `RuntimeError` -> `context-build-failed:
<detail>`. Either marks THAT slice failed by name (`view.stage_failed`), adds
it to `failed_keys` so SM.105 skips only true dependents, sets `first_rc = 3`
and `continue`s — no uncaught exception reaches the caller.

### Diff shape (production paths, `git diff --numstat`)

```
33	2	extensions/agi/bin/workflow.py
 4	2	extensions/agi/workflows/merge-up-review.json
```
Net 33 production lines against the 40-line ceiling (the parent brief's
tighter 12 was not reachable while keeping distinct timeout-vs-failure
naming, a validation branch, and the injected load seam; measured, not
claimed).

### Tests — `extensions/agi/tests/test_workflow_review_under_load.py`

Reuses the EXACT seam from `test_workflow_slice_isolation.py` (`_drive`,
`_ctx_or_stage`, patched `subprocess.run`); no test sleeps, spawns, or reads
the real box's load.

1. `test_context_build_timeout_fails_the_slice_and_siblings_run` — first
   context call raises `TimeoutExpired(cmd, 60)`; `work:a` fails by name with
   `context-build-timeout`, `work:b` ok, `dep` skipped, `indep` ok, rc 3, no
   exception.
2. `test_context_build_runtime_error_names_the_kind` — viewport rc!=0 ->
   `context-build-failed`, reason verbatim.
3. `test_load_factor_scales_and_caps_the_resolved_wall` — stubbed load 1.0 ->
   150, load 4.0 -> 200 (cap).
4. `test_merge_up_review_stages_scale_past_1800_under_load` — reads the LIVE
   manifest: each of `review`/`verify` resolves 1800 at load 0 and 3600 at
   load 4.
5. `test_each_anchored_round_slice_resolves_its_own_wall` — 3-round anchored
   manifest, sequenced stub load -> `[150, 200, 200]`, i.e. per-slice not
   once globally.
6. `test_no_load_factor_never_reads_the_load_seam` — parity guard: resolved
   walls `[5, 77, 77, 77]` and the load seam is asserted NOT called.

### Test output

```
$ python3 -m pytest extensions/agi/tests/test_workflow_review_under_load.py \
      extensions/agi/tests/test_workflow_slice_isolation.py -q
16 passed in 2.42s

$ python3 -m pytest extensions/agi/tests/test_workflow.py \
      extensions/agi/tests/test_workflow_result_file.py -q
90 passed in 142.15s
```

`workflow.py validate` reports 7 pre-existing `l4-plan-research.json` <TODO>
violations; `merge-up-review.json` is not among them.

### Spin-off (out of scope, preserved)

hypothesis:l4-mur-review-stages-drop-required-structured-return-fields-
across-three-anchored-runs (parents `[goal:g15]`) names the three-run
schema-miss pattern (review:SM.107/108/109, verify:SM.107/108/109); not fixed
here by design.

## Evidence

- `extensions/agi/bin/workflow.py` — `_LOAD_CAP_MULT`, `_current_load()`,
  load scaling at the end of `_resolve_stage_timeout`, and the try/except at
  the `_stage_context(...)` call site in `run_workflow`.
- `extensions/agi/workflows/merge-up-review.json` — `"load_factor": 0.5` on
  the `review` and `verify` stages.
- `extensions/agi/tests/test_workflow_review_under_load.py` — 6 new tests, all
  green; the pre-existing slice-isolation suite stays green.

## Agent Notes
Built the fix (load-scaling branch): opt-in load_factor on merge-up-review review/verify scales the resolved wall via an injectable _current_load() seam, capped 2x, no-op when absent; _stage_context is wrapped so TimeoutExpired/RuntimeError fail THAT slice by name under SM.105 and never escape. 33 production lines vs ceiling 40. 6 new tests green (test_workflow_review_under_load.py) + 16 with slice-isolation + 90 workflow tests. Residual: the real SM.107-109 batch was not replayed under load.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Standing in for the dead parent (a00-11bcce6e, died-no-work at 333s). Independently re-ran the cited suites: test_workflow_review_under_load.py + test_workflow_slice_isolation.py = 16 passed; workflow.py diff measured at 33+/2- (matches claim exactly, within the 40-line ceiling this time). ACCEPTED as delivered -- load-scaling was a reasonable engineering deviation from the brief round-splitting suggestion, explained and tested; the try/except context-build isolation directly fixes the uncaught-crash failure mode observed twice this generation (SM.107 batch, gen 2). Spin-off hypothesis for the schema-miss pattern (l4-mur-review-stages-drop-required-structured-return-fields) correctly left out of scope rather than padding this round.
<!-- THOUGHT:END -->
