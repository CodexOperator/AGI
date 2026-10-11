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
thought_session: belam-s2-IV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs; progress lives on the town board. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s2-IV 09:4xZ 10-11, woke: crons re-armed (CHECK ab926671, hourly 460e3c20); landed SM's council-approved re-merge 2387a51ce7 (alive approve 09:37Z; blob == DG3 76644978bf; guard + falsifier clean); DG5 restarted (plan 7 DONE). belam-s2-III's gen, below, unchanged. belam-s2-III 09:3xZ 10-11, at the rotation line: card whole for belam-s2-IV. That gen: council route stood up on the owner's order (rulings to the council, belam ffs council-approved tips only + the secret guard + the origin falsifier, re-read the approver's ref before every ff); trap sweep (98 rules into skills); loop end closed (12 outcomes, 3 bigger outcomes, 3 overviews, 24cdb55824); agi-quiet-watch timer; AGI_POST drop-in + every post restarted (tui, .38, .20 alert live on 10 of 11); 657 archive refs restored from the pre-move bundle; memguard A1 installed on owner GO. OWNER verbatim this gen: "Need to make council do all this review work while you idle mostly and await loop finish. I think council is being skipped on final loop step and I think a lot of the traps across various cards could go into skills or whatever other relevant docs" · "Council, but I break ties" · "I ff on council OK only (Recommended)" · "One sweep, then a rule (Recommended)" · "Hmm your check missed the team being hung ... Maybe an automated check if all posts are quiet for 5 mins and no process send a mail alert to SM" · "Bad we fix the post issue agi seat shouldn't be used anymore unless absolutely needed. The post should include all relevant info including box location" · "Yes let’s do it thank you" (memguard A1 + A2).
<!-- THOUGHT:END -->

## §0 State (09:4xZ 10-11, read from date -u)
| | |
|---|---|
| STANDING | owner 07:5xZ 10-10: every 4-h CHECK = TRAJECTORY FIRST -- what is stuck, idle posts, season leaves -> SM (engine) / TM (research) (skill agi-merge-pass §1 T1-T3). Reviews = Sonnet subagents (skill agi-review; workflow.py retired) |
| post | belam-s2-IV (woke 09:3xZ 10-11; predecessor belam-s2-III); user agi-belam, home ~, works in ~/t on posts/belam. belam's OWN unit still runs pre-.38 pieces + no AGI_POST in env until this restart (set AGI_POST=belam by hand) |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5G / Max 6G / oomd 40% · the OS hostname is still the old Prime's (box = the row cell) |
| posts on E (v5) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam = 12; each logged in by the owner |
| L = local-town | SHUT DOWN 02:0xZ 10-09 (owner: "confirm local town is clear and shut it down"); belam-s2-I is the ONLY Prime; every seat key carried L->E (sends sign again); L's .env NOT carried; refs/grid bundle on L's USB /mnt/agi-flash |
| mail | NEW MAILBOX LIVE (owner 04:0xZ 10-09; "Hub is old design should not be needed anymore"): `AGI_POST=belam box send <p>` (stdin) · `AGI_POST=belam box read` · signed commits on refs/box/<from>/<to> in the SHARED MAIN repo, no g.git, no hub, no carry; agi-run wakes on "mail: box read". Proved both ways 04:0xZ with SM + TM. Matrix = levels differ <= 1: belam mails the masters ONLY; a director goes via its master (belam -> DG1 = [off-matrix]). AGI_POST must be set by hand (unit sets AGI_SEAT only; residue R6, DG1 leaf via SM 04:1xZ). BOX ONLY for EVERY post (owner 04:5xZ to belam + to SM: "switch everyone to box only please including DG 1 and yourself"; SM sent the rule to all 10 by box, names any post silent on box): no send.py send, no inbox-file writes, no cross-session pings |
| root on E | agi-belam has sudo NOPASSWD ALL (grok-era sudoers; owner 00:2xZ "Yes that’s fine" for now; council narrows it after) |
| GitHub | E login user's gh (repo) wired to git (gh auth setup-git); post uids have none -> push via `sudo -n -u belam git -C /data/work/agi push origin <ref>` |
| crons | box: user belam's crontab on E is LIVE (10 lines = the graph; crons_apply 02:05Z no-op): grid_sync */5 · ref pushes */5 · trunk push :07 · send.py wake */2 (the L note "E has no crontab" was wrong) · session-only (re-arm at wake): CHECK ab926671 (13 */4, trajectory-first) · hourly 460e3c20 (47 *: memory + stuck-dialog scan + box read) |
| host act E | installed 22:22Z 10-08 at dd1563bc3c: rollback `sh /var/backups/agi-act-20261008T222239Z/rollback.sh` |
| landing | belam commits on posts/belam, pushes posts/belam, then as user belam `merge --ff-only posts/belam` in MAIN; a director tip lands ONLY with a council approve line (doc:council-loop); the TRUNK (local-maxxing/season2/main) is carried by the branch_push cron at :07 -- no post pushes it by hand (TM 09:3xZ 10-10: TM's uid has no GitHub credential on E) |
| merge pass | B6 MERGED ef9b043e68 (10-10); state BASE for B7 = 4e9dbced38 (trunk now ~350 commits past, 0 experiment files -> B7 not due by rule; the season close needs the owner's word) |

## §1 Plan
```
STANDING (owner 21:5xZ 10-10): IDLE mostly, await loop finish. The council rules; belam breaks ties only.
1. [merge-up] with 'council: <post> approve <ts>' -> verify the approve on refs/box/<council>/sanctuary-master -> FULL anonymize guard -> ff MAIN. Nothing else.
2. CHECK every 4 h (trajectory, skill agi-merge-pass §1) + hourly scan (memory, stuck dialogs). PASS B7 when experiments land past 4e9dbced38.
3. OWNER RULINGS OWED: season-2 CLOSE (run B7 + the morals review now? asked 04:1xZ 10-11, after the loop end closed 24cdb55824) · host-act GOs (.12 ring, .11.1) · claude pin (§6) · host-identity lane (§6) · publish the 657 archive refs (§6)
4. a tie from the council -> rule it; everything else -> the council
5. goal:g7.16.1.11.37 host side DONE 10:2xZ 10-11 (my GOs): STEP 1 re-render = carry.env pin c70e3ef313 -> b4e1afaf04 (backup /etc/agi/carry.env.pre-pin-20261011T101540Z; measured first in scratch: only agi-post@.service changed). STEP 2 witness = DG4's LIVE lane 95847b8fa6 run in 3 restarted posts' envs (TM, self-perpetuating, DG2): only f6c red. STEP 3 = the 3 drop-ins moved to /var/backups/agi-dropins-retired-20261011T102822Z + daemon-reload; HOSTDIR lane 0 FAIL (f6c green); their sources -> extensions/agi/guard/deprecated/ in the same commit (agi-signers-repoint stays: the unit calls it). Rollback: put the 3 files back + daemon-reload; the pin backup restores the old unit. The other 9 posts take the new unit at their next start (l1 green then).
6. MEMGUARD A2 LIVE (owner GO 08:43Z): PROVEN 10:13Z on b4e1afaf04; RE-STAGED 10:53Z on c04b4988f3 (DG1's one-fetch / young-skip / clear-on-good) -> PROVEN, a2.since 10:13:05Z kept. A re-stage by hand = save ~/memguard-A0/a2.since (A0 rm -rf's the stage) -> A0 on the LANDED sha -> restore it -> sudo systemctl stop agi-memguard (a1.undo refuses an active unit) -> a1.undo -> a1 -> a1.proof -> a2.sh -> SHA=<sha> a2.proof.sh; memguard-restage.sh landed cf8219a95e but is NOT to be used until DG1's race fix lands (council 11:11Z: a pid stopped between its check and the stop stays frozen). Undo: sh ~/memguard-A0/src/extensions/agi/boxkit/memguard-a2.undo.sh
7. restarts on E this gen: DG5 09:4xZ, thought-master 10:16Z (new unit) -- both active, -c, no dialog. The idle test for any later restart: transcript >= 60 s AND no non-baseline proc in the unit cgroup (baseline: agi-run, agi-track, sleep, script, strace, grep, awk, claude, gk mcp/npm/node, dbus-daemon, their sh wrappers) AND MemAvailable >= 2.5 GB; then `sudo systemctl restart agi-post@<p>`; then scan the pane log ~<p>/o (grep -a) for 'Esc to cancel'
8. /dev/shm + SWAP: red 09:56Z (SwapFree 248 kB; agi.slice at MemoryHigh; ~2.2 GB of tmpfs paged out) CLOSED 10:00Z: DG1 + DG4 freed /dev/shm (18 MiB used) -> SwapFree 2.3 GB, agi.slice 4412 MiB, its swap 1214 MiB (idle posts' anon, normal). Re-read SwapFree + /dev/shm at each hourly scan
9. .32 WAKE UNIT DONE 11:4xZ 10-11 (my GO, trunk ee5b59605a): measured first -- 0 live agi-run box loops in all 12 units (every post but the 7 transients had NO wake); carry.env pin b4e1afaf04 -> ee5b59605a (backup /etc/agi/carry.env.pre-pin-20261011T114855Z; pin since 12:08Z = dd025b19f2, backup ...-20261011T120833Z, .37's [trunk-unreadable] ExecCondition) re-projected agi-boxwake@.service + 12 per-post h.conf + agi-post@ Wants=; the 7 transients stopped and their files moved to /var/backups/agi-boxwake-transients-20261011T114940Z (a plain stop restarts them while Wants= names the unit); agi-boxwake@<p> active x12 from the template, NRestarts 0; live wake ~4 s on TM and SM. Rollback: the pin backup + systemd-run from the transient backup. Hourly scan: `systemctl is-active agi-boxwake@<p>` for every post
NEVER: rule a [decision] the council can rule · assign a design or a build · dispatch · write in another post's tree
```

## §2 Landed (belam-s2-III: council route (doc:council-loop 82ee392646, agi-master-gate) · first council landing 7ac20cd62a · trap sweep 0ed3a367ae (98 rules into skills) · .13.3 COMPLETE land a65c401470 · PASS B6 ef9b043e68 + goal:g1.43 · .8 rulings to SM (Stop-hook timeout 180; agi-at calls the same growth check). belam-s2-II below; detail in git + the goal notes)
B5 7276f11d36 · .35 RLIMIT_DATA · AA1.V v5f/g · kid identity · key-stranding fix + rows · .13.1/.13.2/.11.1.1/.3/.21/.36/.5/.34/.19/.13.3 closes (all via SM, full guard each)
mine: free tier -> nvidia/nemotron-3-ultra-550b-a55b:free · skill agi-review + review-lanes.sh + doc:agi-review-brief · goal:g1.42 (B5 residues; open 11/12/25 owner + 15 mine) · rc-keepalive title heal + rate limit · signers-repoint + no-session-bus drop-ins (/etc/systemd/system/agi-post@.service.d/50-,51-) · crons._systemd_bus_env disabled: fix · ladder goal .15 active

## 🔴 Where it stops
belam-s2-IV idle under the council route (MAIN ee5b59605a + this card); host acts done this gen: memguard A2 (re-staged c04b4988f3), .37 re-render + drop-in retire, .32 wake template. Owed: .38.1 MAIN install GO when DG3's piece lands; memguard re-stage by hand when a template change is owed (restage.sh waits for DG1's race fix); owner rulings (plan 3).
- next command: wait for mail (`AGI_POST=belam box read`) / the CHECK cron (13 */4) / the hourly scan (47 *); at a rotation re-arm both crons first (CronList)

## §4 Traps (the rest live in the skills since the sweep 0ed3a367ae)
| # | trap | rule |
|---|---|---|
| 92 | re-running the UNCHANGED E act re-enables agi-carry-fetch.timer (host-act-encryption-town.sh:88) | never re-run the act until goal:g7.16.1.11.25 lands |
| 99 | a [merge-up] with no council line | refuse it, send it back to the council route (doc:council-loop §Rulings and landing) |

| 100 | the whole team idle at their prompts, 0 unread, each waiting on another (02:3xZ 10-11: SM idle after a compaction; council waiting on SM's bigger outcomes) -- the hourly dialog scan cannot see it | root timer agi-quiet-watch (1 min; extensions/agi/guard/quiet-watch): every post but belam quiet >= 5 min with no claude descendant -> box [quiet] to SM, then <= 1 per 30 min until a post is busy; `journalctl -t agi-quiet-watch` |

## §5 Verification
E act: agi-boot exit 0 · vstore 700 root · slice live · DG5 mail test: received + woke + replied 22:43:53Z · 11 posts active on E, 0 restarts at each login

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| root-guard mail identity (asked of the owner 09:0xZ 10-10 as (c), my rec S3): council 06:0xZ 10-11 ruled ONE host identity per box (<box>-host) for every root guard (memguard, heal, alarms, my agi-quiet-watch), mailing only the box's master + belam, one key per author; box's matrix needs a harness value or ONE named rule for host rows, chosen in the lane. Interim: red lines to SM's + belam's ~/.notice | lane it when the owner says go (it is a key/identity round = my HOLD lane); until then the guards stay keyless |
| 657 refs/archive/worktrees/* imported into MAIN 03:1xZ 10-11 from the pre-move bundle (/mnt/agi-flash/agi-backup-20261008T201541Z/agi-all.bundle, verify ok); origin holds 0 | owner: publish them to origin (public) or keep them local-only; rec keep local + the bundle as the second copy |
| CLAUDE UPGRADE = every post's hooks off (council 00:59Z 10-11, leaf under .36): every post runs /usr/local/bin/claude -> ~belam/.local/bin/claude (owner user belam's own install, moved 10-09 14:46; 4 versions on disk); posts set DISABLE_AUTOUPDATER=1 but the owner's 2 RC sessions as belam do not (~/.claude.json autoUpdates false only). An upgrade that rejects settings.json 'tui' skips the WHOLE file -> no meter/turn/.8 gate on any post, silently | owner: pin the posts to a root-owned copy (/opt/agi/claude-2.1.295 + /usr/local/bin/claude -> it) so the owner's updates never reach the posts; move the pin only after the NEW BINARY passes: .36's scratch-HOME probe under script (no fullscreen dialog, alternate_on 0) AND goal:g7.16.1.11.36.1's hooks-loaded proof (agi-brief stamps within N s) on that version; settings-tui.t.sh is only the text check beside them (council correction 01:0xZ 10-11: the text lane passes on exactly the upgrade that breaks us) |
| egress watchdog NEVER RUNS (literal \" quotes: always exit 0) while E is in FULL tunnel | owner: fix it (drop 6 backslashes; then 3 missed pings -> split, never back) or leave it; idea:egress-watchdog-keeps-e-reachable |
| guard layer 5 (sanctuary-watch) not installed + a STRAY /data/work/.sanctuary/guard/guard.env (Sep 25) and an OLD guard-init.sh copy beside it: since c84628156d (09:5xZ 10-11) guard-init DIES on that guard.env by design; the old copy would bypass the landed code. Until the act: nobody runs sudo guard-init (SM 09:5xZ) | owner GO for guard-init = ONE act: mv guard.env + the old guard-init.sh -> *.retired-<ts> (never rm), then install layer 5 (needs config:guard E lines first, council via SM) |
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
