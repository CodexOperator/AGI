---
id: build:tests-test-write
mint_id: 6409f73e1d964e598d9801ab633a64d3
type: build
parents:
  - mvp:the-modal-shell-over-the-verbs
  - goal:g13.1
next_edges: []
build_kind: code
confidence: 1.0
edited_by: sanctuary-director
origin: build-scan
payload_ref: extensions/agi/tests/test_write.py
scaffold_hash: 55fb1454eaa9eb25
season: 1
tags:
  - build
  - code
thought_session: sanctuary-director-genVI
title: "Build: extensions/agi/tests/test_write.py"
---
# build:tests-test-write

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Five more tests: inline bytes land with a trailing newline ensured, payload and payload_text are the same operation, a node with location: docs_root writes into the configured tree and NOT into the default one with the same relative ref, an unknown location refuses instead of defaulting, and create stamps the location it used. The third and fourth are the ones with teeth -- both are ways bytes could land in the wrong tree while the command reports success.
<!-- THOUGHT:END -->