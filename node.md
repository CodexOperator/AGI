---
id: goal:g7.16.1.5
mint_id: 298ba4d426264864a7278927bf6e0813
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.5
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: e196cfe8ce12c83b
season: 2
seeds: []
status: horizon
tags:
  - ram-disk
  - worktrees
  - council-loop
title: "G7.16.1.5: round worktrees live on one capped RAM disk once every write is a commit"
town: core
---
# goal:g7.16.1.5

## OWNER 2026-09-29 22:0xZ, verbatim (Prime pane)
"How goes the write rework to make it straight commit only? Would that mean we might automatically get RAM disk writes for free if everything is a commit? For the commits I mean spawning worktrees might still need its own ram disk which would be useful since if everything is a commit and we have grid crons and such doing things then it doesn't matter to constantly delete and restart worktrees as needed. And without stream we have more room for an even bigger RAM disk like 5-6gb maybe more."

## OWNER 2026-09-29 22:2xZ, verbatim (Prime pane)
"If the worktrees are merged then prune them. If not idk if we wanna merge them it probably has stale code that got lost in the process since our parent spawns suffered so much lately. Also maybe raise the OOM kill limit from 50% to around 85%. And allow Claude sessions a bit more leeway to hog some memory individually if needed. Idk why the box failed earlier when you first got rebooted. But ideally give the RAM disk about 7GiB if available."
"Also I see having write py commit writes on write.py is tricky but I don't think it's impossible since it loads the old script into memory. Only exception is if it's broken where it can't even apply the fix to itself properly."
"Otherwise yeah everything is a commit so it's even less writing to disk. And we could likely serialize them and create a queue setup that write the commits async when it gets a chance to flush the queue like cron or something."

## Done by the Prime, 22:2xZ 09-29 (inputs for whoever builds this)
- The RAM disk exists: tmpfs `/mnt/agi-ram`, size 7 GiB, mode 0700, in /etc/fstab with nofail. Nothing uses it yet. Its path still needs its config cell.
- Worktree prune (tooling at <home>/wt-prune/prune.py): 0 of 1021 worktree HEADs are reachable from any trunk (landings are fresh commits), so "merged" is never provable by ancestry. The prune keeps every byte: a detached HEAD is pinned at refs/archive/worktrees/<name>; an uncommitted state is committed through a temp index onto refs/archive/worktrees/<name>-dirty; ignored files except caches are renamed to <home>/wt-archive/<name>/. 7 removed, then PAUSED at io PSI some avg10 = 85 % (ambient load, not the prune). It resumes after PASS B3.
## Why this exists
goal:g7.16.1 (the council loop): a next-bundle candidate for the council to place, minted by the Prime so the owner's idea is not lost. It depends on goal:g4.18.5 (bundle 4 row W1, "a write is a commit"): once no write leaves a worktree holding state that isn't in a commit, a worktree is disposable. Measured 22:1xZ 09-29 by belam-S2-L5-XVIII: 1022 git worktrees, all on /data (the dm-crypt USB SSD, ~35 ms/op, banked on doc:card-belam §6), ~106 MiB apparent each; RAM 15.6 GiB + 4 GiB swap, ~9.6 GiB available with 7 CC sessions; the tmpfs suite/gate worktree (skill agi-master-gate, 158 MiB) is the one precedent.

## Target end-state
- Round and gate worktrees are checked out on ONE capped tmpfs mount (7 GiB at /mnt/agi-ram, reached through a config cell, never a literal); the object store stays on disk, so a commit is the only durable write.
- A worktree is removed as soon as its branch tip is committed and harvested, and re-added on demand; a reboot loses nothing a commit holds.
- The cap is part of the box memory budget: a launch holds on memory_alarm WARN/ALARM like every other launch.

## Invariants
- A worktree is never removed while it holds an uncommitted change (git status --porcelain non-empty = keep).
- Nothing under .agi/nodes is ever written outside a commit (goal:g4.18.5 holds first).

## Falsifier
1. `findmnt -n -t tmpfs <paths.<town>.worktrees_ram>` exits 0 and every live round worktree in `git worktree list` sits under it.
2. Negative: zero worktrees removed with a non-empty `git status --porcelain` (the janitor's log), and zero worktree paths under <repo>/.agi/worktrees created after the cutover.

## Out of scope
goal:g4.18.5 · goal:g7.16.1.4 · pruning the 1022 existing worktrees (an irreversible pass: the owner's go).

## Agent Notes
Assigned to **the council** (placement).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
