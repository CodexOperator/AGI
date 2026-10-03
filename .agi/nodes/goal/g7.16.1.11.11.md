---
id: goal:g7.16.1.11.11
mint_id: a208e4ea2728400c937517eea4a36415
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.11
goal_kind: subgoal
origin: goal
scaffold_hash: af53d9b7737fcab7
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - design
  - g7.16.1.11
  - aa1
  - boxes
  - mail
title: "G7.16.1.11.11: AA1 boxes -- a v5 post hands bytes to an adjacent post through git refs only; the parent-cell matrix decides where mail may go; one ~1.8 KB script replaces send.py for it"
town: core
---
# goal:g7.16.1.11.11

## Why this exists
goal:g7.16.1.11 (the council design doc for a radically simple engine): the council's AA1 section (doc:rse-aa1-boxes on posts/alive, measured 23:3xZ-23:4xZ as a v5 uid) found that a v5 post can neither SEND (every .agi/sessions/inbox/*.md is belam:belam 664, the dir 775 with no group entry) nor CONSUME (send.py read prints, then PermissionError writing the read marker, so the same order re-prints at every read); the inbox dir is 2,368 files / 8.6 MB; the trunk's signers piece holds 3 of the posts' keys, and v5 commits sign as <post> while the unit sets %i@agi (verify-commit: No principal matched). belam's [decision] 23:52Z placed the bundle on DG1 to write goals + hypotheses from it; builds come only after these leaves.

## OWNER 2026-10-01 23:0xZ + 23:2xZ, verbatim (via the council bundle)
"We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something."
"This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
"Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."
Skills line (owner 23:4xZ via belam 23:49Z): "update the other skills to reflect the way the new system works"


## Target end-state
- Mail is a signed, tree-less commit chain on refs/box/<from>/<to>: OUT is only <from>'s to extend; IN = the union of refs/box/*/P (no file, no lock); HELD = refs/held/P/<from>, moved only by P's own read, never carried; UNREAD = IN --not HELD. Mail is addressed to the POST, so it survives a session rotation. The will box is the card (exists).
- Delivery state is DERIVED from refs, never written down a second time.
- Where mail may go is a PROJECTION of the config:posts parent cells read at AGI_TRUNK: a and b are adjacent iff one is the other's parent, or an inert row (a row with no harness; today `council`) sits between them and is eliminated (vertex elimination: its parent and its children become one clique). Off-matrix: refused at send AND at read.
- `box` (send TO <msg | read | n | carry HUB POST..) is <= 1,800 B EXPANSION, 0 B in the zygote, and replaces send.py (317,096 B) for every engine.v4 post; agi-run's wake becomes `box n | wc -l` grew (a successor wakes on its predecessor's unread). No .agi/sessions/inbox write by a v4 post.
- ONE principal form, `<post>@agi` (what the unit already sets); signers come from AA2's root-owned ring.
- VERSIONING (AA1.V, belam [decision] 00:25Z, owner 00:3x-00:4xZ: every turn is a grid commit from a tiny tree): agi-turn makes ONE signed one-node commit per changed node from the node's tiny tree onto posts/<p> (the box send primitive over a one-node tree; +578 B expansion: agi-turn 1,074 B, agi-wt 819 B, agi-link retires); ~/t is a detached READ view (a stray edit is reported `[out-of-tree]`, never committed); a node moved on the tip since pull is archived under refs/archive/<p>/<mint>, never overwritten; the handoff down or up the figure eight is mail (`box send <next> 'handoff posts/P@<sha>'`). Falsifiers AA1.V1-V4 are the seeds of the two aa1v hypotheses.

## Invariants
- Forward-only: a post can create and move a ref, never delete one (packed-refs.lock is root-owned); a squat is a denial until its owner moves the ref back, never a forgery.
- A refused commit stays UNREAD and loud at every read (true state over throughput).
- No flag day: old-setup posts (belam, SM, DG3, old TM) keep send.py until each moves; a moved post reads both until the last old post is gone.
- The 25 scratch cases B1-B8 of doc:rse-aa1-boxes are the regression set.
- SIZE BAR (the bundle's statement of the owner's line): the base install stays under 8 KB (config:engine <= 8,192 B), unfolded from a 1 KB seed (1,023 B); boxes, the lap and the land check are EXPANSION read by `sect`, 0 B in the zygote; nothing model-manual that could be automated; reuse an existing piece before adding one.

## Falsifier
1. On the real shared .git, as the agi-alive uid: a send from a post adjacent to alive, then `AGI_POST=alive box n | wc -l` = 1, `box read` prints the body, and the next `box n | wc -l` = 0 (AA1.1).
2. Negative: `git grep -n 'sessions/inbox' -- <the box script + the v4 agi-run wake line>` returns zero hits, and `wc -c` of the box script <= 1800 for AA1.1 (AA1.M's bounded send retry makes it 1,927 B and the level a() line (belam 19:5xZ: a and b mail iff their levels differ by at most 1, inert rows count 0) 2,005 B, which landed with the level round: the cap is 2,005 for goal:g7.16.1.11.11.1).

## Out of scope
goal:g7.16.1.11.12 (the key ring, the lap, the 8 KB budget) · goal:g7.16.1.11.13 (land) · goal:g7.16.1.11.14 (skill deltas) · a SECOND box for the hub carry (AA1.3 waits for hardware) · retiring send.py for the old setup.

## Agent Notes
Assigned to **director-general-1**.
