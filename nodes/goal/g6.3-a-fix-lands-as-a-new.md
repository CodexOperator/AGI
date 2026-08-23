---
confidence: 1.0
goal_id: G6.3
goal_kind: subgoal
id: "goal:g6.3"
origin: goals-doc
parents:
  - goal:g6
seeds:
  - hyp:payload-in-node
status: active
tags:
  - goal
  - subgoal
title: "G6.3: A fix lands as a new version of a build node"
type: goal
---

**The mechanism to test, and the reason to test it on real work.** Today an
engine fix is edited in the engine repo, and `level3.py` re-derives the build
node afterwards — the node trails the code. The target is the reverse: a fix is
applied *as a version update to the build node*, and the engine file follows
from it via `stitch.py`.

This is also how the grid's version dimension gets exercised for the first time
on content that matters. `refs/grid/node/<id>` already records one version per
change and the grid held 535 refs after its first full pass; what has never been
tested is a build node accumulating **meaningful** versions — v1 → v2 → v3 as a
real fix evolves — and `stitch.py` materialising a chosen version rather than
whichever is current.

Falsifier: take one real fix from this session, apply it as a build-node version
update, stitch it out, and confirm the engine file is byte-identical to what the
direct edit produced. If it is not, the version layer is not yet a source of
truth and should not be described as one.
