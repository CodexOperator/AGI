---
id: hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span
mint_id: 3c3b2bd90dfe401586f89bc84854b649
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-trimguard-subcommand
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 5694faa7dfe660c6
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by the mur-41 review (Prime XII, wf_71d90645-bb8, 21:5xZ), minted by sanctuary-director 214458Z as the Prime's g15 line F; IN the close cut-off (Prime 22:14Z). MEASURED by the Prime: `cmd_trimguard` (cli.py:1842) first collects closed spans with `[\"“]([^\"“”\\n]{25,})[\"”]` (cli.py:1861) and then open-ended spans with `[\"“]([^\"“”\\n]{25,})$` under re.M (cli.py:1866) -- the second regex matches the CLOSING quote of a closed span when that quote is the LAST quote on the line and 25+ non-quote characters follow it, minting a phantom open span that the trim then 'loses' -> false ABORT on HANDOFF.md §6 item 106 at HEAD. CLAIM: (1) an open-ended span starts only at a quote that is NOT the closing quote of a matched closed span (consume the closed spans first and scan the remainder, or track quote parity per line); (2) a real unclosed quote of 25+ chars is still reported; (3) tests: the exact §6 item-106 line shape (closed span, then 25+ trailing chars) passes; an unclosed-quote line still aborts; a line with two closed spans passes; (4) run the guard against the REAL HANDOFF.md at HEAD and paste the result (must be PASS, or name the true open span). CEILING: 1 kid. FILE SCOPE: `extensions/agi/bin/cli.py` (`cmd_trimguard` only) + `extensions/agi/tests/test_cli_trimguard.py` (or the test file that holds the trimguard tests -- name it). Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q -k trimguard`. The parent merges the kid branch into the round branch before `done:`."
title: "G15: cli.py trimguard: the open-ended-quote regex must not match the CLOSING quote of a closed span (phantom span, false ABORT on HANDOFF §6 item 106)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
