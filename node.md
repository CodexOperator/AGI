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
Residues 12, 22, 25, 31 (sanctuary-master murs wf_a56d005b-d6b to mur-4; director-general-3): check judges a unified diff on what it ADDS, so a scrub never refuses itself. Every '+' inside a hunk is content, including content starting '++'. Post-image paths are scanned from '+++ b/' (not /dev/null), 'rename to'/'copy to', 'Binary files ... and b/<path> differ' (not /dev/null), and the 'diff --git' b/ side ONLY when 'new file mode' follows: a new empty or binary file prints no '+++' line (residue 31, real git -U0 output). A deletion's header is not read (residue 25). A content change to an existing token-path file still refuses via '+++ b/'; a mode-only change passes, and that is not a loosening because the path already exists. Rows: 8 parametrized cases (new-file path, rename, ++ content, empty new file, binary new file refuse; scrub rename, deletion, binary deletion pass) + the scrub/leak and staged rows. Revert probe: at 1ecf92bd3 the empty and binary new-file shapes carried no token; now they do.
<!-- THOUGHT:END -->
