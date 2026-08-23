---
confidence: 1.0
goal_id: G6.7
goal_kind: subgoal
id: "goal:g6.7"
origin: goals-doc
parents:
  - goal:g6
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G6.7: Publish the engine as a grid ref, not a written tree"
type: goal
---

**The question: could a fourth grid dimension replace `stitch.py --out`?** The
grid already has three — D1 chain (`refs/heads/*`), D2 node
(`refs/grid/node/<id>`), D3 session (`refs/grid/session/...`). A D4 *release*
dimension would take each build node's payload, `mktree` it into the engine's
directory layout, `commit-tree` it, and move `refs/grid/release/agi`. The live
engine becomes a ref you can move and roll back, and `agi` is published by
pushing that ref rather than by writing 74 files and committing them.

**Answer the blocking part first, because it decides everything else: there is
no code in the graph to stitch.** A level-3 node holds `payload_ref` — a
*pointer* into the engine repo — plus a mechanically-derived contract.
`stitch.py`'s own docstring is honest about the consequence: `--out` is
"near-identity: resolve 73 pointers, copy 73 files… not a compiler". That shape
was a deliberate decision, recorded in `hyp:level3-node-anatomy` — source lives
on disk exactly once, never inlined. So D4 has nothing to pick out. **The fork
is not `stitch.py` vs. the grid; it is whether a node holds its payload or
points at it**, and that is **G6.3**, which is already the gate on G6.5.

**Once payloads are in nodes, D4 is the better publisher, for one reason worth
stating plainly: a `commit-tree` cannot partially apply.** `stitch.py --out`
writing 74 files can fail on file 35 and leave a half-written engine — the exact
class of defect this project has paid for three times (H0, H0b, H0i). Grid
commits are built with plumbing and never touch a working tree, so either the
ref moves or nothing happened. G6.5's sequencing exists precisely because a cron
that writes the engine before the version layer is trusted is a data-loss defect
waiting to happen; an atomic publisher is what makes step 2 of that sequence
safe rather than merely sequenced.

**And it is not "yet another layer".** D4 reuses the same object store, the same
plumbing helpers and the same push path D2 and D3 already use — the marginal
cost is a ref namespace and a tree-builder, not a second system. A node version
whose content is also on D1 is the same blob.

**So `stitch.py` is not retired — it is re-scoped, exactly as proposed:**
`--verify` stays the valuable half (an independent claim about what the tree
should contain, which `cp -r` cannot make), and `--out` becomes the *test*
materialisation — put the graph on disk, run the suite against it — while
publishing goes through the ref.

Ordering, and none of it is optional: **G6.3** (payload in the node) → this →
**G6.5** step 2 (cron may commit the engine). Building D4 before G6.3 would
produce a publisher with nothing to publish.

Falsifier: with payloads in nodes, build `refs/grid/release/agi` from the graph
and confirm the tree it names is byte-identical to what `stitch.py --out`
produces. If it is not, one of the two is lying about what the graph contains.

**Gained a hard precondition 2026-08-23 (`verdict:payload-in-node`): D4 inherits
S9's defect structurally, not incidentally.** D4's whole plan is to `mktree` each
build node's payload using the same plumbing `commit_file()` uses. Pointed at
that code as it ships, D4 would silently mis-hash every symlinked payload and
downgrade every exec-bit payload — **across the entire published engine tree, in
one commit.**

And atomicity does not save it. G6.7's selling point is "either the ref moves or
nothing happened", which is worthless when the tree being atomically published is
simply the wrong tree, moved cleanly. An atomic publisher of corrupt content is
worse than a partial writer, because the partial writer leaves evidence.

So **S9 is not a shared inconvenience, it is the same fix with two callers.**
G6.3 and G6.7 do not each need their own mode-aware rewrite; they need the one
rewrite to land before either attempts its falsifier.
