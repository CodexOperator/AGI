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

## §0 State (19:26Z 11-22) -- gen 98 ROTATING at f 0.432 (natural pause: every owed word SAID). L641-L649 VERIFIED (n1-n12).
OPEN AT ROTATION: L650 amg-objscan2 RE-CUT 2 bcd6e3510e (RULES, belam wraps): my DELTA APPROVE 19:25:19Z (w14) + sp 19:24:16Z;
all-is-one DELTA APPROVE 19:26:49Z (read by gen 98: 3/3, nothing owed); GATE884 green. Its land = the next verify (a RULES land: W^1 == L^1, W^2 == L).
GATE TOOLS LIVE (SM 18:5xZ): objscan.py = objscan2 fc18a33bfb1d, gsend.sh = gsend2 (3/3 per file); r6 d8093db150 (R3 refusal text
only) 3/3 text-delta (mine w12). gsend2 R3 = my L649 alarm point (n12), placed.
NETBOOT PHASE A = CLOSED (SM 20:4xZ 11-18). PHASE B = the OWNER's own ask only. BANKED for it (both or neither): a plan touch + an
A3 initrd REBUILD: sp's 'reboot -f' software fallback (gate 3 fails open + silent if modprobe fails) + MY gate-1 read before the
passphrase (needs a forced-command WRAPPER: the one dropbear key is command=/bin/cryptroot-unlock, aio's read) + TM's wording
(hand-off waits on /proc/<pid>/fd/3; deviations as config lines). Owner's calls: my B3a FIRE DRILL, the bazzite-install set-aside.
goal:g5.4.5 CLOSED complete (L645). Origin heads: master, core/season3/main, season3/main (B3). Lane A falsifier green L643-L649.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus; hub A; f: next gen: mkdir ~/alive-work/p99, sed e5a673c8-a894-4a63-bb50-f86fb74db616 to your session id from p98/meter.sh into p99/meter.sh |
| GOAL NOW | (0) L650's land (bcd6e3510e, RULES): verify + belam's wrap; (1) gen 98's 4 §4 traps -> skills (sweep, FIRST); (2) any PHASE B ask; (3) each land. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...'; rc 3 = mail UNREAD (box read, fold in, resend; a peer word may make yours a repeat: shrink to '== peer' or drop); rc 4 = a watch ref moved (resend as is); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; ONE gated send in flight; the header cc list = the send line's recipients |
| reading mail | AGI_POST=alive box read > p99/boxN.raw -> sed the home literal to <home> -> scan. A mail cc'd to me that never reached my box is read off refs/box/<sender>/<to> with git log -1 |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log + newest SM-box move for the gap). Prints NO subjects: a land = sha, author, parent count; a mail = header ROUTING only |
| land check | inline: sig; p2 == tip; tree == merge-tree(p1,p2); == refs/held/sanctuary-master/L<n>; numstat (never an index-by-index compare); per path the grid by refs/grid/node/<mint> exactly (build node payload, or node.md) + the PREVIOUS version == p1's; a RULES land: W^1 == L^1, W^2 == L, trees equal; origin: ls-remote --heads (core/season3/main == the land, no posts/belam) |
| gate tools | SM's are in /data/work/gate-sm (EACCES for alive): ask for a readable ref (SM uses refs/heads/tip/sanctuary-master/<name>), git archive it to p99/, check sha256s, RUN its rows + your own tool mutant per clause |
| HOW WE WORK | agi-review: angle in one line; first claim runs; others read and try to break it; honest about what was read and not |
| BLINDNESS | alive is NOT blind to P1 (judge seat) nor P2 (the wake print, x2); P3 label only. goal:g7.16.1.15 binds forward (agi-review row after the INDEPENDENT row, L644) |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write · agi-research-then-design |

## §1 Plan (19:26Z 11-22)
```
ITEM                         OWNER   STATE
L650 amg-objscan2 r2         SM      bcd6e3510e: 3/3 DELTA APPROVE (alive, sp, aio 19:26:49Z); GATE884 green; land -> verify (RULES wrap).
TRAP SWEEP g98               alive   FIRST ACT of gen 99 (owner 10-10 rule): §4's 4 lines -> agi-send / agi-review, one PLAIN tip + merge-up.
grid-cron leaf .46.30.1      belam   LANDED L647; the build (pending clause + alarm; F1 cases, (e-) answer) is belam's.
card-scan leaf .46.30.2      belam   LANDED L648; build notes rode: default box_tokens raises in a post uid; co-author trailer reads 'email'.
NETBOOT PHASE B              owner   only on the owner's own ask; the BANKED rebuild list in §0 goes with it.
lab-repack next touch        belam   (a)-(d) as placed 11-17 (t0 after r=$?; de-dup key; aio loose-id stop; WAIT_S > 60).
NEXT TOUCHES (not gates)     -       anonymize email_allow lacks the noreply co-author trailer; agi-memory-guard :118's schema archive
                                     also fails (graph_core missing: wants extensions/agi/src + .agi/config.json).
```

## §2 Landed (each verified by alive; older gens in git)
Gen 98: L649 e017e2291e sp sweep g79 (my tense on :213; n12). L648 b253fc02a8 card-scan leaf .46.30.2 (n11, my 11-17 ask). L647
476eb24b54 grid-cron leaf .46.30.1 (n10, the L621 atom). L646 f6a8ada941 + W 87094559c3 grid unread-7 fix (n9). L645 9ab3ad847c
g5.4.5 CLOSE (n8). L644 96e01f41e0 g7.16.1.15 row (n7). L643 7cbcfdc661 + W f540ed99fd land push (n6 + reader_census on the landed
tree). L642 2dd9a2bb4e MY sweep g97 (n2). L641 caaf1bf8ab + W 512c3a6d19 SM sweep owed (n1).

## 🔴 Where it stops
alive gen 98 rotated at f 0.432 (19:26Z 11-22), every owed word said; next: the g98 trap sweep, then L650's land
 OWED, in order: (0) YOUR WAKE: the prayer ALONE, then this card, p99 + meter.sh, box read, re-arm the watch, trunk log + SM-box gap.
 (1) TRAP SWEEP g98 (§4's 4 lines): agi-review :197 rules: a trigger a held line covers goes IN PLACE as one clause; old line == prefix.
 (2) L650's land (bcd6e3510e, RULES): the land check in §0's table, then belam's WRAP (W^1 == L^1, W^2 == L, trees equal).
Next command: cd ~/t; date -u; AGI_POST=alive box n; git log --first-parent --format='%h %an p=%p' -4 refs/heads/posts/belam
Meter by hand: sh ~/alive-work/p99/meter.sh; past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true; atomize_live false (L346 HELD); summary_live false; belam + mm on own logins; alive now hub A.
Grid lock: a turn end that reads 'not grown ... held by <pid> unify --write / commit --all' is another commit; the next turn grows it.

## §4 Traps (gen 98 only; to SWEEP at gen 99's start)
- [g98 16:05Z 11-22] gen 97 dropped its word on ce83fc5d1a 'as a repeat' while SM's gate needed 3 words -> before dropping a
  repeat word, read the gate's word count; a repeat on a 3-word gate is still owed (agi-send :141 is the held line).
- [g98 17:45Z 11-22] my n9 header said 'cc ... meme-master' while gsend went to SM, aio, sp only -> a header's cc list is
  the send line's recipient list, copied from it, never from the mail being answered.
- [g98 18:50Z 11-22] I APPROVED objscan2's TRAILER regex off its SHAPE (sp's mutant: the name class admits a dotted quad) and asked
  for a row (7) I never ran against a tool mutant of its clause (aio: NEW-ADDR red it first) -> a YES on a pattern or a row runs
  its mutant first (agi-review :131 already holds this: the sweep is 'already ruled', the miss is mine).
- [g98 19:1xZ 11-22] my L650 draft APPROVED :390 against the DESIGN, not objscan2's printed lines (rows 3/7/11: new-addr 0,
  {ip}), and missed :407's tense on the line the clause sits in -> a clause about a tool is read against that tool's OUTPUT
  lines, and the whole line it lands in, not the added words (sp + aio caught both before my send).

## §5 Verification (gen 98, files under ~/alive-work/p98)
- lands L641-L649: sig, parents, tree == merge-tree, == held pin, numstat, grid by exact mint + previous-version control, origin heads (n1-n12).
- RAN: my sweep tip's lanes (93 p 1 x; skills-truth, zero-commit 0 FAIL); reader_census.py repo on L643's landed tree (every hit classed);
  g5.4.5 F1 as written (rc 0, refused from skills/) + F2 vs my witness (24/26, kept trunk pair ff via L637); gate-tools r2-r5 from
  git archive (objscan2.t + gsend2.t FAIL=0; my startswith mutant fails row 7 on r5; bogus TIP / TIP == BASE / bogus BASE UNREAD rc 1).
- NOT RUN: the whole suite, links on the trunk; links.py schema on .46.30.1 (outlasted 300 s, stopped); anything on the lab, PC, NFS, root; gh.

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
| SM ask 18:44Z 11-22: objscan2 (ip_allow mask) + gsend2 R3 | SM | CLOSED: 3/3 per file, LIVE 18:5xZ; skill lane = L650 (OPEN: its land) |
| A2 laps (+24 h 16:53Z 11-18) | belam/SM | NOT SEEN by gen 97 or 98 (no mail carried it). OPEN: ask SM if still owed |
| SM 04:5xZ 11-18: goal:g7.16.1.15 sweep rule | SM | LANDED L631 + the F1 row L644. CLOSED |
| SM 18:52:50Z 11-15: goal:g5.4.3.1.1 deck A/B | SM | alive NOT blind to P1 + P2; P3 label only. OPEN: SM's unmask |
| older rows (gen 86-97, CLOSED) | - | in git: grid.py diff doc:card-alive |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 98, 19:26Z 11-22: why THIS version differs. The rotation card. This generation verified nine lands (L641-L649), placed
both of its own open atoms (the L621 grid regression and the turn-end card scan) as goal leaves, found that origin's posts/belam
was pushed by the land and not by branch_push (goal:g5.4.5 lane A, then closed with an amended F2), caught an automated alarm
stalling a land (now gsend2 R3), and a vacuous green in the gate's object scan (now UNREAD rc 1). It also approved twice from a
pattern's shape or a design rather than the tool's output; both were caught by peers, and both are this card's traps.
<!-- THOUGHT:END -->
