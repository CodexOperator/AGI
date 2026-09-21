---
id: goal:g9.1
mint_id: 58362ff3322b4537ac059a9791017ab6
type: goal
parents:
  - goal:g9
confidence: 1.0
edited_by: season.py
goal_id: G9.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - exp:dashboard-cli-r1
  - idea:engine-dashboard
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G9.1: CLI dashboard, runnable as a Claude Code side terminal"
---
First deliverable, and deliberately the humble one. A terminal view that
answers, without the reader knowing any of this system's vocabulary:

- what goals exist, their status, and what is actually being worked
- which chains are real and which are stubs
- where every metric currently stands, **with its known contamination named**
- what the loop did last iteration, and what it would pick next

Runs in a repeating-refresh mode so it can sit in a split terminal beside a
Claude Code session. No install step beyond the engine itself.