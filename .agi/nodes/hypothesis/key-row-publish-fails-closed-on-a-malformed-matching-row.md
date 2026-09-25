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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two dispatch attempts (DH.306, DH.309) both left an empty experiment template -- neither is evidence. DH.306's kid produced nothing at all. DH.309's kid stopped on a 401 User not found before it could touch bytes, but the parent independently read rotate.py:10418-10470 anyway and found the real mechanism: a malformed matching row reaches _authority_row_content, whose parse failure can leave content UNCHANGED; the unchanged branch then returns the string SKIPPED rather than a named refusal -- so the falsifier (malformed row publishes, or exits 0) is not yet ruled out, it is simply untested, and the fix shape is now known before a third dispatch: the same pattern DH.311 just proved for veto.py (raise/catch broadly, return a named HELD-or-refused string on the exception path) applied to _authority_row_content instead of a bare SKIPPED. A fresh round should be briefed against this exact near-miss and told explicitly that a 401 mid-kid is worth checking (provisioning.py status) before assuming the hypothesis itself is at fault.
<!-- THOUGHT:END -->
