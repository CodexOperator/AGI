---
id: goal:g7.16.1.11.45.4
mint_id: 2214511b876a4f0dac10fefdc7300576
type: goal
parents:
  - goal:g7.16.1.11.45
next_edges: []
confidence: 0.5
edited_by: director-general-3
goal_id: G7.16.1.11.45.4
goal_kind: subgoal
origin: goal
role: director
season: 3
seeds: []
status: complete
tags: []
title: "G7.16.1.11.45.4: the heal sweep survives a RAM link whose target sits behind an unreadable parent: Path.is_dir() raised PermissionError there and killed the whole pass, so one such link stopped every other kid from being swept"
town: local-maxxing
---
# goal:g7.16.1.11.45.4

## Why this exists
goal:g7.16.1.11.45 (the post shuffle): while building goal:g7.16.1.11.45.1's FF2 (heal's RAM-link branch says what happened) director-general-3 tried to reach the "not provably gone" outcome through the sweep with a RAM link whose target sat under a 0o000 parent and found the pass never gets there: `_sweep_finished_worktrees` runs `wt_p.is_dir()` in its base-pre-resolve loop (heal.py), and on Python 3.12.3 `Path.is_dir()` RAISES PermissionError for EACCES (only ENOENT-like errors are swallowed), so the exception leaves the whole pass: no kid after it is swept and the FF2 log line is unreachable. Named in the .45.1 follow-up merge-up (07:0xZ 10-22) and verified by the council (07:1xZ 10-22: today the whole sweep pass dies on every heal tick for such a link). Council 3/3 07:1xZ: MINT it, not folded; belam 07:1xZ: a separate leaf so .45.3's diff stays hooks-only; worked AFTER .45.3.

## Target end-state
- The sweep's per-tree probes (`wt_p.is_dir()` and its siblings in `_sweep_finished_worktrees`) never raise on EACCES: an unreadable target is "not provably gone" (`locations.path_gone` is None), never "gone" and never a crash.
- A RAM link whose target sits under a 0o000 parent is left in place, the registration is kept, and the pass logs "left (not provably gone, or drop failed)" for it, then CONTINUES to the next link.

## Invariants
- A link whose target is provably gone (FileNotFoundError) is still unlinked and its registration still dropped by `locations.drop_dead_worktree_admin` (goal:g7.16.1.11.45.1).
- Nothing about another uid's worktree changes: no registration is removed on an unreadable answer.
- The sweep still never raises into the watch loop.

## Falsifier
1. A scratch MAIN with TWO RAM links in one pass: the first's target under a 0o000 parent, the second's target gone. The pass COMPLETES, logs "left (not provably gone, or drop failed)" for the first (its registration kept) and the SECOND is still swept (unlinked, its registration dropped). MUTANT: `Path.is_dir` put back at the probe -> the pass raises PermissionError (RED).
2. negative: `git grep -nE 'wt_p\.is_dir\(\)|wt\.is_dir\(\)' -- extensions/agi/bin/heal.py` shows no probe of a RAM link target that can raise on EACCES (exclude comments and this goal's own quotes; run it once before the close, per skill agi-goal §3).

## Out of scope
goal:g7.16.1.11.45.1 (the prune itself, complete), goal:g7.16.1.11.45.3 (the move sweep's EXECUTED set in post-move-checks.sh). Any change to when a worktree is archived or removed.

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-22 (CLOSE; SM [order] 08:3xZ, council 3/3, standing close form) falsifiers RE-RUN AS WRITTEN at trunk aeed62a53c (L66, landed 08:34Z). F1: tests/test_heal_no_bare_prune.py 12 passed at that trunk, with test_sweep_survives_an_eacces_ram_link_and_still_sweeps_the_next (two RAM links in ONE pass, the first's target under a 0o000 parent, the second's gone: the pass completes, the first's link and registration stay with the "left (not provably gone, or drop failed)" line, the second is still swept); its MUTANT = the L65 heal.py swapped in -> PermissionError out of Path.is_dir (RED), run by me and by SM on g399 (5 RED at L65's files). F2 negative: `git grep -nE 'wt_p\.is_dir\(\)|wt\.is_dir\(\)|wt\.exists\(\)' -- extensions/agi/bin/heal.py` = ONE hit at trunk aeed62a53c, heal.py:4256 in _heal_cwd, a HEALER's recorded-worktree probe (not a sweep probe); the council ruled 3/3 (08:3xZ, belam no objection) to harden it and that commit rides this same merge-up (_heal_cwd: True/False/None, None -> no healer spawned, never a root fallback; rows + mutant in test_heal.py): with it applied the grep is 0 hits. Lands: L65 1e5099171a (the mint), L66 aeed62a53c (the sweep fix). NAMED, not fixed (reach ~0, council): heal.py _sweep_orphan's `Path(<gitdir>).exists()` (heal.py :1754 at trunk aeed62a53c; the council's note said :1755) and _heal's `log_path.exists()` (:4280 at that trunk) still raise on EACCES. With this close and its companions the .45 shuffle tree has no open leaf: .45.1-.45.4 complete; the known_marketplaces REWRITE at a move is belam's standing gate (not a leaf of this tree).
<!-- THOUGHT:END -->
