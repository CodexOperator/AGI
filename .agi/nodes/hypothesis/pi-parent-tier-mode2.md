---
id: hypothesis:pi-parent-tier-mode2
mint_id: 4ae522af783740e5ab495720b5992e25
type: hypothesis
parents:
  - goal:g4.3
next_edges:
  - experiment:a00-763e629b-5c04ad
confidence: 0.5
edited_by: season.py
evidence_runs: 0
season: 1
thought_session: season
title: Pi parent tier mode2
verdict: pending
---
# hypothesis:pi-parent-tier-mode2

## Hypothesis

**Claim.** `goal:g4.3` mode 2 — a parent that owns one loop and spawns its own
kids — can be added to the **pi** runtime as a *tier parameter on the existing
dispatch path*, with no second selection path, no second gate, and no second
brief. Concretely: `dispatch.py` learns `--tier {kid,parent}`; a parent slot is
dispatched by the same code that dispatches a kid slot, differing only in the
model it is given, the brief it is assembled, and the fact that its brief tells
it to invoke `dispatch.py --tier kid --target <id>` itself.

**Why this is not obvious, and why it is the load-bearing claim.** pi has **no
spawn primitive** — its tools are `read, bash, edit, write, grep, find, ls`, so
a pi parent can only spawn a kid by shelling out. That makes the tier boundary
a *process* boundary rather than an API one, and process boundaries are where
this project has historically grown parallel code paths: the CC runtime got its
own completion contract this way (`goal:s8`), and the pi runtime got its own
model handling that read the config and used none of it. The claim is that the
shell-out is an implementation detail of *how a parent spawns*, not a reason
for a parent to have its own dispatcher.

**Proves it.** One `--max-iters 1` run dispatches a single parent slot; that
parent spawns kids sequentially through the same `dispatch.py`; the resulting
kid nodes are indistinguishable in format, gating and wiring from kids
dispatched directly, and `post_wire` closes them with no tier-specific branch.
The falsifier for the shared half specifically: `grep` the gate-invocation path
and find **zero** new branches keyed on tier beyond the single lookup that
chooses model and brief.

**Disproves it.** Any of: the spawn gate, evidence gate, `post_wire` or target
selection needing tier-specific logic; `heal.py` being unable to distinguish a
parent that is legitimately slow (because its kid is running) from a hung one,
so that the timeout has to be tier-aware in a way that is really a second
scheduler; or a parent needing a brief that cannot be assembled from the same
source as a kid's, which would make `goal:g1.9` a prerequisite rather than a
neighbour.

**Scope.** pi only. The CC half of mode 2 is
`hypothesis:a00-652a7e70-1adcde`'s sibling and is deliberately not carried
here — one node, one argument.

**Known constraint this must respect.** Kids are serialized at
`agent_dispatch.claude_max_parallel: 1` while all agents share one working
tree, so a parent spawning kids must spawn them one at a time. Whether that is
a property of the parent's brief or of the dispatcher is itself part of what
the experiment settles; making it a property of the brief alone would mean a
parent that ignores its brief can still collide.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Seeded by the delegator, not a kid, because aiming kids at `goal:g4.3` kept
producing CC-framed work — correctly, since that goal's body opens "Anywhere
the engine invokes `pi`, allow invoking Claude Code instead". The first aimed
kid (`hypothesis:a00-652a7e70-1adcde`) read that faithfully and wrote about the
CC dispatcher's direct-kid mode. Nothing in the graph said "pi gets a parent
tier"; it existed only as prose in HANDOFF §3a item 2, which is exactly the
kind of state that has no node behind it and therefore cannot be aimed at.

Written as a claim about *where the tier boundary goes* rather than as a task,
because the interesting question is not whether a parent can be made to spawn
kids — it obviously can, via bash — but whether doing so is a flag or a fork.
g4.3's own invariant already answers what counts as failure, so the falsifier
is stated as a grep over the gate path rather than as "it works".

The pi-has-no-spawn-primitive fact is recorded here rather than assumed,
because it is the thing that makes this hypothesis non-trivial and it is not
written down anywhere else in the graph.
<!-- THOUGHT:END -->