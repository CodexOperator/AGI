---
confidence: 1.0
goal_id: G5
goal_kind: long-term
id: "goal:g5"
origin: goals-doc
seeds:
  - exp:g5-lifecycle-enforcement
  - idea:engine-schema-registry
  - idea:engine-snapshot-build-site
  - idea:engine-snapshot-goals
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
