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
gen 9 rotates at 0.41, under the 0.47 line, at PASS 9's ALL DONE. (1) Said: F27 "Rotate when [meter] post=<post> <f> reads f >= 0.47"; the hook: "at the line run rotate.py rotate yourself". (2) Machine: this seat's PASS 8 steps 4-9 took the meter 0.243 -> 0.33 for 30 rounds -- the cost is the read (30 KB of review extracts + 67 KB of verify verdicts, then the bodies); PASS 9 has 56 rounds, so ~0.15, and 0.41 + 0.15 = 0.56. (3) Near miss: working on to 0.47 obeys F27 and rotates inside the residue read, so the successor re-reads everything already read -- a split triage pays for the read twice and leaves a half-judged batch. (4) The property of this case: the one remaining step is an indivisible read-then-write larger than the window left, and ALL DONE is the only clean break before it; the successor starts at step 4 with the verdicts on disk.
<!-- THOUGHT:END -->

## §0 State (08:4xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-IX gen 9 · woke 05:4xZ · Opus 5.5 · pid 1216418 (session-73.scope) · ROTATING 17:2xZ at 0.41 (PASS 9 ALL DONE) · gen 8 pid 100337 idle, alive |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` (clean, = season2/main e55816f35b) · tz UTC · stream DOWN |
| GUARD | user@1000 high 5246M / max 5829M · a pi stage ~210 MiB · DE + gen 8 + remote-control INSIDE; belam gen 9, TM, DT in session-73.scope OUTSIDE (§6) |
| TOWN | DE gen 23 · TM gen 25 (rotated ~08:0xZ) · DT gen 33 · SM DOWN (owner's go) · 4 kid-worktree suite locks are pre-reboot dead pids |
| merge | PASS 8 CLOSED 07:37Z (season2/main e55816f35b) · **PASS 9 ALL DONE 17:22:03Z**: TIP 9e16b8ed90 pinned (trunk sync of DT key row a27dae50b0) · 56 rounds / 28 chunks · 51 accept_with_residue · 4 demote (engine-delta-1, engine-delta-5, a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid, l4-suite-green-on-main-the-18-reds-after-h2-and-rc-propagati) · 1 review-only · 2 empty-response rounds retried ok (p9retry1/2) · 3 runaway greps killed |
| decisions | 08:4xZ model-loading GO on 4 conditions -> DT 08:5xZ: condition (3) holds all 4 (agents in user@ app.slice: headroom 2383 MiB vs a 4.3-4.7 GB peak) -> 12:4xZ (d) hold until PASS 9 closes, (b) banked · 08:4xZ 2c GO: claude rm 5861181b DONE 08:46Z, reap verb = DE's DH.389 · 12:4xZ DH.380 alerts file: (a) I read ~/logs/memory-alarm-alerts.log, --status repoint banked |
| crons | CHECK fc879bab dies with gen 9 -> the successor re-arms it ("13 */4", next 20:13Z) · PASS 9 one-shot b0761a73 FIRED 13:47Z |
| spend | credits 13.75 USD · PASS 8 0 USD |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   PASS 8 (0-9) · CHECKs 08:4x / 12:4x / 16:4xZ · PASS 9 steps 0-3 + ALL DONE 17:22Z
next   the successor: PASS 9 steps 4-9 · the 20:13Z CHECK · judge DE/DT merge-ups
open   SM seat (owner's go) · the wedge's trigger (unproven) · §6
```

## §2 Landed (this seat)
a288a071df trunk sync · e55816f35b PASS 8 merge (season2/main) · local-maxxing/main ff a288a071df · b89c72454 residue batch + 5 defect hypotheses + board note · 9e16b8ed90 trunk sync (PASS 9 step 1) · card commits

## 🔴 Where it stops
17:2xZ 09-26 belam-S2-L5-IX rotates at 0.41: PASS 9 ALL DONE (56 rounds: 51 accept_with_residue, 4 demote, 1 review-only) -- the successor runs steps 4-9
```
 0. WAKE: re-arm the CHECK (fc879bab died with gen 9: pointer to crons section 1, "13 */4"); re-link the quorum card (trap 10). No PASS one-shot to re-arm: PASS 9 fired (pass_started_at SET) -- never relaunch it.
 1. Step 4: `cd .agi/worktrees/prime-root && python3 /tmp/belam-pass9/verdicts.py -v` (TIP 9e16b8ed9025e3e119625742ef31d5213e3e1607, OS a27dae50b0). band-byte-audit is review-only: read runs/mur-p9chunk23of28*/verify_band-byte-audit.json, retry it alone via retry.sh if it died. 12 RED keyword hits (node deletion 9, secret 2, api_key 1): read each in context. Objective gates vs OS: secret scan of added lines (counts only), node deletions by mint_id.
 2. Step 5 in prime-root: tree clean (trap 37) -> ff origin/season2/main -> merge-tree preview -> merge --no-ff TIP -> commands.py run verify -> push season2/main -> ff local-maxxing/main to TIP -> grid commit (background).
 3. Step 6 from VERIFY, never the review list (trap 38): hypothesis:pass9-0926-residue-batch under goal:g1 + one hypothesis per NEW code defect (assigned: director-engine; PASS 8's already-minted five are follow-up rows) -> ONE [decision] to DE; research rows via TM -> DT.
 4. Steps 7-9: state file (last_merged = TIP, pass fields null), one numbers-only town:local-maxxing note, commit by exact path, ONE [merge-up] to TM, owner report <= 6 lines.
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
`links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` (its 'last alerts' reads the old path) + `tail ~/logs/memory-alarm-alerts.log` · `memory_alarm.py` with the cadence's args + `--dry-run`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| 3 of 5 seats sit in session-73.scope, outside user@'s 5829M cap (measured 05:57Z) | spawn seats via `systemd-run --user --scope` (the tmux-spawn path), or cap user-1000.slice -- the owner's guard, the owner's call |
| guard follow-ups (TM 08:49Z + 09:33Z): the 4 queued model rounds cannot fit user@'s high beside the seats; guard-init.sh 'last alerts' reads sanctuary-guard/alerts.log, empty of memory alarms since DH.380 | run model loads in their own scope outside user@ with a MemoryMax (~6G); repoint 'last alerts' at ~/logs/memory-alarm-alerts.log -- your guard files, outside git |
| 2c leftovers (DE 07:39Z): exited session 710907bf "agi role orchestration setup" (cwd repo root, likely yours) + ~20 "Remote Control · offline" app rows (no CLI verb) | `claude rm 710907bf` if it is yours to drop; the app rows only from the app UI |
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (stream down) |
| the owner chain rule keeps an idle predecessor per rotation (~0.35 GiB each; gen 8 inside user@) | reap idle predecessors while the guard caps user@? the owner's call |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
