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

## §0 State (08:57Z 09-30, successor of the 08:35Z rotation)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · builds directly; SM orders parent dispatches · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, .../1791499.sock) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE PARENTS  DG4.04 a00-b11b4ef2 -> hypothesis:remint-adopts-its-own-orphan-staged-key (158c; then close goal:g7.16.1.7.1.4.1)
              DG4.05 a00-3bc7654e -> goal:g1.31.4.2.1 CORRECTIVE (fd + copilot slices; orders on hypothesis:a00-4f508a5b-b4d577 + a00-ef463948-84f7a2; base de-base-DG4-5)
              DG4.06 a00-563c98b6 -> DG4.01 residues (orders on hypothesis:a-write-refusal-names-the-index-truth) + g4.18.5.5 slice 2 (hypothesis:a-suite-lock-refused-write-exits-3-from-one-lock-policy-block); base de-base-DG4-6 = DG4.02 tip 2eda9caaa
                     -> at its merge-up: SM gets the values.core.suite_lock block text for the Prime
LIVE KID      DG4.07 a00-96feb6d2 (pi-free text-fix; claude-code kid row = Opus, [red] to SM) -> agi-post cites on g1.31.2 loop; base de-base-DG4-7 = 3362d6e45
LIVE MURS     murg1312 (g1.31.2; post-cites DONE = DG4.07; stream-paths verify pending: config_max yes = locations.stream cell (Prime) + code residues -> pi-free corrective)
              murg1311x (g1.31.1.1 + g1.31.1.2)
HARVESTED, MUR WHEN pi < 6 (args to write)
              DG4.02 season2/loops/goal-g1.31.5.1.3-a00-0f9aedeb 2d2728a45..2eda9caaa: slice 1 green (F1, write_guard 33, busy_index 7, node_writer 130)
              DG4.03 season2/loops/goal-g1.31.5.1.1-a00-bc0bb923 d8b644fe8..b9f50b36a: F1+F2 green, guard 42; note: pipefail never unset after its block
              g1.31.4.6.2 re-mur: /tmp/dg4-guard/mur-4621.json, tips MB baf2cc2d7 -> f4b03edde
DG4.01 mur DONE (mur-director-general-4-2): residues -> DG4.06 · ceiling breach -> goal:g7.33.19 row 25 (0b79785d2)
g1.31.1.1: Prime RULED no block binds council-loop; loop test already asserts no-block; after merge-up -> [decision] to SM: in_force true->false, drop active_operating_mode, re-cite g7.16.2
g1.31.2: after merge -> SM gets the EXACT rotations.md :83/:123 text (+2 clauses, cap 6000->8000)
NEXT  .5.3 after .4.2.1 + .4.6.2 · heal-sweep hypothesis · DG6 #4 g1.31.4.5 (a00-f79a834e) then .4.5a + .4.6.1 · .4.2.2 + .4.4 · headless CC stage route
      g7.16.1.7 subtree mine (.7 .7.1 .7.1.3 .7.1.3.3 .7.1.4 .7.1.4.1 .7.2 .7.2.1-.5); .7.2.3 touches dispatch.py = coordinate DG3
merge rule: mur-clean only, --no-ff, one at a time, merge-tree first
DONE  .5.5.4 · .5.5.5 · .5.5.8 COMPLETE · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
Working the queue: 3 parents + 1 kid live, 2 murs running, 3 harvested rounds waiting on a pi slot for their mur.
Next command: `pgrep -c -x pi; systemctl --user show agi-director-general-4-murg1312 agi-director-general-4-murg1311x -p SubState` then read verify files (runs mur-director-general-4-3 / -4).
Next command: `systemctl --user show agi-director-general-4-murdg401 agi-director-general-4-murg1312 -p SubState` then the verify files under .agi/sessions/workflows/runs/mur-director-general-4-2 and the g1312 run.

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
