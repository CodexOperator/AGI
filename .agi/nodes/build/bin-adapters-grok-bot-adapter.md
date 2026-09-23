---
id: build:bin-adapters-grok-bot-adapter
mint_id: 93a56c119e7442f6bdb844afbf08832f
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-11ad274b
link_ref: extensions/agi/bin/adapters/grok_bot_adapter.py
location: source_root
loop: goal:g7.25.1@s2
origin: build-version
payload_ref: extensions/agi/bin/adapters/grok_bot_adapter.py
role: kid
season: 2
status: active
tags:
  - build
  - code
  - adapter
  - grok-bot
  - g17.14
title: Grok Bot adapter module — fourth harness behind the unified spawn seam
town: core
---
<!-- BODY:BEGIN -->
# build:bin-adapters-grok-bot-adapter

`extensions/agi/bin/adapters/grok_bot_adapter.py` — the fourth harness adapter,
carried onto this tip byte-for-byte from the `goal:g17.14` lineage (sibling tip
`season2/loops/goal-g7.25.1-a00-28ff2420`, `44e6f11a7`). SHA-256
`66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`, 162 lines.

Surfaces: `NAME`, `resolve_bin`, `model_args` (a missing tier errors by name,
never a silent fallback), `child_env` (the ONE credential-none rule), a
measurable stub `build_command`, `is_alive`, a real `restart`, and an explicit
`needs_credential -> False`. It is loaded by `adapters.load("grok_bot")`; it is
not yet reachable through config because the `harnesses.grok-bot` row is
Belam's cell (`goal:g7.25.2`) and out of scope here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R14 #3/#4 correction recorded in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place (RECORD AND PROPOSE ONLY -- no deprecate, no id change, no status change, nothing executed this round). DUPLICATE LIVE ID, measured: .agi/nodes/build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md (mint_id 07acc9ce35114326a66c8e5a9d9a877a) and .agi/nodes/build/bin-adapters-grok-bot-adapter.md (mint_id 93a56c119e7442f6bdb844afbf08832f) BOTH declare id: build:bin-adapters-grok-bot-adapter and both carry payload_ref/link_ref extensions/agi/bin/adapters/grok_bot_adapter.py. The loader keeps the a00 file and hides the DT.24 canonical (mint 93a56c11) from every reader; links.py still reports 0 broken links because both files resolve the id. PROPOSED FIX, not executed: give this a00 node its own id (a free id under the same payload is acceptable since the other node already owns build:bin-adapters-grok-bot-adapter) and deprecate the a00 node with status: deprecated plus a move to .agi/nodes/deprecated/build/ -- mint_id 07acc9ce stays, never git rm, never a supersedes: pair. TOKEN STALENESS, measured: the frontmatter spawn_check_reason here says "parent id(s) resolve to no node: ['mvp:grok-bot-adapter-minimum']" but mvp:grok-bot-adapter-minimum resolves live (its file exists, status active) -- the reason is stale; the field is left as-is this round per the dispatch order (record only). Duplicate-id detection itself is a reader gap (goal:g10): no committed reader flags two live files sharing one id. ADDRESSABILITY GAP, measured this round: write.py -> node_writer.find_node_file resolves this id to nodes/build/bin-adapters-grok-bot-adapter.md (step 1, the canonical slug) FIRST, so the R14 #3 THOUGHT landed on the canonical file and NOT on the a00 duplicate; under the one-write rule (a node edit goes through write.py) the a00 file cannot be addressed by id at all. The duplicate record therefore lives here until a writer can address a second file sharing an id.
<!-- THOUGHT:END -->

## Agent Notes
DT.24 (a00-8f215541): re-landed through write.py in place so the write log carries a sanctioned update_node entry keyed to this node canonical mint id; the DT.23 landing was hand-written and left no write-log record. Payload bytes (sha256 66b7891f...6081c, 162 lines), parents, payload_ref, link_ref and build_kind are unchanged.
