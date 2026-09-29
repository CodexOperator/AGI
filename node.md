---
id: build:bin-verification
mint_id: 31f5d65b54e84282bd6c3e6b86ea4fb8
type: build
parents:
  - goal:g7.16.1.2.5
  - mvp:dg3-r5-retired-template-fails
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-3
link_ref: extensions/agi/bin/verification.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/verification.py
scaffold_hash: 6440e5a969f262fa
season: 2
tags:
  - build
  - code
title: "Build: extensions/agi/bin/verification.py"
town: core
---
# build:bin-verification

`extensions/agi/bin/verification.py` -- the one verification pass (skill agi-verify): check levels quick / rotation / full, the node-count floor, the suite window, and the built-in checks (anonymize, bin freshness, seat model, node dirs, formation).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council bundle 2 row R5 (director-general-3, mvp:dg3-r5-retired-template-fails): check_formation FAILs when active names a template that resolves under nodes/deprecated/. The type check still comes first, so a list-valued active FAILs rather than raising. find_node_file is unchanged, so links still resolve retired nodes. Bundle 1's read-back (0/2 FAIL, 1 PASS, THOUGHT-only wake) is unchanged.
<!-- THOUGHT:END -->
