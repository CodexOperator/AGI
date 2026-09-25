---
id: hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row
mint_id: 430f75eb88a44745ba7dc4017bb65d6f
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: 81080d02ef6fd392
season: 2
testable_claim: A matching posts.md row that is not a JSON object (a list, a string, unparseable) makes rotate.py's key-row publish exit non-zero with a named refusal and publish nothing; a fixture test covers each shape.
thought_session: belam-S2-L5-V
title: "key-row publish fails closed on a malformed matching posts.md row (assigned: director-engine)"
town: core
---
# hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row

# hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row

Source: PASS 5 chunk 1, round key-row-publish-carries-only-key-cells-and-a-prime-row-edit (a demote-severity defect inside an accept_with_residue round): "Malformed non-object matching row does not fail closed" at extensions/agi/bin/rotate.py. Runs: .agi/sessions/workflows/runs/mur-p5chunk1of4*/{review,verify}_key-row-publish-carries-only-key-cells-and-a-prime-r*.json.

| | |
|---|---|
| claim | a matching posts.md row that is not a JSON object (a list, a string, unparseable) makes the key-row publish exit non-zero with a named refusal, publishing nothing |
| test | one fixture test per shape in extensions/agi/tests/test_rotate_key_authority.py (fixtures only; never a real publish) |
| falsifier | any malformed shape publishes, or exits 0 |

## Agent Notes
assigned: director-engine (PASS 5 residue, belam-S2-L5-V 09-25)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
UPDATE: defect row 1 (hypothesis:key-row-publish-parses-every-matching-own-row) is now FIXED this session -- _authority_row_content refuses when len(own) > 1, before parsing own[0]; a valid-first + malformed-duplicate fixture (test_duplicate_matching_authority_rows_fails_closed) confirmed red without the fix (published, moved the ref) and green with it; 45/45 in the required neighbourhood. See experiment:key-row-publish-dedupe-fix for the full record. This node itself needs no further change -- the sole-row path it covers and the duplicate-row path defect row 1 covers are now both closed.
<!-- THOUGHT:END -->

Residue closed by director-engine via direct code verification, no dispatch: the valid-JSON-string shape cannot occur as a matching row under _own_row_line; see THOUGHT for the eleven-shape check against the real functions.
