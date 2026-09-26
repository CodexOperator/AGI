---
id: experiment:a00-e8971175-58aa9c
mint_id: aafdf94dd5844d81bce9b37ae1f2fee0
type: experiment
parents:
  - hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session
next_edges: []
confidence: 0.9
edited_by: a00-5aaa03c7
evidence_runs:
  - experiment:a00-e8971175-58aa9c
loop: hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session@s2
model: stealth/space-bunny-alpha
production_lines: 76
profile: balanced
role: kid
scaffold_hash: 2770eb2cd59077ec
season: 2
title: the late s12 wait is bounded by a config cell and past it the record closes abandoned
town: core
verdict: proved
---
# the late s12 wait is bounded, and past the bound the record closes `abandoned`

## What was built (conjunct (2) only; (1) is kid 1's STALE-PIN, untouched)

| item | where |
|---|---|
| bound resolver `reaper.late_reap_wait_max_s` | `extensions/agi/bin/heal.py:693` `_late_reap_wait_max_s(root)` |
| one-shot close `abandoned` | `heal.py:711` `_close_late_reap_abandoned(...)` |
| the bounded waiting branch | `heal.py:771-791` (inside `_late_reap_for_skipped`) |
| the ONE log line | `heal.py:932-937` (inside `_late_reap_skipped_pass`) |
| tests | `extensions/agi/tests/test_heal_late_reap_bound.py` (5 tests, new file) |

## The config cell

- **Name: `reaper.late_reap_wait_max_s`** (seconds, positive number).
- **I did NOT write the cell into the shipped `.agi/config.json`.** It is
  DECLARED here only, and the code default `1800.0` applies today. The cell
  is therefore not inert, but it is also not owner-set: an owner who wants a
  different bound adds `"reaper": {"late_reap_wait_max_s": N}` and it is read
  at runtime, never cached, never a literal at the call site.
- **Default 1800 s (30 min), and why:** the same record's
  `observations.spawn_to_registry_s` (written at `heal.py:843`) shows the
  registry normally lands within a second or two of the rotation, so 1800 s is
  three orders of magnitude of headroom past a healthy join — a slow host or a
  loaded box is still covered — while a stuck pre-reboot window stops emitting
  a line per pass after at most a handful of watch cycles. A code default is
  the RESOLVER for a missing cell, not a second value: absent, unreadable, or
  malformed (`"soon"`, `0`, `true`) all fall back to 1800 and never raise.

## The age source

`record["recorded_at"]`, parsed by the existing `_parse_record_ts`
(`heal.py:1900`, UTC-correct `...Z` handling), against the function's own
`now` seam. Chosen over a file mtime or `time.time()` at first sight because a
rotation record's `recorded_at` is written with the rotation itself and
survives a reboot; an mtime of the rotations dir does not.

**MEASURED GAP:** a record whose `recorded_at` is absent or unparsable has no
clock at all, so it is never abandoned — it returns
`waiting` + `reason: "no-recorded_at"` and keeps its line. Inventing a
wall-clock there would be a guess a reboot can invalidate; the gap is stated,
not faked.

## Idempotence (one line, ever)

The close writes `s12_self_reap.state = "abandoned"` — the SAME dict the
success path writes (`heal.py:843`), plus `abandoned_at`, `waited_s`,
`bound_s`, `successor_id`, `reason`. On any later pass the branch reads that
marker first and returns `{"action": "abandoned", "already": True}` WITHOUT a
write; the pass driver logs the abandonment only `if not outcome["already"]`,
so the per-pass `waiting` line stops for good. Readers of `s12_self_reap`
elsewhere (the prediction-successor resolver at `heal.py:2115`) do
`reap.get("chain") or []`, so a `chain`-less abandoned record is read as
empty identity, never a raise — checked, not assumed.

## The near-miss avoided

Putting the age bound on `reg_file.st_mtime` (tempting: the existing latency
computation at `heal.py:846` already reads it) — a file created by a
pre-reboot process, so its age is a reboot artifact, not a wait. The bound is
on the record's own `recorded_at` instead.

## Falsifier RAN

`extensions/agi/bin/heal.py` copied to scratch, the bound deleted (the waiting
branch restored to its one-line `return ... "waiting"`), the same five tests
run against that copy:

```
$ python3 -m pytest test_falsifier.py -q     # heal = heal_nobound.py
FAILED test_under_bound_still_waiting            - KeyError: 'waited_s'
FAILED test_past_bound_closed_abandoned          - AssertionError
FAILED test_second_pass_no_second_line           - AssertionError
FAILED test_absent_bound_cell_uses_code_default  - KeyError
FAILED test_no_timestamp_never_abandons           - AssertionError
5 failed
```

Against the built bytes:

```
$ python3 -m pytest extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_heal_pin_reap.py \
    extensions/agi/tests/test_heal_late_reap_bound.py -q
103 passed
```

Cases: (a) 60 s old → `waiting`, no close, no write; (b) 7200 s old →
`abandoned` on disk with the full shape; (c) the driver run TWICE over the
same record → exactly one `ABANDONED` line, zero `waiting` lines, and a third
call reports `already: True`; (d) the cell absent → 1800 default, then a
declared 30 → abandoned at 60 s, then a malformed value → back to 1800, no
raise.

Production lines: 76 added / 1 removed in `extensions/agi/bin/heal.py`
(measured by `git diff --numstat` over the production paths; test file
excluded). Under the 2x-ceiling re-brief threshold of 80 — over the 10-12 the
brief hoped for, because both new helpers carry a docstring in a file whose
neighbours all do. No config cell was written; no pane, pid, unit, crontab or
`~/.claude/sessions` was touched; `rotate.py` was not edited; the STALE-PIN
branch in `_judge_leases` was not touched.

## Agent Notes
late s12 wait bounded by reaper.late_reap_wait_max_s (declared, code default 1800s), aged on the record's own recorded_at; past the bound the record closes s12_self_reap.state=abandoned with exactly one log line, idempotent; 5 new tests, 103 pass in the heal neighbourhood, falsifier (bound deleted) fails all 5

PARENT REVIEW DH.368 (a00-5aaa03c7): ACCEPTED for conjunct (2). Read the bytes: _late_reap_wait_max_s (heal.py:693) reads reaper.late_reap_wait_max_s via locations.config_path, rejects bool/non-positive/malformed, falls back to the 1800.0 code default; the bounded branch at :771-791 ages on the record own recorded_at through _parse_record_ts (:1977) and closes via _close_late_reap_abandoned (:711) into the SAME s12_self_reap shape the success path writes (:843); the single ABANDONED line is the pass driver own (:932-937), guarded by not outcome["already"]. 76 production lines vs the 10-12 the brief hoped for -- over the 2x re-brief threshold of 80? no, under it, but honest: two helpers with docstrings in a file whose neighbours all carry one. Accepted as scoped, noted as fat.

probes: (wire) the SAME 60s-old record judged with the cell at 10 vs 1e9 flips abandoned -> waiting, so the cell is read at runtime and a cached or hardcoded bound cannot produce this [PASS]. (auth) a record whose recorded_at is 10000s in the FUTURE (a box with a fast clock) is never abandoned -- waited clamps at 0 and the file is left unwritten [PASS]. (gate) a record whose late reap ALREADY succeeded (result: success_late, s12_self_reap.reaped_late true) with a vanished successor registry is never rewritten as abandoned -- the driver result!=skipped gate holds and the reaped_late marker survives [PASS]. (gate) the pass driver run THREE times over one 99999s-old record writes exactly ONE ABANDONED line and zero later waiting lines, and the abandoned record still reads as empty chain for the prediction-successor resolver at :2115 [PASS].

Probe file (parent-run, not the kid suite): /data/work/agi/.agi/worktrees/post-director-engine/.agi/sessions/iter-DH.368/a00-5aaa03c7/probe_parent_2.py -> 4 passed.

MEASURED WIDTH (recorded, not a disproof): the bound is only as wide as _parse_record_ts grammar, which accepts ...Z and naive-local only. A record stamped by any timezone-aware writer (datetime.now(timezone.utc).isoformat(), the modern default, carrying +00:00) is UNPARSABLE, falls to reason no-recorded_at, and waits forever -- the exact unbounded wait this conjunct removes. Every production writer today emits the Z form (rotate.py:5649, :5761, :5811, :6297), so no live record is affected today; the reader is narrower than the writers could become. Widening the reader, or the close reason being distinguishable from a genuinely absent clock, is the honest next step for this conjunct.

Struggle worth passing on: my first two probe runs were FALSE NEGATIVES, not defects -- I stamped records with +00:00 offsets and read the log through AGI_WATCH_LOG, which does not exist (the cell is AGI_REAPER_LOG, heal.py:340). A probe that asserts on an empty log passes as "no ABANDONED" and looks like a refutation of a correct change. Assert the log file EXISTS and the line COUNT is what you expect before you believe a zero.
