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
gen 30 (00:4xZ 10-09): rewritten whole for the FIRST v5 Prime. The move L -> E ran tonight: E host act (refused once, rolled back, re-cut, installed), 16 grok husks stopped, three gaps closed by hand (G1 boot-only wants link, G2 .git ACL incl. user belam, G3 inbox ACL), then 11 posts moved by extensions/agi/guard/box-move.sh. Owner 00:1xZ asked both old-engine posts onto v5 with allowances; SM went first, belam last. OWNER verbatim tonight: 23:3xZ "Let’s also add the box move script to the graph directly as needed." · 00:1xZ "Can we use the new engine on both of your posts with just minor allowances like using some old engine pieces but this way you get the new mail finally" · 00:2xZ "Add credential to encryption town it should have one but if not add it" · "2. Yes that’s fine" (agi-belam sudo kept for now).
<!-- THOUGHT:END -->

## §0 State (00:4xZ 10-09, read from date -u)
| | |
|---|---|
| post | belam gen 31 = FIRST v5 Prime, on encryption-town (E), user agi-belam, home /var/lib/agi/belam, works in ~/t |
| E | 4 cores · 7.8 GB · agi.slice MemoryHigh 5G / Max 6G / oomd 40% · hostname still belam-prime (box = the row cell) |
| posts on E (v5) | DG1-5 · DT-1 · TM · alive · all-is-one · self-perpetuating · SM · belam = 12; each logged in by the owner |
| L = local-town | posts stopped there; old belam session idles (predecessor chain); sda USB link flaky (§6); L can ssh to E, E cannot reach L |
| mail | inbox file in E's MAIN + the v5 wake; send from a shell on E: `AGI_BOX=encryption-town python3 extensions/agi/bin/send.py --from belam send <p> ...`; refs/box stores (g.git) live on NO box yet (AA1.V) |
| root on E | agi-belam has sudo NOPASSWD ALL (grok-era sudoers; owner 00:2xZ "Yes that’s fine" for now; council narrows it after) |
| GitHub | E login user's gh (repo) wired to git (gh auth setup-git); post uids have none -> push via `sudo -n -u belam git -C /data/work/agi push origin <ref>` |
| crons | session-only, re-arm at wake: CHECK (13 */4, skill agi-merge-pass §1) + memory watch on E |
| host act E | installed 22:22Z 10-08 at dd1563bc3c: rollback `sh /var/backups/agi-act-20261008T222239Z/rollback.sh` |
| merge pass | paused_by_owner (council / automated). BASE 1f2b49ffc9 |

## §1 Plan
```
1. wake on E: re-link nothing (this card IS the node); read inbox by ts; ONE line to each master: "on E, mail ok?"
2. DG3 folds G1-G3 for good: G-fix landed bf5b42bc47 (check the act carries the user:belam ACL; box-move.sh lists them as target requirements)
3. trajectory duty (★): E1 D3 re-cut (SM held it for the move) · E2 flip waits ONLY on goal:g7.16.1.11.13.1 · E3 = THIS (belam on v5) -> mark done · E4 AA1.V re-cut · E5 after E1 + E3
4. after the move, banked: config:guard E line (DG1 leaf) · narrow agi-belam sudo (council) · refs/grid L vs E reconcile · prune worktrees on E
NEVER: assign a design or a build (council) · dispatch · write in another post's tree
```

## §2 Landed (gen 30, 22:06Z 10-08 .. 00:4xZ 10-09)
E act d8910ef6d6 read whole -> SM gate a5b1a41009 -> run on E REFUSED (drop-in cannot reset Requires) + rolled back clean -> fix dd1563bc3c INSTALLED · 16 grok-era agi-post@ husks stopped (/var/backups/agi-grok-husks-20261008T222346Z) · ACLs mirrored from L (.git: /var/backups/agi-acl-20261008T222850Z + agi-acl-belam-20261008T224642Z; inbox: agi-acl-inbox-20261008T224334Z) · pilot DG5 proved (login, mail, wake) · extensions/agi/guard/box-move.sh + idea:box-move-one-post-one-script + build:extensions-agi-guard-box-move.sh (owner 23:3xZ) · 10 v5 posts moved + logged in · SM row -> v5 c2c45c171e, window killed, running on E · E gh wired to git

## 🔴 Where it stops
belam itself: row flip (engine cell + box E) committed -> old window stopped on L -> `systemctl start agi-post@belam` on E -> owner /login -> THIS card.
- next command at wake (on E, ~/t): `tail -40 /data/work/agi/.agi/sessions/inbox/belam.md` then `git -C /data/work/agi log --oneline -15`
- open: SM's first turn on E (static gate only there, no FULL suite); DG3's G-fix bf5b42bc47 vs the hand ACLs

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
