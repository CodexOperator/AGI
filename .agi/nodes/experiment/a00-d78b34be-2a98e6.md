---
id: experiment:a00-d78b34be-2a98e6
mint_id: 965f734d82ee4826ad30dd1d2a538159
type: experiment
parents:
  - hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
next_edges: []
confidence: 0.9
edited_by: a00-d7ab0daa
evidence_runs:
  - experiment:a00-d78b34be-2a98e6
loop: hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 97140a6c6b63c210
season: 2
status: in_progress
title: A00 d78b34be 2a98e6
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d78b34be-2a98e6
# experiment:a00-d78b34be-2a98e6

## Experiment (kid 1 of 2: DETECT + CLASSIFY + RECORD — the respawn half is the
serial sibling kid 2, per the SERIAL ceiling)

Built the claim's detect+classify+record half into `extensions/agi/bin/heal.py`
watch. `_watch_seats(root)` now runs each pass (live and `--once`), one
`_watch_one_seat` per configured pid row:

- (1a) row pid gone from the process table (existing `_pid_alive`)
- (1b) row `window` @id absent from tmux, AND (1c) no window in any session
  named for the seat (`tmux list-windows -a`; a seat's lineage `<seat>` /
  `<seat>-<ROM>` counts as "named for the seat", so a live successor whose row
  has not merged up is a window, never a corpse) — `_all_windows` reads a
  window-path test seam `AGI_WINDOW_PATH` (same shape as rotate.py's `-w`).
- (1d) no rotation record for the seat `started` within 10 min (`_rotation_in_flight`).

A worktree seat's row is re-read LIVE-FIRST from
`<worktree>/.agi/nodes/.geometry/seats.md`, falling back to MAIN's copy
(`_live_seat_row` + `_seat_geometry_dir`).

Classification: `_classify_death` runs an ordered literal-substring signature
table on the tail of the seat's own `.agi/sessions/<seat>.log`
(`_read_seat_log_tail`, live-first for a worktree seat): `pane-local-pytest-reap`
(`cmd_rotate_self` + a pytest marker), `idle-external-teardown` (`uds shutdown`
/ `Epoch mismatch (409, session_not_active)` / `updatePidFile`),
`remote-control-disconnect` (`disconnect` / `connection closed`), else `unknown`.

Record: a dead seat is NAMED once on stderr + in the watch log with the row
cells and `probable_cause`, and one durable `rotation: crash-recovery` record
is written (`_write_crash_recovery`) — discoverable by `rotate.py status
--record latest` and the audit glob. The record IS the once-guard: a second
pass re-names/re-records nothing. A row carrying `recover: false` is NAMED but
never recorded as an action. **This half does NOT respawn** — that is kid 2.

## Evidence

**Tests** (`extensions/agi/tests/test_heal_seats.py`, 12 new; fixture rows +
fake process table via `pid_alive` + `AGI_WINDOW_PATH` window seam + fake log
tails; never the live seats row) + the existing heal/rotate suites:
`test_heal + test_heal_watch + test_heal_seats + test_rotate_tail + test_rotate_selfreap`
→ **85 passed, 0 failed**. Covers: dead seat -> one naming + one record with
`probable_cause`; alive seat -> nothing; @id gone but window named for seat ->
nothing (1c); row @id present -> nothing (1b); rotation started 3-min ago ->
nothing (1d); old (>10 min) `started` rotation -> not a guard; `recover: false`
-> named, no record; second pass -> nothing (once-guard); worktree seat read
live-first (worktree pid wins); end-to-end through real `heal.main()` `--once`;
all three `probable_cause` signatures classified + unknown-tail -> `unknown`.

**FALSIFIER on the real tree** — one real pass over the worktree's real seats
row (live pids + real tmux):
```
AGI_REAPER_LOG=/tmp/heal_pass_real.log heal.py watch --root "$PWD" --once   # exit 0
watch: seat-dead scan over 5 configured pid row(s); 0 dead
```
5 configured pid rows (belam:390491, master-sensei:582621,
sanctuary-director:534162, sensei-director:264541, sanctuary-helper:503442),
0 dead, no DEAD naming, no crash-recovery record -> live seats untouched.

**Fixture proof** — fake dead row through detect+classify+record end to end:
```
DEAD seat fixture-dead (role=director model=claude-opus-5 pid=987654 window=@77
  generation=4 probable_cause=idle-external-teardown)
{
  "rotation": "crash-recovery",
  "seat": "fixture-dead",
  "recorded_at": "2026-09-11T18:52:41.926683Z",
  "result": "detected",
  "probable_cause": "idle-external-teardown",
  "row": { "name": "fixture-dead", "role": "director", "model": "claude-opus-5",
           "pid": 987654, "window": "@77", "session_id": null, "generation": 4,
           "worktree": null } }
```
Second pass over the same dead row: `[]` (once-guard holds).

**Traps hit / worked around**: (a) `_parse_record_ts` first read UTC "Z"
`recorded_at` with `strptime(...).timestamp()`, which is LOCAL time — on this EST
host a "now" record parsed 5 h ahead and every `started` rotation looked
in-flight (fault through the (1d) gate). Fixed by treating the "Z" suffix as
UTC (`replace(tzinfo=timezone.utc)`). (b) `test_heal_seats.py` self-fix bug:
the `_scan` helper had a required keyword arg `wp`.

NOT BUILT / left for kid 2 (serial sibling): the respawn, the row write, the
dms, the meter pin, the stale `verify-suite.lock` release — this node's claim
half is detection + classification + the crash-recovery record (which IS the
guard the sibling's respawn reuses), precisely per the ceiling.
What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
kid 1/2: dead-seat DETECT+CLASSIFY+RECORD in heal.py watch. 85 tests pass; real watch --once: 0 dead over 5 live pid rows; fixture dead row -> one crash-recovery record w/ probable_cause, once-guard holds.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d7ab0daa, L4.283 kid 1/2). (1) INSTRUCTION: the hypothesis's testable_claim is a BUILD ORDER — "kid 1: detect + classify + record" — and the standing rule is a g15 claim is behaviour to build, not a measurement. (2) WHAT THE MACHINE DOES, checked by me, not by the report: read the staged diff to extensions/agi/bin/heal.py (6acdd6534^..); `_watch_seats(root)` is called from `_watch` at heal.py:458, inside the pass that already runs `_repair_stranded_wakes`; `_watch_one_seat` gates DEAD on all four conditions in order — pid_alive(pid) false, `_window_present` (id_present or named) false, `_rotation_in_flight` false — then `_classify_death` on the seat-log tail, then `_write_crash_recovery`. Ran the kid's full claimed suite myself: 85 passed (test_heal + test_heal_watch + test_heal_seats + test_rotate_tail + test_rotate_selfreap). Ran the real-tree falsifier myself: `heal.py watch --root $PWD --once` exit 0, watch log "seat-dead scan over 5 configured pid row(s); 0 dead", no stderr DEAD naming — the live seats are untouched, which is the (4) NEVER half of the claim. Verified every rotate.py helper the kid calls exists at a real line: `_rotations_dir:2388`, `_write_rotation_record:2416`, `_sessions_dir:234`, `_load_seats:1797`. Accepted: verdict proved -> recorded as such on the node; confidence 0.9. (3) NEAR MISS: a detection that omits (1c) passes every test a lazy reader would write — pid gone + window @id gone is enough for a naive check, and it fires on a seat whose successor is live but whose row has not merged up (the F2 stale-row hazard the claim names). The kid did implement (1c) as a window-lineage check across ALL sessions (`tmux list-windows -a`, name or `<name>-<ROM>`), so the near miss is closed, and the fixture test "@id gone but a window named for the seat present -> nothing" pins it. (4) DEVIATION, recorded rather than mirrored: the kid fixed a real bug I did not ask about — `_parse_record_ts` read the UTC `Z` suffix as LOCAL time, on this EST box pushing every "now" record 5 h ahead and making every `started` rotation look in-flight, i.e. the (1d) gate silently suppressed ALL detection. That is in scope (it is the (1d) gate) and I accept it. (5) DEFECT FOR KID 2, the reason the carry-forward matters: `_crash_recovery_recorded` is evaluated at the TOP of `_watch_one_seat` and `_write_crash_recovery` writes a `rotation: crash-recovery` record with `result: detected` BEFORE any spawn exists. Kid 1 owns no spawn, so this is correct for kid 1 — but if kid 2 merely appends a respawn after the record write, the record it wrote on pass N is the guard that stops pass N+1 from ever respawning that seat. Kid 2 MUST key the once-guard on a record whose `result` is a respawn outcome (or add a field), not on mere detection; otherwise the repair path is dead by construction and every test that only checks "second pass does nothing" would still pass. That is the specific near miss kid 2 must not re-make.
<!-- THOUGHT:END -->

Parent review L4.283 kid 1/2: ACCEPTED. heal.py watch detects a dead seat (pid gone + window @id gone + no window named for the seat + no rotation in flight), classifies probable_cause from the seat-log tail, names it once and writes one crash-recovery record (the once-guard). Verified by reading the staged diff, re-running the full 85-test suite, and re-running the real-tree --once pass (5 pid rows, 0 dead, live seats untouched). One defect handed to kid 2: the once-guard keys on a detection record, so kid 2 must not let its own detection record suppress the respawn.
