---
id: experiment:a00-ec12a41e-f4356d
mint_id: ddf695b0c8994852a074e55b1b139645
type: experiment
parents:
  - hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span
next_edges: []
confidence: 0.95
edited_by: a00-32df852f
evidence_runs:
  - experiment:a00-ec12a41e-f4356d
loop: hypothesis:l4-trimguard-never-reads-a-closing-quote-as-an-open-span@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5b89577c2534178d
season: 2
title: A00 ec12a41e f4356d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ec12a41e-f4356d

## Experiment

Hypothesis `l4-trimguard-never-reads-a-closing-quote-as-an-open-span` claims
the open-ended-quote regex in `cmd_trimguard` (cli.py) reads the CLOSING
quote of a closed span as an OPEN span when 25+ non-quote chars follow it to
end of line, minting a phantom span that falsely ABORTs the trim.

**Reproduced at HEAD (914b68251) before any edit:**
```
env -u TMUX -u TMUX_PANE python3 extensions/agi/bin/cli.py trimguard
§6 lines 135-151  bytes=2557  real quoted spans: 2
  MISSING  ', verbatim in `doc:l4-owner-decisions`): $26.52 of $132'
ABORT: 1 owner quote(s) resolve in NO node.   (exit 1)
```
Root cause confirmed: `[\"“]([^\"“”\n]{25,})$` (re.M) matched the CLOSING
quote of the closed span `"keep using pi rounds till done"` on HANDOFF §6
item 106, because that quote is the last quote on its line and 34 non-quote
chars follow it. Only ONE real 25+ char double-quoted span exists in the live
§6; the printed "2" was that real span plus the phantom.

**Fix — replace the two independent regex passes with one quote-parity walk:**
refactored span extraction into pure `_collect_owner_spans(sec)`, which walks
each line left to right: a quote opens a span, the next quote closes it
(closed span captured), and a quote with no close before end of line is an
open span. An open span can therefore only START at a real opening quote —
never at a quote the walk already consumed as a CLOSING quote. This preserves
the "a real unclosed quote still aborts" behaviour while killing the phantom.

**Result after fix (same real HANDOFF.md at HEAD):**
```
§6 lines 135-151  bytes=2557  real quoted spans: 1
OK: all 1 owner quotes resolve in .agi/nodes/ — safe to collapse.   (exit 0)
```
The guard now PASSes on the live section with no phantom.

## Evidence

Tests added: `extensions/agi/tests/test_cli_trimguard.py` (4 hermetically
drive the span decision via `_collect_owner_spans`):
- closed span + 25+ trailing chars (exact item-106 shape) → only the real
  closed span, no phantom;
- a real unclosed quote of 25+ chars → still reported (abort preserved);
- a line with two closed spans → both reported;
- the live HANDOFF §6 at HEAD → exactly 1 closed span, 0 open spans.

```
env -u TMUX -u TMUX_PANE python3 -m pytest test_cli_trimguard.py -q
4 passed
env -u TMUX -u TMUX_PANE python3 -m pytest test_cli.py test_cli_trimguard.py -q
23 passed
```

The suite-level gate ("run a targeted path, not a bare directory") held:
named test files, never the bare directory.

## Agent Notes
trimguard false-ABORT fixed: replaced open-ended regex with one quote-parity walk (_collect_owner_spans); phantom closing-quote-as-open span killed, real unclosed quotes still abort, live HANDOFF §6 now PASSes (1 real span, 0 phantom). 4 new hermetic tests + existing cli tests green (23 passed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-32df852f, L4.297) — kept at proved.

WHAT THE INSTRUCTION SAID. The hypothesis's claim (1): an open-ended span starts only at a quote that is NOT the closing quote of a matched closed span (consume the closed spans first and scan the remainder, or track quote parity per line). Claim (4): run the guard against the REAL HANDOFF.md at HEAD and paste the result.

WHAT THE MACHINE ACTUALLY DOES. I ran the artifact myself, not the report. `env -u TMUX -u TMUX_PANE python3 extensions/agi/bin/cli.py trimguard` at HEAD with the kid's diff applied prints `§6 lines 135-151 bytes=2557 real quoted spans: 1` then `OK: all 1 owner quotes resolve in .agi/nodes/ — safe to collapse.` exit 0. Pre-fix the same command printed the phantom `MISSING ', verbatim in \`doc:l4-owner-decisions\`): $26.52 of $132'` and ABORT exit 1. cli.py:1878 `_collect_owner_spans` walks each line and consumes a quote pair before it can ever be read as an opener, exactly the parity claim. I independently listed every >=25-char quoted span in HANDOFF.md:135-151 with grep/awk and found exactly ONE real span, `keep using pi rounds till done` — so the pre-fix printed `2` was one real span plus one phantom, and the post-fix `1` is the whole real §6. Tests: `python3 -m pytest extensions/agi/tests/test_cli_trimguard.py extensions/agi/tests/test_cli.py -q` -> 23 passed, including the four hermetic cases the claim demanded (item-106 shape, real unclosed quote still aborts, two closed spans, live §6 has no open span).

NEAR MISS. A fix that only excluded the exact item-106 string, or that special-cased the closing-quote position for one line shape, satisfies the words of claim (1) and loses the mechanism — it would still phantom on any other closed span followed by 25+ trailing chars. The kid instead replaced both regex passes with one parity walk, which is the general instrument the claim named as the alternative. The other near miss: dropping the open-ended pass entirely, which would have silenced the false ABORT but also killed claim (2) — the walk keeps a true unterminated span reportable, and the test pins it.

DEVIATION. None from a standing rule. No engine behaviour outside cmd_trimguard changed; the only addition is the pure helper plus its test file named in the hypothesis scope.

CAVEAT I AM RECORDING RATHER THAN PENALISING. The parity walk applies the archived-marker strip to the whole line before extraction instead of to the captured span text; for every line shape in the live §6 this is equivalent, and the live guard and the tests pass, but it is a widening of the strip's surface that no test pins. Left as a note, not a demotion: the claim's four acceptance cases all hold on bytes I ran.
<!-- THOUGHT:END -->