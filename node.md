---
id: goal:g7
mint_id: d020b2d79cb545edb5c23fb2d63c7d54
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G7
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g7.1
  - goal:g7.10
  - goal:g7.2
  - goal:g7.3
  - goal:g7.4
  - goal:g7.5
  - goal:g7.6
  - goal:g7.7
  - goal:g7.8
  - goal:g7.9
  - idea:engine-graph-core
  - idea:engine-grid
  - idea:engine-migrate-to-sqlite
status: active
tags:
  - goal
  - root
thought_session: season
title: "G7: Nothing the loop produces is ever silently lost"
---
The graph is what makes it safe to stop mid-sprint, which only holds if stopping
cannot lose work and no artefact can quietly disappear or quietly lie.

**Invariants:**
- **Node count never drops** across a snapshot.
- The engine is never vendored into a project. It arrives as a gitignored clone
  that can be pulled; a committed copy diverges forever.
- No project-local `bin/*.py` shadowing an engine script. Treat any that exists
  as stale until proven otherwise.
- A partial answer is never served as a complete one.

Paid for in full: stale project-local `snapshot-build-site.py` silently wiped
29,264 files (**H0**); a second stale override broke the render path (**H0b**);
`find_chains` did not terminate on this corpus (**H0c**); a truncated
`find_chains` result was cached and re-served silently forever (**H0e**).
Banked on the other side: the git grid — per-node and per-session refs, cron
sync at a ≤5-minute crash window, rejected drafts survive (**H10**).

Owns: **L9**'s unpinned-clone gap (record the expected engine commit in config;
warn, never fail, on drift — it closes the whole staleness class), **H1**/**H2**
(state into the DB), **L16** (close the config-name compatibility window only
once pinning exists — it is load-bearing until then).