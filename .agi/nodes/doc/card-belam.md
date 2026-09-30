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
thought_session: belam-S2-L5-XVII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 18 is a crash recovery, not a rotation: the ack refused on its own dirty row (rotate.py:3002), which was the spawn's own gen 17->18 write, so it was committed alone (skill agi-rotate: commit THAT, never bundle) before the ack. The trunk sync repeats gen 17's 1b340f1f4 for the one key-row commit that landed after it (3a4dcd6ce); the posts.md conflict was the stale gen 1 DG1/DG2 rows on season2/main, so the trunk side was kept and the merged file equals the trunk tip.
<!-- THOUGHT:END -->

## §0 State (21:0xZ 09-29, gen 18 recovered at 20:59Z)
| | |
|---|---|
| post | belam-S2-L5-XVIII gen 18 (RECOVERED: spawned 20:59Z, ack continue bb35f4c12 after committing the spawn's own row 12d8b278d; quorum link intact; meter 0.07) |
| formation | council loop LIVE until 23:00Z (owner 16:5xZ: "Keep working till 7pm next and I'll check my CC sub then") · bundle 3 = goal:g7.16.1.3 (grok core simplify; H1 g4.18.3 · H2 g4.18.4 first) with DG1 · alive @4 · all-is-one @5 · self-perpetuating @6 · DG1 @7 · DG2 @8 · DG3 @10 (agi-c5) · DG4 @12 agi-47 (owner 22:0xZ) · DG5 @14 agi-c8 (NEW 23:37Z, owner 23:3xZ; goal:g7.16.1.7) · council RESUMED 23:4xZ (owner 23:3xZ, no stop time) · DG3-5 room `directors` (owner 23:5xZ) · lens + outcome rule in doc:council-loop (4f93caa35) · SM @13 (agi-1c) · stream-master @14 (NEW, side post) · TM/DT/DE DOWN |
| merge | bundle 3 CLEAN re-confirmed ddea3a61f (SM 20:20Z, 23/23 residues closed, 0 red) = bundle 4 base · trunk syncs 1b340f1f4 (gen 17) + ce35d8c6f (gen 18: 3a4dcd6ce, ancestry only; the trunk is 0 behind season2/main) · PASS B2 2fb5c2043 · posts [red] fixed dcd06014e + sync #3 07f02d4a2 · PASS B3 due 17:47Z (BASE 922ff3f48d; 220 commits / 30 experiments / 0 D at 16:4xZ) |
| STREAM | OFF (owner 17:3xZ: "put stream-master on new box first then start the stream"): panic --retract + unit stopped + Xvfb :2 / kiosk / graphweb stopped (freed ~4.7 GB); stream-master (@5 agi-5c) told to hold; encryption-town readiness = investigator report pending |
| crons | RE-ARMED 21:0xZ by gen 18: CHECK c2bcbd3f "13 */4 * * *" · STOP d530989b 04:00Z 09-30 (owner: until ~midnight ET; 9 posts) · NEW LOOP 23:5xZ in doc:council-loop (DG2 MVP-vs-hyp forks -> DG1 builds-vs-goals subgoals -> DG1 OUTCOME per goal -> SM mur -> SM BIGGER_OUTCOMEs -> council new goals -> council OVERVIEWs -> belam) · [outcome] parents gain goal (c67f80708, d70d2593a) "0 23 29 9 *" · PASS B3 9f6c36ee "33 23 29 9 *". Session-only: a successor re-arms |

## §1 Plan
```
DONE   PASS B2 · config:formations + registry · posts [red] · goals g1.30 g4.18.3 g4.18.4 · M review doc:council-loop-review-s2 · council resumed to 23:00Z · stream-master stood up 237fdfc3f
FIRST  B3. PASS B3 (below)
then   F. row F: config:rotations first_turn `formation` line (goal:g7.16.1.2.9, exact draft at its body :35-38) · S. the 23:00Z stop -> owner <= 6 lines, hold for the CC-subscription call
STREAM-MASTER -> encryption-town: CONDITIONAL GO (plan <home>/enc-town-plan.md). OWNER must: grant sudo there (firefox + xvfb) and pick the branch of a separate s2 clone; formal migrate NO-GO today; air the masked FEED, never the 3D dashboard (7.6 cores of software WebGL)
PLACED goal:g6.41.1 (owner 17:3xZ "Make the recovery path restart tmux and your session as well") = bundle 3 ROW R after H4, before G/S2, leaf -> DG1 (alive 1559f7ae5): P1+P6 one launcher (rotate.py:1734 _launch_window, :1493 _shell_cmd) · P5 via memory_alarm.read_psi · closes on dummy scopes, never the live service · P2-P4 + falsifier 1 (RESUMED) = bundle 5 row 0. The box stays EXPOSED until P1 lands
PLACED THE WRITE/RENDER SPLIT (owner 17:4x-18:0xZ) = goal:g7.16.1.4 = BUNDLE 4 (old bundle 4 -> 5): W0 g4.19 (retitle or park) -> g4.18.5 (rows; a write is a commit) -> g4.18.6 (links = raw mint ids) -> g4.18.7 (read leaves write.py, owner 18:0xZ verbatim; lacks heading_level: [red] to alive)
OWNER  17:3xZ: RETIRE GOALS.md + the render round trip ("stop bothering with it") -> handed to alive as a bundle-3 row; NEVER render or --check GOALS.md again, never commit it
OWNER  17:2xZ: goal:g4.18.5 (write.py rows + line edits; a write is a commit behind the permission layer; assigned DE, a council bundle may take it) · move stream-master to encryption-town "once possible" (town:streaming-suite note; skill agi-post §3; needs encryption-town reachable)
HELD   g1.30 / g4.18.3 / g4.18.4 dms to DE (DE down; the council took g4.18.3 + .4 into bundle 3) · encryption-town config
```

## §2 Landed (gen 16): 2fb5c2043 · acff4a1ab · 1532a604b · feed41d3e · dcd06014e · 07f02d4a2 · fc4320819 · fee990795 · 899ea077f · b3f12726e · 7705a3a73 · 883e27369 · 237fdfc3f · gen 17: 45cf51809 · fa6f2c51b · a70ad4312 · 1b340f1f4 · gen 18: 12d8b278d · bb35f4c12 · ce35d8c6f · a8106f76a · 4b9ea1da0 (DG4 row) · 4876c1920 (DG4 card + goal:g7.16.1.5 horizon, owner RAM-disk idea) · W2d mint ruling (a) to DG2+DG1 22:1xZ

## 🔴 Where it stops
FIRST LINE FOR THE SUCCESSOR (Prime HARD RULE, gen 18 at f 0.39+): PASS B3 step 5 (the merge into season2/main) is YOURS -- when the pass ends (events.log "ALL DONE" / the launcher unit agi-pb3-launch inactive and every retry done): verdicts.py over <home>/passB3, the RED gates (anonymize BASE..TIP; the 3 formation D paths l4-formation-1/-3/-4 resolved by mint_id; goal:g7.16.2 other-box user segment grep), then section 2 step 5 in prime-root. TIP pinned 578650193 (the trunk moved on after it; merge only TIP). Retries so far: chunk5 (empty provider response) -> retry5. 01:0xZ 09-30 belam-S2-L5-XVIII. Was 21:0xZ 09-29 belam-S2-L5-XVIII (recovered): crons re-armed, trunk synced + pushed; inbox read through 20:54Z, nothing open for the Prime; waiting on the owner items for the stream-master move; council STOP 23:00Z, PASS B3 23:33Z; verify smoke BLIND on goal:g4.18.7 heading_level ([red] to alive 18:0xZ)
```
B0. RE-ARM (session crons die with a session): CHECK "13 */4 * * *" · council STOP "0 23 29 9 *" · PASS B3 "33 23 29 9 *" (memory gate first).
B3. IN FLIGHT since 23:33Z (state pass_started_at): TIP PINNED 578650193 (trunk sync 4c3c44b50 in); SAMPLED 40/257 rounds = 20 chunks, CAP 2 (council live), <home>/passB3 (sample.json, events.log); launcher unit agi-pb3-launch; RED gate owed before step 5: 3 formation nodes under .geometry/formations show D (l4-formation-1/-3/-4) -- resolve by mint_id (moved to deprecated = not a deletion). Was: section 2 of .agi/sessions/prime-merge.crons.md (skill agi-merge-pass §2-§4): copy <home>/passB2 -> passB3, retag pb3 (grep every pb2 after copying).
    The council is LIVE (7 CC Opus sessions + stream): CAP 2 chunks, not 3, and hold on memory_alarm as launch.sh does.
    RED gates beyond the skill: anonymize over BASE..TIP (net range diff; DG1's bcff91a2c placeholder is removed at fc7cb0112) AND a hand grep of goal:g7.16.2
        for the other-box user segment (residue 46). Either open = hold the merge. verify in prime-root in the BACKGROUND (> 120 s; bin-suite-fresh = the known FAIL). Residue 75 (a) LANDED 07ee9c46b (DG3; 5/5 match core's mint_ids, checked by the Prime): B3 carries it, nothing to check.
    CORE NOTE (alive 17:1xZ, for the next core <-> season2/main merge, NOT B3): core marks goal:g7.31.3.3 + .1-.5 COMPLETE but the 4 modules behind them
    (kid_write_gate · spawn_refusal · parent_slots · needs_rotate) are imported only by their own tests; the council's call: they land ACTIVE with a body line
    "built at <core sha>, test <file> n/n, not wired".
F.  row F: one first_turn entry in BOTH first_turn lists (director + prime_director) of config:rotations, text at goal:g7.16.1.2.9 :38;
    judge it in-process first (F12: `None` = allowed), then a write.py write as prime_director, commit by path.
S.  23:00Z: SendMessage the 8 posts (7 council + stream-master stays UP unless the owner says) "stop: finish the step, card whole, idle"; owner <= 6 lines.
V.  the video: <home>/manim-agi/agi_explainer.mp4 is on the owner's device; Drive/YouTube need the owner's own sign-in.
D.  /data: < 10 GB free -> no PASS launch. W. AFTER B3 closes: resume the worktree prune (goal:g7.16.1.5 body; 7/881 done, every byte kept under refs/archive/worktrees/*): systemd-run --user --unit=agi-wt-prune --slice=agi-work.slice --nice=19 --collect /usr/bin/python3 <home>/wt-prune/prune.py --apply --sleep 1 -- stop it while io PSI some avg10 > 60. RAM disk /mnt/agi-ram 7 GiB is UP (fstab nofail).
G.  GUARD IN THE GRAPH (owner 00:1xZ, subagent 00:5xZ): extensions/agi/guard/{guard-init.sh,sanctuary-health,sanctuary-watch,GUARD.md} + build nodes; guard.env -> config:guard (.agi/nodes/.geometry/guard.md, keys by box name via /etc/sanctuary-guard/box = local-town); /data/work/.sanctuary/guard/* + GUARD.md are SYMLINKS into the repo (originals *.pre-graph-20260930); dry-run = nothing changed, --status all ok. Residue to directors: refuse on a missing config:guard. goal:g7.16.1.8 = init pass + captive stand-up (horizon). Council owner-task 00:5xZ: rewrite goals g7.16.1.5-.8, g7.32.6, g4.18.5 from the owner verbatim through their lenses.
K.  KEYSYNC (00:1xZ 09-30): every rotation re-mints a key on season2/main and blocks every rotate until the trunk has it; timer agi-keysync (every 2 min, transient: re-arm after a reboot with systemd-run --user --unit=agi-keysync --slice=agi-engine.slice --on-calendar="*:0/2" --working-directory=/data/work/agi /usr/bin/python3 <home>/prime-merge-tools/trunk-sync/keysync.py) makes an ancestry-only merge ONLY when the pending commits touch posts.md alone and the trunk already carries every changed row pubkey; anything else -> ONE [red] to belam. Log keysync.log. Hand syncs tonight: ce35d8c6f 578650193 93f4567b5 90fb2b640.
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
| 44 | `write.py create goal` needs origin/seeds/heading_level + confidence + tags (schema) | set them at create; GOALS.md is RETIRED (owner 17:3xZ): never render it |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm | `git worktree list`; `find -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 50 | a reboot empties /tmp | PASS tooling lives on <home> (passB2, prime-merge-tools/trunk-sync) |
| 52 | after a --resume, `send.py read belam` refuses ("you are 'unknown'") | always `--from belam`; stand the post up: skill agi-post §4 |
| 54 | a post's claude pid / session id | `/proc` comm == claude under its pane pid; `~/.claude/sessions/<pid>.json` sessionId + name |
| 56 | commit "by exact path" in the shared MAIN still takes a file ANOTHER post is editing (fee990795 swept DG3's WIP test edits) | before editing a shared engine/test file: `git status` it AND ask; commit a pinned blob (hash-object + update-index on a temp index), never the live file |
| 55 | verify in prime-root after a merge: `bin-suite-fresh` FAIL | the known FAIL (skill agi-verify §1); run verify in the background (> 120 s) |

## §5 Verification: `links.py links` 0 broken · verify 18:1xZ gen 17: 11/13 PASS, smoke active 4859 / deprecated 231 / total 5090 (FAILs = goals-check vs retired GOALS.md + bin-suite-fresh, both known) · `spawn_budget.py status`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| REBOOT 04:50Z 09-29: systemd-oomd made 67 kills, then sanctuary-health failed PSI-full >= 40% past 300 s and the watchdog rebooted BY DESIGN | APPLIED 22:4xZ (owner picked (b)): oomd 85 % on user@1000 + its root slice (agi.slice stays 40 %), watchdog PSI_FULL 60 %, user@1000 MemoryHigh 13319M live. Knobs GUARD_OOMD_LIMIT / GUARD_USER_HIGH_PCT added to guard-init.sh (was a literal); backups *.bak-20260929T2245Z; apply log <home>/guard-apply-20260929T2245Z.log; --status all ok. Both kills today (05:15, 17:28) took the WHOLE claude-remote-control.service = every post. Before: owner asked oomd 50 -> ~85 % + more per-session leeway. Both oomd and the watchdog measure memory STALL time (PSI), not RAM used. The watchdog reboots at full avg60 >= 40 % for 300 s (sanctuary-health exit 2; the journal misprints it as ENOENT), so at 85 % a sustained thrash reboots the box before oomd kills one session. Options: (a) oomd 70 % + watchdog 40 % · (b) oomd 85 % + watchdog PSI_FULL 60 % (guard.env) · (c) oomd 85 % alone (NOT recommended). Recommend (b), plus user@1000 MemoryHigh 12618M -> 13.3G for leeway (no per-session cap exists while post_scope is off). All applied by ONE guard-init.sh re-run (the 50 % is a literal at guard-init.sh:209), which restarts oomd + daemon-reloads the user manager -> do it at a quiet point, owner present |
| belam row says claude-opus-5-5 / high / quiet; the live Prime runs claude-opus-5-5[1m] / max: a resume built from the row (goal:g6.41.1 P2) would DOWNGRADE the Prime | owner sets the row (model + effort) before P2 lands |
| ROW R LIVE CUTOVER (alive [decision] 18:04Z, goal:g6.41.1, DG1 11b2de165): tmux stays in claude-remote-control.service until restarted; a restart drops EVERY post + the Prime's crons + your remote link | after PASS B3 closes, owner present: (c) = StartTransientUnit(PIDs) into a Delegate=yes scope under agi.slice, every cgroup.procs pid but MainPID, repeat to empty (R1 v2 014912b17; AttachProcessesToUnit REFUSED on dummies) live ONLY if green + SM-clean; interim = ONE kill domain until P6 per-post scopes, else (a) planned restart; not (b) (box oomd-exposed to bundle 5). Dummy proof = GO now. STEP 1 at the cutover commit (alive [rule] 18:4xZ; the test is SKIPPED in every suite run, green once in DG3's build): env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q -- record its pass line here; NO pass line = (a), never (c) |
| docker data-root still on / | a stop-the-daemon window; owner's word |
| DISK LATENCY: sda (USB SSD, dm-crypt, / + /data) ~35 ms/op | `sudo smartctl -a /dev/sda` · `sudo dmesg -T` |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` |
| (closed gen 17) grid: 3 missing mint_id backfilled fa6f2c51b; 18 'unresolved' were all retired build nodes, now counted apart a70ad4312 | none |
