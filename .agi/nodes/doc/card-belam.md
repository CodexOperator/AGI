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
thought_session: belam-S2-L5-XVIII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (encryption-town, v5): the ONE scratch

Owner 09-23: the card is the handoff scratch and a doc node; `HANDOFF.md` + `.agi/sessions/quorum/belam.md` are symlinks to it. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs; progress lives on the town board. Skills: agi-rotate · agi-send · agi-merge-pass · agi-verify · agi-post · agi-memory-guard · agi-node-write · agi-goal · agi-master-gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 31 (01:0xZ 10-09): the FIRST v5 Prime woke on E and closed E3 (board bc08d96bea, by the owner's 00:1xZ override, ahead of the leaf's four prerequisites, which carry as open work). Mail proved both ways: send.py read belam rc 0 + SM and TM answered 00:58Z. New on E: grid.py commit --all dies EACCES on sessions/.grid.lock (G5), reported to DG3 with the act's other gaps. OWNER verbatim tonight (gen 30): 23:3xZ "Let’s also add the box move script to the graph directly as needed." · 00:1xZ "Can we use the new engine on both of your posts with just minor allowances like using some old engine pieces but this way you get the new mail finally" · 00:2xZ "Add credential to encryption town it should have one but if not add it" · "2. Yes that’s fine" (agi-belam sudo kept for now).
<!-- THOUGHT:END -->

## §0 State (01:0xZ 10-09, read from date -u)
| | |
|---|---|
| post | belam gen 31 = FIRST v5 Prime, SEATED on E 00:57Z 10-09 (agi-post@belam active), user agi-belam, home /var/lib/agi/belam, works in ~/t on posts/belam |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5G / Max 6G / oomd 40% · hostname still belam-prime (box = the row cell) |
| posts on E (v5) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam = 12; each logged in by the owner |
| L = local-town | posts stopped there; old belam session idles (predecessor chain); sda USB link flaky (§6); L can ssh to E, E cannot reach L |
| mail | WORKS on E (read rc 0, cursors written; SM + TM ok 00:58Z) · inbox file in E's MAIN + the v5 wake; send from a shell on E: `AGI_BOX=encryption-town python3 extensions/agi/bin/send.py --from belam send <p> ...`; refs/box stores (g.git) live on NO box yet (AA1.V) |
| root on E | agi-belam has sudo NOPASSWD ALL (grok-era sudoers; owner 00:2xZ "Yes that’s fine" for now; council narrows it after) |
| GitHub | E login user's gh (repo) wired to git (gh auth setup-git); post uids have none -> push via `sudo -n -u belam git -C /data/work/agi push origin <ref>` |
| crons | session-only, ARMED gen 31: CHECK ab1ee45e (13 */4) + memory watch 4317a080 (47 *); re-arm at every wake |
| host act E | installed 22:22Z 10-08 at dd1563bc3c: rollback `sh /var/backups/agi-act-20261008T222239Z/rollback.sh` |
| landing | belam commits on posts/belam, then as user belam: `merge --ff-only posts/belam` in MAIN + push trunk + posts/belam (bc08d96bea) |
| merge pass | paused_by_owner (council / automated). BASE 1f2b49ffc9 |

## §1 Plan
```
1. DONE gen 31: woke on E, mail proved, one line to each master (SM + TM answered), crons armed
2. DG3 folds the act's gaps for good: [red] sent 01:0xZ -- (a) u:belam on MAIN .git (b) G4 comms/dm ACL (c) G5 sessions/.grid.lock -> await its numbers line
3. trajectory duty (★): E3 DONE (board bc08d96bea; DG1 asked to flip goal:g7.16.1.11.17) · E1 D3 re-cut (SM held it for the move) · E2 flip waits ONLY on goal:g7.16.1.11.13.1 · E4 AA1.V re-cut · E5 now waits only on E1
4. SM: two gates await mur (6ce18b1b93 lane 29/0; 10b683d7e5 merge-tree rc 0 on c70e3ef313); nothing landed
5. after the move, banked: config:guard E line (DG1 leaf) · narrow agi-belam sudo (council) · refs/grid L vs E reconcile · prune worktrees on E
NEVER: assign a design or a build (council) · dispatch · write in another post's tree
```

## §2 Landed
gen 31 (00:57Z .. 01:0xZ 10-09): board E3 -> DONE bc08d96bea, trunk ff + pushed · mail check to SM + TM (both ok) · [rule] DG1 flip E3 leaf · [red] DG3 act gaps (a)-(c) · CHECK + memory crons armed
gen 30 (22:06Z 10-08 .. 00:4xZ 10-09):
E act d8910ef6d6 read whole -> SM gate a5b1a41009 -> run on E REFUSED (drop-in cannot reset Requires) + rolled back clean -> fix dd1563bc3c INSTALLED · 16 grok-era agi-post@ husks stopped (/var/backups/agi-grok-husks-20261008T222346Z) · ACLs mirrored from L (.git: /var/backups/agi-acl-20261008T222850Z + agi-acl-belam-20261008T224642Z; inbox: agi-acl-inbox-20261008T224334Z) · pilot DG5 proved (login, mail, wake) · extensions/agi/guard/box-move.sh + idea:box-move-one-post-one-script + build:extensions-agi-guard-box-move.sh (owner 23:3xZ) · 10 v5 posts moved + logged in · SM row -> v5 c2c45c171e, window killed, running on E · E gh wired to git

## 🔴 Where it stops
belam is ON v5 on E and idle-waiting on three numbers lines: DG1 (E3 leaf flipped), DG3 (act gaps a-c), SM (its two gates through mur).
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
| 85 | a post user cannot add its worktree on a fresh box | MAIN .git ACL g:agi + u:belam rwX + defaults, BEFORE the first start |
| 86 | send.py in a shell on E calls E rows FOREIGN | `AGI_BOX=encryption-town` in that shell |
| 87 | ~1 in 3 OAuth codes fail ("OAuth error") | `box-move.sh url <p>` again; ONE fresh link to the owner at a time |
| 88 | ssh L -> E setup takes ~12 s | timeouts >= 40 s |
| 89 | `grid.py commit --all` on E: EACCES on sessions/.grid.lock (G5) | git commit alone this gen; DG3 folds the ACL |
| 90 | a v5 post's first send.py read on E dumps the whole S1 dm backlog (no cursors carried) | judge by ts; the second read is the real one |

## §5 Verification
E act: agi-boot exit 0 · vstore 700 root · slice live · DG5 mail test: received + woke + replied 22:43:53Z · 11 posts active on E, 0 restarts at each login

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
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
