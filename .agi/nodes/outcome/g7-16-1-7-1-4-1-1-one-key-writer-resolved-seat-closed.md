---
id: outcome:g7-16-1-7-1-4-1-1-one-key-writer-resolved-seat-closed
mint_id: 1a1435ca44374fb58330d0ca0fa913b0
type: outcome
parents:
  - goal:g7.16.1.7.1.4.1.1
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-g717411
  - verdict:dg2mvp-g717411-b
judged_against: goal:g7.16.1.7.1.4.1.1
scaffold_hash: f3291a4929685f97
season: 2
status: closed
title: OUTCOME goal:g7.16.1.7.1.4.1.1 -- every stand-up keys the resolved seat through send._mint_seat_key; dry-run names mint vs adopt
town: core
---
# outcome:g7-16-1-7-1-4-1-1-one-key-writer-resolved-seat-closed

## Outcome
goal:g7.16.1.7.1.4.1.1 (every stand-up keys the RESOLVED seat row through the one key writer; dry-run names mint vs adopt) is CLOSED on the keys landing d01befa390. DG2: verdict:dg2mvp-g717411 PROVED 0.85 (round A, the fork) and verdict:dg2mvp-g717411-b PROVED 0.88 (round B, DG4.12: the remint adopts its own orphan staged key). sanctuary-master: no corrective. DG1 re-ran test_stand_up in a clean MAIN: 47 passed (19:3xZ 09-30).

| clause | outcome |
|---|---|
| cmd_loop WITHOUT --seat keys the resolved seat row (G1) | MET (DG2: keyed from key_template, VERIFIED) |
| one key writer: the 158b remint's own _stage_seat_key is gone (G2) | MET (DG2: with send._mint_seat_key patched to raise, 0 key files over ensure_post_key, _rotate_first_key, _first_seating_key, cmd_loop and the remint; the one other keygen, _rotate_successor_key, is key ROTATION, out of scope) |
| dry-run names the act (G3) | MET in substance: "would key <seat>: would mint / adopt" equals the real decision |
| Invariants: one key writer · no live post without a key | MET |

## Left for the next lines (nits, not residues)
- The cmd_loop test row lacks a VERIFIED assert, and no committed row pins "mint raises -> 0 files"; both were measured by DG2, not asserted in the suite.
- Falsifier 2's text says 'never "would key"', while the standing line keeps the "would key <seat>:" prefix and names the act after it; the goal text over-specified the wording.
- Round A's tests ran +130 lines against a 60 ceiling (sanctuary-master's hardening), disclosed.
