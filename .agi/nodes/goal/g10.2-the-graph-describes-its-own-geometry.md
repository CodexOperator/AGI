---
id: goal:g10.2
mint_id: 4b27be7298144a7e801b6e63ce5a5ae0
type: goal
parents:
  - goal:g10
confidence: 1.0
edited_by: season.py
goal_id: G10.2
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
title: "G10.2: The graph describes its own geometry"
---
**A `nodes/.geometry/` directory holding a handful of nodes that describe the
shape of the graph itself** — what the axes are, what a version is, what a chat
attaches to, how zoom and LOD compose. Not documentation *about* the system in
prose somewhere: nodes, in the graph, subject to every rule other nodes obey.

The point is the loop closing on itself. Today those rules live in engine code
and in this file. Put them in `.geometry/` and **the rules become modifiable
through the graph**, which is the same arrow **G6.1** draws for engine code,
applied to the engine's own model of itself. The init script (**G1.5**) ships
the starting geometry; a project that needs a different shape edits nodes rather
than forking the engine.

Constraint that keeps this honest: a geometry node must be *read by something*.
A `.geometry/` directory the engine does not consult is prose with a
directory name — the exact failure **G6.6** found in `agent-prompt.md`. Ship a
geometry node only when a real code path reads it.

### The two axes are orthogonal, and conflating them is the current defect

- **Zoom** — which region of the graph, and at what structural grain. Already
  numeric 1–5 (**G2**). This is *where you are*.
- **Level of detail (LOD)** — how much of each node is printed at that grain. Does
  not exist yet. This is *how hard you are looking*.

Today they are fused: a node's grain is baked into its type (`level3:`) and there
is one rendering per node. The target is that any node at any zoom can be pulled
to full LOD — its complete contents, expanded — while its neighbours stay compact.
Pick a node or a small set, raise their LOD, read; pick another set, push it a zoom
level in or out. **Like slides you click through, with one-word commands, orienting
in seconds rather than in tool calls** (see **G1.6**).

The rendered artefact is a long tapestry of expanded ASCII nodes, sized so the
whole selection lands cleanly in token space. Compaction is an LOD setting, not a
separate renderer.

### Zoom must not name itself

**A node must not be titled `level3`.** The zoom level is a property of the *view*,
never of the node. The environment injection says "you are at zoom 3"; the nodes
say what they are.

The reasoning is specific and it is the sharpest thing in this goal: zoom exists,
for a human, to produce **tunnel vision** — block out everything but the relevant.
An LLM has no tunnel vision. It only has peripheral vision; it sees the whole
context at once. So for an agent, zooming is **not** occlusion — it is a slight
reduction in dimensionality. Designing the zoom axis as though the agent needs
blinders imports a constraint from the wrong nervous system. Naming the level on
the node is that mistake made concrete: it tells the agent to identify with a
grain instead of simply working at one.

Consequence for **G2.1**/**G6.6**: `level3:` as an id prefix is a migration
artefact, and the type should become a *facet* the renderer reads, not a name the
node wears. Do not rename anything yet — ids are permanent (that rule holds) — but
stop minting the grain into new ids.

### Eventually: everything loads in

**G6.8** draws today's payload boundary at the filesystem, and git refs sit outside
it on purpose. That is the *current* line, not the final one. The horizon is that
git refs, sessions, and run history all become addressable regions of the same
hypergraph, materialised on demand as an agent asks for more touch of its
environment — not pre-loaded, not a second system, just further out in the same
space. **The supermap convention (G1.3) is the addressing scheme that makes this
possible**, which is why G1.3 is worth building before the thing it will address
exists.

Falsifier, and it has to be behavioural rather than aesthetic: give an agent a task
that today requires leaving the graph, and measure the graph-call to file-read
ratio (the Design Ethic's measurable). The hypergraph is real when that ratio
inverts on work that currently fails it — the standing baseline is 3:28 from
`exp:evidence-gate-coverage`. If agents still reach for the filesystem, the
environment is a document with better formatting.

Depends on: **G2** (zoom axis), **G1.3** (addressing), **G9.4** (the viewport is
the same query with a human front-end), **G6.8** (what is in it at all).