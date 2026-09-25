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
DH.312 (director-engine, this session) landed the real fix: _parse_authority_row raises when a matching row is not a JSON object; _publish_row_to_authority catches ValueError and TypeError and returns a named authority: FAILED refusal before any fetch, commit or push completes. Its own experiment (a00-6b3e3540-f28c29) tested a list shape, a string-like shape, and a truncated shape, then found on adversarial self-review that the string-like fixture (the line dash quote name quote colon quote aa quote) is actually unparseable JSON rather than a valid bare JSON string, so the verdict was corrected from proved to inconclusive_lean_disproved and a genuine valid-JSON-string shape was banked as an open residue for a follow-up round. Closed that residue this session without a dispatch, by direct verification against the real imported rotate.py functions rather than a hand copy. _own_row_line matches only a raw, unescaped name-colon-seat substring in the line. _parse_authority_row succeeds and returns a non-dict only when json.loads accepts the whole trimmed line as one scalar or one unwrapped list. For a row to satisfy both predicates at once, the unescaped name-cell text has to sit inside valid JSON that still parses to something other than a dict at the top level -- structurally that is only reachable wrapped in a list, which the merged fix already tests. Any bare scalar (string, number, boolean, null) that would satisfy _own_row_line is not itself valid JSON containing that key-value text; any valid JSON string whose value happens to contain that text must escape its inner quotes, and escaping breaks the raw substring match. Verified exhaustively against rotate._own_row_line and rotate._parse_authority_row directly across eleven candidate shapes, including nested containers -- own_row_line came back true only for the list-of-dict family, never for a scalar. So the string shape named in the original testable_claim is unreachable as a matching row by construction, not merely untested: the claim holds for every shape the matching predicate can actually produce. No follow-up round needed; do not dispatch one for this residue.
<!-- THOUGHT:END -->

Residue closed by director-engine via direct code verification, no dispatch: the valid-JSON-string shape cannot occur as a matching row under _own_row_line; see THOUGHT for the eleven-shape check against the real functions.
