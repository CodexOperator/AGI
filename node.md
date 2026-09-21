---
id: goal:g7.1
mint_id: 3feb9ce4e95341bb96ecc424bc5b7421
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - exp:integrity-detection-r1
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.1: Referential integrity on every parent reference"
---
L15 validates `goal:`-prefixed parents only. Everything else dangles silently,
and on this corpus 60.3% of parent references did — a `hypothesis:` vs `hyp:`
prefix mismatch that quietly disconnected most of the `spawns` graph the
attractiveness ranking is computed over. Nothing warned, and the ranking was
read as authoritative for months.

Extend the existing check to all parent references: warn by default, `--strict`
to fail. The mechanism exists; only its scope is wrong. Owns TODO **H4d**.

**Corpus swept 2026-08-25. `INTEGRITY` is 0 — every parent reference in the
corpus resolves.** The check was extended and then run to ground: 82
unresolvable parent references across 20 distinct strings, on a corpus with 0
duplicate ids (G7.2's blocker had to clear first), plus 7 blank `parents:`
entries that named nothing. All are gone. **No node was created or deleted to
make a reference resolve** — the two that could not be fixed by editing a node
were fixed at their sources instead (G7.5 by repairing the file that would not
parse, G7.8 by repairing the kit that was missing a requirement).

**The decided policy, in the order it is applied:**

1. **Unambiguous prefix typo on a node that carries real content → repoint.**
   Exactly one qualified: `a00-ddbe3410-exp001-graph-core-r1-t001` →
   `hyp:graph-core-r1`. It has a title, tags, `status: complete` and a second
   parent (`task:t-001`) that already resolved.
2. **Dangling parent on a hop-padding node → drop the link, leave it
   parentless.** 72 of the 82. These are the `X-r1-extendN` / `X-r1-r1-extendN`
   families: contentless nodes whose entire body is hop arithmetic
   (*"Chain extension experiment cycle 1 (hops = 2*0+8 = 8)"*), byte-identical
   across domains. **Repointing them was available and was rejected on
   purpose** — `hyp:X-r1` exists for all ten domains, so the typo was fixable,
   but fixing it would reconnect 60+ synthetic hops and inflate
   `longest_chain_length` and `avg_chain_depth` with exactly the gamed structure
   the metrics rule exists to refuse. **A resolvable reference is not a reason
   to restore a chain that carries no signal.** Dropping is the honest record:
   they were never really attached.
3. **Genuinely absent ancestor → drop the link.** 6 refs, incl.
   `exp:chain-engine-r15`, `exp:a00-c2ec59b7-b391d9-r2` (whose hypothesis still
   lists it under `spawns:` — a forward dangle no check reads yet) and
   `verdict:autoresearch-tree-skill-r1:extend7`. Where a sibling pattern
   suggested a plausible substitute it was **not** taken; inferring an edge is
   inventing one.

Note what this leaves: **76 nodes are now parentless.** That is the intended
outcome, not a regression — it makes the disconnection visible where it was
previously disguised as a broken pointer. Orphan count is the honest successor
metric to dangling-reference count.

Note what this leaves: 76 nodes were made parentless by step 2, and **75 of them
were then deleted outright** as the noise they were — recorded separately in
**S15**, which owns the node-count drop that purge caused. The one survivor,
`verdict:chain-engine-r15`, was kept because it carries a real measurement
(*"7 domains achieve 12-hop chains on cold reload … 241 tests pass"*) even though
what it measures is the padding technique itself.

**Still unbuilt, and the reason this stays `active`:** the sweep was manual. The
check reports, it does not enforce — nothing stops the next generator run from
minting the same class of reference. `spawns:` and `next_edges:` are still
unchecked in both directions, which this sweep proved matters: the repaired
G7.5 node's stray line was a `spawns:` entry, and three `next_edges:` pointed at
nodes S15 deleted. A reference is a reference; checking only one field name is
the same scope mistake L15 made with `goal:`.