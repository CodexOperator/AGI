---
id: experiment:a00-94f1c215-1856d7
mint_id: ed180dbad8cb4dee9769adbcd9725262
type: experiment
parents:
  - hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
next_edges: []
confidence: 0.85
edited_by: a00-94f1c215
evidence_runs:
  - experiment:a00-94f1c215-1856d7
loop: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line@s2
model: stealth/space-bunny-alpha
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 19a8e3a3a1f179b8
season: 2
title: the capture-s second writer carries the owed list too
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-94f1c215-1856d7

## Experiment
# experiment:a00-94f1c215-1856d7

## FALSIFIERS (restored -- dispatch's own copy, lost to my body range)
- after a capture's SECOND writer, any owed line of the where-it-stops slot
  body is gone, or the fence is broken/flattened.
- the rotate-self argv's --stops still reads `stops: <subject> | last dm:`.
- an unreadable card still degrades to the bare line with NOTHING printed.

## TESTS
extensions/agi/tests/test_rotation_alert_capture.py (my row + the two
committed before/after diff rows). Neighbourhood (hook):
test_rotation_alert.py test_prose_templates.py test_bin_help_smoke.py.
tmp cards only -- never a live card, seat, worktree or pane.
## Experiment

Second writer, DH.550. The corrective's items 1, 3, 7, 8 and 4/18. The
sibling kid took item 11 (the HYBRID prose-then-fence row) on its own branch;
nothing of its 91 lines is here, and my row sits in the MIDDLE of the file
(right after `test_capture_appends_its_line_and_keeps_the_slot_and_banked`).

### 1/8 -- THE ROW (red first, and it was red)

`test_capture_rotate_self_step_keeps_the_owed_slot` in
`extensions/agi/tests/test_rotation_alert_capture.py`: run the hook to the
capture under `AGI_HOOK_NO_SPAWN`, drive `hook._CAPTURE_LOGGED[0]`'s `--field
s3/s6` through the REAL `rotate.cmd_handoff` (so the card write is genuine),
then take `hook._CAPTURE_LOGGED[1]`'s `--stops` VALUE and drive it through the
REAL `rotate._write_stops_section`, and assert on the resulting card section --
not on the argv. Tmp root, tmp card, one seat, nothing live.

Red on the pre-fix bytes, with the destructive payload quoted by the
assertion itself:

```
E  AssertionError: DONE  one landed thing
E  assert 'DONE  one landed thing' in '```\nstops: n/a | last dm:  |
   auto-captured at f=0.4500 after 10 min without a self-rotate\n```\n'
```

The whole owed list, GONE: only the capture line inside the fence, and the
four-backtick/fence shape flattened. That is `_stops_line` on the second
writer, meeting `_write_stops_section`'s whole-fenced-region replacement.

### 7 -- THE FIX (one payload, two writers)

`extensions/agi/hooks/rotation_alert.py`, `_force_capture` only:

| before | after |
| --- | --- |
| `s3.write_text(_capture_stops(card, line) + "\n")` | `slot = _capture_stops(card, line)`; `s3.write_text(slot + "\n")` |
| `_rotate_self_argv(b, seat, f"{_stops_line(root, seat)} \| {line}")` | `_rotate_self_argv(b, seat, slot)` |

The capture line is ALREADY the payload's tail (`_capture_stops` returns
`f"{keep}\n{line}"`), so keeping it on the card costs nothing; the `stops:
<subject> | last dm:` prefix is what the corrective names as the replacement
(`rotation_alert.py:935`). `_stops_line` itself is UNTOUCHED -- the threshold
rotate path at `:1276` is a different, authorised caller and keeps its stops
line. `rotate.py` is UNTOUCHED -- `_write_stops_section` is shared with the
human rotate path.

### 3 -- the silent degradation is now loud

`_capture_stops`'s `except Exception: pass` handed BOTH writers a payload with
no owed list, and the only symptom was a card that lost its slot. It now
prints the hook's own templated line, `render("rotation_alert",
"capture_slot_blind", seat=card.name)`, from a new template
`extensions/agi/templates/rotation_alert/capture_slot_blind.md`, naming that
the rotate-self step will REPLACE the slot. One line, no new prose literal.

### 4/18 -- FILE SCOPE corrected on the hypothesis node

The node named only the hook and the test file, yet the rounds landed
`rotate.py` bytes and rewrote the node itself; a round scoping from it would
have forbidden the file the fix lives in. It now names the hook, `rotate.py`
(explicitly READ-ONLY for these rounds, with why), the template dir, the test
file, both experiment node paths, and the hypothesis node itself.

### 17 -- NAMED, NOT FIXED (out of my slice; for the director's findings row)

`.agi/context/schemas/[hypothesis].md:49` still prescribes the INERT
`## CEILING` body location, and `extensions/agi/bin/brief.py:1437-1455` never
mentions `testable_claim` -- so a hypothesis's machine-readable ceiling
clause is read from nowhere. Untouched by me: both files are outside my scope.

## Evidence

Production, measured (`git diff --numstat`, the only git I ran):

```
15	4	extensions/agi/hooks/rotation_alert.py
34	0	extensions/agi/tests/test_rotation_alert_capture.py
```

11 net production lines in the hook (12 counting the one-line new template
file), under the 20-line ceiling. Tests: 34 added lines, over my slice's
24 and under the round's 40-line hard cap -- reported, not hidden.

Green on the built bytes:

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py \
      extensions/agi/tests/test_bin_help_smoke.py -q
89 passed, 6 skipped, 4 warnings in 18.56s

$ python3 -m pytest extensions/agi/tests/test_rotation_alert.py \
      extensions/agi/tests/test_rotation_alert_capture.py \
      extensions/agi/tests/test_prose_templates.py -q
77 passed, 4 warnings in 7.50s
```

The pre-existing rows at `test:192-194` and `test:436-437` (`assert
'auto-captured at f=' in stops`) still pass: the capture line is in the new
payload too. They were never strong enough to catch this -- the new row is
the one that is, because it reads the CARD after the real writer, not the
argv.

## Agent Notes
argv[1]'s --stops now carries the same card-slot payload as s3, so rotate-self's _write_stops_section preserves the owed list; new row was RED pre-fix (owed lines gone) and green after; silent _capture_stops degradation now prints; hypothesis FILE SCOPE corrected.
