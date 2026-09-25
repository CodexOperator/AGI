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
thought_session: belam-S2-L5-VII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 7 re-seated the town BY HAND through heal's own recovery path with three seams changed (deviation). (1) The card said: "RE-SEAT: thought-master -> director-engine -> director-thought -> stream-master ... heal._watch_one_seat per seat with a /tmp/agi-recover-<seat>.sh launcher". (2) What the machine does: the watcher (heal.py watch, reaper unit) named TM/DE/DT DEAD every 30 s and failed every respawn with tmux "command too long" (agi-crons log; _launch_recovered heal.py:2575 hands tmux the whole prompt inline); stream-master's row has no box, so the watcher skips it as foreign; _recover_seat (heal.py:2770) takes a worktree seat's card from the SHARED MAIN sessions dir, whose DE/DT copies are stale (gen-18 state; 5 AUTO-CAPTURED lines) while their worktree cards carry the owner's words; _window_present matches the @id alone, so after the tmux server restart DT's pre-reboot @3 matched DE's NEW @3 and DT read ALIVE ("nothing done", built and run). (3) Near miss: gen 5's recipe verbatim (cwd-less launcher -> heal's TypeError fallback -> MAIN) satisfies "re-seat via heal" and wakes DE/DT in MAIN on stale cards, then stops at DT. (4) Why the standing path does not apply: the standing path IS the watcher and it cannot land a spawn on this box; only the launcher, the worktree card and a provably-foreign @id collision were changed — row write to MAIN, respawned record and dms are heal's own. Script: scratchpad reseat.py (dies with /tmp; recipe in trap 30).
<!-- THOUGHT:END -->

## §0 State (22:4xZ 09-25)
| | |
|---|---|
| post | belam-S2-L5-VII gen 7 · seated 22:29Z · Opus 5.5 · @1 pid 69212 `agi-ec` · meter ~0.12 · gen 6 idle in @0 (owner chain rule; its CHECK deleted 22:30Z) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root = `season2/main` in `.agi/worktrees/prime-root` · tz UTC · rebooted 21:45Z + 22:19Z (sleep targets masked by the peer) · memguard active · MemAvailable 11.4 GiB after four spawns |
| TOWN | RE-SEATED 22:33-22:37Z by the Prime (THOUGHT): TM gen 22 @2 (ACKED) · DE gen 20 @3 · DT gen 31 @4 (both in their worktrees, on their worktree cards) · SM gen 4 @5 (restarts the stream relay) · DE/DT/SM rows keep the dead pid until each acks |
| fixes | hot patch 48e16356f0 on the trunk (goal:g6.49: per-boot mem_cap probe, memoized sweep, liveness backstop) · reaper + alarms restarted 22:24Z |
| merge | PASS 6 CLOSED 10:49Z → season2/main 63c89d0068 · PASS 7 noticed 12:44Z, run_at 17:43Z, HELD by gen 6 (town down): pass_started_at null → runs under CHECK case (d) once the acks land and memory holds with the stream up |
| owner | 13:5xZ: the owner's words open doc:unified-head + both director cards · directors stay Sonnet · 22:0xZ: the hot patch "light chain" |
| directors | director-engine + director-thought, claude-sonnet-5 max · dispatches FREE (ladder.md:42-43 pi-free) · `doc:unified-director-brief` §1 |
| branches | owner 09-25: directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |
| crons | CHECK d88c4dcb "13 */4 * * *" re-armed 22:3xZ (session-only, 7-day) · no PASS one-shot (PASS 7 runs under case d) |

## §1 Plan
```
done   town re-seated (TM DE DT SM) · CHECK re-armed · card re-linked
next   acks (DE DT SM) -> posts.md commit -> the re-seat defects + durability -> director-engine -> PASS 7
open   guard on local-town (3) · DE: the 4 PASS 6 defect hypotheses (defect 3 banked) · DT: lm-* demotes · §6
```

## §2 Landed (this seat)
town re-seat (rows by heal: TM 22 · DE 20 · DT 31 · SM 4) · CHECK d88c4dcb · this card + quorum re-link

## 🔴 Where it stops
```
22:4xZ 09-25 belam-S2-L5-VII: the town is re-seated; DE/DT/SM acks pending, then the defect assignment, then PASS 7.
 1. ACKS: TM acked; DE/DT/SM rows carry the new window + the dead pid until each acks. posts.md is dirty from the recovery row writes: commit it by exact path once the acks land (never with another post's edit).
 2. DEFECTS -> director-engine ([decision], one hypothesis each): (a) _launch_recovered inline prompt = "command too long" (open since gen 5's 06:44Z dm) (b) _recover_seat card from the shared dir, not the seat's tree (c) _window_present @id-only reads a reused id alive after a tmux restart (d) stream-master row lacks box -> skipped as foreign. + durability (4): boot oneshot that re-seats via heal; rotate.py stays the one rotation authority.
 3. PASS 7 under CHECK case (d): crons file §2 as written; /tmp tooling was wiped by the reboot: rebuild it from gen 6's transcript (fc2ded3f, PASS 6 09:53Z) or the §2 text.
 4. Guard is NOT on local-town: encryption-town ~/work/.sanctuary/GUARD.md (5 layers): measure docker (llama-server) first, GUARD_DOCKER_BUDGET_belam_gpu, dry-run, then sudo apply (§6 row 1 first).
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
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name; one shows → `brb`, then `brb --off` past the delay |
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
| 30 | the watcher cannot re-seat after a reboot (THOUGHT: inline prompt, shared card, reused @id, box-less SM) | per seat, from MAIN: `heal._watch_one_seat(Path('.agi'), row, windows, rot, launcher=L, pin_table=, seat_sessions=)` with L = write the command to /tmp/agi-recover-<seat>.sh + `heal._launch_recovered(..., cwd=cwd)`; rot = rotate whose spawn_window prompt_file = `<worktree>/.agi/sessions/quorum/<seat>.md`; drop from `windows` only an @id that equals the row's window AND is named for another seat; 30 s + MemAvailable >= 3 GiB between seats |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · `brb --status` · `systemctl --user list-units 'agi-*'`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| guard's watchdog reboot on local-town needs tang on gw for LUKS, else the box waits at the passphrase prompt | confirm local-town's unlock path before arming layer 4 |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
