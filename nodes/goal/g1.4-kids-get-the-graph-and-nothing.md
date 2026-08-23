---
confidence: 1.0
goal_id: G1.4
goal_kind: subgoal
id: "goal:g1.4"
origin: goals-doc
parents:
  - goal:g1
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G1.4: Kids get the graph and nothing else"
type: goal
---

**A kid should not be able to spend motion on anything but the graph.** Weight
is the reason: everything a kid reads rides along in its context for the rest of
the run, and most of what it reads is context the graph already holds — this is
G1.1's finding stated as a permission rather than a capability. A kid that
*cannot* open a source file cannot re-derive what it was already handed.

The parent is exempt. It reviews, judges and commits; that is filesystem work by
definition. This is a constraint on kids only.

**Staged on purpose, and the order is not negotiable.**

1. **Now — say it and measure it.** The kid brief states graph-only, and
   `dispatch.py` logs every tool call a kid makes. A metric counts non-graph
   calls per kid per iteration. Kids can still escape when genuinely stuck, and
   *that escape is the measurement* — it says exactly which question the graph
   could not answer.
2. **Then — the allowlist.** Kids spawn with graph tools only; no `Read`,
   `Grep`, `Glob`, `Bash`. The allowlist is derived from what stage 1 observed,
   not guessed in advance.

**The gate between the stages, stated so it cannot be skipped:** if stage 1 shows
kids reaching for files the graph genuinely cannot answer, that is a **G1.1 gap,
not a discipline problem**. Clamping the tools first would convert a missing
navigation feature into a silent kid failure, and the loop would report fewer
tool calls while producing worse nodes — the metric improving as the work gets
worse. Fix the graph, then clamp.

Falsifier: non-graph tool calls per kid trend to zero in stage 1 *without* node
quality dropping. If quality drops, the graph is not yet carrying what it claims
and stage 2 must not ship.
