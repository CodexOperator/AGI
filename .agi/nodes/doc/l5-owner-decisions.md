---
id: doc:l5-owner-decisions
mint_id: 205d2bbac2e64008be78913b739c2d90
type: doc
parents:
  - goal:g19
next_edges: []
edited_by: belam
scaffold_hash: 37589d8aa215c1ea
season: 2
tags:
  - doc
  - l5
  - owner-decisions
title: L5 owner decisions — verbatim, banked by the Prime
town: core
---
<!-- BODY:BEGIN -->
# L5 — owner decisions, verbatim (banked by the Prime; the ONE place L5 owner text lives)

Owner quotes are protected HERE, never in HANDOFF.md or a card. Rulings land beside each quote. Stamps from `date -u`.

### OWNER 2026-09-17, banked 13:33Z (date -u; received after the 12:09Z inbox read) — L5 named (Prime pane, remote-control, to belam gen 28), verbatim

> "Nice. Happy to see it. I can see everything got closed out. One question I had was that I remember a couple days ago, several belong generations ago, I asked if the GitHub branch collapse and the session renames were queued to be done. And he said that yes they were. But checking now, the session names are still using our old sessions that we came up with on the spot. Rather than the official session names we came up with later. And I believe the GitHub branches still have not been collapsed. When did that slip through the crack? And it's fine that it did. I'm just curious because several generations ago, it was on the list that we need to get those things done. But then now that it's closed out, those things still haven't been done. I would like to go ahead and set up an L5, a small one. To just take care of any leftover straggling bug fixes and first and foremost the first thing it needs to do is take care of collapsing all these branches and take care of renaming the sessions properly so they're all named and easy to address let me know if you have any questions and we can go ahead and set this loop up and get it going we're not going to activate a lot of hosts we're strictly just going to have you running a single director running several parents at a time"

PRIME MEASUREMENT (belam gen 28, 12:1xZ-13:3xZ), where it slipped:
- Branch collapse: ruled 09-11 02:0xZ; Option B GO 09-12 18:4xZ; first pass APPLIED 09-13 ~00:4xZ (Belam XX: core/main, core/season2/main, core/season2/posts/*/main created; --delete-old for TOWN kinds only; posts + loops "wait for the mirrors", SM.25b). The mirror prerequisite chain moved to the last hours of L4 (SM.25b -> SM.36 09-16 12:1xZ -> SM.53 -> SM.90 09-17 08:2xZ -> SM.92 09-17 08:5xZ); no round was ever named "second pass". THE CRACK: 09-16 14:1xZ ("let's leave it at your plan") deferred SM plans (4)+(5) out of the close, and the branch prefixes had been folded under (5) town numbering by the 18:0xZ town ruling; every closeout lineup after it (01:0xZ, 03:0xZ, 04:0xZ 09-17) and COMPLETE.md's heads omit it. Measured at open: origin refs/heads = 21 (9 intended; 12 to go: 3 season2/posts/* pre-v3 twins, 3 core/season2/posts/*/main live posts -> hidden refs/agi/posts/*, 3 season2/loops/*, season2/sensei/genless-templates, collaborator-branch, copilot/add-open-source-license); local = 678 branches (646 merged into season2/main, never pruned), 109 dead kid worktrees under .agi/worktrees/a00-*.
- Session renames: ordered 09-16 17:4xZ; STAGED 20:24Z by belam gen 25 (rotate.py rename-post: sanctuary-director -> director-belam 54 surfaces, sensei-director -> director-sanctuary 67 surfaces, "applied at each post's rotation boundary"). Both posts rotated after (point 07:29Z, sensei-director 07:33Z 09-17) and nothing applied: rotate.py DEFINES _apply_staged (line 3898) and NO code path calls it -- a docstring promise. The two .rename.json files still sit in .agi/sessions/seats/. A bug, not a decision; nobody verified the first boundary after the staging.

### OWNER 2026-09-17, banked 13:33Z (date -u) — L5 GO with defaults (Prime pane, remote-control, to belam gen 28), verbatim

> "No, because that is how we get scope creep inside of a simple, tidy pass loop. go with default at this time. One thing is your director should be named director-belam, not anything else when you do get around to renaming the session. we are not live streaming this so don't worry about having that running. Also, follow all the same standard rules regarding trying to like fix anything else that comes up, little gaps and things in the loop, and keep iterating until everything is truly well and truly done. Again, first thing should be branch deletes, and the next thing should be post session name updates, and then everything else. You are good to go."

RULED (as read by the Prime, belam gen 28, 13:3xZ):
1. ORDER, fixed: (1) branch deletes -> (2) post session-name updates -> (3) everything else (the straggler bugfixes + every little gap surfaced in-loop, fixed in-loop as g15 hypothesis nodes per the standing 09-11 05:1xZ rule). Iterate until truly done; L5 closes only when goal:g19's done-state holds.
2. NOT in L5: the thought-town relocation (scope creep inside a tidy pass); it stays banked from the L4 close.
3. The single director is named director-belam -- nothing else -- once the rename lands; until then its code name stays sanctuary-director.
4. No livestream: view-<post> sessions and the livestream repoint are not required; a missing view session is never a red.
5. Defaults ACCEPTED: all 5 town nodes on remote (target 13 refs/heads); both foreign branches deleted (collaborator-branch, copilot/add-open-source-license -- deleting the latter closes the Copilot PR); director = today's sanctuary-director post; formation = Prime + ONE director + up to 4 live parents (<=5 kids each), every other post idle.

### OWNER 2026-09-17, banked 13:45Z (date -u) — quiet every idle post, verbatim

> "Can we archive all other posts fully? They keep getting nudge spammed. Or add them to quiet posts is fine so they get nothing at least"

APPLIED by the Prime 13:45Z (f54c02af0), the reversible option: `config:posts` `settings=quiet` on every row except belam and the L5 director sanctuary-director (17 rows; `send.py` `_row_is_quiet` = the ONE nudge choke point, so send/wake/heal/stranded-retry all type nothing; the dm is still written to the inbox). Not archived: the idle windows stay (an idle session costs nothing) and sensei-director must stay alive to rotate once in L5.02 for its rename. Rewind = the same cell back to "".
