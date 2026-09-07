---
id: goal:g1.4
mint_id: adc82c05ab6a4b3d89c78179571b3f2b
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.4: Kids get the graph and nothing else"
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

**Live evidence for stage 2, 2026-08-31.** A pi kid with an unrestricted shell
ran `git commit -A` and swept a second kid's half-written node and a human's
uncommitted engine edits into one commit labelled with its own node id
(`d34048aa1`, left in place as the record). Nothing was lost; the history now
says something untrue. The kid was not misbehaving — its contract said how to
signal completion and nothing about git, so committing read as part of
finishing. Both contracts now forbid git in words.

**Words are stage 1, and this is exactly the case that shows their ceiling.**
A wording fix depends on every future kid reading and obeying a prohibition; an
allowlist makes the call unavailable. Note also what the failure was *not*: it
was not a node written badly, it was a **raw write to a path the graph does not
own** — the general shape stage 2 removes. The narrower reading is worth
holding onto: the dangerous surface is not "tools" in the abstract, it is
uncontrolled write paths, of which a kid's shell is the widest.

**This does not license skipping the gate.** The observation is that a shell
lets a kid do damage, not that kids need the graph less than they thought — no
kid this session reached for a file the graph could not answer. Stage 1's
measurement is still what derives the allowlist.

**The gate between the stages, stated so it cannot be skipped:** if stage 1 shows
kids reaching for files the graph genuinely cannot answer, that is a **G1.1 gap,
not a discipline problem**. Clamping the tools first would convert a missing
navigation feature into a silent kid failure, and the loop would report fewer
tool calls while producing worse nodes — the metric improving as the work gets
worse. Fix the graph, then clamp.

Falsifier: non-graph tool calls per kid trend to zero in stage 1 *without* node
quality dropping. If quality drops, the graph is not yet carrying what it claims
and stage 2 must not ship.