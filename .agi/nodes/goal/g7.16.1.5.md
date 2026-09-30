---
id: goal:g7.16.1.5
mint_id: 298ba4d426264864a7278927bf6e0813
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: alive
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
title: "G7.16.1.5: worktrees are disposable cells on one capped RAM disk inside one memory budget (config:guard), and the 1022 old worktrees are archived as refs then pruned"
town: core
---
# goal:g7.16.1.5

## OWNER 2026-09-29 22:0xZ, verbatim (Prime pane)
"How goes the write rework to make it straight commit only? Would that mean we might automatically get RAM disk writes for free if everything is a commit? For the commits I mean spawning worktrees might still need its own ram disk which would be useful since if everything is a commit and we have grid crons and such doing things then it doesn't matter to constantly delete and restart worktrees as needed. And without stream we have more room for an even bigger RAM disk like 5-6gb maybe more."

## OWNER 2026-09-29 22:2xZ, verbatim (Prime pane)
"If the worktrees are merged then prune them. If not idk if we wanna merge them it probably has stale code that got lost in the process since our parent spawns suffered so much lately. Also maybe raise the OOM kill limit from 50% to around 85%. And allow Claude sessions a bit more leeway to hog some memory individually if needed. Idk why the box failed earlier when you first got rebooted. But ideally give the RAM disk about 7GiB if available."
"Also I see having write py commit writes on write.py is tricky but I don't think it's impossible since it loads the old script into memory. Only exception is if it's broken where it can't even apply the fix to itself properly."
"Otherwise yeah everything is a commit so it's even less writing to disk. And we could likely serialize them and create a queue setup that write the commits async when it gets a chance to flush the queue like cron or something."

## Done by the Prime, 22:2xZ 09-29 (inputs for whoever builds this; box paths live off-graph, in the keeper)
- The RAM disk exists: one tmpfs mount, 7 GiB, mode 0700, in fstab with nofail. Nothing uses it yet; its path still needs its config cell.
- Worktree prune (the Prime's prune tool, off-graph): 0 of 1021 worktree HEADs are reachable from any trunk (landings are fresh commits), so "merged" is never provable by ancestry. The prune keeps every byte: a detached HEAD is pinned at refs/archive/worktrees/<name>; an uncommitted state is committed through a temp index onto refs/archive/worktrees/<name>-dirty; ignored files except caches move to the off-graph archive. 7 removed, then PAUSED at io PSI some avg10 = 85 % (ambient load, not the prune). It resumes after PASS B3.

## Why this exists
goal:g7.16.1 (the council loop): the owner's two sections above, minted by the Prime so the idea is not lost. It rests on goal:g7.16.1.6 (a node write is one commit on its own ref): once no write leaves state that is not in a commit, a worktree is disposable. Measured 22:1xZ 09-29 by belam-S2-L5-XVIII: 1022 git worktrees, all on the slow disk (~35 ms/op), ~106 MiB apparent each; RAM 15.6 GiB + 4 GiB swap, ~9.6 GiB available with 7 CC sessions; the tmpfs suite/gate worktree (skill agi-master-gate, 158 MiB) is the one precedent. Read 00:4xZ 09-30 by alive: config:boxkit USER_OOM_PCT is still 50.

## Target end-state
Zoomed out (council lens, vision:alive -- a body that sheds and regrows cells freely because nothing it needs lives in them; the box reports its own memory truth):
```
A  RAM WORKTREES  round + gate worktrees check out on ONE capped tmpfs (7 GiB; its path = a config cell, never a literal);
                  the object store stays on disk, so a commit is the only durable write; a worktree is removed as soon as
                  its tip is committed and harvested, re-added on demand; a reboot loses nothing a commit holds
B  MEMORY BUDGET  ONE home: config:guard, keyed by box class, holds the whole budget -- user OOM % (the owner's ~85 %, set
                  22:4xZ as GUARD_OOMD_LIMIT_<box>), agi.slice %, watchdog %, MemoryHigh, and a Claude session's own
                  high/max (raised for the owner's "leeway", never unbounded); config:boxkit and every applied unit READ it
                  (boxkit's USER_OOM_PCT 50 is a second, disagreeing home today); the tmpfs cap counts INSIDE the budget:
                  a launch holds on memory_alarm WARN/ALARM like every other launch
C  PRUNE          the 1022 existing worktrees pruned by the owner's rule ("If the worktrees are merged then prune them"):
                  since merged is never provable by ancestry, EVERY worktree is archived first, then removed; an archive
                  is a git ref (refs/archive/worktrees/<name>, HEAD pinned, dirty state committed onto <name>-dirty: objects
                  shared, ~0 bytes each), never a tarball; the prune runs gated on io/memory pressure and resumes itself,
                  its liveness a row of the census (goal:g7.16.1.1.6)
```

## Invariants
- A worktree is never removed while it holds an uncommitted change that is not archived (git status --porcelain non-empty = archive first, then remove).
- Nothing under .agi/nodes is written outside a commit (goal:g7.16.1.6 holds first).
- The kill line and P6 are ONE judgement (config post_scope.live, false at 00:4xZ): while every post shares one slice, one oomd kill at the 85 % line takes every post at once -- the owner's option (b) accepts that until P6's go, and P6's go re-reads the guard cell.
- Every self-healing loop this line adds (the prune, the worktree janitor) is a ROW of the one liveness census (goal:g7.16.1.1.6: loop + cadence in a config cell; age > 2x cadence = ONE [red] naming the loop), never a watcher of its own.
- Every memory number lives in ONE config cell (config:boxkit); the box, memory_alarm and every launcher read the same cell.

## Falsifier
1. `findmnt -n -t tmpfs <the worktrees_ram cell>` exits 0 and every live round worktree in `git worktree list` sits under it. (A)
2. Every memory number in config:guard == the property applied on the box, and config:boxkit carries NO memory number of its own (it reads config:guard); a Claude session's own high/max read above their 09-29 values. (B)
3. `git worktree list | wc -l` falls to the live rounds only, and every removed worktree has a refs/archive/worktrees/<name> ref; zero archive tarballs. (C)
4. Negative: zero worktrees removed without an archive ref; zero worktree paths under <repo>/.agi/worktrees created after the cutover. (A · C)

## Out of scope
goal:g7.16.1.6 (the write form this line needs; the owner's "write.py commit writes on write.py" line lives there: the running process holds the old code) · goal:g4.18.5 · goal:g7.16.1.4 · the owner's async commit QUEUE ("serialize them and create a queue ... flush the queue like cron") -- superseded by the owner's later 23:0xZ shape on goal:g7.16.1.6 (a write IS an immediate commit on its own ref, no cron); a queue returns only if a measured write latency demands it.

## Agent Notes
Assigned to **the council** (placement).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council rewrite, alive (writer) with self-perpetuating and all-is-one (00:5xZ 09-30), on the owner task relayed by belam: "I would like the council to go over my verbatim text and make updates to each goal s structure and wording as needed to make sure that the new owner words are reflected in the goal format ... apply their lenses and zoomed out thinking at my words". Both OWNER sections untouched. The goal had DROPPED three owner lines; now: B the memory budget (the owner ~85 % and the Claude-session leeway) and C the prune by the owner rule "If the worktrees are merged then prune them" are targets; the write.py self-commit line moved to goal:g7.16.1.6 A where the write path lives; the async commit QUEUE is out of scope, superseded by the owner later 23:0xZ shape on .6. (alive) the goal misreported its own state: Out of scope said pruning waits on the owner go, but the owner gave it at 22:2xZ; and the Prime inputs carried 13 home-path literals and a hardware detail, now off-graph. (all-is-one) the budget has ONE home, config:guard keyed by box class (GUARD_OOMD_LIMIT already 85, option b); boxkit USER_OOM_PCT 50 was a second disagreeing home, so B names it a reader, never boxkit 50 -> 85. (self-perpetuating) archives are git refs, never tarballs; the kill line and P6 (post_scope.live false) are one judgement; the pruner liveness is a ROW of the one census (goal:g7.16.1.1.6), never a watcher of its own. Near miss: writing boxkit 50 -> 85 would have made a second writer for a number already set.
<!-- THOUGHT:END -->
