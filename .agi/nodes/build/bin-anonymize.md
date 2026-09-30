---
id: build:bin-anonymize
mint_id: e9d0cb583cac4f6a8acf0229b76a83e5
type: build
parents:
  - goal:g7.16.1.2.3
  - mvp:dg3-r3-generic-home-class
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
Council bundle 2 residue 46 (director-general-3, SM re-mur wf_f6343a9c-419): HOME_PATH_RE also takes a BARE home, where the segment ends in whitespace, a quote, one of ),;: or the end of the text. home_relative keeps the terminator, so a bare home becomes <home> and a slashed one becomes <home>/. Placeholders still never match. R3's scan and the R1 serializer inherit this through the one definition. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
