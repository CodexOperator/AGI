---
id: build:bin-write
mint_id: e182844f902942749470304cda98f744
type: build
parents:
  - mvp:the-modal-shell-over-the-verbs
  - goal:g13.1
next_edges: []
build_kind: code
confidence: 1.0
edited_by: sanctuary-director
origin: build-scan
payload_ref: extensions/agi/bin/write.py
scaffold_hash: b0dad82bf930e6f8
season: 1
tags:
  - build
  - code
thought_session: sanctuary-director-genVI
title: "Build: extensions/agi/bin/write.py"
---
# build:bin-write

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two additions on top of the payload verb. payload_text <content> writes the bytes inline, the way note writes a body, so replacing a payload no longer needs a scratch file; payload <path> stays for bytes that already exist as a file or are large, and payload - reads stdin at the CLI layer for content the script separator cannot carry. Every payload write now resolves through the nodes named location, with a location set in the same edit winning over the one on disk, because naming a new base and moving the bytes is one intention. create --payload stamps location explicitly rather than leaving the default implicit -- an implicit default is the hardcoding this replaced, one level up. Found while writing this very thought: prose containing the script separator breaks parse_script for EVERY prose verb, not just payload_text. The stdin path covers payload; note and thought have no equivalent escape yet.
<!-- THOUGHT:END -->