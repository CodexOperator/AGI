---
id: build:bin-adapters-grok-bot-adapter
mint_id: 93a56c119e7442f6bdb844afbf08832f
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-67fbbdf2
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
Why THIS version exists: the adapter and its test were built on the goal:g17.14.* lineage and exist as committed bytes on two sibling loop tips (44e6f11a7, 1e9e94b75), but neither tip is on core/season2/main and the file is absent on this base. That is DT.23 residue 1: a real engine file with no build node on the tip level3.py scans, so a rescan would mint a second, competing `build:bin-adapters-grok-bot-adapter` and any provenance link to the file would not resolve. This node and the file arrive together as ordinary writes in this worktree — no merge, no cherry-pick — so the tip has exactly one build node per file. `mint_id 93a56c11…` is the DT.21 canonical id, deliberately reused rather than re-minted, and it is unclaimed elsewhere on this tip (checked). Parent `mvp:unified-spawn-path` is the design node that specified the harness seam and it resolves here. The stale `spawn_check_reason` both prior nodes carried ("schema 'build' is discriminated on 'build_kind', which this node does not set") is FALSE on bytes that do set `build_kind: code`, so it is not carried. `origin: build-version` records that this is a version carried onto a new tip, not a fresh scan.
<!-- THOUGHT:END -->