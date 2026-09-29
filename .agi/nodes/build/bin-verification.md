---
id: build:bin-verification
mint_id: 31f5d65b54e84282bd6c3e6b86ea4fb8
type: build
parents:
  - goal:g7.16.1.2.6
  - mvp:dg3-p-park-tag
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
Council bundle 2 row P (director-general-3, mvp:dg3-p-park-tag): check_formation reads the park TAG parked:<goal> through ONE git grep (_grep_live, no rglob, deprecated skipped) and FAILs while any THOUGHT still carries the retired THOUGHT-line park mark. parked_carriers is the one reader the write.py set-active hook shares. R5's retired-template FAIL is unchanged.
<!-- THOUGHT:END -->
