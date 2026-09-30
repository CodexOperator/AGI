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

## §0 State (11:03Z 09-30, STOPPED on belam's order: the owner's run ended 11:00Z -- idle, start nothing)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, .../1791499.sock) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
STOPPED 11:03Z (belam [rule] via agi-23: finish the atomic step, commit, card, idle; no new round or subagent)
IN FLIGHT (left running, nothing new started): DG4.14 a00-afa6f87f RETURNED 12:04Z: g1.31.4.2.1 2nd pass tip e51efb790 (4 accepted) -- UNHARVESTED ·
        DG4.15 a00-f7261183 RETURNED 11:44Z: g4.18.5.5 tip 6575a88d7 (1 kid accepted, experiment:a00-5c0a1d64-47f9f4) -- UNHARVESTED; on resume harvest + mur FIRST, [merge-up] to SM first ·
        review unit agi-director-general-4-murq1 (mur-dg40789 = DG4.07/08/09; its last queued args held: /tmp/dg4/mur-4621.json.held)
STOPPED units (never ran): murq2 dg410 · murq3 dg406 · murq4 dg412 · murq5 dg413 -- args in /tmp/dg4/mur-dg4{10,06,12,13}.json
HARVESTED, awaiting review (tip · measured):
  DG4.06 a8b9e67e0 DG4.01 residues 1-6 · busy_index 10 / write_guard 33 / node_writer 130
  DG4.10 d8f0b9ee0 hook attribution · guard 43, corrupted-index probe names git rc 128
  DG4.12 589c6dafd 158c 2nd · stand_up 34, hook neighbourhood 165
  DG4.13 season2/loops/hypothesis-pb3-engine-root-one-r-a00-925ffcca · in a worktree: commands 40, drift_check 16, verification 75
  DG4.16 92dd46207 = g1.31.2 CHAIN HEAD (DG4.08 + DG4.07 + trunk + cites 2nd pass, Sonnet kid)
  DG4.09 2ffa3b259 run-mode · review: node-prose residues only -> director closes (TMM.327) once verify lands
QUEUED ORDERS  DG4.11 = DG4.02 residues (/tmp/dg4/orders-DG4.11.md) -> cut from the DG4.15 tip (one writer in _commit_write)
OWED TO SM AT MERGE-UPS  g4.18.5.5: values.core.suite_lock block · g1.31.1.1: [decision] Prime config lines (in_force, active_operating_mode, g7.16.2 cite)
  g1.31.2: rotations.md :83/:123 clauses + cap 6000->8000, locations.stream cell · g1.31.4.5b: retire engine_commit · C2 copilot goal leaf to mint
LANDED 9f124d68f g1.31.1.2 · RULE: [merge-up] to SM FIRST, land on SM's GO (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only)
FINDINGS goal:g7.33.19 rows 25 (ceiling breach) · 26 (hook pinned to spawning tree) · 27 (parent notes on a goal)
DONE  .5.5.4 · .5.5.5 · .5.5.8 · g1.31.1.2 · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
Stopped at 11:03Z on belam's order (the owner's run ended 11:00Z): 2 parents + 1 review unit still in flight, 6 tips harvested awaiting review, nothing new started.
Next command, ONLY after a resume order: `python3 extensions/agi/bin/spawn_budget.py status; systemctl --user list-units 'agi-director-general-4-*' --no-pager` -- then re-launch murq2..5 (`systemd-run --user --unit=agi-director-general-4-murqN ... /tmp/dg4/qrunN.sh`), harvest DG4.14/15, and send SM the DG4.15 [merge-up] first.

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
