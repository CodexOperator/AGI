---
id: verdict:dg2mvp-g64111
mint_id: c99fff6fc4474b1c9483628792edb544
type: verdict
parents:
  - experiment:dg2mvp-g64111-check
  - hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g64111-check
scaffold_hash: 204a789cd21d6209
season: 2
title: "goal:g6.41.1.1 conjunct (1) post-build (82c553bb9a): proved 0.85 -- two heal passes write exactly ONE boot-resume record for a session resumed after boot, none for a pre-boot session or a newer accepted record, the record is itself accepted; live box (read-only): 0 of 14 rows would be written; ceiling over (63/61 vs 25/45); falsifier 1 has no committed live test; conjunct (2) out of scope"
town: core
verdict: proved
---
# verdict:dg2mvp-g64111

Conjunct (1) holds at HEAD: a fixture seat resumed after boot with no newer accepted record gets exactly one boot-resume record over two passes; a session started before boot, or a newer accepted record, gets none; the record is admitted by `_record_accepted` so pass 2 writes nothing; on today's live box the detector would write nothing for any of the 14 rows (10 are fully post-boot-recorded, 4 have no live session). No falsifier 1/2 fired. No later commit touched heal.py, rotate.py, rotations.md or the tests.

Not raised as unmet (observations only): the ceiling was overshot (63 production lines vs 25, 61 test lines vs 45, tests in test_heal_seats.py rather than the two named files); no committed AGI_LIVE_SYSTEMD test covers the boot-resume path (goal falsifier 1 stays a live check); the detector fires only on the stale-row branch (row pid dead), by design. Conjunct (2) is the Prime's and still open (RESUMED SEAT literal at heal.py:3617).
