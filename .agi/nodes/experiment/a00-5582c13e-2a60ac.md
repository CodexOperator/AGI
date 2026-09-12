---
id: experiment:a00-5582c13e-2a60ac
mint_id: 077220c108f84ba1903133bd9eb085f4
type: experiment
parents:
  - hypothesis:l4-sensei-calls-flattens-multi-line-commands-names-non-bash-tool-inputs-and-prints-the-boundary-only-inside-the-window
next_edges: []
confidence: 0.95
edited_by: a00-584b7e7a
evidence_runs:
  - experiment:a00-5582c13e-2a60ac
loop: hypothesis:l4-sensei-calls-flattens-multi-line-commands-names-non-bash-tool-inputs-and-prints-the-boundary-only-inside-the-window@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 457af2197f56bae3
season: 2
title: A00 5582c13e 2a60ac
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5582c13e-2a60ac

## Experiment

FIX-ONLY round for goal:g15 claim on `extensions/agi/bin/sensei.py` calls
subcommand (parent hypothesis:l4-sensei-calls-flattens-multi-line-commands-...).
Measured the pre-fix defect in the current tree, implemented the claim, and
proved it on the built bytes with tests appended to test_sensei.py.

Pre-fix (read from the tree before editing):
- `_snippet` (was :1304-1309) cut by width and KEPT embedded newlines, so a
  multi-line Bash command produced several table rows.
- `cmd = inp.get("command", "")` (:1347) sent every non-Bash tool call to an
  EMPTY command column.
- the boundary loop (:1338-1346) ran BEFORE the `hi` break (:1345), so a
  user-turn boundary after the --to window could print.

Changes (extensions/agi/bin/sensei.py):
1. `_snippet` now collapses every whitespace run (`" ".join(str(cmd).split())`)
   BEFORE cutting, so every row is one line.
2. new `_display_cmd(inp)` resolves the command column in order of presence:
   command, file_path, pattern, path, notebook_path, `to` + first 40 chars of
   `message`, else `json.dumps(inp, separators=(',',':'))`; an empty input
   prints `-`. Wired into the row print in `cmd_calls`.
3. the `if hi is not None and n > hi: break` now precedes the boundary loop,
   so a boundary after the printed window never prints.

## Evidence

`python3 -m pytest extensions/agi/tests/test_sensei.py -q` -> 15 passed (10
existing + 5 new: a=multi-line Bash -> one row; b=Read/Grep/SendMessage name
file_path/pattern/to and empty->'-'; c=boundary after --to never prints and the
inside one prints once; d=Bash-only golden byte-identical; e=empty input prints
'-'). Full neighbor suite (test_sensei/test_send/test_seatsig/test_heal/
test_bin_help_smoke/test_write_self_row) -> 403 passed, 3 skipped.

Live demonstration (cmd_calls on a synthetic 3-call transcript, --to 2, width 40):
```
1 · 2026-09-12T00:00:01Z · Bash · cat a.txt sleep 2 pwd      <- multi-line flattened to ONE row
── user turn 1 ──
2 · 2026-09-12T00:00:03Z · Read · a.txt                      <- names file_path, no empty column
```
User turn 2 (before call 3) does NOT print because --to closed the window at 2.
All four falsifiers eliminated: no newline row, no empty Read/Grep column,
no boundary past --to, Bash-only golden unchanged (explicit equality assert in
test_calls_d).

## Agent Notes
sensei.py calls: multi-line command flattened to one row, non-Bash tool_use names file_path/pattern/to/json (empty->'-'), boundary past --to never prints; 403 nbhd tests green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-584b7e7a, SL7.95): accepted proved. (1) INSTRUCTION, quoted from testable_claim: (1) _snippet collapses every run of newline / carriage return / tab / multiple spaces to ONE space BEFORE cutting to width; (2) the command column for a non-Bash tool is, in order of presence, command, file_path, pattern, path, notebook_path, to + first 40 chars of message, else json.dumps; empty input prints -; (3) the boundary lines print only inside the window; (4) Bash-only output byte-identical. (2) MECHANISM: read the actual diff (extensions/agi/bin/sensei.py) rather than the report — _snippet now does " ".join(str(cmd).split()) before the width cut (:1304-1317); new _display_cmd resolves the ordered keys and returns "-" for an empty dict, json.dumps(inp,separators=(",",":")) otherwise; cmd_calls now tests `if hi is not None and n > hi: break` BEFORE the boundary loop (:1366-1369), so no boundary can print past --to. All three defects measured pre-fix on this tree were present and are gone. (3) NEAR MISS: a kid could have collapsed whitespace only AFTER the width cut — that still emits a row whose visible length differs from width and whose tail is a newline fragment; or it could have left the boundary loop where it was and merely moved the break after the print — the boundary STILL prints before the check either way. Both satisfy a loose reading of (1)/(3) and lose the mechanism. Tests (a) and (c) pin exactly those, so the near miss is falsified. (4) INDEPENDENT RUN: 15 passed in test_sensei.py, 388 passed / 3 skipped across test_send/test_seatsig/test_heal/test_bin_help_smoke/test_write_self_row (403 total, matches the node body). Evidence_runs=self; parents resolves to the target hypothesis. No scope violation: only sensei.py calls + test_sensei.py touched.
<!-- THOUGHT:END -->
