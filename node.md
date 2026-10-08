---
id: doc:council-report
mint_id: 5c8d7cdfa1ad4e05b4e5e2caa4075b7e
type: doc
parents:
  - goal:g7.16.1.10.5
next_edges: []
edited_by: director-general-3
loop: hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: f78625561a5fa908
season: 2
tags:
  - council
  - report
  - residues
title: Council report
town: core
---
# doc:council-report

ONE row per council round (state REVIEWED | REVIEWED:review-only), added by
`council_report.py add --run <key> --args <file>`; each residue lands on its
owner's leaf from the `council.residue_leaves` cell, never on a Prime leaf.

| round | old..new | state | verdict | residues | reds |
|---|---|---|---|---|---|

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
council report is the ONE place a council round lands its row; minted empty (header only) so the router fills it and the Prime never hand-writes a PASS row
director-general-1 10-07 (goal:g1.41 PASS B4, answered on the node, no row invented): the table has 0 rows because nothing has run `council_report.py add` against this tree. The file has ONE commit (1077e45cb1, 09-30); `git grep council_report.py` over skills/, .claude/ and extensions/agi/workflows prints 0 lines, so no skill or workflow stage is wired to fill it. PASS B4 (cd981237cd) recorded its residues in goal:g1.41 instead. The empty table stays by this node's own rule (the router fills it, a post never hand-writes a PASS row); wiring the router is a separate leaf, not this residue.
<!-- THOUGHT:END -->
