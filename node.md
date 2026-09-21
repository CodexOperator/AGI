---
id: goal:g2.5
mint_id: 1400b89c012d4ee08f666ad61b471bc0
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - hyp:zoom-encoded-node-ids
  - build:bin-grid@v2
  - build:src-graph-core-identity@v2
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G2.5: Node ids are hierarchical addresses, not lineage"
---
**An id should answer "where is this node" in one string, with no lookup and no
ambiguity.** Today's scheme is `<type>:<kebab-slug>` minted from title text,
collisions resolved by appending `:2`. It fails three ways, all observed here:

- **The loader hides files.** Duplicate ids meant a node present on disk was
  silently absent from the graph (G7.2), and the two loaders disagreed about
  what to do (G7.4). 17 such pairs existed on 2026-08-24; the generator that
  produced them was fixed the same day.
- **The grid ref was not injective.** `sanitize()` collapsed every unsafe
  character to `-`, so `build:bin-stitch@v2` and `level3:bin-stitch-v2` mapped
  to one ref and would have shared a version history. Fixed 2026-08-24 by
  percent-encoding (`build:bin-grid@v2`) — but that is an escaping patch. It
  makes collisions impossible *to cause by encoding*; it does not make ids
  addresses.
- **Slugs are not stable under editing.** The id derives from title text, so
  retitling either changes identity or desynchronises slug from title. The
  graph currently gets both.

**The scheme, and the correction that matters: ids are addresses, not
ancestry.** Every real node is a code-level node and carries a **fixed 7-character
id**. The entire current graph is 7 characters wide — ids do not grow as the
graph gains nodes or versions.

Zoom levels are **not different nodes.** A zoomed-out view shows the *same*
nodes, grouped by the renderer into supernodes, and a supernode's id is simply a
**prefix** of its members' ids:

```
j8ids9    supernode        (6 chars — a renderer grouping, not a stored node)
j8ids93   the build node   (7 chars — a real file on disk)
j8ids9    <- truncate(j8ids93, 6) yields its parent group, by string slicing
```

So the coarsest view is 5 characters, the next 6, and real nodes 7. Truncating
an id to N characters *is* the lookup — no join, no index, no traversal.

Properties that follow:
- **Addressing is O(1) and unambiguous.** Any node, any supernode, named by one
  short string. An id can also *direct* placement: give a build node the 6-char
  id of a different supernode and that is the instruction to move it there.
- **Grouping is renderer-side and live.** Supernodes are computed, never stored.
  Nothing has to be re-parented to change a view.
- **Ids are ref-safe by construction.** Alphanumeric only, so `sanitize()`
  collapses to the identity function and the escaping layer stops mattering.

**Capacity, and this is the real constraint.** One alphanumeric character is 36
values case-insensitively, 62 case-sensitively, so **a supernode holds at most
36 (or 62) members** — and that budget applies to *renderer groupings*, not to
parent/child links. At 814 nodes the corpus needs at least 23 six-character
groups under the 36-alphabet (14 under 62). That is a statement about how the
tag taxonomy must partition, not about the graph's shape.

⚠️ **The falsifier run on 2026-08-24 measured the wrong quantity and does not
carry over.** `exp:id-fanout-budget` counted children per parent by the
`parents:` field (max 20, on `idea:engine-graph-core`) and
`verdict:zoom-encoded-node-ids` proved the budget on *that* reading. Under the
address model the binding number is **members per shared prefix**, which is
determined by tags (G2.6), not by lineage. The old measurement stands as a fact
about lineage fan-out and is retained as prior art; it is **not** evidence for
this goal's capacity claim. Re-running it against tag-derived groupings is
pre-registered and unrun.

**Tension resolved 2026-08-25: two identifiers, two jobs.** A re-derived address
is a moving address — retag a node, its group changes, its prefix changes, its id
changes. Keying grid history on that would make every regroup a ref migration,
and four of those on 2026-08-24 were enough to price it. So the graph carries
**two** identifiers and they are never the same field:

| | **mint id** | **address** |
|---|---|---|
| Assigned | once, at node creation | derived, re-derived freely |
| Ever changes | **never** | on every regroup/retag |
| Shape | uuid or equivalent, opaque | 7 chars, alphanumeric, hierarchical |
| Keys | `refs/grid/node/<mint-id>` | addressing, zoom, prefixes |
| Read by | the grid, cross-links, provenance | humans, renderers, agents |

The address stays mutable and cheap precisely *because* nothing durable hangs
off it. History follows the mint id, so a node can be regrouped, retagged and
re-addressed without touching a single ref.

**Known gap, found landing this: no generator mints a `mint_id`.** The backfill
(`bin/backfill-mint-ids.py`) is the only thing that assigns one, so every node a
generator creates — `level3.py`, `snapshot-goals.py`, `decompose-engine.py`, and
the `cli.py scaffold` path — arrives without one and is skipped by
`grid.py commit --all` with a loud per-node error until a backfill runs. Observed
immediately: two new `level3` nodes from the same session needed a second
backfill pass. A mint id should be assigned **at node creation**, by whatever
writes the file, with the backfill retained only for repair. Until then, "run
the backfill after any generator" is an unscripted manual step, which is exactly
the class this project's design ethic says to eliminate.

**Grouping stays hash-derived for now, deliberately.** Addresses mint from a
hash of the node, which means today every 6-char prefix holds exactly one member
— the hierarchy is present in the format but not yet exercised. That is accepted
rather than patched: the grouping that will populate prefixes comes from tags
(**G2.6**), and inventing a placeholder taxonomy first would be throwaway work
built on `type` values that are themselves being retired (see G2's note on
`level3`). The ≤36-members-per-prefix budget binds when tags land, not before.

**Sequencing.** Minting 7-char ids rewrites every id in the corpus, so it needs
a migration that preserves grid history plus an old→new mapping kept as prior
art. Assignment must be **deterministic and stable under insertion** — an id
derived from sort position renumbers everything after an inserted node, which is
the failure mode to design out first.

Closes the identity half of **G7.2** and **G7.4**. Depends on **G2.6** for the
grouping the prefixes encode.