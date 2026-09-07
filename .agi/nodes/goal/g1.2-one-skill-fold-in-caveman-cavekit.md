---
id: goal:g1.2
mint_id: e4f95f4dffe74c939d08cfbae7351937
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.2
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.2: One skill: fold in caveman, cavekit, and gitnexus"
---
Four systems overlap in this repo and none of them know about the others:
**agi** (this loop), **caveman** (compressed communication, ~75% fewer tokens),
**cavekit** (kits → build sites → tiered task graphs, with its own peer-review
and convergence machinery), and **gitnexus** (a real code index with symbols,
call graph and execution flows).

Each holds a piece this loop needs. Caveman is directly the design ethic —
motion is expensive, so compress it — and belongs in kid briefs, not just in
chat. Cavekit's build-site → task decomposition is *already* wired in, via
`snapshot-build-site.py`, and its tier/dependency model is close to what G6.4
needs for build-node branching. GitNexus is the natural seed for zoom levels 4–5
where agi has no data at all.

Take pieces; do not merge wholesale. The failure to avoid is four overlapping
vocabularies for one idea — this project has already shown what happens when two
documents describe the same defects (H3b). Absorbs **H8** (SKILL.md propagation),
which should be done as part of deciding the boundary rather than before it.

**Known constraint, measured:** GitNexus excludes any directory named `bin/`, so
it currently indexes zero symbols for all fifteen engine entry points. See
**S1** — that is the same problem from the other end.