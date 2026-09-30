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

## §0 State (19:5xZ 09-30; NO STOP -- owner 17:4xZ: until 21:00Z Sonnet 5.5 subagents allowed; FROM 21:00Z every NEW round and review pi-free only)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-12 [afd9c6] since gen 10, 14:xxZ; fallback: send.py --from director-general-4 send --to sanctuary-master) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; lanes per §0)
```
LANDED 72dff76359 STACK DG4.06+15+21+11+22 · 2cbe754da1 DG4.17 (trees removed)
WITH SM, awaiting GO (tip · worktree to remove once landed: in trunk + clean, harvest iter-* first)
  g73319 2b68fbc07e dg4-g73319 · g75213 4336e659e4 dg4-g75213 (Prime: 3 guard cells + live bind) · SM-1 bd01ee8969 dg4-sm1
  SM-2 802577c1bd dg4-sm2 · DG4.12 af2c27335f dg4-dg412c (ON SM-2) · DG4.13 9baba2bc99 dg4-dg413c · r49 7eb1c65aed dg4-r49 (ON DG4.13)
  g1.31.4.2.1 LINEAGE 4620846a3f dg4-fdreaders + dg4-dg414c · DG4.18 c576956960 dg4-dg418m (Prime: locations.stream, rotations cap, grid)
  g1315131 d9fcbcbed5 dg4-g1315131 (Prime: hold_wait_s 90) · DG4.19 910989982e dg4-dg419c · DG4.10+20 a7b40781c3 dg4-dg420c
ALL HARVESTED ROUNDS DELIVERED (12 merge-ups with SM). Pi mur chain done (q2..q10).
HELD       C2c goal:g1.31.4.2.1.1: built 7d9f955842 (.agi/worktrees/dg4-c2c) but the copilot hooks LOCATION is invented (repo records none) -> [red] to SM 19:4xZ: needs a real copilot probe (premium turn = Prime/owner go) or park; + dispatch.py sess_dir (DG3). Not a merge-up.
HANDED     findings row 48 (kid commit dies on index.lock, parent waits silently) -> SM (dispatch/cli = DG3 region)
FROM 21:00Z: every NEW round + review pi-free only (workflow.py merge-up-review --harness pi-free; dispatch.py tier-0 parent), no Sonnet subagents
```

## 🔴 Where it stops
12 merge-ups with SM awaiting GO; nothing building; C2c HELD on a [red]. On each [GO][landed]: remove that round's worktrees (lossless). Then SM's next order. Rotate at f >= 0.47 (captive captured the card at 0.40).
Next command: `python3 extensions/agi/bin/send.py read director-general-4; git worktree list | grep dg4-`

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
| worktree cwd | creating a worktree flips the harness cwd into it: use absolute paths / git -C /data/work/agi |

## §5 Verification
links 0 broken · DG4.01 family 150 · g1.31.2 loop: test_locations 85, paths audit rc 0, cite ast rc 0 · g1.31.1.2 loop: F1 green, links 5377/0

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
