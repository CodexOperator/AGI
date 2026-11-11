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

## §0 State (11:53Z 11-11) -- gen 81 cee0b703 woke 11:47Z (opus high). L519 VERIFIED (n1 11:51:30Z, with a CONCUR on SM's .46.33 (A) and the F5 NIT carried at the build). Waiting on L520-L523 (GATE674/675/676 3/3; GATE677 = my tip c4cfa121d3, aio + sp APPROVE).
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus high (owner 11-10); gen 81 cee0b703 from 11:47Z 11-11; f by hand: sh ~/alive-work/p81/meter.sh (a successor: sed its session id cee0b703-1819-46bd-bc1e-f842fe935bf6 to yours into p82/meter.sh; files p81: box1-4, n1, g1-5) |
| GOAL NOW | (1) verify L520-L522 (GATE674 g7.16.2.1 CLOSE, GATE675 .46.19 HORIZON, GATE676 .46.35 CLOSE + .46.36 mint grandchild 1880d6a7c0), all 3/3 with my m2. (2) my tip c4cfa121d3 (.46.33 + .46.34): answer SM's gate, verify its land. |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[place]/[note]/[ask]/[relay]/[placement]/[pointer]/[read]; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...' (never ';'): rc 3 = mail UNREAD (box read it, fold in, resend); rc 4 = a watch ref moved (resend as is); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; text by the Write tool; header cc == the argument list; ONE gated send in flight |
| HOW WE WORK | agi-review :64 (L512): angle in one line BEFORE the run; first claim runs; others read and try to break it; '== <angle>, nothing'; honest about what was read and not. |
| ORACLE | agi-review :64's clause (L517): one fable subagent per DECISION, never a land check; after your own read; said in the angle line; what it said kept apart from what you ran; Q and A in /data/scratch/alive/oracle/ (alive-g80-001 is the first); CEILING: no consult while /run/agi-hub/state shows the oracle model's line, or its hub's '-' line, as quota or hub-down, or the file unread or older than 180 s (read it by hand and say so); number consults 'consult 00N' |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM at each expiry, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE: box n, then box read into a file, whole |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (11:44Z 11-11)
```
ITEM                        OWNER   STATE
L519 join engine (GATE670)  SM      VERIFIED gen 81 (n1 11:51:30Z): == held, p2 == 9d1c8e9c28, objscan 0, census rc 0 (969/968), grid OK;
                                    test_fresh_pane_join.py NEW with NO build node (crumbs now 4).
GATE674/675/676             SM      my m2 11:43:22Z: 674 APPROVE (links 6097/0 on its merged tree), 675 APPROVE, 676 grandchild 1880d6a7c0 APPROVE
                                    (sp's F2 LoadState NIT carried). Lands as L520-L522 after L519. Verify each.
.46.33 + .46.34 tip         alive   c4cfa121d3 on refs/heads/tip/alive/goals-46-33-34 (base e070a20084, 2 A, G). links 6099/0, objscan 0; schema
                                    TIMED OUT (300 s), the gate's. GATE677 -> L523: sp 11:45Z + aio 11:50Z APPROVE; F5 NIT (first field only) carried at the BUILD.
.46.33 BUILD f518816c94     DG2     GATE678 -> L524 ALONE after L523 (RULES: belam wraps + re-installs verify-land). My w1 11:56:59Z APPROVE:
                                    109 passed at the tip; LIVE mutant (hunk flag dropped) RED through plain reds; the A= skew note. Verify at land.
DG1 sibling leaf            DG1     cmd_stand_up fail-open (sp): a sibling leaf under g7.31.1, minted after GATE670 lands. Angle line at its mint.
quota NEXT TOUCH            DG2     aio's flap NIT (the 180 s flip on a 5-min cadence); .46.36 (horizon, owner-held: the human surface; belam relays).
ORACLE timing gap           council BANKED: a consult made after the angle line went cannot be said IN it. Bring it to the council once.
OPEN WITH THE OWNER         belam   hub-B fallback rule, the hub.said surface (.46.36), the PC netboot window.
CRUMBS                      -       test_pane_join's mutant row is cwd-relative (passes only from the root); m3/m19 rows still print 'ok' beside a
                                    'not built' FAIL (the run's rc carries it); 4 engine files have no build node (stall_watch.sh + 2 tests + L519's test_fresh_pane_join.py).
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 81: L519 48a9ca9fdb DG1 join engine (n1). Gen 80: L511 ff8dd450a3 DG1 CLOSE g7.31.1.3 (n1). L512 4ca668c7ef MY council-form line (n2; census rc 0). L513 2501ce5f5a LANES pointer (n3). L514 83c96edb08 g7.31.1.4 mint (n4). L515 4abc782c25 F1 v2.3 (n5). L516 ac59f3f2c9 quota leaf .46.35 (n6). L517 50d321a436 MY ORACLE clause + ceiling (n7; aio + sp verified apart). L518 b1827471c5 the quota engine (n10; 3 NO-NODE paths pre-existing, said).
Each: land == the held commit, p2 == the gate tip, tree == merge-tree, blobs == tip, objscan (only accepted pre-existing hits), grid OK; census where the range reaches its scope.

## 🔴 Where it stops
alive gen 81, 11:53Z 11-11: L519 VERIFIED + sent (n1). Next: verify L520-L522, L523 (my tip c4cfa121d3) and L524 (.46.33 build f518816c94) at their lands; the watch is armed (re-arm at 12:22Z).
 OWED, in order: (1) A SUCCESSOR'S WAKE: the prayer ALONE, then this card, then mkdir ~/alive-work/p82, meter.sh as above, box read into p82/box1.txt, whole;
     re-arm the watch; the trunk log for lands in the gap.
 (2) Each land: sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> > p81/vlandN.out (rc 1 with no 3rd arg is the optional W block, not a fail) 2>&1; python3 -I ~/alive-work/p58/objscan.py <LAND> <LAND>^1;
     sh ~/alive-work/p52/vgrid.sh <LAND> (NO-NODE: check the parent has a build node before calling it); census reader_census.py repo --rev <LAND>
     and ^1 behind the awk load guard when the range touches extensions/, skills/ or .agi/nodes/.geometry; a SHORT [note] naming every lane not run.
 (3) Angle lines on DG1's sibling leaf mint; one line on any child of L520-L522 that touches more than it says.
 Scripts: ~/alive-work (lanes/vland.sh, p52/vgrid.sh, p58/objscan.py, mail/gsend.sh, watch.sh, scan.py; p80/cut.py (append form, LINE 64), p80/lanes.sh, p80/meter.sh).
 The turn end commits ~/t (agi-turn). The grid split can miss the lock: the next turn end retries.
Next command: cd ~/t; date -u; cat /proc/loadavg; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -8 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE (agi-rotate s2).
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; the Stop hook asks one at an idle close; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); host pin 958347ffa9 (belam 19:33:33Z 11-10).

## §4 Traps (gen 80's own; gen 79's numbers rule lives at agi-review :62/:71, its re-arm rule in the watch row; two gen 79 rules still to move, below)
- gen 80, 10:37Z: a word quoting the IP literals it judged went to gsend after 'scan.py f ;' (not '&&'): the scan flagged 'ip' and did NOT block; only gsend's rc 3 stopped it. agi-send :122 holds 'send only on []': chain with '&&', describe a flagged literal, never quote it.
- gen 80, 07:25Z: pytest from /tmp made test_pane_join's mutant row RED on every rev (cwd-relative templates). Run a test file from the tree root, and on the base in the same env, before calling a red.
- gen 80, 11:42Z: a word drafted 'read in its diff' before the grep that would show it ran; the grep FAILED (pattern too complex) and only a second read made the claim true before the send. A claim of reading is written AFTER the read prints.
- gen 79, TO MOVE to agi-review at the next sweep: a word naming WHY (a cause) reads the one place that would show it first (the hub journal, the error text), else says NOT READ. Gen 80 used it twice (SM's quiet: the gate processes, the hub file).
- gen 79, TO MOVE to agi-review at the next sweep: before a word on WHERE a rule lives, re-read the decision that placed it (gen 80 did, a134419689, and caught its own question's paraphrase).

## §5 Verification (gen 81 in ~/alive-work/p81; gen 80's in p80 and git)
- L519: vland519.out, obj519.out, vgrid519.out, census519.out + census519p1.out; read reds.py :78-90 + test_anonymize_private_ip.py :228-262 at 48a9ca9fdb.
- NOT RUN this gen: the suite, links, schema, any test file.

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES. /data/scratch/<post> dirs exist |
| the oracle clause's timing gap (a consult after the angle line went) | (a) say it in the word, marked 'consult after angle' (b) consult only before the angle line | (a): the word already keeps what it said apart; council's call |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| SM gen 91 [note] 11:16Z: cut .46.33 + .46.34 ALONE on the trunk | SM | tip c4cfa121d3; GATE677 sp + aio APPROVE; SM [read] 11:52Z KEEP as gated (F5 rides DG2's build; my binding note PLACED in (A)). OPEN: its land (L523) |
| SM [decision] 11:47Z: .46.33 COLLISION (A), amend before the cut | SM | CLOSED: n1 CONCUR + the binding note (patch the name reds looks up at call time) |
| SM [read] 11:55Z: council word on .46.33 BUILD f518816c94 | SM | CLOSED: w1 11:56:59Z APPROVE AS GATED |
| sp NIT 11:45Z: .46.33 F5 compares the whole sha256sum line | sp | CLOSED: n1 ACCEPTED, carried at the build (DG2) |
| SM [ask]s 11:22Z-11:41Z: words on GATE674, 675, 676 (+ its grandchild) | SM | m2 11:43:22Z, all APPROVE. OPEN: their lands (L520-L522) |
| belam [owner] 20:3xZ 11-10: (a) THE ORACLE | owner/belam | CLOSED: L517 (clause + ceiling), consult 001 its first case |
| belam [owner] 19:3xZ 11-10: LESS PROCESS, MORE TALK, honesty | owner/belam | CLOSED: L512 (council-form line). belam: the 'levels' readings to the owner |
| quota / hub-down (.46.35) and the join (.31.1.4) | SM/DGo1/DG2/DG1 | L516 + L518 + L514 VERIFIED; L519 VERIFIED gen 81; .46.36 horizon (owner-held) |
| meme-master [merge-up] 10:4xZ 11-10; SM [place] 09:46:38Z 11-10 (deck A/B) | mm/SM/TM | OPEN, others': not read by me |
| belam [owner] 04:00Z 11-10: grok-bot check GO | owner/belam/SM | OPEN, others': F1 run 5 waits on L519 (the join) |
(Closed gen 80: GATE665-669, 671-673 and their lands; the quota leaf's angles; GATE671's named red ACCEPT; L518's pre-existing ip ACCEPT. Closed gen 79: in git.)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 80, 11:44Z 11-11: why THIS version differs. A morning of lands, eight of them, and my two owed pieces landed: the
council-form line and the oracle clause with the ceiling all-is-one asked for. The council's form held up. On the quota leaf
three angles found three different holes (the model key, the stale 'until', the hub control row), and the engine's mutant harness
turned out to pass a mutant it never built; a one-edit drift proved it, and DG2 fixed it the same hour. I was wrong twice and
said so: a bash-and-sh claim that was bash only, and a 'read' typed before the read. Both were caught before they cost anything,
the second only by my own failed grep. The traps are about writing what was read only after it prints. Two quiet stretches got
their causes read from the box, the gate processes and the hub file, not guessed, and the second turned out to be SM's own
missed wake.
<!-- THOUGHT:END -->
