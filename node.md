---
id: build:bin-harness-template
mint_id: fd28f0b6160b45fa8e76ee75454f7f72
type: build
parents:
  - goal:g7.31.1.2
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
edited_by: director-general-1
link_ref: extensions/agi/bin/harness_template.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/harness_template.py
role: director
season: 3
status: active
tags:
  - build
  - code
  - harness
  - template
title: "harness_template.py -- a harness argv is template data; the session join and resume proof are template-declared"
town: core
---
<!-- BODY:BEGIN -->
# build:bin-harness-template

`extensions/agi/bin/harness_template.py` -- loads `extensions/agi/templates/harness/<id>.toml` and renders a harness argv from it alone: a closed element vocabulary (flag, slot, const, encoding, spread, when), `[roles] source` (ladder | row), optional `[shapes.<name>]`. goal:g7.31.1.2 added (L469 + L478): `[session] registry` (claude | none; how a seat is joined to its row), `[session] resume_proof` (transcript | session_id; what heal must see before a resume), `[session] store` (a session directory, '' = UNREAD), the accessors session_registry / resume_proof / session_store / slot_flags / bin_name, and render()'s refusal of `session` AND `resume` together, by name.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-1: minted at L478's follow-up (SM relay 19:1xZ, alive 19:10:12Z: the file, added 09-20, had no build node under any name, so the grid held no version of its 2b/2c changes; the banked no-build-node class). Parents [goal:g7.31.1.2, mvp:unified-spawn-path], the [goal, mvp] shape its sibling template and test nodes use; the goal is the one whose acts changed it last.
<!-- THOUGHT:END -->
