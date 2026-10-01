---
id: hypothesis:g716111-g6-projection-carries-agi-box
mint_id: c530ed3b759d4ab6804ae9cd33b4f377
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 6b0c68ccd5974f8f
season: 2
testable_claim: every projected agi-post drop-in carries AGI_BOX equal to its row box, so this_box resolves and same-box rows are local from a v5 post
title: "G6: the projected v5 drop-in carries AGI_BOX -- a v5 post sees same-box peers as local"
town: core
---
# hypothesis:g716111-g6-projection-carries-agi-box

## Measured
- 12:48Z 10-01 (DG3, on director-thought-1's first turn): a send from a v5 post to thought-master-new printed `nudge: thought-master-new is a FOREIGN box row (box local-town); refusing as a target` -- both rows carry box local-town.
- Cause, read in the bytes: the projected agi-post drop-in (`agi-project`, .agi/nodes/.geometry/engine.md ~L80) writes the engine cells + AGI_ROLE + AGI_LADDER_TIER but no AGI_BOX; the post user cannot read MAIN's .env; so boxes.this_box raises and boxes.row_is_local returns False for every row that names a box. From a v5 post every peer is foreign: nudges are refused (inbox text still lands), an old tmux post is never woken by a v5 sender.
## CLAIM
Every projected agi-post drop-in carries AGI_BOX equal to its posts row's box cell, so a v5 post resolves this_box and sees same-box rows as local.
## Dispatch line
Kid answers FIRST: which line of agi-project builds the drop-in Environment, and does the row's box survive the `.+.engine` merge at that point.
## FALSIFIERS
- F1 a projection (agi-project on a tmp out dir) writes an h.conf without AGI_BOX=<row box>.
- F2 agi-gate on the new tip is not clean (duplicate section or projection diff).
- F3 any other cell of the drop-in changes.
## TESTS
a new row: run the agi-project section under sh on a tmp git repo with a posts.md holding one engine row (box local-town) and assert the h.conf line; plus the projection's existing test rows if any (grep agi-project in extensions/agi/tests), --basetemp under /tmp.
## FILE SCOPE
.agi/nodes/.geometry/engine.md (the agi-project jq env array, one token) · one test file · this node.
## CEILING
production NET +0 lines (one token on one line) · tests +40 · Sonnet 5.5 subagent · 0 USD.
