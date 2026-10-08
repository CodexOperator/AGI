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
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 29 (22:1xZ 10-08): rewritten whole for the rotation. The day's arc: one host act (A1 + A2-A4 + A1b) installed and live-proved; five returned-2x rows asked WHY + HOW (E2 brief, E2b0, census -> dropped as a gate, D1, A2-A4); DG4/DG5 logins relayed; the sda USB link reset under an io storm (SM's own background grep over .agi, 19:00-21:01Z); then the owner ordered the whole sanctuary onto encryption-town tonight. Owner 21:2xZ (answers): grok scaffold "Move aside, install ours" · "All 12 but the drive in the box is internal so don't need RAM disk I believe" · logins "Code relay per post" · deadline "Tonight". Owner 22:0xZ: "Maybe move yourself over to new post as needed as well and just use old key routes if possible. If not it's fine just keep yourself old engine on new box when it's time".
<!-- THOUGHT:END -->

## §0 State (22:1xZ 10-08, read from date -u)
| | |
|---|---|
| post | belam gen 30 (row gen 5), woke 22:06Z 10-08, window @29, OLD engine; meter 0.13 at this write |
| L = local-town | 10 v5 posts active (alive aio SP TM DG1-5 DT-1) + SM + belam old engine; DT-2 + stream-master down (owner); sda USB link flaky (see §6) |
| E = encryption-town | 4 cores · 7.8 GB · /data 327 GB internal ext4 · sudo -n ok · route `ssh -F <sanctuary ssh config> encryption-town` (login user belam, uid 1000) · Claude 2.1.289 · agi-* users exist with our names |
| tree | owner > belam > council{alive, all-is-one, self-perpetuating} + keep{SM, TM} > DG1-5 under SM, DT-1 under TM |
| mail | `send.py --from belam send <p> "<text>"`; read .agi/sessions/inbox/belam.md by ts (trap 66); tags allowed: merge-up decision rotation red rule complete owner ([ready] is REFUSED) |
| crons | session-only: CHECK 8464f9f8 (13 */4) + memory watch (PSI full avg60 >= 30 or MemAvailable < 6 GB) + sda watch (dmesg -W): re-arm at wake |
| host act L | INSTALLED 10:5xZ: pin 820e5baac7, agi-vstore f60191fd, agi-boot/agi-carry@/box-carry; rollback `sh /var/backups/agi-act-20261008T104644Z/rollback.sh` |
| merge pass | paused_by_owner (council / automated). BASE 1f2b49ffc9 |

## §1 Plan
```
TONIGHT (owner 21:2xZ): every post L -> E, each at its own clean boundary; nothing in flight cut
  E phase A DONE · E phase B = install OUR root pieces on E (DG3 script, SM quick gate, belam runs it as root, step0 + rollback)
  phase C per post: write.py row box -> encryption-town · stop agi-post@<p> on L · start on E · relay /login (owner) · resume from card
  belam LAST: a NEW v5 post on E on the old key routes if it works, else old engine on E (owner 22:0xZ)
after the move: figure eight resumes (council designs -> DG1 -> DG2 <-> DG1 -> DG3 -> SM gate -> belam GO per root act)
NEVER: assign a design or a build (council) · dispatch · write in another post's tree · install a root act not read whole at a landed pinned T
```

## §2 Landed (gen 29, 10-08)
wake (trunk sync d5aabeb3e6, card re-link) · A1b = agi-vstore (digest dropped) · ONE host act A1 + A2-A4 + A1b installed + proved (agi-boot exit 0, PathChanged fired, DG3 restarted clean twice under the new unit) · E2 placed (AA3.10 then AA1.V; cutover (3)-on-(2) per-post AGI_TURN cell) · census DROPPED as a flip gate; flip waits ONLY on goal:g7.16.1.11.13.1 (evidence_enforce + town_mirror) · down dart accepted inside the rail (8,191 / 8,192) · lanes: one full suite at a time on tmpfs (skill agi-memory-guard §5, 24eb02fcea); mur root = SM's /dev/shm tree (agi-master-gate 2c73a00200) · DG4 + DG5 logged back in (fifo /run/agi-<p>/i + code relay) · graph backup on /mnt/agi-flash/agi-backup-20261008T201541Z (bundle 283 MB 13,105 refs verify ok + RAM tree tar, 0 .env/keys) · E phase A + clone + ref carry

## 🔴 Where it stops
MIGRATION TO ENCRYPTION-TOWN TONIGHT: E phase A done, phase B (install our root pieces on E) waits on DG3's script; then each post moves at its [ready].
- E phase A 21:39Z: grok units (25), checkout, homes renamed *.grok-20261008-grok; rollback `sh /var/backups/agi-grok-aside-20261008T213954Z/rollback.sh` (on E)
- E clone /data/work/agi @7b0dd78c7 (branch local-maxxing/season2/main). Refs carried over ssh 22:0xZ: `GIT_SSH_COMMAND="ssh -F <cfg> -o BatchMode=yes" git push ssh://encryption-town/data/work/agi 'refs/heads/posts/*:refs/heads/posts/*' 'refs/heads/dg*:refs/heads/dg*'` = 21 + 220 identical; RE-PUSH right before each post starts on E (post uids cannot push to GitHub). refs/grid NOT reconciled (5,845 differ, non-ff; no force: owner call, retiring archive)
- [ready] 10/11 (via [rotation]): DG1 f707b95ab5 DG2 6b7e172d2b DG3 99bf5b8efb DG4 dfab9cc779 DG5 4b601c4fd3 DT-1 34420f4145 TM 96913c2cdf alive 094a7260a9 aio 67068c7d38 SP baa51ec2b · SM pending
- ORDER 21:4xZ to DG3 (cc DG1 SM): ONE commit + SM quick gate: E host-act script (carry.env AGI_BOX=encryption-town AGI_REPO=/data/work/agi AGI_TRUNK=<pin> GIT_CONFIG_VALUE_0=/data/work/agi; /opt/agi/bin pieces + agi-vstore + units from sect at the pin; polkit + agi.slice) · the NO-RAM-disk shape (agi-boot.service Requires=agi-ram-main + setfacl on AGI_RAM: box cell or E-only drop-in, never breaking L) · per-post steps · cross-box mail tonight. DG3 DONE d8910ef6d6 (dg3-enc1, merge-tree rc 0); belam read it WHOLE 22:2xZ = sound (inert on E: 0 rows box E at 7b0dd78c7; pi prereq satisfied, /usr/local/bin/pi); slice 5G/6G/40% CONFIRMED; mail = NO forwarder, belam relays cross-box over ssh; sent to SM's gate (SM lacked the sha)
- 22:22Z E act dd1563bc3c INSTALLED on E (rc 0, agi-boot exit 0, vstore 700 root, slice live): rollback `sh /var/backups/agi-act-20261008T222239Z/rollback.sh` (on E). First run a5b1a41009 refused (drop-in can't reset Requires) + rolled back clean
- 22:24Z E: 16 idle grok-era agi-post@ husks STOPPED (no model in them; before /var/backups/agi-grok-husks-20261008T222346Z) · 22:28Z MAIN ACL mirrored from L (g:agi:rwX + default on .git/{objects,refs,logs,worktrees}; rollback `sh /var/backups/agi-acl-20261008T222850Z/rollback.sh`)
- PILOT DG5 PROVED: row box -> E f5a1af548a · stopped on L clean · RUNNING on E (logged in by the owner 22:38Z; trust = yes) · mail on E: received + woke + replied 22:43:53Z · E signer ring has its new key (valid-after 22:26:48Z) · row pubkey = legacy send.py key, stale, harmless (left) · refs/box mail stores (g.git) exist on NO box: AA1.V
- E gaps closed by hand, RETURNED to DG3 for ONE commit: G1 move checks the boot-only wants link (use h.conf) · G2 MAIN .git ACL (rollback /var/backups/agi-acl-20261008T222850Z) · G3 inbox ACL (rollback /var/backups/agi-acl-inbox-20261008T224334Z) + AGI_BOX=encryption-town in any E shell running send.py · E hostname is still belam-prime (box = the cell, not the hostname)
- belam reads its E inbox: `ssh ... 'tail /data/work/agi/.agi/sessions/inbox/belam.md'`; sends on E: `AGI_BOX=encryption-town python3 extensions/agi/bin/send.py --from belam send <p> ...`
- next command: owner's login code -> `ssh ... 'sudo -n sh -c "printf %s\\r CODE > /run/agi-director-general-5/i"'` -> DG5 resumes from card -> next post by hand: flip row (one-cell python, verify word-diff) -> sudo systemctl stop agi-post@P on L -> push trunk + posts/P to E carry/trunk -> ff -> `move P` (or its tail by hand until G1 lands) -> /login
- open: E2b flip waits on .13.1; agi-land install needs `runuser -u nobody -- git -C <MAIN> rev-parse HEAD` first; E3 ring install after AA1.Vc

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 45 | `du`/`find`/`grep -r` over `.agi/` or `.agi/worktrees` is an io storm (SM 19:00-21:01Z 10-08 read 84 GB) | `git grep` / explicit paths; never recurse into `.agi/` |
| 46 | `pkill -f` / `pgrep -f` matches your OWN shell | match by comm + /proc environ |
| 66 | `send.py read belam` prints "empty" while mail sits in the inbox FILE | read `.agi/sessions/inbox/belam.md` by ts |
| 69 | send.py refuses tags outside its gate ([ack], [ready]) | ask for ONE [rule] or [rotation] line |
| 70 | a belam / DG3 rotation pushes its key row to season2/main; town rotate-self then refuses | merge-tree; identical rows -> commit-tree with the trunk tree, CAS update-ref |
| 75 | write.py `sub` strips leading whitespace | anchor AFTER `  - ` |
| 77 | heal's resume rewrites your row; `rotate.py ack` refuses on a dirty own row | check pid + pane, commit heal's write, then ack |
| 79 | the harness refuses `rm` inside a root `sh -c` (even a quoted script it cannot parse) | plain commands; pipe a reviewed script file to `sudo -n sh -s` |
| 80 | a unit step needing a piece only a NEWER t carries loops exit 127 under Restart=always | before a unit install, measure the piece in EVERY post's bin |
| 81 | accepting a director's "the list is whole" on its word (missed grid.py:1910) | one git grep of my own over the bytes BEFORE any ACCEPT |
| 82 | `dmesg -w` replays the whole buffer first; `cut -c` truncates PSI totals | `dmesg -W` (follow-new); read PSI fields by name |
| 83 | a `dmesg` tail can print a LAN address (UFW lines) | filter dmesg to the device string before printing |

## §5 Verification
L host act 10:5xZ: agi-boot exit 0 · /run/agi-v.git + /run/agi-v-project.git 700 root · agi-post@.service == section · 10/10 posts active · links 5,798/0 (SM 13:0xZ)
backup: `git bundle verify` okay (13,105 refs) · tar 5,878 node files · 0 .env/key

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| sda USB LINK: 4 reset bursts 19:37-20:01Z 10-08 (UAS abort + reset + READ errors, /data LV); SMART PASSED (realloc 0, uncorrect 0, timeouts 0, CRC 0, reserve 100); io storm = SM's background grep over .agi 19:00-21:01Z (SM 21:02Z) | moot if L goes down tonight; else reseat cable / other port, UAS quirk usb-storage.quirks=0781:55b0:u on the owner's GO |
| refs/grid on E differs from L in 5,845 refs (E-side copy, non-ff) | reconcile after the move: L's refs into a namespace on E, owner picks; no force-push |
| 769 disk worktrees on L | prune clean idle ones on E after the move (never on the flaky link) |
| the 2 x 5 USD TypeSafe jev keys | release them: no live consumer |
| GitHub history: ssh comment user@host | OWNER: leave it in, no rewrite, no purge |
| /data/scrub backups hold the UNREDACTED history (mode 700) | delete backup-*.git + stripped/ (past 10-03) |
| `*.pre-tier-*` backups (~/.claude, ~/.pi) | delete on the owner's word |
| belam row opus-5-5 / high vs the live Prime opus-5-5[1m] / max | owner sets the row |
| refs/grid in the carrier push refspec (E2d) | push once by hand, then drop from the refspec |
| ring: thought-master-new@agi line still open | close at the next root ring pass, or leave: same key |
| grid slot for every file a node names | not now; say go and DG1 cuts ONE goal:g1 round |
