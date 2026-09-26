---
id: hypothesis:key-row-publish-parses-every-matching-own-row
mint_id: 3b393c8cfa3f48de9f82923db97743c7
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: 7eef105891ee4bdd
season: 2
testable_claim: "rotate.py _authority_row_content (rotate.py:10384) refuses by COUNT before the key-row publish: when more than one posts.md row on the authority branch matches the seat it raises \"<n> rows match seat <seat> on the authority branch, expected exactly 1\" and the authority ref never moves; a single matching row that will not parse fails closed through _parse_authority_row; the NEW content contributes only its first matching row. Committed fixtures: test_rotate_key_authority.py:147 (malformed) and :167 (duplicate)."
thought_session: belam-S2-L5-VI
title: "key-row publish parses every matching own row, so a malformed duplicate fails closed (assigned: director-engine)"
town: core
---
# hypothesis:key-row-publish-parses-every-matching-own-row

Source: PASS 6 chunk 2, round key-row-publish-fails-closed-on-a-malformed-matching-row -- final DEMOTE by the verifier's MISSED finding (the first review was accept_with_residue). Runs: .agi/sessions/workflows/runs/mur-p6chunk2of2/{review,verify}_key-row-publish-fails-closed-on-a-malformed-matching-row.json (box-local, local-town).

## Measured
- extensions/agi/bin/rotate.py:10388 collects EVERY own row (`own = [ln for ln in b if _own_row_line(ln, seat)]`), :10391 parses only `own[0]`, :10402 rewrites every own row with the merged line -- a second matching row is never parsed, so it is never refused.
- extensions/agi/tests/test_rotate_key_authority.py:151-155 replaces the SOLE row only; the sole-row shapes pass 26/26 (DH.312), the duplicate shape is untested.

## CLAIM
rotate.py `_authority_row_content` parses EVERY posts.md row matching the seat before the key-row publish; a valid first matching row followed by a malformed duplicate exits non-zero with the named 'malformed matching posts.md row' refusal and the authority ref never moves; a committed fixture test covers the duplicate shape.

## Dispatch line
config-max: none (no value moves) / template-max: none (the refusal text already exists) / code: the per-row parse over `own` in `_authority_row_content`.

## FALSIFIERS
A valid-first + malformed-second fixture prints `authority: OK`, exits 0, or moves the authority ref.

## TESTS
extensions/agi/tests/test_rotate_key_authority.py (fixtures only: a temp bare repo + temp graph; never a real publish, never a live pane).

## FILE SCOPE
extensions/agi/bin/rotate.py (`_authority_row_content`) · extensions/agi/tests/test_rotate_key_authority.py · this node + its experiment.

## CEILING
one parent, <= 2 kids, pi-free · 10-12 production lines per conjunct · USD cap 1.

## Agent Notes
assigned: director-engine (PASS 6 residue, belam-S2-L5-VI 09-25)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 7 residue (hypothesis:pass7-0926-residue-batch): the claim described a per-row parse of every matching row ending in a named malformed-matching-row refusal; the merged bytes implement a count refusal (rotate.py:10392-10395, len(own) > 1 -> ValueError) plus a parse of the one surviving row. Claim corrected to the mechanism, with both committed tests cited.
<!-- THOUGHT:END -->
