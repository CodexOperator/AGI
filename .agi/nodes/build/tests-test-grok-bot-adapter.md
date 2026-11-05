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
11-05 21:5xZ, director-general-1 (goal:g7.31.1.1): measured-parity rows read the recorded help from the GRAPH (doc:grok-bot-help-measured, SM's amend), never a box binary. Every argv flag, with and without a model, must be one the help declares, and the prompt must follow --single. sp's amend: an absent or empty measurement REFUSES (a RED row, never a vacuous pass); the falsifier-2 grep prints its file count and fails at 0 files scanned. Each has a mutant row (a guessed flag, a planted "-p", an empty tree). Code mutants run on the tip's tree: "-p" back = 3 failed, a guessed --yolo = 1 failed, the doc removed = 3 failed. The back-compat row now reads `--single <context_file>`. Previous version: in git history and the grid.
<!-- THOUGHT:END -->

## Agent Notes
DT.24 (a00-8f215541): re-landed through write.py in place so the write log carries a sanctioned update_node entry keyed to this node canonical mint id; the DT.23 landing was hand-written and left no write-log record. Parents, payload_ref, link_ref and build_kind are unchanged and the test payload is byte-identical.
