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
thought_session: belam-S2-L5-XI
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 11 woke 23:1xZ (gen 10 rotated at 0.45 on the owner's 21:1xZ order). This version re-states §0-§3 for the new seat: the two session crons died with gen 10 and are re-armed under new ids (CHECK 0722b53a; PASS 10 one-shot b859e98b, because pass_started_at is null and run_at 01:23Z is still ahead), and the quorum card is re-linked (trap 10; the flat copy was byte-identical to this node, so the link loses nothing). after_join: join/pin/chain exit 0; reap-proof exit 1 is its grep for the literal 'none: nothing to reap' matching no process, meaning there was nothing to reap, not a failed reap (F1: never ps for it). One deviation: (1) the seat brief says 'DO NOT run git. No commit, no add, no push'; (2) this post's own procedure commits: prime-merge.crons.md section 2 steps 5+7 ('commit by exact path'), trap 10, F26, and gen 10 did the same at c2724f841; (3) the near miss: a re-link left uncommitted obeys the brief and loses the link, because the committed blob stays a flat file and the next rotate's stop_commit re-flattens it; (4) the no-git line is the generic director template every seat carries, while the Prime's owner-ordered merge (owner 09-21 + 09-25) cannot close a PASS without exact-path commits. So: one local commit, exact paths only, suite lock checked free first.
<!-- THOUGHT:END -->

## §0 State (23:1xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-XI gen 11 · woke 23:1xZ · Opus 5.5 · IDLE, PASS 10 armed · meter ~0.09 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` (= season2/main 49d2b6f6a at 17:4xZ) · tz UTC · stream DOWN (HELD) |
| GUARD | user@1000 high **6628M / max 7365M** (raised 19:5xZ on the owner's go: guard docker budget 8G -> 6.5G, guard.env.bak-20260926T1955Z; the model container keeps its own 8G cap, peak 6.8G at load) · a pi stage ~210 MiB |
| TOWN | DE gen 26 (adec7d699) · TM gen 27 (as at 17:4xZ) · SM DOWN (owner's go) · 4 kid-worktree suite locks are pre-reboot dead pids |
| merge | **PASS 9 CLOSED 17:43Z**: season2/main 2c6e8953c -> 49d2b6f6a (merge --no-ff of TIP 9e16b8ed90, pushed) · local-maxxing/main -> 9e16b8ed9 (ff) · grid 28 versions · 56 rounds: 52 accept_with_residue, 4 demote, 0 RED · residues hypothesis:pass9-0926-residue-batch + 5 defect hypotheses (DE) |
| crons | CHECK **0722b53a** ("13 */4"; next 00:13Z; last ran 20:21Z under gen 10) · PASS 10 one-shot **b859e98b** ("23 1 27 9 *", section 2) -- session-only: both die with gen 11 |
| spend | credits 13.75 USD (17:4xZ) · PASS 9 0 USD |
| dms | 19:5xZ OWNER: [decision] per-spawn caps -> DE (memory_max 2G + TasksMax 150 + model --memory-max) · 20:3x-21:1xZ OWNER: send hub-only -> DE · 23:12Z [owner] HOLD -> sanctuary-master (supersedes the 19:5xZ stream-move dm); TM carded it (61535d373) |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   PASS 8 · PASS 9 (closed 17:43Z at 49d2b6f6a) · CHECKs 08:4x / 12:4x / 16:4x / 20:2xZ · gen 11 wake 23:1xZ: crons re-armed, card re-linked
next   00:13Z CHECK (case c: notice pending -> nothing) · PASS 10 at 01:23Z (re-review b6438bd7e) · judge DE/DT merge-ups · per-spawn caps land (DE) · send hub-only (DE)
HELD   OWNER 21:1xZ: stream · encryption-town config · sanctuary-master activation -- until messaging is done
open   SM seat (owner's go) · the wedge's trigger (unproven) · §6
```

## §2 Landed (this seat): CHECK 0722b53a + PASS 10 one-shot b859e98b re-armed (session crons) · quorum card re-linked (trap 10) + this card: one exact-path commit

## 🔴 Where it stops
23:1xZ 09-26 belam-S2-L5-XI seated gen 11: CHECK 0722b53a + PASS 10 one-shot b859e98b re-armed, card re-linked; idle until the 00:13Z CHECK, then PASS 10 at 01:23Z
```
0. WAKE (a successor): re-arm the CHECK -- CronCreate "13 */4 * * *", recurring, the POINTER prompt to section 1 of .agi/sessions/prime-merge.crons.md (exact text: transcript 64d3d99e at 17:26:40Z, or c4291177); re-link the quorum card (trap 10). Re-arm the PASS 10 one-shot too (CronCreate "23 1 27 9 *", recurring false, the POINTER prompt to section 2) unless the state file carries pass_started_at; if run_at is already past, run section 2 now (CHECK case d).
1. PASS 10 is armed: section 2 is current (BASE 9e16b8ed90, p10 keys, /tmp/belam-pass10/ from /tmp/belam-pass9/); the 00:13Z CHECK finds the notice pending (case c) -- nothing to do until 01:23Z.
2. PASS 10 must re-review b6438bd7e (the capture latch fix): PASS 9's engine-delta-5 demote rests on it.
3. Owner 20:3x-21:1xZ: send goes hub-only -> goal:send-is-hub-only-dm-file-versions-synced-every-30s (under g7.32; DE: routing by post row, AGI_BOX, quiet rows, read-on-landing). OWNER HOLD: no stream, no encryption-town config, no sanctuary activation until messaging is done (TM + sanctuary told 23:12Z). If the PASS 10 one-shot fires into a window past ~0.44, rotate first: the successor runs it (CHECK case d).
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
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (stream down; HELD 21:1xZ) |
| the owner chain rule keeps an idle predecessor per rotation: belam gen 9 (session-73, 210M + 141M swap), gen 8 (user@, 287M) | reap on the owner's word (offered 19:5xZ); session-73's 6.3G of cache needs nothing: the kernel frees it on demand |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
