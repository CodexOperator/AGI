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
thought_session: belam-S2-L5-XI
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

## Agent Notes
OWNER 20:4xZ 09-26 (Prime pane), verbatim: "Also is the hub a separate branch or using the master branch or something? I was thinking between all DMs going straight into the correct town branch, or into season2/main and every nudge check is from that branch. But as you said in a db sense a lot of messages on one branch could pile up weirdly. So my thought was to expand each post node under .geometry with its assigned town which includes both the physical box and the repo branch they own and repo location so local worktree only or remote (which implies a local worktree of course). Send pushes message dm node to the correct branch for that post only, or the nearest, lowest-level remote branch available if there is no remote. Then the cron reads the active posts and sync only their messages from the appropriate branch via the post rows containing the config info. Each post also gets an local: true/false row to show that that post is active on that box or not. The town branching design of the repo handles the rest so no towns cross-contaminate each others local status. Small config extension and barely any code change. And less hardcoding now. Does it make sense? Also the 1 min delay is fine. We can even do 3 to see how it does. Keep it a cron." -- supersedes the 30 s of the title: the sync is a cron at 1-3 min (start at 3), a config cell. Prime refinement sent to DE: derive local at read time (row box == this box) rather than commit it.

OWNER 20:5xZ 09-26 (Prime pane), verbatim: "How does it check local box? Does it use the local worktree of the town GitHub branch box value? If so thats fine, but I wanna rework that to be able to let one town work across multiple boxes if needed. So really each post just has its own box value and the town has no box values, only a remote head to push to. Even more so, if each post has a designated remote head that is their “inbox” destination recorded, the nudge can pull from either that remote head and sync to local worktree or first sync just the dm to the local worktree of that remote head and then sync the post branch worktree with the local worktree then send nudge. (the send pushes to the appropriate remote head via post reference, the cron checks which box it’s on, which posts are local, and how the remote DM node version should be cascaded down through the worktrees via syncs. Also when send resd is used, it writes a new node version with the read flag set to true and pushes that node to the sender post remote, and uses write to do a DM node push to the sender’s DM file node appending, not rewriting the fact that message was read. The cron dm file check then also automatically returns read status by using a “reply” route in send.py. Or could even make it so the nudge automatically inserts the node file ‘add’ diffs or whatever to only show new insertions to save tokens on displaying the append, no separate read needed if key check comes back verified. Then the dm node files could naturally be appended via “reply” so a single conversation can stay grounded, but otherwise the “reply” would write a fresh one causing a bigger insertion diff than an append only. And again only append body text insertions as part of nudge and tag it clearly in the nudge as a post reply or post DM if not a reply. I think that covers the whole loop in an LLM friendly way that is config and template maxxed. We may need template updates for this. Does this simplification for elegance make sense?"

OWNER 21:0xZ 09-26 (Prime pane), verbatim: "Can we not have the local box name be a global env variable that gets set as part of the ini routine somehow? Like the box label in the network or something. Then just check that." -- replaces refinement (1): the box identity is AGI_BOX, set by the box init routine to a LOGICAL label (local-town, encryption-town), never the raw host name; unset -> refuse by name, never guess.

OWNER 21:1xZ 09-26 (Prime pane), verbatim: "Will this send and read redesign complicate things? It is overall reducing functions not increasing them so I think it will be fine. Also will the quiet flag still work with this system? Each post has a quiet row true or false and the cron does not fire nudge unless a [red] item comes through. Also if nudge deposits whole message body due to valid key, it should mark the message as read as well. Assuming it fully posted into the tmux pane and was not blocked. Not read until pane not busy and message is in pane." (apostrophes dropped for the write.py quoting)

belam-S2-L5-XI 00:4xZ 09-27, on the OWNER's go (an owner-pasted line from belam-S2-L5-X): ADD the "(default) box is always foreign" refusal to this redesign. MEASURED on local-town: a row with no box cell takes the posts node's default_box = core-town for locality (boxes.row_is_local, boxes.py:168-182), while this_box = local-town (AGI_BOX from the MAIN .env, which every worktree root resolves), so the six no-box rows (director-belam, director-sanctuary, sanctuary-master, sanctuary-helper, master-sensei, stream-master) are FOREIGN here and every sweep refuses them again (send.py:2198-2204; 72 lines in agi-crons-agi-3fbc6951.log), labelled "(box (default))" rather than the box they resolved to. DONE WHEN: (1) every live row carries its OWN box cell, written at seating from AGI_BOX -- default_box never decides locality; (2) a row whose box is empty or matches no live box is refused as a nudge target on EVERY box (the (default) box is always foreign), ONCE per row and cause, naming the resolved box -- not once per sweep; (3) no send-keys ever lands in a window addressed by such a row. Not the cause of the director-thought report: its row (post-director-thought-a8 / 88bad1aa / @8 / pid 1530011 / box local-town) matches its live session, and wake reads idle nothing-pending @8.
