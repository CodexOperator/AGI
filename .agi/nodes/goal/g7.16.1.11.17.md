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
title: "G7.16.1.11.17: belam runs on v5 -- belam's successor wakes on the new post system at the first rotation after the remainder holds (the ring/anchor with agi-signers retired and the A10 ckpt on the hub, A12 re-installed safely, the land step); key issuance, metrics and verify stay the old Python this season"
town: core
---
# goal:g7.16.1.11.17

## Why this exists
goal:g7.16.1.11: goal:g7.16.1.11.10 moves every post BUT belam to the new post system ("belam stays on the old system"). belam [owner] 17:4xZ 10-02 asked, and the owner answered "File it now (Recommended)" to the question of a leaf for belam's own move (banked town:local-maxxing Agent Notes c88f1ae44); belam: "DG1 file a HORIZON leaf beside goal:g7.16.1.11.10: 'belam runs on v5'". It is the sibling that .10 leaves out, not a widening of .10.

## Target end-state
- belam's seat row reads the new system's engine cell (engine.v 4, the same shape as every other post's row) and belam's session runs as its own agi-post unit, not the old setup's window.
- The move happens at belam's FIRST ROTATION after all four of these hold (belam's successor wakes on v5; owner 00:1xZ "successor-after-next" timing stands; RE-STATED 10-07 by the council placement of the owner's bypass, alive 14:54Z):
  (1) the ring and the anchor: the ring is installed on v5 and the anchor signer exists (grow-gate's AGI_ANCHOR), agi-signers is RETIRED in the SAME step as the ring install (belam's GO), and the A10 ckpt is on the hub with the FIRST holding block cut BY HAND with the landed `ckpt sign` at each ring-signer rotation (the open grace AA2.57 otherwise);
  (2) A12 re-installed safely: bin/agi-out exists in every v5 post's t (measured 10-07: 2 of 12 homes carry it) and the unit's agi-out step cannot loop on a stale t (OUT.7 landed 666098f19, OUT.8 PATH-aware pending), then belam's install GO;
  (3) the land step: agi-land is BUILT (aa3-lanes 17/17) but installed nowhere readable; root installs it and ONE real land succeeds;
  (4) verify runs as a v5 uid IF verify gates the move (goal:g7.16.1.11.19).
- NO LONGER prerequisites (owner's bypass, 10-07): the full AA2 per-generation key build (the K1 mint half is season 3), per-spawn key issuance (provisioning.py stays, belam issues), metrics and verify as shell builds (the old Python is kept this season; shell rewrites are season 3).

## Invariants
- No second Prime window: the old-setup session ends when the successor's unit is up, never two writers of the Prime's cells.
- The [config] and anchor rings keep their rule on v5: only owner and prime_director write config nodes; only the anchor signer lands anchor edits. A move that leaves either ring unwritable by belam does not happen.
- One-command rollback is named before the move (the same shape as the other posts' moves in goal:g7.16.1.11.10).

## Falsifier
1. All four hold on the trunk and the box: a ring-signed landing passes the v5 grow-gate with agi-signers absent; `ckpt check` on the hub lists the first holding block; every v5 post's home carries bin/agi-out (a box listing, 12 of 12) and a stale-t start of the unit runs without a restart loop (`sh extensions/agi/tests/agi-out-stale.t.sh` exits 0); `sh extensions/agi/tests/aa3-lanes.t.sh` exits 0 with agi-land installed readable and ONE real land recorded; where verify gates the move, `commands.py run verify` as a v5 uid exits without a traceback.
2. Negative: belam's row never reads engine.v 4 while any of the four is not built (the move is refused, not worked around).

## Out of scope
goal:g7.16.1.11.10 (every other post) · goal:g7.16.1.11.12 / .13 (the AA2 and AA3 builds themselves; this leaf only names what remains of them) · the council's flow-rotation design (goal:g7.16.1.11.15 phase W) · the engine pieces the council placed for NEXT season (pq nested inner signature, revoke piece, flowrot, round B mail collection, the sealer box side) · goal:g3.8 (metrics) · goal:g7.16.1.11.20 (messaging).

## OWNER 2026-10-07 14:4xZ, verbatim (relayed by belam gen 27)
"Also I know we used to have a bunch of metrics and stats we tracked with then python files. Can we bring those back? We don't have to rewrite them as scripts in this season just the next. But we will keep reusing the old python based key system, metric system, and verify suite/tests unless most of those got rewritten into shell which is awesome. Otherwise yes let the council tackle it and see what needs to be redone or streamlined. I will hear about it from your successor. Thank you for your service. We are still aiming to have to rotate onto new system as well given these requirements where I bypass some of the engine work till next season I think it should be a lot more doable sooner"

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-07 14:5xZ: the owner's bypass (old Python kept this season, shell rewrites = season 3) narrowed the four prerequisites; the council (alive 14:54Z, sp 14:48Z, aio 14:51Z measured lines) placed the remainder as ring/anchor + agi-signers retire + A10 ckpt on the hub, A12 re-install, the land step, verify as a v5 uid only if it gates the move. Was: AA3 land built, AA2 per-generation keys built, a v5 [config] ring, the anchor signer. Status stays horizon: promoting it to active is the next belam's call (banked).
<!-- THOUGHT:END -->
