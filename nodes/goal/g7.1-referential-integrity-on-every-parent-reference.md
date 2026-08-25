---
confidence: 1.0
goal_id: G7.1
goal_kind: subgoal
id: "goal:g7.1"
mint_id: 3feb9ce4e95341bb96ecc424bc5b7421
origin: goals-doc
parents:
  - goal:g7
seeds:
  - exp:integrity-detection-r1
status: active
tags:
  - goal
  - subgoal
title: "G7.1: Referential integrity on every parent reference"
type: goal
---

L15 validates `goal:`-prefixed parents only. Everything else dangles silently,
and on this corpus 60.3% of parent references did — a `hypothesis:` vs `hyp:`
prefix mismatch that quietly disconnected most of the `spawns` graph the
attractiveness ranking is computed over. Nothing warned, and the ranking was
read as authoritative for months.

Extend the existing check to all parent references: warn by default, `--strict`
to fail. The mechanism exists; only its scope is wrong. Owns TODO **H4d**.

**Corpus swept 2026-08-25, and the policy is now decided rather than implied.**
The check was extended and then run to ground: 82 unresolvable parent references
across 20 distinct strings, on a corpus with 0 duplicate ids (G7.2's blocker had
to clear first). 79 were resolved; 3 were deliberately left standing and are
owned elsewhere (G7.8 and G7.5 below). Node count did not move — no node was
created or deleted to make a reference resolve, which is the rule this sweep was
run under.

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

**Still unbuilt, and the reason this stays `active`:** the sweep was manual. The
check reports, it does not enforce — nothing stops the next generator run from
minting the same class of reference, which is precisely what G7.8 records.
`spawns:` and `next_edges:` are still unchecked in both directions.
