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

## §0 State (13:58Z 09-30, resumed on belam's order until 18:00Z -- a STOP comes at 18:00Z)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-12 [afd9c6] since gen 10, 14:xxZ; fallback: send.py --from director-general-4 send --to sanctuary-master) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE PARENTS  DG4.19 a00-d2c9ccdf -> hypothesis:a-skipped-rotate-join-leaves-no-stranded-window (row 34; from MAIN)
LIVE KID      DG4.20 a00-2b0cde65 (claude-code Sonnet) -> hook COMMENT text fix; base de-base-DG4-20 = d8f0b9ee0 + trunk
DG4.15 = SM's FIRST (g4.18.5.5, tip 6575a88d7, green): mur murdg415 (run mur-director-general-4-9) REVIEW accept_with_residue, config_max yes; VERIFY PENDING
   review residues: write wait NOT in values.core.suite_lock (still values.core.write_commit_wait_s) · hold rule has no cell · heal.py unlinks verify-suite.lock by LITERAL · config block absent (Prime)
   -> on verify: ONE corrective DG4.21 from 6575a88d7 (resolver reads file + write_commit_wait_s + hold from ONE block with STOPGAP fallback; heal.py via suite_lock_name), re-mur,
      then [merge-up] to SM (agi-12) + the exact values.core.suite_lock block text for the Prime
MUR CHAIN (each /tmp/dg4/qrunN.sh waits on the previous unit): murq2 dg410 DONE -> murq3 dg406 -> murq4 dg412 -> murq5 dg413 + 4621 -> murq6 dg414 -> murq7 dg417 -> murq8 dg418
   run dirs .agi/sessions/workflows/runs/mur-director-general-4-N (newest = highest N)
HARVESTED tips (all green on their touched family):
  DG4.06 a8b9e67e0 · DG4.12 589c6dafd · DG4.13 ...engine-root-one-r-a00-925ffcca · DG4.14 e51efb790 (dispatch.py +22 = DG3's file) · DG4.17 7c1da7497 · DG4.18 8097dec13
  DG4.10 d8f0b9ee0 (mur done: pure-text residues -> DG4.20)
QUEUED (SM order, drain AFTER: DG4.15 merge-up · DG4.11 · DG4.19)
  DG4.11 = DG4.02 residues (/tmp/dg4/orders-DG4.11.md) -> cut from the DG4.15/DG4.21 tip (one writer in _commit_write)
  SM-1 hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove (.5.3; DG2 b6e56296a5) -> on land the Prime restarts heal; .5.3.1 closes on a >= 25-tree pass, 0 kills
  SM-2 hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat (.7.1.4.1 lane; DG2 d087b6091e): G1 · G2 · G3 · prod <= 40, tests <= 60
OWED TO SM AT MERGE-UPS  g4.18.5.5: values.core.suite_lock block · g1.31.1.1: [decision] Prime config lines (in_force, active_operating_mode, g7.16.2 cite)
  g1.31.2: rotations.md :83/:123 clauses + cap 6000->8000, locations.stream cell · g1.31.4.5b: retire engine_commit · C2 copilot goal leaf to mint
LANDED 9f124d68f g1.31.1.2 · RULE: [merge-up] to SM FIRST, land on SM's GO (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only)
FINDINGS goal:g7.33.19 rows 25 · 26 · 27 · 34 (stranded window)
DONE  .5.5.4 · .5.5.5 · .5.5.8 · g1.31.1.2 · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
DG4.15 verify pending, then its corrective DG4.21 and the merge-up to SM; DG4.19 + DG4.20 live; 7-unit mur chain running.
Next command: `ls .agi/sessions/workflows/runs/mur-director-general-4-9/; python3 extensions/agi/bin/spawn_budget.py status; systemctl --user list-units 'agi-director-general-4-*' --no-pager`

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
