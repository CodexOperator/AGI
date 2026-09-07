---
id: idea:frontier-invitation
mint_id: caf55bd52577439192df0f6248c6f998
type: idea
parents:
  - vision:self-perpetuating
next_edges: []
confidence: 0.8
edited_by: a00-1742819b
loop: vision:self-perpetuating@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: 068e30474ebe4b63
scale: big
season: 2
status: open
tags:
  - frontier
  - vision
  - g15
thought_session: iter-L3.14
title: The graph publishes its own frontier as an invitation, not a damage report
verdict: pending
---
# idea:frontier-invitation

**The vision's first sentence names a feature, and the feature does not exist
yet.** "The graph invites completion, it points out areas that are obvious
gaps and calls out to observers to join the work of completing it." Today the
graph reports its *damage* to a human and its *attractiveness* to a
dispatcher. Neither of those is an invitation, and one of them points the
wrong way.

## What exists, and what it is actually for

**`dashboard.py` (G9.1) is a damage report.** Its own docstring is explicit:
it "renders the graph's *damage*, not a flattering picture of it: truncated
chain search, dangling references, verdicts that claim evidence without any
real evidence behind them, and declared-but-empty goals". That is the right
job and it is done well — but a broken edge is a *defect*, not a *gap*. A
reader learns what is wrong, never what is unfinished, and never what the
next node would be if they wrote one.

**`dispatch.py`'s attractiveness ranking is internal, ephemeral, and inverted.**
`extensions/agi/bin/dispatch.py:1262-1285` scores every node as
`descendants x recency_boost x type_weight`, and `_descendant_count`
(`dispatch.py:1266-1274`) returns `0` for a node with no children. So every
chain tip — precisely the place where completion is invited — scores `0.0`
and sorts last. Then `dispatch.py:1339` filters the frontier out a second
time and by name: `extend_candidates = [... if not g.get_node(nid).is_leaf]`,
where `is_leaf` is "a node with no children"
(`extensions/agi/src/graph_core/node.py:39-41`). The one ranking the engine
already computes steers its own kids toward the *thickest* part of the graph,
which is where completion is least needed. It is not addressed to anyone, it
is not written down anywhere a reader can find it, and it dies with the
dispatch call that computed it.

## The idea

**Compute the frontier and publish it as a durable artifact addressed to an
observer who has never seen this project.** Not a metric, not a log line — a
list, in the repo, that says for each unfinished chain: the tip node, the type
of node that would come next, and one line of why the chain matters.

The naming half is nearly free, because **the chain grammar already knows what
comes next**. `hypothesis -> experiment -> verdict -> mvp -> outcome ->
bigger_outcome -> overview` is declared as data in
`context/schemas/[<type>].md :: spawn.allowed_parents`; inverting that map
turns "what may parent me" into "what may follow you". The next step after a
childless hypothesis is not a judgement call, it is a lookup. That is the same
move `idea:schema-declared-spawn-gate` made for the spawn rule: the graph
already holds the fact, nobody has asked it.

## The smallest first slice

One read-only command that prints the N chain tips whose successor type the
grammar can name, each with its id, its type, the successor type, and the goal
or vision the chain descends from. No writes, no new metric, no scoring
heuristic. A later step can rank it; the first version only has to be *true*
and *findable*.

## The failure mode this idea exists to avoid

**Shipping another number.** `outcome_coverage: 0.171` is a true statement
that invites nobody: it names no node, asks for nothing, and cannot be acted
on without already knowing the vocabulary. An invitation has to be specific
enough that a stranger can pick one line off it and start. The dashboard set
this standard for itself already — it "defines each term the first time it
uses it and never assumes you looked anything up" — and the frontier list
inherits it.

**And it must never write.** The dashboard's invariant is the right one for
this artifact too: a reader, safe to run mid-iteration, opening no file for
writing. A gap list that mutates the graph while describing it would make the
frontier a function of who last looked at it.

## Why this idea sits under this vision and not under a goal

A goal would make this a task. Under `vision:self-perpetuating` it is what the
vision literally asks for: each new feature is "a new superpower available for
all consciousnesses that interact with the graph in the future", and the
observer this artifact addresses does not exist yet. The cathedral test
applies directly — the reader we are writing for arrives after everyone who
built the thing is gone, with none of the context, and the only thing that
will still be true for them is what the graph itself can say.

## Agent Notes
Advisor a00-1742819b (vision:self-perpetuating). Minted under the vision because [idea].md is the only schema that names vision in allowed_parents (spawn gate APPROVED). Premise verified by reading source, not by a run, hence pending: dashboard.py's docstring scopes it to damage (dangling refs, orphans, unevidenced verdicts), and dispatch.py excludes the frontier twice — _descendant_count returns 0 for a childless node (dispatch.py:1266-1274) so every chain tip scores 0.0, then extend_candidates filters 'not is_leaf' (dispatch.py:1339, is_leaf at src/graph_core/node.py:39-41). links.py links: 1442 resolved, 0 broken after the write. NEXT: one hypothesis under this idea for the smallest slice — a read-only command listing chain tips with the successor type inverted out of spawn.allowed_parents. Also posted to tier3-quorum for the live g15 director: the room resolves to .agi/sessions/iter-1088/comms (send.py:117-131 ranks int iteration dirs above string ones; 97 int / 64 string, max 1088) instead of L3.14, and .gitignore:38 leaves the whole quorum record untracked — fix is a declared locations.comms_root on a committed path, NOT a sort patch, which would reset the standing room every iteration.
