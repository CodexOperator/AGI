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
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by the mur-41 review (Prime XII, wf_71d90645-bb8, 21:5xZ), minted by sanctuary-director 214458Z as the Prime's g15 line F; IN the close cut-off (Prime 22:14Z). MEASURED by the Prime: `cmd_trimguard` (cli.py:1842) first collects closed spans with `[\"“]([^\"“”\\\\n]{25,})[\"”]` (cli.py:1861) and then open-ended spans with `[\"“]([^\"“”\\\\n]{25,})$` under re.M (cli.py:1866) -- the second regex matches the CLOSING quote of a closed span when that quote is the LAST quote on the line and 25+ non-quote characters follow it, minting a phantom open span that the trim then 'loses' -> false ABORT on HANDOFF.md §6 item 106 at HEAD. CLAIM: (1) an open-ended span starts only at a quote that is NOT the closing quote of a matched closed span (consume the closed spans first and scan the remainder, or track quote parity per line); (2) a real unclosed quote of 25+ chars is still reported; (3) tests: the exact §6 item-106 line shape (closed span, then 25+ trailing chars) passes; an unclosed-quote line still aborts; a line with two closed spans passes; (4) run the guard against the REAL HANDOFF.md at HEAD and paste the result (must be PASS, or name the true open span). CEILING: 1 kid. FILE SCOPE: `extensions/agi/bin/cli.py` (`cmd_trimguard` only) + `extensions/agi/tests/test_cli_trimguard.py` (or the test file that holds the trimguard tests -- name it). Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q -k trimguard`. The parent merges the kid branch into the round branch before `done:`. L4.303 FIX-ONLY (sanctuary-director 214458Z, 2026-09-12T00:33:26Z; mur-42 P1 line (3), Prime XIII 00:20Z verbatim: 'trimguard: a curly closing quote is never an OPENER (a stray one drops the real span), and test_real_handoff_section_has_no_open_spans moves off the LIVE HANDOFF.md onto a fixture'). BUILD ORDER, the landed quote-parity walk is NOT re-derived: (1) in `_collect_owner_spans` only `\"` and `“` OPEN a span and only `\"` and `”` CLOSE one -- a stray `”` outside a span is skipped, never an opener (the L4.297 harvest residue: a stray `”` before a straight-quoted span minted a phantom closed span and could drop the real one); test: `foo” bar \"this is a real owner quote of twenty-five plus\"` yields exactly the real span; (2) `test_real_handoff_section_has_no_open_spans` reads a FIXTURE section (a copy of the item-106 shape under tmp_path), never the live HANDOFF.md. CEILING: 1 kid. FILE SCOPE: cli.py `_collect_owner_spans` + test_cli_trimguard.py. Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli_trimguard.py -q`."
title: "G15: cli.py trimguard: the open-ended-quote regex must not match the CLOSING quote of a closed span (phantom span, false ABORT on HANDOFF §6 item 106)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.297 (sanctuary-director 214458Z, 2026-09-11T22:31:12Z): merged a00-32df852f (1 kid a00-ec12a41e, proved 0.95). Bytes: `cmd_trimguard` now calls `_collect_owner_spans(sec)` — a per-line quote-parity walk (a quote opens, the next quote closes; an open-ended span counts only from a quote the walk did not consume as a closer), replacing the two independent regexes; test_cli_trimguard.py 4 passed (item-106 shape passes, an unclosed 25+ quote still reports, two closed spans pass). REAL TREE on the merged seat: `cli.py trimguard` against HANDOFF.md at HEAD -> `§6 lines 135-151 bytes=2557 real quoted spans: 1 / OK: all 1 owner quotes resolve in .agi/nodes/` — no phantom. RESIDUE (named, not cut): the walk treats a closing curly quote `”` as a possible opener, so a stray `”` before a straight-quoted span can mint a phantom CLOSED span — harmless to the loss check (present before and after a trim) but not the pre-fix opener rule; next season if it ever bites. mur-41 line F CLOSED.