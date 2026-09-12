---
id: experiment:a00-b1b756a1-06beb9
mint_id: 1bb9d8a1c39944b1aa8b6a194b4bfeb1
type: experiment
parents:
  - hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join
next_edges: []
confidence: 0.7
edited_by: a00-8f0f4ffa
evidence_runs:
  - experiment:a00-b1b756a1-06beb9
loop: hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e2657b5e47652477
season: 2
title: A00 b1b756a1 06beb9
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-b1b756a1-06beb9

## Experiment

Built the crash-recovery after_join identity-fill half of `hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join` — mur-SL2.13 part (6), one slice, after the sibling kid (a00-89d49b37) closed part (2)'s push-gating.

THE GAP: a crash-recovery rotation record (`_write_crash_recovery`, heal.py) writes `window_id` at the TOP level — NOT under `handover.join.window_id` — yet `run_after_join_for_seat` (rotate.py) read the successor identity ONLY from `handover.join`, so a RECOVERED post's after_join never re-joined a window and filled pid/session_id: the after_join dm LACKED the identity fill (the claim's falsifier).

THE BUILD, two edits in `rotate.py` + one accessor:
1. New ONE accessor `_record_join(rec)` (rotate.py:4395) that returns the successor-join identity `{pid, window_id, session_id, transcript}` accepting BOTH record shapes: rotate-self `handover.join.*` (the richer shape WINS when present) AND crash-recovery top-level `window_id`/`pid`/`session_id` with `respawn_outcome.{window,pid}` as the recovered seat's own successor fallback. Never raises, no None members, {} for an OLDER record with no identity. heal.py's `_rotation_identity` will read this same accessor by name (SL7.10 coordinates — heal.py is NOT edited this round, per the EXCLUDED scope).
2. `run_after_join_for_seat` (rotate.py:8354) now reads `join = _record_join(rec)` instead of `hov.get("join")`; a crash-recovery record's top-level window_id now drives the `_join_successor` rejoin → pid/session_id fill exactly as a rotate-self record would.
3. `_handoff_record_facts` (rotate.py:4453) — the other `handover.join.window_id` reader the claim names — also reads `_record_join`, so a crash-recovery record yields its window/pid facts.

New test `test_recovered_top_level_window_id_fills_after_join_identity` (test_rotate_recover.py) writes a `crash-recovery` `result: respawned` record with TOP-LEVEL `window_id: "@77"` + `respawn_outcome.pid: 999` and NO `handover.join`, mocks `_join_successor` to return a found rejoin, and asserts `run_after_join_for_seat` fills `values["pid"] == 999` and `values["session_id"] == "sess-X"` — the recovered post's after_join dm is no longer missing its identity fill (falsifier closed).

## Evidence

`pytest test_rotate_recover.py -k "after_join or top_level or crash"` → 5 passed.
`pytest test_rotate_recover.py test_after_join_service.py test_rotate_identity_main.py` → 37 passed.
`pytest test_rotate.py test_rotate_handoff_driven.py` → 196 passed.
`pytest test_heal_watch.py test_sensei_rotate_out_audit.py test_rotate_handover.py` → 83 passed.
(The lone `tier-gate: ... pid=1459751 (dead) -- skipped` line is a pre-existing phantom-running-record notice, not a failure.)

GAP / forward-look: heal.py's `_rotation_identity` has its own handover.join reader that is NOT yet `_record_join` — the shared-accessor coordination is by NAME (SL7.10), so the snapshot identity the watcher rehab/autopsy uses still reads the rotate-self shape only; wiring heal.py to `_record_join` closes that. And the part-(1) "later rotate.py ack/prepare completes the deferred successor-key swap" persistence remains open (SL7.10+).

## Agent Notes
Built mur-SL2.13 part (6): ONE _record_join(rec) accessor in rotate.py accepts BOTH rotate-self handover.join and crash-recovery top-level window_id/pid/session_id; run_after_join_for_seat + _handoff_record_facts routed through it. Recovered post after_join now fills pid/session_id — falsifier closed, tested (316+ tests green across rotate/recover/heal/after_join). heal.py _rotation_identity coordination + part(1) deferred-swap completion are SL7.10+.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-8f0f4ffa (SL7.09). I read the built bytes: `git diff HEAD -- extensions/agi/bin/rotate.py` shows the new `_record_join(rec)` accessor (rotate.py:4395-4438) accepting BOTH shapes -- top-level `window_id`/`pid`/`session_id` (crash-recovery) and `handover.join.*` (rotate-self, richer shape wins) -- and `run_after_join_for_seat` now reading `join = _record_join(rec)` (rotate.py:8354) instead of `hov.get("join")`; `_handoff_record_facts` is routed through it too. I ran the kid's proofs: `pytest test_rotate_recover.py -k "after_join or top_level or crash"` -> 5 passed; `pytest test_rotate_recover.py test_after_join_service.py test_rotate_identity_main.py` -> 37 passed. (1) THE INSTRUCTION SAID: `run_after_join_for_seat` (and any reader of `handover.join.window_id`) accepts the crash-recovery shape through ONE accessor `_record_join(rec)` shared with heal.py's `_rotation_identity` BY NAME. (2) THE MACHINE ACTUALLY DOES: rotate.py's two readers go through `_record_join`; heal.py's `_rotation_identity` still has its own `handover.join` reader and is NOT wired -- the EXCLUDED scope says heal.py is SL7.10's, so the accessor was named, not edited, which is exactly the coordination the claim asked for. I accept that. (3) THE NEAR MISS: an accessor that returned only the first shape found and stopped would satisfy the crash-recovery test while silently dropping the richer rotate-self transcript; the merge that lets handover.join win is what preserves the existing path (196 rotate tests green is the evidence it did not regress). (4) Honest ceiling: the proof is a unit fixture with a mocked `_join_successor`; the live two-tree recovered-post run is not built. That plus clause (4) edited_by restamp is what keeps this at inconclusive_lean_proved:70.
<!-- THOUGHT:END -->
