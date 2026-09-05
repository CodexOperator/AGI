---
id: build:tests-test-write
mint_id: 6409f73e1d964e598d9801ab633a64d3
type: build
parents:
  - mvp:the-modal-shell-over-the-verbs
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director
origin: build-scan
payload_ref: extensions/agi/tests/test_write.py
scaffold_hash: 55fb1454eaa9eb25
tags:
  - build
  - code
thought_session: L1.13
title: "Build: extensions/agi/tests/test_write.py"
---
# build:tests-test-write

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version as a node. Carries five tests for the payload verb: the bytes land together with the thought, the destination mode survives, a node with no payload_ref is refused by name, a missing source refuses rather than emptying the file, and a missing destination refuses rather than creating one. The last two are the ones worth having -- both are ways a typo could destroy a payload silently. Verified red with the change stashed.
<!-- THOUGHT:END -->
