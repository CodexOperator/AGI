---
confidence: 1.0
goal_id: G10
goal_kind: long-term
id: "goal:g10"
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
title: "G10: The hypergraph: an environment, not a document"
type: goal
---

**The end state this whole system is walking toward.** Not "a graph the agent can
query" — a *place the agent is in*. There are no blocks of prose anywhere in the
working context; everything an agent sees is graph, rendered. The agent receives
an injection of the hypergraph at the resolution its director chose, moves through
it, and asks for more of it. Every other goal here is a component of this one.

**The reason, and it is the load-bearing claim of the project:** memories are weak
things. A memory is a lossy re-encoding made after the fact, and every layer of
memory machinery bolted onto an LLM harness is an attempt to compensate for having
thrown the original away. The graph does not remember — **it keeps the original
thought verbatim, as it occurred, and lets a later agent connect to it directly.**
That is why this system has no memory layer and should never grow one. Nothing
here needs to *recall*; it needs to *reach*.

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
`exp:evidence-gate-coverage`. If agents still
