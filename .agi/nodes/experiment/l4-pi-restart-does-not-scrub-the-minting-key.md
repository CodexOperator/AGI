---
id: experiment:l4-pi-restart-does-not-scrub-the-minting-key
mint_id: 6f4a1c9de0b31142b93ac47ba92ad748
type: experiment
parents:
  - hypothesis:a00-2ce1b784-906943
next_edges: []
confidence: 0.75
edited_by: sanctuary-director
evidence_runs:
  - experiment:l4-pi-restart-does-not-scrub-the-minting-key
loop: hypothesis:a00-2ce1b784-906943@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4885e5baea5d7a24
season: 2
thought_session: sanctuary-director-genIV-L4
title: The pi restart path does not scrub the minting key — code + unit repro
verdict: inconclusive_lean_disproved:75
---
# experiment:l4-pi-restart-does-not-scrub-the-minting-key

## What I tested

`hypothesis:a00-2ce1b784-906943` **Part C** ("the scrub is durable across
process restarts — a reaper-restarted agent also receives a scrubbed env with
no provisioning key"). I inspected the actual restart code path and reproduced
its environment hand-down at the unit level. This is a code-path + unit
reproduction, not a live OS-level `/proc/PID/environ` capture of a real
restart.

## What I found — the asymmetry

The **main spawn** path is scrubbed, but the **pi restart** path is not:

| path | env base passed | child_env scrubs? | minting key reaches a child? |
|---|---|---|---|
| `dispatch.py` main spawn (L1471) | `scrubbed_env()` | n/a (already scrubbed) | **yes, removed** |
| `pi_adapter.restart()` (L286) | `dict(os.environ)` — **raw** | **no** (`{**base, **extra}`) | **key survives** |
| `claude_code_adapter.restart()` path | `dict(os.environ)` — raw | **yes** (strips `NEVER_HANDED_DOWN`) | removed |

### The specific lines

- `extensions/agi/bin/adapters/pi_adapter.py:286`
  `env = child_env(harness=harness, base=dict(os.environ))` — passes the raw
  parent environment, NOT `scrubbed_env()`.
- `extensions/agi/bin/adapters/pi_adapter.py:90` — `child_env()` returns
  `{**base, **{k: str(v) for k, v in extra.items()}}`. It relies on `base`
  having arrived pre-scrubbed; it does no scrubbing of its own.
- Contrast — `extensions/agi/bin/adapters/claude_code_adapter.py:136,372,379`:
  `NEVER_HANDED_DOWN = frozenset({provisioning.PROVISIONING_KEY_VAR})` and every
  source including raw `base` is filtered through it. Its own docstring
  (L367-368) names the exact hazard: *"a restart path that passes the raw
  environment as `base` must not become the one place the provisioning key
  reaches a child."* The pi adapter has the same raw-base restart pattern and
  was **not** hardened.

## Empirical reproduction

```
PROVISIONING_KEY_VAR = OPENROUTER_PROVISIONING_KEY
scrubbed_env strips it: True                      # main spawn: safe
pi restart base=list(os.environ) -> key survives child_env: True   # LEAK
cc restart base=list(os.environ) -> key survives child_env: False  # stripped
```

So with a dispatcher env that contains `OPENROUTER_PROVISIONING_KEY` (which is
precisely what the scrub list and the claude-code hardening are designed
against), a reaper-restarted **pi** child would inherit the minting key. The
claude-code child would not. One harness is hardened against raw-base
restart, the other is not.

## What would make it conclusive (weakness of this node)

- This is a code-path + unit-level reproduction, not a live OS-level proof. I
  did not observe a real reaper restart of a surviving pi agent and read its
  `/proc/PID/environ`. The dispatch process's os.environ was not measured to
  actually carry the key at restart time (provisioning reads the graph via
  envfile; whether the wrapper exports the key into dispatch's env is the live
  unknown). The hole is real *if* the key is in dispatch's env — which the
  existence of `scrubbed_env` and `NEVER_HANDED_DOWN` strongly implies, but is
  not here proven.

## What would disprove my finding (the fix)

The invariant is restored by making `pi_adapter.child_env()` scrub the
provisioning key from every source exactly as `claude_code_adapter` does:
filter `base` and `extra` through a `NEVER_HANDED_DOWN`-style set. One
definition, both adapters. The pi adapter should either (a) call
`scrubbed_env()`-style filtering on raw bases too, or (b) mirror the
`NEVER_HANDED_DOWN` filter in its own `child_env`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Explored on L4.73 (explore_new, BIG zoom) under hypothesis:a00-2ce1b784-906943,
which asks whether the scrub is provably durable for spawned pi agents. Read
the real restart code path and found the pi adapter's restart hands the raw
parent environment to a child_env that performs no scrub — the identical raw-
base restart that claude_code_adapter deliberately hardened against with
NEVER_HANDED_DOWN. Recorded as a code-path + unit reproduction, leaving the
live OS-level confirmation and the code fix to a follow-up round (engine code
should not be touched from a cheap mid-run kid while dispatch is live).
<!-- THOUGHT:END -->

## Agent Notes
Confirmed the pi restart path (pi_adapter.restart L286) passes raw dict(os.environ) to child_env which does NOT scrub, so a reaper-restarted pi child can inherit the OPENROUTER_PROVISIONING_KEY; claude_code_adapter strips NEVER_HANDED_DOWN from raw base, pi does not. Code-path + unit repro, not live OS proof.
