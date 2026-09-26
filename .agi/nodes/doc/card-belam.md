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
gen 9 runs PASS 8 at PER=2 x CAP 3, not gen 8's 5 x CAP 6. (1) Said: crons section 2 (3) "every chunk its own background process ... <=6 live (GUARD ...: user@1000 capped at 5829M with the town inside it; was <=11)"; card step 1 "<= 6 live pi reviewers". (2) Machine: launch.sh's CAP counts CHUNKS (live.$n); workflow.py runs a chunk's rounds[] in parallel, one pi process per stage, each wrapped `systemd-run --user --scope` (workflow.py:1771-1772, mem_cap.wrap_argv) so it lands in user@1000.service/app.slice; measured 05:57Z: one pi scope 209 MiB, user@ hard (current - inactive_file) 1230 -> 1478 MiB. (3) Near miss: CAP=6 over build.py's 6 chunks of 5 satisfies "<=6 live" read as chunks and puts ~30 pi (~6 GiB) under user@'s 5246M high, where DE and alarms live -- reclaim, then OOM. The box's MemAvailable (10.6 GB) gate cannot see it: user@ is the cap. (4) Not a deviation from the rule, the stricter reading of it; added a user@ headroom gate (high - hard >= 1500 MiB) and a live CAP file. Measured beside it: 3 of 5 seats (belam gen 9, TM, DT) sit in session-73.scope, OUTSIDE the cap -- banked, the guard is the owner's.
<!-- THOUGHT:END -->

## §0 State (05:5xZ 09-26)
| | |
|---|---|
| post | belam-S2-L5-IX gen 9 · woke 05:4xZ · Opus 5.5 · pid 1216418 (session-73.scope) · meter 0.10 at 05:5xZ · gen 8 pid 100337 idle, alive |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` · tz UTC · stream DOWN |
| GUARD | user@1000 high 5246M / max 5829M · 05:57Z hard 1478 MiB (anon 937) · DE + gen 8 + remote-control INSIDE; belam gen 9, TM 346048, DT 348635 in session-73.scope OUTSIDE (§6) |
| alarm | memory_alarm cadence live · last WARN 05:29:43Z, cleared 05:32Z |
| TOWN | DE gen 23 · TM gen 24 · DT gen 33 · SM DOWN (owner's go) · 4 kid-worktree suite locks are pre-reboot dead pids (a00-0c992f07, -3a39d410, -be4e901f, -f2ba10d3) |
| merge | **PASS 8 RUNNING** · pass_started_at 05:51Z · trunk sync a288a071df (78a0d4b08b key row, clean) · TIP PINNED a288a071dfc0f23ab15085de5bf0a58a54f7fefb · BASE 08a9cf60f8 · 291 commits · 30 rounds (26 hyp/43 exp + 4 engine-delta/45 paths) · 15 chunks of 2 · CAP 3 live in `/tmp/belam-pass8/cap` · launched 05:56:46Z · Monitor bj8wc8odc (30 min, re-arm) |
| crons | CHECK fc879bab "13 */4" (next 08:13Z), POINTER to `.agi/sessions/prime-merge.crons.md` section 1 · PASS 8 one-shot NOT re-armed (ran under case d) |
| spend | credits 13.75 USD · pi-free route 0 USD |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   CHECK re-armed · pass_started_at · /tmp tooling rebuilt · trunk sync a288a071df · 30 rounds launched 05:56Z
next   PASS 8: watch -> verdicts.py -> RED gate -> step 5 in prime-root -> residues (test_commands_manifest on memory_alarm.py) -> state -> board note -> [merge-up] dm -> owner report
open   SM seat (owner's go) · the wedge's trigger (unproven) · DE queue · §6
```

## §2 Landed (this seat)
a288a071df trunk sync (origin/season2/main 78a0d4b08b into the trunk, PASS 8 step 1)

## 🔴 Where it stops
05:5xZ 09-26 belam-S2-L5-IX: PASS 8 RUNNING (pass_started_at 05:51Z) -- 15 chunks x 2 rounds on pi-free, CAP 3, TIP a288a071df pinned; a successor resumes at step 4.
```
 1. PASS 8 IN FLIGHT: pass_started_at is SET -- never relaunch. `tail /tmp/belam-pass8/events.log`; a successor re-arms ONE Monitor on it (the command is in this session's transcript 4ba9efb9: exits|ALL DONE|rc=[1-9]|ABORT + launcher death).
 2. A stage that died on 'Provider returned an empty response': write /tmp/belam-pass8/p8retryN.json with ONLY the failed rounds (merge_up 'p8retryN ...'), `bash /tmp/belam-pass8/retry.sh p8retryN`.
 3. On ALL DONE: `cd .agi/worktrees/prime-root && python3 /tmp/belam-pass8/verdicts.py -v`, then crons section 2 steps (4)-(9) with TIP a288a071dfc0f23ab15085de5bf0a58a54f7fefb.
 4. Residue already known: test_commands_manifest fails on memory_alarm.py (gen 8's 20680940c; TM [red] 04:5xZ) -> a defect hypothesis (assigned: director-engine).
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
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name; `pgrep -c` / `-x` only on the relay |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 17 | the Agent tool for graph recon | NEVER -- no Claude subagents (owner, F32) |
| 19 | a rotation's key row lands on season2/main; rotate-self refuses while the trunk is behind | merge it (sync.sh, merge-tree preview first) |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 25 | identity can drop mid-seat | `--from belam` on every send.py call |
| 26 | a reboot wipes /tmp PASS tooling | rebuild: transcript fc2ded3f (gen 6) tool_result 09:53:13.147Z split on `\n===\n` (build/launch/verdicts) + the result after 09:53:48.187Z (sync.sh, resolve.py), then this session's (4ba9efb9) retarget: BASE, dir, p8 prefixes, verdicts retry/unwrap, resolve opus-5-5/medium, PER + CAP file + user@ gate |
| 27 | every push prints the remote's moved location | `git push ... 2>&1 \| grep -v '^remote:'` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 29 | send.py refuses a dm body holding a literal harness tag | write it without the angle brackets |
| 30 | after a reboot heal re-spawns SOME seats | `reseat.py` from MAIN (transcript 82d56d5d); it seats into the caller's scope (session-73: outside user@) |
| 31 | resolve.py enforces the directors' model cells in a posts.md conflict | claude-opus-5-5 / medium (owner 09-26) |
| 33 | GUARD: pi stages land in user@ app.slice (~210 MiB each) | launch.sh CAP counts CHUNKS; PER x CAP <= 6 pi; gate on user@ hard, not MemAvailable |
| 34 | `pgrep -f 'workflow.py run'` matches seat wrappers (their prompts carry it) | anchor: `pgrep -f '^(/usr/bin/)?python3 .*bin/workflow.py run'` |
| 35 | foreground `sleep` is blocked in Bash | Monitor with an until-loop, or run_in_background |

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
