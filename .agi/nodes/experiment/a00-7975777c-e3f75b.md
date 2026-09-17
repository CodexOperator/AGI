---
id: experiment:a00-7975777c-e3f75b
mint_id: 84eed88ef4c54a45a2e23c5c43680b08
type: experiment
parents:
  - hypothesis:l4-a-posts-generation-is-measured-from-its-row-or-latest-record-never-from-a-handoff-header-it-can-hand-edit
next_edges: []
confidence: 0.8
edited_by: a00-76d8789e
evidence_runs:
  - experiment:a00-7975777c-e3f75b
line_ceiling: 40
loop: hypothesis:l4-a-posts-generation-is-measured-from-its-row-or-latest-record-never-from-a-handoff-header-it-can-hand-edit@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "CONJ1 (post gen measured): post row carrying generation cell + the real genless 072853Z-shaped record (rotate-self success, seated_at+session_id, no gen_after) + stale header 12 -> _generation_measured=(33,True,\"config:seats row\"), read=33, header never wins (pass). writer-wire: test_successor_row_write_writes_generation_for_non_prime exercises the real _successor_row_write through live write.submit admission -> non-prime row gets generation cell (pass). CONJ2 (header never gates): row cell=33 w/ header 12 -> 33; row genless w/ record gen_after 33 -> (33,True,\"latest rotation record\") + stderr \"header generation 12 ignored -- measured 33\" (pass). CONJ3 (measured=False named): no cell+no record+header 12 -> (0,False), read 0 (pass)."
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 0c3394a7493c95c8
season: 2
title: a-post-row-carries-its-measured-generation-so-check-5-and-the-meter-count
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7975777c-e3f75b

## Experiment

Conjunct 1 of `hypothesis:l4-a-posts-generation-is-measured-from-its-row-or-
latest-record-never-from-a-handoff-header-it-can-hand-edit`: make a real
post's generation MEASURED (measured=True) from its own row.

The parent probe falsified conjunct 1: a real non-prime post's row carries no
`generation` cell AND its latest rotation record carries no `gen_after`
(the non-prime records are GENLESS by the old goal:g15.25 design), so
`_generation_measured` returned (0, False) for the real post despite a
hand-editable header claiming 33/53. Conjuncts 2 and 3 (header never gates,
measured=False named) were already landed by the prior kid and are KEPT.

Chose option (A) — the claim's PRIMARY mechanism: the spawn-row write now
persists the `generation` cell in the post's OWN config:seats row, and
`_generation_measured` reads it (row-first, already implemented). This
SUPERSEDES goal:g15.25 claim (6-rows) ("non-prime never carries a gen");
the invariant's tests were reconciled to assert the row now carries the
measured number.

## Evidence

rotate.py `_successor_row_write` (the ONE identity-cell writer for a seat's
own row):
  cells = {"session_ref": session_ref, "window": window}
  cells["generation"] = generation           # was: if _is_prime_role(role)
  (the `_is_prime_role` guard on the gen cell is dropped; the return
   `_gen_field` always prints generation=N)

Tests (test_rotate.py, test_rotate_handover.py, test_rotate_recover.py):
- added `test_real_genless_record_resolves_from_row_cell_measured_true`: a
  real-shaped NON-prime record with NO gen_after + a row with a generation
  cell -> _generation_measured == (33, True, "config:seats row") and
  _read_generation == 33 (the parent's exact observed record shape).
- updated the >3 invariant tests that asserted the non-prime row is
  generation-less: they now assert own["generation"] == the measured value.
- updated `test_successor_row_write_never_writes_generation_for_non_prime`
  -> `..._writes_generation_for_non_prime`.

Suite: rotation/heal/sensei/verification sweep green
  test_rotate.py + test_rotate_handover.py + test_rotate_recover.py +
  startup + prepare + sensei_rotate_out_audit + g1517 + identity_main:
  621 passed
  heal + heal_seats + heal_sweep + heal_watch + sensei + sensei audits +
  verification + verify_suite_record + verify_unified + closeout + tail +
  verb + next: 417 passed
  rotate_alert_two_tree + autopsy + closeout_steps + complete +
  copilot_harness + first_decision + handoff_driven + latch_sweep +
  launch_wrapper + legal_hint + selfreap + sm36_residue + templates +
  verb_resolvers + heal_ack_rotation + heal_pin_reap:
  240 passed, 1 xfailed

Production diff (rotate.py, test files excluded): 10 added / 13 removed --
within both the 20-line ceiling and the 40-line re-brief bound.

Legacy-post note: an existing non-prime post whose row is STILL genless gets
its durable row cell on its NEXT rotation/recovery write (the writer now
writes it), restarting its chain from 1 — honest, engine-written, and never
from the hand-editable header. Conjunct 2 (header info-only) and conjunct 3
(measured=False named when no row cell and no record) are preserved.

## Agent Notes
Option A delivered: the spawn-row write now persists the generation cell in a non-prime post's own row, so _generation_measured reads it (row-first) as measured=True with the real number; rejoices g15.25 claim 6-rows which the invariant tests were reconciled to. Conjuncts 2 and 3 kept. Full rotation/heal/sensei/verification sweep green.

Parent review SM.93: ACCEPTED as proved. This kid fixes the concrete falsifier I ran against its predecessor (real non-prime record carries no gen_after): the engines spawn-row write (_successor_row_write) now persists the generation cell for EVERY role, so a real posts generation is measured (measured=True) from its own row. Independently re-probed all three conjuncts on the built bytes -- all pass, including the writer-wire (real write.submit admission) and header-never-gates. Verdict proved kept. CAVEAT (flagged to harvest): supersedes goal:g15.25 claim (6-rows) "non-prime posts are generation-less" -- deliberate, the two g15 claims genuinely conflict and the measure-me requirement wins; invariant tests reconciled. Also: a PRE-EXISTING genless row is still unmeasured (measured=False) until its next engine rotation/write persists the cell -- a named, honest migration transition, not a guess.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (SM.93) of THIS version: (1) WHAT THE TARGET SAID: conjunct 1 a posts generation is MEASURED (measured=True) from what the engine writes -- row cell primary; the record-gen_after fallback of the prior kid was dead because non-prime records are genless. (2) WHAT THE MACHINE NOW DOES: _successor_row_write drops the _is_prime_role guard on cells["generation"], so the ONE identity-cell writer persists the generation cell for every role; _generation_measured already reads row-first, so a posts real number is returned measured=True. Verified live: non-prime row via real write.submit admission carries generation=N (test_successor_row_write_writes_generation_for_non_prime); a post row w/ cell + the real genless record + stale header 12 -> (33,True). (3) NEAR MISS I ALMOST COUNTED AGAINST IT: the claims literal test-3 (record carries gen_after -> 33 w/ info line) is NOT satisfiable with real data -- non-prime records never carry gen_after -- so the operative path is the row cell, which this builds; the info-line path still holds for the synthetic case. (4) DEVIATION FROM STANDING RULE: supersedes goal:g15.25 claim (6-rows) "non-prime never carries a gen" -- a deliberate, node-documented conflict resolution (the two g15 claims are contradictory; measuring is the build order); invariant tests reconciled to match. CEILING: 10 prod lines <= 40.
<!-- THOUGHT:END -->
