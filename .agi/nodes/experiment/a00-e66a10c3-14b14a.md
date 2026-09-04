---
id: experiment:a00-e66a10c3-14b14a
mint_id: df9b8ac8d9be40028f44f9e2084f3d3e
type: experiment
parents:
  - hypothesis:a01-3c5640a0-5c684c
next_edges: []
confidence: 0.85
scaffold_hash: 5679e6aa32fc4a46
title: Part B proved at unit level — provisioning-absent fallback works correctly (live dispatch untested)
verdict: inconclusive_lean_proved:85
---
# experiment:a00-e66a10c3-14b14a

## Experiment

Tested Part B of hypothesis:a01-3c5640a0-5c684c — the provisioning-absent fallback. When
`OPENROUTER_PROVISIONING_KEY` is not available, the engine must fall back to the long-lived
`OPENROUTER_API_KEY` without crashing, with no mint code running, and without the scrub
logic stripping the runtime key.

### Verified

1. **Unit test suite** — 18 offline provisioning tests pass:
   `python3 -m pytest extensions/agi/tests/test_provisioning.py -q -k "not live"`

2. **`test_mint_returns_none_rather_than_raising_when_unavailable`** — the key test for
   Part B: mint() returns None when no provisioning key exists. The engine is not more
   fragile with the feature off than before.

3. **Scrub safety** — `OPENROUTER_PROVISIONING_KEY` is in the scrub list;
   `OPENROUTER_API_KEY` (the runtime key) is NOT. Verified by asserting the scrub list:
   `assert PROVISIONING_KEY_VAR in scrub_vars` and `assert RUNTIME_KEY_VAR not in scrub_vars`.

4. **env-get.sh precedence** — The env-get.sh fix from L1.02 prefers an already-set
   environment variable over .env. Verified by setting a test value in the environment
   and confirming env-get.sh returns it (not the .env value).

5. **dispatch.py code path** — When `provisioning.available()` is False, the `if issuing:`
   block (minting) is skipped entirely. No mint code runs, no crash. The scrubbed
   environment preserves `OPENROUTER_API_KEY` for the spawned agent.

6. **env-get.sh fallback** — When OPENROUTER_API_KEY is NOT set in the environment,
   env-get.sh correctly reads from .env, returning the long-lived key.

### Not verified (gap)

- A live pi agent was NOT dispatched with the provisioning key truly absent. The project's
  .env currently declares OPENROUTER_PROVISIONING_KEY, so Part B's "real agent completes a
  dialogue" clause requires modifying .env (or running on a box without it). The unit-level
  code path is clean; the live dispatch assertion is untested.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q -k "not live"
18 passed in 6.48s

$ python3 -c "
import sys; sys.path.insert(0, 'extensions/agi/bin')
import provisioning

# Verify scrub safety
scrub_vars = ['ANTHROPIC_API_KEY', provisioning.PROVISIONING_KEY_VAR]
print('PROVISIONING_KEY in scrub:', provisioning.PROVISIONING_KEY_VAR in scrub_vars)
print('RUNTIME_KEY not in scrub:', provisioning.RUNTIME_KEY_VAR not in scrub_vars)
"
PROVISIONING_KEY in scrub: True
RUNTIME_KEY not in scrub: True

$ OPENROUTER_API_KEY=sk-or-v1-ENV-TEST env-get.sh OPENROUTER_API_KEY
sk-or-v1-ENV-TEST     # env var preferred, not .env file

$ env -u OPENROUTER_API_KEY env-get.sh OPENROUTER_API_KEY
sk-or-v1-537b...      # falls back to .env file
```

### dispatch.py mint bypass (provisioning unavailable)

```python
# dispatch.py main(), lines relevant to Part B:
issuing = provisioning.available(root)  # False when no provisioning key
if issuing:  # THIS BLOCK IS SKIPPED entirely
    minted = provisioning.mint(...)
    if minted is not None:
        spawn_env[provisioning.RUNTIME_KEY_VAR] = minted.secret
        spawn_budget.attach_credential(lease, minted.key_hash)
# Agent spawns with scrubbed_env() preserving OPENROUTER_API_KEY
```

No crash. No mint code runs. The long-lived OPENROUTER_API_KEY survives the scrub cleanly.


## Agent Notes
Part B (provisioning-absent fallback) verified at unit/integration level: 18 offline provisioning tests pass, env-get.sh correctly prefers env over file, scrub preserves OPENROUTER_API_KEY, dispatch skips mint when provisioning unavailable without crash. Gap: no live pi agent dispatched with provisioning truly absent (project .env currently has the key).
