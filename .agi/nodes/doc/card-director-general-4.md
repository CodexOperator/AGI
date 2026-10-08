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

## §0 State (21:1xZ 10-07) -- RE-SEATED under sanctuary-master (owner 21:0xZ: "Let's stand up DG4 and DG5 to help split the workload a bit.")
| | |
|---|---|
| post | director-general-4 · UP: no parent, kid or unit running; trunk merged into posts/director-general-4 (ee1972c144) |
| order | SM [order] 21:05Z: build goal:g1.41 lanes, ONE commit chain per round; DG1 writes the hypothesis, DG2 the lanes, DG1 sends SM ONE [merge-up]; Sonnet 5.5; NO key / identity / rotate work (g7.16.1.11 HOLD) |

## §1 Plan (goal:g1.41, board e538e69d87)
```
B  .geometry/engine-grow.md :41,60 (ring cell) + engine-post.md :144 polkit ... WAITS on A1 landing
F  grid.py :895,911-913,1240-1280 ........................................... WAITS on belam's owner Q (double-write fix shape)
A2-A4  engine-root.md + engine.md ....................................... pass to DG4 at A1's landing (DG3 holds)
```
A2-A4 BRIEFED (DG1 21:49Z): hypothesis:g141-a2-a4-root-pieces-fail-closed-on-a-bad-cell-a-missing-agi-run-an-absent-carry-post-and-a-bad-post-name @ 92511e63f4 on posts/director-general-1; build only AFTER DG2 lanes + A1 (DG3) landed; cut from live trunk; engine.md = A4 only, measure fenced/whole (awk over fences) in the same commit; skip-and-rc-0 + later agi-gate refusal are belam decisions

## 🔴 Where it stops
```
ONE ASK (DG1 [order] 16:29Z, supersedes idle): the agi-at row DONE = 3d53e53986 (branch dg4-agiat-row, test-only, x14e, mutants RED; sent to DG1 + DG3). Then idle. Before that: IDLE (DG1 HOLD 16:27Z): build NOTHING from the old brief. Landed by others: lane B v5 a326fc3364 · boot leaf a7b3af22ea · E2a crons_apply installed (belam host act) · E2b0 v8 014209084b · grid_census = DG3 (DG2 rows in flight). DG3 is the only live builder.
MINE, landed or returned: A2-A4 e9892ee5c8 (branch dg4-a2a4-recut: 6ceac30357, 91015ff007, 1146e783aa). Lane F cancelled (owner).
NEXT: only a NEW belam order (tell DG1 its text in one line). No goal invented to fill a budget.
read inbox: `python3 extensions/agi/bin/send.py --from director-general-4 read director-general-4` (once, whole). pytest: PYTHONPATH=<scratch>/pylib (pip install --target pytest).
```

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
