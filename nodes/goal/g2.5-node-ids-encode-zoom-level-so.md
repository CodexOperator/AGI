---
confidence: 1.0
goal_id: G2.5
goal_kind: subgoal
id: "goal:g2.5"
origin: goals-doc
parents:
  - goal:g2
seeds:
  - hyp:zoom-encoded-node-ids
  - level3:bin-grid@v2
status: active
tags:
  - goal
  - subgoal
title: "G2.5: Node ids encode zoom level, so a collision is structurally impossible"
type: goal
---

**Ids are the one piece of a node that must survive every transform, and today
they survive none of them.** The current scheme is `<type>:<kebab-slug>` minted
from source text, with collisions resolved by appending `:2`. It fails in three
independent ways, all observed in this corpus:

- **The loader hides files.** Every load of agi-tree prints ~18
  `WARN: duplicate node id ... kept X, hidden Y` lines. A node that exists on
  disk is silently absent from the graph (G7.2), and the two loaders disagree
  about what to do about it (G7.4).
- **The grid ref is not injective.** `grid.py sanitize()` rewrites any character
  outside `[A-Za-z0-9._%-]` to `-`, so `level3:bin-stitch@v2` and a hypothetical
  `level3:bin-stitch-v2` both become `refs/grid/node/level3/bin-stitch-v2` and
  silently share one version history. Confirmed live on 2026-08-24 by the three
  `@v2` build nodes minted that day. The function's own docstring already argues
  that collapsing to `-` "would let two ids share one ref and silently overwrite
  each other, which is a worse failure than the crash" — it then does exactly
  that for every other punctuation character.
- **Slugs are not stable under editing.** The id is derived from title text, so
  retitling a node either changes its identity or requires the slug to stop
  matching the title. Both are bad; the graph currently gets both.

**The scheme to build.** Ids are hierarchical and positional, like a phone
number: a node's id is its parent's id plus **one** additional alphanumeric
character identifying it among its siblings. The coarsest level is **5
characters**; each finer level adds one. Level 3 — the code level, G2.1's base —
is therefore 7 characters, which pins the two levels above it at 5 and 6.

Three properties follow, and they are the whole point:
- **Uniqueness is by construction, not by check.** Enforce sibling-local
  uniqueness at each level and global uniqueness only at the root; global
  uniqueness of every id below falls out. There is nothing left for a collision
  resolver to do, so there is no `:2` suffix and no "kept X, hidden Y".
- **An id is a path.** Truncating an id to N characters yields the id of its
  ancestor at that zoom level, so a coarse view can be computed from a fine one
  by string slicing — no lookup, no join. That is what makes it *related between
  zoom levels* rather than merely unique.
- **Ids are ref-safe by construction.** Alphanumerics only, so `sanitize()`
  becomes the identity function and the grid's injectivity problem disappears
  rather than being escaped around.

**The open decision, stated honestly: this or UUIDs.** UUIDs are off-the-shelf,
collision-free without any hierarchy discipline, and the storage cost is
irrelevant at this scale (810 nodes × 36 chars is noise). The argument against
them is not storage or CPU — it is that **this project's entire delivery
mechanism is an embedded ASCII map a model reads**, and a map of UUIDs is
unreadable by the reader it exists for. G9 is a goal about legibility; a
36-character opaque id is a direct tax on it, paid on every injected map, every
iteration, forever. Decide on that axis, not on bytes.

**Falsifier — run 2026-08-24, and it did not fire.** One alphanumeric character
is 36 values case-insensitively, 62 case-sensitively, so **no node may have more
than 36 (or 62) children**. Measured over all 831 node files: max fan-out is
**20**, on `idea:engine-graph-core`. Zero parents exceed 36; zero exceed 62. The
level-3 layer — the one this goal pins at 7 characters and flagged as the
known-large-fan-out risk — has the same worst offender at the same 20. Chain:
`hyp:zoom-encoded-node-ids` → `exp:id-fanout-budget` →
`verdict:zoom-encoded-node-ids` (proved, conf 0.9, evidence resolves,
independently recomputed by the reviewing parent).

So the fixed one-char-per-level rule survives this corpus with 1.8× headroom,
and no variable-width or escape-hatch design is needed today. **Watch
`idea:engine-graph-core`:** it is the c
