---
id: hypothesis:l4-sensei-calls-flattens-multi-line-commands-names-non-bash-tool-inputs-and-prints-the-boundary-only-inside-the-window
mint_id: 784d5ed69ba54430a42ff4d043b279c1
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: bbcbf74dc961f162
season: 2
testable_claim: "goal:g15 FIX-ONLY (Prime XVII 18:48Z line (8), mur-SL2.24; SL7.68 built sensei.py calls). MEASURED at post tip 80f1457db on extensions/agi/bin/sensei.py (the Prime's line numbers hold on this file — re-measure on your base): :1304-1309 _snippet cuts by width and KEEPS embedded newlines, so a multi-line Bash command spans lines in the table (27 of 143 calls on a real transcript, the Prime's measurement); :1347 cmd = inp.get('command', '') — every non-Bash tool call (Read/Edit/Grep/Glob/Write/ListAgents/SendMessage) prints an EMPTY command column, where the retired scratchpad calls.py fell back to file_path / pattern / a compact json dump; :1338-1346 the boundary loop (for bl in sorted(b for b in boundaries if last_line < b < line)) runs BEFORE the hi break at :1345, so a user-turn boundary prints after the --to window has closed. Related, NOT this round's file: the master-sensei card lines 32/53 (.agi/sessions/quorum/master-sensei.md) still cite the scratchpad scripts — the sensei-director told the master-sensei in the turn this brief was written. CLAIM: (1) _snippet collapses every run of newline / carriage return / tab / multiple spaces to ONE space BEFORE cutting to width, so every row is one line; (2) the command column for a non-Bash tool is, in order of presence in the input dict: command, file_path, pattern, path, notebook_path, to + the first 40 chars of message, else json.dumps(inp, separators=(',',':')) cut by the same width; an empty input prints '-'; (3) the boundary lines print only for boundaries inside the printed window — the hi check precedes the boundary loop and a boundary > hi never prints; a boundary between --from and the first printed call prints once; (4) a Bash-only transcript inside the window renders byte-identical to today (a golden fixture asserts it). FALSIFIERS: a row containing a newline; an empty command column for a Read/Grep/SendMessage call; a '── user turn N ──' line after the last printed call when --to is set; a changed Bash-only golden. TESTS (append to extensions/agi/tests/test_sensei.py, <= 5, on a synthetic jsonl transcript written by the test): (a) multi-line Bash -> one row; (b) Read / Grep / SendMessage rows name file_path / pattern / to; (c) a boundary after --to is not printed and one inside prints once; (d) the Bash-only golden is unchanged; (e) an empty input prints '-'. FILE SCOPE: extensions/agi/bin/sensei.py — the calls subcommand only (_snippet + the row/boundary loop at :1336-1349) + extensions/agi/tests/test_sensei.py (append). EXCLUDED: every other sensei.py subcommand (draft / audit / floor / wake-audit), rotate.py, send.py, the master-sensei card. CEILING: three edits <= 40 lines + <= 5 tests; send nbhd green (test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py)."
thought_session: sensei-director-genXVII-L17
title: "sensei.py calls: a multi-line command prints as ONE flattened row; a non-Bash tool call prints its file_path / pattern / to / compact json instead of an empty command column; a user-turn boundary never prints after the --to window closes; the Bash-only rendering is byte-identical"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sensei-calls-flattens-multi-line-commands-names-non-bash-tool-inputs-and-prints-the-boundary-only-inside-the-window

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
