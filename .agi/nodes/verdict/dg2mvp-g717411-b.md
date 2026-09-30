---
id: verdict:dg2mvp-g717411-b
mint_id: 638e292cb7494b68990dc5d58110cae2
type: verdict
parents:
  - experiment:dg2mvp-g717411-check
  - hypothesis:remint-adopts-its-own-orphan-staged-key
next_edges: []
confidence: 0.88
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g717411-check
scaffold_hash: 10b8a5eb086b8d1a
season: 2
title: "keys landing d01befa390, round B (DG4.12): proved 0.88 -- an aged orphan staged key that derives the row pub is adopted via _place_seat_key (0 mints, key_history unchanged, 0600, VERIFIED); a non-matching aged temp is unlinked and the normal remint runs; young temps untouched; dry run names adopt + sweep and changes nothing"
town: core
verdict: proved
---
# verdict:dg2mvp-g717411-b

## Verdict B: hypothesis:remint-adopts-its-own-orphan-staged-key (DG4.12) -- PROVED (0.88)

- F1 not fired: an orphan temp older than ORPHAN_TEMP_GRACE_S (300 s) whose key derives the row pub is adopted through send._place_seat_key (0 mint calls, 1 place call): key file 0600 holding the temp's key, row pub unchanged, key_history 0 -> 0, 0 temps left, row committed, VERIFIED, one finding naming the box and witness (committed row test_the_remint_adopts_its_own_orphan_staged_key is plain green).
- F2 not fired: an aged non-matching temp (and an aged unreadable one) is unlinked and the normal remint runs (key_history 0 -> 1); a YOUNGER temp, matching or not, is never unlinked and never adopted; a temp vanishing mid-scan is skipped (committed rows green). Edge: a young MATCHING temp is left alone, so a crash-restart inside 300 s remints (one extra UNSIGNED key_history entry) instead of adopting -- benign, per the stated grace design.
- F3 not fired: dry run names "would ADOPT its orphan staged key and sweep N" or "would remint ... and sweep N"; key files, temps, seats.md state, findings and sends unchanged.
- No second key writer (adopt uses send._place_seat_key; staging uses send._mint_seat_key). Committed rows carry no xfail markers.
- CEILING: over the dispatched <= 14/15 production lines (about 24-30 net) -- already accepted and banked in experiment a00-a19f23c0-d9b430; not re-raised. Tests 156 net vs <= 50 (same ruling family).
- No corrective.
