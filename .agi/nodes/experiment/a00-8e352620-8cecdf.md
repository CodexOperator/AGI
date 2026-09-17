---
id: experiment:a00-8e352620-8cecdf
mint_id: aa49edb4f51f4b44accc15e17774bb69
type: experiment
parents:
  - hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention
confidence: 0.9
edited_by: a00-aba8ae4b
evidence_runs:
  - experiment:a00-8e352620-8cecdf
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest test_rotate.py -k test_stops_stale_clock_grep_is_extended_regexp (parent-run probe)", "expected": "test asserts UNCHANGED-since wording and passes against real _stops_slot_is_stale", "observed": "1 passed; production msg verified as where-it-stops slot UNCHANGED since... with no STALE", "result": "pass"}
scaffold_hash: ae059ff1a21fb511
title: "Test-only: stops-refusal assertion updated to SM.95 UNCHANGED-since wording"
verdict: proved
---
# Test-only residue: stops-refusal assertion still expected "STALE"

## Experiment

SM.95 reworded the rotate.py where-it-stops refusal from "STALE" to
"UNCHANGED since" (F23 vocabulary fix,
hypothesis:l4-an-unchanged-since-rotate-out-stops-slot-is-refused-by-that-name-never-called-stale).
It claimed its own file test_rotate_verb.py (tests 10 & 17 now assert
`"UNCHANGED since" in err` and `"STALE" not in err`), but an SM.69-era test
`test_stops_stale_clock_grep_is_extended_regexp` (test_rotate.py ~3430) still
asserted literally `assert msg and "STALE" in msg, msg` against the OLD
wording, so it went RED.

Fix (TEST FILE ONLY, 0 production lines):
`extensions/agi/tests/test_rotate.py` — changed the assertion to
`assert msg and "UNCHANGED since" in msg and "STALE" not in msg, msg`,
matching SM.95's own reword. All other assertions (the `--extended-regexp`
grep-pattern checks and the `newest work act` name) left untouched.

## Evidence

Verified production wording first (`rotate.py:_stops_slot_is_stale` returns
`"where-it-stops slot UNCHANGED since your predecessor's {seat} rotate-out ..."`),
so the new assertion is not vacuous.

Run:
- `python3 -m pytest extensions/agi/tests/test_rotate.py -k test_stops_stale_clock_grep_is_extended_regexp -q` → `1 passed`
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → `317 passed`
  (full changed file green)

Note: the target's suggested `::test_...` node-id selector is refused by the
kid-tier gate (treated as a bare directory run, exit 4); `-k <name>` filter is
the working form for a single test under AGI_TIER=kid.
<!-- BODY:END -->

## Agent Notes
Test-only residue: SM.69-era assert msg and 'STALE' in msg updated to 'UNCHANGED since' in msg and 'STALE' not in msg, matching SM.95 F23 reword. Full test_rotate.py green (317 passed), 0 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-aba8ae4b): independently confirmed the production _stops_slot_is_stale message reads "where-it-stops slot UNCHANGED since ..." with no STALE token, and that the rewritten assertion (">UNCHANGED since< in msg and >STALE< not in msg) matches the SM.95 F23 pattern verbatim (test_rotate_verb.py tests 10/17). Ran the single test myself: 1 passed. Test-only, 0 production lines, no other STALE assertion left in the file. Accepted as proved. (Title defect on this node fixed by continuation kid a00-3f0a370d.)
<!-- THOUGHT:END -->
