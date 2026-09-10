---
id: experiment:a00-3480c19d-2c9906
mint_id: 851c0e08bf0245a791e0cadb9dc51e45
type: experiment
parents:
  - hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write
next_edges: []
confidence: 0.9
edited_by: a00-9f23c509
evidence_runs:
  - experiment:a00-3480c19d-2c9906
  - experiment:a00-51f3164a-10051e
loop: hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 024b4b0866f75115
season: 2
title: "Meter Repair L4.99: bare --pin refuses; --seat unaffected"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3480c19d-2c9906

## Experiment

Parent (hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write) is FIX-ONLY: the
mechanism half was already proved on disk (experiment:a00-51f3164a-10051e is
inconclusive_lean_proved:85) and this kid's whole job was falsifiers (a)–(h):
build the repair and prove the refusal hal for the claim "IDENTITY IS
SUPPLIED, NEVER INFERRED". Repair built in `rotate.py` ONLY as the parent
prescribed — in `resolve_transcript` and `cmd_meter`, never `find_pin_log`,
never weakening the `--seat` path.

**Two refuses, two seams (edits to `extensions/agi/bin/rotate.py`):**

1. READ side (`resolve_transcript` rule 3): when a SEATLESS read (seat=None)
   falls into the newest-mtime cross-agent pin search and the winner carries a
generation (written_gen is not None), it is ANOTHER agent's pin — the caller
never named it — so the resolver now returns `(None, "pin_unattributed")
   instead of a confident number. cmd_meter turns that into a loud refusal
   that names what supplies identity (`rotate.py meter --seat <NAME>` or
   `rotate.py meter --session-log <path>`). Legacy pins (bare path, no
   generation field — the record format that predates gen-stamping) keep the
   room-level semantics and are untouched.

2. WRITE side (`cmd_meter` pin block): a `--pin` may record ONLY a transcript
   the caller explicitly named (rule 1 `--session-log` or rule 2 `$AGI_SESSION_LOG`)
   or one a NAMED `--seat` attributes. When none is supplied the command
   REFUSES, non-zero, BEFORE anything is written, and the error NAMES the
   exact command including the `--session-log` path it needs. This is the gate
   that closes the adoption: a bare `--pin` can no longer adopt a foreign pin
   and re-stamp it with the caller's generation (the re-stamp that silenced
   seat_pin-stale).

Tests (a)–(f) added to `extensions/agi/tests/test_rotate.py`: (a) bare --pin
with the distractor present (caller's own pin FIRST and correct, foreign
`belam.meter` written LAST) REFUSES and leaves the caller's pin file
BYTE-UNCHANGED; (b) the refusal's stderr contains the literal string
`--session-log`; (c) --pin WITH explicit --session-log still writes, still
stamps the caller's generation, still prints the fraction; (d) $AGI_SESSION_LOG
alone still permits a pin write; (e) a bare seatless READ refuses when the pin
it would consult is another agent's generation-bearing pin; (f) --seat NAME
with a correct own-generation pin still reads and returns the fraction.

**Real-tree (h) — the shape no suite can see, on a dir with 24 real pins:**

```
$ rotate.py meter --pin /tmp/probe.meter; echo exit=$?
ERR: the newest pin a seatless read would consult belongs to another agent
(it carries an owner's generation) -- refusing ... --session-log <path> ...
exit=1                      # AND /tmp/probe.meter was NOT created
$ rotate.py meter --seat sanctuary-director; echo exit=$?
0.3701\t370107/1000000 tokens\tsource=seat_pin\tthreshold=0.47
exit=0                      # --seat regression-free
```

The bare `--pin` refused via the READ side because the newest real pin happens
to be generation-bearing; the WRITE side is the gate that catches the legacy
(`a00-*.meter`) production pins and is locked by test (a).

## Evidence

- **test_rotate.py full GREEN, unedited `test_pin_path_never_doubles_agi_dir`
  among them (falsifier g): `90 passed in 3.13s`.**
- **Direct consumers of the changed file also green (not the full suite, per
  the parent's HARD CEILING):** `test_rotate_complete.py` +
  `test_claude_code_adapter.py` + `test_rotation_alert.py` =
  `57 passed in 1.73s`.
- **New falsifier tests, all green:** a–f (18-meter/pin subset incl. existing
  seat & claim tests further up).
- **Real-tree (h):** bare `--pin` -> exit 1, no `/tmp/probe.meter` (was a
  silent capture before); `--seat sanctuary-director` -> `0.3701` exit 0.
- `find_pin_log` **unchanged** (signature and return), so
  `test_pin_path_never_doubles_agi_dir` and the `--seat`/`seat_pin-stale`
  semantics all hold as-is.

## Agent Notes
Repair built+proved: bare --pin now REFUSES (write gate in cmd_meter: identity must be --session-log//--seat) and seatless read REFUSES on another agent's gen-bearing pin (pin_unattributed in resolve_transcript). find_pin_log untouched; --seat unaffected; test_rotate.py 90 green (test_pin_path_never_doubles unedited); real-tree bare --pin exit 1 with no probe.meter, --seat sanctuary-director prints 0.3701.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.99: ACCEPTED as proved after independent reproduction. (1) The instruction said falsifiers (a)-(h), the refusal must name --session-log, find_pin_log untouched, --seat must not regress. (2) I ran the machine myself, not the kid's report: git diff shows exactly two seams in extensions/agi/bin/rotate.py — a seatless+generation-bearing return of "pin_unattributed" inside resolve_transcript (after pin_file-missing, before seat_pin-stale) and the write-side identity gate in cmd_meter; grep confirms no change to find_pin_log. My own run: test_rotate.py 90 passed; `rotate.py meter --pin /tmp/probe-parent.meter` exits 1 with the ERR naming --seat/--session-log and NO probe file created; `--seat sanctuary-director` prints 0.3701 exit 0. (3) Near miss avoided: fixing this inside find_pin_log would have satisfied "bare --pin refuses" and broken test_pin_path_never_doubles_agi_dir, which tests PATH resolution with seat=None — the kid fixed the adopter, as prescribed. (4) Caveat I am recording, not demoting for: the real-tree refusal fired via the READ side (newest real pin is generation-bearing) rather than the WRITE side; the write gate is covered only by the test fixture (a), since production legacy pins carry no generation. That is exactly what the hypothesis predicted, so it stands. Verdict proved with evidence_runs self + experiment:a00-51f3164a-10051e is justified: mechanism (a00-51f3164a) + repair (this run).
<!-- THOUGHT:END -->
