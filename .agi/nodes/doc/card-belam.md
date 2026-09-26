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
gen 8 resumed after the 03:56Z power cycle (owner, relayed by the sanctuary session: 1 the watchdog, 2 a memory alarm, 3 resume). Deviation: the Prime wrote engine code (memory_alarm.py + its test + the config:crons cadence, 20680940c). (1) Said: "Set a memory alarm if possible ... add whatever pressure / available-memory alarm fits the engine's alarm system", ordered BEFORE "Then resume normal operations". (2) Machine: rotate.py alarms is the rotation meter only (rotate.py:21810); sanctuary-watch has no pressure option; config:crons runs any named cadence that carries a cmd (crons.py:254-263), so the fitting home is a cadence whose cmd holds every threshold, and send.py dms surface through mail_alert + the 2-min wake. (3) Near miss: routing it to director-engine as a hypothesis keeps the role split and leaves the box unalarmed while the town's load returns, because DE's seat was dead (heal re-spawned it at 04:14Z). (4) Why the role rule did not apply: the owner ordered it of the Prime, first; its review lands at PASS 8/9. The 02:1xZ concurrency-up (30 live) is superseded by the guard's user@ cap: <= 10 live, no model-loading kid while the town is up.
<!-- THOUGHT:END -->

## §0 State (04:4xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-VIII gen 8 · RESUMED 04:1xZ after the 03:56Z power cycle · Opus 5.5 · pid 100337 · agi-rc @0 · row re-pinned 3e9a1ea36 (trap 28) · meter > 0.40: rotate before PASS 8 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` · tz UTC · LUKS unlocks by clevis tang (bound; tang answered 04:1xZ) · stream DOWN (relay not running) |
| GUARD | APPLIED 04:18Z (owner): `guard-init.sh --status` all 5 layers pass · user@1000 5829M (High 5246M) holds EVERY seat + spawn · agi.slice 4080M (engine 512M: reaper + alarms moved in 04:27Z) · oomd · softdog reboots at PSI full >= 40% for 5 min · watch timer 2 min · brain container capped 8192M |
| alarm | memory_alarm cadence (20680940c), every minute: WARN MemAvailable < 2048 MiB · PSI some avg60 >= 10 · user@ >= 95% of its cap; ALARM < 1024 MiB · PSI full avg60 >= 20 -> ~/logs/sanctuary-guard/alerts.log + a [red] dm to belam; silent while ok |
| TOWN | DE gen 23 @1 (heal crash-recovery 04:14Z; its row names gen 22's dead pid until its ack) · TM @2 + DT gen 33 @3 re-seated 04:28Z by reseat.py (trap 30) · SM DOWN (owner's explicit go) |
| merge | PASS 7 closed f6afb0c7c7 · PASS 8 noticed 00:44Z, run_at 05:47Z, section 2 now <= 6 live under the guard · trunk moved: 1b3eeabfc landed DE @295f73ade2 |
| directors | rows claude-opus-5-5 / medium · <= 10 live town-wide, pi rounds only, no model-loading kid while the town is up ([decision] 04:3xZ: DE delivered, TM pending) |
| branches | owner 09-25: directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |
| crons | CHECK a9db1585 "13 */4" (next 08:13Z) · PASS 8 one-shot c3e55a4a "47 5 26 9 *" · both POINTER prompts to `.agi/sessions/prime-merge.crons.md` sections 1/2: edit the file, not the cron |

## §1 Plan
```
done   00-02Z: crons · card · gc 258->80 MiB · hygiene hyp ede1350c2 · swarm ORDERS goal-first efe8908fb · 04-05Z (outage): guard · memory_alarm · row re-pin · TM + DT re-seated · concurrency limits
next   PASS 8 at 05:47Z -- ROTATE FIRST · the 08:13Z CHECK · judge DE/DT merge-ups (swarm arms vs their last 5 single-parent rounds)
open   SM seat (owner's go) · the wedge's trigger (unproven, §3.3) · DE queue (§3.2) · DT swarm 2 under the guard · §6
```

## §2 Landed (this seat)
63ba49a42a card + re-link · git gc 01:51Z (258 -> 80 MiB, fsck clean) · ede1350c2 hypothesis:cron-layer-keeps-its-disk-footprint-bounded -> DE · efe8908fb swarm ORDERS goal-first gate + --room · guard applied 04:18Z (system files, not git) · 3e9a1ea36 row re-pin · 20680940c memory_alarm · reseat TM + DT 04:28Z

## 🔴 Where it stops
05:4xZ 09-26 belam-S2-L5-VIII rotates at 0.48; PASS 8 fired in its session UNSTARTED (pass_started_at null) and is the successor's, case (d): guard + memory_alarm live (a WARN 04:39Z cleared 04:41Z), town back except SM, PASS 8 at 05:47Z is the successor's.
```
 0. WAKE (a successor): re-arm the CHECK (pointer, section 1); if now < 05:47Z re-arm the PASS 8 pointer one-shot, else run section 2 under CHECK case (d) unless the state file carries pass_started_at; re-link the quorum card (trap 10). gen 8 deletes ALL its crons at rotation (the resume had restored the pre-reboot verbatim pair beside its pointers: re-arm ONE pair). CHECK 04:43Z: nothing for the Prime (dms since 00:43Z predate gen 7's rotation), notice pending = case (c).
 1. PASS 8: <= 6 live pi reviewers; hold on a memory_alarm WARN in ~/logs/sanctuary-guard/alerts.log. /tmp tooling died with the reboot: rebuild from gen 7's transcript 82d56d5d (22:48Z 09-25).
 2. DE gen 23 queue ([decision]s in its inbox): 2c stale sessions / registry FIRST (owner) · 2d hygiene (ede1350c2) · the goal:g6.41 pair (heal re-spawned DE after this reboot but only DETECTED TM/DT) · mint "create refuses an unresolved parent" (node_writer.py:689-702 fails open) · the mem_cap probe re-running per wrap (PASS 7 defect).
 2b. Swarm trial: swarm 1 harvested both arms; swarm 2 builds --orders from the amended node (efe8908fb); judge at the merge-ups.
 3. The wedge (owner: worth a look): 0 global OOM kills; 1 hung task (gmain 03:31:26Z); 58 of 59 memcg kills = the mem_cap probe (~255 MiB each), capped, not the cause; only 3 kid dispatches 02:10-03:30Z; first distress = dockerd health-check failure on the then-UNBOUNDED brain container 03:18:25Z. Trigger unproven (no PSI history, empty container log); guard + alarm record the next one.
 4. SM: re-seat only on the owner's explicit go; the stream is down.
```
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the cron's box-local read consumes dms into the crons log too |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject, re-fences the slot | first slot line = plain text |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py via sync.sh: temp index + ff-only, never a conflicted MAIN |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | re-link after rotation: `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commit by exact path |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name (journal/kernel lines carry it: pipe through `sed "s/$(hostname)/<host>/g"`); one shows -> `brb`, then `brb --off` past the delay (`brb back` only prints usage) |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 23 | `pgrep -a` / `ps -ef` on the relay prints the stream keys | `pgrep -c` / `-x` only |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 25 | identity can drop mid-seat | `--from belam` on every send.py call |
| 26 | /tmp PASS tooling carries the LAST run's values AND a reboot wipes /tmp | retarget before a run; rebuild from the crons file text |
| 27 | every push prints the remote's moved location (`remote:` lines) | `git push ... 2>&1 \| grep -v '^remote:'` |
| 28 | after a reboot the seat row keeps the dead pid, so heal's crash-recovery can seat gen N+1 over a live Prime | `rotate._successor_row_write(Path('.agi'), actor=, seat=, role='prime_director', session_ref='', generation=, window=, pid=)`, commit posts.md by exact path |
| 29 | send.py refuses a dm body holding a literal harness tag | write it without the angle brackets |
| 30 | after a reboot heal re-spawns SOME seats (DE 09-26) and only detects + dedupes others (TM, DT) | `python3 <scratch>/reseat.py <seat>...` from MAIN; rebuild it by replaying the Write + Edit of `scratchpad/reseat.py` in transcript 82d56d5d (done 04:3xZ 09-26); 30 s + MemAvailable >= 3 GiB between seats |
| 31 | resolve.py enforces the directors' model cells in a posts.md conflict | claude-opus-5-5 / medium (owner 09-26) |
| 32 | a one-off `geometry_config.load_rows` reads 0 rows without graph_core on sys.path | `import rotate` first, then load |
| 33 | GUARD: user@1000 holds every seat + spawn in 5829M | size concurrency to it; a model-loading kid does not fit while the town is up; `guard-init.sh --status` |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` · `memory_alarm.py` with the cadence's args + `--dry-run` · `brb --status`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (stream down) |
| the owner chain rule keeps an idle predecessor per rotation (~0.4 GiB of user@'s 5.8G each) | reap idle predecessors while the guard caps user@? the owner's call |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
