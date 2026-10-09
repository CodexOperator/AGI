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
thought_session: belam-s2-I
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs; progress lives on the town board. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-s2-I 20:1xZ 10-09, at the rotation line: card whole for belam-s2-II. This gen: E3 done; mail moved to box only for every post; Doppler key into .env (wrong workspace -> PASS B5 reviews held); RC drop explained (8 h tokens on idle posts) + root keepalive; box health on E (AGI_BOX in .env restored the box-gated crons; 541 orphan dbus buses reaped + reaper; grid_sync 30 min; 92C throttling to the owner). OWNER verbatim this gen (banked on their nodes): 01:0xZ "Btw we should resume the merge pass ... do it in parallel" · 01:2xZ "Just belam-s2-I and you can restart since it’s new engine" · 04:2xZ "1. Local town will remain down for the foreseeable future ..." · 05:0xZ "Let’s lower the floor ..." · 08:0xZ "Also we use the provisioning key primarily not the api key" · "Yes let’s do that" (keepalive).
<!-- THOUGHT:END -->

## §0 State (01:1xZ 10-09, read from date -u)
| | |
|---|---|
| post | belam-s2-I (owner 01:2xZ: the generation count RESTARTS on v5; was "gen 31"; successor = belam-s2-II, no loop number) = FIRST v5 Prime, SEATED on E 00:57Z 10-09 (agi-post@belam active), user agi-belam, home ~, works in ~/t on posts/belam |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5G / Max 6G / oomd 40% · hostname still belam-prime (box = the row cell) |
| posts on E (v5) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam = 12; each logged in by the owner |
| L = local-town | SHUT DOWN 02:0xZ 10-09 (owner: "confirm local town is clear and shut it down"); belam-s2-I is the ONLY Prime; every seat key carried L->E (sends sign again); L's .env NOT carried; refs/grid bundle on L's USB /mnt/agi-flash |
| mail | NEW MAILBOX LIVE (owner 04:0xZ 10-09; "Hub is old design should not be needed anymore"): `AGI_POST=belam box send <p>` (stdin) · `AGI_POST=belam box read` · signed commits on refs/box/<from>/<to> in the SHARED MAIN repo, no g.git, no hub, no carry; agi-run wakes on "mail: box read". Proved both ways 04:0xZ with SM + TM. Matrix = levels differ <= 1: belam mails the masters ONLY; a director goes via its master (belam -> DG1 = [off-matrix]). AGI_POST must be set by hand (unit sets AGI_SEAT only; residue R6, DG1 leaf via SM 04:1xZ). BOX ONLY for EVERY post (owner 04:5xZ to belam + to SM: "switch everyone to box only please including DG 1 and yourself"; SM sent the rule to all 10 by box, names any post silent on box): no send.py send, no inbox-file writes, no cross-session pings |
| root on E | agi-belam has sudo NOPASSWD ALL (grok-era sudoers; owner 00:2xZ "Yes that’s fine" for now; council narrows it after) |
| GitHub | E login user's gh (repo) wired to git (gh auth setup-git); post uids have none -> push via `sudo -n -u belam git -C /data/work/agi push origin <ref>` |
| crons | box: user belam's crontab on E is LIVE (10 lines = the graph; crons_apply 02:05Z no-op): grid_sync */5 · ref pushes */5 · trunk push :07 · send.py wake */2 (the L note "E has no crontab" was wrong) · session-only (re-arm at wake): CHECK 541c0eb9 (13 */4, box read + launch when the key sees ws 72750376) · memory 4317a080 (47 *) · one-shots 45a8ec64 04:37Z · 4825bc4e 06:07Z |
| host act E | installed 22:22Z 10-08 at dd1563bc3c: rollback `sh /var/backups/agi-act-20261008T222239Z/rollback.sh` |
| landing | belam commits on posts/belam, pushes posts/belam, then as user belam `merge --ff-only posts/belam` in MAIN; the TRUNK push is TM's alone (skill agi-merge-pass §4; breached twice gen 31, owned to TM) |
| merge pass | RUNNING in parallel (owner 01:0xZ 10-09). PASS B5: BASE bcdb15f10f · TIP 82e6731fa7 · 17 rounds · launcher STOPPED 08:1xZ: mint 403 -- the .env key (Doppler agi/dev OPENROUTER_ADMIN) owns ws 023ce4bd, config mints into ws 72750376 (new account, 5b6342571d); the right key is likely in Doppler project `access` (needs doppler login / access token) · state MAIN .agi/sessions/prime-merge.state.json |

## §1 Plan
```
1. PASS B5 (merge pass RUNNING in parallel, owner 01:0xZ): BLOCKED on the key that owns ws 72750376 (config spawn workspace, new account 5b6342571d). E's .env key = Doppler agi/dev OPENROUTER_ADMIN, owns ws 023ce4bd -> mint 403. Likely Doppler project `access`: needs a `doppler login` on E (as belam) or an access service token from the owner. Then: swap it into .env (never printed), `sh ~/pass-b5/launch.sh` (background), verdicts.py, skill §2 steps 5-9. Kit + 17 rounds ready; TIP 82e6731fa7; RED checks clean
2. dbus leak: name the client (SM 20:2xZ asks a ROOT exec audit ~30 min: auditd / bpftrace execve on dbus-launch|dbus-daemon, parent chain + env). Reaper agi-dbus-reap holds it meanwhile; DG1 has the engine leaf (unit refuses autolaunch)
3. heat on E (92C, powerclamp): owner checks cooling; optional agi.slice CPUQuota ~300% on the owner's word
4. trajectory (★): E3 DONE (goal .17 complete) · E1 D3 re-forward returned to DG1 · E2 waits on .13.1 (conflicts with .13.2, DG4 re-cut) · E4 AA1.V re-cut returned to DG1/DG3 · E5 waits on E1
5. landings come from SM by box: before EVERY ff run the FULL anonymize guard with .env (trap 94), then `merge --ff-only <L>` in MAIN as belam; the :07 cron pushes the trunk
6. banked: config:guard E lines (DG1 .26) · narrow agi-belam sudo (council) · refs/grid L vs E reconcile · prune worktrees on E · egress watchdog fix (owner)
NEVER: assign a design or a build (council) · dispatch · write in another post's tree
```

## §2 Landed
belam-s2-I 20:1xZ: box health -- 541 orphan autolaunched session buses (post users, 1.27 GB) stopped + root reaper agi-dbus-reap (30 min; 3efda84b84); CPU 91C with powerclamp throttling (load 16-50) -> grid_sync */5 overlapped (> 6 min runs) -> every 30 min (e463b253d5); root fixes via SM
belam-s2-I 19:5xZ: E crons were refusing every box-gated job (MAIN .env had no AGI_BOX) -> AGI_BOX=encryption-town in .env + config:crons maint_gc / graph_metrics / memory_alarm(_posts) -> encryption-town (3acbd2b9a9), crontab 13 lines; mail_poll + prime_merge stay off · stall cleared: 5 posts' agi-run box-wake loops dead, DG1 sat on 8 unread 04:51-19:0xZ, woken by hand, engine leaf via SM
belam-s2-I 09:5xZ: DG4 .13.2 veto-strict ff'd 4b84358559 (full guard with .env run by me: diff ok; message 'email' = the public noreply trailer -> allow-list leaf) · .env breaks the guard for non-belam uids -> my call: hashed secret denylist (target) + loud skip (interim), leaf via SM · E FULL baseline 98 reds -> triage leaf via SM
belam-s2-I 08:0xZ: E key from Doppler (project agi, config dev, OPENROUTER_ADMIN -> MAIN .env OPENROUTER_PROVISIONING_KEY; never printed; .env belam 640 + u:agi-belam:r) -> provisioning available, `mint per-run` -> PASS B5 reviews launched · .env.example: provisioning is the main way (owner) · Doppler: belam's tokens are service tokens (belam/prd ro, agi dev/stg/prd rw in ~/.config/sanctuary/doppler as user belam); `access` project needs a doppler login or its own token

## 🔴 Where it stops
belam-s2-I rotated at its line (20:1xZ 10-09; hook "write your card, git commit it, then touch ~/.fresh;kill $PPID"). Successor = belam-s2-II (owner: generation restarts on v5; the rename lands with goal:g7.16.1.11.23, still horizon, so the RC name stays "belam").
- next command at wake (on E, ~/t): `AGI_POST=belam box read` (box is the ONLY mail route), then re-arm the session crons (CHECK 13 */4 with the ws-72750376 launch condition, memory watch 47 *)
- open at handoff: SM's dbus audit ask (plan 2) · PASS B5 key (plan 1) · DG1 working SM's 8 delivered msgs (.25/.26, D3, AA1.V, placements) · 5 posts' agi-run box-wake loops dead (trap 96): the root keepalive + hand wakes cover them until DG1's leaf

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 46 | `pkill -f` / `pgrep -f` matches your OWN shell | match by comm + /proc environ |
| 66 | `send.py read belam` prints "empty" while mail sits in the inbox FILE | read the file by ts |
| 69 | send.py refuses tags outside its gate ([ack], [ready]) | `[rotation] [ready] ...` |
| 97 | E runs HOT (91C, intel_powerclamp idle injection = load 16-50 with 4 R procs) and post users leak dbus session buses | read thermal_zone temp with load; `ps -C dbus-daemon` count (reaper keeps it low); one heavy lane at a time |
| 96 | agi-run's 'while sleep 5' wake loops die for good when the sleep is killed (5 posts lost the box wake 10-09; DG1 sat on 8 unread for 14 h); typing /remote-control in a connected pane opens a menu that eats the next line | count each post's 'sleep 5' (2 = healthy); wake by hand; Esc closes the RC menu; engine fix via SM 19:1xZ |
| 95 | RC dropped for half the posts 09:06-10:00Z 10-09: claude.ai access tokens live 8 h; every post was logged in within ~2 h last night, so all expired 06:38-09:20Z, and a post idle at expiry never refreshed -> its RC link died ('login was rejected' / 'could not reach RC ~30 min'); busy posts refreshed fine. Refresh tokens unique + valid to 11-05..11-07; clock synced | not the box: re-login or `/remote-control <post>` (bare /remote-control names the session after its first prompt, 'go'); FIXED 15:0xZ: root timer agi-rc-keepalive (30 min; one turn only when a token is < 2 h from expiry; a122028fee, idea:rc-keepalive-refreshes-idle-posts); the 4 expired posts refreshed without a login; 6 dropped links reconnected with `/remote-control <post>` |
| 94 | other uids cannot read MAIN .env (by design) -> their anonymize secret class crashes | until the hashed denylist lands, belam runs the FULL guard (`anonymize.py check --root /data/work/agi --diff-file F`) before every ff |
| 93 | a post home (/var/lib/agi/<post>) in a node = an anonymize RED (test_anonymize_guard) | write `~` in nodes and cards |
| 92 | re-running the UNCHANGED E act re-enables agi-carry-fetch.timer (host-act-encryption-town.sh:88; its verify :87 dies if the unit is gone) | never re-run the act until goal:g7.16.1.11.25 lands (SM 04:4xZ) |
| 86 | send.py in a shell on E calls E rows FOREIGN | `AGI_BOX=encryption-town` in that shell |
| 89 | a dir default ACL does not reach a file made before it (.grid.lock) | set the file's own entry too |
| 90 | a v5 post's first send.py read on E dumps the whole S1 dm backlog (no cursors carried) | judge by ts; the second read is the real one |

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
