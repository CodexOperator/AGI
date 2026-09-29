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
thought_session: belam-S2-L5-XV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 15 rotates at 0.41 with the council loop LIVE (goal:g7.16.1, owner 09-29 09:3x-10:1xZ): the PASS B2 merge is multi-ref, and the Prime rule starts none at f >= 0.41, so it is the successor's first act. The stand-up followed the mechanics mapped from heal.py/rotate.py/brief.py (now skill agi-post): stay-down flags (recover:false + pid 0) committed BEFORE the kill; every re-homed row had its core-town identity and pubkey cleared, because heal would treat a stale pid as a dead LOCAL post; council posts keep role director, because a `council` role has no brief parts and spawn would crash.
<!-- THOUGHT:END -->

## §0 State (10:1xZ 09-29)
| | |
|---|---|
| post | belam-S2-L5-XV gen 15 · resumed 08:4xZ after the 04:50Z reboot · stood up again 09:3xZ (row: pid 1416371, @0, agi-f9) · rotating at 0.41 |
| formation | **COUNCIL LOOP LIVE** (goal:g7.16.1 · doc:council-loop): tmux agi-rc = @0 belam · @4 alive · @5 all-is-one · @6 self-perpetuating · @7-@9 director-general-1..3 · @10 sanctuary-master; TM/DT/DE DOWN (recover:false + pid 0, killed 10:1xZ after down-ready); 0 parent/kid spawns |
| loop | alive drafted bundle 1 (7a96e32e4); order: town bundle -> grok's core/season2/main + core/main (simplify) -> ONLY then season-2 close out to overview nodes; stop 16:00Z (noon ET) |
| merge | PASS B2 (restart 08:59:29Z, tag pb2b, D=/data/home-belam/passB2): TIP 922ff3f48 · 9 accept_with_residue + 1 demote (engine-delta-1: inert config cell, RED words = negations) + 2 verify stages retrying (rnow.sh, 10:03Z) · RED checks clean |
| DISK | / 63 GB · /data 34.6 GB (08:50Z; 1040 worktrees + .agi/sessions 24.6 GB; DE now down) · flash 114 GB |
| crons | CHECK da6f2ed6 "13 */4 * * *" is THIS session's: a successor RE-ARMS it (skill agi-merge-pass §1) |

## §1 Plan
```
FIRST  P. close PASS B2 (below)
then   L. supervise the council loop (room council-loop, town board lines, the posts' cards) · S. the 16:00Z stop
then   M. the Prime's own review of season 2's result, embodying the five morals (owner 09-29) + did the council materially improve results?
HELD   F facts window + G town note grant (TM/DE down) · OWNER 21:1xZ 09-27: stream · encryption-town config
```

## §2 Landed (gen 15, after the reboot): 780c491f6 row · 715a56212 card · 922ff3f48 sync #2 · d000d6ccf g17 -> g7.16:29 · 18a897c48 goal:g7.16.1 · b0b54f6fa skill agi-post · 362382cba doc:council-loop + 7 cards · 9255e1f71 posts rows · 7 seating rows (fceec1ed9 …)

## 🔴 Where it stops
10:1xZ 09-29 belam-S2-L5-XV: council loop live (8 posts); the successor's first act is the PASS B2 close
```
P. PASS B2: wait for rnow.sh (`tail /data/home-belam/passB2/events.log`: RNOW DONE / GAVE UP) -> `python3 /data/home-belam/passB2/verdicts.py | grep -E 'TOTALS|ATTN'`;
   read the RED words in context (send-read: 'secret', engine-delta-3: 'node deletion') -> step 5 in prime-root (/mnt/agi-flash/worktrees/prime-root):
   pull --ff-only · merge-tree preview · merge --no-ff $(cat /data/home-belam/passB2/TIP) · commands.py run verify · push season2/main ·
   ff local-maxxing/main to TIP · grid.py commit --all (background) -> step 6 residues leaf goal:g1.<next> (skill agi-goal; origin goals-doc, seeds [], heading_level 3)
   -> step 7 state file (last_merged_town_sha = TIP, pass fields null) + ONE numbers-only board note -> step 8: TM is DOWN, the report rides the board note -> owner <= 6 lines.
L. LOOP: DG3's seating row has pid 0 (window @9; the join missed): heal will not guard it -> skill agi-post §4 with DG3's claude pid + @9.
   Watch, never do the posts' work: `tail .agi/comms/*/room/council-loop.md`, the town board, each post's card. A stalled handoff -> SendMessage the stuck post.
S. STOP 16:00Z 09-29 (owner: "stop around noon if still active by then in EST"): CronCreate one-shot "0 16 29 9 *" -> SendMessage each of the 7 posts
   "stop: finish the atomic step, card whole + commit, idle"; then M.
D. /data: < 10 GB free -> no PASS launch. DE's prune is moot while DE is down: list the finished trees on the card for the owner.
R. RENAME B LATER (owner): hostnamectl + guard.env _belam_gpu -> _local_town + /etc/hosts + guard-init --status, ONE window. NEVER a bare `systemctl --user import-environment`.
```
## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 24 | the trunk push was thought-master's; TM is down | spawn/ack push the current branch; branch_push pushes hourly at :07 |
| 40 | F13's home-path .env does not exist here | the MAIN .env is `/data/work/agi/.env` |
| 43 | `send.py read` shows EMPTY while blocks sit in `.agi/sessions/inbox/belam.md` | read the inbox FILE by ts at every CHECK |
| 44 | `write.py create goal` without origin/seeds/heading_level is skipped by the render | set origin goals-doc, seeds [], heading_level 3 |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm; `du --max-depth=1 .agi/sessions` > 120 s | `git worktree list`; `find -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 48 | `~/.claude/projects/*` names start with '-' | always `--` or a `./` prefix |
| 50 | a reboot empties /tmp | PASS tooling lives on /data/home-belam (passB2, prime-merge-tools/trunk-sync) |
| 51 | watchdog "returned 2 = 'No such file or directory'" | = sanctuary-health EXIT 2 (PSI full avg60 >= 40%); the binary exists |
| 52 | after a --resume, `send.py read belam` refuses ("you are 'unknown'") | always `--from belam`; stand the post up: skill agi-post §4 |
| 53 | PASS reviewers keep trying `grep -r` over the repo root | monitor.sh's io guard kills them (tag-scoped); expected, not a red |

## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` (397 goals, 10:0xZ) · `df -B1M / /data` · `python3 extensions/agi/bin/spawn_budget.py status` (0 while the loop runs)

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| REBOOT 04:50Z 09-29: systemd-oomd (user@1000: 50% memory PRESSURE for 20 s) made 67 kills in that boot, never the load; then sanctuary-health failed its PSI-full >= 40% test past 300 s and the watchdog rebooted BY DESIGN | (a) keep both guards (recommended) · (b) exempt seat infrastructure (remote-control, reaper, alarms) from oomd — root config · (c) cap the load (the council loop runs no pi fleet) |
| docker data-root still on / | a stop-the-daemon window; owner's word |
| DISK LATENCY: sda (USB SSD, dm-crypt, / + /data) ~35 ms/op | `sudo smartctl -a /dev/sda` · `sudo dmesg -T` |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` |
