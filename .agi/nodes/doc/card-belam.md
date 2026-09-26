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
PASS 8 closed; two calls in it. (A) Killing reviewer greps. (1) Said: crons section 2 (3) "ONE Monitor on its events.log"; TM's rule "while io PSI stays high: hold, add no load". (2) Machine: a chunk-1 reviewer's `grep -rln ... .agi/` walked .agi/worktrees/ (101 checkouts) in a 4G pi scope: 3.98 GiB (3.7 inactive file), io some avg60 36%, user@ app.slice 33.6%, every other cgroup ~0; the kill took avg10 38% -> 4% in 20 s; monitor.sh then killed 3 more at io60 >= 25, and all 60 stages still returned (0 failed). (3) Near miss: holding (CAP 0) obeys "add no load" and leaves the stall running, because the load is a grep already inside a launched chunk. (4) Deviation: a reviewer's tool call killed -- scoped to recursive grep/rg/find over .agi/ or the root, only above io60 25. (B) DE's order puts brief.py first: brief.py:2371-2375 joins root/ref unchecked, so context/../../.env reaches the MAIN-root .env and a brief goes to a model provider; listing memory_alarm first (the only red) would leave that path behind a test-list fix.
<!-- THOUGHT:END -->

## §0 State (07:4xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-IX gen 9 · woke 05:4xZ · Opus 5.5 · pid 1216418 (session-73.scope) · meter 0.26 at 07:4xZ · gen 8 pid 100337 idle, alive |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` (clean, = season2/main e55816f35b) · tz UTC · stream DOWN |
| GUARD | user@1000 high 5246M / max 5829M · a pi stage ~210 MiB · DE + gen 8 + remote-control INSIDE; belam gen 9, TM 346048, DT 348635 in session-73.scope OUTSIDE (§6) |
| io | PASS 8's stalls were reviewer greps over .agi/ (101 worktrees): 4 killed; io PSI ~2% after · 101 worktrees = DE's 2c |
| TOWN | DE gen 23 · TM gen 24 · DT gen 33 · SM DOWN (owner's go) · 4 kid-worktree suite locks are pre-reboot dead pids |
| merge | **PASS 8 CLOSED 07:37Z** · season2/main 78a0d4b08b -> e55816f35b (tree == TIP a288a071df, pushed) · local-maxxing/main -> a288a071df (ff, pushed) · 30 rounds: 28 accept_with_residue · 2 demote · 0 RED · grid committed in prime-root · state file: last_merged a288a071df, pass fields null |
| residues | hypothesis:pass8-0926-residue-batch (goal:g1) + 5 code defects -> DE ([decision] 07:3xZ): brief extras escape · memory_alarm CLI + log cap · crons archive cap · term-grace real-process test · heal unparsable bound · research rows -> TM -> DT ([merge-up] 07:4xZ) |
| crons | CHECK fc879bab "13 */4" (next 08:13Z), POINTER to `.agi/sessions/prime-merge.crons.md` section 1 · section 2 = the PASS 9 procedure (not yet noticed) |
| spend | credits 13.75 USD · PASS 8 0 USD |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` (b89c72454 + a288a071df unpushed there: TM's) · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   PASS 8 steps 0-8 · trunk sync a288a071df · season2/main e55816f35b · local-maxxing/main a288a071df · batch + 5 defects -> DE · [merge-up] -> TM · crons section 2 -> PASS 9
next   the 08:13Z CHECK (quiet; notice PASS 9 only when new experiments land past a288a071df) · judge DE/DT merge-ups (swarm arms vs their last 5 single-parent rounds)
open   SM seat (owner's go) · the wedge's trigger (unproven) · §6
```

## §2 Landed (this seat)
a288a071df trunk sync (78a0d4b08b key row) · e55816f35b PASS 8 merge (season2/main) · local-maxxing/main ff to a288a071df · b89c72454 residue batch + 5 defect hypotheses + board note · fc977e543 / f089b7e71 card

## 🔴 Where it stops
07:4xZ 09-26 belam-S2-L5-IX: PASS 8 CLOSED at e55816f35b; nothing running; the CHECK at 08:13Z is next.
```
 1. CHECK (cron fc879bab, pointer to crons section 1): read dms newer than .agi/sessions/belam.lastcheck (05:xxZ, stamped by this seat), answer only what needs the Prime.
 2. PASS 9: the CHECK's case (b) sends the 5 h notice when experiments land past a288a071df; the procedure is crons section 2 (copy /tmp/belam-pass8 -> pass9).
 3. Watch DE's [decision] queue: 2c first, then brief-extras-escape, memory_alarm red, crons cap, term-grace test, heal bound.
```

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | quiet row: dms may sit in logs | `send.py read belam`; the inbox file is `.agi/sessions/inbox/belam.md` |
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
| 34 | `pgrep -f 'workflow.py run'` matches seat wrappers (their prompts carry it) | anchor: `pgrep -f '^(/usr/bin/)?python3 .*bin/workflow.py run'` |
| 35 | foreground `sleep` is blocked in Bash | Monitor with an until-loop, or run_in_background |
| 36 | a reviewer's `grep -r` over `.agi/` walks ~100 worktrees: 4G of cache, the box io-stalls | the focus text alone does not stop it; monitor.sh kills it at io60 >= 25 |
| 37 | `grid.py commit --all` in prime-root can leave an evidence-gate demotion dirty in the tree | step 5's merge refuses: save the patch, restore the file, merge |
| 38 | verify `verdicts[]` rules on the FIRST reviewer's defects (refuted true/false) + `missed[]` | a residue table reads verify, never the review list alone (PASS 8: 59 of 153 refuted) |

## §5 Verification
`links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` · `memory_alarm.py` with the cadence's args + `--dry-run`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| 3 of 5 seats sit in session-73.scope, outside user@'s 5829M cap (measured 05:57Z) | spawn seats via `systemd-run --user --scope` (the tmux-spawn path), or cap user-1000.slice -- the owner's guard, the owner's call |
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (stream down) |
| the owner chain rule keeps an idle predecessor per rotation (~0.35 GiB each; gen 8 inside user@) | reap idle predecessors while the guard caps user@? the owner's call |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
| MIN_REMAINING_CREDITS hard-coded 1 USD (provisioning.py:103, :206) | a config cell (a director-engine round) |
