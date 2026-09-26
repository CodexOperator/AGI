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
| TOWN | RE-SEATED 22:33-22:37Z by the Prime (THOUGHT): TM gen 22 @2 (acked 28066c6076) · DE gen 20 @3 (waking; worktree card) · DT gen 31 @4 (acked eb064b313b; worktree card) · SM gen 4 @5: first DECLINED the seat without the owner's explicit go (live stream + keys, relayed words), then acked 87513b0b44 and works WITH THE OWNER directly (stream delay) -- never steer SM from here |
| fixes | hot patch 48e16356f0 on the trunk (goal:g6.49: per-boot mem_cap probe, memoized sweep, liveness backstop) · reaper + alarms restarted 22:24Z |
| merge | **PASS 7 CLOSED 00:06Z 09-26** → season2/main f6afb0c7c7 (pushed; merge --no-ff of trunk @08a9cf60f8, tree == TIP) · local-maxxing/main → 08a9cf60f8 (ff) · grid on season2/main 8 versions 0 errors · 9 rounds / 2 chunks pi-free 22:49-00:00Z 0 USD: 1 accept · 6 awr · 2 demote · 0 RED · residues f22a49b85d (hypothesis:pass7-0926-residue-batch + 3 code defects → DE; lm demote → TM) · state reset (last_merged_town_sha 08a9cf60f8; notice/run_at/pass_started_at null) · tooling /tmp/belam-pass7 + /tmp/belam-trunk-sync (rebuilt from gen 6's transcript fc2ded3f; retarget for PASS 8) |
| owner | 13:5xZ: the owner's words open doc:unified-head + both director cards · directors stay Sonnet · 22:0xZ: the hot patch "light chain" |
| directors | director-engine + director-thought, claude-sonnet-5 max · dispatches FREE (ladder.md:42-43 pi-free) · `doc:unified-director-brief` §1 |
| branches | owner 09-25: directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |
| crons | CHECK d88c4dcb "13 */4 * * *" re-armed 22:3xZ (session-only, 7-day) · no PASS one-shot (PASS 7 runs under case d) |

## §1 Plan
```
done   town re-seated · CHECK re-armed · card re-linked · re-seat hypotheses -> DE · owner's swarm trial routed (+ schemas in the parent brief) · PASS 7 CLOSED
next   the 04:13Z CHECK (section 1 as written; a new trunk delta -> the 5 h notice) · judge DE/DT merge-ups (swarm arms vs their last 5 single-parent rounds)
open   guard on local-town (3) · DE: re-seat + anchor hypotheses, the 4 PASS 6 defect hypotheses (defect 3 banked) · DT: lm-* demotes · §6
```

## §2 Landed (this seat)
town re-seat (rows by heal: TM 22 · DE 20 · DT 31 · SM 4) · CHECK d88c4dcb · 3888ca1fb4 card + quorum re-link · d9a5e8bfe8 hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart + hypothesis:a-reboot-brings-the-town-back-without-a-human (goal:g6.41) · 08a9cf60f8 trunk sync · 5bbcbe7128 + b72c1c9264 hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis (goal:g7.16, owner verbatim ×2) · f6afb0c7c7 season2/main PASS 7 (pushed) · local-maxxing/main ff → 08a9cf60f8 · f22a49b85d PASS 7 residues + board note

## 🔴 Where it stops
```
00:1xZ 09-26 belam-S2-L5-VII: PASS 7 CLOSED; the town is up; DE + TM hold the queue; the CHECK fires 04:13Z.
 1. The crons file section 2 still describes PASS 7: at the next notice rewrite it as PASS 8 (BASE = 08a9cf60f8; /tmp/belam-pass7 → pass8, p7 → p8 prefixes); the tooling in /tmp dies at reboot: gen 7's transcript 82d56d5d (22:48Z) holds every file.
 2. DE: [decision] 22:4xZ -- (1) hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart (inline prompt, shared-dir card, @id reuse, box-less SM row) then (2) hypothesis:a-reboot-brings-the-town-back-without-a-human (the anchor unit). No reply until the merge-up.
 2b. OWNER ASK 22:5xZ -- parent MINI-SWARMS trial: hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis (goal:g7.16, 5bbcbe7128; owner verbatim + ORDERS in the node). Build arm = DE ([decision] direct), research arm = DT via thought-master ([decision]); 3 parents/swarm, <= 3 swarms town-wide (DE 1, DT 1, 3rd to the first clean split at MemAvailable >= 3 GiB), <= 2 kids/parent, <= 1 model kid per research swarm. Judge at their merge-ups vs each branch's last 5 single-parent rounds; promote ORDERS to the parent template + 2 config cells only after the verdict.
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
| 31 | /tmp/belam-trunk-sync/resolve.py enforces the directors' model cells in a posts.md conflict | it now writes claude-opus-5-5 / medium (owner 09-26); change it with the owner's next model call |
| 32 | a one-off `geometry_config.load_rows` reads 0 rows without graph_core on sys.path (it swallows the ImportError) | `import rotate` first, then load |
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
