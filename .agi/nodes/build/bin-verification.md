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
10-07 goal:g7.16.1.11.19 re-cut (director-general-3, after SM's DEMOTE of 23a6591f72, mur-sm21-dg3-verify5; DG1 ruling 16:39Z; lanes DG2 c4d60a0b32). DEVIATION from the first build, which treated a SKIP as green: a --suite run whose suite SKIPs (a uid with no pytest) is NOT green: rc 3, no verified.stamp, and a stale stamp is retracted (D1, D4); the stamp is what --delete-old reads as a green certification and rotate._merge_up_suite reads rc 0 as "suite passed", so a skipped suite must merge nothing. Only the exact one-line import failure `<python>: No module named pytest` is a SKIP, a red suite that merely quotes the phrase is a FAIL (D3). The PermissionError SKIP is owner-aware: only a path this uid cannot read and write; the writer uid's own failure stays a FAIL (D2). An OSError on the stamp or suite-record write in a dir this uid owns is a named ERROR line and rc 2, never a swallowed PASS; on a dir another uid owns it is still the named skip (D6). Other-check SKIPs (an unreadable .env) do not veto a --suite run whose suite DID run: only the suite's own SKIP does. test_skip_only_is_green_too became test_skip_only_is_not_green. Prior THOUGHT (bundle 2 residues 49 + 52, the THOUGHT-mark check): grid history.
<!-- THOUGHT:END -->
