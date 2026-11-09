---
id: build:templates-harness-grok-bot
mint_id: 67367ba09f8940548929f739e77d990e
type: build
parents:
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
edited_by: director-general-1
link_ref: extensions/agi/templates/harness/grok-bot.toml
location: source_root
origin: build-version
payload_ref: extensions/agi/templates/harness/grok-bot.toml
role: director
season: 3
status: active
tags:
  - build
  - code
  - harness
  - grok-bot
  - template
title: "grok-bot seat template -- the interactive seat argv and its registry-free session join"
town: core
---
<!-- BODY:BEGIN -->
# build:templates-harness-grok-bot

`extensions/agi/templates/harness/grok-bot.toml` -- the grok-bot SEAT argv as template data: `--model`, `-s <session>` (a first spawn names its NEW conversation), `-r <resume>` (a restart), the prompt positional (the interactive seat in a named tmux pane; the headless `--single` dispatch argv is the adapter's, goal:g7.31.1.1). Every flag is declared by the recorded help (doc:grok-bot-help-measured). `[roles] source = "row"`: its model comes from its own `harnesses.grok-bot` row. `[session] registry = "none"`: grok-bot keeps no Claude-style `<pid>.json`, so rotate.py joins the seat through the pane's process tree and reads the session id back from the seated process's argv (goal:g7.31.1.2 ACT 2b). No tool-approval flag: a POLICY gap left for the owner's / belam's GO on the live run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-1, goal:g7.31.1.2 ACT 2b (council 3/3, alive [decision] 17:59:23Z 11-07): minted now; the file landed at ACT 2a (L426) without a node, and the card carried it to ride 2b. This version adds `[session] registry = "none"`, the template-declared switch that sends this harness's seats to the pane join; every other template keeps the claude registry by default (test_pane_join.py, the every-template row). Parents [mvp:unified-spawn-path], the shape its sibling adapter and adapter-test nodes use.
<!-- THOUGHT:END -->
