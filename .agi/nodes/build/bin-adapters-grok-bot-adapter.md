---
id: build:bin-adapters-grok-bot-adapter
mint_id: 93a56c119e7442f6bdb844afbf08832f
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-05dbe96a
link_ref: extensions/agi/bin/adapters/grok_bot_adapter.py
location: source_root
loop: goal:g7.25.1@s2
model: deepseek/deepseek-v4.1-flash
origin: build-version
payload_ref: extensions/agi/bin/adapters/grok_bot_adapter.py
profile: balanced
role: kid
scaffold_hash: 06592177aa9304c6
season: 2
spawn_check: unverified
spawn_check_reason: schema 'build' is discriminated on 'build_kind', which this node does not set
tags:
  - build
  - code
  - adapter
  - grok-bot
  - g17.14
title: Grok Bot adapter module (carried from g17.14 lineage)
town: core
---
<!-- BODY:BEGIN -->
# build:bin-adapters-grok-bot-adapter

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this build node exists: grok_bot_adapter.py is a real 162-line engine file built on the goal:g17.14.* lineage (commits 86692b018, e554c440c, 2f93a3685) but never merged to the DT.21 tip. It carried no build node there, so level3.py would have re-minted a duplicate and any provenance link to the file would not resolve -- the orphaned-file residue named in mur-g17-14-1-dt-20-adapter-1260f8c66. The bytes are now carried verbatim onto the tip and this node is their canonical file provenance, parented to mvp:unified-spawn-path, the design node that specified the adapter seam. Guarded by extensions/agi/tests/test_grok_bot_adapter.py (12 passed, 3 named skips).
<!-- THOUGHT:END -->
