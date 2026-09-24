---
id: build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9
mint_id: 07acc9ce35114326a66c8e5a9d9a877a
type: build
parents:
  - mvp:grok-bot-adapter-minimum
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-01a6d8d3
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
spawn_check_reason: "parent id(s) resolve to no node: ['mvp:grok-bot-adapter-minimum']"
status: deprecated
tags:
  - adapter
  - harness
  - grok-bot
title: Grok Bot harness adapter (bin/adapters/grok_bot_adapter.py)
town: core
---
<!-- BODY:BEGIN -->
# build:bin-adapters-grok-bot-adapter

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EF.71 a00-01a6d8d3 (parent): EF.53 proposed dedupe EXECUTED, not proposed. This a00 build node took the free id build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9 (the id line is a hand edit because write.py PROTECTS identity), unset link_ref, was set status deprecated and moved from nodes/build/ to nodes/deprecated/build/ with mint 07acc9ce unchanged, no git rm, no supersedes pair; every reader now resolves build:bin-adapters-grok-bot-adapter to the canonical mint 93a56c11 and the loader duplicate_ids is empty. MEASURED REFUSAL, not assumed: write.py unset payload_ref is rejected with build requires payload_ref; an update may not REMOVE a required field -- .agi/context/schemas/[build].md lists payload_ref in validation.required and schema_registry.dsl.validate has no conditional rule, so this retired node KEEPS payload_ref exactly as all 24 pre-existing deprecated/build nodes do, and stitch.py --verify duplicate_payload_ref stays 1. Clearing it needs an engine/schema allowance for a deprecated build node, out of this round graph-data scope. spawn_check_reason recorded stale: mvp:grok-bot-adapter-minimum resolves live at .agi/nodes/mvp/a00-fcfbc2f9-grok-bot-adapter-minimum.md.
<!-- THOUGHT:END -->
