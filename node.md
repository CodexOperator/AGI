---
id: goal:g8.2
mint_id: 5df2daa9211c410b82909da5c031be6c
type: goal
parents:
  - goal:g8
confidence: 1.0
edited_by: season.py
goal_id: G8.2
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - build:lib-find-root.sh@v2
  - build:skills-agi-SKILL.md@v2
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G8.2: One engine, any project, including itself"
---
**The engine must never need to know which project it is running.** It already
mostly holds: `driver.sh` walks up for a config file, the goal and build-site
snapshots are project-agnostic, and the same binary ran against fantasia (a
game) and agi-tree (an engine graph) this session without modification.

What is newly true and worth protecting: **agi can be pointed at itself.** The
census, the level-3 scan and `stitch` all ran against the engine's own source
this session, which is what makes G6 a closed loop rather than a slogan. That
self-application must stay a *normal use of the general tool*, never a special
mode — the moment there is an `if project == "agi-tree"` branch anywhere, the
generality that makes G8 possible is gone.

Falsifier, and it is cheap to run: a third project — neither fantasia nor
agi-tree — should reach a rendered map and a first chain with no engine change
at all. L18 already proved the goals-only stage works on a bare project; this
extends it through a full iteration.