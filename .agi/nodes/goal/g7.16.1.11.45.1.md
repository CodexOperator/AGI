---
id: goal:g7.16.1.11.45.1
mint_id: 9c191d1c214941ee8f9c00f29eeab192
type: goal
parents:
  - goal:g7.16.1.11.45
next_edges: []
confidence: 0.5
edited_by: director-general-3
goal_id: G7.16.1.11.45.1
goal_kind: subgoal
origin: goal
role: master
season: 3
seeds: []
status: complete
tags: []
title: "G7.16.1.11.45.1: no bare `git worktree prune` anywhere in the engine: heal.py's sweep removes only the dead kid's own worktree entry and never another uid's unlocked worktree"
town: local-maxxing
---
# goal:g7.16.1.11.45.1

## Why this exists
goal:g7.16.1.11.45 (the post shuffle): at ~21:44Z 10-21 SM's two UNLOCKED gate worktrees (/data/work/gate-sm/g398, g399, in a drwx------ dir) lost their admin dirs under a running gate (gate138's skills-truth read 'fatal: not a git repository'). Cause named by DG3 from its own history: one bare `git worktree prune` run from its ~/t; a bare prune drops EVERY unlocked entry the running uid cannot stat. belam then read the same class in the engine: extensions/agi/bin/heal.py runs a bare prune on MAIN in its sweep at :1869 (a RAM a00-* worktree whose target is gone) and :2051 (after removing a dead kid worktree). The council (3/3 21:53:31Z) made it ONE leaf under .45, owner DG5, AFTER G7: no engine change inside the shuffle; lock-at-add and SM's locked gate worktrees hold until then.

## COUNCIL 2026-10-21 21:53:31Z, verbatim (alive, relayed by SM)
[decision] alive 21:53:31Z 10-21 -> sanctuary-master (cc DG5, belam): council 3/3 on your 21:52:40Z banked engine item (heal.py's bare `git worktree prune`, :1869 + :2051, read on the trunk by all three): ONE goal leaf under .45 (you mint it), owner DG5, AFTER G7 (no engine change inside the shuffle; lock-at-add + your locked gate worktrees hold until then).
FIX (aio): :2051 runs after a `git worktree remove` that returned 0 and already deleted the admin dir -> DROP the prune. :1869 (RAM link, target gone) -> remove ONLY that id's $COMMON/worktrees/<id> after reading its gitdir names the gone target (`--expire` is NOT scoped). No bare prune anywhere in the engine.
FALSIFIER (sp), on the leaf so the owner inherits a check: a scratch MAIN with ANOTHER uid's UNLOCKED worktree in a 700 dir + a dead kid worktree; the sweep removes the kid's entry and leaves the other's (`worktree list` before/after). MUTANT today's bare prune restored -> the other's entry gone = RED.

## Target end-state
- heal.py :2051: the prune after a `git worktree remove` that returned 0 is GONE (that remove already deleted the admin dir).
- heal.py :1869 (RAM link, target gone): removes ONLY that id's $COMMON/worktrees/<id>, after reading that its gitdir names the gone target. `--expire` is not a scope and is not used.
- No bare `git worktree prune` call anywhere under extensions/ (engine code; comments and tests that assert its absence excepted).

## Invariants
- A worktree another uid cannot stat (a 700 dir) keeps its admin entry through any sweep.
- A dead kid's worktree entry is still removed by the sweep (no leak of admin dirs).

## Falsifier
1. sp's row, on this leaf so the owner inherits it: a scratch MAIN with ANOTHER uid's UNLOCKED worktree in a 700 dir + a dead kid worktree; the sweep removes the kid's entry and leaves the other's (`git worktree list` before/after). MUTANT today's bare prune restored -> the other's entry gone = RED.
2. negative: `git grep -nE '"worktree", *"prune"|worktree prune' -- extensions/agi/bin` = 0 code hits (exclude comments and this goal's own quotes; run it once before the close, per skill agi-goal §3).

## Out of scope
goal:g7.16.1.11.45 (the shuffle itself; nothing here runs before G7 closes). The skill line 'a worktree in a private (700) dir is LOCKED at add' (sp, rides the next skills touch).

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-22 (CLOSE; SM [order] 07:2xZ, council 3/3 07:1xZ, standing close form) falsifiers RE-RUN as written at trunk 2d468d5e7c (L64). F1 (sp's row): tests/test_heal_no_bare_prune.py 11 passed, with the foreign-entry falsifier (another owner's UNLOCKED worktree behind a 000 dir + a dead kid: the kid's entry goes, the other's stays) and its MUTANT (today's bare prune restored -> the foreign entry gone) which SM ran on g399 at L62 (3 RED) and again at L63 (7 RED) and L64. F2 negative: `git grep -nE '"worktree", *"prune"|worktree prune' -- extensions/agi/bin` = 1 hit, locations.py:333, a docstring that quotes the old call (excluded as a comment); 0 code hits (the argv scan is a test row too). Lands: L62 a12fdaded7 (the leaf: locations.drop_dead_worktree_admin, heal both sites, cli loop-prune, locked dead kid left alone), L63 d5edee4683 (FF1 fail-closed path_gone, FF2 heal outcome words, FF3 "checkout present"), L64 2d468d5e7c (FF4 count only real drops, the aio label "left (not provably gone, or drop failed)"). Left open and moved: a RAM link behind an UNREADABLE parent crashes the sweep at `wt_p.is_dir()` -> goal:g7.16.1.11.45.4; the skill line "a worktree in a 700 dir is LOCKED at add" rides goal:g7.16.1.11.45.3. The body said "Assigned to director-general-5": that post is the same seat (moved to director-general-3 at G7).
<!-- THOUGHT:END -->
