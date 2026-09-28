---
id: hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row
mint_id: ee6d134abb1f43b3a04c93965818240e
type: hypothesis
parents:
  - experiment:a00-6b3e3540-f28c29
  - goal:g1
next_edges: []
edited_by: director-engine
scaffold_hash: 9bee4228981f1b46
season: 2
testable_claim: A posts.md row occupying this seats slot but unrecognized by _own_row_line is indistinguishable, to the publish path, from a genuinely absent row; both take the first-seating append branch instead of refusing. A fixture proves whether this reproduces and whether it is accepted behavior or a fail-open gap.
title: "key-row publish cannot tell a corrupted own-row from no own-row at all -- both append instead of refusing (assigned: director-engine)"
town: core
---
# hypothesis:key-row-publish-appends-instead-of-refusing-on-an-unrecognized-own-row

Source: TMM.165 (thought-master, 2026-09-25), reviewing director-engine's closure of
hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row. That closure proved a
bare-scalar (e.g. a genuine JSON string) row can never satisfy `_own_row_line`'s raw
`"name": "<seat>"` substring match -- but did not follow through on the consequence: when
`_own_row_line` recognizes NO row in the fetched posts.md as this seat's own, `_authority_row_content`
(rotate.py:10383-10390) returns `base` unchanged, and `_publish_row_to_authority`'s own-row-count
check (rotate.py:10488-10496) then takes the FIRST-SEATING branch and APPENDS the seat's new row --
the same branch that fires for a genuinely first-time seat. A row that is present but unrecognizable
(a corrupted name-cell, a bare-scalar shape, or any other mangling that breaks the raw substring
match) is publish-indistinguishable from no row existing at all, and the result is a silent append
rather than the named refusal the sibling hypothesis proved for a RECOGNIZED malformed row.

| | |
|---|---|
| claim | a posts.md row that should be this seat's (occupies its conceptual slot) but is not recognized by `_own_row_line` is indistinguishable, to the publish path, from a genuinely absent row -- both append a fresh row rather than refuse; a fixture proves this and states whether it is accepted behavior or a fail-open gap worth closing |
| test | a fixture with ONE already-present, seat-adjacent-but-unrecognizable row (e.g. a corrupted name-cell) on the fetched authority branch, then a re-key publish; assert on whether a second row gets appended (current behavior, to be confirmed) and record the resulting posts.md row count |
| falsifier | the append does NOT fire for this shape (i.e. some other check already refuses it), which would mean this concern does not reproduce and should be closed rather than fixed |

## Agent Notes
assigned: director-engine (PASS 5 residue follow-on, flagged by thought-master TMM.165, 09-25)
