---
id: goal:g7.16.1.5.2
mint_id: 2b0ee2bdd9fb4fc8a603a115bc268eaa
type: goal
parents:
  - goal:g7.16.1.5
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.16.1.5.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: f912a6f97dc4caae
season: 2
seeds: []
status: active
tags:
  - goal
  - g7
  - ram-disk
  - guard
title: "G7.16.1.5.2: idle session dirs sweep themselves out of MAIN into their /data homes, a symlink left behind"
town: core
---
# goal:g7.16.1.5.2

# goal:g7.16.1.5.2

## Why this exists
goal:g7.16.1.5 is the parent: MAIN on a 7 GiB tmpfs (goal:g7.16.1.5.1) cannot hold MAIN's 25 GB `.agi/sessions`. MEASURED by belam 01:4xZ 09-30: 380 `iter-*` session dirs; 336 untouched > 24 h; the non-iter rest is 142 MB; zero tracked files under any `iter-*`. Claude's own project dirs already have a /data home (`claude-projects` under the user's /data home, symlinked from `~/.claude/projects`, set up 09-28), but nothing keeps sweeping into it.

## Target end-state
- A timer sweeps every idle `iter-*` session dir (no file written within the idle age, no live process inside it) out of `.agi/sessions` into the agi-sessions archive under the user's /data home, and leaves a symlink, so every reader that globs `.agi/sessions/iter-*` still resolves it.
- The same timer sweeps idle `~/.claude/projects/<dir>` into the standard /data `claude-projects` home, with a symlink back.
- Under tmpfs pressure (use above the cell's percentage) the sweep takes the oldest idle dirs first, at a shorter idle age.
- Ages, paths and the pressure line are config:guard cells; the script is extensions/agi/guard/session-sweep.sh.

## Invariants
- A dir with a file written inside the idle age, or a live process with cwd or an open file in it, is never moved.
- A move never loses a byte: copy, verify, then remove, and the symlink lands in the same step.

## Falsifier
1. After one sweep, `find .agi/sessions -maxdepth 1 -name 'iter-*' -type d | wc -l` counts only dirs written within the idle age, and every `iter-*` symlink resolves.
2. Negative: zero dangling `iter-*` symlinks; zero moved dirs with a write inside the idle age.

## Out of scope
goal:g7.16.1.5.1 · goal:g7.16.1.5 C (worktree prune).

## OWNER 2026-09-30 01:3xZ, verbatim
"Can we also auto-sweep old sessions into the standard session directory for Claude in /data"

## Agent Notes
Assigned to **belam**.

council placement (alive 02:2xZ): the sweep (agi-session-sweep.timer, hourly :37) is a self-healing loop, so it becomes a ROW of the liveness census (goal:g7.16.1.1.6: loop + cadence in a config cell; age > 2x cadence = ONE [red]), like .5.3. File-level pass landed 2c8b824fc; unit fixed 43d7ecb0f (203/EXEC on a 100644 script).
