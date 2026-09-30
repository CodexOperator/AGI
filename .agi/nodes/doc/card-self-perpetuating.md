---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: self-perpetuating
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (21:5xZ 09-30 · rotating out at f=0.454, before the line: the next step cannot finish in this session)
| | |
|---|---|
| post | self-perpetuating · outgoing CC session agi-53 (ref 21dc2d, session 824fea59) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed and the assignment below asks for it |
| history | the whole history was rewritten 06:3xZ-08:0xZ: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map`; every sha here is post-scrub |
| sessions | names change after every reboot/rotation: map ListAgents' tmux @window against the posts row's window cell. 13:5xZ: alive agi-e3 [761106] @16 · all-is-one agi-8f [242e8c] @1 (rotating) · SM agi-12 @27 · DG1 agi-8c [9e0227] @21 · DG3 agi-b4 @26 · Prime agi-23 |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
NEXT   goal:g7.16.1.11 (owner 21:3x-21:4xZ 09-30, assigned to the council via agi-a3): ONE council design doc for a
       RADICALLY SIMPLE engine -- per-post Unix users, write = a git commit, no standing worktrees, render off the
       git graph, an MCP wrapper, a KEEP/REPLACE/SCRAP table. The three lenses design it FIRST, then ONE [decision]
       line to belam with the doc id; DG3 builds only after. Free lane; no users created, no sudo.
then   lens DG3's .10.3/.10.5/.10.7 as they land · no OVERVIEW until g7.16.1.1.6, .6, .7, bundle 4 close
```

## §2 Landed (09-29 -> 09-30)
- goal:g7.16.1.10 (merge-up reviews off the Prime): leaves .10.1-.10.7 by DG1; .10.7 the merge gate placed with DG3 (1c31bfe443), negative covers all 3 refusals; SM added the lane (7e24903cdb)
- .7 coverage: 6 HORIZON leaves .7.1.5-.7 + .7.2.6-.8 by DG1; .7 guard = box NAME (e74848a415); finding 1 withdrawn (already fixed in HEAD)
- S-goal pass: s34 s4 s21 retired in place -> g6.50 · g4.21 · g4.18.5.4 (retire + renumber verbs); s1 -> g1.6.1
- .7 + .8 rewrites · g7.16.1.1.6 (proof + census) · bundle 2 outcome · rulings: keys (C) + witness · replace payload NO · W2b body refs = declared regions · residue 154 fail-closed

## 🔴 Where it stops
goal:g7.16.1.11 council design doc handed on whole: read the goal and the inbox first, then convene the three lenses
```
python3 extensions/agi/bin/write.py goal:g7.16.1.11 'read body 1:80'
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; verify-suite.lock blocks commits | write.py lands uncommitted under the lock: commit by exact path once it clears (background wait loop) |
| a pre-commit hook refuses owner email / GPU name / pytest-of-<user> / box tokens | redact and commit again; never --no-verify |
| a sha from memory is wrong after the scrub | map it through the commit-map, or re-read git log |
| a new file + `git commit -- path` fails | `git add -- <path>` first |
| renumber: write.py refuses `set id` | git mv + the id line by hand, other fields via write.py, ONE commit |
| an owner quote keeps its contractions; a stamp never post-dates its commit | escape `'"'"'`; check `git log -1 --format=%cI` |
| a review of the working tree can race a director's fix | re-check a regression against HEAD before routing it |
| a big design is context-heavy | fan the reading out to subagents (Sonnet 5.5; Opus only when the owner opens it) and keep the judgment |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken

## §6 BANKED
(none)
