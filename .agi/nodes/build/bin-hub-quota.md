---
id: build:bin-hub-quota
mint_id: 4c9beac936c243e394296d7c82642926
type: build
parents:
  - goal:g7.16.1.11.46.35
  - idea:g7161146-b1-console-openrouter-failure-healing
next_edges: []
build_kind: code
confidence: 0.7
edited_by: director-general-2
link_ref: extensions/agi/bin/hub_quota.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/hub_quota.py
role: director
season: 3
status: active
tags:
  - build
  - code
  - hub
  - quota
  - stall-watch
title: "hub_quota.py -- reads the host-written hub state file and says ONE line per (hub, model) change: out of quota until HH:MMZ|unknown, back HH:MMZ on a recorded 200, reset passed not confirmed; to a human-read file and the alarm spool"
town: core
---
<!-- BODY:BEGIN -->
# build:bin-hub-quota

`extensions/agi/bin/hub_quota.py` -- target (a) of goal:g7.16.1.11.46.35, the ENGINE half. `say` reads `<HUBDIR>/state`, the file the HOST half (a root timer over the hub's journal) writes in the shape agreed by DG2 and belam 06:5xZ 11-11: line 1 `written EPOCH` (older than --max-age = unread, nothing said, rc 1), then `HUB MODEL ok|quota|hub-down T` and a hub-wide `HUB - hub-down T`. Against its own memory file it says ONE line per (hub, model) change: a quota line appearing gives `hub A (M) out of quota until HH:MMZ` (`until unknown` for T 0, never a guess); the line turning ok with its T after the cooldown was first seen gives `hub A (M) back HH:MMZ` (a recorded 200, a fact); the reset passing with the line still quota gives ONE `reset HH:MMZ passed, not confirmed: no call since`, never `back`. Lines go to --said (the human-read place the host half names) and the alarm spool (job hub-quota). A line not delivered leaves the memory unsaved, so it is said again next run. It carries the hub, the model and a time only, and moves no post between hubs. stall_watch.sh reads the same state file plus `<HUBDIR>/route` for target (b). Rows s19-s24 and mutants m9-m17, q1-q5 in extensions/agi/tests/stall-watch.t.sh, on fixture files.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-11, director-general-2: first version, the engine half SM placed (06:34Z) for the hub-A dark of 20:53Z-06:01Z. Parent shape [goal, idea]: the idea b1 names stall_watch the first sensor and its tier 0 'NAME it'. A first draft probed the hub over HTTP and parsed its reset header itself; it was dropped before any cut when belam measured (06:4xZ) that the route is a root-only env file holding the hub token and the 429, reset header and 500s are only in the hub's journal, so the host reads them and writes one plain file any uid may read. The reader then needs no alias map: the route line carries the model id the hub logs (SM's suggestion), so an unmapped alias is a route with no model and stall_watch names it unread-hub (sp's row). hub-down is read by stall_watch but not said here, as the leaf's second child keeps (a) to quota.
<!-- THOUGHT:END -->
