---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines; rules live in skills, progress on the town board.

## §0 State (21:4xZ 09-30) -- STOOD DOWN (owner 21:3xZ, verbatim via the seating post: "Stand down DG 4 and pass on any leftovers back on the board as unclaimed bundle goals.")
| | |
|---|---|
| post | director-general-4 · DOWN: no live parent, kid, unit or subagent; nothing building |
| leftovers | 25 open goal leaves -> status horizon, Agent Notes "Unassigned (was director-general-4)" (write.py sub, 25 commits) |

## §1 Where everything stopped
```
LANDED on local-maxxing/season2/main: 72dff76359 STACK DG4.06+15+21+11+22 · 2cbe754da1 DG4.17 · a2e42a3bf0 g1315131 (+ Prime cell hold_wait_s 90)
  · 5a7a3bb828 DG4.10+20 · e81abd3f69 DG4.19
WITH SM (delivered, SM gates + lands them; worktree = .agi/worktrees/<name>, remove after landing, lossless):
  g73319 2b68fbc07e dg4-g73319 · SM-1 bd01ee8969 dg4-sm1 · SM-2 802577c1bd dg4-sm2 · DG4.12 af2c27335f dg4-dg412c (ON SM-2)
  DG4.13 9baba2bc99 dg4-dg413c · r49 7eb1c65aed dg4-r49 (ON DG4.13) · g1.31.4.2.1 LINEAGE 2ec78512d4 dg4-fdreaders (+ dg4-dg414c)
  g75213 7cd127824e dg4-g75213: code gate green, GO = the Prime's DISK bind of <MAIN>/.claude/worktrees + 3 guard cells
  DG4.18 c576956960 dg4-dg418m: HELD on 3 Prime cells (locations.stream, rotations byte_cap 8000, 2 grid versions)
PARKED  goal:g1.31.4.2.1.1 (C2c copilot hooks): 7d9f955842 in dg4-c2c, location invented -> never a merge-up until a real copilot probe (SPEND, Prime)
BACK ON THE BOARD (horizon, unassigned): active before -> g1.31.4.2.1.1 · g1.31.5.1.3.1 · g1.31.5.1.3 · g7.16.1.5.3.1 · g7.16.1.7.1.4 · g7.16.1.7.1 · g7.16.1.7
  already horizon -> g4.18.5.6 · g7.16.1.10.1 · .10.2 · .10.6 · g7.16.1.7.1.3 · .7.1.3.3 · .7.1.4.2 · .7.1.6 · .7.1.7 · .7.1.8 · g7.16.1.7.2 · .7.2.1-.7.2.6 · .7.2.8
  notes: g1.31.5.1.3.1's fix LANDED (a2e42a3bf0; DG2 re-runs run_on.sh x3 on it) -> likely closeable by whoever claims it
FINDINGS goal:g7.33.19 rows 47-50 (row 48 handed to SM: DG3 region)
```

## 🔴 Where it stops
Down. A successor on these leaves starts from the board; the merge-ups above are SM's to land. No command owed by this post.

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared -- swept DG3's WIP once (1098822e1) | hunk/line check IN THE SAME COMMAND as `git commit -- <paths>`; retry only on an index.lock error |
| stale .git/index.lock | a lock no process holds (fd scan) -> move aside to /tmp, never delete |
| verify-suite.lock | the conftest refuses cleanly -> retry on "suite window refused"; a printed LOCKED is no guard |
| engine slice memory | `file` there can be SHMEM (RAM disk): reclaim cannot free it; read memory.stat shmem first |
| write.py on a node with a THOUGHT | replace body must cover the H1 section through THOUGHT END (carry the block whole); never --force |
| config.json | not json.dumps round-trippable: insert cells as text, json.loads to verify |
| SendMessage | a bare name can fail ("Failed to send") -> ListAgents, retry with the [ref] |
| config:guard ring | a director's write.py on config:* is refused (owner / prime_director only): hand the exact text to SM |
| renumber by script | never str.replace a Why/id prefix: it hit the id row of .5.5.5 (d1eb5ecad); use write.py or anchor on the full line |
| suite lock rotating | short live suites hold it with a new pid each time: retry the conftest refusal with backoff (7 tries = ~90 s) |
| send body | never backticks or $( in a send.py body: the shell eats them (19:5xZ lost a quoted phrase) -- body from a scratch file |
| worktree cwd | creating a worktree flips the harness cwd into it: use absolute paths / git -C /data/work/agi |

## §5 Verification
links 0 broken · DG4.01 family 150 · g1.31.2 loop: test_locations 85, paths audit rc 0, cite ast rc 0 · g1.31.1.2 loop: F1 green, links 5377/0

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
