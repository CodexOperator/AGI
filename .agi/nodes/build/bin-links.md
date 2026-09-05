---
id: build:bin-links
mint_id: af3bbccbaa6f4aec8908e46e37816ce1
type: build
parents:
  - mvp:the-modal-shell-over-the-verbs
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director
location: source_root
origin: build-scan
payload_ref: extensions/agi/bin/links.py
scaffold_hash: b1d27882fe79fbb3
tags:
  - build
  - code
thought_session: L1.13
title: "Build: extensions/agi/bin/links.py"
---
# build:bin-links

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version as a node -- links.py had no build node until now, found while recording this change. link_path takes the nodes location and resolves through locations.resolve_payload_path, so link resolution and payload resolution agree by construction instead of by coincidence; resolve() reads location off the frontmatter it already has.
<!-- THOUGHT:END -->
