---
id: hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env
mint_id: 51dc1553880c456bae246bb605662719
type: hypothesis
parents:
  - hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: 3519dfd795747b9c
season: 2
testable_claim: All four adapters' restart() build the child env from dispatch.scrubbed_env(); a restarted child lacks every ENV_VARS_TO_SCRUB key set in the restarting process.
title: "every adapter restart spawns from the scrubbed env, never raw os.environ (assigned: director-engine)"
town: core
---
# hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env


# hypothesis:every-adapter-restart-spawns-from-the-scrubbed-env

## Measured
- DH.385 parent a00-09d1b5a8's wire probe: `AGI_MODEL_SLOT_LOCK=/tmp/a-squatted.lock python3 -c "import pi_adapter as pa; print(pa.child_env(harness={'env':None}, base=dict(os.environ)).get(...))"` -> `/tmp/a-squatted.lock` -- the restart path (dispatch.py:3626 `adapter.restart(...)`) never passes through dispatch.scrubbed_env().
- pi_adapter.py:326 `env = child_env(harness=harness, base=dict(os.environ), tier=tier)`; claude_code_adapter / copilot_cli_adapter / grok_bot_adapter `restart()` each read `os.environ` too (1 hit each, director-engine gen 23).
- So a RESTARTED round inherits every ENV_VARS_TO_SCRUB key: the Claude-Code Anthropic credentials (the quota leak dispatch.py:289-294 exists to stop), the key-minting key (goal:g1.11), the AGI_ORDERS_* text, and AGI_MODEL_SLOT_LOCK. The first spawn (dispatch.py:2606) and the dry-run mirror (:1376) already use scrubbed_env().

## CLAIM
Every adapter's restart() builds its child env from the same scrubbed base as the first spawn: with any ENV_VARS_TO_SCRUB key set in the restarting process, the restarted child's env lacks it, for all four adapters.

## Dispatch line
config-max: none (ENV_VARS_TO_SCRUB stays the one list) / template-max: none / code: each restart() takes its base from dispatch.scrubbed_env() (or a base passed in by the caller at dispatch.py:3626) -- one source, never a second scrub list.

## FALSIFIERS
1. For any of the 4 adapters, a restart child env built with ANTHROPIC_API_KEY or AGI_MODEL_SLOT_LOCK in the parent env still carries it.
2. A second, adapter-local scrub list appears.
3. test_*adapter*.py / test_dispatch*.py restart tests regress.

## TESTS
the adapters' restart test neighbourhood (`git grep -l "def test.*restart" extensions/agi/tests`); env seams only -- never start a real claude / pi process (TMM.202).

## FILE SCOPE
extensions/agi/bin/adapters/{pi,claude_code,copilot_cli,grok_bot}_adapter.py (restart only), dispatch.py:3626 call site if the base is passed in, their tests, this node + its experiment.

## CEILING
1-2 kids · ~15 production lines · pi-free · 0 USD.
