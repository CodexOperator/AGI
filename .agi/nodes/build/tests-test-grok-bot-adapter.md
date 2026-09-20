---
id: build:tests-test-grok-bot-adapter
mint_id: e659085120824239a16e616608262610
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-67fbbdf2
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
Why THIS version exists: DT.23 residue 3. On the sibling tips the peers test sat behind the same `live_cfg` fixture as the three grok-specific tests, and that fixture `pytest.skip`s when Belam's `harnesses.grok-bot` row is absent — so the regression it guards (a shipped row lost, or an adapter stem mis-derived by `adapters.resolve`) was swallowed by a gate that has nothing to do with it. The row is not landing in this round (Belam owns it, `goal:g7.25.2`), so the test is split rather than un-gated wholesale: `live_cfg_raw` reads the real `.agi/config.json` with no gate, `live_cfg` keeps the grok gate for the two tests that genuinely need the row, and the peers test now reads the raw fixture and covers all four shipped rows. No non-live assertion is weakened; the only assertion changed is the peers test's, and it gained two rows (`claude-code`, `pi-local`). `mint_id e6590851…` is the g17.14-lineage canonical id for this test node; its former parent `mvp:grok-bot-live-config-test` does not resolve on this tip, so the node parents to `mvp:unified-spawn-path` — the same design node as the adapter build node — keeping the two files one lineage. Recorded here so the next level3 scan does not re-mint a duplicate.
<!-- THOUGHT:END -->