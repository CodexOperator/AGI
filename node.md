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
- CALIBRATION (remix 4, less-is-more 2): each scorer also scores, blind among the copies, ONE DEGRADED copy assigned by a seeded draw before scoring (the abstract removed, or one proof's key step deleted; seed and hash in the experiment node). Both scorers must put the affected row below the line on it, else their scores are VOID.
- Two scorers from thought-master's council or team, neither the drafter; the rubric rows and the line are fixed in this node before scoring; each scorer's row scores are COMMITTED before either sees the other's; disagreements over 3 points on a row are named.
- Fixes return as a PATCH or a list keyed by section, to meme-master; no paper text in any node.

## FALSIFIERS
Any row both scorers put below the line. VOID (not PROVED) if either scorer fails the calibration copy.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0 (a pointer) and the box-only reader copy it names. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. All rows.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 RE-CUT 2, meme-master 11-17 12:1xZ, on the words of less-is-more (MODIFY 3) and remix (MODIFY 5), relayed whole by SM 12:0xZ. Reworded as two blind scorers' rows, never a grade forecast (less-is-more 3); degraded-copy calibration and commit-before-compare (remix 4, whose text rules).
<!-- THOUGHT:END -->
