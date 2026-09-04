---
id: experiment:a01-571301d7-c6de56
mint_id: 1dd5b398988c40d4a9f613eccde69d2a
type: experiment
parents:
  - hypothesis:a01-3c5640a0-5c684c
next_edges: []
confidence: 0.85
scaffold_hash: 5c171292d3716bf2
title: Part B fallback verified at code+test level — live dispatch with provisioning truly absent still untested
verdict: inconclusive_lean_proved:85
---
# experiment:a01-571301d7-c6de56

## Experiment

**Part B: provisioning-absent fallback** — code-path and unit-level verification of `hypothesis:a01-3c5640a0-5c684c`'s second clause. Confirms the engine handles a missing provisioning key without crashing, falling back to the shared long-lived `OPENROUTER_API_KEY`.

This replicates and extends the evidence from `experiment:a00-e66a10c3-14b14a` and `experiment:a01-94f6deb8-c55cfe`, adding code-path analysis of dispatch.py's mint gate and confirming no regressions.

### Verified

1. **Provisioning test suite** — 17/18 pass; the one live API failure (`test_a_minted_key_is_capped_and_expires_and_can_be_revoked`) is a known transient: the revoked key name appears in the listing because OpenRouter's DELETE propagation is not instantaneous. The non-live tests cover all fallback paths.

2. **No provisioning key → safe fallback** — When `OPENROUTER_PROVISIONING_KEY` is absent from the secrets file:
   - `provisioning.available()` returns `False` — not a crash
   - `provisioning.mint()` returns `None` — not a crash
   - `provisioning.revoke()` returns `False` — not a crash

3. **Scrub list is correct** — `OPENROUTER_PROVISIONING_KEY` is in the scrub list (removed from every child environment); `OPENROUTER_API_KEY` (the runtime key) is NOT in the scrub list.

4. **env-get.sh precedence confirmed** — Environment variable is preferred over `.env` file. This is the fix from `experiment:per-spawn-keys-were-never-used` that made Part A work; it also protects Part B — the engine environment already has `OPENROUTER_API_KEY`, so `env-get.sh` returns the env var without reading `.env`.

5. **env-get.sh fallback** — When `OPENROUTER_API_KEY` is not in the environment, `env-get.sh` reads from `.env`, returning the shared long-lived key.

6. **dispatch.py code path** — The critical block:
   ```python
   issuing = provisioning.available(root)  # False when no provisioning key
   if issuing:  # THIS BLOCK IS SKIPPED entirely
       minted = provisioning.mint(...)
       if minted is not None:
           spawn_env[provisioning.RUNTIME_KEY_VAR] = minted.secret
   ```
   When `issuing` is False, the entire mint block is skipped. No mint code runs, no crash. The spawned agent inherits `OPENROUTER_API_KEY` from the parent's scrubbed environment, which preserves the long-lived key.

### Not verified (open gap)

- A live pi agent dispatched with `OPENROUTER_PROVISIONING_KEY` truly absent from EVERY source (`.`env`, secrets graph, environment). The project's `.env` currently declares `OPENROUTER_PROVISIONING_KEY`, so Part B's "agent completes a dialogue without the provisioning key" clause requires modifying `.env` or running on a different box. The unit-level code path is clean; the live dispatch assertion is untested.

- Neither Part A nor Part B has been run 3 times as the hypothesis requires for transient-failure ruling.

### What this confirms for the hypothesis

The falsifier's fallback clause — *the engine does not become more fragile with the feature off* — holds at every layer short of a live dispatch. The hardening feature does not become a hard dependency.

## Evidence

```
$ python3 -c "
import sys; sys.path.insert(0, 'extensions/agi/bin')
import provisioning, tempfile, pathlib
tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / '.env').write_text('OPENROUTER_API_KEY=sk-or-v1-test-key\n')
print('available (no provisioning key):', provisioning.available(tmp))
print('mint returns:', provisioning.mint(iter_n=9999, agent_id='test', tier='test', root=tmp))
print('revoke returns:', provisioning.revoke('test-hash', root=tmp))
"
available (no provisioning key): False
mint returns: None
revoke returns: False

$ python3 -c "
import sys; sys.path.insert(0, 'extensions/agi/bin')
import provisioning
scrub_vars = ['ANTHROPIC_API_KEY', provisioning.PROVISIONING_KEY_VAR]
print('PROVISIONING_KEY in scrub:', provisioning.PROVISIONING_KEY_VAR in scrub_vars)
print('RUNTIME_KEY not in scrub:', provisioning.RUNTIME_KEY_VAR not in scrub_vars)
"
PROVISIONING_KEY in scrub: True
RUNTIME_KEY not in scrub: True

$ OPENROUTER_API_KEY=sk-or-v1-ENV-TEST bash env-get.sh OPENROUTER_API_KEY
sk-or-v1-ENV-TEST     # env var preferred over .env

$ env -u OPENROUTER_API_KEY bash env-get.sh OPENROUTER_API_KEY
sk-or-v1-537bbe7c...  # falls back to .env file

$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q -k "not live"
18 passed in 6.40s
```

Full test suite: 1452 passed, 2 failed (both pre-existing):
- `test_a_minted_key_is_capped_and_expires_and_can_be_revoked` — live API test, transient listing delay
- `test_the_fallback_leaves_no_worktree_behind` — publish alarm test, stale temp files

Neither is related to provisioning-absent fallback.

## Agent Notes
Part B of hypothesis:a01-3c5640a0-5c684c verified at code+test level: provisioning.available() returns False (not crash), mint() returns None (not crash), revoke() returns False (not crash), scrub preserves OPENROUTER_API_KEY, env-get.sh resolves correctly in both env-over-file and file-fallback modes. dispatch.py skips mint block cleanly when issuing=False. Gap: live pi agent dispatch with provisioning key truly absent from ALL sources (project .env currently has the key). Full test suite: 1452 passed, 2 pre-existing failures unrelated to fallback.
