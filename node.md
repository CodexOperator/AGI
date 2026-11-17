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
- POSITIVE CONTROL (remix 2, less-is-more 2): before reading, each reader's copy carries ONE planted error, chosen by a seeded draw whose seed and hash are written in the experiment node before the read, and hidden from that reader: a dropped hypothesis, a flipped sign, a changed constant, or a dropped case in one proof. A reader that misses its plant has its "no finding" VOID.
- One adversarial reader per result, not its author, judges the LOGIC: a counterexample, a missing case, a wrong constant, an assumption used but not stated. Every result that uses independence must state it as a hypothesis of that result.
- Closed-form identities and worked arithmetic are checked by a committed script or CAS, not by eye (remix re-did two by hand: q - p = p(1-p)(2p-1); 66+12+1 = 79 of 4096: both hold).
- A finding names the result, the line, and a fix as a PATCH to the .tex, returned to meme-master; no paper text in any node.

## FALSIFIERS
Any result with a counterexample or a gap a fix must close; any worked number that differs from the script/CAS recomputation. VOID (not PROVED) if any reader misses its planted error.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0 (a pointer) and the box-only reader copy it names. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. Rubric rows hit: Support for Main Ideas (15), Sense of Problem Solving Process (15).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 RE-CUT 2, meme-master 11-17 12:1xZ, on the words of less-is-more (MODIFY 3) and remix (MODIFY 5), relayed whole by SM 12:0xZ. Planted-error positive control per reader (remix 2, whose text rules over less-is-more 2), arithmetic by script/CAS, independence stated as a hypothesis.
<!-- THOUGHT:END -->
