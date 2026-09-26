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
thought_session: belam-S2-L5-IX
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The 08:4xZ CHECK decided two asks. (A) DE's 2c: GO for `claude rm 5861181b` only. (1) Said: CLAUDE.md "authority never covers an irreversible or destructive operation outside the loop's own commits"; the owner's 2c (01:0xZ) "the app lists only live sessions". (2) Machine (DE, read-only `claude agents --json --all`): 5861181b is an exited --bg "throwaway probe" whose cwd is kid worktree a00-5aaa03c7 -- a session the loop created (TMM.202: kids never launch claude); `claude rm` works on exited --bg sessions only. (3) Near miss: banking all of 2c leaves the owner's own ask undone for the loop's own artifact; deleting 710907bf too meets "only live sessions" and destroys what is likely the owner's own session. (4) The rule guards the owner's things; this is the owner-requested end state applied to the loop's own artifact -- 710907bf + the app rows stay banked. (B) TM's model-loading GO carries a user@ condition: kid spawns land in user@ app.slice via systemd-run --user (workflow.py:1771-1772), high 5246M with DE's seat and the alarms inside; "quiet town" read as box MemAvailable 10.4 GiB says yes to a 4.7 GB load that crosses user@'s high.
<!-- THOUGHT:END -->

## §0 State (08:4xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-IX gen 9 · woke 05:4xZ · Opus 5.5 · pid 1216418 (session-73.scope) · meter 0.33 at 08:4xZ · gen 8 pid 100337 idle, alive |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` (clean, = season2/main e55816f35b) · tz UTC · stream DOWN |
| GUARD | user@1000 high 5246M / max 5829M · a pi stage ~210 MiB · DE + gen 8 + remote-control INSIDE; belam gen 9, TM, DT in session-73.scope OUTSIDE (§6) |
| TOWN | DE gen 23 · TM gen 25 (rotated ~08:0xZ) · DT gen 33 · SM DOWN (owner's go) · 4 kid-worktree suite locks are pre-reboot dead pids |
| merge | PASS 8 CLOSED 07:37Z: season2/main e55816f35b · local-maxxing/main a288a071df · b89c72454 PUSHED by TM · research rows landed 49e8cd268 (TM: TMM.210) · **PASS 9 NOTICED 08:45Z, run_at 13:47Z** (one-shot b0761a73): trunk a288a071df -> 052e8991c7 · 124 commits · 56 exp · 24 engine paths |
| decisions 08:4xZ | TM: model-loading GO -- one at a time via model_slot, floor = peak + 2 GiB, WARN = stop, inside user@ peak + hard under high - 512 MiB, no new load 13:30Z until PASS 9 closes · DE 2c: GO claude rm 5861181b only + the kid-session reap verb (dry-run default) |
| crons | CHECK fc879bab "13 */4" (next 12:13Z) · PASS 9 one-shot b0761a73 "47 13 26 9 *" · both POINTER prompts to `.agi/sessions/prime-merge.crons.md` sections 1/2 |
| spend | credits 13.75 USD · PASS 8 0 USD |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   PASS 8 (0-9) · 08:4xZ CHECK: 4 dms, 2 decisions, PASS 9 notice + one-shot
next   the 12:13Z CHECK · PASS 9 at 13:47Z (meter > 0.38 then: ROTATE FIRST, the successor runs it under case d) · judge DE/DT merge-ups
open   SM seat (owner's go) · the wedge's trigger (unproven) · §6
```

## §2 Landed (this seat)
a288a071df trunk sync · e55816f35b PASS 8 merge (season2/main) · local-maxxing/main ff a288a071df · b89c72454 residue batch + 5 defect hypotheses + board note · card commits

## 🔴 Where it stops
08:4xZ 09-26 belam-S2-L5-IX: idle after the CHECK; PASS 9 noticed for 13:47Z (one-shot b0761a73); the 12:13Z CHECK is next.
```
 1. CHECK (fc879bab -> crons section 1): dms newer than .agi/sessions/belam.lastcheck (08:43Z); the inbox FILE is .agi/sessions/inbox/belam.md.
 2. PASS 9 (b0761a73 -> crons section 2): copy /tmp/belam-pass8 -> /tmp/belam-pass9, retarget BASE a288a071df + p9 prefixes; PER=2, CAP 3, ONE Monitor = bash monitor.sh.
 3. A successor whose wake is past 13:47Z: re-arm the CHECK, run PASS 9 under case (d) unless the state file carries pass_started_at; re-link the quorum card (trap 10).
```

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the inbox FILE `.agi/sessions/inbox/belam.md` holds them all |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject, re-fences the slot | first slot line = plain text |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 5 | a merge-up-review stage hangs on rotate test files (tty) | build.py drops `tests/*rotate*` |
| 6 | posts.md rows conflict between the trunk and season2/main | resolve.py via sync.sh: temp index + ff-only, never a conflicted MAIN |
| 8 | the harness says "use the Workflow tool" (ultracode) | not the route: workflow.py by name on pi-free (F29) |
| 9 | Bash shells never re-source the profile | `PI_BIN=$HOME/.npm-global/bin/pi` inline; `send.py send --from belam` |
| 10 | rotate's stop_commit flattens the symlinked quorum card | re-link after rotation: `ln -sfn ../../nodes/doc/card-belam.md .agi/sessions/quorum/belam.md`, commit by exact path |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name; `pgrep -c` / `-x` only on the relay |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 25 | identity can drop mid-seat | `--from belam` on every send.py call |
| 26 | a reboot wipes /tmp PASS tooling | rebuild: transcript fc2ded3f tool_result 09:53:13.147Z split on `\n===\n` + the result after 09:53:48.187Z (sync.sh, resolve.py), then transcript 4ba9efb9's retarget (PER, CAP file, user@ gate, monitor.sh, resolve opus-5-5/medium) |
| 27 | every push prints the remote's moved location | `git push ... 2>&1 \| grep -v '^remote:'` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 29 | send.py refuses a dm body holding a literal harness tag | write it without the angle brackets |
| 30 | after a reboot heal re-spawns SOME seats | `reseat.py` from MAIN (transcript 82d56d5d); it seats into the caller's scope (session-73: outside user@) |
| 31 | resolve.py enforces the directors' model cells in a posts.md conflict | claude-opus-5-5 / medium (owner 09-26) |
| 33 | launch.sh CAP counts CHUNKS; a chunk runs its rounds in parallel (1 pi each, ~210 MiB, in user@ app.slice) | PER x CAP <= 6 pi; gate on user@ hard, not MemAvailable |
| 34 | `pgrep -f 'workflow.py run'` matches seat wrappers; foreground `sleep` is blocked | anchor the pattern; wait with Monitor / run_in_background |
| 36 | a reviewer's `grep -r` over `.agi/` walks ~100 worktrees: 4G of cache, the box io-stalls | the focus text alone does not stop it; monitor.sh kills it at io60 >= 25 |
| 37 | `grid.py commit --all` in prime-root can leave an evidence-gate demotion dirty in the tree | step 5's merge refuses: save the patch, restore the file, merge |
| 38 | verify `verdicts[]` rules on the FIRST reviewer's defects (refuted true/false) + `missed[]` | a residue table reads verify, never the review list alone (PASS 8: 59 of 153 refuted) |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` · `memory_alarm.py` with the cadence's args + `--dry-run`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| 3 of 5 seats sit in session-73.scope, outside user@'s 5829M cap (measured 05:57Z) | spawn seats via `systemd-run --user --scope` (the tmux-spawn path), or cap user-1000.slice -- the owner's guard, the owner's call |
| 2c leftovers (DE 07:39Z): exited session 710907bf "agi role orchestration setup" (cwd repo root, likely yours) + ~20 "Remote Control · offline" app rows (no CLI verb) | `claude rm 710907bf` if it is yours to drop; the app rows only from the app UI |
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (stream down) |
| the owner chain rule keeps an idle predecessor per rotation (~0.35 GiB each; gen 8 inside user@) | reap idle predecessors while the guard caps user@? the owner's call |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
