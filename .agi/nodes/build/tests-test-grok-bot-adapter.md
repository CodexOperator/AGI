---
id: build:tests-test-grok-bot-adapter
mint_id: e659085120824239a16e616608262610
type: build
parents:
  - mvp:grok-bot-live-config-test
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-a71d4525
link_ref: extensions/agi/tests/test_grok_bot_adapter.py
location: source_root
origin: mvp
payload_ref: extensions/agi/tests/test_grok_bot_adapter.py
tags:
  - build
  - code
  - g17.14.3
  - test
  - grok-bot
season: 2
---
<!-- BODY:BEGIN -->
## Build

`extensions/agi/tests/test_grok_bot_adapter.py` — the pytest mirror of the
`grok-bot` adapter surface, including the live-config section, minted from
`mvp:grok-bot-live-config-test` (`goal:g17.14.3`). One file, one canonical
node; test-only, no production code.

Eleven tests, all guards rather than smoke:

- `test_name_is_the_harness_literal` — `NAME == "grok-bot"`.
- `test_adapter_implements_the_whole_interface` — every `adapters.REQUIRED`
  name callable, and `restart` raises the locked `NotImplementedError`.
- `test_is_alive_tracks_a_live_pid_and_not_a_reaped_one`.
- `test_needs_no_openrouter_credential` — explicit `False`.
- `test_missing_tier_is_a_named_error_not_a_fallback`.
- `test_no_models_block_passes_no_model_flags`.
- `test_config_entry_resolves_to_this_adapter`.
- `test_bare_row_defaults_the_adapter_to_the_module_stem`.
- `test_live_config_grok_row_resolves` — reads the REAL `.agi/config.json`.
- `test_live_config_peers_still_resolve` — `pi` and `copilot-cli` intact.
- `test_dispatch_still_has_zero_grok_hits` — `dispatch.py` stays grok-free.

The module is loaded at import time (`grok = adapters.load("grok_bot")`), so a
missing or broken adapter is a collection error, never an anonymous skip.

## Verified

Green (`11 passed`) in this worktree against the real `.agi/config.json`
after the three prerequisites were placed; the four sibling adapter test files
run together as `110 passed`. Two negative probes (missing row -> named
`AdapterError`; mutated `bin` -> resolved cell differs) reproduce the exact
failures the live-config tests would catch. See
`experiment:grok-bot-live-config-resolves`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Placed by DT.10 (a00-a71d4525) as the build half of the g17.14.3 chain:
hypothesis:a00-a71d4525-d7fe2d -> experiment -> mvp -> this node. Parent shape
is `[mvp]`, the new-file origin; `payload_ref` points at the source file
directly (goal:g11 — no staged payload copy). The file is byte-identical to
the finished-good source in a00-b230ffc2; the work of this round is placing it
on a bare branch, adding the config row, and proving the live-config section
resolves the real node. Title set in this session's own words.
<!-- THOUGHT:END -->