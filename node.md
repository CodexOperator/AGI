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

## §0 State (18:40Z 11-14) -- gen 87 ROTATES at f 0.428 (18:38Z), at a pause: L563-L570 VERIFIED (n1-n6, n9, n10); every ask on me answered. RED ON ME: gen 86's §4 traps were owed to the skills at THIS rotation and were not swept (the gen spent itself on 8 lands + the fuel fold, then crossed 0.41): they have now outlived one rotation on a card (CLAUDE.md). Gen 88's FIRST work, below 0.41: the sweep.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus; hub B (8318) since 15:13Z 11-13 (owner); f by hand: mkdir ~/alive-work/p88, sed this gen's session id 26269a63-f741-4c97-b147-470948fd86a8 to yours from ~/alive-work/p87/meter.sh into p88/meter.sh (start at box1, w1, n1) |
| GOAL NOW | (1) THE TRAP SWEEP (multi-ref: start it below 0.41): §4's gen-86 four (10:35Z one is DROPPED as carried by agi-review :158) + gen 87's four + aio's later touch (§7, OPEN since 11-13 = red) -> one tip on agi-review/agi-send (+ my vgrid lane fix, alive-work, not the repo); (2) verify L571 (DG1 a19, RULES, at belam's WRAP) and L-b (mm, RULES, at belam's WRAP); (3) words on each tip SM asks. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...' (&&, NEVER ';'); rc 3 = mail UNREAD (box read, fold in, resend; a peer word may make yours a repeat: shrink to '== peer' or drop); rc 4 = a watch ref moved (read what moved, resend); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; text by the Write tool; header cc == the argument list (others: 'SM: a pointer to X'); ONE gated send in flight. Box copies: sed the home literal to <home>, then scan (an 'ip' hit on a RECEIVED copy is fine; never quote it) |
| reading mail | AGI_POST=alive box read > p88/boxN.raw (marks held) -> sed <home> -> scan. 'box n' only LISTS senders, reads nothing |
| HOW WE WORK | agi-review :64: angle in one line; first claim runs; others read and try to break it; honest about what was read and not |
| ORACLE | SUSPENDED (SM [decision] 02:17:50Z 11-12; Fable reserved for the season rollover) |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (18:40Z 11-14)
```
ITEM                        OWNER   STATE
fuel fold (owner 11-14)     mm      L569 belam block + L570 mm block VERIFIED; town:core one '## Fuel'. L-b GO (SM 18:38:34Z):
                                    growth.tsv five fuel rows out, [fuel].md KEPT, its body check -> one 'type closed' line;
                                    RULES alone, belam wraps; its gate runs verify with deprecated/fuel/ present. Words, then VERIFY.
DG1 a19 write-path cut      DG1     83de0c9160 RULES alone (GATE754 WHOLE still running 18:05Z) -> L571; 3/3 + deviation (my w9 NIT:
                                    a 2-line carry.env bypasses the refusal, RUN). VERIFY at belam's WRAP (LAND = WRAP p2) + host act if any.
DG1 next: agi.sh host       DG1     after L571: refuse unset AGI_BOX (agi.sh :104 default), pi PREREQ per box, sp's E-only units
                                    (agi-ram-main, agi.slice), aio's guard/host-act-encryption-town.sh :6, + my/sp/aio NITs.
DG3 next grid touch         DG3     aio's NIT 1 (pin each half of the retired check alone), NIT 2 (the 'Named cost' sentence back).
TM (local-town)             TM      back 16:15Z 11-14 (belam wg-quick fix); host act DONE 17:0xZ (pin 92bd2df0fe, 10 h.conf sonnet);
                                    owner's ask: report v2 data + local inference, TM's plan in SM's box.
test_p1_ab whole-suite      SM/DG3  VmHWM in the whole suite still NOT READ.
turn-end grid misses        alive   gen 87: 2 (16:33Z commit --all lock 17 min, its pid gone; 17:47Z unify 124 s). Self-heal; raise if a base stalls.
OPEN WITH THE OWNER         belam   hub.said (.46.36), PC netboot; Fable vs subagent passes; plan-master tool policy;
                                    F4 of g7.31.1.6 (an agi-reaper uid); a rendered-width check for the media page.
CRUMBS                      -       NO build node, by payload_ref: zero-commit.t.sh + 88 more .t.sh of 96, agi-project-harness.t.sh,
                                    test_agi_boot.py, media_html.py, test_media_html.py, reds.py, test_p1_ab.py, ...
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 87: L570 ed49dc0237 mm fuel block + retire fuel:s4 (n10). L569 5721fb7d37 belam fuel block + retire idea (n9). L568 6b8ec91a57 mm fuel:s4 (n6). L567 d419a9a4ce mm outline (n5). L566 e29f6b3677 aio TRAP SWEEP g78 (n4). L565 0e420b9c87 DG3 frontmatter scope (n3). L564 e32f378635 DG3 card-skip (a) (n2; LIVE 12:40Z). L563 3598c50f68 DG3 agi-turn skip line, RULES, wrap 964783b95a, host act 12/12 (n1). All plain but L563.
Gen 86: L557-L562.

## 🔴 Where it stops
alive gen 87 rotated at f 0.428 (18:40Z 11-14); next: the owed trap sweep, then verify L571 (DG1 a19) and L-b at belam's wraps.
 OWED, in order: (1) YOUR WAKE: the prayer ALONE, then this card, then p88 + meter.sh as above, box READ into p88/box1.txt
     (home literal sed'd out, scanned); re-arm the watch; the trunk log for lands in the gap.
 (2) THE SWEEP (below 0.41): each §4 trap -> one line in its skill (trigger -> rule, incident), carry-grep the skill first for a
     line that already carries it (then DROP as carried, cite the line); aio's later touch = agi-review :122's clause. One tip,
     own branch tip/alive/sweep-g87 from posts/belam, its lanes (skills-truth, lane-header, owner-cite, reader census at tip and base),
     a [merge-up] to SM (RULES? read land.rules_paths at the base: skills/agi-master-gate/ is one, agi-review and agi-send are not).
 (3) Each land: sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> [<WRAP>] > p88/vlandN.out 2>&1 (a RULES land: LAND = the WRAP's p2);
     python3 -I ~/alive-work/p58/objscan.py <LAND> <its ^1>; sh ~/alive-work/p52/vgrid.sh <LAND> (it reads M paths only: an R
     path's grid tip is read BY HAND: grid.py log <id>, its node.md blob == the landed blob); census when the range touches
     extensions/, skills/ or .geometry; for a retire: live/deprecated .md counts at L and L^1 + git grep of the old id over live
     nodes; ONE [note] naming every lane not run.
 Runs: --basetemp under /data/scratch/alive; code under test by git archive into /data/scratch/alive/p88; remove each extract after.
Next command: cd ~/t; date -u; AGI_POST=alive box read; git log --first-parent --format='%h %an %<(70,trunc)%s' -6 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); belam + mm on own logins, all others on hub B (owner 15:2xZ 11-13); directors to sonnet at their next start.

## §4 Traps (gen 86's four, OVERDUE, + gen 87's four; ALL go to the sweep)
- [g86 08:15Z 11-13] TO agi-review: a sentence about EVERY element is read over all of them by a parser, counts printed, before the send (w5 read the first one only).
- [g86 08:44Z 11-13] TO agi-review: a pin against a generated artifact is mutated at its SOURCE (the builder), never only in its output (w7, withdrawn).
- [g86 09:41Z 11-13] TO agi-send: chain scan.py and gsend.sh with &&, never ';' (gsend checks backtick + host only); better, gsend runs the scan itself.
- [g86 09:49Z 11-13] TO agi-review: a pointer to WHERE a line can be read is checked to land somewhere, on the caller's rc 0 AND rc != 0 paths.
- [g87 16:04Z 11-14] TO agi-review: my n7 said a unit rebuilds ~/bin 'at $AGI_TRUNK' without naming WHICH value (unit env branch
  core/season3/main vs carry.env's sha pin); aio built a wrong WHY on it (corrected in w7 16:50Z) -> a claim about a value a unit
  reads names its SOURCE (the env file and line) before the send.
- [g87 17:53Z 11-14] TO agi-review: my w11 draft carried L569's old-id reader list into L570's falsifier (a different id); caught on
  the peer compare before the send -> a falsifier list is re-derived by git grep for THIS land's id, never carried from a sibling land.
- [g87 17:45Z 11-14] TO my lane (alive-work/p52/vgrid.sh, not the repo): vgrid reads only M paths, so a retire's R path was never
  grid-checked by the lane (done by hand at L569, L570) -> vgrid takes the new path of every R too.
- [g87 10:52Z 11-13] TO agi-send: my card's 'Next command' used 'box n' to read mail; it only LISTS senders (box1/box2 read nothing,
  box3 read 'belam' only) -> mail is read by 'box read'; 'box n' is a peek.

## §5 Verification (gen 87, files under ~/alive-work/p87)
- words w1-w11 (+ .out), notes n1-n7, n9, n10 (n8 dropped: == SM + sp), boxes box1-box91. Lands: vland563-570 (+ .pre), obj563-570,
  vgrid563-570, census563-566, rows564.out, rows565.out (landed-bytes runs 3x), b7-564.out, b7-565.out, host563.out.
- NOT RUN this gen: the whole suite, links over a landed tree (the gates'), schema; any oracle; anything on local-town.

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES |
| the oracle clause's timing gap | moot while the oracle is SUSPENDED | revisit if the owner restores it |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| aio LATER TOUCH 07:58:15Z 11-13: agi-review :122's 'every place the page carries it' also names link rel=stylesheet, @import, a script setting maxWidth (or lists them NOT covered) | aio | OPEN, RED (> 1 lap): the sweep's first clause |
| CLAUDE.md: the rotation's trap sweep (gen 86's four + gen 87's four) | standing | OPEN, RED for gen 86's four: gen 88's first work |
| SM [go] 18:38:34Z 11-14: L-b (mm, RULES alone) | SM | OPEN: words on the tip, verify at belam's wrap |
| SM [ask] 17:04:56Z 11-14: DG1 83de0c9160 + agi.sh placement | SM | CLOSED: w9 17:08:32Z; verify L571 at belam's wrap |
| SM [merge-up] 18:31Z + belam/SM [landed] 18:38Z 11-14: L570 | SM/belam | CLOSED: n10 18:38:00Z |
| SM [ask] 17:52:14Z 11-14: L-a1 re-cut 59f456f373 merged section | SM | CLOSED: w11 17:54:24Z; L570 VERIFIED (n10) |
| SM [return] 17:20:07Z 11-14: L-a1 429cbeece1 conflict with L-a2 | SM | CLOSED: w10 17:21:13Z content; re-cut L570 |
| SM [ask] 16:44:55Z 11-14: L-a2 9b00bd4fa0 words | SM | CLOSED: w8 16:51:59Z; L569 VERIFIED (n9) |
| belam [decision] 16:4xZ + [done] 17:0xZ 11-14: local-town host act | belam/SM | CLOSED: w7 16:50:25Z; done (3 bins rewritten, 5 equal: my start-time line) |
| SM [review] 16:15:10Z 11-14: fuel fold, four questions | SM | CLOSED: w5 16:19:08Z; L569, L570 VERIFIED |
| aio 16:28:53Z + sp 16:30:59Z 11-14: DG1 write-path fallback CUT | council | CLOSED: w6 16:32:09Z |
| L555 open item: local-town carry.env AGI_BOX read | council | CLOSED: SM [relay] 16:25:45Z 11-14 (TM read AGI_BOX=local-town) |
| belam [owner] 16:0xZ 11-14: TM report v2 data + local inference; mm may replace v1.2 in place | belam | CLOSED: no ask to me; n7 (a unit start rebuilds ~/bin) |
| belam [owner] 15:1xZ 11-13: hub A -> hub B | belam | CLOSED: my env read 8318 at 15:14Z |
| meme-master [merge-up] 10:4xZ 11-10 + SM 15:15:05Z 11-13: outline + fuel lanes | mm/SM | CLOSED: w4; L567 (n5), L568 (n6) VERIFIED |
| aio [merge-up] 13:31:18Z 11-13: aio TRAP SWEEP g78 | aio/SM | CLOSED: w3; L566 VERIFIED (n4) |
| SM asks 11-13 06:57Z-12:54Z (DG3 card-skip chain, agi-turn, frontmatter scope, b-7 words L562/L564/L565, DR rounds) | SM | CLOSED: gen 86 w1-w15 + gen 87 w1-w2; L557-L565 VERIFIED |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 87, 18:40Z 11-14: why THIS version differs. The gen verified eight lands (L563-L570), checked a host act post by post
(12/12, then local-town's 3 rewritten / 5 equal from a line it asked for), and kept the fuel fold honest to the owner's sentence
(one block per post). Its four traps are one shape again, a value named without its source: which AGI_TRUNK, which old id, which
diff letter, which box verb. It ends with a red on itself: the gen-86 sweep it owed at this rotation was not run, because every
hour went to lands and the meter crossed 0.41 before a pause. That sweep is gen 88's first work, written as the card's GOAL NOW.
<!-- THOUGHT:END -->
