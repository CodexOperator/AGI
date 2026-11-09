---
id: goal:g5.4.3
mint_id: e48b53f3de494019a4e5c701bd98eeb6
type: goal
parents:
  - goal:g5.4
next_edges: []
confidence: 0.5
goal_id: G5.4.3
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 78b0dcb228aab812
season: 3
seeds: []
status: active
tags: []
title: "G5.4.3: The Meme Master post: the owner's presentation and the paper after it"
town: core
---

# goal:g5.4.3

## Why this exists
goal:g5.4 (the season review and rollover, end to end): the owner asked at 02:54Z 11-09 for a new post to help them make a presentation and the paper after it, "part of the core team", with the drafts grown through graph routes. A presentation and a paper about the season's system is the season review told outward, and g5.4.2 (the season media set) is its sibling there. The council placed it under g5.4 (alive [decision] 03:09:15Z 11-09, 3/3, part (1)). What made it a leaf: that owner ask, and the council's decision that the post is built under this leaf.

## OWNER 2026-11-09 02:54:27Z (c:db98e491500c), verbatim (chat to belam; belam's [owner] relay 02:58:14Z 11-09 to sanctuary-master)
"Can you start a new post to help me work on this presentation and the subsequent paper? It can be called Meme Master and will overall be a part of the core team to work alongside the rest. I have some brainstorm board photos I will need to hand him to turn into a plan for creating the presentation. I figured we could have the presentation and paper drafts be created via graph routes as well, as silly and recursive as that may be. Only thing is I have to actually write all the actual final wordings of both so I'll need his help with that, as in to help shepherd me along the path until I finish rewriting everything by hand, but in small bite-size chunks so I don't have to be overwhelmed by it like a silly person and also work on it in between being busy with the kid.
I figured they could get launch subagents using graph routes via parent/kid dispatches if that works well now or if not just use regular subagents. Mainly I want them to be a post so they can access the graph properly and ask questions as needed. They can also then coordinate with TM to gather benchmarks for the system as needed. I need them to be fully logged in so I can access them remotely as well on the same account you are currently using."

## OWNER 2026-11-09 03:03:02Z (c:b659f3c6bb5d), verbatim (the login answer; belam's [note] 03:05:08Z 11-09)
"Relay the login link"

## OWNER 2026-11-09 03:13:59Z (c:3a09b5900841), verbatim (chat to belam; belam's [owner] relay 03:14:32Z 11-09, the first part of three)
"the class presentation on 11/7 is related yes, it looks cool! Let him start from it."
The page it names: the 11-07 class presentation, a private claude.ai artifact, claude.ai/artifact/4uim4ZkNgg2Ma313tuPFC6, read by url once the post is logged in to the owner's account.

## Target end-state
1. The post meme-master stands: its config:posts row (role director, town core, parent keep), doc:role-meme-master and doc:card-meme-master (parent this leaf) are on the trunk; it is logged in to the owner's account with Remote Control live, and its row reads boot true.
2. Its starting point is the 11-07 class presentation above.
3. The presentation and then the paper exist in the owner's own final wording. The post's part: drafts as doc nodes marked DRAFT, and a shepherd loop that hands the owner one bite-size chunk at a time at the owner's pace, until the owner has rewritten everything by hand.

## Invariants
- The owner writes every final word; no node carries a wording as the owner's final.
- The owner's board photos stay in the post's home and are never committed; the graph gets only text derived from them, privacy-scanned.
- The post boxes sanctuary-master and thought-master; it never boxes belam.

## Falsifier
1. THE POST STANDS, from the repo top, exits 0 only when the row reads boot true and the role doc and the card exist with the card under this leaf:
   ```
   python3 -I -c 'import json,re,sys
   t=open(".agi/nodes/.geometry/posts.md").read()
   r=[json.loads(m) for m in re.findall(r"\{\"name\": \"meme-master\".*\}",t)]
   import os; c=".agi/nodes/doc/card-meme-master.md"
   ok=len(r)==1 and r[0].get("boot") is True and os.path.exists(".agi/nodes/doc/role-meme-master.md") and os.path.exists(c) and "  - goal:g5.4.3" in open(c).read().split("\n---")[0]
   sys.exit(not ok)'
   ```
   RUN at the mint on dfebc8f1c0: exit 1 (no row).
2. THE OWNER'S WORDING: an `## OWNER` block on this node, with its chunk id, in which the owner says the presentation and the paper are finished. Read by hand at the close; nothing mechanical decides it.
3. Negative, from the repo top, exits 0 only when no commit by the post (author meme-master) ever ADDED a binary file (git's numstat '-': a NUL in its first 8000 bytes), on HEAD or any branch, merges included, history included, so a later `git rm` never clears it (the photos never committed; the invariant's class is 'only text', not a list of a photo's spellings; git log exits 128 outside a repo, so the first conjunct pins the top level):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ "$(git log HEAD --branches --format= --numstat --diff-filter=A --diff-merges=remerge --author='^meme-master ' | awk -F"\t" '$1=="-"' | wc -l | tr -d " ")" = 0 ]`
   RUN at c695e19f31 (git 2.43.0): repo top 0 (no commit by meme-master), outside a repo 1. Mutants, scratch repos, the author set by GIT_AUTHOR_NAME (a post's env beats -c user.name), each 1: a camera-named JPEG, a .tif scan, a JPEG with no extension, a photo on a side branch (HEAD-only form: 0), a photo added inside a merge; a text note by meme-master 0.
   LIMITS: a kid committing under its own author is unseen (the post's kids are harness subagents until goal:g7.16.1.11.46.9's CLOSE; re-read F3 then); an image carried as text (SVG, base64 in a .md) reads 0, guarded by the role doc's hand read; refs/held/* and box refs are unseen, guarded by the land's objscan; a binary the post means to commit (a slide export) reads RED by the invariant's own text, the council's to allow.

## Out of scope
goal:g5.4.2 (the season media set) · the season 3 end STOP and the season 4 bundle on the core town board (owner 03:1xZ 11-09, parts two and three: a goal:g5.4 lane of its own, on the council's word) · belam's host acts (uid, home, login relay) · goal:g7.16.1.11.46.9 (whether graph-route parent/kid dispatch works; until its CLOSE the post's kids are harness subagents).

## Agent Notes
Assigned to **meme-master**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-09, the leaf's second version: Falsifier 3 replaced by the council's TERM for this touch (sp 03:36:26Z: name-blind BIN, binary files by numstat; alive 03:43:55Z: (a) HEAD --branches, a photo on the post's own branch was invisible from the trunk; (b) --diff-merges=remerge, a photo added inside a merge was invisible; aio 03:37:21Z AGREE), landed BEFORE the row's boot goes true. Version 1's F3 (images by extension, author meme-master, HEAD only) passed a .tif, an extensionless JPEG, a side branch and a merge (measured by sp and alive; re-run here). Nothing else in this node changed: the OWNER blocks, F1, F2, the Target and the Invariants are version 1's (L455, grid v1).
<!-- THOUGHT:END -->
