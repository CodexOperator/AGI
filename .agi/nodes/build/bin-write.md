---
id: build:bin-write
mint_id: e182844f902942749470304cda98f744
type: build
parents:
  - goal:g7.16.1.2.6
  - mvp:dg3-p-park-tag
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-3
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
Council bundle 2 residues 54 + 55 note (director-general-3): the set-active hook reads update_node's result, and catches an OSError from a carrier's write. Either way the carrier prints 'unpark REJECTED <id> (parked:<goal>): <reason>' on stderr and the loop goes on to the next carrier. Row P's item_regex judgment and the drop-on-set hook are otherwise unchanged. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
