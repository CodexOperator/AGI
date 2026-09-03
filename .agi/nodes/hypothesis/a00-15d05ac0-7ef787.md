---
id: hypothesis:a00-15d05ac0-7ef787
mint_id: f8d4b180f6ef49eab11c56a668134ecc
type: hypothesis
parents:
  - goal:s18
next_edges: []
confidence: 0.0
scaffold_hash: 0c752659b8d6c62b
title: S18 build-site hypothesis content exists only in R-refs, not in goals
testable_claim: For a random sample of 10 build-site nodes carrying a resolvable cavekit_req, >=8 of 10 lack the requirement's acceptance-criteria text in their own body (literally or paraphrased), i.e. the kit file is non-redundant with its host node and inlining is mandatory before deprecation
verdict: pending
---
# hypothesis:a00-15d05ac0-7ef787

## Hypothesis

**Claim:** The 91 resolvable `cavekit_req` references (mapping to real requirements in `context/kits/cavekit-*.md`) point to acceptance criteria and architectural descriptions that are **not** replicated in the host node's own body. The requirement text lives only in the kit file, so deprecating the build-site nodes without inlining that requirement content first destroys information the node was tracking.

**What would prove it:**

Audit a sample of 10 build-site hypothesis or task nodes that carry a resolvable `cavekit_req` value. For each:
1. Read the node's full body.
2. Read the corresponding requirement from `context/kits/cavekit-<domain>.md` (description + acceptance criteria).
3. Check whether the acceptance criteria appear anywhere in the node's body — literally or paraphrased.

If **≥8 of 10** nodes lack their requirement's AC text in their body, the claim is **proved**: the kits are non-redundant with their host nodes, and inlining is essential before deprecation.

**What would disprove it:**

If **≥6 of 10** nodes already contain their requirement's AC text in their body — meaning the `cavekit_req` is merely a redundant cross-reference tag and the real information already lives in the node — then inlining is busywork, and deprecating kits loses nothing the nodes already carry.

**Motivation (from goal:s18 THOUGHT):** The owner's steps (2) "Inline each of the 91 resolvable requirements into its own node body, so the node stands without the kit" and (4) "Only then deprecate the nodes" depend on whether the kit files contain unique information. If they do, inlining is mandatory before deprecation. If they don't, the sequence simplifies to just renaming titles and deprecating.

**Passive observation:** The sampling will also reveal whether the 5 build-site goal nodes differ from the hypothesis/task nodes in how much kit requirement text they absorbed. This informs whether goals-only or all-nodes inlining is the right grain.

**Sample candidates:** `hyp:chain-engine-r1`, `hyp:graph-core-r1`, `hyp:schema-registry-r1`, `hyp:renderers-r1`, `hyp:embeddings-r1`, `hyp:environment-indexers-r1`, `hyp:autoresearch-tree-skill-r1`, plus 3 open build-site hypotheses with no verdict.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1013 (a00-5a762d14), on kid a00-15d05ac0's node. Accepted the claim and the sample design as written; no factual errors found. Verified all 7 named sample candidates exist under `nodes/hypothesis/` (chain-engine-r1, graph-core-r1, schema-registry-r1, renderers-r1, embeddings-r1, environment-indexers-r1, autoresearch-tree-skill-r1). Added the schema-required `testable_claim` frontmatter field (spawn-gate flagged its absence); it is a restatement of the kid's already-written proof threshold (>=8 of 10 lack the AC text). Note: the title says "not in goals" but the claim is about the host node's body — title left as-is, the claim text is authoritative. Verdict stays `pending`; the sampling experiment has not run.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis about whether cavekit requirement content (AC + descriptions) lives only in kit files, not in node bodies. Claims inlining is mandatory before deprecation — testable by sampling 10 build-site nodes and comparing bodies to kit requirement text. Distinct from sibling hypotheses under goal:s18 (experiment-vs-evidence gap, Domain-idea subsumption).
