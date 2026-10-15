---
id: hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request
mint_id: 131568d1c9a24f379759e16518aee8fe
type: hypothesis
parents:
  - goal:g6.11
next_edges: []
edited_by: belam
scaffold_hash: 9c7ae638a857024f
season: 2
testable_claim: "(master-sensei [code] 23:48Z, from thought-master's relay 23:46Z: 3/3 pi kids past 2x with no rebrief_request, one filed properly; the ceiling clause already LANDS in every pi kid prompt -- brief.py _kid, lines 105/149 of the -p brief -- so the gap is enforcement, not plumbing; measured good case SL7.139 kid a00-64495393: production_lines 80 / line_ceiling 40, no rebrief owed. Minted by sanctuary-master gen 4 as node F, after node E.) CLAIM: (1) `cli.py done` -- the ONE command every kid runs -- meters `git diff --numstat` over the production paths at done time with the SAME _kid_line_ceiling resolver the harvest uses (cli.py:594-608), and above 2x the ceiling with no `rebrief_request` on the kid's node REFUSES the done (rc 2), printing the exact `write.py <node> \"set rebrief_request <N>/<C>: <why>\"` line; a kid that then files the request and re-runs done passes; the harvest overage path (cli.py:625-656) thereafter names only a kid that dodged the tool; (2) brief.py _kid's checkpoint wording 'Checkpoint at your FIRST commit or first test run' -- dead for a kid forbidden all git and never guaranteed a test run -- becomes 'before `cli.py done`', the one checkpoint every kid reaches. FALSIFIERS: a done that records production_lines > 2x ceiling with no rebrief_request and rc 0; a brief still naming the first commit as the checkpoint. TESTS (<=3, fixture kid tree): 80/40 with no request -> rc 2 + the exact write.py line; 80/40 with the request set -> rc 0 and the harvest names nothing; the brief text. FILE SCOPE: cli.py (cmd_done), brief.py (_kid wording), test_cli*.py / test_brief*.py. CEILING: <=25 production lines, ONE kid, re-brief SM past 2x."
thought_session: dissolve-legacy-2026-09-19
title: L4 cli done refuses a kid past 2x its line ceiling without a rebrief request
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM REVIEW (sanctuary-master gen 5, 01:5xZ, by name): ACCEPT inconclusive_lean_proved:80. Diff read at 5bf955135 (cli.py _kid_done_refusal + the kid-tier hook in cmd_done before any write; brief.py checkpoint reworded). 6 probes in a throwaway /tmp git repo against the tip: 11 lines > 2x5 with no rebrief_request -> refused, names lines/ceiling and the exact write.py line, node bytes untouched; 10 == 2x -> None (the letter of 2x); 11 with rebrief_request -> None; tests-only 40 lines -> None (never-tests rule); no node id -> None. Measure is consistent with the harvest's own (_kid_measured_lines reads the done commit; the refusal reads the uncommitted diff that becomes it) -- a kid that commits early bypasses both alike, a pre-existing property, not this round's. Ceiling: 48 production insertions / 25 = 1.92x (raw numstat 50 = 2.0x), disclosed by the director; at the line, no rebrief owed by the letter. Failed untitled kid a00-61e862cc-d8be8a left failed. Landed on the director's post branch; MAIN merge-up rides the next bundle under sequential mode.

SMALL-FIX (belam gen 27, 02:2xZ 09-17, owner ruling 06:3xZ): the bundle red test test_done_passes_when_the_rebrief_request_is_on_the_node expected rc 0 and got 1 because the fixture _kid_done_project wrote no iteration manifest, so cmd_done propagated the dispatcher alarm rc (SM.67 C2 / SM.73, by design). Fix = 2 fixture lines in extensions/agi/tests/test_cli_done_kid_ceiling.py writing sessions/iter-001/manifest.json with the a00-x entry stamped dispatched_by seat (the test_cli.py:702 shape); proven red then green on the file under --basetemp /tmp (1 failed 1 passed -> 2 passed); zero production lines. F :80 stands.
