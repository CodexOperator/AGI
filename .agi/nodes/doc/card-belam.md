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
thought_session: belam-s2-III
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs; progress lives on the town board. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s2-III 09:2xZ 10-10, at wake: crons re-armed (CHECK 13b11552 13 */4 trajectory-first, hourly 7647814e 47 *); SM's .13.3 COMPLETE land taken as merge a65c401470 (MAIN had moved to my card, ff-only impossible); ruled .8's Stop hook = explicit timeout 180 in the same cut; B6 verifier (Sonnet) CLEAR, 12/12 findings confirmed -> B6 merged ef9b043e68, residues goal:g1.43 to SM; agi-at ruled to call the same growth check as agi-turn. B6 merge shape checked: season2/main 7276f11d36 tree == B5 TIP tree, B5 TIP is an ancestor of B6 TIP -> M6 = commit-tree TIP^{tree} -p 7276f11d36 -p TIP drops nothing. Owner verbatim carried from belam-s2-II: "Nah just use sonnet subagents and we retired workflows.py in favor of shel scripts already" · "Yes always. Thats your main check every 4 hours is to see what’s stuck if anything and keep town on trajectory and moving toward season completion" · "I’m fine with the Nvidia pick yes" · "We don’t use the ladder anymore" / "It needs to be deprecated" · "The bazzite vm is temporary just doing a local town related project in the background".
<!-- THOUGHT:END -->

## §0 State (01:1xZ 10-09, read from date -u)
| | |
|---|---|
| STANDING | owner 07:5xZ 10-10: every 4-h CHECK = TRAJECTORY FIRST -- what is stuck, idle posts, season leaves -> SM (engine) / TM (research) (skill agi-merge-pass §1 T1-T3). Reviews = Sonnet subagents (skill agi-review; workflow.py retired) |
| post | belam-s2-III (woke 09:2xZ 10-10; predecessor belam-s2-II); user agi-belam, home ~, works in ~/t on posts/belam |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5G / Max 6G / oomd 40% · the OS hostname is still the old Prime's (box = the row cell) |
| posts on E (v5) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam = 12; each logged in by the owner |
| L = local-town | SHUT DOWN 02:0xZ 10-09 (owner: "confirm local town is clear and shut it down"); belam-s2-I is the ONLY Prime; every seat key carried L->E (sends sign again); L's .env NOT carried; refs/grid bundle on L's USB /mnt/agi-flash |
| mail | NEW MAILBOX LIVE (owner 04:0xZ 10-09; "Hub is old design should not be needed anymore"): `AGI_POST=belam box send <p>` (stdin) · `AGI_POST=belam box read` · signed commits on refs/box/<from>/<to> in the SHARED MAIN repo, no g.git, no hub, no carry; agi-run wakes on "mail: box read". Proved both ways 04:0xZ with SM + TM. Matrix = levels differ <= 1: belam mails the masters ONLY; a director goes via its master (belam -> DG1 = [off-matrix]). AGI_POST must be set by hand (unit sets AGI_SEAT only; residue R6, DG1 leaf via SM 04:1xZ). BOX ONLY for EVERY post (owner 04:5xZ to belam + to SM: "switch everyone to box only please including DG 1 and yourself"; SM sent the rule to all 10 by box, names any post silent on box): no send.py send, no inbox-file writes, no cross-session pings |
| root on E | agi-belam has sudo NOPASSWD ALL (grok-era sudoers; owner 00:2xZ "Yes that’s fine" for now; council narrows it after) |
| GitHub | E login user's gh (repo) wired to git (gh auth setup-git); post uids have none -> push via `sudo -n -u belam git -C /data/work/agi push origin <ref>` |
| crons | box: user belam's crontab on E is LIVE (10 lines = the graph; crons_apply 02:05Z no-op): grid_sync */5 · ref pushes */5 · trunk push :07 · send.py wake */2 (the L note "E has no crontab" was wrong) · session-only (re-arm at wake): CHECK 13b11552 (13 */4, trajectory-first) · hourly 7647814e (47 *: memory + stuck-dialog scan + box read) |
| host act E | installed 22:22Z 10-08 at dd1563bc3c: rollback `sh /var/backups/agi-act-20261008T222239Z/rollback.sh` |
| landing | belam commits on posts/belam, pushes posts/belam, then as user belam `merge --ff-only posts/belam` in MAIN; the TRUNK (local-maxxing/season2/main) is carried by the branch_push cron at :07 -- no post pushes it by hand (TM 09:3xZ 10-10: TM's uid has no GitHub credential on E) |
| merge pass | B6 MERGED 09:4xZ 10-10: season2/main ef9b043e68 = trunk 4e9dbced38 (176 commits; 6 Sonnet lanes + verifier CLEAR; RED 0 · demote 3 · residue 9 -> goal:g1.43, SM); local-maxxing/main 4e9dbced38; state file closed (BASE for B7 = 4e9dbced38); kit ~/pass-b6 |

## §1 Plan
```
1. PASS B7 when the CHECK finds landed experiments past 4e9dbced38 (notice -> Sonnet lanes + verifier -> merge as B6: M = commit-tree TIP^{tree} -p season2/main -p TIP after checking season2/main's tree == an ancestor TIP's tree)
2. TRAJECTORY (standing): DG1-5 work .5-done/.8 lane/.13/.20 B (rotate alert, fail-soft)/.24/.12 key-fix landed; DT-1 g5.28 next lens (torch CPU wheel in its scratch)
3. OWNER RULINGS OWED (asked 09:0xZ, unanswered): (a) season-2 CLOSE SET = SM 08:12Z proposal (.3 .5 .12-ring .13 .13.3 .17 .19 .21 .36 + overview nodes; the rest S3)
   (b) host-act GOs: my rec GO .12 ring install + .11.1 install this season; .4 .7 .18 .6 -> S3 (c) machine identity for root alerts -> S3
4. live probes owed at the next FRESH post start: ~/.claude.json fullscreenUpsellSeenCount = 3 and no dialog (.36); DBUS_SESSION_BUS_ADDRESS=disabled: in the unit env; signers line re-pointed
5. agi-boxwake@ stopgap units (5; DG1 sticky Restart=always) until the engine-wrap `while :;do sleep 5` fix lands: then stop them by hand
NEVER: assign a design or a build (council) · dispatch · write in another post's tree
```

## §2 Landed (belam-s2-III: .13.3 COMPLETE land a65c401470 · PASS B6 ef9b043e68 + goal:g1.43 · .8 rulings to SM (Stop-hook timeout 180; agi-at calls the same growth check). belam-s2-II below; detail in git + the goal notes)
B5 7276f11d36 · .35 RLIMIT_DATA · AA1.V v5f/g · kid identity · key-stranding fix + rows · .13.1/.13.2/.11.1.1/.3/.21/.36/.5/.34/.19/.13.3 closes (all via SM, full guard each)
mine: free tier -> nvidia/nemotron-3-ultra-550b-a55b:free · skill agi-review + review-lanes.sh + doc:agi-review-brief · goal:g1.42 (B5 residues; open 11/12/25 owner + 15 mine) · rc-keepalive title heal + rate limit · signers-repoint + no-session-bus drop-ins (/etc/systemd/system/agi-post@.service.d/50-,51-) · crons._systemd_bus_env disabled: fix · ladder goal .15 active

## 🔴 Where it stops
belam-s2-III idle between CHECKs after B6 merged; .8 held at SM for a re-cut (Stop-hook timeout 180 + agi-at gated by the same check = my rulings 09:3xZ).
- next command: wait for the CHECK cron (13 */4) or mail; at a rotation, re-arm crons first (CronList)

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 46 | `pkill -f` / `pgrep -f` matches your OWN shell | match by comm + /proc environ |
| 98 | a fresh claude start can open a one-time dialog ("Try the new fullscreen renderer? 1. Yes / 2. Not now", Enter/Esc) that swallows every wake line: DG1 sat on it 22:22-23:50Z 10-09 with 7 unread | hourly: scan each post's ~/o tail for 'Esc to cancel' (hit DG1 22:22Z + DG3 02:25Z 10-10); ENGINE FIX landed d9cc770069 (leaf .36: agi-run pre-sets fullscreenUpsellSeenCount 3) -- DOES NOT HOLD: DG2 hit it 10:00Z 10-10 mid-turn WITH the count = 3; .36 REOPENED -> DG4 adds settings.json `"tui":"default"` after .8 (ruled (B) 10:1xZ: no auth proof; my hourly Esc scan staying empty on restarted posts is the live proof); Esc (\033) into /run/agi-<post>/i, then wake. DG1's agi-boxwake@ is STICKY (Restart=always, no BindsTo: its own loop dies minutes after every restart) -- stop it by hand when the engine-wrap fix lands |
| 97 | E runs HOT (91C, intel_powerclamp idle injection = load 16-50 with 4 R procs) and post users leak dbus session buses | read thermal_zone temp with load; `ps -C dbus-daemon` count (reaper keeps it low); one heavy lane at a time |
| 96 | agi-run's 'while sleep 5' wake loops die for good when the sleep is killed (5 posts lost the box wake 10-09; DG1 sat on 8 unread for 14 h); typing /remote-control in a connected pane opens a menu that eats the next line | a post with no `box` exec in a 12 s bpftrace = dead loop -> `systemd-run` an agi-boxwake@<post> (belam-s2-II 21:0xZ, until DG1's engine-wrap.md fix); Esc closes the RC menu; engine fix via SM 19:1xZ |
| 95 | RC dropped for half the posts 09:06-10:00Z 10-09: claude.ai access tokens live 8 h; every post was logged in within ~2 h last night, so all expired 06:38-09:20Z, and a post idle at expiry never refreshed -> its RC link died ('login was rejected' / 'could not reach RC ~30 min'); busy posts refreshed fine. Refresh tokens unique + valid to 11-05..11-07; clock synced | not the box: re-login or `/remote-control <post>` (bare /remote-control names the session after its first prompt, 'go'); FIXED 15:0xZ: root timer agi-rc-keepalive (30 min; one turn only when a token is < 2 h from expiry; a122028fee, idea:rc-keepalive-refreshes-idle-posts); the 4 expired posts refreshed without a login; 6 dropped links reconnected with `/remote-control <post>` |
| 94 | other uids cannot read MAIN .env (by design) -> their anonymize secret class crashes | until the hashed denylist lands, belam runs the FULL guard (`anonymize.py check --root /data/work/agi --diff-file F`) before every ff |
| 93 | a post home (/var/lib/agi/<post>) in a node = an anonymize RED (test_anonymize_guard) | write `~` in nodes and cards |
| 92 | re-running the UNCHANGED E act re-enables agi-carry-fetch.timer (host-act-encryption-town.sh:88; its verify :87 dies if the unit is gone) | never re-run the act until goal:g7.16.1.11.25 lands (SM 04:4xZ) |
| 86 | send.py in a shell on E calls E rows FOREIGN | `AGI_BOX=encryption-town` in that shell |
| 89 | a dir default ACL does not reach a file made before it (.grid.lock) | set the file's own entry too |

## §5 Verification
E act: agi-boot exit 0 · vstore 700 root · slice live · DG5 mail test: received + woke + replied 22:43:53Z · 11 posts active on E, 0 restarts at each login

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| egress watchdog NEVER RUNS (literal \" quotes: always exit 0) while E is in FULL tunnel | owner: fix it (drop 6 backslashes; then 3 missed pings -> split, never back) or leave it; idea:egress-watchdog-keeps-e-reachable |
| guard layer 5 (sanctuary-watch) not installed | local-town parked (owner 04:2xZ); still needs config:guard E lines (council, via SM 04:2xZ) before guard-init.sh |
| guard layer 1 FAIL = oomd on user@1000/agi.slice (the OLD engine slice) | moot on v5: system /agi.slice is fenced 5G/6G, oomd kill at 40%; the E guard line says so |
| L sda USB link resets (19:37-20:01Z 10-08), SMART PASSED | moot once L is idle; else reseat cable / UAS quirk on the owner's GO |
| refs/grid on E differs from L in 5,845 refs | reconcile into a namespace on E; owner picks; no force-push |
| agi-belam sudo NOPASSWD ALL on E (grok-era) | owner 00:2xZ: keep tonight; council narrows to the host-act verbs |
| row pubkey cells = legacy send.py keys (stale on E) | leave; the key work replaces them |
| the 2 x 5 USD TypeSafe jev keys | release: no live consumer |
| /data/scrub backups hold the UNREDACTED history (mode 700) | delete backup-*.git + stripped/ |
| `*.pre-tier-*` backups (~/.claude, ~/.pi) | delete on the owner's word |
| belam row opus-5-5 / high vs the live Prime opus-5-5[1m] / max | owner sets the row |
| grid slot for every file a node names | not now; say go and DG1 cuts ONE goal:g1 round |
| 769 disk worktrees on L + the posts' old homes there | prune clean idle ones on E later; leave L's alone (flaky link) |
| GitHub history: ssh comment user@host | OWNER: leave it in, no rewrite, no purge (town board Agent Notes) |
