---
id: hypothesis:paper-numbers-rederive
mint_id: 6e12b6fe0bad4ac6aac6d193666ef1f6
type: hypothesis
parents:
  - idea:paper-graph-route
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
  - paper
title: "Every number in the class paper draft re-derives from the graph by a committed script"
testable_claim: "Every number in the data table and text of doc:draft-paper-v0 that comes from the graph is reproduced, to the stated precision, by running graphstats.py (in the doc) at a named commit; no number in the paper is unsourced."
confidence: 0.6
town: core
---
# hypothesis:paper-numbers-rederive

## Measured
graphstats.py at d7985199d4 (11-17): 5,889 live / 255 retired; 6,797 parent edges; depth max 20, mean 5.47; ancestor set mean 9.38, median 9, p95 16, max 41; 1 cycle (hyp:a00-ddbe3410-iterative-traversal <-> exp:a00-ddbe3410-exp003-iterative-traversal); 66 dangling parent refs; 95 non-moral roots; commits since 2026-04-30: 26,417.

## CLAIM
Every number in the data table and text of doc:draft-paper-v0 that comes from the graph is reproduced, to the stated precision, by running graphstats.py (in the doc) at a named commit; no number in the paper is unsourced.

## Dispatch line
config-max: none / template-max: none / code: none. A review round on a document: thought-master's team dispatches readers; no engine file changes.

## Experiment
Run the script at the named commit and at the current trunk tip; compare every number; read the script for definitional errors (what counts as live, a root, an edge; the legacy type prefixes exp/hyp and quoted ids). A finding is a table: number, paper value, re-run value, cause.

## FALSIFIERS
Any number that does not reproduce at the named commit, or a definition in the script that does not match the paper's words.

## TESTS
The paper builds (tectonic, in meme-master's scratch) after any PATCH is applied; P1-P2 findings carry their recomputation.

## FILE SCOPE
Read: doc:draft-paper-v0. Write: one experiment node + a verdict per finding set; findings as a PATCH or table in the experiment body. Never the owner's private files.

## CEILING
Readers only; no USD spend beyond the team's normal allowance; local or allowed models per the owner's standing rules. Rubric rows hit: Development of Ideas (15), Shows Understanding (15).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17: one of P1-P4 under idea:paper-graph-route, for thought-master's council to word.
<!-- THOUGHT:END -->
