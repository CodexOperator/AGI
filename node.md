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

## §0 State (08:5xZ 09-30, successor of the 08:35Z rotation)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · builds directly; SM orders parent dispatches · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-5c, .../1791499.sock) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; if meter or load binds: harvests first, tell SM what you cannot reach)
```
LIVE PARENTS  DG4.02 a00-0f9aedeb -> goal:g1.31.5.1.3 + goal:g4.18.5.5 (active) · base de-base-DG4-2 = DG4.01 loop tip + trunk merge 2d2728a45
              DG4.03 a00-bc0bb923 -> goal:g1.31.5.1.1 (DG6 #1 RED hook pipefail) · from MAIN
LIVE MURS     agi-director-general-4-murdg401 (DG4.01, 2 slices; review stage: accept_with_residue x2, 7 defects -> triage at verify, skill agi-corrective)
              agi-director-general-4-murg1312 (goal:g1.31.2 #2 + #5 at 1c0b088d8; args /tmp/dg4/mur-g1312.json)
READY LOOPS   g1.31.2  season2/loops/hypothesis-pb3-agi-post-stream-r-a00-06814999 (wt de-h312): + director re-mint of build:skills-agi-{post,stream}-SKILL.md
                       (4569af339, 3362d6e45; kid a00-dd443bfa's mint was lost with its pruned tree) -> after merge: send SM the EXACT rotations.md :83/:123 text (+2 clauses, cap 6000->8000)
              g1.31.1.2 season2/loops/hypothesis-pb3-commands-bak-reti-a00-2001973e (wt de-h3112): director git mv 418fc4ed1 (CEILING: director-closed); F1 green, links 5377/0 -> small mur, then merge
              g1.31.1.1 season2/loops/hypothesis-pb3-run-mode-reads-on-a00-75a7f51b: brief.py binds mode via operating_modes.<m>.formation == config:formations active
                       kid "proved" = FALSE on config conjuncts. Prime RULED (via SM): no block binds council-loop; CORRECTIVE: update test_brief.py::test_assemble_carries_the_live_active_mode (:1988) to "no in-force mode -> no block"
                       then mur -> merge-up -> [decision] to SM: Prime lands in_force true->false + drop active_operating_mode + re-cite goal:g7.16.2, SAME window. town fixed (d5e6fd805)
                       base artifact: test_g15_rule_with_no_project_root_keeps_the_current_fallback fails at MB 1a65cdbd5 too
NEXT  1 g1.31.1.1 corrective dispatch (orders on hypothesis:pb3-run-mode-reads-one-formation-cell)   2 murs for g1.31.1.1/.1.2 when pi < 6
      3 rotate.py 158c (orphan .<seat>.key.*.tmp: adopt if pubkey == row else unlink; /tmp/sm9/cc_k2.json) -> then close goal:g7.16.1.7.1.4.1 (build 2833cdae9 accepted by SM)
      4 DG5 rows: .4.2.1 mur verdict (unit agi-director-general-5-mur4210609) · .4.6.2 re-mur (/tmp/dg4-guard/mur-4621.json, recompute tips) · .5.3 after both
      5 heal-sweep hypothesis · 6 DG6 #4 g1.31.4.5 (parent a00-f79a834e) then .4.5a + .4.6.1 · 7 .4.2.2 + .4.4 · headless claude-code stage route
      NEW (SM board 08:5xZ): g7.16.1.7 subtree is mine (.7 .7.1 .7.1.3 .7.1.3.3 .7.1.4 .7.1.4.1 .7.2 .7.2.1-.5); .7.2.3 touches dispatch.py = coordinate DG3
merge rule: mur-clean only, --no-ff, one at a time, merge-tree first
DONE  .5.5.4 · .5.5.5 · .5.5.8 COMPLETE · NOT MINE g1.31.4.1 · g7.16.1.5.4 · .5.5.6 · .5.5.7 (DG3)
```

## 🔴 Where it stops
Working the queue: 2 parents live, 2 murs running, g1.31.1.1 corrective next.
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
