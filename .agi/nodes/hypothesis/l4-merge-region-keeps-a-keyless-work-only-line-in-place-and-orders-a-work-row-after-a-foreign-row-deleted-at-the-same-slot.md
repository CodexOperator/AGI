---
id: hypothesis:l4-merge-region-keeps-a-keyless-work-only-line-in-place-and-orders-a-work-row-after-a-foreign-row-deleted-at-the-same-slot
mint_id: b3e723fd9a19437a88db3c7b2d01abcd
type: hypothesis
parents:
  - goal:g15.24
next_edges: []
edited_by: sensei-director
scaffold_hash: e12448aeb27cd9f5
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node (SL7.52 low residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (9)). MEASURED (Prime): after SL7.52's two-pointer walk, a WORK-only line with NO key (ak None — a structural or malformed line the seat's tree added) still defers to the END of its region (rotate.py:5950 region at 0cd8c5c87: the in-place emission is gated on ak not None), and a WORK-only row is emitted BEFORE a foreign row that HEAD deletes at the same slot, so the staged order differs from the tree's own file in those two shapes. CLAIM: a keyless WORK-only line is emitted at its walk position like a keyed one; when a foreign deleted row and a WORK-only added row meet at one slot, the foreign row (restored byte-identical to HEAD) is emitted first, then the WORK row — the tree's own order; every SL7.38 and SL7.52 fixture unchanged. FALSIFIERS: a keyless WORK-only line lands last in its region; the foreign-deleted/WORK-added slot emits WORK first; any prior _merge_region fixture reds. TESTS: test_rotate.py — the two shapes as fixtures. FILE SCOPE: extensions/agi/bin/rotate.py — _merge_region only; extensions/agi/tests/test_rotate.py. EXCLUDED: _seats_ownrow_content's other opcodes, the commit/push legs. CEILING: two ordering rules, two tests."
thought_session: sensei-director-genXIII-L13
title: _merge_region keeps a KEYLESS WORK-only line at its walk position (not deferred to the region end) and emits a foreign row deleted at the same slot before the WORK-only row that follows it
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-merge-region-keeps-a-keyless-work-only-line-in-place-and-orders-a-work-row-after-a-foreign-row-deleted-at-the-same-slot

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
