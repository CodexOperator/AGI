---
id: experiment:a00-f559a2f8-85dc82
mint_id: 4184b47f8b2b4aa9a4696feb41792c63
type: experiment
parents:
  - hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs
next_edges: []
confidence: 0.9
edited_by: a00-4125554d
evidence_runs:
  - experiment:a00-f559a2f8-85dc82
loop: hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3c19f61530b666e7
season: 2
title: A00 f559a2f8 85dc82
town: core
verdict: proved
---
# experiment:a00-f559a2f8-85dc82

Built goal:g15.25 SL7.72: the captive after_join is now performed LIVE by a
running heal watch, OR by rotate-self's own post-spawn tail when no watcher
runs — a rotation never depends on a watcher that is not running, and the
record's `after_join` key is never absent and never `{}`.

PRE-FIX (measured): with `.agi/config.json` `agent_dispatch.inline_reaper=false`
and `reaper.unit_enabled` absent, `_after_join_performer_armed` armed by CONFIG
ALONE (`unit_enabled` default True) and step (6.4) deferred to the service by
config alone — so with the watch process DEAD the pre-turn probe recorded
`deferred: after_join` (a lie) and the record stayed `after_join`-absent. All
three falsifiers were reachable.

## What changed

- `extensions/agi/bin/heal.py`:885 `_write_watch_heartbeat(root)` — each watch
  pass writes `<sessions>/reaper.watch.json` = `{"pid": os.getpid(), "at":
  epoch}` (resolved via `locations.sessions_dir`, best-effort, never raises);
  called at heal.py:912 as the FIRST act of each `_watch` pass.
- `extensions/agi/bin/rotate.py`:9222-9259 `WATCH_HEARTBEAT_FILE`+`GRACE_S=120`
  (3 × the 30s poll), `_watch_heartbeat_path`, `_watch_alive(root, *, now=None)`
  — alive iff heartbeat exists, pid live (`os.kill(pid,0)` probe), and
  `now-at <= GRACE`. Absent/unparsable/stale/pid-dead ⇒ NOT alive. Deliberately
  NOT the reaper log's mtime (`send.py` `wake` writes that same log — a fresh
  log mtime can come from a non-watch writer and would read "watch alive").
- `extensions/agi/bin/rotate.py`:9280 `_after_join_performer_armed` — now armed
  iff `forced` OR `_inline_reaper_enabled` OR (`reaper.unit_enabled` not false
  AND `_watch_alive`); an absent/dead/stale watch reads NOT armed.
- `extensions/agi/bin/rotate.py`:9316 `_after_join_tail_should_perform` — the
  production (6.4) decision: perform when `forced` OR `inline_reaper` OR
  `not _watch_alive`. This is real code the tail calls (not a test copy).
- `extensions/agi/bin/rotate.py`:9334 `_after_join_already_performed` — the
  double-perform guard (re-reads the record; True when it already carries
  `after_join`, so the tail never runs twice).
- `extensions/agi/bin/rotate.py`:9622 `run_after_join(..., performer="watch")`
  — record's `after_join` dict now carries `performer` (+ legacy `performed_by`
  in lockstep) and `results: []` when the list is empty, so the key is never
  `{}`.
- `extensions/agi/bin/rotate.py`:9782 `run_after_join_for_seat(..., performer)`
  — threads the performer through; heal's watch call passes `performer="watch"`
  (heal.py:453).
- `extensions/agi/bin/rotate.py`:13100-13131 step (6.4) — perform when
  `_after_join_tail_should_perform`, re-read the record and SKIP if the watch
  already won (`_after_join_already_performed`), and call `run_after_join`
  with `performer="tail"`; deferral line printed only when an alive watch
  really runs it.
- Tests: `extensions/agi/tests/test_after_join_service.py` — three new
  (`test_no_watcher_tail_performs`, `test_watch_alive_tail_skips`,
  `test_after_join_key_never_empty`) + helpers `_live_heartbeat`,
  `_rotation_record`; `test_after_join_performer_armed_branches` updated for
  the liveness arm. `extensions/agi/tests/test_rotate_handover.py` — helper
  `_live_watch_heartbeat`; the two pre-turn-deferral tests now run with an
  ALIVE watch so the tail defers (new semantics: a dead watch now means the
  tail performs, so the old "nothing will ever run" premise no longer holds).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_after_join_service.py extensions/agi/tests/test_rotate_handover.py -q
63 passed in 14.98s
```

```
$ python3 -m pytest extensions/agi/tests/test_after_join_service.py -q -k "no_watcher_tail or watch_alive_tail or key_never_empty"
3 passed, 17 deselected in 0.07s
```

Guard files covering the changed code also green: `test_heal_watch.py` 34 passed,
`test_rotate_startup.py` 88 passed, `test_rotate_tail.py` 26 passed,
`test_rotate.py` 246 passed, `test_rotate_selfreap.py` 22 passed,
`test_heal_ack_rotation.py` 7, `test_heal_seats.py` 17, `test_rotate_prepare.py` 33,
`test_rotate_g1517.py` 5, `test_rotate_alert_two_tree.py` 5+1 xfail.

Focused T1 fixture — the record it leaves (the artifact, not the assertion):

```
armed (no watcher, inline_reaper off): False
tail_should_perform: True
appended: True
RECORD after_join object:
{
  "performer": "tail",
  "performed_by": "tail",
  "delay_s": 20,
  "results": [
    { "label": "join", "cmd": "echo tail-ran", "rc": 0,
      "output": "echoed join-done", "truncated": false, "byte_cap": 4000 }
  ],
  "dm": "## AFTER_JOIN OUTPUT ..."
}
```

## Falsifier check

- "a rotate-self on a box with no heal watch leaves a record without
  `after_join` or with `{}`" — MADE FALSE: with no heartbeat + inline off,
  `_after_join_tail_should_perform` is True (T1), the tail runs and the record
  ends with `after_join.performer="tail"` + real results (artifact above).
- "a live watch and the tail both perform (two model_confirm writes)" — MADE
  FALSE: with a fresh heartbeat, `_watch_alive` True, `_after_join_performer_armed`
  True, `_after_join_tail_should_perform` False (T2 — the tail does not call
  run_after_join), and the watch's `run_after_join_for_seat` writes
  `performer="watch"` exactly once — a second call returns None.
- "the tail performs while the record says `deferred: after_join`" — MADE
  FALSE: `_deferred` is recorded at pre-turn only when `_after_join_performer_armed`
  is True = only when an ALIVE watch is the performer — and in that case the
  tail does NOT perform (T2). When the tail does perform (no alive watch),
  armed is False so the pre-turn records the skipped reason, and step (6.4)'s
  run_after_join overwrites `model_confirm` in place; the double-perform guard
  also skips the tail when the watch already wrote `after_join`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
The liveness mechanism is a DEDICATED heartbeat file written once per watch
pass, never the reaper log's mtime: `_watch_log` delegates to send.py's SHARED
`reaper_log.log`, so a fresh log mtime can come from a non-watch writer
(`send.py wake`) and would read "watch alive" on a dead-watch box — satisfying
the words and losing the mechanism. The heartbeat pid + timestamp via
`os.kill(pid,0)` reuses the existing `_pid_alive` probe idiom. GRACE 120 s = 3×
the default 30 s poll so one missed pass is not misread as death. Asymmetric
by design (task-prescribed): `_after_join_performer_armed` is the SERVICE's
arm state (dead watch ⇒ NOT armed ⇒ pre-turn records skipped, never a lie),
while step (6.4) uses `_after_join_tail_should_perform` (dead watch ⇒ tail
performs). These consciously disagree so a dead watch can never produce a
`deferred:`-lie while the tail actually performs; the tail's own confirm
overwrites the pre-turn probe in place. `reaper.unit_enabled` now guards only
the WATCH service; the rotate-self tail is the unconditional last resort when
no watch is alive, which is exactly what makes falsifier 1 false.
<!-- THOUGHT:END -->

## Agent Notes
Built SL7.72: heal watch writes per-pass heartbeat reaper.watch.json; rotate _watch_alive reads it; tail performs after_join when no alive watch (performer=tail), defers to alive watch (performer=watch); double-perform guard; after_join never {}. 3 new tests + suite green (63 passed on the two files).

PARENT REVIEW (a00-4125554d, SL7.72): accepted, verdict proved. Re-read the bytes: rotate.py:9222-9259 (_watch_alive, GRACE 120s, os.kill probe), :9280 (_after_join_performer_armed requires unit_enabled AND _watch_alive), :9316 (_after_join_tail_should_perform = forced OR inline_reaper OR not _watch_alive, called by real step (6.4)), :9334 (_after_join_already_performed), :9730 (performer + performed_by + results into the record), :13084-13119 (the (6.4) branch + guard). Re-ran test_after_join_service.py + test_rotate_handover.py: 65 passed. The one gap I held open (the (6.4) wiring proven only through seams) was closed in this same round by experiment:a00-f53dbe76-4f7353 (T4/T5 drive real cmd_rotate_self). Residual, NOT held against this node: (1) heal.py:885 writes the heartbeat through locations.sessions_dir (per-worktree join) while rotate reads through _sessions_dir (shared, git_common_root) — they agree only because the systemd unit runs --root at the main checkout; a watch started from a worktree root would fork the heartbeat path. (2) the docstring sentence "Missing/broken config reads armed" contradicted the code (returned False) — repaired by kid 2 in this round.
