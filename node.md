---
id: goal:g1.23.2
mint_id: 5de6ac7992364bde991068dc189726d4
type: goal
parents:
  - goal:g1.23
next_edges: []
confidence: 0.5
goal_id: G1.23.2
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: e4fcf22f653b6459
season: 3
seeds: []
status: horizon
tags: []
title: "G1.23.2: one agi plugin lets Hermes and any plugin or MCP host use the graph and its loop through the existing channels"
town: core
---

# goal:g1.23.2

## Why this exists
goal:g1.23 (decide the distribution shape: drop-in clone, skill package, or install): the owner asked on 11-07 (below) for agi to be easy to use inside Hermes and any other agentic host that takes plugins. A plugin IS a distribution shape, the way agi arrives in another host, so it is g1.23's own question. Measured on trunk bac67e28d6: no live node holds a plugin, distribution or license line (alive's read 23:50:05Z 11-07), and the only tracked files named *plugin* are 4 retired renderer nodes under .agi/nodes/deprecated. Placed by the council (alive [decision] 23:50:05Z 11-07, 3/3) as a horizon leaf: no builder until its design exists.

## OWNER 2026-11-07 20:42:45Z (c:be72d519c116), verbatim
From belam's [owner] 20:47:15Z 11-07 (box commit 86a44591bf on refs/box/belam/sanctuary-master). Item 2, whole, the owner's words in quotes:
"I'm guessing the falsify plugin isn't agi based? I kinda was hoping the plugin would allow easy use of AGI inside of hermes and of course any other agentic env that supports plugins of that format or similar. Like a more complete wrapper on the MCP but I'm unsure of how to totally formalize it and was hoping that this could be a test of the system to do an AGI like implementation where you make all the important decisions and make it all well optimized."
belam's reading, marked MINE in that message, decided as Prime: "falsify (MIT, verified, on time) stays the 11-11 entry: it IS agi's falsifier rule as one organ. An agi plugin (the graph + its loop usable from Hermes and any plugin/MCP host, reusing our existing channels: box, grid, nodes, skills, not new ones) is a new goal for the council to design with no deadline; falsify can be its first tool."
The two lines of item 3 that name the plugin, the owner's words:
"we always wanna reuse existing channels and remix or swirl or rotate them in new unique ways. Less complexity is always better."
"We can use the swarm lesson fuel and new metrics and this to do the plugin overall."

## Target end-state
- agi (the graph and its loop) is usable from Hermes and from any host that loads plugins of that format or MCP servers, through one plugin.
- The plugin uses only agi's existing channels (box, grid, nodes, skills) and adds none.
- falsify can be its first tool (belam's Prime reading).
- It is built under job 2's take-away rule (the whole-system CRAP / DRY pass, owner item 3): each part earns its place, measured.

## Invariants
- No new channel: the plugin reuses box, grid, nodes and skills.
- No builder until a council design doc exists, after the dashboard leaf (council placement 23:50:05Z 11-07).

## Falsifier
1. Exits 0 only when designed: a doc node whose parents include goal:g1.23.2 holds the council's design:
   `git grep -l -E '^  - goal:g1\.23\.2$' -- .agi/nodes/doc | grep -q .`
   RUN at the mint on trunk bac67e28d6: exit 1 (no such doc).
2. Negative, until that doc exists: no plugin code is built. `git ls-files -- extensions skills src | grep -ci plugin` reads 0 (0 at the mint).
The build's own falsifier (a plugin host loads agi and runs one falsify call through an existing channel) is written in the design doc, not here.

## Out of scope
goal:g1.23.1 (the license) · job 2's whole-system optimize pass itself · falsify's 11-11 entry (it stays as belam placed it)

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-07 (mint, v1): minted on the council's placement (alive [decision] 23:50:05Z 11-07, 3/3). Status horizon: the plugin has no builder until a council design doc exists, after the dashboard leaf. Assigned to the council because the design is the council's to write; no post builds it yet. Falsifier written at the mint, as the placement left it open: F1 = that design doc exists (a doc node parented on this goal), exit 1 at bac67e28d6; F2 (negative) = no plugin code under extensions, skills or src before then, 0 at the mint. The build's own falsifier (a host loads agi and runs one falsify call) belongs to the design doc.
<!-- THOUGHT:END -->
