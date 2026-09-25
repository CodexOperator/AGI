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
thought_session: belam-S2-L5-VI
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 6 hands on a DOWN town after two reboots. Deviation: (1) the CHECK says "(d) notice pending, now >= run_at, one-shot never fired -> run the PASS now" (PASS 7, due 17:43Z). (2) The one-shot died in the 13:58Z memory wedge; at 21:55Z and 22:22Z every other seat was down, the stream relay was down, and a peer relayed the owner's order to hold, then to land the reaper/mem_cap fix and restart. (3) Near miss: case (d) taken literally starts a ~3 GB review pass on a box eight hours out of a memory livelock, before the fix that caused the load was on the trunk and with no thought-master to notify. (4) What makes the rule not apply: the owner redirected the session to the hot patch (22:0xZ), and a PASS needs a seated town to hand its residues to. It is held, not dropped: pass_started_at stays null. The trunk was never pushed from here.
<!-- THOUGHT:END -->

## §0 State (22:3xZ 09-25)
| | |
|---|---|
| post | belam-S2-L5-VI gen 6 · seated 09:52Z · Opus 5.5 · ROTATING 22:3xZ at meter ~0.44 (a town re-seat must not straddle a rotation) · row re-pinned 4f85922ca3: pid 29191 · window @0 in tmux `agi-rc` (session_name blank until the rotation writes it) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root = `season2/main` in `.agi/worktrees/prime-root` · tz UTC · REBOOTED 21:45Z (owner reset after the 13:58Z memory livelock) and 22:19Z (a login-screen suspend hung on NVIDIA; sleep targets now MASKED, LightDM autologins belam into XFCE, by the peer) |
| TOWN | DOWN except belam: no panes for thought-master, director-engine, director-thought, stream-master · stream relay NOT running · crash-recovery only 'detected' belam (stale row, fixed) and seated nobody |
| fixes | HOT PATCH 48e16356f0 on the trunk = origin/codex-town/season2/main @ab68638783 (goal:g6.49: per-boot mem_cap probe, memoized reaper sweep, cwd liveness backstop; the owner's "light chain": merge-tree clean except the derived GOALS.md, re-rendered 366/366 · heal + mem_cap tests 170 passed · links 0 broken) · engine units reaper + alarms RESTARTED 22:24:31Z · sanctuary-memwatch (peer's temporary root killer) STOOD DOWN 22:24Z, 0 kills |
| merge | PASS 6 CLOSED 10:49Z → season2/main 63c89d0068 · PASS 7 NOTICED 12:44Z (run_at 17:43Z) and HELD: its one-shot died in the wedge; pass_started_at null · delta at 22:22Z: 1bf60c203b → trunk, 91 commits · 9 exp (now + the hot patch) |
| owner | 13:5xZ: the owner's words open doc:unified-head (9af2dcd074; season2/main 0e52fcdc76) + both director cards (DE 3119882a3f, DT 7a180239fe on their branches) + [owner] dms · directors stay Sonnet; pi has NO xAI OAuth · 22:0xZ: "Check work/.sanctuary on encryption town for fixes ... heal and reaper fixes on codex town ... Has a light chain bare minimum allowed for a hot patch" |
| directors | director-engine + director-thought, claude-sonnet-5 max · dispatches are FREE (ladder.md:42-43 pi-free) · `doc:unified-director-brief` §1 |
| branches | owner 09-25: directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |
| crons | CHECK b79b541a "13 */4 * * *" (session-only; survived both resumes) · no PASS one-shot armed |

## §1 Plan
```
done   PASS 6 · owner HEAD + cards · CHECKs · hot patch 48e16356f0 · engine restart · memwatch down · row re-pin
next   the successor: RE-SEAT THE TOWN (where it stops, 1) -> then PASS 7 (2) -> then durability (4)
open   guard on local-town (3) · DE: the 4 PASS 6 defect hypotheses (defect 3 banked) · DT: lm-* demotes · §6
```

## §2 Landed (this seat)
1bf60c203b trunk sync · 63c89d0068 season2/main PASS 6 (pushed) · local-maxxing/main ff → 1bf60c203b · c40649160d PASS 6 residues · 9af2dcd074 + 0e52fcdc76 HEAD owner block · DE 3119882a3f + DT 7a180239fe cards · 48e16356f0 HOT PATCH (codex-town g6.49) · 4f85922ca3 row re-pin · cards/notes between

## 🔴 Where it stops
````
```
22:3xZ 09-25 belam-S2-L5-VI rotating with the TOWN DOWN after two reboots; the fixes are on the trunk, the engine restarted.
 1. RE-SEAT (owner, via the peer: "you land the fixes and restart"): thought-master -> director-engine -> director-thought -> stream-master (it restarts the stream relay). gen 5's 06:4xZ path: heal._watch_one_seat per seat with a /tmp/agi-recover-<seat>.sh launcher; tmux refused a whole prompt ('command too long'): put the prompt in a file.
 2. PASS 7 HELD, not dropped (pass_started_at null): once the town is up and memory holds, run crons file section 2 as written. /tmp/belam-pass6 + /tmp/belam-trunk-sync were WIPED by the reboot: rebuild from that text.
 3. Guard is NOT on local-town: encryption-town ~/work/.sanctuary/GUARD.md (5 layers) says measure docker (llama-server) first, set GUARD_DOCKER_BUDGET_belam_gpu, dry-run, then sudo apply; sudo works here without a password; `ssh -F ~/work/.sanctuary/ssh/config encryption-town`.
 4. Durability (owner options: a systemd unit per post that autorotates, or one unit for the tmux pane = the magic-pane anchor): REC the anchor + a boot oneshot that re-seats via heal (rotate.py stays the one rotation authority; GUARD caveat: restarting claude-remote-control kills every tmux server started inside it) -> a hypothesis for director-engine once seated.
```
````
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
| 10 | rotate's stop_commit flattens the symlinked quorum card (cause: hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write; DE landed 2054e3e04c) | re-link after rotation: `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commit both by exact path |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name; one shows → `brb`, then `brb --off` past the delay (no `back` on PATH) |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 20 | asking the owner for a go on a design the owner raised | decide, route, report |
| 23 | `pgrep -a` / `ps -ef` on the relay prints the stream keys | `pgrep -c` / `-x` only |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 25 | identity can drop mid-seat | `--from belam` on every send.py call |
| 26 | /tmp PASS tooling carries the LAST run's values AND a reboot wipes /tmp | retarget before a run; rebuild from the crons file text |
| 27 | every push prints the remote's moved location (`remote:` lines) | `git push ... 2>&1 \| grep -v '^remote:'` |
| 28 | after a reboot the seat row keeps the dead pid, so heal's crash-recovery tries to seat gen N+1 over a live Prime | re-pin via `rotate._successor_row_write(root, actor=, seat=, role='prime_director', session_ref='', generation=, window=, pid=)` (heal.py:2809's own writer), commit posts.md by exact path |
| 29 | send.py refuses a dm body holding a literal harness tag (`<system-reminder>`) | write it without the angle brackets |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` byte-identical · `commands.py run verify` (bin-suite-fresh FAIL known) · `brb --status` · `systemctl --user list-units 'agi-*'`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| guard's watchdog reboot on local-town needs tang on gw for LUKS, else the box waits at the passphrase prompt | confirm local-town's unlock path before arming layer 4 |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| retired belam panes + agi-98 (pre-reboot) | gone with the reboots; nothing to reap |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
