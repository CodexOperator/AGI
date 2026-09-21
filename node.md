---
id: hypothesis:l4-one-resolved-generation-for-the-seating-record-the-alert-and-the-bootstrap-on-a-re-spawn
mint_id: 16c9ef2ccf5a4a858020ea7b1db9ca3c
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 15c64d2c2bb42b22
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.49 residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (1)). MEASURED (Prime): after SL7.49 the bootstrap and the announce read the row generation (_first_seating_run, rotate.py:8652 at 0cd8c5c87) but _seating_record (:3756) still writes gen_after: FIRST_SEATING_GEN and the rotation-alert dm still says generation 0 -> 1 on a re-spawn of an existing seat — three writers, two answers; and the `or FIRST_SEATING_GEN` at :8652 coerces a row generation of 0 to 1 while cmd_spawn (:1649-1651) keeps 0. CLAIM: _first_seating_run resolves the generation ONCE (a row generation, including 0 when the row says 0 — None/absent -> FIRST_SEATING_GEN) and passes that value to the seating record, the rotation-alert dm and the bootstrap, so all three agree byte-for-byte; a brand-new seat still records gen 1. FALSIFIERS: a re-spawn fixture with generation 4 writes a seating record whose gen_after != 4 or an alert dm not naming 4; a row generation of 0 reads as 1 anywhere in the three; a new seat's record changes. TESTS: test_rotate_startup.py — the SL7.49 re-spawn fixture extended to assert the record's gen_after and the alert text; a generation-0 case. FILE SCOPE: extensions/agi/bin/rotate.py — _first_seating_run's gen resolution and the two call sites (_seating_record, the alert composer) only; extensions/agi/tests/test_rotate_startup.py. EXCLUDED: cmd_spawn, FIRST_SEATING_GEN, the ack writer. CEILING: one resolved value threaded to two more writers, two tests."
thought_session: sensei-director-genXIII-L13
title: "a first seating on an existing seat resolves ONE generation and every writer uses it — the seating record and the rotation-alert dm no longer hard-code gen_after 1 — and generation: 0 is kept as 0, as cmd_spawn keeps it"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-one-resolved-generation-for-the-seating-record-the-alert-and-the-bootstrap-on-a-re-spawn

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
