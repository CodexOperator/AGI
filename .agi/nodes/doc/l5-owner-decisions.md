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

### OWNER 2026-09-17, banked 14:2xZ (date -u) — the director's unverified read + auto-posting verified dms, verbatim

> "Yeah btw the director considered your message unverified since it came from an automated channel. I got it started now but how hard would it be to make message auto post into the chat itself if verified."

MEASURED (Prime): the director's worktree was 200 commits behind season2/main and its config:posts row carried the Prime's previous pubkey (0dd30447 vs 10009646 at HEAD); send.py read verifies against the READER's checkout while whois verifies against origin/season2/main. Routed to the director as a g15 line (second parent beside L5.01): verify against the authority branch + the recipient's UserPromptSubmit hook runs the one read on an [agi-nudge] prompt and appends the verified bodies as hook context (no tool call; verification recipient-side against the graph, never the typed text).

### OWNER 2026-09-17, banked 14:2xZ (date -u) — hourly watchdog nudges, verbatim

> "can we increase the watchdog nudge interval to every hour as the director is getting nudged constantly and parents and kids are still active of course."

APPLIED by the Prime as a direct write on this order (hypothesis:l5-the-stranded-wake-repair-runs-hourly-on-its-own-cadence, goal:g15): heal.py's stranded-wake repair now runs on `comms.wake_repair_every_s` (default 3600, set explicitly in .agi/config.json) instead of every 30 s poll; the reaper, after_join and round watch keep the 30 s poll; `comms.nudge_stale_after_minutes` 30 -> 60. Deviation recorded on the node: 11 production lines by the Prime, not a round -- the owner asked for it now and the one director was loaded.

### OWNER 2026-09-17, banked 20:03Z (date -u) — parent cap 8, verbatim

> "Feel free to lift concurrent parent cap to 8, parents get each their own worktree right?"

APPLIED by the Prime: the L5 cap on live parents is 8 (was 4, the L4 04:0xZ 09-17 load ruling) in doc:l5-plan, the director duties brief, the successor brief and the card. Yes: every parent round lands on its own branch season2/loops/<hypothesis-prefix>-<agent> in its own worktree .agi/worktrees/<agent>/ (kids branch under it); the tree-wide bound stays spawn.max_live 25 agents (parents + kids together) and parent_max_kids 10 -- with 8 parents live that leaves 17 kid slots fleet-wide; the 4-core box measured 1800 s review timeouts at load 10+, so reviews stay one mur per kid slice.

### OWNER 2026-09-17, banked 20:18Z (date -u) — parent overdue reminder 20 -> 75 min, verbatim

> "can we up the automated parent overdue reminder up from 20 minutes to 45 for the directors? Our parents have been pretty robust and the failures informative, so the context savings would be worth it imo. Or maybe even 70-80 minutes then every 30 after?"

APPLIED by the Prime (config only): `.agi/config.json` `agent_timeout_mins` 20 -> 75 -- it is the ONE knob: dispatch writes it into the round manifest as timeout_seconds, the heal watch sends the director exactly ONE overdue dm when a still-running parent passes it (a live pid is never replaced; a DEAD pid is detected by liveness, not by this timeout, so crash recovery is unchanged). "Then every 30 after" needs code (the dm is once-only by design, hypothesis:l4-a-round-alarms-its-dispatcher-by-default) -> a g15 line for the director: the overdue alarm re-fires every comms.overdue_repeat_min (30) after the first, each dm naming elapsed minutes, still no replacement cut for a live pid.

## Agent Notes
OWNER 2026-09-17 22:5xZ, in the Prime pane (belam gen 29), verbatim: "Does queued mean dispatched? Director just thinks dispatch keyword is a requirement. May need doc changing either for Belam or for your director docs or both" -- APPLIED f34ba093a: queue vocabulary written into both briefs (prime-director-successor.md via write.py, director-belam-duties.md): minted / queued (the director drains its own HEAD 3 queue by the Prime stated priority within the parent cap; never a hold; no further Prime word) / [decision] hold <node> (the only hold) / dispatch now <node> (the only dispatch order) / dispatched; relayed to director-belam as a [rule] line.

OWNER 2026-09-17 23:1xZ, in the Prime pane (belam gen 29), verbatim: "Can we batch some of these because otherwise I do not need to do it now. I have a redesign coming up" -- APPLIED: (1) merge-ups are BATCHED -- the director sends one [merge-up] dm per 4+ ready rounds (or the whole wave); the Prime lands the batch in one pass (one merge per SHA in order, one verify, one push, one GO dm, one g19 note, one card update) and reports to the owner ONCE per batch, never per landing; [red], rotations and rule-changing findings still go alone; (2) L5 stays small and closes after the live wave L5.14-21 lands: queue items that do not block the g19 done-state are retired-with-note or carried into the redesign, not rounded; (3) the owner is not needed for any of this under delegated authority -- the next owner-facing report is the batch landing, then the close.

OWNER 2026-09-18 00:0xZ, in the Prime pane (belam gen 29), verbatim: "Can the thought master and sanctuary master get back to work at this point or no? I have some things I would like to assign to both." -- RULED YES by the Prime under delegated authority (the 13:3xZ formation line "nothing else woken" was the owner own scope rail; the owner lifts it for these two): rows un-quieted 83870465a, both briefed [owner] and woken (busy-deferred: delivered when each pane idles). RAIL until the Prime posts L5 CLOSED: worktree-only -- no MAIN commits, no engine-suite runs, no merge-ups into season2/main, no rotation; dispatch from the worktree as usual. After the close: merge-ups by name, suite windows granted one at a time. Thought-master lane stays the independent pursuit (owner 09-16 17:5xZ); the GPU-box relocation stays banked for the redesign. master-sensei, sanctuary-helper, director-thought, stream-master, director-sanctuary stay idle + quiet.

OWNER 2026-09-18 00:1xZ, in the Prime pane (belam gen 29), verbatim: "And sanctuary master knows she has control over posts, setting up posts, taking them down, rearranging formations via graph." then "Also each town has its own branch now all neat and organized, wouldnt each master own that town branch at this time until council activation later?" -- RULED by the Prime: (1) formation authority = sanctuary-master (config:posts rows: create, retire, rearrange, town + quiet cells); the write gate today is [config].md written_by [owner, prime_director] + self_row, so her row edits are applied by the Prime hand from a [decision] line until she lands the formation-owner carve-out (schema + write.py + test) after L5 CLOSED; (2) town branch ownership until council activation: sanctuary/* + core/* sanctuary-master; local-maxxing/* thought-master; streaming-suite/* stream-master (idle, Prime holds); web-app-suite/* Prime holds (no master); season2/main, season1/main, master = the Prime; merge-ups into season2/main stay GO-by-SHA; the map is recorded on the town nodes (master + branches cells) by sanctuary-master as her first formation act. Relayed to sanctuary-master + thought-master 00:1xZ.
