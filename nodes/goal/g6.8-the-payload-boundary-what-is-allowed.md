---
confidence: 1.0
goal_id: G6.8
goal_kind: subgoal
id: "goal:g6.8"
origin: goals-doc
parents:
  - goal:g6
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G6.8: The payload boundary: what is allowed to be a node"
type: goal
---

**G6.6 said "cover the non-code surfaces" without saying where coverage stops.
This draws the line, so the answer is a rule rather than a judgement call each
time.**

**In — anything that exists as a file in the repo.** That is the whole test, and
it is deliberately mechanical:

- **Code.** Already in. A code node ties cleanly to thought: it can spawn a
  hypothesis about itself, an experiment against itself, or just an idea. That
  bidirectionality is what makes it worth being a node rather than a record.
- **Docs and prose, including the skill docs.** In, for exactly the same reason —
  they spawn the same children, and most of what they assert is measurable
  against the metrics already collected. `SKILL.md` and `agent-prompt.md` are the
  highest-leverage files in the engine and are the reason **G6.6** exists.
- **Philosophy and instruction prose specifically.** In, and with a direction
  attached: **it belongs in the `agi` repo, arriving there from a node in
  `agi-tree`.** Not written into the engine and described afterwards. This is
  **G6.1**'s arrow applied to the documents that steer every agent — the class of
  file where a change made without a node behind it does the most damage, as
  **S8**'s three-way contradiction demonstrates.

**Out — anything with no file behind it.** Today that means, concretely:

- **Git refs are not nodes.** A node per grid ref is tedious to no purpose:
  `refs/grid/node/<id>` is already *about* a node that exists. Making it its own
  node inverts the relationship and doubles the corpus for zero new thought.
- Sessions, run logs, and ephemeral output likewise. They are evidence a node can
  *cite*; they are not thoughts.

### The shape this implies, and it is worth stating because it is the whole model

Two dimensions, not one. **The graph is the lateral dimension** — nodes and their
edges, which can be flattened for reading or left as a 3-D structure of filaments.
**Each node then carries its own linear stack of versions** as it is updated, and
that stack is the grid. Refs are the *geometry* of that second dimension, not
content within the first. That is precisely why they do not need nodes: they are
the axis, not points on it.

**The immediate payoff, and it is concrete: the 104 demoted verdicts can be
resurrected.** They were demoted rather than deleted, so each still holds its
original body at `v1`. Under this model, bringing one back to a decisive verdict
is not an edit and not a rewrite — it is **minting a `v2` that meets the current
standard**, with `v1` preserved as what was actually claimed at the time. The
overclaim stays visible as history; the honest version is what the graph serves.
That is the version dimension doing real work on real content for the first time,
which is exactly what **G6.3** says has never been tested.

**Scope note, so this does not read as permanent:** this boundary is *today's*
line and it is drawn at the filesystem for tractability, not principle. **G10**
holds the horizon where git refs, sessions and history all become addressable
regions of the same hypergraph. When that lands, this goal narrows rather than
being contradicted — the rule becomes "everything is in, materialised on demand"
and the filesystem test retires.

Falsifier: name any file in the engine repo and get a yes/no from this rule
without argument. If a case needs a human to adjudicate, the boundary is not yet
a boundary.
