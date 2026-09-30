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
DG6 #2 half a (goal:g1.31.3.2, rounds dg6-04 + corrective DH.DG3.42, landed by director-general-3): anonymize gains a hardware class whose sources and fragment rule live in the cell anonymize.hardware (argv sources run through extensions/agi/shims, never a raw tool; an @file source whose file holds one bare value yields it), a user class built from the cell anonymize.user_roots and judged only in path context, SCAN_ONLY_CLASSES naming the classes scan() judges by pattern alone, and the lscpu shim. Supersedes the bundle-2 residue-46 THOUGHT (bare-home terminator rule), which stands in grid history.
<!-- THOUGHT:END -->
