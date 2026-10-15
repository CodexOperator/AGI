---
id: build:extensions-agi-guard-sanctuary-health
mint_id: 73b45001055246ba8d4fb2868f5d0dd7
type: build
parents:
  - goal:g7.16.1.7
  - idea:the-guard-is-in-the-graph
next_edges: []
build_kind: code
edited_by: belam
link_ref: extensions/agi/guard/sanctuary-health
location: source_root
payload_ref: extensions/agi/guard/sanctuary-health
scaffold_hash: 570a40d1c0396ce1
season: 2
title: "Build: extensions/agi/guard/sanctuary-health"
town: core
---
# build:extensions-agi-guard-sanctuary-health

`extensions/agi/guard/sanctuary-health` — the sanctuary guard, in the graph (goal:g7.16.1.7; idea:the-guard-is-in-the-graph).
The watchdog daemon's test-binary (layer 4), installed to /usr/local/sbin by guard-init.sh: unhealthy when memory PSI full avg60 >= LIMIT.
`~/work/.sanctuary/guard/sanctuary-health` is a symlink to this file (the untracked original is kept beside it as `*.pre-graph-20260930`).
Settings: config:guard. The why, the layers and the kill switches: `extensions/agi/guard/GUARD.md`.
