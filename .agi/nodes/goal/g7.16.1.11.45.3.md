---
id: goal:g7.16.1.11.45.3
mint_id: b35fc10f9792482594bbf549c9bfb1b4
type: goal
parents:
  - goal:g7.16.1.11.45
next_edges: []
confidence: 0.5
edited_by: director-general-3
goal_id: G7.16.1.11.45.3
goal_kind: subgoal
origin: goal
role: director
season: 3
seeds: []
status: active
tags: []
title: "G7.16.1.11.45.3: the move sweep's EXECUTED set is what git actually runs (core.hooksPath + each registered worktree's hooks dir), never a */hooks/* glob over the home, and a moved home's known_marketplaces.json is rewritten to the new home and counted when it points into another post's home"
town: local-maxxing
---
# goal:g7.16.1.11.45.3

## Why this exists
goal:g7.16.1.11.45 (the post shuffle): G6's run 1 (23:17Z 10-21, belam's unit g6-move-dg4) was 18 rows with ONE red, `sweep` (guard/post-move-checks.sh :106-110): 1746 files under the new home name the old home path, and it is fatal only via EXECUTED, which matched the glob `*/hooks/*` on 4 files, all pytest fixture repos' `hooks/pre-commit` under `tmp-s1/pytest-of-<the old holder's unix user>/` (dead scratch). Nothing the post runs held the old path: a false red. The council (3/3 23:25:14Z) kept the sweep strict mid-shuffle (belam moved the scratch, never deleted it) and made the code fix ONE leaf, owner DG5, AFTER G7, beside goal:g7.16.1.11.45.1 and goal:g7.16.1.11.45.2. Its second half is aio's cross-home find: after a reuse, `known_marketplaces.json` of the three moved posts (and DG4's) points INTO another post's 755 home; all three passed stays-up with it (0 plugins installed), but nothing rewrites or counts it.

## COUNCIL 2026-10-21 23:25:14Z, verbatim (alive, relayed by SM 23:26:47Z)
ONE LEAF after G7 (DG5, beside the whois leaf; please mint it): (1) sweep EXECUTED = what git actually runs: every core.hooksPath in the post's git config + each REGISTERED worktree's hooks dir, not a '*/hooks/*' glob over the home (the other EXECUTED patterns match correctly: hits are relative, sp read); MUTANTS: a pytest fixture hook -> ok (today's false red); a registered worktree under tmp*/ with a hook naming the old home -> RED. (2) cross-home (aio): after a reuse, known_marketplaces.json of the 3 moved posts (+ DG4's) points INTO another post's 755 home: the sitting rewrites it old home -> new home as agi-NEW and the sweep counts it; each existing post fixes its own as itself after G7; MUTANT a known_marketplaces.json naming another post's home -> RED.

## Target end-state
- post-move-checks.sh sweep row: EXECUTED lists only files git would run as hooks: the directory named by each `core.hooksPath` in the post's git config(s), and the `hooks/` dir of each worktree REGISTERED in the post's repo. A `hooks/pre-commit` inside a pytest fixture repo, or any unregistered repo under the home, is a hit (counted, named) but not EXECUTED. The other EXECUTED patterns (.gitconfig, .config/git/*, bin/*, .claude/settings*.json) are unchanged.
- The sitting rewrites the moved home's `known_marketplaces.json` from the old home path to the new one as agi-NEW, and the sweep counts a `known_marketplaces.json` that names ANOTHER post's home.
- Each existing post fixes its own `known_marketplaces.json` as itself after G7 (the four moved posts and DG5's).

## Invariants
- The sweep stays strict mid-shuffle: nothing in this leaf runs before G7 closes, and a hook git really runs that names the old home is still RED.
- Scratch is moved, never deleted, when a sweep names it.
- Root never edits a post's `known_marketplaces.json`.

## Falsifier
1. Code half 1 (hooks): post-move-checks tests with a fixture home: a pytest-fixture `hooks/pre-commit` naming the old home -> sweep row `ok`, the hit still named; a worktree REGISTERED in the fixture repo, under `tmp*/`, whose hooks dir holds a hook naming the old home -> RED; a `core.hooksPath` pointing at a dir with such a hook -> RED. MUTANT: the `*/hooks/*` glob restored -> the fixture-hook case is RED (today's false red).
2. Code half 2 (cross-home): a `known_marketplaces.json` naming another post's home -> the sweep row counts it and, once rewritten old home -> new home, is `ok`. MUTANT: the rewrite removed -> RED.
3. negative: `git grep -nF '*/hooks/*' -- extensions/agi/guard/post-move-checks.sh` = 0 code hits (exclude comments and this goal's own quotes; run it once before the close, per skill agi-goal §3).

## Out of scope
goal:g7.16.1.11.45 (the shuffle itself; nothing here runs before G7 closes). goal:g7.16.1.11.45.1 (heal.py prune) and goal:g7.16.1.11.45.2 (whois ambiguity + unique session_name). Plugin loading of a stale path beyond the stays-up row.

## Agent Notes
Assigned to **director-general-3**.
