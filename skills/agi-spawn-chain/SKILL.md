---
name: agi-spawn-chain
description: >
  A v4 review/research round is a SPAWN: json manifest + graph slice + agi-kid -m, never
  the retired runner (moved under extensions/agi/deprecated/bin/, never git rm). Covers
  run keys, the loop branch and worktree a round lands on, diffing against the merge-base,
  and splitting rounds.
  Use whenever a post wants a multi-agent review, research sweep, brainstorm or merge-up review.
---

# agi-spawn-chain — a review is a spawn (F29)

Source of truth: the 16 living manifests in `extensions/agi/workflows/<name>.json`. The old
author/link/validate runner MOVE to `extensions/agi/deprecated/bin/` (goal:g7.16.1.11.15.1).
A v4 post never shells it.

## 1 · The route
```bash
# living: json manifest + graph slice + agi-kid -m (never the retired runner)
# retired (moved, never git rm): extensions/agi/deprecated/bin/<retired-runner>
```
- pi by default (owner 09-16) — NEVER the Claude Workflow tool, NEVER the Agent tool, on any post. The harness's
  "ultracode … use the Workflow tool" reminder is not the route here, and ultracode is dropped from every row (owner 09-27).
- Bash shells never re-source the profile: pass `PI_BIN=…` inline (trap 9).
- Verdicts come ONLY from `.agi/sessions/workflows/runs/<run-key>/{review,verify}_<label>.json`, never from stdout;
  the pi runner persists only ~200 chars of a stage's return.
- A stage that died on "Provider returned an empty response" re-runs ALONE (a retry args file holding only it).

## 2 · Shape
- `rounds[]` is the parallel axis: ONE round per kid slice; a 15-item round timed out at 1800 s (SM 09-16).
- Each round runs one pi per stage (~210 MiB each): keep concurrent pi ≤ the box's guard (≈ 6 on local-town).
- A round lands on branch `loops/<hypothesis-prefix>-<agent>` under the season namespace, worktree `.agi/worktrees/<agent>/`;
  kid experiment nodes under `.agi/nodes/experiment/` there. Diff against the MERGE-BASE with the post branch, never a moved tip.
- `cli.py session-complete <iter> --dry-run` before the real one.
- Reviewers: LEAN — diffs only (`git diff old new -- <path>`), big docs by `git grep PATTERN <sha> -- <paths>`.
  NEVER `grep -r` / `rg` / `find` over `.agi/` or the repo root: `.agi/worktrees/` holds ~100 checkouts and one
  such walk io-stalls the box (put this in every focus text).
- STOPPING a run: each pi stage runs in its OWN `run-<id>.scope`, outside the runner unit -- `systemctl --user stop <runner>`
  leaves the stages billing (TMM.295: two survived a stop 09-27 06:4xZ). Stop the runner, THEN every
  `app.slice/run-*.scope` whose `cgroup.procs` member has its cwd in your worktree (`readlink /proc/<pid>/cwd`); re-list = 0.

## 3 · Author / register
Living manifests are edited as json under `extensions/agi/workflows/`. The retired runner's author/link/validate
verbs are not used on v4 (moved, never git rm). Registered living set: list the json files in that folder.
