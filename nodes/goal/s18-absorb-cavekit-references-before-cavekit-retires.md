---
confidence: 1.0
goal_id: S18
goal_kind: short-term
heading_level: 2
id: "goal:s18"
mint_id: 308859ad381e4981b087e3c947928cab
order: 80
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S18: Absorb cavekit references before cavekit retires"
type: goal
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
