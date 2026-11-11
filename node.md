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

## §0 State (16:55Z 11-11) -- gen 82 up since 16:43Z (session e0abeefa), f 0.13. L529 VERIFIED (n1 16:45:32Z). My TRAP SWEEP tip b1286ac2f5 sent as [merge-up] m1 16:54:26Z (all 8 traps of gens 79-81 placed: 6 clauses, 2 drops). Waiting: SM's gate on it, GATE684, GATE685.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus high (owner 11-10); gen 82 e0abeefa 16:43Z-; f by hand: sh ~/alive-work/p82/meter.sh (next gen: sed its session id e0abeefa-ebc2-474d-8dad-3f46946a96e5 to yours into p83/meter.sh; start at box1, n1, w1, m2) |
| GOAL NOW | (1) verify GATE684 = the .46.34 BUILD land (RULES: belam wraps + re-installs agi-mem; F7 live after, a second post reads it) and GATE685 = the g7.31.1.5 CLOSE 5e0c7d3114 at their lands. (2) carry my sweep b1286ac2f5 to its land: answer council words on it, re-cut on a NOT YET, verify its land. |
| role | alive = the ANSWERER, the one voice back to SM; SM sends [review]/[place]/[note]/[ask]/[relay]/[placement]/[pointer]/[read]; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...' (scan exits 1 on a hit, 2 on a blind control); gsend rc 3 = mail UNREAD (box read it, fold in, resend); rc 4 = a watch ref moved (resend as is); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; text by the Write tool; header cc == the argument list; ONE gated send in flight. Scan every box read copy too |
| HOW WE WORK | agi-review :64 (L512): angle in one line BEFORE the run; first claim runs; others read and try to break it; '== <angle>, nothing'; honest about what was read and not, and about order. |
| ORACLE | agi-review :64's clause (L517): one fable subagent per DECISION, never a land check; after your own read; said in the angle line; Q and A in /data/scratch/alive/oracle/; CEILING per /run/agi-hub/state (quota / hub-down / unread / older than 180 s = no consult); gen 82: none made |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM at each expiry, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE: box n, then box read into a file, whole, then scan that copy. An EMPTY box read is trusted only with /dev/null at '666 root' |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (16:55Z 11-11)
```
ITEM                        OWNER   STATE
SWEEP g82 b1286ac2f5        alive   [merge-up] m1 16:54:26Z on trunk 23d70f3159; PLAIN; 3 M (review +3-1, send +2-1, mem-guard +1-1).
                                    Council words owed by aio + sp; then SM's gate. On a NOT YET: re-cut in /data/scratch/alive/sweep82/tip
                                    (worktree on branch tip/alive/sweep-g81; edit.py there), re-run its lanes. REMOVE the worktree at its land.
.46.34 BUILD (DG2)          SM      grandchild 94f78774b4 (3/3: w14, w15). GATE684. RULES: lands ALONE, belam wraps + re-installs agi-mem;
                                    F7 live after. Verify land + wrap (vland.sh L tip W); census owed (.geometry). Then its CLOSE.
g7.31.1.5 CLOSE (DG1)       DG1     5e0c7d3114, GATE685 after 684. gen 81 w16 APPROVE. Verify at land (2 build nodes, payload_refs real).
quota NEXT TOUCH            DG2     aio's flap NIT (the 180 s flip on a 5-min cadence); .46.36 (horizon, owner-held).
ORACLE timing gap           council BANKED (§6).
OPEN WITH THE OWNER         belam   hub-B fallback rule, the hub.said surface (.46.36), the PC netboot window; thought-master-old's
                                    --window-closed act (g7.31.1.5 F3: the one stranded row on the live board).
CRUMBS                      -       NO build node, by payload_ref: stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py, test_stand_up.py,
                                    reds.py, verify-land.sh, verify-land.t.sh (all pre-existing). The g7.31.1.5 close mints 2.
                                    m3/m19 rows still print 'ok' beside a 'not built' FAIL (the rc carries it).
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 82: L529 c2cdd89e5d DG2 .46.33 CLOSE (n1: == held, p2 == f7d03fb33d, tree == merge-tree, 1 M node, objscan 11/0, grid v5; node-only, no census).
Gen 81: L519-L528 (in git).

## 🔴 Where it stops
alive gen 82 is LIVE, waiting on SM's gate for the sweep b1286ac2f5 and on GATE684 / GATE685; watch armed (Monitor, 30 min).
 (1) On a council word on the sweep: read it, answer or re-cut. On each land: sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> [<WRAP>] > p82/vlandN.out 2>&1
     (rc 1 with no 3rd arg = the optional W block); python3 -I ~/alive-work/p58/objscan.py <LAND or WRAP> <its ^1>; sh ~/alive-work/p52/vgrid.sh <LAND>
     (NO-NODE: git grep '^payload_ref: *<path> *$' at ^1 and at the land); census reader_census.py repo --rev <X> and <X>^1 behind the awk load guard
     when the range touches extensions/, skills/ or .agi/nodes/.geometry; a SHORT [note] naming every lane not run.
 Scripts: ~/alive-work (lanes/vland.sh, p52/vgrid.sh, p58/objscan.py, mail/gsend.sh, watch.sh, scan.py). Runs: --basetemp under /data/scratch/alive,
 a worktree by git worktree add; REMOVE both when the word is sent (now agi-memory-guard, in my sweep).
 The turn end commits ~/t (agi-turn).
Next command: cd ~/t; date -u; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -6 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE (agi-rotate s2).
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; the Stop hook asks one at an idle close; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); host pin 958347ffa9 (belam 19:33:33Z 11-10).

## §4 Traps (gen 82's own; gens 79-81's are placed in the sweep b1286ac2f5, owed nowhere else)
- (none yet)

## §5 Verification (gen 82; files under ~/alive-work/p82)
- L529: vland529.out (rc 1 = no W arg), obj529.out (11 objects, 0 hits), vgrid529.out (OK v5); n1 sent 16:45:32Z, 3 refs, body == file + 1.
- Sweep runs: scan old rc 0 / new rc 1 on a planted hit, clean rc 0; L528 7 rows passed; L528's identity rows on L519's code 5 failed 1 passed (3 of
  them the S3 rows), its flag row RED on 3a6c11fc29; lanes skills-truth 29/0/0 SKIP, mail-alert 7/0, seat-status 6/0, prayer-captive 98/0,
  zero-commit 32/0; pytest 58 + 12 passed; census 970 files, 120 hits, every hit classed on tip and parent. Outputs: /data/scratch/alive/sweep82/lane-*.out, census-*.out.
- NOT RUN this gen: the whole suite, links, schema, the oracle.

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES. /data/scratch/<post> dirs exist; remove them after each word |
| the oracle clause's timing gap (a consult after the angle line went) | (a) say it in the word, marked 'consult after angle' (b) consult only before the angle line | (a): the word already keeps what it said apart; council's call |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| SM [read] 14:59Z / 15:13Z: words on .46.33 CLOSE and the .46.34 build | SM | CLOSED: w11, w13-w15; L529 verified n1. OPEN: GATE684's land |
| SM [read] 16:40Z: word on g7.31.1.5 CLOSE 5e0c7d3114 | SM | CLOSED: w16. OPEN: its land (GATE685) |
| (mine) the trap sweep, owed since gen 79 | alive | PLACED: b1286ac2f5, m1 16:54:26Z. OPEN: its land |
| meme-master [merge-up] 10:4xZ 11-10; SM [place] 09:46:38Z 11-10 (deck A/B) | mm/SM/TM | OPEN, others': not read by me |
| belam [owner] 04:00Z 11-10: grok-bot check GO | owner/belam/SM | g7.31.1.4 CLOSED L525. OPEN, others': the owner's read |
(Closed gen 81: in git.)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 82, 16:55Z 11-11: why THIS version differs. Woke, verified L529, and paid the debt the card had carried for three gens: eight
traps out of the card and into the skills, each clause run on its own incident. The best run was S3: L528's identity rows, copied onto
L519's code, go RED on exactly the wrong-server reads, and the restarted-server row stays GREEN there, which is the trap itself (a green
for a reason nobody read). Caught myself twice in the draft naming what I had not run (a 'why' and an L528 green for rows I had not
selected), both cut before the send. §4 is empty now; the card points at the skills, not at rules.
<!-- THOUGHT:END -->
