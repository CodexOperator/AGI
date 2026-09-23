---
id: experiment:a00-03083f0a-session-pin-join
mint_id: 82b1048fde8d450e8bbb85fffa631a99
type: experiment
parents:
  - hypothesis:a00-03083f0a-d7d355
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-03083f0a-session-pin-join
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "rotate.cmd_spawn(_spawn_args(seat='director-seat', window_path=None), <tmp graph>) with a private real tmux server (own TMUX_TMPDIR) and a registry_dir holding 4242.json whose content carries 'view:@1.%0' (the live seat window @id)", "expected": "row.window == the live tmux @id and row.pid/session_id == the JOINED registry pid/session_id", "observed": "window '@1' == live '@1'; pid 4242; session_id 'abcd1234-aaaa-bbbb-cccc-dddd12345678'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "read the same seat-start row's short-ref and harness-name cells", "expected": "the SESSION cells the seating JOIN does not forward stay EMPTY at seat start, never a stale/derived value", "observed": "session_ref ''; session_name '' (while session_id and pid ARE joined)", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "rotate.cmd_ack(seat='director-seat', session=row.session_id, ref='caa927', answer='continue', registry_dir=<same dir>) then re-read the row", "expected": "the ack back-fills session_ref and session_name from the SAME JOIN keyed on the row's own window @id, leaving pid/session_id/window byte-identical", "observed": "session_ref 'caa927'; session_name 'agi-d7'; pid 4242; session_id unchanged; window '@1'", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "compare the seat-start row's session_name against the JOIN record's own name, and against the value the later ack back-fills", "expected": "the name IS resolvable at seat start (the same JOIN resolved it) but _first_seating_spawn_writes does not forward it, so the cell is empty", "observed": "registry name 'agi-d7' resolved by the JOIN, yet seat-start session_name ''; ack later writes 'agi-d7'", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: ecc9b8b7c5486774
season: 2
testable_claim: Driving the real rotate.cmd_spawn seat-start path against a private real tmux server AND a real registry JOIN, the committed config:seats row carries the JOINed session_id and pid (matching the live registry fact) at seat start, while session_name and session_ref stay empty until rotate.py ack back-fills them.
title: "Session pin at seat start: the JOIN's uuid/pid land, the harness name and short ref do not"
town: core
verdict: inconclusive_lean_proved:70
---

# experiment:a00-03083f0a-session-pin-join

## Falsifier
After seat start: posts/seat registry shows occupied with the live
pane/session pin matching `tmux`.

## What I did
I settled the SESSION half of that falsifier, which the pane-live experiment
left in prose. The test drives the REAL `rotate.cmd_spawn` seat-start path
against BOTH witnesses at once:

* a private real tmux server (own `TMUX_TMPDIR`, `window_path=None`), so the
  `@id` the row commits is read from tmux itself; and
* a REAL registry JOIN: a `<pid>.json` whose CONTENT carries that live `@id`
  as a delimited token (`view:@1.%0`), the exact shape
  `rotate._join_successor` / `rotate._registry_matches_window_id` consume.

The launch is a `spawn_window` stub that creates the real seat window, reads
the `@id`, and writes the registry record — the real sequence (window absent
at the gate, present after the launch). I then read the COMMITTED
`config:seats` row, run the real `rotate.cmd_ack` ack path with the `--ref`
the claim describes, and read the row again.

    python3 -m pytest extensions/agi/tests/test_seat_session_pin_live.py -q
    2 passed in 21.45s

## Measured — the committed row, seat start vs after ack

| cell | at seat start | after `ack --ref caa927` |
|---|---|---|
| `window` | `@1` (== live tmux @id) | `@1` |
| `pid` | `4242` (JOIN) | `4242` |
| `session_id` | `abcd1234-aaaa-bbbb-cccc-dddd12345678` (JOIN) | unchanged |
| `session_name` | `` (empty) | `agi-d7` |
| `session_ref` | `` (empty) | `caa927` |
| `generation` | `1` | `1` |

Full seat-start row (measured, `json.dumps` of the wire row):

    {"enc_scheme": "none", "generation": 1, "name": "director-seat",
     "pid": 4242, "role": "director",
     "session_id": "abcd1234-aaaa-bbbb-cccc-dddd12345678",
     "session_kind": "remote-control", "session_label": "director-seat",
     "session_name": "", "session_ref": "", "window": "@1"}

After the ack, the ONLY changed cells are `session_ref` and `session_name`:

    ... "session_name": "agi-d7", "session_ref": "caa927", ...

## Answer, plainly
* At seat start the registry's SESSION identity IS partially live: the
  `session_id` uuid and the `pid` land from the real JOIN keyed on the live
  tmux `@id`, and they match the registry file. The PANE pin matches tmux.
* The harness NAME does NOT land at seat start even though the very same JOIN
  resolved it — `_first_seating_spawn_writes` calls `_successor_row_write`
  with `session_id`/`pid` but never the `session_name` kwarg the writer
  accepts, so the cell is written `''`.
* The short ListAgents `session_ref` is `''` at seat start by design and only
  lands at `rotate.py ack`.
* So the falsifier's strict reading — "after seat start ... session pin" — is
  NOT fully settled at seat start: one of the three session cells
  (`session_name`) is resolvable-but-dropped, and `session_ref` needs the ack.

## Named production gap (no change landed — OBSERVE/SETTLE kid)
`_first_seating_spawn_writes` (rotate.py ~6561) has `join['name']` in hand via
`_seating_rec` at its call site, and `_successor_row_write` already accepts a
`session_name` kwarg, but the seating path passes neither: the harness name
resolved by the JOIN is dropped for the one cell designed to carry it. The ack
back-fills it later because the ack's own JOIN re-resolves it. A one-kwarg
forward would make `session_name` land at seat start, consistent with
`session_id`/`pid`. Naming only; not built here.

## Verdict
inconclusive_lean_proved:70 — the JOIN-supplied identity (pid + session_id)
lands and matches live at seat start and the ack completes the ref + name; the
falsifier's session pin is not fully coherent at seat start.
