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
<!-- THOUGHT:END -->
