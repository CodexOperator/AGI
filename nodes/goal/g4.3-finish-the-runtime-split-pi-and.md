---
confidence: 1.0
goal_id: G4.3
goal_kind: subgoal
heading_level: 3
id: "goal:g4.3"
mint_id: 486acf4bc70c403aa16c9d1efdcb8107
order: 22
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G4.3: Finish the runtime split: pi and Claude Code as one path"
type: goal
---

**L12** remainder plus **H9**. Anywhere the engine invokes `pi`, allow invoking
Claude Code instead — a runtime flag, not a parallel code path — and audit hook
parity between the two. H9's kid→parent question channel exists for the CC path
(four escalation triggers, one question per kid) and not for pi.

**H4b** belongs here too: `driver.sh` calls `benchmark.py` with the wrong
arguments under `|| true`, so it may never have run. That matters beyond the
bug — `benchmark.py` is what reaches `ranking.py` and the weighted attractiveness
path, which means the ranking this loop supposedly selects targets with has
never been confirmed to execute at all.
