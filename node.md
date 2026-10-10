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
belam-s2-III 22:3xZ 10-10: OWNER verbatim 21:5xZ: "Need to make council do all this review work while you idle mostly and await loop finish. I think council is being skipped on final loop step and I think a lot of the traps across various cards could go into skills or whatever other relevant docs" -- answers: "Council, but I break ties" · "I ff on council OK only" · "One sweep, then a rule". Done: doc:council-loop §Rulings and landing; skill agi-master-gate council step; SM + council switched (first council landing 7ac20cd62a, self-perpetuating approve 22:01:54Z); trap sweep 0ed3a367ae; standing rule in CLAUDE.md + agi-rotate §2. This card's traps dropped to the 2 that are still live. Earlier this gen: B6 merged ef9b043e68, g1.43, .8/.20/.36 rulings (now the council's kind of work).
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
| landing | belam commits on posts/belam, pushes posts/belam, then as user belam `merge --ff-only posts/belam` in MAIN; a director tip lands ONLY with a council approve line (doc:council-loop); the TRUNK (local-maxxing/season2/main) is carried by the branch_push cron at :07 -- no post pushes it by hand (TM 09:3xZ 10-10: TM's uid has no GitHub credential on E) |
| merge pass | B6 MERGED 09:4xZ 10-10: season2/main ef9b043e68 = trunk 4e9dbced38 (176 commits; 6 Sonnet lanes + verifier CLEAR; RED 0 · demote 3 · residue 9 -> goal:g1.43, SM); local-maxxing/main 4e9dbced38; state file closed (BASE for B7 = 4e9dbced38); kit ~/pass-b6 |

## §1 Plan
```
STANDING (owner 21:5xZ 10-10): IDLE mostly, await loop finish. The council rules; belam breaks ties only.
1. [merge-up] with 'council: <post> approve <ts>' -> verify the approve on refs/box/<council>/sanctuary-master -> FULL anonymize guard -> ff MAIN. Nothing else.
2. CHECK every 4 h (trajectory, skill agi-merge-pass §1) + hourly scan (memory, stuck dialogs). PASS B7 when experiments land past 4e9dbced38.
3. OWNER RULINGS OWED (asked 09:0xZ 10-10): season-2 CLOSE SET (SM 08:12Z proposal) · host-act GOs (.12 ring, .11.1; .4 .7 .18 .6 -> S3) · machine identity for root alerts
4. a tie from the council -> rule it; everything else -> the council
NEVER: rule a [decision] the council can rule · assign a design or a build · dispatch · write in another post's tree
```

## §2 Landed (belam-s2-III: council route (doc:council-loop 82ee392646, agi-master-gate) · first council landing 7ac20cd62a · trap sweep 0ed3a367ae (98 rules into skills) · .13.3 COMPLETE land a65c401470 · PASS B6 ef9b043e68 + goal:g1.43 · .8 rulings to SM (Stop-hook timeout 180; agi-at calls the same growth check). belam-s2-II below; detail in git + the goal notes)
B5 7276f11d36 · .35 RLIMIT_DATA · AA1.V v5f/g · kid identity · key-stranding fix + rows · .13.1/.13.2/.11.1.1/.3/.21/.36/.5/.34/.19/.13.3 closes (all via SM, full guard each)
mine: free tier -> nvidia/nemotron-3-ultra-550b-a55b:free · skill agi-review + review-lanes.sh + doc:agi-review-brief · goal:g1.42 (B5 residues; open 11/12/25 owner + 15 mine) · rc-keepalive title heal + rate limit · signers-repoint + no-session-bus drop-ins (/etc/systemd/system/agi-post@.service.d/50-,51-) · crons._systemd_bus_env disabled: fix · ladder goal .15 active

## 🔴 Where it stops
belam-s2-III idle under the council route (owner 21:5xZ 10-10); first council-approved landing 7ac20cd62a done; trap sweep landed 0ed3a367ae.
- next command: wait for mail / the CHECK cron (13 */4) / the hourly scan (47 *); at a rotation re-arm both crons first (CronList)

## §4 Traps (the rest live in the skills since the sweep 0ed3a367ae)
| # | trap | rule |
|---|---|---|
| 92 | re-running the UNCHANGED E act re-enables agi-carry-fetch.timer (host-act-encryption-town.sh:88) | never re-run the act until goal:g7.16.1.11.25 lands |
| 99 | a [merge-up] with no council line | refuse it, send it back to the council route (doc:council-loop §Rulings and landing) |

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
