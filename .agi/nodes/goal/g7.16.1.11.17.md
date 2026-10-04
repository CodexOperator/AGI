---
id: goal:g7.16.1.11.17
mint_id: 7de86aa8287d48109425855973721fb8
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.17
goal_kind: subgoal
origin: goal
scaffold_hash: f50e84cf3fd04e6c
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - belam
  - g7.16.1.11
title: "G7.16.1.11.17: belam runs on v5 -- belam's successor wakes on the new post system at the first rotation after four things hold (AA3 land built, AA2 per-generation keys built, a [config] ring on v5, the anchor signer)"
town: core
---
# goal:g7.16.1.11.17

## Why this exists
goal:g7.16.1.11: goal:g7.16.1.11.10 moves every post BUT belam to the new post system ("belam stays on the old system"). belam [owner] 17:4xZ 10-02 asked, and the owner answered "File it now (Recommended)" to the question of a leaf for belam's own move (banked town:local-maxxing Agent Notes c88f1ae44); belam: "DG1 file a HORIZON leaf beside goal:g7.16.1.11.10: 'belam runs on v5'". It is the sibling that .10 leaves out, not a widening of .10.

## Target end-state
- belam's seat row reads the new system's engine cell (engine.v 4, the same shape as every other post's row) and belam's session runs as its own agi-post unit, not the old setup's window.
- The move happens at belam's FIRST ROTATION after all four of these hold (belam's successor wakes on v5; owner 00:1xZ "successor-after-next" timing stands): (1) AA3 land is BUILT (agi-land exists: the lanes script of goal:g7.16.1.11.13 no longer exits 13); (2) AA2 per-generation keys are BUILT (the key work of goal:g7.16.1.11.12, held by the owner 21:3xZ 09-30 until the council design is accepted); (3) a [config] ring exists on v5 (today the [config] ring is write.py's role gate: config nodes may be hand-edited only by owner and prime_director, which belam exercises through write.py); (4) the anchor signer exists on v5 (grow-gate's AGI_ANCHOR: the anchor-signed schema and growth edits belam makes today, as for Z4 phase A).

- STATUS 06:0xZ (self-perpetuating's ruling from the landed text, trunk 5d9182afb): (3) the [config] ring and (4) the anchor signer are DESIGNED, and their builds are NESTED here as hypotheses: g716111-ab-a-config-node-edit-by-belam-lands-through-the-v5-ring-with-no-write-py-in-the-path (3: section AB's ring, belam writes the first version) and g716111-ab-the-anchor-signer-is-belams-generation-key-under-option-b-and-the-upgrade-to-the-owner-capsule-is-one-ring-line (4: option B, belam's generation key IS the anchor signer; option A = one ring line later). Both depend on the AB ring series under goal g7.16.1.11.12 (RING.4 first). The cross-box half of AA2 keys is section W (landed design), HELD on a second box and a real phone (AA2.55, W12-W15 UNRUN). The goal stays a HORIZON until those builds and AA3/AA2 hold.

## Invariants
- No second Prime window: the old-setup session ends when the successor's unit is up, never two writers of the Prime's cells.
- The [config] and anchor rings keep their rule on v5: only owner and prime_director write config nodes; only the anchor signer lands anchor edits. A move that leaves either ring unwritable by belam does not happen.
- One-command rollback is named before the move (the same shape as the other posts' moves in goal:g7.16.1.11.10).

## Falsifier
1. All four hold on the trunk: `sh extensions/agi/tests/aa3-lanes.t.sh` exits 0 or 2 (not 13) = AA3 land built; the AA2 per-generation-key hypotheses under goal:g7.16.1.11.12 read proved; a config-node edit by belam lands through a v5 ring with no write.py in the path; an anchor-signed edit lands through the v5 anchor signer. (Each of the last three is named by its own round's experiment; none is specified further here.)
2. Negative: belam's row never reads engine.v 4 while any of the four is not built (the move is refused, not worked around).

## Out of scope
goal:g7.16.1.11.10 (every other post) · goal:g7.16.1.11.12 / .13 (the AA2 and AA3 builds themselves; this leaf only names them as prerequisites) · the council's flow-rotation design (goal:g7.16.1.11.15 phase W).

## Agent Notes
Assigned to **director-general-1**.
