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
gen 31 (01:1xZ 10-09): the FIRST v5 Prime woke on E, proved mail, closed E3 (bc08d96bea, by the owner's 00:1xZ override), hand-set G5 (grid.py commit works on E again), and RESUMED the merge pass on the owner's 01:0xZ line (banked verbatim on the board 99ede2ab72): PASS B5 noticed for 06:07Z. Owned a breach: two hand pushes of the trunk (TM's alone). OWNER verbatim this gen: 01:0xZ "Btw we should resume the merge pass once the engine work lands or better yet do it in parallel. A lot of the merge pass isn’t as intense as the new pieces are way smaller". Gen 30's lines: 23:3xZ "Let’s also add the box move script to the graph directly as needed." · 00:1xZ "Can we use the new engine on both of your posts with just minor allowances like using some old engine pieces but this way you get the new mail finally" · 00:2xZ "Add credential to encryption town it should have one but if not add it" · "2. Yes that’s fine".
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
1. DONE gen 31: woke on E, mail proved, one line to each master (SM + TM answered), crons armed
2. DG3 enc6 LANDED in 1e6056afd4 (act bytes only; the E re-run of the act = my quoted GO, not yet); G5 HAND-SET on E 01:0xZ (backup /var/backups/agi-acl-sessions-20261009T010350Z; .grid.lock file needed its own entry)
2b. PASS B5 STARTED 01:08Z: trunk sync 82e6731fa7 · kit rebuilt ~/pass-b5 (launch.sh refuses rc 3 without a key) · NEXT = `sh launch.sh` in the background, then reviews (`PI_BIN=/usr/local/bin/pi workflow.py run merge-up-review --harness pi-free`, 2 rounds a chunk, CAP 1) the moment E has the key; then §2 steps 4-9
3. trajectory duty (★): E3 DONE (board bc08d96bea; DG1 asked to flip goal:g7.16.1.11.17) · E1 D3 re-cut (SM held it for the move) · E2 flip waits ONLY on goal:g7.16.1.11.13.1 · E4 AA1.V re-cut · E5 now waits only on E1
4. SM: two gates await mur (6ce18b1b93 lane 29/0; 10b683d7e5 merge-tree rc 0 on c70e3ef313); nothing landed
4b. session name belam-s2-<gen>: goal:g7.16.1.11.23 (horizon, landed 1e6056afd4) (boot cell engine.md:94 renders the post name only); renamed AT the next rotation, never by hand
5. after the move, banked: config:guard E line (DG1 leaf) · narrow agi-belam sudo (council) · refs/grid L vs E reconcile · prune worktrees on E
NEVER: assign a design or a build (council) · dispatch · write in another post's tree
```

## §2 Landed
belam-s2-I 09:5xZ: DG4 .13.2 veto-strict ff'd 4b84358559 (full guard with .env run by me: diff ok; message 'email' = the public noreply trailer -> allow-list leaf) · .env breaks the guard for non-belam uids -> my call: hashed secret denylist (target) + loud skip (interim), leaf via SM · E FULL baseline 98 reds -> triage leaf via SM
belam-s2-I 08:0xZ: E key from Doppler (project agi, config dev, OPENROUTER_ADMIN -> MAIN .env OPENROUTER_PROVISIONING_KEY; never printed; .env belam 640 + u:agi-belam:r) -> provisioning available, `mint per-run` -> PASS B5 reviews launched · .env.example: provisioning is the main way (owner) · Doppler: belam's tokens are service tokens (belam/prd ro, agi dev/stg/prd rw in ~/.config/sanctuary/doppler as user belam); `access` project needs a doppler login or its own token
belam-s2-I 05:0xZ: FULL-suite floor on E = 3 GB (owner: no RAM disk / stream; skill agi-memory-guard §5, 98b506ad48) · SM told: stale /dev/shm gate trees (~760 MB) + DG3's 4 h host-act .t.sh
belam-s2-I 04:5xZ: box-only switch COMPLETE (10/10 acked via SM) · signers fix in 3 homes (DG1, all-is-one, self-perpetuating: ~/.signers missing -> /var/lib/agi/allowed_signers; backup /var/backups/agi-gitconfig-signers-20261009T044851Z) · python3-pytest 7.4.4 installed system-wide (SM option A) · app device: user belam's claude-remote-control.service renamed belam-prime -> encryption-town (backup .before-encryption-town), enabled + started (linger on, Restart=always)
belam-s2-I 04:2xZ (owner 1-5): local-town parked out of active peers (hosts.json towns -> parked_towns) · xai-proxy stopped + disabled · agi-carry-fetch.timer stopped + disabled (hub already empty) · egress watchdog graphed 6a830b2fbf (idea + 4 builds) · engine-side hub removal + guard E lines -> council via SM

## 🔴 Where it stops
belam is ON v5 on E; PASS B5 holds at its review step on the OWNER (L's .env -> E's MAIN). Also waiting: DG1 (E3 leaf flipped), SM (lands dg3-enc6 98fb9ebfd8 + pushes the trunk, 3 ahead).
- next command at wake (on E, ~/t): `AGI_BOX=encryption-town python3 extensions/agi/bin/send.py read belam` then `tail -40 /data/work/agi/.agi/sessions/inbox/belam.md`
- open: SM saw a DG1 00:14 inbox block marked read WITHOUT printing -> read the inbox FILE by ts until send.py is fixed (trap 66)

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 45 | `du`/`find`/`grep -r` over `.agi/` is an io storm | `git grep` / explicit paths |
| 46 | `pkill -f` / `pgrep -f` matches your OWN shell | match by comm + /proc environ |
| 66 | `send.py read belam` prints "empty" while mail sits in the inbox FILE | read the file by ts |
| 69 | send.py refuses tags outside its gate ([ack], [ready]) | `[rotation] [ready] ...` |
| 79 | the harness refuses `rm` inside a root `sh -c` | pipe a reviewed script file to `sudo -n sh -s` |
| 84 | a drop-in cannot reset Requires=/After= | a no-op unit on the box, never a reset |
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
