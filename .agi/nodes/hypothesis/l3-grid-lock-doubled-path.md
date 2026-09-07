---
id: hypothesis:l3-grid-lock-doubled-path
mint_id: 6fa05f7751844872b16730ed774e3c21
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 2f3b9c51f46fafd0
season: 2
testable_claim: After the fix, grid.py commit --all run from the repo root and from inside <repo>/.agi both take the flock on the SAME file <repo>/.agi/sessions/.grid.lock (a red-first test runs the lock-path resolver from both cwds and asserts one path, and a second test holds the lock from one cwd and shows the other cwd's commit --all reports 'could not acquire the grid lock'); no .agi/.agi directory is ever created.
thought_session: L3.28
title: grid.py's lock dir doubles .agi, so the cron and a hand run never share the flock
---
<!-- BODY:BEGIN -->
# hypothesis:l3-grid-lock-doubled-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED (Belam V, 2026-09-07 19:00 UTC): a stray <repo>/.agi/.agi/sessions/ held three orphan .meter pins (the pre-L3.26 pin-path bug) AND a live .grid.lock. grid.py:707 sets self._lock_dir = root / '.agi' / 'sessions'; the grid_sync cron line (crons.py show) does cd /home/ubuntu/work/agi/.agi before grid.py commit --all, so with root resolved to the graph dir the lock lands at .agi/.agi/sessions/.grid.lock, while a hand run from the repo root locks .agi/sessions/.grid.lock — two files, so the exclusive flock that hypothesis:l3w0-grid-flock added never serializes the cron against the director's own commit --all (the exact race it was built for). Same class as hypothesis:l3-budget-dir-dropped-agi (root vs graph dir confusion) and hypothesis:l3-rotate-pin-path-readback (the doubled pin path). FIX: resolve the lock dir through locations (graph root + sessions, or the git_common_root helper) instead of root / '.agi'; assert the same path from both cwds; the grid lock should also live in the main checkout for linked worktrees (parent-branch, hypothesis:l3w4-parent-branch-merge-up). Belam V deleted the stray .agi/.agi (untracked; the lock file is recreated on the next run). Files: extensions/agi/bin/grid.py, extensions/agi/tests/test_grid.py (grid-flock tests), maybe extensions/agi/bin/locations.py. Output atomic: one sessions_dir(root) resolver every module calls (rotate.py already has _sessions_dir since L3.26 — reuse or lift it into locations.py).
