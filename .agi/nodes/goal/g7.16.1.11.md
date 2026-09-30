---
id: goal:g7.16.1.11
mint_id: 227e7f1ac32d4b49bf45356fd8ffbbee
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11
goal_kind: subgoal
origin: owner
scaffold_hash: 0250fcfcc84f8baf
season: 2
status: active
tags:
  - council-loop
  - redesign
  - per-post-users
  - radically-simple
title: "G7.16.1.11: a council design doc for a radically simple engine -- per-post Unix users hold identity, keys and write permission; no standing worktrees; write = a git commit; render off the git graph"
town: core
---
# goal:g7.16.1.11

## Why this exists
goal:g7.16.1 (the council loop) is the formation the owner handed this design to ("make the council work on it"). What it measured: tonight's fixes to enable key control, and the size of the machinery that rebuilds user boundaries in Python because every post runs as ONE Unix user. Measured 21:3xZ 09-30: rotate.py 23,229 lines · send.py 6,384 · write.py 4,572 · heal.py 4,291 · node_writer.py 1,773 · provisioning.py 1,598 · spawn_budget.py 1,169. About 150 active goals carry key / identity / rotate / spawn / guard / whois / sign work. doc:s3-plan HEAD 1.6 had already queued "one Unix user per post + role groups" for season 3; the owner pulls it forward now.

## Target end-state
- ONE council-authored design doc node (a doc:*, parent this goal) for a RADICALLY SIMPLE engine. For every piece it asks the owner's question: "what is it I am ACTUALLY trying to get the machine to do here?"
- The doc covers, each as a decided section:
  - per-post Unix users: user + keys + signing key held by the account, named in the post's .geometry row; role/town groups; per-file permissions on node files; post configs linked into the user's own settings as symlinks
  - write = a shell script over a git commit (or a system read/write pair that adds up to one); render = one real render script, or the git graph / an off-the-shelf package as the graph view
  - NO standing worktrees: per-node trees checked out on the fly and recycled when done (a fresh one too); tests mix and match code across per-node trees, if that holds up
  - an MCP wrapper over the engine as it works now
  - core's magic pane (the grok team, half working) read as input
- A table of every current machine piece: KEEP · REPLACE-BY (kernel permission, git, off-shelf package) · SCRAP, with the lines each retires.
- The doc's acceptance test is the spike list: (a) two users commit signed into one shared repo, (b) the kernel refuses a cross-post node write, (c) Claude Code + pi run as each user, and cross-user messaging works or is replaced by graph files, (d) each user gets its own memory slice. The spike runs only after the owner reads the doc.

## Invariants
- No Unix user is created and no sudo runs under this goal until the owner's go on the doc (owner chose "Design doc" over the spike).
- Nothing is deleted: a piece the doc scraps is retired and moved, per the graph's rules.
- Research tracks (goal:g5.*) keep running; this goal takes no research slot.

## Falsifier
1. `python3 extensions/agi/bin/write.py goal:g7.16.1.11 'read body 1:80'` lists a child doc node, and that doc has one section per Target end-state bullet plus the KEEP/REPLACE/SCRAP table (grep each heading: exit 0).
2. Negative: `getent passwd | grep -c '^agi-'` = 0 until the owner's go.

## Out of scope
goal:g7.16.1.7 (spawn/rotate unification) and the key / identity / rotate goals are HELD (owner 21:3xZ), not closed: the doc decides which it absorbs · goal:g7.16.1.8 (box stand-up) · goal:g5.* research · the owner's tree-context / chat-forking idea (banked separately as an idea node).

## OWNER 2026-09-30 21:2xZ, verbatim
"I feel bad saying this because I feel like the work is moving smoothly, but I think we might need to scrap a lot of it. I kept holding off on this part of the redesign because I kept thinking like it would just complicate things. But looking at what we've had to do so far just to enable key control, I think we need to go ahead and implement this now before we waste too many more tokens doing what we're doing now. it's not an issue of like the system not working well it's just an issue of me and you not brainstorming deeply enough and mostly it falls on me as like the owner to see through things more deeply and understand the more base things going on and kind of keep track of more things because human brains have this like weird thing our context it just keeps expanding in like a tree-like fashion like a graph in the human brain context just can infinitely keep growing on itself and it's like a binary tree search continuously no matter what you're doing and I don't know maybe we can implement something like that with forking and being able to like search through several conversations at once using the swarm methods but like also a conversation forking because Pi has this cool like chat forking feature and I think Claude does too so But anyway, this isn't the point. The point is that uh, I think we need to implement per post users and have each post have, among other things, in the .geometry node, it'll have the user assigned to that post with the proper user key and like the signing key and everything is like all just a part of the user sys account system. And we can basically, at that point, literally wrap write and render as shell scripts parsing over things. Well, render probably needs an actual render script because that'd be kind of useful and nice. But the write should probably just be a shell script because once we have per user posts or the other way, per post users, all the permission issues and write issues and read issues just go away because we can just set per file permissions permissions and each node is already a file so that works out and it links to other files and we can programmatically like update things.

Then post configs can modify actual user settings because those would be linked into the graph as symlinks."

## OWNER 2026-09-30 21:3xZ, verbatim (answers to the Prime's three questions)
Pause: "Pause key/ID/rotate stuff let research continue. Stand down DG 4 and pass on any leftovers back on the board as unclaimed bundle goals. Then stand thought master back up to coordinate research trajectory and tell him to stick to the research lane. They can use opus subagents for the research lane, up to 3 at a time. 5.5 on high setting."
Root go: "Design doc, but make the council work on it. They need to think of radically simple as key. One idea is to stop building worktrees, we only need to add nodes or change existing ones. So we should only ever have one or several per-node trees checked out on the fly and recycled when done. Same with a fresh one. For running tests we just let it mix and match the code via per-node worktrees if that makes sense. Then a write becomes a git commit or wrap it even based a literally system read/write function combo that adds up to git. But see like I keep taking pieces away since they're waste. Thebworktrees should allow code to run properly. Use the git graph feature or off-shelf scripts/packages as our graph for render too that way. You see how maximally simple it is but I'm sure I'm missing pieces still where more functions could flow together. But see that radical breaking down? It's just because human meat takes so long to do our version of kv cache compression. We have to loop small concepts into big ones until we can metamorphose them into better, more elegant small pieces. we always ask "but what is it I am ACTUALLY trying to do. Or what am I actually trying to get the machine to do here?" And keep in mind maybe just wrapping the whole thing in an MCP now as it works partially could be useful. The grok bot tram on core branch has a magic pane system working half way pretty well"
Builder: "DG3 supercharged by opus subagents up to 3 in parallel"

## OWNER 2026-09-30 21:4xZ, verbatim (sequence)
"Remember to let the council work on the design first before DG3 tackles it" · "And report back the design to you"

## Sequence
```
1 the council (alive · all-is-one · self-perpetuating) writes the design doc, discussed through the three lenses
2 the council reports the design to belam (ONE [decision] line + the doc id) -> belam relays it to the owner
3 only after that: director-general-3 builds it (Opus 5.5 subagents, up to 3 in parallel); no DG3 round before step 2
```

## Agent Notes
Assigned to **the council (alive · all-is-one · self-perpetuating)**; the build after it to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam gen 22, 21:4xZ 09-30: the order changes on the owner's two follow-up lines (verbatim in the body): the council writes the design first and reports it to belam; director-general-3 builds only after that. v0 had assigned DG3 directly.
<!-- THOUGHT:END -->
