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
thought_session: belam-S2-L5-XIII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 12 first card. The traps that now live in a skill (merge-pass: 6 19 26 27 31 33 34 36 37 38 39; send: 1 25 29 41; rotate: 2 10; workflow: 8 9) are listed as skills instead of rows -- owner 01:1xZ 09-27: "everyone's card just lists all the relevant skills". Traps no skill carries (3 13 15 24 28 30 40 + the new 42) stay.
<!-- THOUGHT:END -->

## §0 State (13:1xZ 09-27)
| | |
|---|---|
| post | belam-S2-L5-XIII gen 13 · woke 05:4xZ 09-27 · Opus 5.5 |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` · stream DOWN (HELD) |
| GUARD | OWNER GO 02:5xZ 09-27: model container brain-orcabonsai27b STOPPED (`docker start` restores) · docker budget 6656M -> 0 (guard.env.bak-20260927T*) · user@1000 high/max **12618M / 14021M** · agi-work.slice 9302M · sshd lane unchanged (reserve 1911M, ssh MemoryMin 64M CPUWeight 1000) · a pi stage ~210 MiB · load ~17/16 cores, io60 40-70 = the real bind |
| merge | **PASS 11 CLOSED 23:0xZ 09-27**: season2/main 739969f48 · next PASS BASE = 707d8dbbea · stale suite locks in 12 kid/base worktrees (dead pids) -- DE's sweep |
| crons | CHECK **a8bd064d** "13 */4 * * *" (re-armed 21:4xZ 09-27 -- gen 13 missed it at wake: a session-only cron dies with its session; 09:13-21:13Z unchecked). 21:4xZ CHECK: 127 commits past BASE 6c403aeb4b, 0 experiments -> no PASS |
| spend | **DRAINED: 0.606 USD** (flat 06:52Z -> 13:0xZ; owner 13:0xZ: no top-up funds). Cause (TM 06:42Z): config:workflows default + type rows = paid `pi` (deepseek) -> ~12.8 USD of murs. Paid paths CLOSED 56c1156ab. Resume = DE's zero-usd mint fix (§🔴 0) |
| dms | 03:0xZ [decision] -> TM: owner GO (DE cap 8 -> 12 -> 16 gated on load < 16 + io60 < 50; DT pause = TM's call; swarm-size test on TM's board) · 01:4xZ [decision] -> DE: hypothesis:wake-facts-collapse-to-skill-pointers (queued behind the redesigns) |
| branches | directors LOCAL-ONLY · thought-master ALONE pushes `local-maxxing/season2/main` · belam keeps `local-maxxing/main` + `season2/main` |

## §1 Plan
```
done   wake: card re-linked, CHECK re-armed · PASS 10 steps 0-3 (stamp, trunk sync 6c403aeb4, build, launch) · g4.18.2: 8 skills + nodes + links, HEAD line, CLAUDE.md trim, facts trim -> DE
next   g4.18.2 remainder: prime brief trim, other posts' cards pick up the HEAD line at their next write
HELD   OWNER 21:1xZ: stream · encryption-town config · sanctuary-master activation -- until messaging is done
open   SM seat (owner's go) · the wedge's trigger (unproven) · §6
```

## §2 Landed (gen 13): cdcfe5c0b wake re-link + facts region 37:57 · RENAME (owner 06:1xZ) goal:send-is-hub-only-... -> goal:g7.32.6 (post-branch address; mint kept, 6 refs) · 91f9e1236 TMM.288 box backfill, 18 posts rows = core-town (row_is_local unchanged; DH.498 unblocked) · (gen 12): 045d1aab3 wake re-link · 6c403aeb4 trunk sync (belam gen 12 key row) · 3 commits for g4.18.2: skills (8 files + 8 build nodes [goal:g4.18.2, idea:engine-skill-doc] + .claude/skills links, gitignore narrowed) · 9b2f1e378 HEAD line + DE hypothesis · 786dd91da CLAUDE.md 26,597 -> 10,123 bytes · d11cfc027 Prime template 10,470 -> 7,698 · d94a59fca g4.18.2 byte budget · OWNER 01:5xZ: monitor.sh io guard FINE-GRAINED (kills only processes whose ancestor argv carries this pass's tag; others -> spared.log) · sshd lane verified live (ssh.service MemoryMin=64M CPUWeight=1000, system.slice MemoryMin=128M, guard: chain live) · skills block -> doc:unified-director-brief, doc:unified-master-brief, 3 duty briefs, the DE/DT/TM/SM cards

## 🔴 Where it stops
04:0xZ 09-28 belam-S2-L5-XIII rotates at 0.43: PASS 12 retries running serially, then verdicts + merge are the successor's
```
R. RENAME (OWNER 03:5xZ): A DONE -- CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX=local-town here (tmux -g, ~/.profile, ~/.config/environment.d, systemd --user) and =encryption-town on encryption-town (ssh -F ~/work/.sanctuary/ssh/config; profile + environment.d + systemd; no tmux server there); new sessions only. B LATER (owner): hostnamectl + guard.env keys _belam_gpu -> _local_town (guard-init.sh:111 keys by hostname -s) + /etc/hosts + guard-init --status, all in ONE window. MY ERROR 03:4xZ: a bare `systemctl --user import-environment` leaked my shell env (AGI_POST=belam, messaging token, TMUX_PANE) into the systemd user env ~3 min; cleaned; [red] to TM. NEVER run it bare: `set-environment K=V` only.
Q. PASS 12 IN FLIGHT (/tmp/belam-pass12, tag p12chunk; owner order = the go, 5 h notice skipped): 0 stamped 00:44:09Z · 1 synced season2/main 12bc083f8 (PASS 11 merge + DE key row) into the trunk -> TIP PINNED 72d8d565ce0d4cbeea7955946bb185d053805a15, BASE 707d8dbbea · 2 built 25 rounds (21 hyp over 18 hypotheses + 4 engine-delta / 45 files), 13 chunks · 3 launched 00:44Z CAP=3 (held on the 00:41Z memory alarm, auto-resumes) · Monitor = bash /tmp/belam-pass12/monitor.sh (re-arm on expiry)
   03:05Z: 13/13 exited; 9 rounds had a pi rc=1 / timeout stage (02:39-03:05Z, cause unknown: free model probed OK, 0 USD spent, no OOM; owner: DE/TM contention on the shared account) -> retry1-5.json run ONE AT A TIME (events.log 'RETRIES DONE'); retry.sh PASS_TAG fixed p10->p12. RESIDUE for g1.28: workflow.py never persists a failed pi stage's stderr (a 429 would show there).
   NEXT: RETRIES DONE -> python3 /tmp/belam-pass12/verdicts.py -v (a REDKW hit is a keyword: read it in context + git diff --diff-filter=D; PASS 11's was 'no node deletion') -> retry.sh for unstructured/failed -> step 5 in prime-root (pull --ff-only, merge --no-ff 72d8d565ce, verify in background, push season2/main, ff local-maxxing/main) -> 6 residue leaf goal:g1.28 -> 7 state (last_merged = 72d8d565ce) + board note -> 8 [merge-up] TM -> 9 owner -> THEN reset the pass counter: new series 'B' (PASS B1, tag pb1chunk, /tmp/belam-passB1; keys mur-pb1chunk* do not exist).
   DECIDED 00:4xZ + 03:4xZ: tmpfs HOLD (GO = sweep fix merged + 24 h no crit; 4G), shape (a) KID worktrees only, parents on disk. TM's EG.1 landing 57debf3a2 (after TIP) rides the next pass (B1). Facts chain: my F13 trim + cell facts_pointer_target_bytes land WITH DE's chain + its test (region already 2009 B).
M. OWNER 00:0xZ 09-28 (verbatim on town:local-maxxing), [decision] to DE + TM sent: DE merges up its WHOLE post branch now (654 ahead), in-progress labelled -> DE resets DH + mur counters -> TM gates, lands, [merge-up] to me, resets its counters -> MY PASS over it (BASE 707d8dbbea) -> MY pass counter resets: a NEW series tag whose run keys do not exist (73 mur-p* dirs exist; e.g. PASS B1, tag pb1chunk; state pass_n + build.py/launch.sh/monitor.sh tags). RAM: when DE says the tmpfs claim is proved -> step 5 (a)-(c) below (parent + kid worktrees only).
P. PASS 11 CLOSED 23:0xZ 09-27: season2/main 739969f48; residues goal:g1.27.
0. DONE 17:1xZ: DE's zero-usd fix 91ae33672 is in the trunk -- live: can_fund free lane (True), paid lane refused at 0.61 (floor = cell provisioning.min_mint_remaining_usd); 8/30 live spawns on keys used=0; balance 0.6062; test_zero_usd_mint_floor 5 passed. Items 4 -> 5 now OPEN (owner GO 16:2xZ).
   OWED after DH.501 merges up: F13 'Spend checked by hand, one command, from any worktree:' -> 'Spend by hand, from any worktree:' (1988 B; HEAD's older classifier fails it before the merge -- measured 13:1xZ).
   OWED (TM 05:49Z, OWNER 05:48Z): `skills` first_turn entry in config:rotations (director + prime_director) from DE's doc:draft-skills-first-turn (DE post branch 40dd3bdc7).
1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass §1). Next notice when the trunk has new experiments past BASE 6c403aeb4b.
5. RAM WORKTREES (owner 04:2xZ: "handle transition to ram worktrees once the time comes ... it'll ease pressure for tests"): hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram
   (under goal:g7.31.3.3). DE at 04:2xZ: DH.499 LIVE on claims 1+2 (prune tool, dry-run default + paths.<town>.worktrees_root cell); claims 3 (tmpfs) + 4 (reboot prune) = its next round.
   WHEN claim 3 merges up (judge it like any merge-up): (a) guard.env += GUARD_WORKTREE_TMPFS_belam_gpu=4G (backup first; owner GO 02:5xZ covers the guard)
   (b) sudo -n ~/work/.sanctuary/guard/guard-init.sh, then --status: sshd chain live, reserve 1911M unchanged, user@ high/max recomputed (4G comes out of the 12618/14021M)
   (c) set paths.<town>.worktrees_root to the mount ONLY after (b) is green; POST worktrees + prime-root stay on disk (cards, uncommitted edits)
   (d) prove one kid lands there, commits to its branch, survives `git worktree prune`; watch io60 through the next PASS (target < 25)
   (e) sweep = heal.py sweep; its row -> DE's agi-dispatch §5 in the sweep's merge-up (OWNER 17:0xZ, [decision] 17:1xZ) -- check it at that judge
   (e) 92 DIRTY kid worktrees hold unharvested kid nodes (wt-decisions.log): the reaper harvests-or-deprecates before it may reclaim them -- never --force
6. SKILLS index: DONE 21:5xZ (config:rotations `skills` entry, both templates, cap 6000); card SKILLS block removed. OWED: re-add the agi-corrective clause when build:skills-agi-corrective-SKILL.md reaches the trunk (DE merge-up); HEAD B·FORM line -> 'the skill index loads at startup; a card never lists or copies skills'.
3. DE queue: dispatch-now hypothesis:reap-chain-members-get-their-full-term-grace-again (read 03:50Z) · then the redesigns · then the 7 PASS 10 defects (b5f2c2423).
4. AFTER 0 passes (OWNER GO 16:2xZ, verbatim on town:local-maxxing), then 5. Owner items open: TM's layout for DE concurrency (8 -> 12 -> 16, gated on load < 16 + io60 < 50) · DT pause = TM's call · swarm-size test on TM's board.
```
## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 24 | the trunk push is thought-master's alone (owner 09-25) | belam pushes only `season2/main` + `local-maxxing/main` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 30 | after a reboot heal re-spawns SOME seats | `reseat.py` from MAIN (transcript 82d56d5d) |
| 40 | F13's `/home/ubuntu/work/agi/.env` does not exist on local-town | the MAIN .env is `/data/work/agi/.env` |
| 42 | `write.py … 'replace body N:M'` refuses a range with no blank line around it (the HEAD's five diagram blocks are one "paragraph") | `--force` rides the SOURCE argument: `replace body N:M --force <file>`, after asserting the range; a refused replace in a chain still lets a later `thought` land -- check each line's result |


## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` + `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-` (drop column 2: every line carries the host name, TM [red] 02:36Z 09-27)

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| memory ALARM 05:08-05:21Z 09-27: box PSI full avg60 peaked 63.2% (watchdog reboots at >= 40% for 5 min); 2 GB swapped; calm since | the raise to user@ 12618/14021M moved pressure from user@ to the box. Middle ground: GUARD_DOCKER_BUDGET_belam_gpu=2048M -> user@ ~10.8/12.0G (sudo guard-init.sh; reversible) -- the owner's guard, the owner's call |
| 3 of 5 seats sit in session-73.scope, outside user@'s cap | spawn seats via `systemd-run --user --scope`, or cap user-1000.slice -- the owner's guard |
| guard follow-ups (TM 09-26): model rounds cannot fit user@'s high beside the seats; guard-init.sh 'last alerts' reads the old path | model loads in their own scope with MemoryMax (~6G); repoint 'last alerts' at ~/logs/memory-alarm-alerts.log |
| 2c leftovers (DE 07:39Z 09-26): exited session 710907bf + ~20 "Remote Control · offline" app rows | `claude rm 710907bf` if yours; app rows only from the app UI |
| stream-master's seat after the power cycle | re-seat only on the owner's explicit go (HELD 21:1xZ) |
| idle predecessors per rotation (owner chain rule) | reap on the owner's word |
| the origin remote moved (every push prints the new location) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea, 09-23) | opening it is the owner's call |
