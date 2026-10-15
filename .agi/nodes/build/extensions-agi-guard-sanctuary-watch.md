---
id: build:extensions-agi-guard-sanctuary-watch
mint_id: f0372eb6b824418989bb42da8abe1cae
type: build
parents:
  - goal:g7.16.1.7
  - idea:the-guard-is-in-the-graph
next_edges: []
build_kind: code
edited_by: belam
link_ref: extensions/agi/guard/sanctuary-watch
location: source_root
payload_ref: extensions/agi/guard/sanctuary-watch
scaffold_hash: f86ebc3fb73073d8
season: 2
title: "Build: extensions/agi/guard/sanctuary-watch"
town: core
---
# build:extensions-agi-guard-sanctuary-watch

`extensions/agi/guard/sanctuary-watch` — the sanctuary guard, in the graph (goal:g7.16.1.7; idea:the-guard-is-in-the-graph).
Layer 5, installed to ~/.local/bin by guard-init.sh: every 2 min, cap-kill alerts here and ping + ssh probes of every other town in hosts.json.
`~/work/.sanctuary/guard/sanctuary-watch` is a symlink to this file (the untracked original is kept beside it as `*.pre-graph-20260930`).
Settings: config:guard. The why, the layers and the kill switches: `extensions/agi/guard/GUARD.md`.
