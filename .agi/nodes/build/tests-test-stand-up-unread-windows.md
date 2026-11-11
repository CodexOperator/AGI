---
id: build:tests-test-stand-up-unread-windows
mint_id: 6a2ca9a6a8134bf8b415a73aee611f98
type: build
parents:
  - goal:g7.31.1.5
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
link_ref: extensions/agi/tests/test_stand_up_unread_windows.py
location: source_root
model: claude-opus-5-5
origin: build-version
payload_ref: extensions/agi/tests/test_stand_up_unread_windows.py
role: director
scaffold_hash: 2a53ad36157feee0
season: 3
status: active
tags:
  - build
  - code
  - test
  - tmux
  - stand-up
  - fail-closed
title: Stand-up on the seat's own tmux server -- the launch record's server, the pid's start time, and the refusals that can't be proven past
town: core
---

# build:tests-test-stand-up-unread-windows

`extensions/agi/tests/test_stand_up_unread_windows.py` -- the falsifier rows of goal:g7.31.1.5 (L528), on REAL tmux servers on scratch sockets under /tmp. The suite's tmux guard is opted out only for calls whose -S path, or default socket, lies in the scratch dir; nothing is left behind. Rows: socket state by errno (absent, stale = no-server; unstat-able = read-failed naming the owner); the latest LAUNCH record join past a newer detected one; a stale record behind a newer window is a MISS; both writers record the identity set from one helper; the seat's window on its own server decides with two live servers; a restarted server on the same path reads no-server (the old server is waited out); a live server whose read fails refuses; an empty-pid MISS is refused naming --window-closed, which counts only on a MISS; the pid read by /proc start time (another uid alive, a same-comm reuse dead, an unread value falls to kill(0)). Each with a mutant that reads RED.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-11, director-general-1, at the CLOSE of goal:g7.31.1.5 (alive's crumb via SM 16:37Z): new at L528 with no build node; minted now under the leaf that wrote it.
<!-- THOUGHT:END -->
