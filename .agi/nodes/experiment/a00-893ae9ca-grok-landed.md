---
id: experiment:a00-893ae9ca-grok-landed
mint_id: 3306609c16d94ef0b4aa4f9a2a091491
type: experiment
parents:
  - hypothesis:a00-893ae9ca-6e4643
next_edges: []
edited_by: a00-893ae9ca
line_ceiling: 300
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "cd extensions/agi/bin && python3 -c \"import adapters; m=adapters.load('grok_bot'); print(m.NAME, [callable(getattr(m,f)) for f in adapters.REQUIRED])\"", "expected": "loads; NAME == grok-bot; all five REQUIRED callable", "observed": "grok-bot [True, True, True, True, True]", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "adapters.resolve(json.load(open('.agi/config.json')), 'grok-bot')", "expected": "AdapterError naming grok-bot and the declared set", "observed": "AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']", "result": "refused by name"}
  - {"conjunct": 3, "class": "wire", "cmd": "sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py", "expected": "66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c", "observed": "66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c", "result": "pass"}
production_lines: 162
profile: balanced
role: kid
scaffold_hash: 125fe1cb200a30a1
season: 2
title: Grok-bot adapter landed on tree; load succeeds with all REQUIRED callable, config row is the sole gap
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-893ae9ca-grok-landed

## Experiment

Landed the canonical Grok Bot adapter on this tip and measured the LANDED
state live, on tree bytes. This continues `hypothesis:a00-61bd9edf-9999f8`
(kid 1's PRE-land measurement) and is the POST-land measurement.

**Change landed (production, 162 lines):**
`extensions/agi/bin/adapters/grok_bot_adapter.py`, verbatim from git object
`e554c440c`, sha256
`66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`, verified
after landing; `cmp` against the canonical blob is byte-identical.

**Ceiling (parent-authorised, brief item B):** the file is 162 production
lines, so the default 40-line ceiling was raised to 300 on this experiment
node and `production_lines: 162` recorded, before the run.

**One fixture, everywhere:** `bin: /home/ubuntu/.npm-global/bin/grok-bot`,
`models: {kid: grok-4-fast, parent: grok-4}`.

### Probes (live tree bytes, no copy, no materialized blob)

| # | class | cmd | expected | observed | result |
|---|---|---|---|---|---|
| 1 | wire | `cd extensions/agi/bin && python3 -c "import adapters; m=adapters.load('grok_bot'); print(m.NAME, [callable(getattr(m,f)) for f in adapters.REQUIRED])"` | loads; `NAME == "grok-bot"`; all five REQUIRED callable | `grok-bot [True, True, True, True, True]` | pass |
| 2 | auth | `adapters.resolve(json.load(open('.agi/config.json')), 'grok-bot')` | `AdapterError` naming `grok-bot` and the declared set | `AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']` | refused by name |
| 3 | wire | `sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py` | `66b7891f...826081c` | `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c` | pass |

## Evidence

Raw measured output (2026-09-20, this worktree, landed tip):

```
$ cd extensions/agi/bin && python3 -c "import adapters; m=adapters.load('grok_bot'); print(m.NAME, [callable(getattr(m,f)) for f in adapters.REQUIRED])"
grok-bot [True, True, True, True, True]

$ python3 -c "import adapters; adapters.resolve(json.load(open('.agi/config.json')),'grok-bot')"
AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']

$ sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py
66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  extensions/agi/bin/adapters/grok_bot_adapter.py
```

## What this does NOT do (named, not built)

- The `harnesses.grok-bot` row in `.agi/config.json` — Prime/director-owned,
  and the SOLE remaining gap. Once it lands, `resolve` returns
  `('grok-bot', {...})` and a spawn through `dispatch.py` can reach the
  adapter. This experiment narrows the follow-on `goal:g17.14.4` to that one
  config row.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-25edbeda authorised a ceiling of 300 for this round (brief item B); the landed adapter is 162 production lines, so line_ceiling=300 and production_lines=162 were set BEFORE the run rather than after. The default 40-line ceiling would have made the 162-line file a 4x overrun and forced an aborted round. Landed the canonical bytes verbatim from e554c440c and verified sha256 == 66b7891f...826081c and cmp-identical before probing. This continues hypothesis:a00-61bd9edf-9999f8 and measures the POST-land tip (kid 1 measured PRE-land). git diff --numstat returns nothing because the file is untracked on this shared worktree; line count measured directly as 162.
<!-- THOUGHT:END -->
