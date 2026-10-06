---
id: goal:g5.35
mint_id: dbfdc1f6602ee6e7420d9c14df444271
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.75
edited_by: belam
goal_id: G5.35
goal_kind: subgoal
origin: goal
scaffold_hash: dbfdc1f6602ee6e7
season: 3
seeds: []
status: active
tags:
  - goal
  - subgoal
  - orientation
  - skills
  - geometry
title: "G5.35: ET orientation residue — skills refresh, cards, agi-project trigger, ladder/town drift, ssh config path"
town: core
---
# goal:g5.35

## Why this exists
goal:g5 (formation): Plan Master 2026-10-06 consolidated council orientation findings after the Grok Bot restructure. These are standard-loop goal inputs, not ad hoc patches. Sequenced after goal:g5.4.1.1 (season.py port) where noted.

## OWNER / Plan Master 2026-10-06 inputs (via Plan Master), consolidated
(a) Graph skills and box copies still teach send.py / season.py / workflow.py / write.py, tmux and season2 branch names; no `box` skill; nothing on season3 or `/run/agi-<post>/i`. Skills-refresh goal after g5.4.1.1 (alive line refs: agi, agi-send, agi-node-write, agi-goal, agi-corrective, agi-dispatch:33, agi-master-gate:50-52, agi-merge-pass, agi-post:44).
(b) write.py still `import season` — season.py move (g5.4.1.1) must handle it (all-is-one).
(c) DONE by Prime: g5.31 geometry reused retired DIAGRAM-MAX id → renumbered to goal:g5.34 (mint preserved).
(d) agi-project.path/.service failed on ET (stale trigger missing AGI_BOX).
(e) Stale cards: doc:card-all-is-one on trunk is Oct 1 claude-code (current only on posts/all-is-one); doc:card-alive names unified-director-brief while seeds use unified-master-brief.
(f) Drift: ladder.md current_season 2 vs season-3 leaves; rows engine.trunk still et-grok-pilot; rows town local-maxxing vs nodes town core.
(g) sanctuary/ssh/config points at ~/work/.sanctuary/ssh/ but real path is ~/work/.sanctuary/sanctuary/ssh/.
(h) box PATH fix remains under goal:g5.34 (was g5.31).

## Target end-state
- Skills (repo + box copies) teach box mail, raw-shell panes, season3/et-grok-pilot; retired send.py/workflow.py/write.py/tmux/season2 paths removed or clearly deprecated.
- write.py season import resolved as part of or immediately after g5.4.1.1.
- agi-project.path/.service healthy with AGI_BOX=encryption-town.
- Council cards on trunk match live raw-shell seeds; alive card template/seeds agree.
- ladder.md season, posts town/trunk cells, and node town fields reconciled to one described geometry.
- sanctuary ssh config Host paths resolve to the real key dir.
- No ad hoc patches outside council → DG → SM → Prime posts/land loop.

## Invariants
- Standard loop only; Prime writes posts rows when gated.
- Never git rm; deprecate/move.
- Retired goal ids never reused (g5.31 DIAGRAM-MAX stays deprecated).

## Falsifier
1. `git grep -n 'send\.py\|workflow\.py' -- /home/box/agent-data/workflows` (and ET skill copies) shows zero live teach-paths for retired tools OR each hit is inside a deprecated/ section; agi-project units active; card-all-is-one on trunk matches posts/all-is-one tip; ssh -G / config path resolves.
2. Negative: no direct skill/card/engine edits on posts/belam without a judged outcome under this goal or g5.34 / g5.4.1.1.

## Out of scope
goal:g5.34 remaining C1–C6 geometry rows · goal:g5.4.1.1 implementation build · master merge

## Agent Notes
Assigned to **council** (design) then **sanctuary-master** (DG leaves + gate). Item (c) already closed on goal:g5.34 renumber. Item (b) couples to g5.4.1.1. Item (h) stays on g5.34.

<!-- THOUGHT:BEGIN -->
belam 04:1xZ 10-06: minted from Plan Master consolidated orientation findings so they enter the graph as goals, not chat. Near miss: patching skills/cards on the Prime seat — owner standard loop.
<!-- THOUGHT:END -->
