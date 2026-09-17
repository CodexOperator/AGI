---
id: experiment:a00-3e534ff0-89ba0c
mint_id: 2d9d69044b1246c08b934a2b55e364b5
type: experiment
parents:
  - hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp
next_edges: []
confidence: 0.9
edited_by: a00-3e534ff0
evidence_runs:
  - experiment:a00-3e534ff0-89ba0c
line_ceiling: 50
loop: hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 35
profile: balanced
role: kid
scaffold_hash: 0d7526d0d623d554
season: 2
title: mint-failure refuses unless inherited key verified; timeout named; prose persisted whole
town: core
verdict: proved
---
# experiment:a00-3e534ff0-89ba0c

## Experiment

KID SLICE items (1)+(3)+(5) on hypothesis:l4-pi-review-stages... (the parent dispatch split provisioning/merge-up to their own kids; untouched here). Scope locked to extensions/agi/bin/workflow.py + tests/test_workflow.py.

(1) persist — production already existed (`_persist_stage_value`), only a fixture test was missing. Added `test_prose_stage_persists_whole_return`: a real fake-pi run in prose mode persists its FULL return (asserts `_PROSE_TAIL` present, >200 chars, so not the 200-char tree view), rc 0, run_key propagated into the jsonl row, and the row's `returns` keeps the whole prose. Best-effort OSError path already covered by the try/except in `_persist_stage_value` (untouched).

(3) timeout wording — existing `_run_stage_pi` caught `(OSError, SubprocessError)` and reported EVERY failure as "could not start" incl. a TimeoutExpired. Added a dedicated `except subprocess.TimeoutExpired` branch FIRST that reports `timed out after N s`, keeps rc 2, one attempt. New `test_timeout_reports_elapsed_not_could_not_start` asserts the failure line begins "timed out after 600 s", never "could not start".

(5) mint-failure refused — `_resolve_workflow_spawn_env` fell back to the inherited `_pi_env()` on ProvisioningError (a dead/revoked key would spin to timeout). Now: print mint error verbatim, gate the fallback on `provisioning.check_runtime_key_usable`; unusable -> return (None, None) and run_workflow returns rc 3 BEFORE any stage dispatches; usable -> run on inherited env with `[credential] inherited env, verified` line. Rewrote the old `test_pi_mint_error_is_named_then_falls_back` into two cases (a) rc 3, no stage run, mint error verbatim; (b) rc 0, verified line present.

## Evidence

`python3 -m pytest extensions/agi/tests/test_workflow.py -q` -> 82 passed. Targeted run (timeout|mint|fallback|prose_stage|persist) -> 25 passed. Production lines: 35 added (git diff --numstat on workflow.py only; ceiling 50, re-brief threshold 100) — no re-brief needed. test_timeout_is_one_attempt_no_retry and test_pi_fallback_prints_one_named_line_when_provisioning_absent both still green (byte-compatible paths preserved). check_runtime_key_usable read-only.

## Agent Notes
items 1+3+5: prose persisted whole to runs/<key>/<label>.json (fixture test); TimeoutExpired reports 'timed out after N s' rc2 never 'could not start'; failed mint refuses rc3 unless inherited key proven usable via check_runtime_key_usable (else runs with '[credential] inherited env, verified'). 82/82 pass, 35 prod lines, ceiling 50.
