---
id: idea:the-guard-is-in-the-graph
mint_id: c27b06fab5ff4a028734cc6a1f103389
type: idea
parents:
  - goal:g7.16.1.7
next_edges: []
edited_by: belam
scaffold_hash: fe3609ca58d4e5c6
scale: small
season: 2
title: "The sanctuary guard lives in the repo: build nodes + config:guard, old paths symlinked"
town: core
---
# idea:the-guard-is-in-the-graph

## Idea

The sanctuary guard (guard-init.sh, sanctuary-health, sanctuary-watch, GUARD.md) moves out of the untracked
`~/work/.sanctuary/guard/` into the repo at `extensions/agi/guard/`, one build node per file; its per-box settings
(`guard.env`) become the `config:guard` node in `.agi/nodes/.geometry/`, keyed by BOX name, never host name.
The old paths become symlinks into the repo, like the engine's other global handles (skills, hooks, the `agi` command).
scale: small (an extension: new files, no new chain).

## Why

Owner 2026-09-30 00:0xZ (goal:g7.16.1.7): "are the guard scripts and the guard dot env in the graph as a build node
and a .geometry node respectively" -- measured NO: the 09-29 option (b) change was versioned only by `.bak` copies.
Owner order: "Sweet go ahead and do the changes and add it in then symlink it like the rest."

## Falsifier

`sudo ~/work/.sanctuary/guard/guard-init.sh --dry-run` through the symlink reports zero "would change" lines and the
same values it reported from the untracked copy (oomd 85 %, user@ MemoryHigh, watchdog PSI full 60 %); `--status`
passes; the committed files and node hold zero host names and zero IP addresses.
