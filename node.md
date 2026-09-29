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
gen 16 at the 16:00Z council stop. Every Prime-owed write this gen (config:formations twice) waited for sanctuary-master's review, and each wait paid: the review caught 3 defects in the owed commands before they ran (residues 16, 24, 27). The one [red] of the day was the rotation machinery's (e4aaef794 corrupted config:posts on season2/main), not the council's; the file was restored by hand and the cause is goal:g4.18.4. PASS B3 is the next multi-ref act, 17:47Z.
<!-- THOUGHT:END -->

## §0 State (16:1xZ 09-29)
| | |
|---|---|
| post | belam-S2-L5-XVI gen 16 · window @11 · ListAgents agi-0e [8c6a5d] · meter ~0.31 |
| formation | council loop RESUMED 16:5xZ until 23:00Z (owner: "Keep working till 7pm next and I'll check my CC sub then"; STOP one-shot a743e484 "0 23 29 9 *") · alive @4 · all-is-one @5 · self-perpetuating @6 · DG1 @7 · DG2 @8 · DG3 gen 2 @12 (agi-aa) · SM gen 2 @13 (agi-1c) · TM/DT/DE DOWN |
| loop | bundle 1 CLEAN 80c1c245d · bundle 2 CLEAN 9c54fb3c4 (R1 R3 R5 M P T) · bundle 3 = grok core simplify, not started · review doc:council-loop-review-s2 (899ea077f) |
| merge | PASS B2 closed 2fb5c2043 · posts [red] fixed on season2/main dcd06014e · trunk sync #3 07f02d4a2 · PASS B3 17:47Z (BASE 922ff3f48d) |
| STREAM | Twitch LIVE (T below) |
| crons | CHECK 89c68201 "13 */4 * * *" · PASS B3 one-shot 9d39a606 "47 17 29 9 *": both THIS session's; a successor RE-ARMS the CHECK and B3 if not yet past |

## §1 Plan
```
DONE   PASS B2 · DG3 row · config:formations 1532a604b + registry fee990795 · posts [red] dcd06014e + sync 07f02d4a2 · goals g1.30 g4.18.3 g4.18.4 · council stop 16:00Z · M review 899ea077f
NEXT   B3. PASS B3 17:47Z (below) · T. the stream until the owner ends it
HELD   g1.30 / g4.18.3 / g4.18.4 [decision] dms to DE (DE down) · bundle 3 on the owner's word · OWNER 21:1xZ 09-27 encryption-town config
```

## §2 Landed (gen 16): 519768b2c · 98cb94453 · 2fb5c2043 · acff4a1ab · 1532a604b · feed41d3e · dcd06014e · 07f02d4a2 · fc4320819 · fee990795 · 899ea077f

## 🔴 Where it stops
16:1xZ 09-29 belam-S2-L5-XVI: council stopped, review written; PASS B3 at 17:47Z; the Twitch stream is live
```
B3. 17:47Z one-shot = section 2 of .agi/sessions/prime-merge.crons.md (tooling: copy /data/home-belam/passB2 -> passB3, retag pb3). RED gates beyond the skill:
   anonymize over BASE..TIP (net range diff; DG1's bcff91a2c placeholder is removed again at fc7cb0112) AND a hand grep of goal:g7.16.2 for
   the other-box user segment (residue 46: a bare home path the regex once missed; closed 45-51 at 22677d774). Either open = hold the merge.
T. TWITCH STREAM LIVE (owner 14:3xZ "only livestream on twitch"; 15:0xZ dashboard + `live 0`; 16:5xZ "delay the stream by 4 minutes again" = `live 4m`, grown into at 1.15x):
   streamer-stub systemd unit grabs a PRIVATE Xvfb :2 (/data/home-belam/xvfb) = kiosk firefox on graphweb :8765 (3D dashboard);
   the masked feed /data/home-belam/classfeed/feed.py :8766 is the other page. X_KEY commented in ~/work/streamer-stub/.env (backup .env.pre-class).
   Controls: ~/bin/sb-status · brb · retract · back · panic. OFF on the owner's word -> `panic`, `systemctl --user stop streamer-stub`, restore .env.
   Start the unit with `systemctl --user start streamer-stub`: bin/stream.sh runs FOREGROUND when INVOCATION_ID is set (it is, in a CC shell).
V. The video (owner): /data/home-belam/manim-agi/agi_explainer.mp4 sent to the owner's device; Drive/YouTube need the owner's own sign-in.
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
| 56 | commit "by exact path" in the shared MAIN still takes a file ANOTHER post is editing (fee990795 swept DG3's WIP test edits) | before editing a shared engine/test file: `git status` it AND ask; commit a pinned blob (hash-object + update-index on a temp index), never the live file |
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
