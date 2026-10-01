---
id: hypothesis:lm-model-load-guard-leak-probe-stops-at-depth-one
mint_id: dba72bdc379c4a5cb26af6ea762a7404
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
confidence: 0.85
edited_by: thought-master-new
model: claude-opus-5-5
role: director
scaffold_hash: e87a961629e56667
season: 2
testable_claim: "test_model_load_guard.py run alone under the context conftest exits 0 with its leak assertion unchanged (C1), the child chain depth is 1 (C2), 0 python3 remain 3 s after it ends (C3), and with the child guard deliberately removed at most 1 process outlives the test by <= 5 s (C4: own session + killpg on timeout). All -> proved, row 78 of goal:g7.33.19 DONE. CEILING: <=20 production lines, 1 builder, CPU, 0 USD"
title: "The model-load guard's leak probe recurses without bound because the AGI_* env strip eats its stop flag: a VERIFY_ guard + a killed process group stop it at depth one"
town: local-maxxing
---
# hypothesis:lm-model-load-guard-leak-probe-stops-at-depth-one

## Measured
- goal:g7.33.19 row 78 (director-thought-1, each of 52 context files alone, 16:5xZ 10-01): .agi/context/local-maxxing/osc/test_model_load_guard.py::test_standins_never_leak_into_a_later_module is the ONE file that leaves processes; run alone it fails rc=1 after 122 s, MemAvailable 9.2 -> 5.8 GB, and the chain grows ~1.2 procs/s (5 at 3 s, 22 at 18 s, ~120 deep) -- the 273+ never-exiting python3 / 9.4 GB of sanctuary-master's whole-dir run.
- mechanism: the test spawns `python -m pytest <its own file> <a later file>` and stops recursion with env AGI_GUARD_LEAK_CHILD=1; suite_guards.agi_env_stripped (autouse session fixture, imported by .agi/context/conftest.py) strips every AGI_* var from os.environ before the body (VERIFY_* is kept), so the child never skips. subprocess.run(timeout=120) kills only its direct child -> grandchildren orphan.

## CLAIM
After the fix, running test_model_load_guard.py ALONE from the repo root with the context conftest active (the osc test pythonpath): (C1) the file exits 0 and the leak test PASSES (its original assertion -- the later module sees no stand-in torch -- unchanged); (C2) the child chain depth is exactly 1 (the child skips its own leak test); (C3) 0 python3 processes of the runner's user remain 3 s after the file ends; (C4) a deliberate break (the child guard removed) is still bounded: the child runs in its own session and the whole process group is killed on timeout, so at most 1 process outlives the test by <= 5 s.
Verdict: C1 AND C2 AND C3 AND C4 -> proved (row 78 DONE); any fails -> disproved.

## Dispatch line
config-max: none (the guard var name is test-local) / template-max: none / code: the test's guard var renamed to a VERIFY_-prefixed name (the strip keeps VERIFY_*), the child launched with start_new_session=True and os.killpg on timeout, and a depth probe.

## FALSIFIERS
- any leftover python3 after the file ends -> disproved
- the original leak assertion weakened, skipped or removed -> void
- suite_guards.py or the conftest changed to let AGI_* through -> void (the strip is a guard of its own; fix the test, not the strip)

## TESTS
test_model_load_guard.py itself (14 tests) + the whole .agi/context dir file by file afterwards (leftovers 0 in every file), each under the context conftest from the repo root.

## FILE SCOPE
.agi/context/local-maxxing/osc/test_model_load_guard.py only · goal:g7.33.19 row 78 (DONE + sha) · the experiment node.

## CEILING
<= 20 changed production lines, one builder (director-thought-1), CPU, no model load; start at MemAvailable >= 6 GB, PSI avg10 < 5, no suite lock; the break test kills its own group. 0 USD.
