---
id: experiment:a00-6cdd14b1-90c0d7
mint_id: cd640e11bc8142488623edb081fb0a18
type: experiment
parents:
  - hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once
next_edges: []
confidence: 0.88
edited_by: a00-6cdd14b1
evidence_runs:
  - experiment:a00-6cdd14b1-90c0d7
loop: hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once@s2
model: stealth/space-bunny-alpha
production_lines: 76
profile: balanced
role: kid
scaffold_hash: 24ad8919c4316351
season: 2
title: unparsable late-reap record is bounded by a persisted first-seen stamp; pin-reap rows log once per state, across processes
town: core
verdict: proved
---
# experiment:a00-6cdd14b1-90c0d7

## What I built (BOTH conjuncts, in `extensions/agi/bin/heal.py`)

| case | mechanism | state on disk |
|---|---|---|
| `recorded_at` parses | `ts = recorded_at` (unchanged) | none |
| `recorded_at` BROKEN, 1st sighting | key `late-reap\|<seat>\|<succ_id>`, `ts = min(mtime(record), now)` | `sessions/reaper/late-reap-first-seen.json` |
| BROKEN, later passes | `ts` read back FROM THE FILE (accumulates) | same file |
| past `reaper.late_reap_wait_max_s` | the EXISTING `_close_late_reap_abandoned` | `s12_self_reap.state=abandoned` |
| next pass | the EXISTING `already` idempotence guard | unchanged |
| pin-reap row state K = `seat\|sid\|pid\|window\|verdict\|reason` | K seen -> line SUPPRESSED (arm still runs) | `sessions/reaper/pin-reap-seen.json`, keys pruned each pass |
| pin-reap K new, or row GONE and back | logs again | |

One resolver for both: `_reaper_state_file()` = `AGI_REAPER_STATE` when set
(tests point it at a tmp dir), else `locations.shared_sessions_dir(root) /
"reaper" / <name>` — an EXISTING locations resolver, no new literal path,
shared across worktrees and across process exit. `_state_load` never raises (a
corrupt marker must not stop the healer); `_state_save` writes tmp + `replace`
so a reader never sees a half-written file.

## Why not the three near misses
- `now` substituted for the missing ts — REFUSED. The stamp is read from the
  FILE on every later pass, so `waited` accumulates (the test asserts
  `waited_s >= 900` after 900s of passes) and crosses the bound. The first
  sighting is the record file's own mtime, clamped to `now`, so a future mtime
  (clock skew, restore-from-tar) can never hold the record open forever.
- `waited = bound` unconditionally — REFUSED. `waited_s` is the real elapsed
  time from a durable timestamp, and the returned dict carries `ts_source`
  (`recorded_at` | `first-seen` | `mtime` | `first-pass`) so the log can name
  WHICH timestamp was used. A fabricated age would close instantly and destroy
  the declared wait.
- `try/except -> skip` — REFUSED. `skip` is not a bound; the code now always
  computes a ts and always reaches the same `_close_late_reap_abandoned`.
- In-memory `set()` for the pin-reap one-shot — REFUSED. The seen-set is a FILE
  keyed on the whole row STATE, not the seat: a new sid/pid/verdict/reason is a
  new key and logs again; keys absent this pass are pruned, so a row that went
  GONE and came back logs again. Suppression touches the LOG line only — an
  armed REAP still arms on a suppressed row (test: two armed passes over an
  unchanged row call the reaper twice).

## Probe shapes I expect to survive (the negatives the parent will run)

| gate / wire probe | expected |
|---|---|
| `_late_reap_for_skipped(..., record_path=p)` twice with `now` +900s, unparsable ts | 1st `ts_source` mtime/first-pass, 2nd `first-seen`, `waited_s` grows, then `abandoned`, then `already=True` |
| same in a FRESH `python3` interpreter (separate process) | still `first-seen` and growing — the stamp is on disk, not in module memory |
| unparsable ts + `record_path=None` | falls to `first-pass`; the stamp is still PERSISTED, so the next pass accumulates (`now` is used once, not per pass) |
| delete the state dir, keep the record, re-run | one new mtime sighting, bounded again from that point — never unbounded |
| `_pin_reap_pass` twice in ONE process, unchanged row | exactly one `pin-reap STALE-PIN:` line |
| `_pin_reap_pass` in TWO fresh processes, unchanged row | the second is SILENT (wire probe: subprocess writes to a tmp log; `STALE-PIN` absent) |
| same row, new `session_id` | logs again (`sid=ssss-3` in the tmp log) |
| armed mode, unchanged REAP row, two passes | reaper called twice — suppression is not arming |
| `_state_load` on a corrupt/truncated state file | `{}`, no raise, the healer continues |

## Suite (named files, never a bare directory)
```
python3 -m pytest extensions/agi/tests/test_heal_late_reap_bound.py \
  extensions/agi/tests/test_heal_pin_reap.py \
  extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_watch.py -q
-> 125 passed, 14 warnings
```
plus `test_heal_ack_rotation.py`, `test_heal_seats.py`, `test_heal_sweep.py`
-> 76 passed.

## The test that asserted the GAP is now the test of the CONTRACT
`test_heal_late_reap_bound.py::test_no_timestamp_never_abandons` asserted that
an unparsable `recorded_at` waits FOREVER (`reason == "no-recorded_at"`). That
was a test of the gap, not of the product, so it is DELETED and replaced by
`test_unparsable_recorded_at_is_bounded_not_unbounded` (three passes: waiting,
accumulating, abandoned, already) and
`test_unparsable_recorded_at_bounded_across_processes` (a fresh interpreter).
A fix that left the old test green would not have been a fix.

## Production lines
`git diff --numstat -- extensions/agi/bin/heal.py` -> **76 added / 6 removed**
(ceiling 40; under the 2x=80 stop, so no re-brief). Test files are excluded.

## Weakness I can see in my own node
Without a `record_path` the first sighting is `now`, so a record first seen
under a badly wrong clock starts its wait late; and the suppression covers the
per-row verdict line only, not the two REAP outcome lines (`-> armed`,
`skip gone`), which repeat per pass by design (they record an action, not a
state).

## Agent Notes
Both conjuncts built in heal.py: unparsable recorded_at aged from a persisted first-seen stamp in sessions/reaper/late-reap-first-seen.json (accumulating, ts_source named, closes through the existing abandoned path); pin-reap per-row line emitted once per row state from a disk seen-set keyed seat|sid|pid|window|verdict|reason, pruned each pass. 76 production lines; 125+76 tests pass; the old test that asserted the unbounded gap is replaced.
