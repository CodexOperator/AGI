---
confidence: 1.0
goal_id: G6.1
goal_kind: subgoal
id: "goal:g6.1"
mint_id: 73547cd61d2f4e37847b43ee6e050a83
origin: goals-doc
parents:
  - goal:g6
seeds:
  - exp:stitch-roundtrip-r1
  - idea:engine-decompose-engine
  - idea:engine-stitch
status: active
tags:
  - goal
  - subgoal
title: "G6.1: agi-tree becomes the source of truth agi is assembled from"
type: goal
---

**The direction of authority reverses.** Today the graph describes the engine
after the fact. The target is that the engine is *assembled from* the graph —
the code is a projection of level-3 nodes, not a thing the nodes comment on.
This is the goal G2.1 serves and the reason level 3 is built first.

Ordering that follows from it: a decomposition census (which surfaces exist) →
level-3 nodes with contracts attached (what each promises) → stitch-to-directory
(the projection runs) → the engine's own changes originating as nodes.

**The arrow reversed 2026-08-25, and it is measured rather than declared.** The
last step above ran for the first time: **S12's fix reached `agi` without a
single file in that repo being opened by hand.** The path is
`payloads/<payload_ref>` (edit) → `grid.py commit --all` (the graph records it
as the node's next version) → `stitch.py --out <engine> --from-grid --publish`
(the engine tree is written from the graph). `--grid-version` landed the same
way, immediately after, as the second instance rather than a one-off.

What makes that a projection and not a copy: `resolve_payload` prefers the
graph's own staged bytes over the engine tree, so once a payload is checked out
the engine is **never consulted** — `stitch --from-grid` reproduces a file the
engine no longer has on disk, which is a regression test, not a thought
experiment. The four preconditions all cleared in one pass: **S9** (the grid
can carry a mode losslessly), **G6.3** (the payload is in the node's ref),
**S14** (a generator-made node is never skipped by the grid), and **G6.6**'s
coverage half (180 of 180 in-boundary engine files carry a node — 0 uncovered,
0 stale claims, measured against `payload_boundary.classify`).

**Bootstrap deviation, recorded on purpose.** The change that made this possible
was itself made as a direct engine edit, because it is the change that makes
graph-first edits possible and nothing else could have carried it. That is the
one legitimate instance; every engine change after it originates here.

**Still open, and the reason this stays `active` — the *reverse* direction is
still engine-first.** `level3.py` derives every contract by scanning the engine
tree, and `stitch.py --verify` compares stored contracts against files on disk
there. So the graph now *writes* the engine but still *learns* about it by
reading the engine, which means a payload edited only in the graph has a stale
contract until a publish + rescan. The loop closes when derivation reads the
payload out of the node's ref the same way materialisation now does.
