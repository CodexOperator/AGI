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
gen 16 rotates at f 0.36 BEFORE PASS B3, not at the 0.47 line: a PASS is multi-ref and runs 1-2 h of monitoring, so it cannot finish inside this window, and the Prime rule hands such a step on whole rather than starting it (the near miss: starting B3 at 17:47Z obeys the cron and strands the merge mid-step at the line). Row F (a config:rotations first_turn entry) is handed on for the same reason: it edits what every post runs at wake, and it needs an in-process judge plus a dry wake read, not a rushed write.
<!-- THOUGHT:END -->

## §0 State (17:2xZ 09-29)
| | |
|---|---|
| post | belam-S2-L5-XVI gen 16 → successor gen 17 |
| formation | council loop LIVE until 23:00Z (owner 16:5xZ: "Keep working till 7pm next and I'll check my CC sub then") · bundle 3 = goal:g7.16.1.3 (grok core simplify; H1 g4.18.3 · H2 g4.18.4 first) with DG1 · alive @4 · all-is-one @5 · self-perpetuating @6 · DG1 @7 · DG2 @8 · DG3 @12 (agi-aa) · SM @13 (agi-1c) · stream-master @14 (NEW, side post) · TM/DT/DE DOWN |
| merge | PASS B2 2fb5c2043 · posts [red] fixed dcd06014e + sync #3 07f02d4a2 · PASS B3 due 17:47Z (BASE 922ff3f48d; 220 commits / 30 experiments / 0 D at 16:4xZ) |
| STREAM | Twitch LIVE, owned by stream-master now (doc:card-stream-master, skill agi-stream); delay 4m; dashboard page |
| crons | ALL die with this session. Successor RE-ARMS: CHECK "13 */4 * * *" · PASS B3 one-shot "47 17 29 9 *" (or run it at once under case (d) if past) · council STOP one-shot "0 23 29 9 *" |

## §1 Plan
```
DONE   PASS B2 · config:formations + registry · posts [red] · goals g1.30 g4.18.3 g4.18.4 · M review doc:council-loop-review-s2 · council resumed to 23:00Z · stream-master stood up 237fdfc3f
FIRST  B3. PASS B3 (below)
then   F. row F: config:rotations first_turn `formation` line (goal:g7.16.1.2.9, exact draft at its body :35-38) · S. the 23:00Z stop -> owner <= 6 lines, hold for the CC-subscription call
HELD   g1.30 / g4.18.3 / g4.18.4 dms to DE (DE down; the council took g4.18.3 + .4 into bundle 3) · encryption-town config
```

## §2 Landed (gen 16): 2fb5c2043 · acff4a1ab · 1532a604b · feed41d3e · dcd06014e · 07f02d4a2 · fc4320819 · fee990795 · 899ea077f · b3f12726e · 7705a3a73 · 883e27369 · 237fdfc3f

## 🔴 Where it stops
17:2xZ 09-29 belam-S2-L5-XVI: rotating before PASS B3; the successor's first act is PASS B3 at 17:47Z
```
B3. section 2 of .agi/sessions/prime-merge.crons.md (skill agi-merge-pass §2-§4): copy /data/home-belam/passB2 -> passB3, retag pb3 (grep every pb2 after copying).
    The council is LIVE (7 CC Opus sessions + stream): CAP 2 chunks, not 3, and hold on memory_alarm as launch.sh does.
    RED gates beyond the skill: anonymize over BASE..TIP (net range diff; DG1's bcff91a2c placeholder is removed at fc7cb0112) AND a hand grep of goal:g7.16.2
    for the other-box user segment (residue 46). Either open = hold the merge. verify in prime-root in the BACKGROUND (> 120 s; bin-suite-fresh = the known FAIL).
    CORE NOTE (alive 17:1xZ, for the next core <-> season2/main merge, NOT B3): core marks goal:g7.31.3.3 + .1-.5 COMPLETE but the 4 modules behind them
    (kid_write_gate · spawn_refusal · parent_slots · needs_rotate) are imported only by their own tests; the council's call: they land ACTIVE with a body line
    "built at <core sha>, test <file> n/n, not wired".
F.  row F: one first_turn entry in BOTH first_turn lists (director + prime_director) of config:rotations, text at goal:g7.16.1.2.9 :38;
    judge it in-process first (F12: `None` = allowed), then a write.py write as prime_director, commit by path.
S.  23:00Z: SendMessage the 8 posts (7 council + stream-master stays UP unless the owner says) "stop: finish the step, card whole, idle"; owner <= 6 lines.
V.  the video: /data/home-belam/manim-agi/agi_explainer.mp4 is on the owner's device; Drive/YouTube need the owner's own sign-in.
D.  /data: < 10 GB free -> no PASS launch.
R.  RENAME B LATER (owner): hostnamectl + guard.env _belam_gpu -> _local_town + /etc/hosts + guard-init --status, ONE window.
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
