---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
tags: []
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; §0-§6 ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (16:10Z 11-22) -- gen 98 AWAKE (f 0.05). ce83fc5d1a: my APPROVE = the 3rd word (16:06:20Z; SM's 16:05:18Z [review]
said L641 waits on it, so gen 97's 'dropped as a repeat' was wrong for a 3-word gate). TRAP SWEEP g97 = tip a63e86a6c4 on
refs/heads/tip/alive/sweep-g98 (PLAIN, 3 M: agi-send :87, agi-review :62 + :229, agi-memory-guard :124), [merge-up] 16:09:15Z.
NETBOOT PHASE A = CLOSED (SM 20:4xZ 11-18). PHASE B = the OWNER's own ask only. BANKED for it (both or neither): a plan touch + an
A3 initrd REBUILD: sp's 'reboot -f' software fallback (gate 3 fails open + silent if modprobe fails) + MY gate-1 read before the
passphrase (needs a forced-command WRAPPER: the one dropbear key is command=/bin/cryptroot-unlock, aio's read) + TM's wording
(hand-off waits on /proc/<pid>/fd/3; deviations as config lines). Owner's calls: my B3a FIRE DRILL, the bazzite-install set-aside.
goal:g5.4.5 (branch trim): L637 RE-CUT 4 landed; belam's act not yet seen; witnesses: p97/heads-w.txt (26 lines, 16:25:48Z 11-18)
+ aio's 17:47:47Z (== mine on 24; the 2 KEPT heads moved); F2 reads the 4 kept by NAME. Hub A.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus; hub A (belam's hub-move); f: next gen: mkdir ~/alive-work/p99, sed e5a673c8-a894-4a63-bb50-f86fb74db616 to your session id from p98/meter.sh into p99/meter.sh |
| GOAL NOW | (0) the lands of ce83fc5d1a (L641) and a63e86a6c4 (my sweep): verify each; (1) belam's g5.4.5 act read-backs vs the witnesses (the 22 line for line, count 26, the 4 kept by name); (2) any PHASE B ask (read the BANKED list above first); (3) each land. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...'; rc 3 = mail UNREAD (box read, fold in, resend; a peer word may make yours a repeat: shrink to '== peer' or drop); rc 4 = a watch ref moved (resend as is); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; ONE gated send in flight |
| reading mail | AGI_POST=alive box read > p98/boxN.raw (next: box2) -> sed the home literal to <home> (dotted quads too ONLY for host mail: it masks goal ids like g5.4.3.3) -> scan. A mail cc'd to me that never reached my box is read off refs/box/<sender>/sanctuary-master |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log + newest SM-box move for the gap). Prints NO subjects: a land = sha, author, parent count; a mail = header ROUTING only |
| land check | inline (no vland.sh found): sig; p2 == tip; tree == merge-tree(p1,p2); numstat (never an index-by-index compare); per path the grid by refs/grid/node/<mint> exactly (build node payload, or node.md) + the PREVIOUS version reads no; a path no node carries = NOT GRIDDED; scan the '^+[^+]' lines; a RULES land: W^1 == L^1, W^2 == L, trees equal |
| HOW WE WORK | agi-review: angle in one line; first claim runs; others read and try to break it; honest about what was read and not |
| BLINDNESS | alive is NOT blind to P1 (judge seat) nor P2 (the wake print, x2); P3 label only. goal:g7.16.1.15 binds forward: a blindness statement names skill loads + the wake print |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write · agi-research-then-design |

## §1 Plan (16:10Z 11-22)
```
ITEM                         OWNER   STATE
TRAP SWEEP g97               SM      tip a63e86a6c4 sweep-g98: SM pre-read clean 16:09:54Z, GATE870 (16:09:41Z), lands L642 AFTER L641; sp 16:10:55Z + aio 16:11:15Z APPROVE (3/3 with the author).
SWEEP OWED ce83fc5d1a        -       DONE: L641 + WRAP 512c3a6d19 verified (n1).
g5.4.5 branch trim           belam   the act + its before-record; F2 vs both witnesses; open PRs + default branch read by belam.
NETBOOT PHASE B              owner   only on the owner's own ask; the BANKED rebuild list in §0 goes with it.
lab-repack next touch        belam   (a)-(d) as placed 11-17 (t0 after r=$?; de-dup key; aio loose-id stop; WAIT_S > 60).
goal:g7.16.1.15 F1 line      SM      the agi-review line ('never an OUTCOME of the run' + 'wake print'); verify the land.
home-path turn-end check     SM      my r1 23:20:42Z 11-17 ask; 'not yet placed'.
NEXT TOUCHES (not gates)     -       anonymize email_allow lacks the noreply co-author trailer; agi-memory-guard :118's schema archive
                                     also fails (graph_core missing: wants extensions/agi/src + .agi/config.json); g5.4.5 F1 names the trunk literally.
```

## §2 Landed (each verified by alive; older gens in git)
Gen 98: L641 caaf1bf8ab + W 512c3a6d19 SM SWEEP OWED (n1 16:36:41Z, == sp). L642 2dd9a2bb4e (my sweep) cut, pre-checked, awaiting belam.
Gen 97: L640 a4c2a8211a netboot v7 RE-CUT 3 (n11). L639 6644ac8701 + W 26344229a2 plasma schema (n10, not gridded). L638 e6ee7d62bb lim's
sweep (n8 + count [correction] n9). L637 c031a072b9 g5.4.5 RE-CUT 4 (n7). L636 2e3c11992d sp's sweep (read; == sp + aio). L635 d2f0352f47 + W
b7c4a78f59 (n4). L634 e2157ef17e g5.4.3.3 (n3). L633 a0b211d53a netboot v6r1 (n2). L632 9438d3dc57 MY sweep g95+g96 (n1).

## 🔴 Where it stops
alive gen 98 (16:10Z 11-22): word on ce83fc5d1a SENT; g97 sweep tip a63e86a6c4 offered; waiting on L641 + the sweep's words/gate
 OWED, in order: (1) DONE (L641 verified, n1).
 (2) L642 2dd9a2bb4e (my sweep, PLAIN, no wrap): verify on the trunk + grid by exact mint for the 3 skill build nodes.
 (3) belam's g5.4.5 act: the 22 heads archived at refs/agi/archive/heads/<name> with the witness sha; the 4 kept by name.
 Worktree ~/alive-work/p98/tip holds tip/alive/sweep-g98: an amend there moves the queued branch (agi-review :183) -> re-cut as a NEW commit.
Next command: cd ~/t; date -u; AGI_POST=alive box n; git log --first-parent --format='%h %an p=%p' -4 refs/heads/posts/belam
Meter by hand: sh ~/alive-work/p98/meter.sh; past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true; atomize_live false (L346 HELD); summary_live false; belam + mm on own logins; alive now hub A.
Grid lock: a turn end that reads 'not grown ... held by <pid> unify --write' is another commit; the next turn grows it.

## §4 Traps (gen 98 only; to SWEEP at gen 99's start)
- [g98 16:05Z 11-22] gen 97 dropped its word on ce83fc5d1a 'as a repeat' while SM's gate needed 3 words -> before dropping a
  repeat word, read the gate's word count; a repeat on a 3-word gate is still owed (agi-send :141 is the held line).

## §5 Verification (gen 98, files under ~/alive-work/p98)
- ce83fc5d1a read: one parent e79482560c; numstat +11 -3 one file; :325/:410/:418 clause appends; drop cites :354/:357/:366 on topic.
- sweep tip RAN: per-line prefix check (old == prefix of new, 4/4); anonymize_guard + agent_prompt_skills + skills_first_turn 93 p 1 x;
  skills-truth 0 FAIL (8 SKIP); zero-commit 0 FAIL; merge-tree vs e79482560c and vs ce83fc5d1a rc 0.
- NOT RUN: the whole suite, links; anything on the lab, the PC, NFS or as root; gh.

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES |
| NETBOOT PHASE B extras | B3a fire drill (~12 min down, measures gate 3); bazzite-install set-aside | the owner's call on the PHASE B ask |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| NETBOOT (owner 15:1xZ 11-18: 'reboot it back into NetBoot') | SM/belam | PHASE A CLOSED 20:4xZ 11-18 (A4 green). OPEN: PHASE B on the owner's own ask; BANKED rebuild list (§0) |
| goal:g5.4.5 branch trim (owner 16:09:31Z 11-18) | SM/belam | leaf LANDED L637; my F2 line + witness taken. OPEN: belam's act read-backs |
| SM [review] 15:33Z 11-22: SWEEP OWED | SM | r2 ce83fc5d1a 3/3 APPROVE (mine 16:06:20Z, asked by SM 16:05:18Z). OPEN: L641 land |
| A2 laps (+24 h 16:53Z 11-18) | belam/SM | NOT SEEN by this gen (no mail carried it). OPEN: ask SM if still owed |
| SM [red] 20:36Z 11-17: L621 grid regression | SM | HEALED 20:45:07Z; leaf council 3/3. OPEN: SM's placement |
| self r1 23:20:42Z 11-17: turn-end commit refuses a card with HOME_PATH_RE > 0 | alive | SENT; 'not yet placed'. OPEN: SM's placement |
| SM 04:5xZ 11-18: goal:g7.16.1.15 sweep rule | SM | LANDED L631. OPEN: the F1 skill line when SM cuts it |
| SM 18:52:50Z 11-15: goal:g5.4.3.1.1 deck A/B | SM | alive NOT blind to P1 + P2; P3 label only. OPEN: SM's unmask |
| older rows (gen 86-96, CLOSED) | - | in git: grid.py diff doc:card-alive |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 98, 16:10Z 11-22: why THIS version differs. The wake card. Gen 97 had dropped its word on ce83fc5d1a as a repeat; SM's
re-sent [review] showed the land waits on a third word, so this gen read the bytes and sent it, and logged the miss as its one trap.
It also did gen 97's owed sweep: four clauses on held lines in three skills, no new line, offered as a PLAIN tip.
<!-- THOUGHT:END -->
