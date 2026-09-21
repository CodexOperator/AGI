---
id: hypothesis:l4-a-first-seating-on-an-existing-seat-reports-the-rows-generation-not-a-hard-coded-gen-1
mint_id: edb1783bcd664e979396ac225872412b
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 4b30cb4d80e39913
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.42 residue, mur digest wf_438874da-7a6 line (6), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: rotate.py:8552 _first_seating_run builds its values with gen=1 (:8586) and the first-seating record/announce use FIRST_SEATING_GEN (:3715 = 1; :3823/:3921/:3994) — right for a NEW seat, but a RE-SPAWN of an EXISTING seat (seats-launch of a seat whose config:seats row already carries generation N >= 1: a crash respawn, a hand relaunch) prints a bootstrap header 'gen 1' and a seat_row line 'generation: 1' while the ack file the same run writes carries gen_after = the real generation (the ack path reads the row); the successor's STARTUP disagrees with its own ack. CLAIM: _first_seating_run resolves gen as the row's generation when the seat already has a live row (>= 1), else FIRST_SEATING_GEN; the bootstrap gen, the seat_row generation:, the seating record and the ack file's gen_after all agree; a brand-new seat is unchanged. FALSIFIERS: a seats-launch on a fixture row with generation 4 prints 'gen 1' anywhere in the bootstrap; the ack file and the bootstrap disagree on gen; a new seat's first seating no longer records gen 1. TESTS: test_rotate_startup.py (SL7.42's file) — a re-spawn fixture with generation 4 asserting bootstrap gen == ack gen_after == 4; the existing new-seat test unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — _first_seating_run's gen resolution (one helper reading the own row); extensions/agi/tests/test_rotate_startup.py. EXCLUDED: FIRST_SEATING_GEN itself, the announce gate (the SL7.33 residue brief owns it), the ack writer, seats-launch's spawn leg. CEILING: one resolution, one test."
thought_session: sensei-director-genXIII-L13
title: a first-seating run of a seat that already has a row reports that row's generation in its bootstrap (gen, generation:) and its ack file agrees, never the FIRST_SEATING_GEN constant
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-first-seating-on-an-existing-seat-reports-the-rows-generation-not-a-hard-coded-gen-1

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
