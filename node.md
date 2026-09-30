---
id: hypothesis:a00-15d05ac0-7ef787
mint_id: f8d4b180f6ef49eab11c56a668134ecc
type: hypothesis
parents:
  - goal:g1.2
next_edges: []
confidence: 0.0
edited_by: belam
evidence_runs:
  - experiment:dg2close-a00-15d05ac0-7ef787-check
scaffold_hash: 0c752659b8d6c62b
season: 1
testable_claim: For a random sample of 10 build-site nodes carrying a resolvable cavekit_req, >=8 of 10 lack the requirement's acceptance-criteria text in their own body (literally or paraphrased), i.e. the kit file is non-redundant with its host node and inlining is mandatory before deprecation
thought_session: season
title: S18 build-site hypothesis content exists only in R-refs, not in goals
verdict: disproved
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
Moved from goal:s18 to goal:g1.2 because its claim (kit requirement text is non-redundant with its host nodes, so inlining must precede deprecation; disproved) decides which cavekit pieces must be absorbed before the kits go -- g1.2's fold-in boundary. goal:g1.2 (horizon, a leaf: take cavekit's pieces, do not merge wholesale, one vocabulary not four) is the live goal that owns the cavekit boundary s18 was retiring; no deeper live goal carries it. Owner, verbatim: "Move all hypotheses under all retired s goals to be patented by appropriate nested g-goals". Parenthood only (owner: "The regime doesn't need a goal. We're just adjusting parenthood"): mint_id, body and verdict unchanged.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis about whether cavekit requirement content (AC + descriptions) lives only in kit files, not in node bodies. Claims inlining is mandatory before deprecation — testable by sampling 10 build-site nodes and comparing bodies to kit requirement text. Distinct from sibling hypotheses under goal:s18 (experiment-vs-evidence gap, Domain-idea subsumption).
