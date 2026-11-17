---
id: hypothesis:paper-meets-rubric
mint_id: 7fb2a6a3c3bc4168b6a8c5171751665c
type: hypothesis
parents:
  - idea:paper-graph-route
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
  - paper
title: "The class paper draft meets every row of the owner's rubric"
testable_claim: "Scored blind by a seat that did not draft it, doc:draft-paper-v0 earns at least 12 of 15 on each 15-point row and at least 4 of 5 on the abstract and the conclusion, with a one-line reason per row and a concrete fix for any row below the line."
confidence: 0.6
town: core
---
# hypothesis:paper-meets-rubric

## Measured
Rubric (owner, 11-17): Appropriate Topic (Mathematical Depth) 15; Abstract 5; Clarity (organized, visually easy to follow, correct grammar and mathematical notation) 15; Development of Ideas (appropriate background discussion, examples when necessary) 15; Support for Main Ideas (necessary definitions, theorems, examples) 15; Sense of Problem Solving Process (uses definitions and theorems correctly, correct overall logic) 15; Shows Understanding of Overall Topic (big picture clear, pieces fit together) 15; Conclusion 5; Total 100.

## CLAIM
Scored blind by a seat that did not draft it, doc:draft-paper-v0 earns at least 12 of 15 on each 15-point row and at least 4 of 5 on the abstract and the conclusion, with a one-line reason per row and a concrete fix for any row below the line.

## Dispatch line
config-max: none / template-max: none / code: none. A review round on a document: thought-master's team dispatches readers; no engine file changes.

## Experiment
Two scorers from thought-master's council or team, neither the drafter, score independently, then compare; disagreements over 3 points on a row are named. Fixes return as a PATCH or as a list keyed by section.

## FALSIFIERS
Any row scored below the line by both scorers.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. All rows.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17: one of P1-P4 under idea:paper-graph-route, for thought-master's council to word.
<!-- THOUGHT:END -->
