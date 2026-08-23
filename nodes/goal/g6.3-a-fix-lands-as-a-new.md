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

**Payload model decided 2026-08-23 (iter-9006 → 9008), and the falsifier is now
known to be passable.** The chain is `hyp:payload-in-node` →
`exp:grid-payload-roundtrip` → `verdict:payload-in-node` (proved, conf 0.75,
evidence resolves).

- **The pick: grid-ref payload.** `payload_ref` keeps its shape; only its
  *resolution rule* changes, from "read this path off the engine tree" to "read
  this path from `refs/grid/node/<id>`'s tree". Inline body lost — three
  independent docstrings rule it out and a source file containing a fence breaks
  the node's own parser. Blob-sha lost on authoring mechanics, not storage: the
  blob must exist before the sha can be written, so the edit is never expressible
  as one node write, and a sha-to-sha diff says *that* something changed and
  nothing about *what*.
- **Proved at the mechanism level, with bytes.** Git's tree format carries
  content, exec bit and symlink-ness losslessly across real version history — 4
  files × 3 bumps, sha256-matched against a non-git baseline.
- **Blocked on S9, and this is the operative sentence:** "payload lives in the
  node's grid ref" is a proved **design**, not a proved **deployment**. Wiring
  resolution to `commit_file()` as it ships today reproduces the failing variant.
  S9 first.

This also settles that the anatomy decision was not overturned by fiat. A grid
ref is never checked out, so it is not a second copy of the tree — it is a second
*name* into the same object store. When bytes match, git's hashing makes them the
same object, which is a stronger non-drift guarantee than "never inlined" was
reaching for.
