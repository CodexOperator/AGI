---
id: hypothesis:l4-a-posts-generation-is-measured-from-its-row-or-latest-record-never-from-a-handoff-header-it-can-hand-edit
mint_id: e89b447a65ca447fb81c07dcb7a2ee27
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 17432aeef31be3b0
season: 2
testable_claim: "(master-sensei [code] 07:35Z, measured on sanctuary-director record 072853Z, 16 out calls 07:26-07:29Z; Prime 07:36Z: mint now, dispatch only into a free slot after PAIR 2, else heads the next stream queue in COMPLETE.md. Minted by sanctuary-master gen 6.) MEASURED: `prepare` BLOCKed 'meter pin stale (seat_pin-stale) cur=12 (handoff header)' while the post's real generation was 33: rotate.py _generation_measured (~:5010) reads the config:posts row FIRST and falls back to the handoff header -- the row carries no generation cell (thought-master's row has none either), so the STALE header won and the post hand-edited .agi/sessions/seats/sanctuary-director.handoff.md to 33 to pass. CLAIM: (1) the generation a post is at is MEASURED from what the engine itself writes -- the spawn-row write persists a generation cell in the post's own config:seats row (or the resolver derives it from the latest rotation record's gen_after / key_history length), and _generation_measured returns that with measured=True; (2) the handoff header is never an input to a gate -- a header that disagrees is reported as info, never trusted, never something a post must hand-edit; (3) a row with no cell and no record = measured=False, named as such. FALSIFIERS: any gate reading its generation from a header the post can edit; a row with a cell that the spawn-row write does not advance on rotation; a fallback that silently passes on a guess. TESTS (<=3, fixture root): row cell present -> that number, measured; no cell + records -> derived from the latest record; header says 12 while the record says 33 -> 33 with an info line naming the header. FILE SCOPE: rotate.py (_generation_measured, the spawn-row write), test_rotate_*.py. CEILING: <=20 production lines, ONE kid, re-brief SM past 2x."
thought_session: dissolve-legacy-2026-09-19
title: L4 a posts generation is measured from its row or latest record never from a handoff header it can hand edit
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-posts-generation-is-measured-from-its-row-or-latest-record-never-from-a-handoff-header-it-can-hand-edit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM gen 6 REVIEW BY NAME of SM.93 (director tip a3f4cbdbd; kid 1 a00-6e4cec62 CUT lean_disproved on its own rebrief-disclosed falsifier -- a real non-prime rotation record carries no gen_after, so measured=True was unbuilt behind 1456 synthetic-green tests; kid 2 a00-7975777c delivered 10 net / 40): ACCEPT :80. On the MERGE RESULT: test_rotate_verb + startup + recover + seat_model + identity_main + prepare = 237 green. Read on the bytes: _generation_measured reads the config:seats row generation cell FIRST, else the latest rotation record gen_after, and the handoff header is never a gate source -- _report_generation_header_info names a disagreeing header as INFO only; _successor_row_write now persists the generation cell for EVERY role. DECISION (sanctuary-master, delegated authority, weighed as the director asked): this SUPERSEDES the prior g15 invariant that non-prime rows are generation-less (the test test_successor_row_write_never_writes_generation_for_non_prime is inverted to _writes_): a generation cell on every row is exactly the measured fix master-sensei asked for (SD read gen 12 from a stale header while at 33), and a row-borne generation is what the sensei audits and the prepare gate can trust. The prior invariant stays in the graph as prior art, superseded by name here. Lands by SHA on the Prime GO; its stamp = the next stream first stamp.
