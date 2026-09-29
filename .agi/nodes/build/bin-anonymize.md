---
id: build:bin-anonymize
mint_id: e9d0cb583cac4f6a8acf0229b76a83e5
type: build
parents:
  - goal:g7.16.1.2.1
  - mvp:dg3-c-home-path-token
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-3
link_ref: extensions/agi/bin/anonymize.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/anonymize.py
scaffold_hash: 9bdf153839da7df1
season: 2
tags:
  - build
  - code
title: "Build: extensions/agi/bin/anonymize.py"
town: core
---
# build:bin-anonymize

`extensions/agi/bin/anonymize.py` -- the physical-token guard at the write seam (SM.122): ONE token list (`box_tokens`), ONE checker (`check`), a box-local pre-commit hook.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council bundle 2 row R1 (director-general-3): HOME_PATH_RE is the ONE spelling of a home-directory path on ANY box (/(home|Users)/<segment>/), and home_relative rewrites this box's HOME to ~ and any other box's to <home>/. rotate.py's record writer uses it; R3's check is to reuse it rather than re-spell the pattern. Bundle 1's check semantics (added lines, post-image paths, new empty/binary files; residues 12/22/25/31) are unchanged.
<!-- THOUGHT:END -->
