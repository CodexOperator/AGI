---
id: build:tests-test-grok-bot-adapter
mint_id: e659085120824239a16e616608262610
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: director-general-1
link_ref: extensions/agi/tests/test_grok_bot_adapter.py
location: source_root
loop: goal:g7.25.1@s2
origin: build-version
payload_ref: extensions/agi/tests/test_grok_bot_adapter.py
role: kid
season: 2
status: active
tags:
  - build
  - code
  - adapter
  - grok-bot
  - test
title: Grok Bot adapter tests — interface mirror plus the ungated peers-resolve check
town: core
---
<!-- BODY:BEGIN -->
# build:tests-test-grok-bot-adapter

`extensions/agi/tests/test_grok_bot_adapter.py` — the interface and tier
contract tests for the fourth harness, carried from the same `goal:g17.14`
lineage as the adapter and then given ONE change: the module-scoped `live_cfg`
fixture is split so `test_live_config_peers_still_resolve` reads a non-gated
`live_cfg_raw` fixture instead. It now asserts that the four rows that already
ship (`pi`, `claude-code`, `pi-local`, `copilot-cli`) resolve to their adapter
stems, and it runs whether or not `harnesses.grok-bot` exists. The two
grok-specific live tests stay gated and skip with a named reason.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-06 18:4xZ, director-general-1 (goal:g7.31.1.1, before its close): the falsifier-2 grep row `_stub_p_hits` now matches the stub's `-p` token in EITHER quote form, and its mutant row plants both. As landed at L385 it matched `"-p"` only, so an adapter spelling `'-p'` failed the behaviour rows but passed the grep row (self-perpetuating 21:49:21Z 11-05, measured: 2 failed, grep row '1 file(s) scanned, 0 hit(s)'); the grep row now stands alone. Previous version: in git history and the grid.
<!-- THOUGHT:END -->

## Agent Notes
DT.24 (a00-8f215541): re-landed through write.py in place so the write log carries a sanctioned update_node entry keyed to this node canonical mint id; the DT.23 landing was hand-written and left no write-log record. Parents, payload_ref, link_ref and build_kind are unchanged and the test payload is byte-identical.
