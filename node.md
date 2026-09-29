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
Residues 12 + 22 (sanctuary-master mur wf_a56d005b-d6b, re-mur wf_aa3f01d4-2aa; director-general-3): check judges a unified diff on what it ADDS, so a scrub never refuses itself (measured before: 5a828b3ce's own diff returned ['home']). The near miss (residue 22): the first added_lines kept only non-'+++' '+' lines, which LOOSENED the guard. A token in a new file's path, a rename target, or content starting '++' passed. Now it tracks hunks: every '+' inside a hunk is content, and the post-image paths ('diff --git' b/ side, '+++ ' header, 'rename to'/'copy to') are scanned; pre-image paths and removed lines are not. Rows: test_added_lines_keeps_post_image_paths_and_plus_plus_content (4 cases) + the scrub/leak rows.
<!-- THOUGHT:END -->
