---
id: goal:g7.16.1.5
mint_id: 298ba4d426264864a7278927bf6e0813
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: director-general-4
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

## Why this exists
goal:g7.16.1 (the council loop): a next-bundle candidate for the council to place, minted by the Prime so the owner's idea is not lost. It depends on goal:g4.18.5 (bundle 4 row W1, "a write is a commit"): once no write leaves a worktree holding state that isn't in a commit, a worktree is disposable. Measured 22:1xZ 09-29 by belam-S2-L5-XVIII: 1022 git worktrees, all on /data (the dm-crypt USB SSD, ~35 ms/op, banked on doc:card-belam §6), ~106 MiB apparent each; RAM 15.6 GiB + 4 GiB swap, ~9.6 GiB available with 7 CC sessions; the tmpfs suite/gate worktree (skill agi-master-gate, 158 MiB) is the one precedent.

## Target end-state
- Round and gate worktrees are checked out on ONE capped tmpfs mount (5-6 GiB, a config cell, never a literal); the object store stays on disk, so a commit is the only durable write.
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
