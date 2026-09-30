---
id: goal:g7.32.6
mint_id: 6115b3a2a9784c66adac27ca7413a8f5
type: goal
parents:
  - goal:g7.32
next_edges: []
confidence: 0.7
edited_by: all-is-one
goal_id: G7.32.6
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 5fdc8c65def64593
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - engine
  - messaging
thought_session: belam-S2-L5-XI
title: "G7.32.6: ONE conversation per dm pair or room -- message, reply and read are versions on its own grid ref, pushed at once to each member's remote head; wake is an adapter verb; 3 routes -> 1 write + 1 wake"
town: core
---
# goal:g7.32.6

## OWNER 2026-09-27 06:1xZ (belam's pane), verbatim -- the rename
"But also the goal may need renaming because DMs aren't hub only anymore but get sent according to post branch address in send redesign."

## OWNER 2026-09-26 20:3xZ (Prime pane), verbatim
"Okay I was thinking of simplifying send to only use the hub route. Send automatically pushes a single dm push to the correct dm file on-chain, as a new dm file node version, always "overwriting" the existing dm file with a fresh version and setting the read row to false. Then every box with an active post has a cron that runs every 30 seconds to sync DM files only directly for the active posts on that box. Nudge only fires as part dm file sync, matter of fact the nudge script can be the local box sync script activated by the cron. No separate inbox system. Reading inbox is reading the dm file and setting the read row to true and pushing that back to remote. Other seats then get read status via graph on their next 30s cron.

So send calls write.py, and nudge calls both write.py and read.py. All DMs across all boxes local. Or not share the 30 second delay which is useful for sending corrections anyway. Can fine tune the delay via config to see how different values perform. I guess cron can just check all active seats across all boxes on every box for now to keep it simpler. It's a cheap call at our current roster size."

## OWNER 2026-09-28 06:5xZ (belam's pane), verbatim -- concurrent sends lose one
"Btw DE had parents message completion so your DM may have been swallowed. That may be the issue. Parents and you sending DMs around the same time causes one to get lost."
Measured by belam 06:3xZ from `.agi/sessions/inbox/director-engine.md` + `send.py status director-engine`: 06:22:42 / 06:22:50 / 06:23:20 three parent completion dms · 06:23:24 belam (read marker after it) · 06:27:44 belam [rule] dm: NO read marker after it and NO nudge (status marker=407s = last nudge ~06:24, pending=0) · 06:28:12 parent a00-1e3fe297. Earlier the same morning: two belam inbox sends (05:2xZ) both landed `pending=0` and `send.py wake` refused with nothing-pending while the block sat unread. The file keeps every block; what is lost is the NUDGE (pending counter / marker), so the reader never looks.

## OWNER lines carried from Agent Notes (verbatim, moved unedited: the body order keeps Agent Notes to the assignment)

OWNER 20:4xZ 09-26 (Prime pane), verbatim: "Also is the hub a separate branch or using the master branch or something? I was thinking between all DMs going straight into the correct town branch, or into season2/main and every nudge check is from that branch. But as you said in a db sense a lot of messages on one branch could pile up weirdly. So my thought was to expand each post node under .geometry with its assigned town which includes both the physical box and the repo branch they own and repo location so local worktree only or remote (which implies a local worktree of course). Send pushes message dm node to the correct branch for that post only, or the nearest, lowest-level remote branch available if there is no remote. Then the cron reads the active posts and sync only their messages from the appropriate branch via the post rows containing the config info. Each post also gets an local: true/false row to show that that post is active on that box or not. The town branching design of the repo handles the rest so no towns cross-contaminate each others local status. Small config extension and barely any code change. And less hardcoding now. Does it make sense? Also the 1 min delay is fine. We can even do 3 to see how it does. Keep it a cron." -- supersedes the 30 s of the title: the sync is a cron at 1-3 min (start at 3), a config cell. Prime refinement sent to DE: derive local at read time (row box == this box) rather than commit it.

OWNER 20:5xZ 09-26 (Prime pane), verbatim: "How does it check local box? Does it use the local worktree of the town GitHub branch box value? If so thats fine, but I wanna rework that to be able to let one town work across multiple boxes if needed. So really each post just has its own box value and the town has no box values, only a remote head to push to. Even more so, if each post has a designated remote head that is their “inbox” destination recorded, the nudge can pull from either that remote head and sync to local worktree or first sync just the dm to the local worktree of that remote head and then sync the post branch worktree with the local worktree then send nudge. (the send pushes to the appropriate remote head via post reference, the cron checks which box it’s on, which posts are local, and how the remote DM node version should be cascaded down through the worktrees via syncs. Also when send resd is used, it writes a new node version with the read flag set to true and pushes that node to the sender post remote, and uses write to do a DM node push to the sender’s DM file node appending, not rewriting the fact that message was read. The cron dm file check then also automatically returns read status by using a “reply” route in send.py. Or could even make it so the nudge automatically inserts the node file ‘add’ diffs or whatever to only show new insertions to save tokens on displaying the append, no separate read needed if key check comes back verified. Then the dm node files could naturally be appended via “reply” so a single conversation can stay grounded, but otherwise the “reply” would write a fresh one causing a bigger insertion diff than an append only. And again only append body text insertions as part of nudge and tag it clearly in the nudge as a post reply or post DM if not a reply. I think that covers the whole loop in an LLM friendly way that is config and template maxxed. We may need template updates for this. Does this simplification for elegance make sense?"

OWNER 21:0xZ 09-26 (Prime pane), verbatim: "Can we not have the local box name be a global env variable that gets set as part of the ini routine somehow? Like the box label in the network or something. Then just check that." -- replaces refinement (1): the box identity is AGI_BOX, set by the box init routine to a LOGICAL label (local-town, encryption-town), never the raw host name; unset -> refuse by name, never guess.

OWNER 21:1xZ 09-26 (Prime pane), verbatim: "Will this send and read redesign complicate things? It is overall reducing functions not increasing them so I think it will be fine. Also will the quiet flag still work with this system? Each post has a quiet row true or false and the cron does not fire nudge unless a [red] item comes through. Also if nudge deposits whole message body due to valid key, it should mark the message as read as well. Assuming it fully posted into the tmux pane and was not blocked. Not read until pane not busy and message is in pane." (apostrophes dropped for the write.py quoting)

belam-S2-L5-XI 00:4xZ 09-27, on the OWNER's go (an owner-pasted line from belam-S2-L5-X): ADD the "(default) box is always foreign" refusal to this redesign. MEASURED on local-town: a row with no box cell takes the posts node's default_box = core-town for locality (boxes.row_is_local, boxes.py:168-182), while this_box = local-town (AGI_BOX from the MAIN .env, which every worktree root resolves), so the six no-box rows (director-belam, director-sanctuary, sanctuary-master, sanctuary-helper, master-sensei, stream-master) are FOREIGN here and every sweep refuses them again (send.py:2198-2204; 72 lines in agi-crons-agi-3fbc6951.log), labelled "(box (default))" rather than the box they resolved to. DONE WHEN: (1) every live row carries its OWN box cell, written at seating from AGI_BOX -- default_box never decides locality; (2) a row whose box is empty or matches no live box is refused as a nudge target on EVERY box (the (default) box is always foreign), ONCE per row and cause, naming the resolved box -- not once per sweep; (3) no send-keys ever lands in a window addressed by such a row. Not the cause of the director-thought report: its row (post-director-thought-a8 / 88bad1aa / @8 / pid 1530011 / box local-town) matches its live session, and wake reads idle nothing-pending @8.

belam-S2-L5-XI 01:0xZ 09-27, OWNER verbatim: "Would the mint write design be first? Um send pieces depend on it, and rotate depends on send" -- ORDER of the three graph redesigns: (1) goal:g4.18.1, the mint/write route; (2) this goal + goal:g7.32.5 (send = write.py, so it builds on (1)); (3) goal:g7.31.3.3 spawn/rotate (its refusals ride this goal's reply route). The owner's 21:1xZ HOLD items wait on (2).

OWNER 06:0xZ 09-27 to belam, verbatim: "It's because pids rotate but tmux panes stay the same. We shifted to PIDs for messaging at some point and it broke things. I think the redesign is also doing it but if PIDs get updated auto as part of rotate it also fixes it" -- belam measured 06:0xZ: the four seats rotating on local-town (belam, thought-master, director-thought, director-engine) carry a LIVE pid in their row; rotate's successor row write stamps it (rotate.py:6695). Stale pids sit on rows of seats not seated on this box.

## Why this exists
goal:g7.32 (session ingest + magic-pane messaging + adapter pane methods + send.py thin router): messaging is its core part, and it is measured broken in four ways the owner named. (1) Three routes, not one: verdict:dg2-s1-dm-family (inbox file · comms dm/room file · CC SendMessage; a pi post cannot use the third). (2) A nudge is lost when two sends cross (OWNER 06:5xZ 09-28 above). (3) The default-box rule refuses six live rows on every sweep (belam 00:4xZ 09-27 above). (4) pid-keyed messaging broke when pids rotated (OWNER 06:0xZ 09-27). Order (OWNER 01:0xZ 09-27, "Would the mint write design be first?"): this stands on the write form (goal:g4.18.5 -> goal:g7.16.1.6) and runs right after goal:g7.16.1.6 (council placement, Prime ruling (a) 00:0xZ 09-30).

## Target end-state
Four parts, each a leaf when the directors split the build (A first; B-D stand on it):
```
A ONE CONVERSATION  a dm pair and a room are ONE node type (members: 2 = dm, N = room); a message, a reply and a read are each a VERSION of it
                   (one write.py write, goal:g7.16.1.6 A); a reply appends to the same conversation, so it stays grounded
B DELIVERY         the conversation type sets push_on_write (goal:g7.16.1.6 A): a message pushes its ONE ref at once to each member post's remote head
                   (the post row's "inbox" destination; none -> the nearest, lowest-level remote branch); the receiving box pulls it on the fetch + wake
                   line goal:g7.16.1.6 keeps, at a config-cell interval (1-3 min, start at 3) -- no messaging-only cron
C WAKE             an ADAPTER verb (CC -> SendMessage · pi -> its own; goal:g7.16.1.7's adapter map), addressed to the post ROW and resolved to its
                   pane at wake time, never a stored pid; it shows only the new version's inserted body text, tagged `post dm` or `post reply`;
                   a quiet post wakes only on [red]; the graph reports THREE states per message: written (its version) · delivered (in a non-busy pane) · read;
                   a full-body deposit with a valid key in a non-busy pane records delivered AND read (OWNER 21:1xZ); a tag-only wake records delivered only
D ONE READ STATE   unread = the conversation's versions after the member's last-read version; a read is a version that changes ONLY the member's read cell
                   (the commit read up to: a few bytes, a delta in git's packs, never a copy; OWNER 20:5xZ asks for the read version), pushed
                   like a message, so the sender's box sees it on its next fetch -- no state.json, no pending counter, no inbox (.agi/sessions/inbox/* retires)
   3 routes -> 1 write + 1 wake
```
- Box identity: each live post row carries its OWN `box` cell, written at seating from AGI_BOX (a logical label set by the box init routine, never the raw host name). Locality = row box == AGI_BOX, derived at read time, never committed. A town holds no box value, so one town may span boxes.
- A retired member's conversations retire with it (deprecated + moved; refs never deleted): kid conversations (123 of 152 season-2 dm files) leave the live count with their kid.

## Invariants
- Nothing sent is lost: two concurrent sends to one conversation both land as versions (update-ref compare-and-swap; the loser re-parents onto the new tip) and both wake.
- One writer: send, reply and read are write.py writes; no verb exists only for messages; reading a conversation is the render path (goal:g4.18.7).
- AGI_BOX unset -> refuse by name, never guess. A row whose box is empty or matches no live box is never woken on ANY box (the "(default) box is always foreign" rule), named ONCE per row and cause.
- A read version NEVER wakes anyone, and a wake writes nothing but the addressee's read: the loop read -> version -> push -> wake -> read is broken by construction (an N-member room would multiply a wake storm by N).
- Where the Prime's reading or the council's shape differs from an OWNER line, the OWNER line wins.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_conversation.py -q` exits 0 and pins: one type for dm and room · two concurrent sends -> two versions + two wakes · a read is a version the sender's box sees · a quiet post wakes only on [red] · a wake resolves the pane from the row at wake time · the wake text = the inserted lines only, tagged · a read produces 0 wakes on every box.
2. Cross-box, measured: a dm from a local-town post to a core-town post wakes its addressee within one fetch/wake interval (the config cell) of the send, and the sender's box shows it read within one more.
3. Negative: `git grep -nE 'sessions/inbox' HEAD -- extensions/agi/bin` = 0 hits · `python3 extensions/agi/bin/crons.py show` lists no messaging-only job · 0 send-keys into a window addressed by a row without a live box cell.

## Out of scope
goal:g7.16.1.6 (the write + push form this stands on) · goal:g4.18.5 · goal:g4.18.6 · goal:g4.18.7 (the render path a read uses) · goal:g7.16.1.7 (the post row's pane cell and the adapter map) · goal:g7.32.5 (the parent hub-route grant: absorbed or retired by name when this lands) · the magic pane system · season-3 key templates and per-post accounts.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all-is-one (council) 01:1xZ 09-30, on belam's [owner-task], OWNER 00:5xZ 09-30 verbatim: "I'd like the council to go over my verbatim text and make updates to each goal's structure and wording as needed to make sure that the new owner words are reflected in the goal format" and "apply their lenses and zoomed out thinking at my words". What the lens (vision:all-is-one: one tool for any act, the same for every role) changed in THIS version: (1) body order: the 7 owner lines that sat in Agent Notes moved byte-identical into an OWNER section (verified by a script: all 20 owner lines present); the Prime's design lines, the RE-SHAPE and Done-when folded into ONE Target, because two design statements in one node disagreed on delivery (the grid keeps every earlier version). (2) a dm and a room are ONE conversation type; message, reply and read are versions: one writer, no messaging-only verb. (3) delivery CORRECTED: the council's own re-shape said the ~15-min moved-set push delivers, which misses the owner's 1-3 min (20:4xZ) by 5-15x; now push_on_write single-ref push + the fetch/wake line goal:g7.16.1.6 keeps (settled with alive, who writes .6). (4) wake addresses the post row, resolved at wake time (OWNER 06:0xZ 09-27: pids rotate, panes stay). (5) three states per message (alive's lens) with OWNER 21:1xZ's deposit-is-read rule kept; a read is a version touching only the read cell (OWNER 20:5xZ), not per-member pointer refs (refs would grow as members x conversations). (6) a read never wakes (self-perpetuating's loop breaker). A-D are the leaves when the directors split the build.
<!-- THOUGHT:END -->

## Agent Notes
Assigned to **the directors, by their own split (room `directors`)**.
