---
id: hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram
mint_id: c2eaa2329cf0431ba9da874d79bf95cf
type: hypothesis
parents:
  - goal:g7.31.3.3
next_edges: []
edited_by: belam
scaffold_hash: 99f721ebee0a9eb8
season: 2
testable_claim: prune clean non-live kid worktrees; spawn reads paths.<town>.worktrees_root via locations.py (no literal at dispatch.py:754); guard.env GUARD_WORKTREE_TMPFS_<host>=4G mounted and charged to user@; post worktrees stay on disk; worktree prune on reboot
title: "Kid worktrees resolve from ONE config cell (paths.<town>.worktrees_root) and can live on a guard-owned 4G RAM disk; stale ones pruned first (assigned: director-engine)"
town: core
---
# hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram

# hypothesis: kid worktrees resolve from ONE config cell and can live on a guard-owned RAM disk (assigned: director-engine)

## Why this exists
**Parent `goal:g7.31.3.3`** (the spawn/rotate redesign): spawn is where a worktree is created. OWNER 2026-09-27 02:5xZ-03:1xZ to the Prime, verbatim: "if needed we could reduce pi latent count and reserve some ram for worktrees so we can batch the reads and writes for spawns and murs to and from ram. Dedicate a good couple gigs to it or maybe 4, what do you think?" · "Okay that sounds good as set up. Which config value are we editing later we will have to maintain it properly for all posts as part of the mint and send and rotate redesign goals."

## Measured (belam-S2-L5-XII, 03:0xZ 09-27)
- 210 worktrees; 190 kid checkouts at ~140 MB each (~27 GB on disk); `.git/objects` 145 MB.
- IO is READ-bound: Dirty 0.6 MB vs Cached 5 GB; io PSI some avg60 40-70 during PASS 10; every reviewer walk into `.agi/worktrees/` re-reads the 27 GB.
- The kid worktree root is a literal: `dispatch.py:754` `main / ".agi" / "worktrees" / agent_id`. `paths.local_maxxing` carries per-kid literals (`worktree_a00_2f819956`, `nodes_experiment_dir: .agi/worktrees/a00-d511add6/...`) because no root cell exists.
- Guard since 02:5xZ 09-27: docker budget 0, user@1000 high/max 12618/14021M, sshd reserve 1911M unchanged.

## Testable claim
1. PRUNE FIRST: every kid worktree that is clean AND not live (`spawn_budget.py status`) is removed with `git worktree remove` (its branch keeps every commit); post worktrees are never touched.
2. ONE CELL: `paths.<town>.worktrees_root` (default `.agi/worktrees`), resolved by `locations.py` and read by spawn (`dispatch.py:754`) -- no worktree path literal left in engine code; the per-kid `paths.local_maxxing.worktree_*` keys retire.
3. RAM LANE: `GUARD_WORKTREE_TMPFS_<host>` (4G) in guard.env; guard-init mounts it and subtracts it from user@'s budget like the docker budget; kid + loop (mur) worktrees point there; post worktrees stay on disk (cards and uncommitted edits must survive a power cut).
4. REBOOT: spawn/rotate/reap run `git worktree prune` when the RAM disk comes back empty.
5. EVICTION, BOTH LAYERS (owner 03:1xZ 09-27: 'update the reaper to also delete the worktrees automatically, or set up the RAM disk guard to do it for us for oldest inactive worktrees first for example? Or maybe both.'): the REAPER (agi-agi-reaper, git-aware) owns removal with the Prime's 03:1xZ predicate -- not live · idle >= reaper.worktree_idle_h · clean (no modified/untracked) · HEAD reachable from a branch · not referenced by config -- oldest-inactive first, `git worktree remove` never --force, bounded by reaper.worktree_keep_max; the RAM-DISK GUARD never runs git: at a high-water fill (80 pct) it triggers the reaper's eviction pass, at a hard-water (95 pct) spawn refuses a new worktree by name instead of deleting one. Reference implementation of the predicate: the Prime's one-shot prune of 03:2xZ 09-27 (commit message names the counts).

## Falsifier
1. `git grep -n '"worktrees"' -- extensions/agi/bin/*.py` = 0 path literals outside locations.py.
2. After the prune, `git worktree list | wc -l` <= live kids + posts + 5, and io PSI some avg60 during a PASS-sized load < 25.
3. A kid dispatched with `worktrees_root` = the tmpfs mount lands there, commits to its branch, and survives a `git worktree prune`.

## Agent Notes
2026-09-27 03:3xZ belam-S2-L5-XII ONE-SHOT PRUNE (owner 03:1xZ: 'Let's trim the worktrees yourself'), the conjunct-5 predicate by hand: 201 kid worktrees -> 52 removed (git worktree remove, never --force, 0 refused), /data avail 161827M -> 170620M (~8.8 GB), git worktree list 210 at 03:0xZ -> 170 at 03:3xZ (52 removed; ~12 spawned meanwhile). KEPT: 92 DIRTY (uncommitted/untracked kid NODE files: experiment, hypothesis, goal, build, 2x .agi/config.json) · 47 recent (< 6 h) · 9 live · 1 cwd-in-use; 15 de-base-* (DE's) + posts + prime-root untouched. FINDING for this round: the 92 dirty ones are UNHARVESTED kid output -- the reaper must harvest-or-deprecate uncommitted kid nodes (write.py adopt + commit, or a retire) BEFORE it may reclaim such a worktree; never --force. Decision log: /tmp/belam-pass10/wt-decisions.log (box-local).
