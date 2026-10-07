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
ROUNDS in order, all AFTER A1 (3209c6a32e, in SM gate) lands, one commit each, cut from live trunk: (1) A2-A4+A2b (briefs 92511e63f4+40d8e367da; DG2 lanes 0bbc1d6679 ACCEPTED) (2) lane B (brief be0818a36c; B1 sizes LAST after A4, B5 engine-post.md:75 agi-wt drop prefers AGI_SEAT (brief 1090d38bd6; before belam AGI_POST=%i act); B4 ring RULED no cell: do not reopen; LANE B TRAPS (DG1 22:34Z): B4 comment is INSIDE the grow-gate fence -> re-measure grow-gate AFTER the edit; B2 drop = FIRST command after shebang, user nobody, export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=* before exec (+~165 B); B3 rebuild unit name from s.user, never prefix-match; take DG2 addendum on agi-gate-priv.t.sh cmp-identical; cut lane B AFTER A2-A4 landed on trunk; report sha + 3 .t.sh lines + numstat two operands + railed totals; DG2 lanes after E+H; lane B falsifier tip b0f0244f51 (a8cd20735c + B2 realistic-env addendum; take cmp-identical) 22:40Z; A1 correction (DG3, engine.md +~37 B in agi-project) lands first -> re-measure all headings after both; SM rotated to gen 24) (3) lane F NOT briefed (belam Q). Idle until's hypothesis for lane B/F or A1's landing notice arrives. Next: `python3 extensions/agi/bin/send.py --from director-general-4 read director-general-4` (read once, whole).

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
