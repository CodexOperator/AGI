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

## CORRECTIVE G6.2 -- closes mur-de-base-g6 g6-code (verify accept_with_residue: missed M1)
BASE      CUT FROM de-base-G6 tip 016ba8f26 (worktree /mnt/agi-ram/worktrees/de-base-G6). No merge. Never rebase.
1. Mutation blind spot -- extensions/agi/tests/test_project_agi_box.py -- the fixture's row box equals the projection's AGI_BOX (local-town), so a hardcoded "AGI_BOX=local-town" in engine.md:80 passes both tests. TRUE WHEN a row projects a fixture whose box is NOT local-town (run with AGI_BOX=<that box>) and asserts AGI_BOX=<that box>; paste the run of that mutation (hardcoded literal in a scratch copy) going red.
DEMOTED   review R1-R4 (all refuted by the g6 verify: house skip convention · no engine cell named box exists · the file IS the drop-in · env-file precedence out of diff) · notes (size annotation, default-box literal pre-existing, WT bytes, F3 cells) · verify M2 (F2 stays a gate run, never a test) · M3 (merge-scope fact).
FILE SCOPE extensions/agi/tests/test_project_agi_box.py · this node.  CEILING tests +20 · production 0 · Sonnet 5.5 subagent · 0 USD.

## RESULT G6.2 (director, closes mur-de-base-g6b residues: verify V3 + missed M1 M2)
NUMSTAT   git diff --numstat 016ba8f26 a3fdc5090 -> 8	7	extensions/agi/tests/test_project_agi_box.py (tests net +1 vs the +20 ceiling; production 0). G6 whole: git diff --numstat 6b536b730 a3fdc5090 -> engine.md 1/1, test_project_agi_box.py 47/7.
MUTATION  pasted by the G6.2 kid (scratch copy /tmp/g62mut/engine.md, "AGI_BOX=\(.box)" -> "AGI_BOX=local-town", the worktree untouched): FAILED test_mut[other-town] - assert 'AGI_BOX=other-town' in '...AGI_ROLE=director AGI_LADDER_TIER=1 AGI_BOX=local-town' -> 1 failed, 1 passed in 0.08s
REAL      test_project_agi_box.py on a3fdc5090: 3 passed in 0.19s (kid) · mur-de-base-g6b review accept, 3/3 MET.
MERGE     a3fdc5090 needs 016ba8f26 (verify M3): the chain lands whole at its last tip, never the corrective alone.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director closes mur-de-base-g6b in-loop (node prose only, TMM.327): RESULT G6.2 carries the two-operand numstat, the kid pasted mutation red and the merge-order note; review notes 1-2 refuted by the verify
<!-- THOUGHT:END -->
