---
name: town
written_by: [prime_director, owner]   # list-shaped; links.parse_written_by reads a list (L4.50 flip) — town rows are prime/owner-written, like config:vetoes and config:rotations
derived_from: owner ruling 2026-09-12 (doc:l4-owner-decisions body 697-717 @e6d090a77, Prime XVII 18:48Z)
structural: true
fields:
  visions: {type: list}          # vision node ids this town owns. `core` may spell the list or the literal `auto`, meaning "every vision node no other town claims" — `auto` is RESOLVED BY THE LOADER, never hardcoded.
  council: {type: str}           # the NAME of a row in config:posts (`posts.md` is the post-first spelling; `.geometry/seats.md` is the deprecated alias, accepted in this window)
  season: {type: int}            # the town's OWN counter (core 2, streaming-suite 1, web-app-suite 1 — owner ruling)
  season_history: {type: list}   # [{season, global_season, opened, closed}]
  written_by: {type: list}       # [prime_director, owner] — never a kid
  branches: {type: str, refuse: "DERIVED, never a cell — towns.py refuses this key BY NAME at read time; see body"}  # branch names fall out of the cells, never a cell
validation:
  required: [visions, council, season]
  types:
    visions: list
    council: str
    season: int
    season_history: list
spawn:
  allowed_parents: [ladder]
  min_parents: 1
  max_parents: 1
---

# town

**A town is a SUPER node** — owner ruling 2026-09-12 (verbatim in the
`derived_from` above): a town's cells are its `visions` (the vision nodes this
town owns; `core` is every vision no other town claims), `council` (the
`config:posts` row that keeps it), `season` (the town's OWN counter),
`season_history` (the season ledger) — and crucially the town's BRANCH NAMES
are DERIVED from those cells, never stored as a cell. Reading `town:*` nodes is
what `crons.py apply` does for `crons.md`; the towns are the declared rows.

## `branches:` is DERIVED, NEVER a cell

The schema REFUSES `branches:` as a frontmatter cell by name. A town's branch
names (`core/main`, `core/season2/main`, `core/season2/posts/<post>/main`,
`core/season2/posts/<post>/loops/<round>/<agent>`) fall out of the town's
cells — `season`, `council` (post name), and the loop/agent layers — and are
rendered by `towns.derive_names`. Storing them would let the cells and the
branches drift apart; the whole point of the super node is that the branch
names are a view over the cells. If a `branches:` key ever appears, `towns.py`
refuses the node by name.

## `visions: auto`

`core` is allowed to spell its list OR the literal `auto`, meaning "every
vision node no other town claims". `auto` is RESOLVED BY THE LOADER against
the other towns' explicit `visions` lists at read time — never hardcoded into
a file, exactly like `branches:` is never stored.

## `written_by`

`[prime_director, owner]` — same as `config:vetoes` and `config:rotations`.
A town is prime/owner-written; a kid never mints one. The Prime creates the
three towns at merge-up from the create lines.

## spawn

A town's parent is the ladder (`.geometry/ladder.md`), which is where the
towns list and `town_branches` are already declared — the town node is the
row underneath that declaration. Exactly one ladder parent, never a vision
(a vision is a town's CELL, not its ancestor).

## The first towns — created by the Prime at merge-up

`core` (season 2, council `council-core`), `streaming-suite` (season 1,
council `council-streaming-suite`), `web-app-suite` (season 1, council
`council-web-app-suite`). No town node is minted by a round; `ls
.agi/nodes/town/` stays empty until the Prime runs the create lines.