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

## §0 State (19:1xZ 09-30; NO STOP -- owner 17:4xZ: until 21:00Z Sonnet 5.5 subagents allowed; FROM 21:00Z every NEW round and review pi-free only)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-12 [afd9c6] since gen 10, 14:xxZ; fallback: send.py --from director-general-4 send --to sanctuary-master) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; lanes per §0)
```
LANDED 72dff76359: STACK DG4.06+15+21+11+22
WITH SM (delivered, awaiting GO / gating): g73319 2b68fbc07e · g75213 4336e659e4 (Prime: 3 guard cells + live bind) · SM-1 bd01ee8969 · SM-2 802577c1bd
  · DG4.17 2c4c5d34bb · DG4.13 9baba2bc99 · DG4.12 af2c27335f (STACKED ON SM-2: land after it) · g1.31.4.2.1 LINEAGE 4620846a3f (orig+DG4.05+DG4.14+14c+g13142+b)
BUILDING (Sonnet 5.5 subagents; on their report: verify bytes + tests -> [merge-up] with review badge)
  g1315131b .agi/worktrees/dg4-g1315131  SM [red+] goal:g1.31.5.1.3.1; tip 6815fde7b1 met F1 (HARD 3/3, false rc3 5/0/0); review accept_with_residue
            (latency MAJOR-leaning) -> b: hold_wait_s 90, non-finite refused, pid<=0 stale, lock re-check per commit attempt, own-marker clear
            -> then [merge-up]; Prime cell: values.core.suite_lock.hold_wait_s = 90; ceiling 53/30 prod disclosed
  DG4.19d   .agi/worktrees/dg4-dg419c    tip 64b8f3c0a9 (+THOUGHT 1301b3a9bc) review accept_with_residue -> d: heal skip also already_gone, guarded pre-kill record write -> [merge-up]
  DG4.18c   .agi/worktrees/dg4-dg418m    DG4.18 8097dec13 + trunk merge c576956960 (de-based branch fixed, 0 D); NEW red test_commands::test_a_bare_first_word_runs_a_declared_command
            (passes on trunk) -> c fixes it; test_engine_for_resolves_the_engine_enclosing_the_graph is RED ON TRUNK too (not ours)
            -> [merge-up] + Prime items: locations.stream cell, rotations.md skills cap 6000->8000 (g1.31.2), grid versions of 2 experiment nodes
PI MUR     murq10 dg420 running (DG4.20 0f0e5905cf comment-only) -> accept -> [merge-up]
FINDINGS   goal:g7.33.19 rows 47-50 (bfd33b11f7)
FROM 21:00Z: every NEW round + review pi-free only (workflow.py merge-up-review --harness pi-free; dispatch.py tier-0 parent)
```

## 🔴 Where it stops
8 merge-ups with SM; 3 correctives building (g1315131b · DG4.19d · DG4.18c); DG4.20 pi mur running. A subagent's report lands in THIS session only -- a successor re-derives from the branches: `git -C <tree> log --oneline -3` per tree above.
Next command: `python3 extensions/agi/bin/send.py read director-general-4; for t in dg4-g1315131 dg4-dg419c dg4-dg418m; do git -C .agi/worktrees/$t log --oneline -2; done`

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
