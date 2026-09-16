---
id: hypothesis:l4-window-names-the-suite-lock-holder-pid-tree-age-command-and-runner-row-in-one-line
mint_id: e7c4ba01a23644709d682fbf20cbe21f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 90ef3c3aecdf1f47
season: 2
testable_claim: "SM.63 (master-sensei [sensei] line 18:28Z, measured on belam 181151Z wake: 17 calls before the first (d), 5 of them hand calls after `verification.py window` on a HELD lock printed only 'lock: held by <pid> since <ts>' (render_window :948) -- cat lock, ps -p, readlink /proc/<pid>/cwd, the ppid chain; sanctuary-master gen 4 paid the same two calls twice at 18:2xZ/18:4xZ to learn WHO held pid 584314 / 767301). CLAIM: (1) `verification.py window` on a live holder prints ONE lock line carrying pid, age (seconds since the lock mtime), the holder's tree resolved from /proc/<pid>/cwd against MAIN and .agi/worktrees/* (spelled as the post or worktree name, MAIN as 'main'), and the command's first 60 bytes from /proc/<pid>/cmdline; (2) when the pid (or an ancestor within 4 ppid hops) is a registered spawn-budget runner the line appends that runner's agent id, tier and iter from spawn_budget's status rows -- read through spawn_budget's existing reader, never a second parse of the budget dir; (3) a dead or unreadable pid, or a missing /proc entry (non-Linux fixture), degrades to today's line plus 'unresolved', never a traceback; (4) `lock: free` is byte-identical to today. FALSIFIERS: a held lock whose line lacks pid, age, tree or command; a runner pid that prints without its agent id; a traceback on a fake pid; any change to the free line. TESTS (<=4, fixture groot + a fake /proc via monkeypatch): live holder in a worktree -> tree = post name, age, cmdline head; holder under MAIN -> 'main'; registered runner -> agent id/tier/iter appended; dead pid -> free (unchanged). FILE SCOPE: verification.py (render_window lock branch + one helper), test_verification.py (or the existing window test module), spawn_budget.py ONLY if its reader must expose rows as data. CEILING: <=35 production lines, ONE kid, re-brief SM past 2x. NOT in scope: the lock grant/take protocol, the suite runner, the after_join wake sequence."
title: L4 window names the suite lock holder pid tree age command and runner row in one line
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-window-names-the-suite-lock-holder-pid-tree-age-command-and-runner-row-in-one-line

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
