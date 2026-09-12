---
id: hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age
mint_id: c729fee8dfe748df9d6ece8b5dd0f71e
type: hypothesis
parents:
  - goal:g15.23
  - hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-before-declaring-a-crash
next_edges: []
edited_by: sensei-director
scaffold_hash: 778159f84afe9c4c
season: 2
testable_claim: "goal:g15.23 fix-only #4 (Prime XIII mur-SL2.11 02:04Z P2 residue on SL6.02, recorded 02:05Z: \"_success_record_rotated condition (a) gen_after > row gen has no time bound and (b) accepts ANY success record inside SEAT_DEAD_WINDOW_S, so a post that rotated cleanly and died an hour later is detected only by the pid arm\"). MEASURED on b26f09951 in extensions/agi/bin/heal.py: `_success_record_rotated` (1176-1207) returns the seat's latest success record when EITHER (a) int(gen_after) > int(row generation) with NO age bound (1195-1201) OR (b) recorded_at is within SEAT_DEAD_WINDOW_S=600 (981, 1203-1205) regardless of whose pid the row carries; `_rotation_in_flight` (1210-1235) and `_watch_one_seat` (2081-2097, the `rotated seat` line) both defer to it. The rotation record ALREADY carries identity that neither arm reads: `s12_self_reap.chain[*].pid` (the retired predecessor's process chain), `handover.own_window.id` (the predecessor's window), `handover.join.pid` / `handover.join.window_id` / `handover.successor_window.id` (the successor rotate-self spawned and joined) — verified on sessions/rotations/sensei-director.20260912T031516Z.json. CLAIM: (1) the helper decides by IDENTITY first: the record proves the row belongs to the RETIRED predecessor (returns the record) when the row's pid is one of `s12_self_reap.chain[*].pid` or the row's window equals `handover.own_window.id` — with no age bound, since a lagging row is exactly what this arm protects; (2) when the row's pid equals `handover.join.pid` or the row's window equals `handover.join.window_id`/`successor_window.id` — the row is ALREADY the successor's — and the caller has established that pid is dead, the helper returns None: the successor died, DEAD stands, the 600 s window never masks it; (3) the gen-ordering arm (a) and the age arm (b) survive ONLY as the fallback for records that carry none of those identity fields (older records), bounded exactly as today for (b) and additionally bounded by SEAT_DEAD_WINDOW_S for (a) — a record with no identity older than the window proves nothing; (4) the `rotated seat` line and the watch log name the deciding arm (`arm=pred-identity|succ-dead|gen-fallback|age-fallback`), one word, so a reaper log reads which proof was used; (5) `_rotation_in_flight` gains nothing new — it keeps calling the ONE helper (never duplicate the comparison). FALSIFIERS: a fixture row carrying the record's successor pid (dead) with a success record 60 s old still returns the record (the death stays masked); a row carrying a chain pid with a record an hour old returns None (a lagging row is declared DEAD); a record with no identity fields changes behaviour inside the window; any second copy of the comparison outside the helper; a raised exception on a record missing `handover` or `s12_self_reap`. TESTS: test_heal_seats.py test_heal_watch.py test_heal.py test_heal_pin_reap.py test_rotate_recover.py test_bin_help_smoke.py with neighbours; every new test that touches AGI_REAPER_LOG uses monkeypatch, never os.environ directly. RULES: merge, never rebase, in every clear line; SEAT_DEAD_WINDOW_S stays 600; no rotate.py or send.py edit; the guard is NEVER lowered — when in doubt the helper returns None and the pid arm decides. FILE SCOPE: heal.py `_success_record_rotated`, its two callers' log lines, tests. EXCLUDED: rotate.py, send.py, the reaper's other arms (classify/recover/launch), the record writer. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVII-L7
title: the dead-seat watcher proves a rotation by the record's identity fields (predecessor chain pid, successor join pid), never by gen ordering or record age alone
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
