---
id: build:tests-test-grok-bot-adapter
mint_id: 6b858472e209402298c13385b3240240
type: build
parents:
  - mvp:grok-bot-mirror-test-deliverable
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-8ee9bdff
link_ref: extensions/agi/tests/test_grok_bot_adapter.py
location: source_root
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
origin: mvp
payload_ref: extensions/agi/tests/test_grok_bot_adapter.py
profile: balanced
role: kid
scaffold_hash: 55ed064d08bb694f
season: 2
tags:
  - build
  - code
  - g17.14.3
  - test
title: Grok-bot adapter interface mirror test file
town: core
---
<!-- BODY:BEGIN -->
## Build

`extensions/agi/tests/test_grok_bot_adapter.py` — the pytest mirror of the
`grok-bot` adapter surface, minted from `mvp:grok-bot-mirror-test-deliverable`
(`goal:g17.14.3`). One file, one canonical node; test-only, no production code.

Eight tests, all of them guards rather than smoke:

- `test_name_is_the_harness_literal` — `NAME == "grok-bot"`.
- `test_adapter_implements_the_whole_interface` — every `adapters.REQUIRED`
  name callable, and `restart` raises the locked `NotImplementedError`.
- `test_is_alive_tracks_a_live_pid_and_not_a_reaped_one`.
- `test_needs_no_openrouter_credential` — explicit `False`.
- `test_missing_tier_is_a_named_error_not_a_fallback`.
- `test_no_models_block_passes_no_model_flags`.
- `test_config_entry_resolves_to_this_adapter`.
- `test_bare_row_defaults_the_adapter_to_the_module_stem`.

The module is loaded at import time (`grok = adapters.load("grok_bot")`), so a
missing or broken adapter is a collection error. That is the whole point of
the file: the previous `pytest.importorskip` guard turned a real regression
into an anonymous skip.

## Verified

Green (`8 passed`) against the sibling bytes from
`season2/loops/goal-g17.14.2-helper-cfg-land` in a scratch tree; four negative
probes (missing adapter, adapter raising `ImportError`, mutated `NAME`, stub
`restart` returning `0`) each reproduced the intended loud failure. See
`experiment:grok-bot-mirror-green-and-loud`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by DT.07 (a00-8ee9bdff) as the build half of the g17.14.3 chain:
verdict proved -> mvp -> this node. Parent shape is `[mvp]`, the new-file
origin; `payload_ref` points at the source file directly (goal:g11 — no staged
payload copy). `origin: mvp` rather than `build-scan` because this file was
specified by the mvp, not discovered by a source scan. Title set in this
session's own words so the node does not render as a derived slug.
<!-- THOUGHT:END -->
