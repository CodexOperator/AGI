---
id: goal:g1.39
mint_id: 09f8ba5918e94c739cf9fa96ee9652f4
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G1.39
goal_kind: subgoal
origin: goal
scaffold_hash: 30e8a04910645e69
season: 2
seeds:
  - goal:g1
status: retired
tags:
  - claude-code
  - kid
  - permissions
  - lane
title: "G1.39: a claude-code kid can run a bare `python3 -m pytest <file>` in its own checkout, so a test round on that lane is provable by the kid -- or the lane says by name what a kid cannot run"
town: core
---
# goal:g1.39

## Why this exists
goal:g1 (the engine's own fixes): the pid-fixture round (hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread, 10-02 00:4xZ-00:5xZ) ran on belam's A+ claude-code Sonnet lane as two KIDS and the kid could not prove a single test. Measured from the kids' own logs (SM, 00:5xZ): DG1.07 kid a00-5118dcab: mkdir and cat inside its checkout RAN, cli.py done RAN; `cd /mnt/agi-ram/worktrees/...`, `PYTHONPATH=... timeout 600 python3 -m pytest -p probe4242 ...` and `timeout 600 python3 -m pytest ... | tail -5` were DENIED by the permission layer; DG1.08 kid a00-a11948b7 (told to run a BARE `python3 -m pytest <file> -q` from its cwd): bare pytest, sed and write.py were all denied. Net: a claude-code kid can edit files but cannot run a test, so every test round on that lane is unprovable by its kid; the director had to re-run the proof by hand (green at the tip, red on the base, whole file 139 passed twice). Cause UNMEASURED: no deny rule for pytest in .claude/settings.json or ~/.claude/settings.json and no hook (SM); first suspects are the headless permission check and the kid's cwd being a symlink into /mnt/agi-ram.

## Target end-state
- FIRST a measurement: one probe kid (or a probe run under the same adapter flags) records, for each of `python3 -c pass`, `python3 -m pytest --version`, `python3 -m pytest <one file> -q`, `sed --version`, `git status -s`, `cat`, which the permission layer allows and which it denies, with the exact deny text, from a checkout under /mnt/agi-ram AND from the same checkout reached by a real (non-symlink) path. The answer names the CAUSE (flag, allowlist, cwd resolution, or tool-list entry) with file:line.
- THEN either the kid tool list allows a bare pytest of a named test file from the kid's own cwd (the adapter's allowlist names it), or the lane's brief says by name that a kid cannot run tests and who proves the round (the director, from the kid's tree).
- A kid brief never again tells a kid to run something its tool list denies.

## Invariants
- No test run is allowed outside the kid's own checkout (never a bare-dir pytest: the kid-tier gate stays).
- The privileged tool lists (parent at ladder 3, director at ladder 1) are not widened by this goal.

## Falsifier
1. The probe's result table is committed on the round's experiment node (6 commands x allowed/denied + the deny text + the cause at file:line), and after the fix `python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k two_parents_keep_separate` run by a claude-code kid exits 0 with its output on the node.
2. Negative: `git grep -n 'run a bare' -- <the kid orders template>` shows the instruction only where the allowlist names it (a kid brief that demands a denied command is a defect).

## Out of scope
goal:g1.38 (dispatch refuses a parent that cannot dispatch) · the ladder rows / models (the Prime's) · goal:g1.35 (a parent whose commit failed cannot report done).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
