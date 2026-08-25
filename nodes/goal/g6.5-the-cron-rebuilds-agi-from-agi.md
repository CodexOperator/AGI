---
confidence: 1.0
goal_id: G6.5
goal_kind: subgoal
id: "goal:g6.5"
mint_id: 1144ba54807845f2b7dfa655e7f47571
origin: goals-doc
parents:
  - goal:g6
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G6.5: The cron rebuilds agi from agi-tree, then commits and pushes it"
type: goal
---

**The shape being committed to: `agi-tree` is the development environment,
`agi` is the shippable package.** Work happens in the graph; the engine repo is
what falls out of it. When the grid cron runs it should re-derive the census,
re-scan level 3, `stitch` the result into the engine tree, and — once that is
trustworthy — **commit and push the engine repo too**, so `agi` is always a
published build of `agi-tree` rather than a thing edited in parallel.

**Answering the question directly: today the two repos' commits are NOT the
same work, and that is the defect.** This session's engine changes were edited
directly in `agi`, and the level-3 nodes merely *describe* the result through
`payload_ref`. The graph trails the code. G6.3 reverses the arrow (a fix lands
as a build-node version), G6.4 gives it provenance (a non-build chain produces
the next version), and only then is an automatic rebuild-and-push safe — at
that point the engine commit is a *derivation*, and its message can cite the
node and verdict that caused it.

**Sequencing, and it is not negotiable:**
1. **Now — verify only.** Cron runs the generators and `stitch --verify`, and
   reports drift. It writes nothing to the engine.
2. **After G6.3** — cron may stitch and commit the engine.
3. **After G6.4** — the engine commit message carries the node → verdict →
   version chain that produced it.

A cron that writes the engine from the graph before the version layer is
trusted is a data-loss defect waiting to happen, and this project has already
paid for that class twice (H0, H0b). Report drift; never silently reconcile it.

**The generality worth preserving:** `agi` already has the tooling to run
against *any* project, including itself. Pointing it at itself is what makes
this loop closed; pointing it at fantasia is what makes it a product. Neither
should require a different engine — see **G8.2**.

Pairs with **S2** (done) and **S5** (the engine repo has no sync at all yet).
