---
id: experiment:a00-8584ff07-645be9
mint_id: 33755c445a7345608420c900786bfe8d
type: experiment
parents:
  - hypothesis:l4-the-watcher-reads-a-recovery-records-top-level-identity-and-every-arm-reaches-the-log
next_edges: []
confidence: 0.85
edited_by: a00-8d21fb68
evidence_runs:
  - experiment:a00-8584ff07-645be9
loop: hypothesis:l4-the-watcher-reads-a-recovery-records-top-level-identity-and-every-arm-reaches-the-log@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b93699016a0434f3
season: 2
title: A00 8584ff07 645be9
town: core
verdict: inconclusive_lean_disproved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-8584ff07-645be9

## Experiment

Closed the SL7.10 gap: does the watcher actually READ a crash-recovery record's
identity, and is the accessor honest about the REAL shape the producer writes?
Two test-first claims, then fixed the code to match reality.

**(A) ROUND-TRIP — real producer, real bytes.** Built a crash-recovery record
by calling the REAL producer `heal._write_crash_recovery` (through the `_rot_shim`
and, independently, the real `rotate` module) into a tmp rotations dir, loaded
what it wrote, and ran `_rotation_identity` on it:
```
real accessor -> ([], [], [], ['@10'])
```
The producer (`_write_crash_recovery`) emits top-level `window_id` = the recovery
target window, and NO top-level `pid` and NO top-level `session_id` (the dead
predecessor's pid/session ride in nested `row`; the successor's real pid in
`respawn_outcome`). So `_record_join`'s earlier `rec.get("pid")` and
`rec.get("session_id")` reads never fire on any real record — the prior unit
test passed against a HAND-ROLLED dict, not the writer's output (the near-miss
parent review flagged). **Fixed:** `_record_join` now reads exactly `window_id`
on the crash-recovery branch, and drops the dead pid/session_id reads;
docstrings updated.

**(B) REACHABILITY — the branch is structurally UNREACHABLE from the watcher.**
`rotate._rotation_record_files` explicitly skips any `rotation: crash-recovery`
record (`if ... == "crash-recovery": continue`), so `_latest_rotation_record`
returns None for a seat whose only record is a crash one, and
`_success_record_rotated` further gates on `result == "success"` (a recovery
record reads `respawned`/`detected`). Empirical, real rotate module:
```
record files count (crash excluded): 0
latest_rotation_record: None
```
**Therefore the watcher CANNOT read a crash-recovery record's identity** from
`_watch_one_seat`/`_rotation_in_flight` — the crash-recovery branch of
`_record_join` is DECORATIVE for the watcher. Per instructions I did NOT lower
the guard (a recovery record's successor is the RESPWN target, not a rotation
predecessor); the code comment and this node document the finding plainly.
The succ-dead arm reaching the log remains proved (`test_succ_dead_arm_reaches_log`).

## Evidence

Tests added/updated in `extensions/agi/tests/test_heal_watch.py`:
- `test_record_join_reads_both_record_shapes` — crash-recovery case now asserts
  the honest shape: succ_pids stays empty (producer emits no top-level pid),
  succ_windows reads top-level window_id.
- `test_crash_recovery_record_roundtrip_real_producer` (A) — real writer → reads
  succ window `@10`; asserts NO top-level pid/session_id exist.
- `test_crash_recovery_record_unreachable_from_watcher` (B) — after writing only
  a crash-recovery record for a seat, `_success_record_rotated` returns (None,None)
  and `_rotation_in_flight` is False; accessor CAN read it when handed directly.

Code change (FILE SCOPE `extensions/agi/bin/heal.py` only): `_record_join`
crash-recovery branch now reads only top-level `window_id`, with a comment
documenting the unreachability and the "do not lower the guard" rule.

Suite: test_heal_watch.py 34 passed; test_sensei_wake_audit + test_rotate 238
passed / 3 skipped; test_heal_seats + test_rotate_identity_main +
test_heal_pin_reap 45 passed. rotate.py, send.py, the reaper arms and
SEAT_DEAD_WINDOW_S untouched.

## Verdict reasoning

The hypothesis claims the watcher reads a recovery record's top-level identity.
The accessor CAN read it (round-trip proved), but the WATCHER structurally cannot
(reachability disproved — discovery excludes crash-recovery records). The claim
as stated, about the watcher path, does not hold; this is the honest
correctness-preserving negative finding the parent requested. Lean disproved.

## Agent Notes
watcher CANNOT read crash-recovery identity (unreachable by design, verified with real rotate module); accessor made honest about real producer shape (top-level window_id only). Round-trip + reachability tests added; suites green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8d21fb68, SL7.10). WHAT THE INSTRUCTION SAID: the target node claims cl.1 "the watcher reads a recovery records top-level identity", falsifier "a crash-recovery record with top-level window_id yields no identity". WHAT THE MACHINE ACTUALLY DOES: verified independently. (a) rotate.py `_rotation_record_files` L4301-4302 literally `if rec.get("rotation") == "crash-recovery": continue` -- with the comment "a crash-recovery is NEVER a rotation" -- so `_latest_rotation_record` can never hand a crash-recovery record to `_rotation_identity`; and `_success_record_rotated` adds `result != "success" -> (None,None)`, which a respawned/detected record also fails. The crash-recovery branch of `_record_join` is therefore UNREACHABLE from the watcher, not merely unexercised. (b) The corrected accessor now reads exactly top-level window_id, which is the one identity field `_write_crash_recovery` emits (verified: heal._rotation_identity of a real-producer record -> ([],[],[],["@310"])); the earlier pid/session_id reads were phantom and are gone. THE NEAR MISS: satisfying cl.1 by lowering the exclusion or admitting recovery records as rotations would make the branch reachable and BREAK the design rule that a crash-recovery is never a rotation proof -- a "fix" that passes the falsifier while removing the guard. The kid refused it; that refusal is the correct behaviour and is recorded in-code. ACCEPTED: (A) and (B) both real; 34 tests pass; the disproof is a correctness-preserving negative finding, not a failure to build. VERDICT: the node is honest at inconclusive_lean_disproved:85 for the watcher-path claim, while clauses 2 and 3 of the parent hypothesis remain proved by experiment:a00-887a80cc-6cb719.
<!-- THOUGHT:END -->
