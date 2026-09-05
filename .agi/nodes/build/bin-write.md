---
id: build:bin-write
mint_id: e182844f902942749470304cda98f744
type: build
parents:
  - mvp:the-modal-shell-over-the-verbs
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director
origin: build-scan
payload_ref: extensions/agi/bin/write.py
scaffold_hash: b0dad82bf930e6f8
tags:
  - build
  - code
thought_session: L1.13
title: "Build: extensions/agi/bin/write.py"
---
# build:bin-write

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version as a node, and the version that adds the payload verb: replace the bytes a build node points at, in the same submit as the thought that explains them. This was the last node operation with no name -- write.py could revise every field of a build node except the one thing the node exists to describe. The write itself is node_writer.replace_payload, so this module still performs no file write and test_edit_py_contains_no_file_write stays green. Refusals over guesses: a missing source is an error rather than an emptied payload, a missing destination is an error rather than a create, and the destination mode is preserved so replacing a script cannot drop its exec bit (goal:s9). Minted late: the module that IS the write path had no node in the graph until now, found by trying to record this thought against it.
<!-- THOUGHT:END -->
