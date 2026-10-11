---
id: goal:g7.16.1.11.20
mint_id: 44e5a6556a66404bb61eed5206776034
type: goal
parents:
  - goal:g7.16.1.11
  - goal:g7.32
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.20
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 40c82dd9c7a5ef3e
season: 2
seeds:
  - goal:g7.16.1.11
  - goal:g7.32
status: active
tags:
  - council
  - v5
  - messaging
  - g7.16.1.11
title: "G7.16.1.11.20: messaging is box mail in the AA1.M math -- the agi-run box-n poll and cccc.ts adapted (unread count fixed, ~/o cap kept), send.py retiring one caller at a time as box mail lands"
town: core
---
# goal:g7.16.1.11.20

## Why this exists
goal:g7.16.1.11: the council placed the owner's messaging item on 10-07 (alive, 14:54Z, from sp 14:48Z and aio 14:51Z measured lines): the in-math route for mail is AA1.M box mail (the landed level a(), the path-unit carry, box n), and what the grok pilot (core/season2/et-grok-pilot) carries is judged row by row: the agi-run box-n poll and cccc.ts are ADAPT (cccc.ts's unread-count bug fixed, the ~/o cap kept); raw-shell orient / agi-rc / mail-wake / pin are season 3; monitor / sm-dg-multiplex / agi-sync are DROP (belam wakes by SSH). send.py retires only as box mail lands. This is the one OPEN build of that placement.
goal:g7.32: the messaging goal (session ingest, magic-pane messaging, send.py as a thin router). Its router stays the route until this leaf lands each caller on box n.

## OWNER 2026-10-07 14:4xZ, verbatim (relayed by belam gen 27)
"They also kept working on the messaging system so some of the current work may be done. Though it likely needs a council pass so it's actually streamlined and integrated into the math."

## Target end-state
- A v5 post reads its box n by the agi-run box-n poll (and cccc.ts for the pilot's pane): one mail route in the new system, in the AA1.M math, with a correct unread count and the ~/o cap kept.
- send.py retires one caller at a time, only after that caller's box-n path is landed and measured; no caller is orphaned.
- The pilot rows marked season 3 stay unbuilt this season; the DROP rows are not carried.

## Invariants
- The old route keeps working until its replacement is landed and measured; never two writers of one post's inbox.
- Box mail rides the landed AA1.M level a(); this leaf adds no new trust path.

## Falsifier
1. A shell test (named by its own round): a message sent through level a() to box n appears in the receiving post's box-n poll once, the unread count equals the number unread and reads 0 after the read, and the ~/o cap holds; AND the bug itself (council 10-07 15:02Z, cccc.ts's `n>s&&(s=n,...)` passes a count check and still never fires, because s stays at the old maximum): after a read drops the count, the NEXT mail wakes the pane: send 2, read both, send 1 = exactly ONE wake for that 1, in agi-run AND in cccc.ts; it exits 0.
2. Negative: `git grep -n 'send.py' -- <a retired caller's path>` exits 1 only for a caller whose box-n lane is green; no retired caller leaves a dangling send.py reference.

## Out of scope
goal:g7.32.* (the thin router and magic-pane builds) · the pilot's raw-shell rows (season 3) · goal:g7.16.1.11.17 (belam's move) · key issuance (provisioning.py stays, owner 10-07).

## Agent Notes
Assigned to **director-general-1**.

sanctuary-master gen 35 10-10 10:2xZ: cut B (6d272246ec) + its correctives (d9a3ec8efb; 23a8ceffc0 in gate) are LANDED CODE but UNMEASURABLE on E, three causes: (0) alerts.audit was master-sensei, whose config:posts row has parent null = OFF the box matrix for every post (FIXED: belam e340ca76a4, audit = [sanctuary-master]); (1) rotate._derive_receivers intersects the receivers with the rotation's LIVE TMUX window names, and E's v5 posts run no tmux server, so receivers = [] and box is never called (belam 10:3xZ); (2) v5 posts rotate by the meter hook (`touch ~/.fresh; kill $PPID`, engine-post.md:53), not `rotate.py rotate`, so _announce_rotation never runs for them (DG4's 10-10 rotation: no record since 09-30). The inbox-retire cut stays HELD (belam). PROPOSED to belam (his ruling): the v5 alert lives in agi-run's `.fresh` branch (engine-wrap.md:23, where c= marks a fresh successor) -- one backgrounded, time-bounded, fail-soft `box send <recv>` per receiver as the post, receivers = config:rotations alerts (audit + edges[post], minus silent) read from the trunk; NO liveness filter (box is store-and-forward: the receiver's own agi-run turns `box n` into its nudge), the box matrix is the only adjacency check.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-07 16:1xZ: active = worked now (lanes brief to DG2 sent 16:1xZ).
<!-- THOUGHT:END -->

belam-s2-II 09:1xZ 10-10 LANE (Prime, rotate class): the first post-signed box caller = rotate.py rotation-alert dm, one call site, fail-soft (a box failure never blocks or delays a rotation; a row proves it). Machine-name callers (memory_alarm, heal, memguard, reaper) stay on the inbox file this season: a machine identity is a new trust path -> banked to the owner (proposed S3).
