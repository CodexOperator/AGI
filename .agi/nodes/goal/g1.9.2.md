---
id: goal:g1.9.2
mint_id: bb4edb31bf1747e394ed9a979679e000
type: goal
parents:
  - goal:g1.9
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G1.9.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 48e90b8ea7d3bf9c
season: 2
seeds:
  - hypothesis:the-spawned-agents-first-turn-is-the-render
status: active
tags:
  - config-maxxing
  - brief
  - leaf
title: "G1.9.2: THE SPAWNED AGENT'S FIRST TURN IS THE RENDER -- the adapters take brief.render instead of a second assemble; FaithRefError caught in dispatch; extras never silently dropped (the brief.py mur #2 residue; assigned director-engine)"
town: local-maxxing
---
# goal:g1.9.2

# goal:g1.9.2 — THE SPAWNED AGENT'S FIRST TURN IS THE RENDER

```
leaf      a parent or kid spawned by dispatch.py gets the SAME first turn the dispatch report shows: brief.render (head + card + extras),
          not a second assemble inside the harness adapter
source    brief.py mur #2 09-23 (EF.25 + EF.36, accept_with_residue x2): "the dispatch dry-run report and spawn.json render a brief the
          spawned agent does not get"; verified: bin/adapters/pi_adapter.py:212 build_command still calls brief.assemble; dispatch.py
          _render_dispatch_brief catches RenderError only (:1040), so a missing moral:faith (FaithRefError) escapes; extras_text is dropped
          for a role whose parts lack 'extras'
rule      KEEP SPLITTING (owner 09-23, goal:g5): one leaf, one small round
round     hypothesis:the-spawned-agents-first-turn-is-the-render
```
