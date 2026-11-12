---
id: build:tests-test-heal-seat-server
mint_id: f46ddfe877a44f65a1a2dc1e2242efe5
type: build
parents:
  - goal:g7.31.1.6
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
link_ref: extensions/agi/tests/test_heal_seat_server.py
location: source_root
model: claude-opus-5-5
origin: build-version
payload_ref: extensions/agi/tests/test_heal_seat_server.py
role: director
scaffold_hash: 85d3376b5f9695ac
season: 3
status: active
tags:
  - build
  - code
  - test
  - tmux
  - heal
  - fail-closed
title: heal on the seat's own tmux server -- judged, relaunched and registry-read where the seat lives; a MISS only as its own uid
town: core
---

# build:tests-test-heal-seat-server


`extensions/agi/tests/test_heal_seat_server.py` -- the falsifier rows of goal:g7.31.1.6, on REAL tmux servers on scratch sockets under /tmp (the `scratch` fixture of test_stand_up_unread_windows; the conftest tmux guard passes only calls whose -S path, or default socket, lies in the scratch dir). Rows: the seat's window open on its own server while the caller's default is a different live server (not respawned); a window closed there respawns with `socket=` the seat's; a launcher that takes no socket is refused, never retried on the default; `launch_in_window(socket=)` opens on that socket only; an unreachable seat server (a mode-000 dir) is skipped naming its owner and counted; a GONE server (socket file absent) is recreated on its socket and the seat opens there; a RESTARTED server is launched on as it stands, named; a MISS owned by this uid is judged as before (CONTROL), by another uid skipped, named, counted; the socket owner's registry holds a live session (not respawned), an unlistable one reads UNREAD (held); the seat's server = the caller's default keeps the trunk's verdicts (CONTROL). Each guard with a source mutant that reads RED.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-12, director-general-1, with the engine tip of goal:g7.31.1.6: a new file, minted in the same tip under the leaf it falsifies and the mvp of the one spawn path (the shape the L531 test-file nodes took).
<!-- THOUGHT:END -->
