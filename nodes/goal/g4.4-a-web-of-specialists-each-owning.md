---
confidence: 1.0
goal_id: G4.4
goal_kind: subgoal
id: "goal:g4.4"
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G4.4: A web of specialists, each owning a region"
type: goal
---

**Where the model-tiering goes once the dial exists.** G4.2 gives per-tier effort;
this is what to do with it. The target shape: many small, hyper-specialised models
each owning a **region of a zoom level** of the hypergraph, a smaller number of
capable parents reviewing across regions, and a very small number of directors
holding intent. Specialisation is by *territory*, not by task type — an agent that
only ever works one region accumulates a sharper prior about it than a generalist
re-reading it cold every time.

**The objective function, stated plainly because it is the actual constraint:
functional output per token spent.** Not quality alone and not cost alone — the
ratio. A director on the largest model is worth its cost only if it multiplies
what the tiers below produce.

**Fine-tuning is the horizon, and it has a dependency the rest of this list
doesn't:** a specialist tuned on a region needs that region to be stable enough to
be worth learning. That argues for doing **G10** and **G6.8** first — you cannot
tune a model on a territory whose shape and contents are still being decided.

**Honest near-term constraint, recorded so the plan is not built on it.** Local
inference on a 16 GB machine does not produce a peer to the parents; it produces a
*mechanical* worker. That is not a disappointment, it is the split this system
already believes in — the harness derives mechanically, the model fills judgement
(**G2.2**). The jobs a local model can genuinely take off the paid tiers are the
mechanical half: frontmatter assembly and validation, census and counting, LOD
compaction (**G10**), draft node scaffolding for a parent to review. Every one of
those is currently done by a paid model or a bespoke script.

What it cannot do is act as an autocomplete in front of a larger model — there is
no cross-provider speculative decoding, and any "check my draft" arrangement pays
the full input cost of the draft anyway. The saving comes from work the local model
**completes**, never from work it merely starts.

Depends on **G4.2** (the dial), **G4.1** (parallel kids must stop colliding before
there are many more of them), and **G10** for stable territory.
