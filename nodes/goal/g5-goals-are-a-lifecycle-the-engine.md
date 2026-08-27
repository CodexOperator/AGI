---
confidence: 1.0
goal_id: G5
goal_kind: long-term
heading_level: 2
id: "goal:g5"
mint_id: 71c02192f832480f85cb075ad649a451
order: 25
origin: goals-doc
seeds:
  - exp:g5-lifecycle-enforcement
  - goal:g5.1
  - idea:engine-schema-registry
  - idea:engine-snapshot-build-site
  - idea:engine-snapshot-goals
  - mvp:strict-goal-refs
status: active
tags:
  - goal
  - root
title: "G5: Goals are a lifecycle the engine reads, not a human convention"
type: goal
---

`status:` should be a field the engine acts on: stop accruing score to
`phasing-out` and `complete` goals while keeping their chains attributable, and
fail loudly when a seed node points at a goal id that does not exist.

**Invariant:** a project is legitimate at three depths — goals only (ideation),
goals + seed ideas (chains starting), goals + build site (execution). A
goals-only project is a valid state, not a broken one.

Banked: **L15** — goals are first-class nodes, derived from this file, linked by
parent-pointing, with referential integrity live and an H0-safe origin-guarded
prune. A missing `GOALS.md` prunes nothing.

Owns: **L5** (rotation the engine enforces), **L18** (the ideation stage; a
missing build site must degrade like a missing `GOALS.md` does, not abort the
driver).

**Landed 2026-08-23** (`exp:g5-lifecycle-enforcement`, `mvp:strict-goal-refs`):
retired goals stop scoring while staying attributable; **L5** rotation warns
every iteration (`METRIC_WARNING goal_rotation=`, currently reading 37/3);
**L18** a goals-only project runs instead of aborting; and `--strict-goals`
makes a dangling goal reference fail the run, wired into `driver.sh` while the
count is still 0 — which is when to start enforcing, not after the first one.
