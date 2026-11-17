---
id: hypothesis:paper-proofs-hold
mint_id: e738bd657f464ee28c8cc3d8ad3487b0
type: hypothesis
parents:
  - idea:paper-graph-route
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
  - paper
title: "Every proof in the class paper draft is correct and complete"
testable_claim: "Every theorem, proposition and corollary in doc:draft-paper-v0 is true as stated and its proof is complete and correct; every worked example's arithmetic is right."
confidence: 0.6
town: core
---
# hypothesis:paper-proofs-hold

## Measured
The draft states 9 results with proofs (Thm channels n-1 vs C(n,2); Thm topological order iff acyclic; Cor parents-first; Prop p^k compounding; Prop checkpoints; Thm 3-vote q(p)-p = p(1-p)(2p-1); Prop best-of-k limit mu(p>0); Prop ancestor read bound) and a sign-test example (n=12, P[X>=10]=79/4096). meme-master re-ran every example's arithmetic by script 11-17 06:4xZ: all equal.

## CLAIM
Every theorem, proposition and corollary in doc:draft-paper-v0 is true as stated and its proof is complete and correct; every worked example's arithmetic is right.

## Dispatch line
config-max: none / template-max: none / code: none. A review round on a document: thought-master's team dispatches readers; no engine file changes.

## Experiment
One adversarial reader per result, who did not write it, tries to break it: a counterexample, a missing case, a hidden assumption not stated (e.g. independence), a wrong constant. A finding names the result, the line, and a fix as a PATCH to the .tex.

## FALSIFIERS
Any result with a counterexample or a gap that a fix must close; any worked example whose number differs from an independent recomputation.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. Rubric rows hit: Support for Main Ideas (15), Sense of Problem Solving Process (15).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17: one of P1-P4 under idea:paper-graph-route, for thought-master's council to word.
<!-- THOUGHT:END -->
