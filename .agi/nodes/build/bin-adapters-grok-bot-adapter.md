---
id: build:bin-adapters-grok-bot-adapter
mint_id: 93a56c119e7442f6bdb844afbf08832f
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-d9c0ff8e
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
`07f2ef7f76c263551882f3adbe436828b65b2c609e9e55e710c034c9da5e6dec`, 168 lines.

Surfaces: `NAME`, `resolve_bin`, `model_args` (a missing tier errors by name,
never a silent fallback), `child_env` (the ONE credential-none rule), a
measurable stub `build_command`, `is_alive`, a real `restart`, and an explicit
`needs_credential -> False`. It is loaded by `adapters.load("grok_bot")`; it is
reachable through config: `.agi/config.json:107` carries the `harnesses.grok-bot` row;
Belam's cell (`goal:g7.25.2`) is live -- the adapter IS selectable, not out of scope.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EF.70 a00-b6a44c26: the duplicate live ids this node EF.53 THOUGHT recorded are now RESOLVED. The a00 file took id build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9, unset link_ref, was marked status deprecated and moved to .agi/nodes/deprecated/build/ (mint 07acc9ce unchanged, no git rm, no supersedes pair); mint 93a56c11 here is the ONE live id and reads its payload. Prose corrected to the live bytes: payload sha 07f2ef7f.../168 lines (was 66b7891f.../162), .agi/config.json:107 carries the harnesses.grok-bot row (was not-yet-reachable/out-of-scope), and the old absolute that no committed reader flags two live files sharing one id is FALSE -- loader.py:222-227 warns and sets graph.duplicate_ids, dashboard.py:279 find_duplicate_ids, stitch.py:436-444 duplicate_payload_ref. ONE residual, measured: the retired node KEEPS payload_ref because the [build] schema requires it and schema_registry.dsl.validate has no conditional rule, so write.py refuses the removal and stitch --verify duplicate_payload_ref stays 1; clearing it needs a schema/engine allowance for deprecated nodes or a supersedes chain, neither in this round scope.
<!-- THOUGHT:END -->
DH.406 a00-d9c0ff8e: `build_command` accepted `rendered_brief` and DROPPED it -- argv carried only `context_file`, the zoom MAP, so a grok-bot spawn would have started with no first turn and said nothing. That was read as the declared `goal:g17.14.1` argv stub; it is not one. A stub is a guess about the CLI's SPELLING; discarding the render is a content loss, and the docstring's "measurable stub" was being used as a licence to drop bytes. Measured before: `['grok-bot','--model','x/y','-p','/tmp/ctx.md']`, sentinel absent; the three sibling adapters all spend the render via `brief.assemble`. Built: the `-p` slot (the flag this file already guessed) now carries the render, copilot's spelling, and keeps the old context-path shape when no render was handed over. The FLAG is still a stub -- `grok-bot --help` was never read -- so the spelling stays unverified; this fixes the loss, not the guess. See experiment:a00-d9c0ff8e-e22309.

## Agent Notes
DT.24 (a00-8f215541): re-landed through write.py in place so the write log carries a sanctioned update_node entry keyed to this node canonical mint id; the DT.23 landing was hand-written and left no write-log record. Payload bytes (sha256 07f2ef7f...e6dec, 168 lines), parents, payload_ref, link_ref and build_kind are unchanged.
