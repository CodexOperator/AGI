---
id: hypothesis:grok-bot-env-bin-overrides-missing-cell
mint_id: c2898244cbd84f20b8185fd22d72b94c
type: hypothesis
parents:
  - goal:g7.25
next_edges: []
confidence: 0.8
edited_by: director-thought-2
model: grok-4.6
role: director
season: 2
tags:
  - grok-bot
  - adapter
  - encryption-town
testable_claim: "On encryption-town, with the live harnesses.grok-bot.bin cell still missing, $GROK_BOT_BIN overrides it: a PATH name or an existing absolute path makes resolve_bin succeed and build_command emit documented argv; a missing absolute refuses by name; unset env still raises the C3 FileNotFoundError."
title: "$GROK_BOT_BIN overrides a missing live grok-bot bin cell without a config write"
town: core
---
# hypothesis:grok-bot-env-bin-overrides-missing-cell

## Measured
- verdict:dt2-grok-bot-live-bin-1004 DISPROVED C3: live cell `~/.npm-global/bin/grok-bot` does not exist here; PATH `grok-bot` does (`/usr/local/bin/grok-bot` -> `grok`).
- Adapter docstring + `adapters.resolve_bin`: `$GROK_BOT_BIN` > harness `bin` > `DEFAULT_BIN` (`grok-bot`). Named refusal when a path-shaped override/cell does not exist.
- `box n` 17:24Z empty. Cell unchanged. Did not write `.agi/config.json`.
- g7.25 F1–F3 still MET (load, resolve of the row, dispatch.py grok hits = 0).

## CLAIM
C1. `GROK_BOT_BIN=grok-bot` (bare PATH name) → `resolve_bin(live row)` returns `grok-bot`; `build_command` emits `[grok-bot, --model, grok-4-fast, -p, hello]`.
C2. `GROK_BOT_BIN=/usr/local/bin/grok-bot` (existing absolute) → that path.
C3. `GROK_BOT_BIN=/no/such/grok-bot` (missing absolute) → FileNotFoundError naming the harness, the path, and `$GROK_BOT_BIN`.
C4. unset env + live row → the same C3 FileNotFoundError as verdict:dt2-grok-bot-live-bin-1004 (regression).
All four → proved. Any fail → disproved. Void: load/resolve of the row itself fails.

## Dispatch line
config-max: none this round (the cell is still g7.30 / SM). template-max: none. code: none (no adapter edit). Measurement of the documented override only.

## FALSIFIERS
- C1 or C2 still raises → disproved
- C3 does not refuse by name → disproved
- C4 succeeds with unset env → disproved (contradicts the prior verdict)
- load/resolve of the row fails → void

## TESTS
No new test file. pytest absent this uid. Commands on the experiment node.

## FILE SCOPE
this hypothesis, its experiment, its verdict, the g7.25 thought/seeds. Not `.agi/config.json`. Not `grok_bot_adapter.py`.

## CEILING
0 production lines, one builder, CPU, 0 USD. Wall cap 5 min. No billed grok spawn.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 17:27Z 10-04 (date -u): owner go. box n empty, live cell unchanged. Nested this leaf under claimed g7.25 rather than waiting on the cell write (out of this post's file scope). Near miss: writing the bin cell ourselves — config-max, g7.25.2 closed, g7.30 is helper's.
<!-- THOUGHT:END -->
