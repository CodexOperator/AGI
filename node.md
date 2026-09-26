---
id: hypothesis:context-fixture-tests-run-in-a-configured-suite
mint_id: cf3f52ca189f4777b5c657ae5e01ee35
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: 3db573059e434ca0
season: 2
testable_claim: director-engine):verification runs .agi/context test modules as a declared second suite, 0 collection errors from a neutral cwd, unrunnable modules skipped by name.
title: .agi/context fixture tests run in a declared suite with zero collection errors (assigned
town: core
---
# hypothesis:context-fixture-tests-run-in-a-configured-suite


# hypothesis:context-fixture-tests-run-in-a-configured-suite

## Measured
- thought-master TMM.212 item 3: SUITE_CMD = 'tests' (verification.py:78), so `.agi/context/**/test_*.py` sits outside every configured suite; re-measured 08:0xZ, PYTHONPATH empty: `pytest .agi/context --collect-only -q` = 127 collected, 18 modules ERROR at collection. PASS 8 found fixture-only evidence that no suite runs.

## CLAIM
The configured verification runs `.agi/context`'s test modules as a DECLARED second suite (a config cell listing the suite roots, never a literal), every collected module imports cleanly from a neutral cwd (0 collection errors), and a module that cannot run on this box is skipped BY NAME with its reason, never an error.

## Dispatch line
config-max: the suite roots as a declared cell (verification's config) / template-max: none / code: verification.py reads the cell; each erroring module gets its import path fixed or a named skip.

## FALSIFIERS
1. `pytest .agi/context --collect-only -q` from a neutral cwd still reports any collection ERROR.
2. The suite roots are a code literal.
3. A module that loads a model or touches the real model slot runs unguarded (belam's guard: no model loads).

## TESTS
the new suite's own collection; extensions/agi/tests/test_verification*.py.

## FILE SCOPE
extensions/agi/bin/verification.py, the declaring config cell (NAME it in your report: a round cannot commit .agi/config.json), the 18 erroring modules' import lines, this node + its experiment.

## CEILING
2 kids · ~40 production lines · pi-free · 0 USD.
