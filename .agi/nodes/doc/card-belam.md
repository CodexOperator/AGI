---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-VIII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 8, owner ask 01:3x-01:5xZ (is the grid cron healthy / does it version only what changed / does compression remove waste; then 'Go on both'). (1) Said to the owner: the one irreversible part of gc is deleting unreachable objects older than two weeks. (2) Machine: a bare git gc also expires reflog entries (90/30 days), prunes worktree admin dirs (3 months) and rerere records; the run passed -c gc.reflogExpire=never -c gc.reflogExpireUnreachable=never -c gc.worktreePruneExpire=never (rr-cache empty), in a window with no grid.py alive (minute%5=1): 258 -> 80 MiB, refs/grid 8196 -> 8196, fsck --connectivity-only exit 0. (3) Near miss: a bare git gc satisfies 'run gc' and silently drops reflog history the owner was never told about. (4) No standing rule bent. The hygiene hypothesis sits under goal:g6.49 (the reaper burns the box; g6.49.2 made 'logged every pass' a defect), not goal:g1 (PASS residues). gen 8's wake reasoning (crons, re-link, row check, ultracode not followed): grid.py diff doc:card-belam.
<!-- THOUGHT:END -->

## §0 State (02:1xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-VIII gen 8 · seated 01:1xZ 09-26 · Opus 5.5 · @1 `agi-ec` · meter 0.08 at wake · gen 7 idle (owner chain rule; its crons deleted) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root = `season2/main` in `.agi/worktrees/prime-root` · tz UTC · rebooted 21:45Z + 22:19Z 09-25 · memguard active |
| TOWN | re-seated 22:33-22:37Z 09-25 by gen 7 (grid THOUGHT) · since: TM 22->23 (e5c9d69b10) · DT 31->32 (fc8e0a7c4f, merged the trunk first) · DE gen 20 · SM gen 4 works WITH THE OWNER directly (stream delay) -- never steer SM from here |
| fixes | hot patch 48e16356f0 on the trunk (goal:g6.49: per-boot mem_cap probe, memoized sweep, liveness backstop) · reaper + alarms restarted 22:24Z 09-25 |
| merge | PASS 7 CLOSED 00:06Z 09-26 → season2/main f6afb0c7c7 (pushed) · local-maxxing/main → 08a9cf60f8 · residues f22a49b85d · **PASS 8 NOTICED 00:44Z** (trunk 08a9cf60f8 → 60aa207f5d · 51 commits · 10 exp · 4 engine paths) → run_at 05:47Z · tooling /tmp/belam-pass7 + /tmp/belam-trunk-sync (retarget for PASS 8; rebuild from gen 7's transcript 82d56d5d if /tmp was wiped) |
| owner | 13:5xZ 09-25: the owner's words open doc:unified-head + both director cards · 22:0xZ: the hot patch "light chain" · 00:2xZ 09-26: both directors → opus 5.5 medium |
| directors | director-engine + director-thought rows = **claude-opus-5-5 / medium** (73cbe21cda; re-checked 01:2xZ after the TM + DT rotations: no splice) · a live session switches at its director's rotation · re-check both rows after every rotation (09-24 revert 6d38b9742e) · dispatches FREE (pi-free) · `doc:unified-director-brief` §1 |
| branches | owner 09-25: directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |
| crons | CHECK **bdcf44b4** "13 */4 * * *" (session-only, 7-day; next 04:13Z) · PASS 8 one-shot **5a147c61** "47 5 26 9 *" · re-armed by gen 8 01:1xZ from `.agi/sessions/prime-merge.crons.md` |

## §1 Plan
```
done   gen 7: town re-seated · PASS 7 CLOSED · PASS 8 noticed · swarm trial routed · stale app sessions -> DE · gen 8: crons re-armed · card re-linked · director rows re-checked · grid-cron check + gc (owner)
next   the 04:13Z CHECK · PASS 8 at 05:47Z (f >= 0.40 -> rotate FIRST) · judge DE/DT merge-ups (swarm arms vs their last 5 single-parent rounds) · DE's hygiene round (2d) after 2c
open   guard on local-town (3) · DE: re-seat + anchor hypotheses, the 4 PASS 6 defect hypotheses (defect 3 banked) · DT: lm-* demotes · §6
```

## §2 Landed (this seat)
CHECK bdcf44b4 + PASS 8 one-shot 5a147c61 (session crons) · quorum card re-link + this card (one commit, exact paths) · grid-cron check (owner ask): healthy, versions only on change (grid.py:858-872) · one-off git gc 01:51Z on the owner's go: 258 -> 80 MiB, fsck clean · ede1350c2 hypothesis:cron-layer-keeps-its-disk-footprint-bounded (goal:g6.49) -> DE [decision] · 02:1xZ owner progress check: swarm ORDERS goal-first gate efe8908fb + concurrency-up [decision] to DE (3rd swarm slot; 2c FIRST beside it) and TM (gate DT's swarm-1 merge-up; research <= 1 model kid)

## 🔴 Where it stops
02:1xZ 09-26 belam-S2-L5-VIII: gc done, hygiene + concurrency-up + goal-first ORDERS routed; idle to the 04:13Z CHECK, PASS 8 fires 05:47Z.
```
 0. WAKE (a successor): re-arm the CHECK (crons file section 1); if now < 05:47Z re-arm the PASS 8 one-shot (section 2), else run section 2 under CHECK case (d) unless the state file carries pass_started_at; re-link the quorum card (trap 10).
 1. PASS 8 fires 05:47Z (one-shot 5a147c61). A PASS must not straddle a rotation: at f >= 0.40 rotate FIRST. /tmp tooling dies at reboot: gen 7's transcript 82d56d5d (22:48Z 09-25) holds every file.
 2. DE: [decision] 22:4xZ 09-25 -- (1) hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart (inline prompt, shared-dir card, @id reuse, box-less SM row) then (2) hypothesis:a-reboot-brings-the-town-back-without-a-human (the anchor unit). No reply until the merge-up.
 2b. OWNER swarm trial: hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis (goal:g7.16, 5bbcbe7128; owner verbatim + ORDERS in the node). Build arm = DE, research arm = DT via thought-master; 3 parents/swarm, <= 3 swarms town-wide (DE 1, DT 1, 3rd to the first clean split at MemAvailable >= 3 GiB), <= 2 kids/parent, <= 1 model kid per research swarm. Judge at their merge-ups vs each branch's last 5 single-parent rounds; promote ORDERS to the parent template + 2 config cells only after the verdict. DE's build swarm = DH.364/365/366. DE's brief route d470b0de79 (its branch): once on the trunk, extras.parent = [.agi/context/schemas/[goal].md, .agi/context/schemas/[hypothesis].md] is ONE config edit for every parent. SWARM 1 (02:0xZ): build DH.364/365/366 merged on DE's branch 01:41Z (3/3 + 2/3 kids; DH.366 falsifier-clean), node repairs 295f73ade + fb2e0ca6e; research OSC.35 p1-p3 harvested, p2 OOM x2 (a kid script in its 6G scope: falsifier 4 fired, box min 6.2 GiB), [merge-up] to TM 01:51Z. pi-free 492 turns / 0 errors. Swarm 2 builds from the amended ORDERS (efe8908fb).
 2c. OWNER 01:0xZ 09-26 stale app sessions ([decision] -> DE, NEXT): registry clean; the app keeps uncleanly-dead sessions; no engine path ends an app session. Judge DE's round against "the app lists only live sessions"; watch SM stays alive. Not started by DE at 01:56Z (its swarm merge-up first); the 02:1xZ [decision] puts it FIRST beside the swarm.
 2d. OWNER 01:5xZ 'Go on both': DE [decision] hypothesis:cron-layer-keeps-its-disk-footprint-bounded (ede1350c2, goal:g6.49), queued after 2c. Judge at DE's merge-up on its four conjuncts: maintenance job <= 1.5x a fresh repack · ~/logs capped + rotated from declared cells · a no-op writes <= 1 line per command · the 09-23 07:35Z re-fetch reproduced + guarded.
 3. Guard is NOT on local-town: encryption-town ~/work/.sanctuary/GUARD.md (5 layers): measure docker (llama-server) first, GUARD_DOCKER_BUDGET_belam_gpu, dry-run, then sudo apply (§6 row 1 first).
```
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the logs too when a post says it wrote |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject, re-fences the slot | first slot line = plain text |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py via sync.sh: temp index + ff-only, never a conflicted MAIN |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | re-link after rotation: `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commit both by exact path |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name (journalctl/kernel lines carry it: pipe through `sed "s/$(hostname)/<host>/g"`); one shows → `brb`, then `brb --off` past the delay (`brb back` only prints usage; 02:14Z 09-26) |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 23 | `pgrep -a` / `ps -ef` on the relay prints the stream keys | `pgrep -c` / `-x` only |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 25 | identity can drop mid-seat | `--from belam` on every send.py call |
| 26 | /tmp PASS tooling carries the LAST run's values AND a reboot wipes /tmp | retarget before a run; rebuild from the crons file text |
| 27 | every push prints the remote's moved location (`remote:` lines) | `git push ... 2>&1 \| grep -v '^remote:'` |
| 28 | after a reboot the seat row keeps the dead pid, so heal's crash-recovery tries to seat gen N+1 over a live Prime | re-pin via `rotate._successor_row_write(root, actor=, seat=, role='prime_director', session_ref='', generation=, window=, pid=)`, commit posts.md by exact path |
| 29 | send.py refuses a dm body holding a literal harness tag | write it without the angle brackets |
| 30 | the watcher cannot re-seat after a reboot (grid THOUGHT: inline prompt, shared card, reused @id, box-less SM) | per seat, from MAIN: `heal._watch_one_seat(Path('.agi'), row, windows, rot, launcher=L, pin_table=, seat_sessions=)` with L = write the command to /tmp/agi-recover-<seat>.sh + `heal._launch_recovered(..., cwd=cwd)`; rot = rotate whose spawn_window prompt_file = `<worktree>/.agi/sessions/quorum/<seat>.md`; drop from `windows` only an @id that equals the row's window AND is named for another seat; 30 s + MemAvailable >= 3 GiB between seats |
| 31 | /tmp/belam-trunk-sync/resolve.py enforces the directors' model cells in a posts.md conflict | it writes claude-opus-5-5 / medium (owner 09-26); change it with the owner's next model call |
| 32 | a one-off `geometry_config.load_rows` reads 0 rows without graph_core on sys.path (it swallows the ImportError) | `import rotate` first, then load |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · `brb --status` · `systemctl --user list-units 'agi-*'`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| guard's watchdog reboot on local-town needs tang on gw for LUKS, else the box waits at the passphrase prompt | confirm local-town's unlock path before arming layer 4 |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
