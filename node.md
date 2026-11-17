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
title: "Two blind scorers put every row of the owner's rubric at or above the line on the class paper draft"
testable_claim: "Two blind scorers, neither the drafter, each put every 15-point row of the owner's rubric at or above 12 and the abstract and conclusion at or above 4, on doc:draft-paper-v0's reader copy, with a one-line reason per row and a concrete fix for any row below the line. This is NOT a forecast of the owner's grade."
confidence: 0.6
town: core
---
# hypothesis:paper-meets-rubric

## Measured
Rubric (owner, 11-17): Appropriate Topic (Mathematical Depth) 15; Abstract 5; Clarity (organized, visually easy to follow, correct grammar and mathematical notation) 15; Development of Ideas (appropriate background discussion, examples when necessary) 15; Support for Main Ideas (necessary definitions, theorems, examples) 15; Sense of Problem Solving Process (uses definitions and theorems correctly, correct overall logic) 15; Shows Understanding of Overall Topic (big picture clear, pieces fit together) 15; Conclusion 5; Total 100.

## CLAIM
Two blind scorers, neither the drafter, each put every 15-point row of the owner's rubric at or above 12 and the abstract and conclusion at or above 4, on doc:draft-paper-v0's reader copy, with a one-line reason per row and a concrete fix for any row below the line. This is NOT a forecast of the owner's grade.

## Dispatch line
config-max: none / template-max: none / code: none. A review round on a document: thought-master's team dispatches readers; no engine file changes.

## Experiment
- CALIBRATION (remix 4, less-is-more 2, plasma 2): each scorer also scores ONE DEGRADED copy, the degradation drawn by seed before scoring (seed and hash in the experiment node) from: one proof's key step deleted, or a definition used before it is given. NOT "abstract removed" (any scorer marks a missing section low, so it cannot catch a lenient one). The row it must drop is named here before scoring: Sense of Problem Solving Process. Each copy is scored in a SEPARATE context, order seeded, never two copies in one context (that tests diff-spotting, not calibration). A scorer who does not put that row below the line on the degraded copy has their scores VOID.
- Two scorers from thought-master's council or team, neither the drafter; the rubric rows and the line are fixed in this node before scoring; each scorer's row scores are COMMITTED before either sees the other's; disagreements over 3 points on a row are named.
- Fixes return as a PATCH or a list keyed by section, to meme-master; no paper text in any node.

## FALSIFIERS
Any row EITHER scorer puts below the line (plasma 1: a split row is a DISPROVED for that row, never left unread). VOID (not PROVED) if either scorer fails the calibration copy.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0 (a pointer) and the box-only reader copy it names. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. All rows.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 RE-CUT 3, meme-master 11-17 12:4xZ, on plasma (gen 2) MODIFY 3 + 2 notes (relayed whole by SM 12:3xZ); remix APPROVE on re-cut 2. Falsifier covers a split row (either scorer below = DISPROVED); calibration drops "abstract removed", names the row, separate contexts (plasma 1, 2).
<!-- THOUGHT:END -->
