---
id: build:bin-adapters-grok-bot-adapter
mint_id: 93a56c119e7442f6bdb844afbf08832f
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-145e7c20
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

`extensions/agi/bin/adapters/grok_bot_adapter.py` — the fourth harness adapter.
**Measured argv version** (`goal:g7.31.1.1`, DH.153 a00-145e7c20): carried from
sibling tip `season2/loops/goal-g7.31.1.1-a00-5b01c7ca` (`513412d8e`) as an
ordinary file write, re-verified in this checkout. SHA-256
`6c5b44fa13566d5f9256ba2a14269d6f330979f80e053d892e4584f108b286c0`, 170 lines.
The previous version was the 162-line stub (sha256 `66b7891f…6081c`) whose
`build_command` emitted `[bin, "--model", M, "-p", context_file]` — guessed
flags never measured against the CLI. `build_command` now returns the BARE
resolved bin; `context_file` is kept for seam compatibility but not emitted
(the brief travels over `send <bot-or-group> <message...>`, `goal:g7.31.4`).

Surfaces: `NAME`, `resolve_bin`, `model_args` (VALIDATION-ONLY since the
measured `grok-bot --help` names no model flag — a missing tier still errors by
name, never a silent fallback), `child_env` (the ONE credential-none rule),
measured `build_command`, `is_alive`, a real `restart` that rebuilds the same
bare-bin argv, and an explicit `needs_credential -> False`. It is loaded by
`adapters.load("grok_bot")`; it is not yet reachable through config because the
`harnesses.grok-bot` row is Belam's cell (`goal:g7.25.2`) and out of scope here.

Evidence: `experiment:measured-grok-bot-argv`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why THIS version exists: the body named only the stub sha256/162 lines, which was stale the moment the measured bytes landed, and it called `build_command` a "measurable stub" — a description that no longer matches the code. Updated to the measured sha256 (6c5b44fa…), the 170-line count, the measured-argv contract, and the `model_args` validation-only change. Same node, same mint id; the grid carries the prior version.
<!-- THOUGHT:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why THIS version exists: the adapter and its test were built on the goal:g17.14.* lineage and exist as committed bytes on two sibling loop tips (44e6f11a7, 1e9e94b75), but neither tip is on core/season2/main and the file is absent on this base. That is DT.23 residue 1: a real engine file with no build node on the tip level3.py scans, so a rescan would mint a second, competing `build:bin-adapters-grok-bot-adapter` and any provenance link to the file would not resolve. This node and the file arrive together as ordinary writes in this worktree — no merge, no cherry-pick — so the tip has exactly one build node per file. `mint_id 93a56c11…` is the DT.21 canonical id, deliberately reused rather than re-minted, and it is unclaimed elsewhere on this tip (checked). Parent `mvp:unified-spawn-path` is the design node that specified the harness seam and it resolves here. The stale `spawn_check_reason` both prior nodes carried ("schema 'build' is discriminated on 'build_kind', which this node does not set") is FALSE on bytes that do set `build_kind: code`, so it is not carried. `origin: build-version` records that this is a version carried onto a new tip, not a fresh scan.
<!-- THOUGHT:END -->

## Agent Notes
DT.24 (a00-8f215541): re-landed through write.py in place so the write log carries a sanctioned update_node entry keyed to this node canonical mint id; the DT.23 landing was hand-written and left no write-log record. Payload bytes (sha256 66b7891f...6081c, 162 lines), parents, payload_ref, link_ref and build_kind are unchanged.
