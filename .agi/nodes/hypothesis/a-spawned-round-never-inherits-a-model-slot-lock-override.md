---
id: hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override
mint_id: 3cc54519c01741faab4fccd74ac210ae
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: eba4fcc45daa5509
season: 2
testable_claim: director-engine):dispatch scrubbed_env drops AGI_MODEL_SLOT_LOCK so no spawned round can step outside the box-wide model slot; --lock stays explicit.
title: a spawned round never inherits a model-slot lock override (assigned
town: core
---
# hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override


# hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override

## Measured
- DT P8.01 (landed 49e8cd268) gave model_slot.py a lock override: `--lock` or the env var `AGI_MODEL_SLOT_LOCK` (.agi/context/local-maxxing/model_slot.py:25-31). With nothing injected, lock_path() is the production box-wide flock.
- dispatch.py:330 `scrubbed_env()` removes only `ENV_VARS_TO_SCRUB` (dispatch.py:295); AGI_MODEL_SLOT_LOCK is not in it, so an override set anywhere up the tree reaches every spawned parent and kid -- each of which could then load a model OUTSIDE the box-wide slot the Prime's memory guard (belam 04:29Z) relies on. `--lock` is explicit and visible in argv; the env var is invisible and inherited (thought-master TMM.215 "open": director-engine's ruling).

## CLAIM
A round spawned by dispatch.py (and heal.py, which shares scrubbed_env) never inherits AGI_MODEL_SLOT_LOCK: the child env lacks the key even when the parent env carries it; `--lock` on an explicit model_slot.py invocation is unchanged.

## Dispatch line
config-max: none (the scrub list is the one declaration) / template-max: none / code: add the key to dispatch.py ENV_VARS_TO_SCRUB with a comment naming why.

## FALSIFIERS
1. With AGI_MODEL_SLOT_LOCK set in the parent env, `scrubbed_env()` (or a dry-run spawn env) still carries it.
2. model_slot.py's own tests (test_model_slot.py, test_default_lock_is_still_the_production_cell) regress.

## TESTS
extensions/agi/tests/ -- the existing scrubbed_env test neighbourhood (find it with `git grep scrubbed_env extensions/agi/tests`).

## FILE SCOPE
extensions/agi/bin/dispatch.py (ENV_VARS_TO_SCRUB only), one test, this node + its experiment.

## CEILING
1 kid · ~3 production lines · pi-free · 0 USD.
