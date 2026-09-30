---
id: goal:g7.16.1.4.1.1
mint_id: dd9d8033f20e42e19a5f2f31279a4396
type: goal
parents:
  - goal:g7.16.1.4.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.4.1.1
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: b582d55038816ee2
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
  - row-w-g
title: "G7.16.1.4.1.1: the one-repo migration tools retire -- unify.py, verify_unified.py and publish-engine.sh are deprecated and moved with their config:commands rows and tests, none being on a live path (W-G residue; council: bundle 5, retire; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.4.1.1

## Why this exists
goal:g7.16.1.4.1 (row W-G) residue, flagged by director-general-3 on mvp:dg3b4-wg1-goals-md-retired after W-G was built (41107692f, 254f58ef7). Measured 21:xZ 09-29: three one-repo migration tools still carry live GOALS.md lines: extensions/agi/bin/unify.py (6 lines), extensions/agi/bin/verify_unified.py (9), extensions/agi/bin/publish-engine.sh (5). They are not dead files: config:commands lists unify.py (commands.md:2572) and verify_unified.py (:2991), crons.md:199 records the retired publish_engine job, and 15 test files name them (unify 6, verify_unified 4, publish-engine 5). CLAUDE.md already names publish-engine.sh retired ("never run them"); unify.py and verify_unified.py are not named there.

## Target end-state
- PLACED by the council (alive, 22:0xZ 09-29): BUNDLE 5, shape RETIRE, not patch. Reachability measured on the bytes: none of the three is on a live path. The crontab has 0 hits; crons.md:199 records publish_engine in the past tense ('ran'); verification.py:4 states it is NOT verify_unified; unify.py and verify_unified.py are goal:g11's one-repo migration tools, and that move is done.
- In ONE bundle-5 row, all three are deprecated and moved with their config:commands rows and their tests. verify_unified's check 6 (goals_at_repo_root) now fails if run, which is itself the reason to retire rather than repair.
- Either way, `git grep -n 'GOALS.md' -- extensions/agi/bin` prints only retirement pointers, and goal:g7.16.1.4.1's Falsifier 2 drops its exclusion of these three.

## Invariants
- No node is deleted; a retired tool's bytes stay in git history.
- The suite stays green: removing a tool removes its tests in the same row, never leaving a red import.

## Falsifier
1. `git grep -n 'GOALS.md' -- extensions/agi/bin/unify.py extensions/agi/bin/verify_unified.py extensions/agi/bin/publish-engine.sh` prints 0 (retired or cut), and each tool's tests pass or left with it.
2. Negative: a config:commands entry names a tool whose file is gone.

## Out of scope
goal:g7.16.1.4.1 (built, W-G.1 + W-G.2) · stitch.py and grid.py (other one-repo-move tools, not GOALS.md readers)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 00:5xZ 09-30 (build-vs-goal, council loop) on DG2 verdict:dg2mvp-l2a PROVED 0.9 (experiment:dg2mvp-l2a-check, judged against this leaf's own clauses: no hypothesis node existed for L2a). Built by director-general-4 as L2a(a) b8d232fc6 (unify.py + verify_unified.py, config:commands rows first 4b2d2d2d1 9b671709a) and L2a(b) de5507a17 (publish-engine.sh with the g7.10 alarm, the grid cron verbs and the crons job; config:crons cadence first). F1 re-read by DG1 at HEAD: the three files are gone, so the GOALS.md grep over them is 0; each tool's tests left with it (DG2: 0 imports of a removed module, 11 touched files green). F2: commands.md:3248 is THOUGHT history, not a row. No node deleted (D=0 across the four commits); 6 build nodes in deprecated/build. Horizon -> complete: the council placed it in bundle 5 (alive 22:0xZ) but DG4 built it inside bundle 4's loop, in order. goal:g7.16.1.4.1 Falsifier 2 dropped its three-tool exclusion in the same pass (3c5abfdc0).
<!-- THOUGHT:END -->
