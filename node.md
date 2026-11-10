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

## §0 State (02:25Z 11-10) -- gen 76 WORKING, f 0.13. Woke 02:14Z: L489 (DGo1's .13.4 CLOSE) had landed 02:09:55Z -> VERIFIED [note] 02:15:20Z. TRAP SWEEP gen 75 cut a8e9f4b056 (refs/heads/tip/alive/sweep-g75, agi-review +1 -1, PLAIN), every retired/skills-truth lane + census RUN on its tree, all green -> [merge-up] 02:24:23Z, awaiting seats' words + SM's gate. GATE639 (DG1's L478 fix 0e6de56a4d) on its whole-suite run 2 since 02:1xZ (run 1 = SM's own selection error, not DG1's).
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code; gen 76 8da3b044 claude-opus-5-5, 02:14Z 11-10 -; on HUB A (owner order via belam: report any 'limit' reply at once); no meter hook -> f by hand: sh ~/alive-work/p76/meter.sh (next gen: sed its session id 8da3b044-9941-43a3-9f87-a54bbda22f87 to yours into p77/meter.sh) every few turns |
| GOAL NOW | (1) GATE639's land: vland + vgrid + objscan + census (load5 < 8) + test_seat_alias_notice.py (must read 0 failed) + [note] naming EVERY lane not run. (2) My sweep-g75: answer seats' words; re-cut on a TERM (cut.sh takes a suffix: a NEW ref per re-cut); vland at its land. (3) Each [review] SM sends. |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[place]/[note]/[ask]/[relay]; NEVER box belam (SM relays WHOLE); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, its WHOLE output to a file (> f 2>&1): rc 3 = mail waiting UNREAD (box read it yourself, fold in, resend); rc 4 = a watch ref moved (resend as is); rc 5 = a backtick or the host name in the text (quote code in words); STAMP on the HEADER line only, DSTAMP every line; text by the Write tool; privacy scan first: python3 -I ~/alive-work/scan.py <file>; header cc == the argument list; ONE gated send in flight; several items ride ONE word |
| watch | Monitor sh ~/alive-work/watch.sh (20 s poll, 30 min expiry, re-arm, then box n + the trunk log for the gap). A restart KILLS it: re-arm. A 'mail: box read' prompt is a WAKE: box read into a file, whole (02:21Z: one read empty, nothing new) |
| council rules | VIEW to both seats (cc SM) -> ONE [decision] to SM after both answered, or 15 min MEASURED; seat terms ride as 'author's + mine, silence = agree'; [correction] amends |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (02:25Z 11-10)
```
ITEM                       OWNER   STATE
MY SWEEP g75 a8e9f4b056    alive   [merge-up] 02:24:23Z (one clause: a land's VERIFIED [note] names EVERY lane not run; xargs trap DROPPED,
                                   carried). Lanes on its tree: mail-alert-retired 7 ok, seat-status-retired 6 ok, skills-truth 29 ok 0 SKIP,
                                   4 retired pytest files 58 passed, census rc 0 both revs. SM [review] 02:25Z to aio + sp; GATE640 BUILT
                                   (every skill lane + census + links), QUEUED after GATE639. OPEN: seats' words, GATE640, land, vland.
GATE639 DG1 FIX (L478 red) SM      0e6de56a4d 3/3. WHOLE suite run 2 since 02:1xZ. OPEN: land, vland + test_seat_alias_notice.py 0 failed.
TRUNK RED since L478       DG1     test_seat_alias_notice x2 (heal.py --seat, no SeatAction). Fixed by GATE639 once it lands.
p1_ab peak_rss row         owner?  belam's suite: test_p1_ab.py peak_rss_kb None under agi-belam, UNCLASSED (likely env); its owner reads it. Not mine.
.46.33 / .46.34 (DG2)      DG2     .46.33 (diff reader) builds first, then .46.34 (cite across stores, my mint 0e8f9413eb), then g7.16.2.1's CLOSE.
FUEL (meme-master)         mm      L485 landed; meme-master tells TM and re-types its own fuel idea; its CLOSE names term (a) OUT.
SM's CRUMB                 SM      the objscan ip-class mask on BASE anonymize.ip_allow paths (DG2's crumb, SM to place).
g7.31.1.2 ACT 2c (DG1)     DG1     L478 + the fix; the live kill + reattach run is the owner's or belam's GO (none given); DG1's CLOSE after it.
BANKED VIA SM              OWNER   the row cell 'resume_failed' (owner's batch).
HELD (card-belam s6)       OWNER   atomize_live + summary_live flips, V1b host act, .46.28 F3, .20.4 crons apply --sudo, g7.31.1/.3, R2 grant.
CRUMBS (next touches)      -       resume-failed reads UNREAD as none (heal.py _last_resume_failed); cred-act.sh label 'a refresh' -> 'written after
                                   the seed'; drop-in's dead '[cred]' echo + no build node; ~33 bin .py with no build node (banked, belam 11-07;
                                   L484 closed two: harness_template.py, test_heal_resume.py; reds.py + verify-land.t.sh remain).
HARD RESETS                OWNER   after any boot (uptime -s after 02:44:54Z 11-04): refs resolve + fsck.
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 76: L489 5b3f7e50aa (DGo1 CLOSE .13.4, plain) 02:15:20Z: p2 == tip 3b4f9dbb4a, tree == merge-tree, 1 M goal node, blob == tip, D 0, objscan 0,
grid OK v3. My F1 NIT not taken (a NIT). NOT RUN: pytest, links (belam: 6086/0), census (no census path), skills-truth, any lane.
Gen 75: L480-L488 each VERIFIED (vland + vgrid + objscan + census at the land); NONE ran pytest or a lane (the gates did).

## 🔴 Where it stops
alive gen 76 WORKING (02:25Z 11-10): my sweep-g75 [merge-up] out; GATE639 on the whole suite.
 OWED, in order: (1) on wake after a restart: the prayer ALONE, then this card, then box read into p76/boxN.txt (or p77/), whole; re-arm the watch.
 (2) Each land as SM cuts it: sh ~/alive-work/lanes/vland.sh <LAND sha> <gate tip> [<wrap sha>] > p76/vlandN.out 2>&1 (read its lines, not its
     rc); sh ~/alive-work/p52/vgrid.sh <LAND> (DIFF right after a land = lag: re-read after belam's split or :00/:30);
     python3 -I ~/alive-work/p58/objscan.py <LAND> <LAND>^1; a blob != tip: check == git merge-file (p1, merge-base, tip); census
     reader_census.py repo --rev <LAND> and <LAND>^1 when load5 < 8 and the range touches extensions/, skills/ or .agi/nodes/.geometry; [note]
     whose NOT RUN line names EVERY lane not run (pytest included). GATE639's land: also run test_seat_alias_notice.py (one file, ~22 s).
 (3) A skills tip's lanes on its own tree: sh ~/alive-work/p76/lanes.sh <trunk> <tip> > out 2>&1 (load5 + start check in-command; fixture on
     /data/scratch/alive, removed; ~3 min). Sweep re-cut: sh ~/alive-work/p76/sw/cut.sh <trunk sha> r1 (refuses a moved trunk, rc 3).
 Scripts: ~/alive-work (lanes/vland.sh, p52/vgrid.sh, p58/objscan.py, mail/gsend.sh, watch.sh, scan.py, p76/meter.sh, p76/lanes.sh, p76/sw/).
 The turn end commits ~/t (agi-turn). A grid split can miss the lock: the next turn end retries.
Next command: cd ~/t; date -u; cat /proc/loadavg; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -4 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE (agi-rotate s2).
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot (owner 11-07); never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); carry.env AGI_TRUNK = f45e10cd16 (belam's re-pin 16:36:19Z 11-09; not re-read this gen).

## §4 Traps (gen 76's own; gen 75's two ride my sweep-g75, a8e9f4b056: one placed, one dropped)
- gen 76: a context read used grep -o -E with a bounded {0,140} repeat under the Bash tool's ugrep: complexity error on every line, then the loop ran past the 120 s cap into the background. Carried by agi-verify's ugrep line (use awk; I used python3 -I) and agi-memory-guard's heavy-run line -> no new rule; DROP at the next sweep.

## §5 Verification (gen 76; older in git)
- L489: p76/vland489.out + vgrid OK v3 + objscan 10 objects 0 hits
- sweep-g75 a8e9f4b056: p76/lanes-sw.out (3 sh lanes 0 FAIL, pytest 58 passed rc 0), p76/census-sw-*.out (rc 0 both, 964/85/120), objscan 5 objects 0 hits, merge-tree with 0e6de56a4d rc 0
- NOT RUN all gen: any full pytest, links whole-tree, any lane on a land; agi-mem cite (no mem row)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data (owned by each post uid) so review copies + pytest basetemps leave the root mount (85% used at 01:4xZ 11-10) | (a) belam host act (b) keep on / | (a), owner's call; belam, sp, alive, aio YES. NOTE: /data/scratch/alive exists, alive-owned; gen 76 used it for lane fixtures |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| alive OWED TRAP SWEEP gen 75 | alive | [merge-up] a8e9f4b056 02:24:23Z; SM [review] to seats 02:25Z, GATE640 queued after 639. OPEN: seats' words, gate, land, vland |
| SM [landed] 02:1xZ 11-10: L489 + GATE639 run 1 = SM's selection error | SM/belam | L489 CLOSED: VERIFIED 02:15:20Z. GATE639 run 2: OPEN |
| SM [review] 01:5xZ 11-10: DG1's FIX 0e6de56a4d (the L478 red) | SM/DG1 | 3/3 (mine 01:51:45Z, aio 01:52:21Z, sp 01:52:46Z). OPEN: GATE639 (whole suite), land, vland + run the test file |
| SM [review] 01:4xZ 11-10: DGo1 CLOSE .13.4 3b4f9dbb4a | SM/DGo1 | CLOSED: L489 VERIFIED 02:15:20Z |
| belam [result] 01:4xZ 11-10: .13.4 F3 PASS; trunk RED since L478 (test_seat_alias_notice x2, heal.py --seat) | belam/SM | REPRODUCED + my L478 [correction] 01:43:43Z; DG1's fix = GATE639. OPEN: its land |
| DG2 g7.16.2.1 FOLLOW-UP 08dbe7e1ce | DG2/SM | CLOSED: L480 VERIFIED. OPEN: DG2's CLOSE (names .46.33 OPEN) |
| DG1 g7.31.1.2 ACT 2c | DG1/SM | L478 VERIFIED on bytes only (its red: GATE639). OPEN: the live kill + reattach GO (owner/belam); DG1's CLOSE |
| DGo1 .46.12 CLOSE + .13.4 re-run + .44.8 horizon | DGo1/SM | L472 VERIFIED; .13.4 CLOSED = L489. OPEN: .44.8 horizon |
| owner atoms (a) pi-call idea, (b) crons.py retirement, (R) OptMem horizon + s11 OVERRULED | owner/belam | L471 VERIFIED. OPEN: the atoms' CLOSES (DGo1/belam) |
| SM CHECK T2 08:47Z (belam's leaf list) | SM/belam | PLACED 08:55Z. OPEN: those places' results |
| belam [owner] 03:14:32Z: Meme Master; bundles on core; STANDING STOP at season 3's end; login standby | owner/belam/SM | g5.4.4 = L461 VERIFIED. OPEN: next-touch NITs; aio NOTE A at the stop |
(Gen 75's closed rows, L480-L488 and FUEL, are in git: 0f57e04241.)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 76, 02:25Z 11-10: why THIS version differs. Gen 76 woke to a land already made, L489, and verified it. Its note named every lane it
did not run, which is the rule gen 75 found I had broken. Then it turned that rule into a skill line. It is one clause on agi-review's
reader-census line, where gen 75 said it belongs. The other trap is dropped, because two skills already hold it. Before the merge-up I ran the
skills tip's own lanes on its own tree, as agi-review asks of an author. So the word I sent carries readings, not promises. The card now holds
the lanes script, so the next skills tip costs one command.
<!-- THOUGHT:END -->
