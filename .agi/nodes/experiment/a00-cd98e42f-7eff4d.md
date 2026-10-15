---
id: experiment:a00-cd98e42f-7eff4d
mint_id: 582b9e9283d54763bf385d8459536502
type: experiment
parents:
  - hypothesis:l4-the-pin-is-the-lease
next_edges: []
confidence: 0.9
edited_by: a00-fa7a06bd
evidence_runs:
  - experiment:a00-cd98e42f-7eff4d
loop: hypothesis:l4-the-pin-is-the-lease@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f08cdad34317cc4d
season: 2
title: A00 cd98e42f 7eff4d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cd98e42f-7eff4d

## Experiment

KID 1 OF 2 (SERIAL) for `hypothesis:l4-the-pin-is-the-lease` — built the
TABLES + the JUDGEMENT as pure functions in `extensions/agi/bin/heal.py`, per
the declared build order. KID 2's half (the pass, the arm, the dm, the
live-tree dry-run proof) is intentionally untouched: `_pin_reap_pass`, its
`_watch` call site, and the `pin-reap` main() entry do NOT exist yet. No edit
to `rotate.py`, no edit to `.agi/config.json`, no kill from the suite, no
read of `~/.claude/sessions`.

Built (clause-by-clause of the hypothesis spec):

- **(1a) `_pin_table(root, rows)`** — returns `({session_id: (seat, pin_path,
  generation)}, skipped)`. Reads each row's seat-stable pin
  `<sessions>/<seat>.meter` through rotate's ONE `_sessions_dir` resolver and,
  for a row carrying `predecessor_pins: N` (READ the cell, absent = 0), the
  chain pins `<seat>.pred-1..N.meter` beside it. Scales by the transcript's
  STEM (the L4.114 identity). A pin whose transcript file is MISSING is
  SKIPPED with a reason (clause 3) and never leases a session. Pin content is
  parsed by rotate's own `_parse_pin_record` — never copied.
- **(1b) `_seat_sessions(registry_dir, windows)`** — one entry per registry
  file whose `tmux` cell's `@id` resolves, through the SAME `_all_windows`
  list, to a live window: `[{pid, session_id, window_id, window_name}]`.
  Owner sessions (`tmux: None`), the streamer stub, and an @id resolving to
  no window are NOT seat sessions (clause 4): never listed. The seat/belam
  NAME gate lives in `_judge_leases` (the layer that holds `rows`; the fixed
  `(registry_dir, windows)` signature cannot see them) — a documented
  deviation from the prose placement, same semantics.
- **(1c) `_judge_leases(pins, sessions, rows, root, now)`** — per seat session
  exactly one of KEEP / PROTECTED / IN-FLIGHT / BELAM-UNPINNED / REAP in that
  verdict order. `_rotation_in_flight` is CALLED (L4.283's guard), not
  copied. `protected` READ from the row (absent = not). Owner remote-control
  and non-seat/non-belam windows never appear. A belam-prefixed window with a
  `belam.pred-N.meter` lease -> KEEP (uniform rule); with no
  `predecessor_pins` cell / incomplete pred chain -> BELAM-UNPINNED, reason
  `no predecessor-pin table yet`, NEVER REAP (the owner's standing rule the
  idle predecessor windows are never closed holds BY CONSTRUCTION until the
  pin SHIFT exists).

Tests in the NEW `extensions/agi/tests/test_heal_pin_reap.py` (15), all
FIXTURE-tree / fixture registry dir / the existing `window_path` seam / fake
pid table: pin mapping + pred-pin + stale-pin-skip; id-resolution + owner/
orphan exclusion; KEEP / REAP / PROTECTED / IN-FLIGHT / old-rotation-is-REAP;
owner absent; outside-seat-window never listed; belam no-pred-table -> XI
KEEP + four BELAM-UNPINNED, nothing reaped; `predecessor_pins: 5` +
`belam.pred-1.meter` naming VI -> VI KEEP; transcript-gone pin -> skipped
+ judged unpinned.

The run I performed:
```
python3 -m pytest extensions/agi/tests/test_heal_pin_reap.py -q\
  extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_seats.py\
  extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_heal_sweep.py -q
```

## Evidence

`python3 -m pytest extensions/agi/tests/test_heal_pin_reap.py -q` ->
`15 passed`.

Engine heal regression (the files I could have touched):
`extensions/agi/tests/test_heal.py test_heal_seats.py test_heal_watch.py\
test_heal_sweep.py test_heal_pin_reap.py` -> `69 passed`.

`python3 -m py_compile extensions/agi/bin/heal.py` -> OK; heal imports and
all three new functions resolve.

Falsifiers held within KID-1 scope: a pinned session is never listed as
would-reap; a session outside the seat/belam window names is never listed;
an armed reap without a dm is KID 2's falsifier and does not apply here
(no reap code shipped); a belam predecessor is never REAP while no pred
table exists; NO edit to rotate.py; no real kill; `.agi/config.json`
untouched; no second `_watch` call site added.",
"}]

## Agent Notes
KID 1: built the pin-is-the-lease TABLES+JUDGEMENT (_pin_table/_seat_sessions/_judge_leases in heal.py) and proved them on fixtures (15 new tests). KID 2 pass/arm/dm/live proof deferred by serial order.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-fa7a06bd, L4.289): accepted, verdict proved at KID-1 scope. Verified by re-running, not by reading the report: `pytest test_heal_pin_reap.py -q` = 15 passed; the five heal test files = 69 passed; `_pin_table`/`_seat_sessions`/`_judge_leases` resolve and reuse rotate.s `_parse_pin_record`/`METER_PIN_EXT`/`_sessions_dir` with ZERO rotate.py edits (git status shows only heal.py modified, the new test file, and this node). Falsifiers checked in the artifact: fixtures only (`tmp_path` + fixture registry dir, never ~/.claude/sessions), no real kill, no .agi/config.json touch, no second `_watch` call site, no _pin_reap_pass yet. ONE DELIBERATE DEVIATION, accepted: the spec s (1b) says _seat_sessions does the seat/belam NAME gate, but its declared signature `_seat_sessions(registry_dir, windows)` carries no rows and therefore cannot; the kid did the @id resolution there and moved the name gate into _judge_leases, where the rows live. The falsifier "a session outside the seat/belam window names is never listed at all" is thus satisfied at the judgement layer, not the table layer -- covered by test_outside_seat_window_not_judged. KID 2 must read `_seat_sessions` output as @id-resolved sessions only, NOT as seat sessions, or it will treat every tmux-attached CC session as reapable.
<!-- THOUGHT:END -->
