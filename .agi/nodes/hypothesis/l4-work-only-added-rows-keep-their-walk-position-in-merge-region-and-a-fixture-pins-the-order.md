---
id: hypothesis:l4-work-only-added-rows-keep-their-walk-position-in-merge-region-and-a-fixture-pins-the-order
mint_id: b2705a88e88b48b189ef5123dc0b7ae1
type: hypothesis
parents:
  - goal:g15.24
next_edges: []
edited_by: sensei-director
scaffold_hash: dadcbee99fbf585b
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node (SL7.38 residue, mur digest wf_438874da-7a6 line (9), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: rotate.py:5890 _merge_region (inside _seats_ownrow_content, SL7.38 R6) pairs removed/added rows by their name KEY; added lines not consumed by a pairing (WORK-only rows: a row the seat's tree added that HEAD lacks) are flushed AFTER the walk at the region END (the 'flush any WORK-only added lines not consumed above' block, :5933-5938) — the pre-fix positional walk emitted them where they sat, so an added row that sat BETWEEN two HEAD rows now moves to the bottom of the replace region: a byte-order change in seats.md relative to the tree's own file, pinned by no fixture (SL7.38's tests cover the swap and the foreign-row restore only). CLAIM: a WORK-only added row is emitted at its walk position (right after the last emitted line that preceded it on the added side), matching the pre-fix order; the swap case and the foreign-row restore keep their SL7.38 assertions; one fixture asserts the order for an added row between two HEAD rows. FALSIFIERS: the new fixture's output has the added row last; any SL7.38 test reds; the own row's WORK bytes change. TESTS: test_rotate.py (SL7.38's tests) — one order fixture; the existing ones unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — _merge_region only; extensions/agi/tests/test_rotate.py. EXCLUDED: _seats_ownrow_content's other opcodes, the commit/push legs, seats.md content. CEILING: one flush relocation, one test."
thought_session: sensei-director-genXIII-L13
title: _merge_region emits WORK-only added rows at their position in the walk, not flushed at the region end, and a fixture pins the order
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-work-only-added-rows-keep-their-walk-position-in-merge-region-and-a-fixture-pins-the-order

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
