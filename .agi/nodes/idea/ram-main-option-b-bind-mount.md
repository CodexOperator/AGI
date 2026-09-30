---
id: idea:ram-main-option-b-bind-mount
mint_id: 2069cbd10b3144649c29177638ea96cf
type: idea
parents:
  - goal:g7.16.1.5.1
next_edges: []
edited_by: belam
scaffold_hash: bd1d068e9bd0af5a
season: 2
title: MAIN on the RAM disk by bind mounts under its own path -- not a symlink, which moves the physical path
town: core
---
# idea:ram-main-option-b-bind-mount

# idea:ram-main-option-b-bind-mount

The owner's option B (01:3xZ 09-30) as one mechanism: MAIN's working files move to the RAM disk under MAIN's own path, by a private bind of the disk dir plus an rbind of the tmpfs tree over MAIN, with .git, .agi/worktrees and .env bound back in from disk. Rehearsed by belam at 01:2xZ on a throwaway repo under /data/tmp: getcwd, show-toplevel and git-common-dir unchanged; a commit made in the RAM tree landed in the disk .git; revert gives back the disk tree with the new commit. The near miss: a symlink from MAIN's path to the tmpfs moves the PHYSICAL path, so Claude re-keys its project dirs (-mnt-agi-ram-agi) and git-common-dir/.. names the stale disk copy; F13's .env lookup is one reader of that path.
Session dirs cannot ride along (25 GB against a 7 GiB tmpfs), so idle ones sweep to /data homes first (goal:g7.16.1.5.2).
