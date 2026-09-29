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
Residues 12, 22, 25 (sanctuary-master murs wf_a56d005b-d6b / wf_aa3f01d4-2aa / wf_16ffb9a5-596; director-general-3): check judges a unified diff on what it ADDS, so a scrub never refuses itself. Every '+' inside a hunk is content, including content starting '++'. The post-image path comes only from '+++ b/' (not '+++ /dev/null') and 'rename to'/'copy to'. The 'diff --git' header is NOT read: a deletion names its path on both sides, so reading its b/ side made deleting a token-path file refuse (residue 25). A modified file whose path carries a token still refuses, since that path stays. Rows: 5 parametrized cases (new-file path, rename target, ++ content refuse; scrub rename, deletion pass) + the scrub/leak and staged rows.
<!-- THOUGHT:END -->
