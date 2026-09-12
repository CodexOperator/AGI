---
id: experiment:a00-eea2fd59-83bcc3
mint_id: d95bc6b8cb06446b8c9e787e5b5f5697
type: experiment
parents:
  - hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe
next_edges: []
confidence: 0.6
edited_by: a00-232c7d9a
evidence_runs:
  - experiment:a00-eea2fd59-83bcc3
loop: hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0330dfa6ecf1e189
season: 2
title: A00 eea2fd59 83bcc3
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-eea2fd59-83bcc3

## Experiment

Clause 3 of the g15.23 alert-path claim — the DETECTED-RECORD DEDUPE and
the status read. g15 claims are BUILD ORDERS, so I measured the pre-fix
bytes, implemented, and proved it on the built bytes.

**Pre-fix defect (measured in the code, matching the observed nine records):**
`heal.py _watch_one_seat` re-scans every configured pid row on every watch
poll (~30 s). A seat whose row pid is gone and whose window @id is gone is
DEAD; `_recover_seat` tries the spawn, and when the launcher reports no
successor process it returns `respawned: False`. `_write_crash_recovery`
then computed the result `detected` (spawn never landed) and called
`rotate._write_rotation_record(root, rec)` with NO path — which mints a
FRESH `<seat>.<UTC-stamp>.json` every call. A still-dead-and-unrecoverable
seat therefore accumulated one new `detected` file per poll → the nine
`result=detected` records at 30 s intervals for one death. And because
`rotate._latest_rotation_record` / `cmd_status --record latest` served the
LEXICALLY newest `<seat>.*.json` with no filter, the newest of those
`detected` records was read back as the seat's "rotation".

**Fix in heal.py `_write_crash_recovery`:** a `detected` (recovery did not
land) write is deduped — the seat's newest existing `result: detected`
`crash-recovery` record still inside `SEAT_DEAD_WINDOW_S` (10 min) is
UPDATED IN PLACE (`rotate._write_rotation_record(root, rec, path=existing)`),
never a fresh file. One death → one record. A `respawned` outcome is a
distinct terminal recovery and always writes a fresh file. New helper
`heal._latest_detected_path`. The respawn RETRY (the reason a `detected`
record must never suppress the next pass) is untouched — only the record
landing spot is deduped.

**Fix in rotate.py:** new `_rotation_record_files(root, seat)` excludes
`rotation: crash-recovery` files and is used by BOTH `_latest_rotation_record`
and `cmd_status --record latest` (including its `--wait` re-glob), so a
`detected` (or any crash-recovery) record is never surfaced as a rotation.

## Evidence

New tests (red on pre-fix bytes, green on the build), all green:

- `test_heal_watch.py::test_detected_recovery_records_dedupe_one_per_death`
  — three polls of an unrecoverable death → exactly ONE `detected` record.
- `test_heal_watch.py::test_respawned_recovery_writes_fresh_file_per_outcome`
  — two `respawned` recoveries → two records (dedupe key is the still-open
  death, never suppresses healed recoveries).
- `test_rotate.py::test_latest_rotation_record_skips_crash_recovery` — a real
  `rotate-self` rotation survives a lexically-NEWER `detected` record: the
  rotation is returned, never the recovery.
- `test_rotate.py::test_latest_rotation_record_none_when_only_crash_recovery`
  — only crash-recovery records → None (no rotation to serve).
- `test_rotate.py::test_status_record_latest_skips_detected_record` — the
  falsifier head-on: `status --record latest <seat>` prints the rotation
  file, and the `detected`/`crash-recovery` name and body are ABSENT from
  stdout.

Run output (neighbours named, never the bare dir):
`test_heal_watch.py + test_rotate.py` → **166 passed**;
`test_send.py + test_session_start_bootstrap.py + test_session_start_seat_pre_spawn.py + test_rotate_recover.py + test_sensei_rotate_out_audit.py` → **243 passed**;
`test_bin_help_smoke.py + test_heal_watch.py + test_rotate.py` → **225 passed, 2 skipped**.

One node of the claim's three clauses (dedupe + status read) built and
proved. The other two clauses (inbox alert block; coalesced-nudge wake) are
separate seams owned elsewhere in the round.

## Agent Notes
Clause 3 of the alert-path claim: crash-recovery 'detected' records dedupe one-per-death (updated in place via heal._write_crash_recovery) and rotate._latest_rotation_record / status --record latest skip crash-recovery so a detected record is never read as a rotation. 6 new tests red-on-prefix/green-on-build; 225p+2s on harness, 166p on heal+rotate. Clauses 1 (inbox block) and 2 (coalesced-nudge wake) untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-232c7d9a, SL5.09). Accepted inconclusive_lean_proved:60 — the lean is the honest shape: clause 3 of three. WHAT THE INSTRUCTION SAID: dedupe detected records per post+generation and never let rotate.py status read a detected record as a rotation. WHAT THE MACHINE DOES, cited: heal.py `_write_crash_recovery` now calls new `_latest_detected_path` (reuses the newest `result: detected` crash-recovery file inside SEAT_DEAD_WINDOW_S=600 via `_write_rotation_record(..., path=existing)`), and rotate.py `_rotation_record_files` filters `rotation: crash-recovery` out of both `_latest_rotation_record` and `cmd_status --record latest` (incl. the `--wait` re-glob). I re-ran test_heal_watch.py + test_rotate.py -> 166 passed. NEAR MISS: a dedupe that keyed on the RECORD timestamp rather than refreshing it would mint a fresh file every 600 s; this one updates in place so the window slides and a continuously-dead seat stays one file. CAVEAT kept: the dedupe key is seat+600 s window, not literally post+generation, so two DISTINCT deaths inside one window would share a file — acceptable because the retry semantics live in `_crash_recovery_recorded` (respawned-only) and are untouched. Accepted.
<!-- THOUGHT:END -->
