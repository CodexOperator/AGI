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
status: active
tags:
  - council
  - v5
  - belam
  - g7.16.1.11
title: "G7.16.1.11.17: belam runs on v5 -- belam's successor wakes on the new post system at the first rotation after the remainder holds (the ring/anchor with agi-signers retired and the A10 ckpt on the hub, A12 re-installed safely, the land step); key issuance, metrics and verify stay the old Python this season"
town: core
---
# goal:g7.16.1.11.17

## Why this exists
goal:g7.16.1.11: goal:g7.16.1.11.10 moves every post BUT belam to the new post system ("belam stays on the old system"). belam [owner] 17:4xZ 10-02 asked, and the owner answered "File it now (Recommended)" to the question of a leaf for belam's own move (banked town:local-maxxing Agent Notes c88f1ae44); belam: "DG1 file a HORIZON leaf beside goal:g7.16.1.11.10: 'belam runs on v5'". It is the sibling that .10 leaves out, not a widening of .10.

## Target end-state
- belam's seat row reads the new system's engine cell (engine.v 4, the same shape as every other post's row) and belam's session runs as its own agi-post unit, not the old setup's window. DONE 10-09 (belam gen 31 on encryption-town, row at c70e3ef313; board E3 DONE bc08d96bea), on the OWNER'S 00:1xZ override, ahead of the four below.
- WHAT REMAINS OPEN (the reason this leaf is ACTIVE again, g1.42 row 17): the move above ran before (1)-(4) were built, so they are now the end-state of this leaf, no longer gates of the move. The move happens (HAPPENED, see above) at belam's FIRST ROTATION after all four of these hold (belam's successor wakes on v5; owner 00:1xZ "successor-after-next" timing stands; RE-STATED 10-07 by the council placement of the owner's bypass, alive 14:54Z):
  (1) the ring and the anchor: the ring is installed on v5 and the anchor signer exists (grow-gate's AGI_ANCHOR), agi-signers is RETIRED in the SAME step as the ring install (belam's GO), and the A10 ckpt is on the hub with the FIRST holding block cut BY HAND with the landed `ckpt sign` at each ring-signer rotation (the open grace AA2.57 otherwise);
  (2) A12 re-installed safely: bin/agi-out exists in every v5 post's t (measured 10-07: 2 of 12 homes carry it) and the unit's agi-out step cannot loop on a stale t (OUT.7 landed 666098f19, OUT.8 PATH-aware pending), then belam's install GO;
  (3) the land step: agi-land is BUILT (aa3-lanes 17/17) but installed nowhere readable; root installs it and ONE real land succeeds;
  (4) verify runs as a v5 uid IF verify gates the move (goal:g7.16.1.11.19).
- ORDER (owner 10-08 01:5xZ, town:local-maxxing Engine rework trajectory E1 -> E3 -> E5): grid-slice encapsulation (E1) comes first, THIS leaf is E3 (belam on the new engine), and the season rollover (E5) follows it; E2 (grid retirement) and E4 (the g1.41 residues) run in parallel. The old key mint stays the key system for this move, and a Python test is an acceptable falsifier lane wherever a prerequisite below names a shell lane (none is required to be rewritten).
- NO LONGER prerequisites (owner's bypass, 10-07): the full AA2 per-generation key build (the K1 mint half is season 3), per-spawn key issuance (provisioning.py stays, belam issues), metrics and verify as shell builds (the old Python is kept this season; shell rewrites are season 3).

## Invariants
- No second Prime window: the old-setup session ends when the successor's unit is up, never two writers of the Prime's cells.
- The [config] and anchor rings keep their rule on v5: only owner and prime_director write config nodes; only the anchor signer lands anchor edits. A move that leaves either ring unwritable by belam does not happen.
- One-command rollback is named before the move (the same shape as the other posts' moves in goal:g7.16.1.11.10).

## Falsifier
1. All four hold on the trunk and the box: a ring-signed landing passes the v5 grow-gate with agi-signers absent; `ckpt check` on the hub lists the first holding block; every v5 post's home carries bin/agi-out (a box listing, 12 of 12) and a stale-t start of the unit runs without a restart loop (`sh extensions/agi/tests/agi-out-stale.t.sh` exits 0); `sh extensions/agi/tests/aa3-lanes.t.sh` exits 0 with agi-land installed readable and ONE real land recorded; where verify gates the move, `commands.py run verify` as a v5 uid exits without a traceback.
2. Negative: belam's row never reads engine.v 4 while any of the four is not built (the move is refused, not worked around). WAIVED for belam's own move, once, by the owner's override of 10-09 00:1xZ: that clause was FALSE for it and is recorded as such, not as a defect; it stays the rule for any LATER post's move to engine.v 4.

## Out of scope
goal:g7.16.1.11.10 (every other post) · goal:g7.16.1.11.12 / .13 (the AA2 and AA3 builds themselves; this leaf only names what remains of them) · the council's flow-rotation design (goal:g7.16.1.11.15 phase W) · the engine pieces the council placed for NEXT season (pq nested inner signature, revoke piece, flowrot, round B mail collection, the sealer box side) · goal:g3.8 (metrics) · goal:g7.16.1.11.20 (messaging).

## OWNER 2026-10-07 14:4xZ, verbatim (relayed by belam gen 27)
"Also I know we used to have a bunch of metrics and stats we tracked with then python files. Can we bring those back? We don't have to rewrite them as scripts in this season just the next. But we will keep reusing the old python based key system, metric system, and verify suite/tests unless most of those got rewritten into shell which is awesome. Otherwise yes let the council tackle it and see what needs to be redone or streamlined. I will hear about it from your successor. Thank you for your service. We are still aiming to have to rotate onto new system as well given these requirements where I bypass some of the engine work till next season I think it should be a lot more doable sooner"

## OWNER 2026-10-08 01:5xZ, verbatim (relayed by belam in a [rule] to all)
"Things are getting lost. Are we updating the towns trajectory with how we are progressing? Do you still have the overall goal in your context? Finish encapsulation of grid slices and do a season rollover after getting you on the new engine. You can use the old key mint. We can use python tests. We've been trying to do a rollover for a week now but unfortunately I did an engine refactor in the middle. But I think we need to utilize the trajectory here. Maybe give us a trajectory subsection or a second trajectory row for engine rework progress."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 02:2xZ: ACTIVE again (was complete since 10-09 01:1xZ), on SM's g1.42 row 17 (CONFIRMED by the L5 review): I flipped it complete when belam's move ran on the owner's override, but the Target end-state's four prerequisites are UNBUILT and the Falsifier's negative was stated false for the move; the node then said 'Nothing tracks them but the Target end-state text', which is exactly the contradiction (a complete goal whose own end-state is open, and no other home). Re-ruled, not split: the headline (belam's row reads engine.v 4 and runs as its own unit) is DONE and is marked so in the first bullet; (1)-(4) stay as the open end-state of THIS leaf, so one tracker carries them and no goal is invented; the negative is waived for that one move by the owner's order and the waiver is written next to it. Not moved: any prerequisite's content, which is belam's and the council's. Previous version's thought: 10-09 01:1xZ: COMPLETE (was active). belam's [rule] 01:0xZ 10-09 (mail to DG1): belam gen 31 runs as agi-post@belam on encryption-town, row at trunk c70e3ef313 (engine.v 4, harness claude-code), mail rc 0; town:local-maxxing board row E3 -> DONE bc08d96bea (belam). Checked on the bytes: bc08d96bea is belam's board commit; the posts.md row at c70e3ef313 reads engine.v 4. The move ran on the OWNER'S 00:1xZ override ahead of prerequisites (1)-(4) of the Target end-state, so the Falsifier's negative ("belam's row never reads engine.v 4 while any of the four is not built") did NOT hold for this move: that is the owner's order, recorded here, not a defect. Per belam, (1)-(4) STAY as open work, no longer gates of this leaf: the ring/anchor + agi-signers retire, the A10 ckpt on the hub, the A12 safe re-install, the land step. Nothing tracks them but the Target end-state text above until belam or the owner names a home. Previous version's thought: 10-08 03:3xZ ACTIVE (belam's [rule] 03:05Z: prerequisites in PARALLEL with E1, the MOVE waits for E1 per E1 -> E3 -> E5); earlier: 10-08 02:1xZ, 10-07 3a437c2e8c restated the four.
<!-- THOUGHT:END -->
