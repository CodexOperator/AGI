---
id: goal:g6
mint_id: ee284312e59e4ee6bccb0a994ae0bc6b
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G6
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g6.1
  - goal:g6.2
  - goal:g6.3
  - goal:g6.4
  - goal:g6.5
  - goal:g6.6
  - goal:g6.7
  - goal:g6.8
  - goal:g6.9
  - idea:deprecate-the-gamed-mass
  - idea:engine-self-decomposition
status: horizon
tags:
  - goal
  - root
thought_session: season
title: "G6: The closed loop: engine work starts in the graph"
---
Run `agi` and `agi-tree` against each other and the pair is closed: a change to
the engine originates as a node in this graph, and the engine that grows this
graph is the thing the node changed. Neither is the author of the other — the
graph is the sequence, the engine is the machinery that reads it.

Today the loop is open. Engine reasoning lives in `TODO.md` and `CLAUDE.md` as
prose, gets read by agents, and never returns to the graph.

**Invariants:**
- An engine change is reviewable as **node → verdict → commit**.
- The decomposition is **generated, never hand-written** — a hand-authored map
  goes stale exactly the way `domain-exporters` did.
- Deprecate superseded mass; **never delete it.** Retired nodes remain prior art
  and remain evidence.

Known state of this graph: the idea layer already decomposes an *older* engine —
`domain-exporters` and `domain-environment-indexers` describe modules that no
longer exist, and there is no idea node at all for `src/agi_algos`, the twelve
`bin/*.py`, `driver.sh`, `hooks/`, `lib/`, `scripts/`, or `extensions/agi-bridge/`.
The half of the engine that actually changes is the half with no representation.
Below the idea layer it is not a decomposition of anything: ~14.5k experiments
and ~14.6k verdicts against 14 ideas is the H3 gaming artifact, not thought.

Owns: **L19**. Preconditions cleared 2026-08-21: H3 config migration (this
project), this file, and H0e (truncated chain results no longer cached as
complete).