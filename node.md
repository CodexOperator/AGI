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

## §0 State (18:5xZ 09-30; NO STOP -- owner 17:4xZ: until 21:00Z pi-free + claude-code Sonnet 5.5 + Sonnet subagents + direct; FROM 21:00Z every NEW round and review pi-free only)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-12 [afd9c6] since gen 10, 14:xxZ; fallback: send.py --from director-general-4 send --to sanctuary-master) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; lanes per §0)
```
LANDED 72dff76359: STACK DG4.06+15+21+11+22 (trees removed)
WITH SM (awaiting GO/gate): g73319 2b68fbc07e · g75213 4336e659e4 (Prime: 3 guard cells + live bind) · SM-1 bd01ee8969 (gating) · SM-2 802577c1bd · DG4.17 2c4c5d34bb (gating 18:34Z) · DG4.13 9baba2bc99
BUILDING (Sonnet 5.5 subagents; each: verify -> Sonnet review -> corrective -> [merge-up])
  g1315131  .agi/worktrees/dg4-g1315131  SM [red+] goal:g1.31.5.1.3.1: held suite lock WAITED (hold_wait_s cell) + peer in-flight marker; judged on DG2 harness bash /tmp/dg2mvp/g41855/run_on.sh <sha> 3
  DG4.12c   .agi/worktrees/dg4-dg412c    merges SM-2 (conflict in _remint_missing_key) + remint residues; lands AFTER SM-2
  g13142    .agi/worktrees/dg4-fdreaders  on 70599a543b: first-decision / harvest-table one naming helper (DG4.14c strict xfail)
REVIEWING  g1.31.4.2.1 lineage 2f60b2dff1..70599a543b (orig + DG4.05 + DG4.14 + DG4.14c, 24 files; dispatch.py +22 = DG3 file) -> one [merge-up] (+ g13142 on top)
PI MURS    murq8 dg418 · murq9 dg419 · murq10 dg420 (DG4.18 8097dec13 · DG4.19 10780f70e · DG4.20 0f0e5905cf) -> residue correctives
FINDINGS   goal:g7.33.19 rows 47-50 added (bfd33b11f7)
FROM 21:00Z: every NEW round + review on pi-free (workflow.py merge-up-review --harness pi-free; dispatch.py tier-0 parent), no new Sonnet
```

## 🔴 Where it stops
Six merge-ups with SM; three rounds building; one lineage under review; three pi murs queued.
Next command: `python3 extensions/agi/bin/send.py read director-general-4; git worktree list | grep dg4-; systemctl --user list-units 'agi-director-general-4-*' --no-pager`

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
