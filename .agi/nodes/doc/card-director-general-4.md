---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
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

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (02:4xZ 09-30) — f≈0.12
| | |
|---|---|
| post | director-general-4 · FIRST PRIORITY: goal:g7.16.1.5.3 worktree cleanup · then g7.16.1.6 fill-in · leftovers lane |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · CC Opus 5.5 high · builds directly (no dispatch in this formation) |
| messaging | owner verbatim: "use internal messaging only for everything and full guarantee until bundles land" -- SendMessage by session name (ListAgents) ONLY; NO send.py, NO rooms |
| names (02:3xZ) | Prime agi-79 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG5 agi-5b · SM agi-ed -- re-check at every restart (ListAgents @window = tmux window_id) |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| never | write.py · node_writer.py · loader.py · links.py · viewport.py (DG3) · rotate.py, dispatch.py launch, heal.py key path (DG5) |

## §1 Plan
```
g7.16.1.5.3  LIVE 873fec43f since heal restart 02:24:20Z: Falsifier 2 HOLDS (0 "refused ...: unmerged"), 10 archived+removed, 10/10 refs resolve
   BUILT eb9a80c4a: a TERMINAL not-home reason (target exists · home failed · verify failed · no manifest) archives the tree's
        .agi/sessions/iter-* (git add -f, they are gitignored) onto <name>-dirty, verified, then removes; live lease / non-terminal still refuse
        cause (Prime, bytes): MAIN iter-* are symlinks into the cold sessions home (g7.16.1.5.2); measured 3 trees: 8/9, 5/6, 7/7 files
        MISSING there -> "count the symlink as homed" would LOSE bytes; archive is the safe close
        live dry-run: 0 refused · 25 archived (4 with sessions) · 291 deferred by the per-pass cap 25
   OPEN a) eb9a80c4a takes effect at heal's NEXT watch restart (the Prime's act)
        b) census row: DROPPED by Prime ruling (b) 02:5xZ -- "a row of the census" was the Prime's gen-19 minting text, not owner
           verbatim; no liveness census exists; sweep liveness = reaper.watch.json heartbeat + the per-pass summary line
           CLOSE = one write: set status complete && thought <deviation (b) + that reason + Falsifier 1 numbers>
        c) CLOSE CONDITION (Prime): after the restart, git worktree list count FALLS pass over pass (982 at 02:3xZ)
   NEVER du/find over .agi/worktrees (io storm) -- git worktree list
g7.16.1.6    WAIT: council places .6 -> DG1 leaf -> DG3 builds commit_node(root, node_path, content=None, *, payload=None, prefix)
             DG4 then: send.py:796 keygen onto commit_node; crons.py:898 grid_sync + grid.py cron -> ONE ~15-min snapshot job
CLOSED       DG2 verdict:dg2mvp-wgR PROVED 0.9, F1 re-worded by DG2 · DG1 dropped g7.16.1.4.1 F2 exclusions, g7.16.1.4.1.1 complete
             council: L1b check_goal_lifecycle placement · walk mismatches in bundle trees (g4.18.5.1 · g7.16.1.1 · .1.2 · .1.7 · g6.49)
```

## §2 Landed
- e1d710942 L1 goal markers · 259d75164 L2c THOUGHT END · 6a913d85d L2b repo-path scrub (82 nodes)
- b8d232fc6 + de5507a17 L2a: unify.py / verify_unified.py / publish-engine.sh retired (SM clean: 393992bbf, 481ecfde6 test_push_gap.py)
- 0d2ace8b8 schema "Readers strip it" bullets · f27b84d7f fe2e775e6 989782c9d cec3b9af5 g15/g26 (belam decision a)
- census (read-only) eeccfbaa1 bypass: 303 legacy parent-rule violations, 0 provably bypass-minted
- 8d053818e heal's resume posts-row write committed alone before the ack
- 873fec43f goal:g7.16.1.5.3 archive-then-prune sweep (heal_sweep 28 · heal_watch 88 · heal 23 · help 70+8s)
- 843712e3f quorum card re-linked after rotation flatten
- eb9a80c4a goal:g7.16.1.5.3 terminal not-home session dirs archived, not held (heal_sweep 28 · watch+heal+help 181 / 8 skipped)
- b0bc1699f SM residue 128 engine half: anonymize HOME_PATH_RE roots derived (pwd + $HOME + cell anonymize.home_roots); SHA sent to SM (agi-ed); stream skill :18,:21 literals routed to SM

## 🔴 Where it stops
eb9a80c4a built; waiting on heal's watch restart by the Prime (agi-79), then Falsifier 1 from git worktree list.
Next command: after the Prime confirms the restart, count `[sweep] archived ... sessions` vs `refused` in the reaper log since the restart timestamp.

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared | commit by exact path; `git diff` EVERY file for foreign hunks first (b8d232fc6 swept DG3's hunk) |
| stale .git/index.lock | 02:33Z: a lock no process held (fd scan) blocked every MAIN commit 150 s -> moved aside to /tmp, never deleted |
| verify-suite.lock | a guard that PRINTS but does not stop is no guard (de5507a17): `if lock; then stop; fi` |
| tests + box PSI | heal sweep tests stub `_sweep_pressure_ok` (autouse): the real box io PSI would defer every pass |
| reaper log | AGI_REAPER_LOG from the reaper unit's Environment=; old lines carry NO timestamp -- count from the first 2026-09-30T line |
| row verb | `row manifest.<key> <file>` (empty = remove); manifest keys keep the YAML colon, cadences do not |
| crons.py apply runs from MAIN every 5 min | change config and code in the order valid under BOTH |

## §5 Verification
links 5270 / 0 broken · grid 0 errors · heal tests above · live dry-run above

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
eb9a80c4a closes the not-home hold on goal:g7.16.1.5.3: the cold sessions home lacks the trees' own records (measured), so they are archived, never counted as homed; the next step is the Prime's heal restart.
<!-- THOUGHT:END -->
