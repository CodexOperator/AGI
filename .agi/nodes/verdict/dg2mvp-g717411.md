---
id: verdict:dg2mvp-g717411
mint_id: 148cf6fd82694efa8d5160f711a56b39
type: verdict
parents:
  - experiment:dg2mvp-g717411-check
  - hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g717411-check
scaffold_hash: 4cafbf62643b196f
season: 2
title: "keys landing d01befa390, round A (goal:g7.16.1.7.1.4.1.1): proved 0.85 -- cmd_loop without --seat keys the resolved seat row (VERIFIED), rotate.py's stand-up paths mint only through send._mint_seat_key (_stage_seat_key gone; mint patched to raise -> 0 key files over 5 stand-up paths), spawn dry-run names mint vs adopt; key tests green; pin nits only"
town: core
verdict: proved
---
# verdict:dg2mvp-g717411

## Verdict A: hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat (goal:g7.16.1.7.1.4.1.1) -- PROVED (0.85)

- CLAIM 1 TRUE: cmd_loop without --seat keys the RESOLVED seat (rotate.py:3493); probe: unkeyed dummy row keyed and VERIFIED, one _mint_seat_key call for the seat name. Falsifier 1 (row has no pubkey afterwards) did NOT fire.
- CLAIM 2 TRUE: `_stage_seat_key` is gone; rotate.py's only keygen() is `_rotate_successor_key` (a key-rotation writer, out of scope per DG1 and named by the hypothesis). The remint stages through send._mint_seat_key(stage=True) and places through send._place_seat_key; caller probe = _mint_seat_key on both the unkeyed-mint and remint paths. Negative probe: mint patched to raise -> 0 key files from ensure_post_key, _rotate_first_key, _first_seating_key, cmd_loop, the 158b remint. Falsifier 2 did NOT fire.
- CLAIM 3 TRUE: spawn's dry plan prints "would mint" / "would adopt" matching the real decision (shared _key_decision). Falsifier 3 (would key with no adopt) did NOT fire. Wording note: the line is "would key <seat>: would adopt" -- the standing `would key` prefix stays, so the goal's literal "never 'would key'" cannot hold; the act is named, which is the intent.
- Tests: test_stand_up 47, test_send -k key 39, test_seatsig 13, test_rotate -k "key or seat" 89: all green.
- CEILING: production net +24 (<= 40); tests +130 net vs <= 60 (hardening commits 20da4f9d12 / 802577c1bd, SM-reviewed).
- Pin gaps, no behaviour gap: committed cmd_loop row does not assert VERIFIED; the goal's negative (mint raises -> 0 files) has no committed row. No corrective written (test-pin nit, not a conjunct).
