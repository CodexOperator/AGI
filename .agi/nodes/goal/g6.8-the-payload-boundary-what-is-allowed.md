---
id: goal:g6.8
mint_id: c0267a5787834c2189726d34a0966993
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.8
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - mvp:census-boundary-scope
  - mvp:level3-boundary-scope
  - mvp:payload-boundary-predicate
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.8: The payload boundary: what is allowed to be a node"
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

## Open boundary question, raised 2026-08-27: experiment output that became nodes

The rule above puts **docs and prose in** and **ephemeral output out**. 38
build nodes wrap a `.md` payload, and those two clauses disagree about 16 of
them.

`context/refs/zoom-roundtrip-ground-truth/**` is one experiment's raw output —
`trial-1/children.md`, `trial-1/reconstruction.md` and siblings, three trials
across two subjects, plus four summary files. By the filesystem test it is
**in** (it is a file in the repo). By "sessions, run logs, and ephemeral
output likewise -- they are evidence a node can *cite*; they are not
thoughts" it is **out**. That is exactly the case this goal's falsifier says
must not need a human to adjudicate:

> Falsifier: name any file in the engine repo and get a yes/no from this rule
> without argument. If a case needs a human to adjudicate, the boundary is not
> yet a boundary.

**So the falsifier has fired.** The remaining 22 `.md` nodes are unambiguous
and stay: `TODO.md`, `HANDOFF.md`, `README.md`, `SKILL.md`, `agent-prompt.md`,
the kits and the build-site plan are all prose that steers agents, which this
goal puts in with a direction attached.

Two things worth recording for whoever closes this:

- **Retiring such a node is not a node operation.** `bin/level3.py` discovers
  from `git ls-files` on the engine plus a payload rglob, so a deprecated node
  whose file still exists is simply re-minted on the next scan. Any decision
  here needs a scan-scope change in the engine, published through the grid.
- **The context-bloat argument for retiring them does not hold.**
  `context/INJECTION.md` is 15 KB / 256 lines and never enumerates build
  nodes — it carries per-type counts and a handful of `spawns->` references.
  Removing 38 nodes would not measurably change what an agent loads.

Suggested resolution, not yet taken: sharpen the test from "exists as a file"
to "exists as a file **and** is authored rather than emitted". That keeps
every prose doc in and puts trial output out, without a judgement call.

## 🔴 The premise this goal rests on is currently false — see G2.10

The argument above for admitting code and prose is **bidirectionality**:

> A code node ties cleanly to thought: it can spawn a hypothesis about itself,
> an experiment against itself, or just an idea. That bidirectionality is what
> makes it worth being a node rather than a record.

Measured 2026-08-27: **half of that does not hold.** `bin/level3.py`
regenerates a build node's entire body on every run, so a build node can be
*cited* by a thought and cannot *contain* one. Probed both ways — prose added
to a body is wiped by the next scan, and a filled-in `why: TODO(model)` is
wiped too. The corpus confirms it: **8,034 `why`/`perf`/`security` fields
across 190 build nodes, 8,034 still `TODO(model)`, 0 ever filled.**

So today a build node **is** the "record" this goal says it is more than. The
boundary drawn here is still the right boundary; what is missing is the
property that justified drawing it there. **G2.10 owns the fix**, and until it
lands, every argument on this page about build nodes holding thought should be
read as intent rather than description.

This also settles the `@v2` question in the other direction from the obvious
one. The five `origin: build-version` nodes look like exactly the redundancy
CLAUDE.md forbids ("a version is a grid commit, not a second node file"). They
are not: they carry 7k-13k characters of real reasoning each and survive
**only** because `level3.py` does not own their origin. Their payloads are
byte-identical to the engine, so collapsing them loses no bytes — and ~47,000
characters of prose, with nowhere to put it. Fix G2.10 first, migrate the
bodies, then retire the convention.
