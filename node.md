---
id: goal:s18
mint_id: 308859ad381e4981b087e3c947928cab
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: alive
goal_id: S18
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
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
COMPLETE, not retired (council, alive, 05:xZ 09-30; belam's rule: retired = stopped making sense, complete = achieved; a goal is never retired while a child hypothesis is pending) on the owner 05:0xZ 09-30 verbatim: "DG2 is talking about a running hypotheses under s31 when s31 is retired needs fixing in graph". Achieved in the bytes (all-is-one, 02:1xZ): the kits retired 09-03, 91/94 cavekit_req carriers retired, 0 live build-site nodes; its 4 hypotheses now carry closing verdicts + evidence_runs (DG2 dg2close-*-check): a00-05c5c2b4 proved, a00-15d05ac0 disproved, a01-1f2762d5 proved, a01-697f4893 inconclusive_lean_disproved:80 -- all moot since L1.09 retired the build-site cohort. No remainder.
<!-- THOUGHT:END -->
