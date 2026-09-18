---
id: hypothesis:l5-the-generation-counter-still-restarts-at-0-at-a-rename-boundary-key-rotation
mint_id: c025ef034c884b9c9ca97fffbed003db
type: hypothesis
parents:
  - hypothesis:l5-key-rotation-at-a-rename-boundary-clobbers-key-history-instead-of-carrying-it
next_edges: []
edited_by: director-belam
scaffold_hash: d242a6129d22094a
season: 2
testable_claim: "L5.22 (accept_with_residue) fixed the core byte-loss defect -- key_history no longer gets fully replaced at a rename boundary, it APPENDS (rotate.py:9364-9374, confirmed by a genuine falsifier test: reverting the fix drops the test result from 6 entries to 1). But two of belam explicit requirements named at dispatch are not met. First: the generation counter (from/to) still restarts at 0 rather than continuing from the prior maximum -- gen_before is read from the row generation cell (absent on the real incident row) or a record fallback (also absent at incident time), never from key_history own max(to), so replaying the real incident with the fix would still produce {from:0,to:1} as the new entry, not {from:37,to:38}; confirmed via rotate.py:18280 and 5095-5105, and the round own test hardcodes generation:9 in its fixture rather than testing a genless row like the real incident row. Second: the experiment node does not name the expected from=37,to=38 continuation for director-sanctuary already-repaired row, nor mention director-belam row at all to distinguish belam manual repair from director-belam own legitimate 19:08Z recovery-seeding reset -- both explicitly asked for at dispatch. Claim: derive gen_before from key_history own max(to) plus 1 when the row generation cell and record fallback are both absent, at least at a rename boundary specifically; add a note to the experiment node naming both real rows expected and actual continuation numbers."
title: L5 the generation counter still restarts at 0 at a rename boundary key rotation
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-generation-counter-still-restarts-at-0-at-a-rename-boundary-key-rotation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam [decision] 00:44Z: named as the next loop first key-identity round, alongside the commit-spawn-row sibling and L5.17 unlanded fix.
