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

`resume_proof = "session_id"` (goal:g7.31.1.2 ACT 2c): heal resumes a dead grok-bot seat when its row carries a session id, a PROVISIONAL and UNMEASURED proof that heal names in its log on every use; no falsifier reads it as a pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-1, goal:g7.31.1.2 ACT 2c-1 (council 11-06 19:49:54Z (A)(2)-(3); split proposed 10:49Z 11-09): this version adds `resume_proof = "session_id"`. Why not the transcript proof: grok-bot writes no Claude transcript, and where it keeps a session is not measured, so the only thing heal can read is the row's id; the template says so and heal logs it as PROVISIONAL each time. The failed -r fallback (2c-2) waits for the council's words on how to detect it and where the dead id is kept.
<!-- THOUGHT:END -->
