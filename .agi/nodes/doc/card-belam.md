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
thought_session: belam-S2-L5-XVI
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 16 closed PASS B2 as its first act (the predecessor handed it on at f 0.41, the multi-ref rule). verify read 11/12 PASS; the one FAIL, bin-suite-fresh, is the skill's documented known FAIL (the pull + merge refresh every bin mtime in prime-root; it clears only in a suite window) and every round's reviewers ran their committed test files — so it did not hold the push, as at PASS B1. The step-6 [decision] dm to DE is HELD, not sent: DE is down for the council loop (recover:false + pid 0), and a dm to a down post is a message nobody reads; goal:g1.30 carries the residues until DE returns or the council bundles them.
<!-- THOUGHT:END -->

## §0 State (10:3xZ 09-29)
| | |
|---|---|
| post | belam-S2-L5-XVI gen 16 · window @11 · ListAgents agi-0e [8c6a5d] · gen 15's @0 still up (own-chain reap GATED OFF; not mine to kill) |
| formation | **COUNCIL LOOP LIVE** (goal:g7.16.1 · doc:council-loop): @4 alive · @5 all-is-one · @6 self-perpetuating · @7-@9 director-general-1..3 · @10 sanctuary-master; TM/DT/DE DOWN; 0 parent/kid spawns |
| loop | bundle 1 = goal:g7.16.1.1 (B -> E -> {C,D} -> A); DG1 minted leaves + 4 hyps @59ad74144 -> handed to DG2 (10:2xZ); stop 16:00Z |
| merge | PASS B2 CLOSED: season2/main 2fb5c2043 (TIP 922ff3f48, BASE ed34f49532) · local-maxxing/main ff -> 922ff3f48 · residues goal:g1.30 · state file closed · next = PASS B3 |
| DISK | / 61 GB free · /data 32 GB free (10:2xZ) |
| crons | CHECK 89c68201 "13 */4 * * *" · STOP one-shot 1fb0d341 "0 16 29 9 *" · PASS B3 one-shot 9d39a606 "47 17 29 9 *" — all THIS session's: a successor RE-ARMS the CHECK, and each one-shot not yet past |

## §1 Plan
```
DONE   P. PASS B2 close · DG3 seating row (pid 2122319 @9) · CHECK + STOP crons armed
NOW    L. supervise the council loop (room council-loop, town board, the posts' cards) · S. the 16:00Z stop
then   M. the Prime's own review of season 2's result, embodying the five morals (owner 09-29) + did the council materially improve results?
DONE   config:formations 1532a604b (file + write.py adopt, the route SM's mur-4 accepted): check_formation PASS active doc:council-loop g7.16.1 wake 0 · the adopt written_by hole -> goal:g4.18.3 (feed41d3e)
HELD   g1.30 [decision] dm to DE (DE down) · F facts window + G town note grant (TM/DE down) · OWNER 21:1xZ 09-27: stream · encryption-town config
```

## §2 Landed (gen 16): 519768b2c card re-link · 98cb94453 DG3 row · 2fb5c2043 PASS B2 merge (pushed) · acff4a1ab goal:g1.30 · 5ad6dadfd board note

## 🔴 Where it stops
10:3xZ 09-29 belam-S2-L5-XVI: PASS B2 closed at 2fb5c2043; supervising the council loop until the 16:00Z stop
```
L. Watch, never do the posts' work: `tail -5 .agi/comms/season-2/room/council-loop.md`, the town board, each post's card.
   A stalled handoff (> 45 min, no room line, post idle in ListAgents) -> SendMessage the stuck post by its ListAgents name.
S. 16:00Z 09-29 (owner: "stop around noon if still active by then in EST"): the one-shot fires -> SendMessage each of the 7 posts
   "stop: finish the atomic step, card whole + commit, idle"; then M.
B3. PASS B3 noticed 12:4xZ on the board (110 commits / 21 experiments / 25 engine paths past 922ff3f48d); runs 17:47Z = section 2 of .agi/sessions/prime-merge.crons.md (tooling /data/home-belam/passB3).
   PASS B3 RED gate: the range must pass `anonymize.py` over BASE..TIP -- bundle 2 residue 36 (2 other-box homes in goal:g7.16.2 + experiment:a00-6cb8a731-232b62, DG3) must be closed first, else hold the merge.
D. /data: < 10 GB free -> no PASS launch.
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
| 44 | `write.py create goal` without origin/seeds/heading_level is skipped by the render | set origin goals-doc, seeds [], heading_level 3; then `set confidence` + `set tags` (SCHEMA-WARNING) |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm | `git worktree list`; `find -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 50 | a reboot empties /tmp | PASS tooling lives on /data/home-belam (passB2, prime-merge-tools/trunk-sync) |
| 52 | after a --resume, `send.py read belam` refuses ("you are 'unknown'") | always `--from belam`; stand the post up: skill agi-post §4 |
| 54 | a post's claude pid / session id | `/proc` comm == claude under its pane pid; `~/.claude/sessions/<pid>.json` sessionId + name |
| 55 | verify in prime-root after a merge: `bin-suite-fresh` FAIL | the known FAIL (skill agi-verify §1); run verify in the background (> 120 s) |

## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` (406 goals, 10:3xZ) · verify @2fb5c2043 11/12 PASS (4954 nodes) · `spawn_budget.py status` (0 while the loop runs)

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| REBOOT 04:50Z 09-29: systemd-oomd made 67 kills, then sanctuary-health failed PSI-full >= 40% past 300 s and the watchdog rebooted BY DESIGN | (a) keep both guards (recommended) · (b) exempt seat infrastructure from oomd — root config · (c) cap the load |
| docker data-root still on / | a stop-the-daemon window; owner's word |
| DISK LATENCY: sda (USB SSD, dm-crypt, / + /data) ~35 ms/op | `sudo smartctl -a /dev/sda` · `sudo dmesg -T` |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` |
| grid commit in prime-root: 3 nodes missing mint_id (errors) | a `backfill-mint-ids.py` round for DE when it returns |
