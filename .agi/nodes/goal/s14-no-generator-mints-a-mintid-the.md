---
id: goal:s14
mint_id: 64daaa144abb4309b36b0bab107ede85
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S14
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S14: No generator mints a `mint_id`; the backfill is the only assigner"
---
Every node a generator creates arrives without a `mint_id`, so `grid.py commit
--all` skips it with a loud per-node error until `bin/backfill-mint-ids.py` runs.
Affects `level3.py`, `snapshot-goals.py`, `decompose-engine.py` and the
`cli.py scaffold` path — i.e. every writer except the backfill itself.

Hit twice in one session on 2026-08-25: two new `level3` nodes and one new goal
node each needed a follow-up backfill pass before their history could be
recorded.

A mint id should be assigned **at node creation**, by whatever writes the file,
with the backfill retained only for repair of pre-existing nodes. Until then
"run the backfill after any generator" is an unscripted manual step — precisely
the class this project's design ethic exists to eliminate, and precisely the
kind of step that gets forgotten and silently costs a node its version history.

Note this is also recorded in **G2.5**, where it is currently **invisible to the
graph**: G2.5's body exceeds `snapshot-goals.py`'s 4000-character cap, so the
paragraph is truncated out of `nodes/goal/g2.5`. That is **S12** demonstrating
itself, and it is why this has its own short goal rather than living only as a
paragraph inside a long one.

**Fixed 2026-08-25.** `ensure_mint_id()` lives in `snapshot-goals.py` beside
`write_frontmatter` and is called from inside it, so **one hook covers every
generator that writes through the shared serializer** — `level3.py`,
`decompose-engine.py`, `backfill-mint-ids.py` and `snapshot-goals.py` itself.
`snapshot-build-site.py` carries its own copy of the serializer for historical
reasons and now imports the *hook* by file path rather than duplicating it, and
`cli.py scaffold` mints inline. It never overwrites: an existing valid mint id
is left exactly as found, and an *invalid* one is left alone **and warned
about**, because rewriting it would silently fork the node's grid history.

Verified on the live corpus: `grid.py commit --all` reports `0 error(s)
(missing mint_id)` across 765 nodes, and it did so on the first run after two
generators had minted new nodes — the case that needed a second backfill pass
twice in one session before this.

Still open, and it is why this fix is a hook rather than a consolidation:
**there are two `write_frontmatter` definitions.** S13's finding — that the one
function touching every node on every run is where a silent serialization bug
scales to the whole corpus — applies with double force to a function that
exists twice.