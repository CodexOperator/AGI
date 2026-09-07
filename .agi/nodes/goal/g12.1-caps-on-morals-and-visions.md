---
id: goal:g12.1
mint_id: ea44e514a73a4c30ab13660a30a9e82f
type: goal
parents:
  - goal:g12
confidence: 1.0
edited_by: season.py
goal_id: G12.1
goal_kind: long-term
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
thought_session: season
title: "G12.1: Caps on morals and visions, and season-boundary edges"
---
**G12 sets the chain; this sets the numbers on it.** Two caps, one new edge
concept, and one open question about who may edit the root of the tree.

## Caps: 5 morals, 3 visions, declared in a config node

The owner: morals capped at 5, visions capped at 3, "all in config node."
Two things are true at once here. First, **zero `config`-type nodes exist in
the corpus today** — `context/schemas/[config].md` describes filesystem
locations and says so of itself: "there are zero `config` nodes in the
corpus... Minting a `.geometry/` node from it is G10.2's job and waits on a
code path that reads more than one field." So "the config node" the owner
points at does not exist yet, the same way `moral` does not exist yet.
Second, there is already a **working precedent for exactly this shape**:
`nodes/.geometry/crons.md` plus `context/schemas/[cron].md` — a real node
that a real applier reads at runtime (goal:g10.2), parented to `goal:g10.2`
rather than left parentless (its own authored version-history note records
that `cron` was minted parentless in v1 and corrected in v2, because
"describes the graph's own shape" is not the same claim as "has no
lineage"). Declaring
`moral_cap: 5` and `vision_cap: 3` the same way — a `.geometry`-style node,
parented under `goal:g10.2`, read by `spawn_gate.py` or an extension of it —
is the same move `crons.md` already made, not a new pattern this project has
to invent.

## Seasons: vision changes only through season-boundary edges; morals never change

The owner: visions "update ... only when we use ... season-boundary edges,"
and "moral nodes always stay the same." `[vision].md` already declares a
`season: {type: int}` field — "which season this version of the vision
belongs to" — so the *concept* of a season is not entirely new to the schema.
What is genuinely new is a distinct **edge kind**. `[shape].md :: edge_fields`
currently declares five: `parents`, `next_edges`, `depends_on`, `seeds`,
`proposes_goals` — none of which distinguishes "this parent edge crosses a
season boundary" from "this is an ordinary intra-season edge." The owner's
spec needs exactly that distinction: vision parents arrive "only through
season roll-over edges," goal parents arrive "only through intra-season
standard edges." Minimally, this needs either a new edge field (e.g.
`season_parents:` alongside `parents:`) or a way to tag entries within
`parents:` by kind — today `parents:` is one undifferentiated list, and
`spawn_gate.py` has no notion of "which kind of edge this entry is."

## The cap collides with reality: 17 visions exist, cap is 3

`vision` has 17 live nodes today against a proposed cap of 3. Three ways to
close that gap, named honestly, none obviously right:

- **Retire 14.** Move them to `nodes/deprecated/vision/` per this project's
  deprecate-never-delete rule — mint id and grid history survive, only the
  address changes. Requires picking which 3 of 17 stay, on what basis: the
  current 17 predate the `overview` tier entirely (see G12's collision
  section), so "best 3" has no obvious metric yet.
- **Merge.** Collapse the 17 into 3 by combining their content — loses the
  one-vision-per-overview-set granularity `[vision].md`'s current design
  already assumes.
- **Cap applies to new visions only.** Grandfather the 17 and enforce 3 only
  from here forward — cheapest, but means "3 visions total" is not actually
  true today, and G12's falsifier carries an asterisk until the 14 are dealt
  with.

This goal does not choose between them.

## Moral mutability: by hand initially; CodexOperator-only permission is an open question, not a decision

The owner: morals can be "modified as well but initially only by hand," and
floated — with an explicit "maybe" — restricting that hand-edit to "the
CodexOperator owner of the repo," with a fallback stated in the same breath:
"if not, just leave them as the unique parentless node type." **Record this
as a debated idea, not a requirement** — the owner has not committed to it.

If pursued, it runs into a real constraint worth stating plainly: **a normal
git clone has no concept of per-path write permission.** `CODEOWNERS`
(GitHub) is a merge-review gate on a pull request, not a filesystem lock — it
does nothing to a local clone or a direct push to an unprotected branch.
Branch protection rules are server-side and can be bypassed by anyone with
admin rights, or simply do not apply outside the protected branch. Neither
mechanism stops a local agent (or a person) from editing `nodes/moral/*.md`
directly and committing — the most a hook (`pre-commit`, `pre-push`) can do
is warn or refuse locally, and only for an agent that has the hook installed
and does not bypass it (`--no-verify` defeats it trivially). So "only the
CodexOperator owner may modify morals" is, at best, an advisory policy
enforceable at review time — not a technical guarantee that a careless or
rogue write is prevented at the point of edit. **If pursued, this should be
scoped as "reviewed-and-reverted if violated," not "cannot happen."** If not
pursued, the fallback the owner already named applies: morals stay nothing
more than the unique parentless node type, editable by hand like any other
node, with no special-cased permission at all.

## Falsifier

Once the config-style node exists: `moral` count <= 5, `vision` count <= 3
(or <= 3 among post-cap visions, if the grandfather reading is chosen), and
every `vision` node's parent set includes exactly one edge tagged as a
season-boundary edge — once that edge kind exists to check.