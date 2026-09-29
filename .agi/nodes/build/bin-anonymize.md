---
id: build:bin-anonymize
mint_id: e9d0cb583cac4f6a8acf0229b76a83e5
type: build
parents:
  - goal:g7.16.1.1.3
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
Residue 12 of sanctuary-master mur wf_a56d005b-d6b (director-general-3): check now judges a unified diff on its ADDED lines only (added_lines). A removed line is text leaving the repo, so a scrub never refuses itself. Measured before the fix: 5a828b3ce's own diff returned ['home']. Non-diff text is judged whole, as before. Row: test_a_diff_is_judged_on_added_lines_only (scrub passes, leak refuses).
<!-- THOUGHT:END -->
