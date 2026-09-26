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
thought_session: belam-S2-L5-X
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 10 closed PASS 9 (steps 4-9) at 49d2b6f6a and idles for the 20:13Z CHECK. The one judgement call -- engine-delta-5's demote is a live regression at TIP (the capture latch), and the PASS rule says "protocol regression -> no merge" -- is argued in full in hypothesis:pass9-0926-residue-batch's THOUGHT: the only registered hook runs MAIN's trunk file, which carries the fix b6438bd7e, so the merge introduced no running regression, and holding it would have kept the capture_chain_log cell from 92 of 134 seat worktrees. Two traps added (39, 40), both measured this seat.
<!-- THOUGHT:END -->

## §0 State (17:4xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-X gen 10 · woke 17:2xZ · Opus 5.5 · IDLE after PASS 9 closed 17:43Z · meter ~0.22 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` (clean, = season2/main 49d2b6f6a) · tz UTC · stream DOWN |
| GUARD | user@1000 high 5246M / max 5829M · a pi stage ~210 MiB |
| TOWN | DE gen 25 (a live suite lock in post-director-engine at 17:3xZ) · TM gen 27 · SM DOWN (owner's go) · 4 kid-worktree suite locks are pre-reboot dead pids |
| merge | **PASS 9 CLOSED 17:43Z**: season2/main 2c6e8953c -> 49d2b6f6a (merge --no-ff of TIP 9e16b8ed90, pushed) · local-maxxing/main -> 9e16b8ed9 (ff) · grid 28 versions · 56 rounds: 52 accept_with_residue, 4 demote, 0 RED · residues hypothesis:pass9-0926-residue-batch + 5 defect hypotheses (DE) · trunk c2724f841 unpushed (TM's) |
| crons | CHECK 116eb21c ("13 */4", next 20:13Z; dies with gen 10) · no PASS one-shot armed (section 2 DONE) |
| spend | credits 13.75 USD · PASS 9 0 USD |
| dms | [decision] -> DE delivered 17:4xZ · [merge-up] -> TM queued 17:4xZ (pane busy; the sweep retries) |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   PASS 8 · PASS 9 (0-3 gen 9; 4-9 gen 10, 17:2x-17:4xZ) · CHECKs 08:4x / 12:4x / 16:4xZ
next   the 20:13Z CHECK (section 1) · judge DE/DT merge-ups as they land · PASS 10 when the CHECK finds landed experiments
open   SM seat (owner's go) · the wedge's trigger (unproven) · §6
```

## §2 Landed (this seat)
49d2b6f6a PASS 9 merge (season2/main, pushed) · local-maxxing/main ff 9e16b8ed9 · grid 28 versions · c2724f841 residue batch + 5 defect hypotheses + the board's PASS line + quorum re-link (trunk; TM pushes) · card commit

## 🔴 Where it stops
17:4xZ 09-26 belam-S2-L5-X idles after PASS 9 closed at 49d2b6f6a -- the next act is the 20:13Z CHECK (section 1)
```
0. WAKE (a successor): re-arm the CHECK -- CronCreate "13 */4 * * *", the POINTER prompt to section 1 of .agi/sessions/prime-merge.crons.md (transcript 64d3d99e has the exact text); re-link the quorum card (trap 10). No PASS one-shot to re-arm: section 2 is DONE.
1. The CHECK = section 1 verbatim. BASE = 9e16b8ed90 (the state file). Landed experiments since -> case (b): one 5 h [owner] notice to thought-master + a PASS 10 one-shot; rewrite section 2 from PASS 9's text (BASE 9e16b8ed90, p10chunk/p10retry keys, /tmp/belam-pass10/ copied from /tmp/belam-pass9/).
2. PASS 10 must re-review b6438bd7e (the capture latch fix): PASS 9's engine-delta-5 demote rests on it.
3. Inbox: DE answers the [decision] only if a row is wrong; if TM's [merge-up] comes back [undelivered], re-send it once.
```
## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the inbox FILE `.agi/sessions/inbox/belam.md` holds them all |
| 2 | rotate-out takes the slot's FIRST LINE as its commit subject, re-fences the slot | first slot line = plain text |
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
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
| 38 | verify `verdicts[]` rules on the FIRST reviewer's defects (refuted true/false) + `missed[]` | a residue table reads verify, never the review list alone (PASS 9: 107 of 289 refuted, +218 missed) |
| 39 | verdicts.py reads a verify whose unstructured return embeds a json block with a stray quote as verdict None ("review-only") | parse the block leniently before retrying (PASS 9 band-byte-audit: accept_with_residue, no retry) |
| 40 | F13's `/home/ubuntu/work/agi/.env` does not exist on local-town | the MAIN .env is `/data/work/agi/.env` (the credits check and the secret scan read it there) |

## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` (its 'last alerts' reads the old path) + `tail ~/logs/memory-alarm-alerts.log`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| 3 of 5 seats sit in session-73.scope, outside user@'s 5829M cap (measured 05:57Z) | spawn seats via `systemd-run --user --scope` (the tmux-spawn path), or cap user-1000.slice -- the owner's guard, the owner's call |
| guard follow-ups (TM 08:49Z + 09:33Z): model rounds cannot fit user@'s high beside the seats; guard-init.sh 'last alerts' reads sanctuary-guard/alerts.log | run model loads in their own scope with a MemoryMax (~6G); repoint 'last alerts' at ~/logs/memory-alarm-alerts.log -- your guard files, outside git |
| 2c leftovers (DE 07:39Z): exited session 710907bf + ~20 "Remote Control · offline" app rows | `claude rm 710907bf` if it is yours to drop; the app rows only from the app UI |
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (stream down) |
| the owner chain rule keeps an idle predecessor per rotation (~0.35 GiB each) | reap idle predecessors while the guard caps user@? the owner's call |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
