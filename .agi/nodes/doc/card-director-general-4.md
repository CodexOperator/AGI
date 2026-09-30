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

## §0 State (13:50Z 09-30, RESUMED on belam's order until 18:00Z -- a STOP comes at 18:00Z)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-12 [afd9c6] since gen 10, 14:xxZ; fallback: send.py --from director-general-4 send --to sanctuary-master) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE PARENTS  DG4.17 a00-012eab57 -> g1.31.1.1 3rd pass (stderr line count + node prose; base de-base-DG4-17 = 2ffa3b259)
              DG4.19 a00-d2c9ccdf -> hypothesis:a-skipped-rotate-join-leaves-no-stranded-window (row 34, rotate.py not-found join branch; from MAIN)
              DG4.18 a00-12019258 -> g1.31.2 stream 3rd pass ($B guard, deliverable 5, commands.stream.fragment, row that can't fail; base de-base-DG4-18 = chain head 92dd46207)
LIVE MURS     murdg415 = DG4.15 g4.18.5.5 (SM's FIRST: on a clean verdict -> [merge-up] to SM + the values.core.suite_lock.file cell text; resolver = verification.suite_lock_name)
              chain murq2 dg410 -> murq3 dg406 -> murq4 dg412 -> murq5 dg413 + 4621 -> murq6 dg414 (each /tmp/dg4/qrunN.sh waits on the previous unit)
HARVESTED tips (measured):
  DG4.15 6575a88d7 g4.18.5.5: SUITE_LOCK = 0 hits, F1 3 passed, write 44 / verification 100 / node_writer 130 (rotate.py + suite_guards.py 1-line reader moves)
  DG4.14 e51efb790 g1.31.4.2.1 2nd: fd+copilot 35, dispatch 138 (+1 base artifact: scrubbed sha) -- touches dispatch.py +22 (DG3's file: name it at merge-up)
  DG4.06 a8b9e67e0 · DG4.10 d8f0b9ee0 · DG4.12 589c6dafd · DG4.13 (branch ...engine-root-one-r-a00-925ffcca) -- all green, in the mur chain
  g1.31.2 chain head 92dd46207 -> DG4.18 · g1.31.1.1 2ffa3b259 -> DG4.17
QUEUED (SM order, drain AFTER: DG4.15 merge-up · DG4.11 · DG4.19)
        SM-1 hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove (.5.3; DG2 b6e56296a5) -> on land the Prime restarts heal; .5.3.1 closes on a >= 25-tree pass, 0 kills
        SM-2 hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat (.7.1.4.1 lane; DG2 d087b6091e): G1 cmd_loop w/o --seat keys the resolved seat · G2 remint via send._mint_seat_key only · G3 spawn dry-run names mint vs adopt · prod <= 40, tests <= 60
        DG4.11 = DG4.02 residues (/tmp/dg4/orders-DG4.11.md) -> cut from the DG4.15 tip once its mur is clean (one writer in _commit_write)
OWED TO SM AT MERGE-UPS  g4.18.5.5: values.core.suite_lock.file (+ wait/hold if the mur says they belong) · g1.31.1.1: [decision] Prime config lines
  g1.31.2: rotations.md :83/:123 clauses + cap 6000->8000, locations.stream cell · g1.31.4.5b: retire engine_commit · C2 copilot goal leaf to mint
LANDED 9f124d68f g1.31.1.2 · RULE: [merge-up] to SM FIRST, land on SM's GO (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only)
FINDINGS goal:g7.33.19 rows 25 · 26 · 27 · 34 (stranded window)
DONE  .5.5.4 · .5.5.5 · .5.5.8 · g1.31.1.2 · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
Resumed 13:5xZ; 2 parents live, DG4.15's review running first, 5-unit mur chain queued.
Next command: `systemctl --user show agi-director-general-4-murdg415 -p SubState; ls .agi/sessions/workflows/runs/ -t | head -3` then the DG4.15 verify file -> [merge-up] to SM.

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
