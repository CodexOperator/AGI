---
id: goal:g7.16.1.5.1
mint_id: 869d35611ddb45d480ec8f3cc3e3e4d3
type: goal
parents:
  - goal:g7.16.1.5
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.16.1.5.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: cd908f15c0685a43
season: 2
seeds: []
status: active
tags:
  - goal
  - g7
  - ram-disk
  - guard
title: "G7.16.1.5.1: MAIN's working files live on the RAM disk under MAIN's own path (option B) -- .git, worktrees and .env stay on disk, bound back in"
town: core
---
# goal:g7.16.1.5.1

# goal:g7.16.1.5.1

## Why this exists
goal:g7.16.1.5 (worktrees are disposable cells on one capped RAM disk) is the parent: its line A moves ROUND worktrees onto the tmpfs; the owner then approved moving MAIN itself (option B, below). MEASURED by belam 01:3xZ 09-30: a checkout is 112 MiB (12,470 files); 20 of 27 post rows carry worktree '' (they work in MAIN, on the trunk branch); ~150 processes (14 claude sessions) sit with cwd MAIN; the RAM disk (7 GiB tmpfs, fstab nofail) held 0 bytes; io PSI reached 37-38 while the suite ran back-to-back on /data (sda ~35 ms/op).

## Target end-state
- MAIN's working files live on the RAM disk and MAIN keeps its path byte-identical: the tmpfs tree is bind-mounted over MAIN's path, and `.git`, `.agi/worktrees` and `.env` are bind-mounted back into it from disk. So Claude project keys, worktree gitdirs, `git rev-parse --git-common-dir`/.. and every cron cwd are unchanged, and a commit lands on disk the moment it is made.
- A disk view of MAIN stays mounted beside it; a timer syncs the RAM working files to it, so a reboot loses at most one sync interval of uncommitted edits.
- At boot, one unit rebuilds the RAM tree from the disk view and re-binds it, before cron and user@ start.
- Every path and interval is a cell of config:guard, keyed by box; the script is extensions/agi/guard/ram-main.sh.

## Invariants
- The object store never lives on tmpfs.
- A cutover or revert never drops a byte: the disk view keeps the hidden copy, and revert syncs RAM back before unmounting.
- The tmpfs cap counts inside the memory budget of config:guard.

## Falsifier
1. `findmnt -n /data/work/agi` shows the tmpfs source AND `git -C /data/work/agi status --porcelain | wc -l` equals its value before the cutover.
2. Negative: after the cutover, `git -C /data/work/agi rev-parse --show-toplevel` prints /data/work/agi (never the tmpfs path), and zero post rows changed.

## Out of scope
goal:g7.16.1.5 A (round worktrees on RAM) · B (budget) · C (prune) · goal:g7.16.1.5.2 (session sweep) · goal:g7.16.1.6.

## OWNER 2026-09-30 01:3xZ, verbatim
"Definitely switch that verify over to RAM disk as well as if needed we can also use that path to grab over more files if needed. I also don't see why we couldn't switch most, if not all, posts to the work tree since the write still does commits to disk anyway."
"I'm fine with option B as well. Just find a good stopping point soon and get everyone switched over. The goal can parent the new versions of all relevant build/.geometry/etc nodes. Let's free that pressure. Can we also auto-sweep old sessions into the standard session directory for Claude in /data"

## Agent Notes
Assigned to **belam**.

OWNER 01:4xZ verbatim: "If needed we can somehow let symlink reads/writes cue on the RAM disk via git maybe somehow and get written or read in sequential batches" -- the sync timer is that batch writer for working files (one sequential rsync per interval); batching COMMITS is the async queue in goal:g7.16.1.6 scope.
