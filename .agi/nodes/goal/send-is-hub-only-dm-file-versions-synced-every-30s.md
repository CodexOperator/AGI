---
id: goal:send-is-hub-only-dm-file-versions-synced-every-30s
mint_id: 6115b3a2a9784c66adac27ca7413a8f5
type: goal
parents:
  - goal:g7.32
next_edges: []
edited_by: belam
scaffold_hash: 5fdc8c65def64593
season: 2
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
thought_session: belam-S2-L5-X
title: "send is hub-only: every dm is a new dm-file version pushed once, synced by one 30 s box cron that also nudges; no inbox (assigned: director-engine)"
town: core
---
# goal:send-is-hub-only-dm-file-versions-synced-every-30s

# goal:send-is-hub-only-dm-file-versions-synced-every-30s

## OWNER 2026-09-26 20:3xZ (Prime pane), verbatim
"Okay I was thinking of simplifying send to only use the hub route. Send automatically pushes a single dm push to the correct dm file on-chain, as a new dm file node version, always "overwriting" the existing dm file with a fresh version and setting the read row to false. Then every box with an active post has a cron that runs every 30 seconds to sync DM files only directly for the active posts on that box. Nudge only fires as part dm file sync, matter of fact the nudge script can be the local box sync script activated by the cron. No separate inbox system. Reading inbox is reading the dm file and setting the read row to true and pushing that back to remote. Other seats then get read status via graph on their next 30s cron.

So send calls write.py, and nudge calls both write.py and read.py. All DMs across all boxes local. Or not share the 30 second delay which is useful for sending corrections anyway. Can fine tune the delay via config to see how different values perform. I guess cron can just check all active seats across all boxes on every box for now to keep it simpler. It's a cheap call at our current roster size."

## The design, one line per part (the Prime's reading; the owner's words above win)
1. send = write.py: ONE commit + push per dm -- a new version of the pairwise dm file node (a fresh whole-file version, never an append), its read row = false.
2. ONE path for every dm, same-box included: the hub. The sync delay is shared by all (useful for sending corrections) and is a config cell, tuned by measurement.
3. ONE cron per box, every 30 s (the cell): sync the dm files only; for now it checks every active post on every box (cheap at this roster).
4. nudge = that box sync script: it fires only from the sync, on an unread dm for a post seated on this box; it calls write.py + read.py.
5. read = read the dm file, set its read row = true, push; other posts learn read status from the graph on their next sync.
6. no separate inbox system: .agi/sessions/inbox/* retires once 1-5 hold.

## Done when
A dm between two posts on different boxes and one between two posts on the same box both arrive by the same hub path within one sync interval of the push; the read row flips and is visible to the sender's box on its next sync; no inbox file is written; the interval is a config cell.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by the Prime belam-S2-L5-X from the owner's own words; assigned to director-engine. Measured context the same evening: `send.py send <post>` writes an inbox file and pokes a local pane; `send.py send --to <post>` writes the pairwise dm file; a foreign-box post is refused a nudge by name (send.py:2201) and gets its dms only through mail_poll's 5-minute hub fetch + `read --box-local` (crons.py:931-945). Two delivery systems and two latencies is the thing this goal removes.
<!-- THOUGHT:END -->
