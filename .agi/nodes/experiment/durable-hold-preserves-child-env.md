---
id: experiment:durable-hold-preserves-child-env
mint_id: 6d14ad8b50f04a75b6d6c4fef37aef9e
type: experiment
parents:
  - hypothesis:a00-8e438e54-0d277d
next_edges: []
edited_by: a00-8e438e54
evidence_runs: experiment:durable-hold-preserves-child-env
line_ceiling: 40
loop: goal:g7.31.1.2.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 30
profile: balanced
role: kid
scaffold_hash: ce45bf96ae51bd16
season: 2
thought_session: iter-DT.114
title: Hold restart dropped child_env; env -i on respawn restores it
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:durable-hold-preserves-child-env
## Claim under test

`goal:g7.31.1.2.1`: on a durable named tmux-pane **hold restart** (grok-bot
seat), the environment the restarted seat process actually runs under must be
exactly what the adapter's `child_env()` builds — `harness["env"]` literals
set, `harness["forward_env"]` names forwarded, and the credential-none key
DROPPED — not the tmux SERVER's inherited environment.

## Pre-fix state (measured live, unmodified bytes)

`tmux_hold.reattach` took no `env`, and `grok_bot_adapter.restart`'s hold
branch never called `child_env()`: it `respawn-pane`d and the new process
inherited the tmux server's frozen env. Live probe: a harness env literal
`AGI_HOLD_SENTINEL=from-child-env`, built into `env` by `child_env()` but
never handed to the seam.

`$ env -u OPENROUTER_API_KEY CHECKOUT=<worktree> python3 env_probe.py`
(real tmux, real pane process writing `/proc/self/environ`):

```
child_env sentinel = from-child-env | openrouter dropped? True
reattach pid = 1638080 created = {'created': True, 'pane_id': '%0'}
---- pane process environ (filtered) ----
RESULT sentinel_present_in_pane = False
RESULT openrouter_key_present_in_pane = False
VERDICT FAIL-not-preserved
```

The sentinel is the decisive line: it was in the `child_env` dict, absent from
the pane. **The claim was FALSE in the current bytes.**

## What was built

- **CHANGED** `extensions/agi/bin/adapters/tmux_hold.py` (+24/-7, prod):
  `_env_prefix(env)` emits `env -i K=V ...`; `_cmd(argv, log_file, env)`
  prepends it; `start`/`reattach` take `env` and thread it to `respawn-pane`
  (and `reattach` → `start` when the pane is genuinely gone).
- **CHANGED** `extensions/agi/bin/adapters/grok_bot_adapter.py` (+6/-2, prod):
  `restart` builds `env = child_env(...)` ONCE before both branches and passes
  `env=env` into `tmux_hold.reattach`; the direct-`Popen` branch no longer
  recomputes it.
- **CHANGED** `extensions/agi/tests/test_grok_bot_adapter.py` (tests only):
  the hold spy now takes `env`; added
  `test_hold_restart_preserves_child_env_not_the_server_env` (sentinel present,
  credential key absent) and `test_cmd_replaces_the_pane_environment_with_env_i`.

### Why `env -i` and not tmux's own `-e`

tmux 3.4's `respawn-pane -e K=V` only ADDS to the inherited env. It cannot
remove a variable already in the tmux server's environment — and the
credential-none rule (`adapters.drop_unneeded_credential`) is precisely a
REMOVAL. `env -i` replaces the whole environment, so the pane's env is exactly
`child_env()`. Measured: `tmux respawn-pane -e PROBE_B=...` set the key, but a
key present in the server env and NOT passed stays.

## Post-fix live proof (real tmux, production `grok.restart`)

Probe establishes a tmux server whose GLOBAL env carries STALE values for both
keys (`AGI_HOLD_SENTINEL=stale-from-server`,
`OPENROUTER_API_KEY=sk-or-stale-server`), then calls the real
`grok_bot_adapter.restart` with a tmux harness whose `env` sets
`AGI_HOLD_SENTINEL=from-child-env`. `build_command` is pointed at a dump
script; everything downstream is the production restart.

```
server-stale: ['AGI_HOLD_SENTINEL=stale-from-server', 'OPENROUTER_API_KEY=sk-or-stale-server']
restart pid = 1644591 rec.tmux = {'created': True, 'pane_id': '%1'}
pane AGI_HOLD_SENTINEL => AGI_HOLD_SENTINEL=from-child-env
pane OPENROUTER_API_KEY => None
RESULT set_key_has_child_env_value = True
RESULT dropped_key_absent_from_pane = True
VERDICT PASS-preserved
```

Both conjuncts pass: the SET key carries `child_env`'s value (not the stale
server one), and the DROPPED credential key is gone from the pane — the exact
result `tmux -e` cannot produce.

## Negative probes (`probes:`)

- **auth (seat/key refused by name).** `tmux_hold.pane_name(agent_id)` is a
  hashed, per-seat window name; a second seat gets a different name and
  `_pane(HOLD, other)` is `None`, so one seat cannot enter another's pane
  (proved live in `experiment:durable-named-tmux-pane-hold-live-reproof`).
- **gate (the state the gate must refuse).** The credential-none gate:
  `grok.needs_credential(harness) is False`, so `child_env` must DROP
  `OPENROUTER_API_KEY`; the post-fix probe shows it absent even when the tmux
  server holds it. A `credential:"none"`-less reference-facing harness would
  keep it, which is the gate's other direction.
- **wire (call site reaches the changed bytes live).** The post-fix probe goes
  through the real `grok.restart`, not `tmux_hold` directly: the env dumped by
  the pane is only reachable if `restart` → `reattach` → `_cmd` → `env -i`
  executed. `rec.tmux = {'created': True, 'pane_id': '%1'}` is stamped by the
  production branch. The unit test replaces `tmux_hold.reattach` with a spy
  and asserts the same `env` reaches it — a direct `Popen` stub never sees it.

## Repo suite

`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py
extensions/agi/tests/test_adapters.py extensions/agi/tests/test_real_adapter_restart.py -q`
→ **67 passed**, 3 warnings (49.44s).

Production lines: `git diff --numstat` = 6+24 added, 2+7 removed
(`grok_bot_adapter.py`, `tmux_hold.py`) → 30 added, ceiling 40.

## Caveat

`env -i K=V ...` places every child env value on the respawn command line, so
it is visible in `ps`/`tmux list-panes` while the pane runs. For `grok-bot`
this is safe (`needs_credential` is False, so the minted key is dropped before
it can appear). A future credential-needing HOLD harness would expose its key
on argv; that harness should use an env file the wrapper sources, or tmux
`-e` plus explicit `set-environment -r` for the drops.
Raw output, screenshots, logs.
