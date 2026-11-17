---
id: build:tests-test-write-node-heading
mint_id: 063e7d4729c4442783d6dc86230ab948
type: build
parents:
  - goal:g7.16.1.11.46.38
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
link_ref: extensions/agi/tests/test_write_node_heading.py
location: source_root
model: claude-sonnet-5-5
origin: build-version
payload_ref: extensions/agi/tests/test_write_node_heading.py
role: director
scaffold_hash: d2b67d007b262863
season: 3
status: active
tags:
  - build
  - code
  - test
  - node-writer
  - heading
title: write_node mints ONE heading -- own, none, titled, the token boundary, the dot, Overview/fence/heading=False, and the stamp, each with a mutant
town: local-maxxing
---

# build:tests-test-write-node-heading


`extensions/agi/tests/test_write_node_heading.py` -- the falsifier rows of goal:g7.16.1.11.46.38: `write_node` mints ONE heading for its node. Each row mints into a scratch root (the `_mint` helper, a `.agi/` with the real schemas linked) and counts the node's own heading with the token-boundary form `^# goal:<id>(\s|$)`: an own heading in the body, none, a titled own id, g1.2 against g1.25.1, a dot in the id, `# Overview` / a code fence / a late heading / `heading=False`, and the stamped `scaffold_hash` against the bytes written (with `is_complete` unchanged). Every row has a mutant that replaces the one helper `_body_opens_with_own_heading` (or `scaffold_hash`) and reads RED.
