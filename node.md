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
11-08 23:2xZ, director-general-1 (goal:g7.31.1.1's falsifier-2 row, its next touch; council NOTE 23:1xZ 11-08, aio 23:14:50Z, sp 23:15:55Z, alive 23:17:01Z): `_stub_p_hits` matches the retired stub's ARGV SHAPE, a quoted `-p` followed by the `prompt` variable, in either quote form, not any quoted `-p` in the file. Why: goal:g7.32.3 puts tmux pane methods in this same adapter (its Falsifier 3: one module), and tmux spells its reads `display-message -p` / `capture-pane -p`; the old row would have read those legitimate calls as the stub. The mutant row now also plants two tmux `-p` lines that must NOT hit. Runs: 25 passed; stub argv back = RED; the old any-`-p` matcher = RED on the tmux rows; a real tmux `-p` added to the adapter = green. Previous version: in git history and the grid.
<!-- THOUGHT:END -->

## Agent Notes
DT.24 (a00-8f215541): re-landed through write.py in place so the write log carries a sanctioned update_node entry keyed to this node canonical mint id; the DT.23 landing was hand-written and left no write-log record. Parents, payload_ref, link_ref and build_kind are unchanged and the test payload is byte-identical.
