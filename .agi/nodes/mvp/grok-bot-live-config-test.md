---
id: mvp:grok-bot-live-config-test
mint_id: ffe9e4ae7dce408e8c4d991ac266c023
type: mvp
parents:
  - experiment:grok-bot-live-config-resolves
next_edges: []
title: test_grok_bot_adapter.py must assert the live config row, not an in-memory copy
confidence: 0.9
status: implemented
tags:
  - mvp
  - grok-bot
  - live-config
  - g17.14.3
season: 2
---
<!-- BODY:BEGIN -->
# mvp:grok-bot-live-config-test

## MVP

`extensions/agi/tests/test_grok_bot_adapter.py` must carry a live-config
section that reads the project's REAL `.agi/config.json` and asserts the
`grok-bot` harness row resolves there. Test-only; no production bytes.

## Minimum behaviour required (the live-config section)

1. **Real file, found by walk.** `_project_root()` walks up from the test
   file until it finds a real `.agi/config.json`; no hardcoded absolute path.
2. **Read-only fixture.** `live_cfg` is a module-scoped fixture that loads the
   on-disk config with `json.loads(read_text(...))` and never writes it back.
3. **Row resolves to the adapter.** `test_live_config_grok_row_resolves`
   asserts `resolve(live_cfg, "grok-bot")` returns `name == "grok-bot"`,
   `row["adapter"] == "grok_bot"`, and `row["bin"] ==
   live_cfg["harnesses"]["grok-bot"]["bin"]` — the `bin` is compared against
   the loaded cell, not a literal path, so the test tracks the config.
4. **Peers unbroken.** `test_live_config_peers_still_resolve` asserts `pi`
   resolves to adapter `pi` and `copilot-cli` resolves to adapter
   `copilot_cli`, so the fourth harness did not disturb the first three.
5. **Dispatch stays harness-agnostic.** `test_dispatch_still_has_zero_grok_hits`
   reads `extensions/agi/bin/dispatch.py` and asserts `"grok"` does not occur
   (case-insensitive) — the `goal:g4.6` property that adding a harness edits
   no dispatch code.

The in-memory tests above the section stay: they exercise the adapter surface
directly. The live-config section is what fails if the shipped row is ever
dropped from `.agi/config.json`.

## Out of scope

- The adapter module (`goal:g17.14.1`) and the config row itself
  (`goal:g17.14.2`) — placed here as prerequisites only.
- Any edit to `dispatch.py`, `DEFAULT_BIN`, or the locked stub `restart`.

## Falsifier

The suite stays green after `del cfg["harnesses"]["grok-bot"]` (the gate probe
shows `AdapterError`), or the `bin` equality passes against a mutated
`/nowhere/grok-bot` cell (the wire probe shows it differs).