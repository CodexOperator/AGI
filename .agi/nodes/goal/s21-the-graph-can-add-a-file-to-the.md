---
id: goal:s21
mint_id: 6349aa237a354f869360370076fdcdb5
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S21
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S21: The graph can add a file to the engine but can never remove one"
---
🔴 **The publish path is one-directional for existence.** `level3.py` mints a
node for a new file authored under `payloads/` and `stitch.py --publish` writes
it into the engine, so the graph can *create*. Nothing anywhere lets the graph
say **"this payload is retired — stop materialising it."** There is no
mechanism, no field and no flag; the capability is absent rather than broken.

This is the missing inverse of **G6.1** and **G6.3**. Those reversed the arrow so
that the graph holds the bytes and the engine tree is what falls out — and a
derivation that can only ever add is not a derivation, it is an append log.

## Found by trying to do it

Five pre-fold files still ship in the engine and are tracked there:

    26 B  autoresearch.config.json      build:autoresearch.config.json
  6,934 B  autoresearch.ideas.md         build:autoresearch.ideas.md
 47,572 B  autoresearch.jsonl            (no node — see below)
  5,662 B  autoresearch.md               build:autoresearch.md
    897 B  autoresearch.sh               build:autoresearch.sh

`TODO.md` already calls them "historical, not load-bearing". Retiring them is
the obvious small chore, and **every available route fails, each in its own
way.** All four were checked against the code, not reasoned about:

**Deprecating the node does nothing to the file.** `stitch.py` reads
`nodes/deprecated/build/` exactly like the live directory, and this is
deliberate and correct — the comment states the reason:

> a retired node still *claims* its `payload_ref`, so dropping it from this scan
> would turn its engine file into an `orphan_files` report — drift, and a
> refused publish — purely because the node was regrouped. Deprecation changes
> an address, not what the graph holds.

That reasoning is right and must not be weakened. **G2.10**'s retirement
convention was built to change a node's *address* without changing what the
graph *holds*; retiring a payload is the other axis and it was never built.

**`git rm` in the engine does not hold.** The bytes are in the node's grid ref,
so the next `stitch --publish` writes the file straight back. Deleting the
engine file is deleting derived output, which is the direction **G6** exists to
forbid.

**Deleting the node file refuses the publish.** `orphan_files` is computed as
`set(scope_files) - claimed`, so an unclaimed file in scan scope fails
`--strict` and gate 2 stops the publish. It also strands the grid ref with
nothing live behind it, which is the decoupling **G2.10** argued against.

**Excluding it from the payload boundary retires the node, not the bytes.**
`payload_boundary.classify()` drives `discover_files`, so a file declared out of
scope makes `level3.py` prune its node as stale — and the file then joins the
**139 unmanaged files** already sitting in the engine with no node at all. The
graph forgets about it; the engine still ships it. That is strictly worse than
today, because now nothing even records that the file exists.

`autoresearch.jsonl` is a fourth case: it has no node, because the boundary
excludes `.jsonl` event streams by rule. Whatever is built here has to say
something about unmanaged files or explicitly decline to.

## Why it matters more than five stale files

The files are the occasion, not the reason. **A publish path that cannot remove
is a graph that silently accumulates**, and every mechanism this project has for
noticing drift is built around *disagreement* between graph and engine, not
*surplus* in the engine. `stitch --verify` counts `missing_payload`,
`stale_contracts`, `duplicate_payload_ref` and `orphan_files` — and a file the
graph has deliberately finished with is none of those four. It is invisible in
exactly the way **G7** exists to forbid.

It also blocks **S18** at its own first step. Absorbing cavekit references
before cavekit retires ends in retiring files, and the ordering hazard already
recorded there (H0i: deleting `context/kits/` prunes 159 `origin: build-site`
nodes) is the same shape seen from the node side. S18 cannot finish while
deletion has no sanctioned path.

## The shape of the fix

**A payload retirement that the graph declares and the publish honours.** A
field on the build node — `payload_retired: true` alongside the existing
`status: deprecated`, since the two are genuinely different axes and **G2.10**
is the precedent for keeping them apart — read by `stitch.py`'s materialise
path, which then skips the file and deletes it from the engine on publish.

Three constraints that fall out of the checks above:

- **`orphan_files` must not fire for a retired payload.** The node still exists
  and still names the file; it now names it as *finished with*. Retirement has
  to be a third state alongside claimed and unclaimed, not the absence of a
  claim.
- **The bytes stay in the grid ref.** Retiring a payload is not deleting
  history, and `stitch --from-grid --grid-version N` must still materialise an
  older version that predates the retirement. This is the same argument that
  made retirement-in-place beat deletion for nodes.
- **Deletion must be idempotent and survive a second publish.** The failure mode
  to fear is a file that comes back, since `--publish` runs hourly from cron.

Deliberately open: whether unmanaged files (139 of them, no node, `.jsonl`
streams and similar) are in scope at all, or whether this covers only files the
graph actually holds. Deciding that is part of the work.

Falsifier: mark one build node's payload retired, publish twice, and check the
engine. The file must be gone after the first publish, still gone after the
second, `stitch --verify --strict` must report zero findings in all four
categories, and `--grid-version N` for a version predating the retirement must
still materialise the file. Today none of that is expressible.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node exists because I asserted the opposite of the truth and got caught by
checking. Asked to retire the five pre-fold files, I offered "deprecate the
nodes and publish, and stitch will prune the engine files" as a menu option and
the owner picked it. It is wrong. `stitch.py` reads deprecated build nodes
*specifically so that it keeps materialising their payloads*, and says so in a
comment written when G2.10 shipped. I had read that comment two iterations
earlier, in the commit message for the retirement convention, and still
mis-stated it.

Worth recording as more than an error, because the shape is reusable: the
project has a strong, correct convention that retiring a node changes its
**address** and not what the graph **holds**, and I generalised it one step too
far into "retiring a node retires its payload". The convention is load-bearing
in the other direction. Two axes that look like one until you need only one of
them.

I checked the three remaining routes before writing this rather than assuming
they would also fail, and they fail differently enough to be worth listing
individually — `git rm` reverts on the next publish, node deletion refuses the
publish, boundary exclusion retires the node and abandons the bytes. That the
failures are all distinct is itself the evidence that this is an absent
capability and not a misconfiguration.

Filed as S rather than G6.10 on the pattern S19 set: a specific named defect
that cross-references its structural parent instead of nesting under it. The
mechanical consequence agreed — order 84 appends and renumbers nothing, where a
G6.10 would have bumped every goal after g6.9 and needed a hand-wired `seeds:`
edge because S7 is still open.

Not built, on the owner's instruction, and the five files are still shipping. If
whoever picks this up finds the retirement field already half-present somewhere,
suspect me: I looked for one and did not find it, but I looked from stitch.py
outward rather than from the schema in.
<!-- THOUGHT:END -->