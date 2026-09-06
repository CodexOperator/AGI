---
id: goal:s18
mint_id: 308859ad381e4981b087e3c947928cab
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S18
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
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
Owner direction, 2026-09-03, and it changes the shape of this goal from "absorb references" to "mine the sites, then close what they started". Measured corpus: 168 origin: build-site nodes -- 91 task, 61 hypothesis, 8 idea, 5 goal, 1 each build/experiment/mvp. Of the 61 hypotheses, only 9 reach a verdict: FIFTY-TWO OPEN CHAINS. The instruction, in order. (1) Go through the build sites and find descriptions that belong in a goal; move those into goals rather than losing them when the sites go. (2) Before deprecating anything describing a stale shape, confirm an equivalent goal already exists AND is being built -- this goal is that goal for the cavekit half, and it is currently horizon, not active. (3) Then walk the 52 open hypothesis chains and spend iterations closing them, UNLESS another part of the graph already contains every piece a given chain was trying to establish, in which case close it on that ground and say so. TWO CONSTRAINTS THAT ARE LOAD-BEARING. snapshot-build-site.py deletes every origin: build-site node it does not re-derive on that run, so kits are removed AFTER their nodes are deprecated, never before (H0i). And the 8 Domain: ... ideas are the top attractors -- idea:domain-graph-core alone has 68 descendants and heads the list every agent is handed -- so deprecating them guts target selection unless something replaces it first. ON THE MECHANISM the owner asked about: deprecation is the right tool and does what was wanted. `retired` is a GOAL status; `deprecated` is a NODE status and moves the file to nodes/deprecated/<type>/. Since L1.05 the injected map hides deprecated nodes and their subtrees, so an agent cannot pick one as a live chain head, while the human viewport still shows them as damage.
<!-- THOUGHT:END -->