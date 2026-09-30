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

## §0 State (17:5xZ 09-30; NO STOP -- owner 17:4xZ via SM: until 21:00Z pi-free + claude-code Sonnet 5.5 + Sonnet subagents + direct; FROM 21:00Z every NEW round and review on pi-free only, live claude-code rounds finish, nothing new on them)
| | |
|---|---|
| post | director-general-4 · owner: resume on the town bundle; subagents Sonnet 5.5 only |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · SM orders parent dispatches · LAND ORDER (SM 09:2xZ): [merge-up] to SM FIRST with tip + range -> SM gates by SHA -> SM's GO -> I land (merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only; 0 dirty overlap) · pre-commit hook refuses owner email / GPU / pytest-of-<user> tokens: redact, never --no-verify |
| messaging | SendMessage by uds address · coordination -> sanctuary-master (agi-12 [afd9c6] since gen 10, 14:xxZ; fallback: send.py --from director-general-4 send --to sanctuary-master) · rulings -> the council (alive) · NEVER the Prime |
| skills | agi-goal · agi-node-write · agi-dispatch · agi-corrective · agi-verify · agi-send · agi-rotate · agi-workflow · agi-master-gate |
| regions | write.py `_commit_write` · rotate.py WHOLLY + heal.py key path (from DG5) · DG6's rows below · rest of write.py = DG3 · dispatch.py / RAM writers = DG3 |

## §1 Plan (SM's order; lanes per §0)
```
DELIVERED, AWAITING SM GO (land: merge-tree T2 on live HEAD, commit-tree -p HEAD -p tip, ff-only)
  g73319 tip 2b68fbc07e (.agi/worktrees/dg4-g73319) ACCEPT -- trunk red test_g15 fallback fixed, test-only
  g75213 tip 4336e659e4 (.agi/worktrees/dg4-g75213) 3 review passes, all MAJOR closed -- PRIME ACTIONS in the merge-up line (3 config:guard cells + the live .claude/worktrees bind)
LANDED 72dff76359 (18:07Z): the STACK DG4.06+15+21+11+22 (tip 89639ad511); its trees removed (a00-3ed24d3e RAM, dg4-dg411, dg4-dg422)
  5349885273 DG4.21 (orphaned kid harvested) · aed1766f51 DG4.11 · dca05676f4 merge DG4.22 (6f48522331) · stacked tip 458 passed 8 skipped 5 xfailed
  reviews: stacked accept_with_residue -> MAJORs closed by DG4.11 + DG4.22 (re-review cites); DG4.11 re-review: item 4 FAILED OPEN (my order) -> DG4.11b (retry diff once, then fail closed) sent 17:4xZ to the Sonnet subagent
  DG4.11b ae6b08595d: retry diff once then FAIL CLOSED (fixes my fail-open order); 181 passed 3 xfailed; config_max block text is in the merge-up line
  prose item CLOSED 6517b71361 + 89639ad511 (write.py unset; AGI_ACTOR=director-general-4 sets edited_by)
PI MUR CHAIN (older harvests, still running): q6 dg414 -> q7 dg417 -> q8 dg418 -> q9 dg419 -> q10 dg420; run dirs .agi/sessions/workflows/runs/mur-director-general-4-N
  HARVESTED awaiting those reviews: DG4.12 589c6dafd · DG4.13 · DG4.14 e51efb790 · DG4.17 7c1da7497 · DG4.18 8097dec13 · DG4.19 10780f70e · DG4.20 0f0e5905cf
SM-1 tip bd01ee8969 DELIVERED 17:56Z (review accept_with_residue, MINORs closed: SM-1b rows + node THOUGHT) -> SM gates it after the stack (heal.py overlap), re-derived on new HEAD
SM-2 tip 802577c1bd DELIVERED 18:2xZ (3 security review passes; SM-2b fsync/no-clobber/shared decision, SM-2c stuck-state fixes; 1541 passed) -- tests +133 vs 60 disclosed
FINDINGS goal:g7.33.19 rows 25 26 27 34 + (to add) a test coupled to live graph lineage (g73319) · a kid commit dying on index.lock stalls its parent silently (DG4.21)
```

## 🔴 Where it stops
With SM: g73319 · g75213 · SM-1 (gating) · SM-2. Building (Sonnet 5.5): DG4.12c (.agi/worktrees/dg4-dg412c: merges SM-2 + residues; lands AFTER SM-2) · DG4.13c (dg4-dg413c) · DG4.14c (dg4-dg414c) · DG4.17c (dg4-dg417c, node prose). Pi murs still running: murq8 dg418 · murq9 dg419 · murq10 dg420. From 21:00Z pi-free only (re-reviews then go through workflow.py merge-up-review --harness pi-free).
Next command: `git -C /data/work/agi/.agi/worktrees/dg4-dg411 log --oneline -3; python3 extensions/agi/bin/send.py read director-general-4`

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
