---
id: goal:s18
mint_id: 308859ad381e4981b087e3c947928cab
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: all-is-one
goal_id: S18
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: retired
tags:
  - goal
  - root
  - short-term
thought_session: g1-g7-rewrite-2026-09-19
title: "S18: Absorb cavekit references before cavekit retires"
---
Cavekit was the bootstrap that seeded this graph and is being phased out.
The graph still leans on it in three ways, and **the retirement order matters
more than the retirement**.

Measured 2026-08-27:

- 94 nodes carry `cavekit_req`. **91 resolve** to a real requirement in
  `context/kits/`; the premise that ids like `R11` dangle is wrong -- they
  resolve. Only **3** are broken, and none of those is an R-ref: they are free
  text in a `<domain>/R<n>` field (`chain-engine/iterative-fix`,
  `structural-bias/synthetic-repair`, `bootstrap/chain-block`), and the last
  two name domains with no kit file at all.
- **233 titles** carry cavekit vocabulary: 142 with `R#`, 91 with `T-#`.
  Legacy-named, not broken.

**The hazard.** `context/kits/` and `context/plans/build-site.md` are
generator inputs for 159 `origin: build-site` nodes -- all 94 tasks and 61
hypotheses among them. `snapshot-build-site.py` deletes every `build-site`
node it does not re-derive on that run, so deleting the kits to "retire
cavekit" prunes 159 real nodes on the next loop. That is H0i exactly, with a
new motive.

Sequence, and it is not negotiable:

1. Fix the 3 malformed `cavekit_req` values.
2. Inline each of the 91 resolvable requirements into its own node body, so
   the node stands without the kit.
3. Rename `R#`/`T-#` out of the 233 titles into graph-native vocabulary.
4. Only then deprecate the nodes -- and **never** delete the input.

Pairs with **S11** (same rename hazard, same sequence) and **G7**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all-is-one (council) 02:4xZ 09-30, CORRECTED 03:1xZ, S-goal retirement (alive convenes; belam owner-task). OWNER 01:2xZ 09-30 verbatim: "All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals." Measured, NOTHING LEFT OPEN: the hazard this row guarded (deleting context/kits prunes every origin: build-site node) is closed, since kits + plans/build-site.md retired 2026-09-03 (CLAUDE.md, L1.09) and snapshot-build-site.py is a permanent no-op here; the absorption happened in the safe order: of the 94 nodes that carried cavekit_req, 91 are retired (deprecated + moved), 0 live origin: build-site nodes remain. The 3 live cavekit_req values are the free-text ones this row itself found (bootstrap/chain-block, chain-engine/iterative-fix, structural-bias/synthetic-repair on three a00-ddbe3410 hypotheses); DG2's verdict on hypothesis:a01-1f2762d5-1d90c0 (proved 0.85, 7211a6473) measured that inlining them changes nothing and nothing reads the field on hypotheses, so they are labels, not links. CORRECTION: the first version of this THOUGHT named them graph-core/R1, R2; those came from retired nodes (my grep -v ran after git grep -h had dropped the paths), caught by DG2. Retired, no remainder leaf; its 4 child hypotheses carry closing verdicts (DG2, 7211a6473). Retired IN PLACE per the agi-goal skill.
<!-- THOUGHT:END -->
