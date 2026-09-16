---
id: hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request
mint_id: 131568d1c9a24f379759e16518aee8fe
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 9c7ae638a857024f
season: 2
testable_claim: "(master-sensei [code] 23:48Z, from thought-master's relay 23:46Z: 3/3 pi kids past 2x with no rebrief_request, one filed properly; the ceiling clause already LANDS in every pi kid prompt -- brief.py _kid, lines 105/149 of the -p brief -- so the gap is enforcement, not plumbing; measured good case SL7.139 kid a00-64495393: production_lines 80 / line_ceiling 40, no rebrief owed. Minted by sanctuary-master gen 4 as node F, after node E.) CLAIM: (1) `cli.py done` -- the ONE command every kid runs -- meters `git diff --numstat` over the production paths at done time with the SAME _kid_line_ceiling resolver the harvest uses (cli.py:594-608), and above 2x the ceiling with no `rebrief_request` on the kid's node REFUSES the done (rc 2), printing the exact `write.py <node> \"set rebrief_request <N>/<C>: <why>\"` line; a kid that then files the request and re-runs done passes; the harvest overage path (cli.py:625-656) thereafter names only a kid that dodged the tool; (2) brief.py _kid's checkpoint wording 'Checkpoint at your FIRST commit or first test run' -- dead for a kid forbidden all git and never guaranteed a test run -- becomes 'before `cli.py done`', the one checkpoint every kid reaches. FALSIFIERS: a done that records production_lines > 2x ceiling with no rebrief_request and rc 0; a brief still naming the first commit as the checkpoint. TESTS (<=3, fixture kid tree): 80/40 with no request -> rc 2 + the exact write.py line; 80/40 with the request set -> rc 0 and the harvest names nothing; the brief text. FILE SCOPE: cli.py (cmd_done), brief.py (_kid wording), test_cli*.py / test_brief*.py. CEILING: <=25 production lines, ONE kid, re-brief SM past 2x."
title: L4 cli done refuses a kid past 2x its line ceiling without a rebrief request
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
