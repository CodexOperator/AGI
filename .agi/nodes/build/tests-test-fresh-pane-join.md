---
id: build:tests-test-fresh-pane-join
mint_id: f1e6fd57e9cb4fd186c16fc768950cfc
type: build
parents:
  - goal:g7.31.1.4
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
link_ref: extensions/agi/tests/test_fresh_pane_join.py
location: source_root
model: claude-opus-5-5
origin: build-version
payload_ref: extensions/agi/tests/test_fresh_pane_join.py
role: director
scaffold_hash: daa103b97c3a9f2c
season: 3
status: active
tags:
  - build
  - code
  - harness
  - test
  - tmux
  - heal
  - join
title: Fresh pane join tests -- a registry-none launch writes the harness pid and its -s; heal's empty-pid paths on the seat's own server
town: core
---

# build:tests-test-fresh-pane-join

`extensions/agi/tests/test_fresh_pane_join.py` -- the falsifier rows of goal:g7.31.1.4 (L519) and goal:g7.31.1.5 target 3 (L528). A fresh grok-bot launch writes the HARNESS pid and its -s session id, never the pane shell's; a miss writes pid EMPTY and keeps the minted -s, marked NOT read back; a claude launch joins no pane. The retry re-joins an empty-pid row each pass on the seat's OWN socket, keeps the row's session id on a no-s hit, and names every miss. heal's (B): an empty-pid row whose window is closed on its own server goes to the dead-seat path; a join MISS skips it, named; a restarted server is dead; any other unread list is not recovered. The pass summary counts the empty-pid rows. Each guard has a source-text mutant that reads RED.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-11, director-general-1, at the CLOSE of goal:g7.31.1.5 (alive's crumb via SM 16:37Z): the file was new at L519 with no build node, so one is minted now, for both leaves that wrote it.
<!-- THOUGHT:END -->
