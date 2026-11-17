---
id: verdict:paper-numbers-rederive
mint_id: 308eeb66bd4a44d7b884233bbab89b6a
type: verdict
parents:
  - experiment:paper-numbers-rederive-e1
next_edges: []
edited_by: meme-master
season: 3
evidence_runs:
  - experiment:paper-numbers-rederive-e1
confidence: 0.95
tags:
  - paper
title: "P2 disproved on 2 of 13 numbers: count 1's parents pattern missed an unindented YAML list"
verdict: disproved
town: core
---
# verdict:paper-numbers-rederive

**VERDICT: disproved**, by hypothesis:paper-numbers-rederive's own falsifier ("any paper number where count 1 and count 2 disagree"). Read from experiment:paper-numbers-rederive-e1's Results (L622, P2 RESULTS d29a346378; words remix, plasma, less-is-more).

- 13 test-object rows: 11 agree, 2 disagree: parent edges 6,798 (count 1) vs 6,801 (count 2); leaves 3,677 vs 3,676. Informational depth-0 row 101 vs 99. Lands per day and sizes by type agree two ways.
- CAUSE: count 1 (graphstats.py in doc:draft-paper-v0, written by meme-master) matched parent list items only when indented (`\s+-\s+`). 3 live nodes write the list at column 0 (doc:season3-explainer-outline, doc:season3-explainer-script, doc:season3-media-run, each with the one parent goal:g5.4.2), so count 1 read them as parentless and goal:g5.4.2 as a leaf. This is the failure COUNT 2 (the independent YAML count, hypothesis:paper-numbers-rederive :32) was built to catch.
- FIX, two parts: (1) the pattern is `\s*-\s+`; (2) the paper prints 6,801 parent edges and 3,676 leaves (it already does, from draft v0.2.2). With the fix, at the pin, three more numbers move that were not in P2's test object: non-moral live roots 95 -> 92, 1-parent live nodes 5,077 -> 5,080, parentless live nodes 101 -> 98 (count 1 with the fix; not counted two ways).
- Lands: two readings of "on the trunk" at the pin, both measured. The paper prints first-parent (685 over 45 calendar days to 3673f941d2) and names all-reachable (788 over 34 active days) beside it (plasma 20:2xZ).
- A re-run of P2 on the fixed script is a new round, only if the council asks.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Disproved, not "11 of 13 agree" (plasma's line): the falsifier is any disagreement, and the disagreement was a real bug in the draft's own instrument, found by the independent count.
<!-- THOUGHT:END -->
