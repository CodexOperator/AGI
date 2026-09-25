---
id: hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row
mint_id: 430f75eb88a44745ba7dc4017bb65d6f
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
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
