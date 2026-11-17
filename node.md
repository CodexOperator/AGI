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

## §0 State (02:06Z 11-17) -- gen 92 AWAKE (woke 01:52Z, meter f 0.145). The g90+g91 TRAP SWEEP is CUT and SENT: tip 0c8ac178f6 on
refs/heads/tip/alive/sweep-g91 ([merge-up] 02:04:31Z, mu1). L600 (.46.38 CLOSE) cut 14de8d7d35 PRE-VERIFIED (vland600/obj600 clean), waits on belam.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus; hub B (8318); f by hand: sh ~/alive-work/p92/meter.sh (gen 92 session aef9bdfa-d8ab-4a6a-8393-f490a8f19f85; at a rotation sed it into p93) |
| GOAL NOW | (0) the sweep tip 0c8ac178f6 through SM's gate + council words, then VERIFY its land; (1) verify L600 (cut pre-verified) and L596 as they land; (2) the deck A/B atom (§7) when TM's measure lands; (3) words on each tip SM asks. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...'; rc 3 = mail UNREAD (box read, fold in, resend; a peer word may make yours a repeat: shrink to '== peer' or drop); rc 4 = a watch ref moved (resend as is when it is not yours); rc 5 = a backtick or the host name; scan ['home'] = a home-path literal in YOUR text (describe it); STAMP header only, DSTAMP every line; text by the Write tool or a cat heredoc; header cc == the argument list; ONE gated send in flight |
| reading mail | AGI_POST=alive box read > p92/boxN.raw (box1 01:53Z empty) -> sed the home literal to <home> -> scan. 'box n' only LISTS (agi-send :92) |
| HOW WE WORK | agi-review: angle in one line; first claim runs; others read and try to break it; honest about what was read and not |
| ORACLE | OFF; Fable for the season rollover ONLY, off dispatch (L579 landed it in the bytes) |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (01:49Z 11-17)
```
ITEM                        OWNER   STATE
TRAP SWEEP g90+g91          -       L601 30440a2dae LANDED 02:45Z, VERIFIED n4 02:51:10Z (grid owed 2, paid 02:49:49Z by sp's turn end).
TRAP SWEEP aio g81+82       SM      110f1bf4cc 3/3 (w2); GATE793 on L601 -> L602: verify it, its grid read too (agi-review + agi-send).
.46.38 CLOSE 0c99ccf81f     -       L600 14de8d7d35 LANDED 02:13Z, VERIFIED n2 02:13:54Z (+ n3 02:14:23Z: the sha1-cut line RUN). F8 as written reads 4 on a correct
                                    build (the trunk moved between the leaf's land and the build's): the close records it; my w2 wording.
.46.37 CHILD 3 20a796a949   SM      3/3 APPROVE (w13 + aio + sp); GATE786 WHOLE after GATE785's re-run -> L596 ~03Z 11-17.
deck A/B arms (g5.4.3.1.1)  SM/TM   waits on TM's measure + pass line ON the node; then SM names runners; council words.
NEXT TOUCHES (not gates)    -       agi-goal :33 'mints it TWICE' stale since L594 (a RULES path, the next agi-goal touch). FLAKES under
                                    load: test_agi_boot high-reading row (GATE779) + test_crons_log_cap stranded-writer row (GATE785):
                                    SM proposes a leaf. DG2: two said lines for one hand move-back (w13). test_an_out_ref..._unread checks
                                    stdout for a stderr line (w8). ladder.md :154 'the model's' lowercase.
OPEN WITH THE OWNER         belam   the four .46.37 calls on belam's card §6 (restart at move vs next start, move back, hub-down move,
                                    a third account); hub.said (.46.36); PC netboot; plan-master tool policy; F4 of g7.31.1.6; P8 bank.
STANDING (host, belam)      belam   next E re-pin passes AGI_BOX=encryption-town; local-town's agi-ram-main + agi.slice STAY.
CRUMBS                      -       NO build node: test_alarm_spool.py, test_goal_skill_h1.py, test_hub_move.py, test_council_report.py,
                                    host-act lane, 88+ .t.sh, reds.py.
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 92: L601 30440a2dae alive trap sweep g90+g91 (n4). L600 14de8d7d35 DGo1 .46.38 CLOSE (n2, n3).
Gen 91: L594 21e9b6208b DG1 .46.38 BUILD (n9). L599 095c02051e DG1 .20.2.1 CLOSE (n8). L598 5b16a255d1 DG1 build:bin-alarm-spool (n7). L595 ee1e7c9e9a DG1 alarm-id BUILD (n6 + m5 correction; /opt installed by belam 21:13Z, read back 44e0118d027e). L597 1b4ebfc35e DGo1 .46.37 CLOSE (n5). L593 ab73f54473 DGo1 .46.38 leaf (n4). L592 93de4f570b DGo1 agi-goal H1 pair (n3). L591 c290160f97 DG1 P9 mint g7.16.1.13 (n2). L590 f76ea09e4f DG2 .46.37 CHILD 2, re-cut (n1). Host: belam's .46.37 host half v6 installed 16:07Z (3/3 after v2/v4/v5 holds).
Gen 90: L579-L589. Gen 89: L576-L578. Older in git.

## 🔴 Where it stops
alive gen 92 at 02:06Z 11-17: the sweep is SENT (tip 0c8ac178f6); next: words/gate on it, then verify L600 + L596 + the sweep's land.
 OWED, in order: (1) answer each council word on the sweep tip (a NIT = one re-cut on 0c8ac178f6, same ref, ONE commit).
 (2) L602 (aio's sweep) and L596 as they land: vland/obj/vgrid/census + ONE [note].
 (3) each land: PLAIN = 'sanctuary-master: LAND N' on posts/belam; RULES = the wrap ('wrap of LN'),
     LAND = WRAP^2. sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> [<WRAP>] > p92/vlandN.out 2>&1; python3 -I ~/alive-work/p58/objscan.py
     <LAND> <LAND>^1; sh ~/alive-work/p52/vgrid.sh <LAND> (DIFF until belam's split: wait for OK); reader census (extensions/agi/bin/
     reader_census.py repo --rev) at LAND and ^1 when the range touches extensions/, skills/ or .geometry; a 'no host act' claim is READ
     (the installed copy under /opt/agi/bin AND who calls which copy); a grep -c that prints 0 gets a CONTROL that must hit; ONE [note].
     Pre-verify the cut at SM's [merge-up] to belam (it names L = sha); belam may stop a cut whose parent went stale: re-run on the re-cut.
 Runs: --basetemp under /data/scratch/alive; scratch worktrees there, removed after (none open now).
Next command: cd ~/t; date -u; AGI_POST=alive box read > ~/alive-work/p92/boxN.raw; git log --first-parent --format='%h %an %<(70,trunc)%s' -8 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); belam + mm on own logins, all others on hub B; directors on sonnet (L579).
Grid lock: a turn end that reads 'not grown ... held by <pid> commit --all / unify --write' is the cron or a peer; flock frees on exit. Not stale unless the pid is alive and stuck.

## §4 Traps (gen 92; g90+g91's six moved to skills by tip 0c8ac178f6, two dropped as carried)
- [g92 02:13Z 11-17] n2 said two sha1 figures 'differ by method' before running the other method (n3 ran it: SM's cut = lines
  49-60 incl. the next H2) -> CARRIED: agi-review's 'a claim larger than the read' family (read narrower / a reading BESIDE it); DROP.
- [g92 02:02Z 11-17] a wait loop on 'pgrep -u me -f reader_census' matched its OWN argv and never ended (stopped by TaskStop) -> CARRIED,
  not new: agi-memory-guard's 'pgrep -f matches the waiter's own argv' line; my miss of a held rule, DROP at the next sweep.

## §5 Verification (gen 92, files under ~/alive-work/p92; gen 91's under p91)
- sweep: sweep.py (6 anchors x1), sweep.msg, added.txt (scan [] + home control), lane-*.out, census-sw-{0c8ac178f6,32f1874eb3}.out, mu1.
- RAN on each incident: F8 4 / own 0 / L599 1; alarm_spool callers at ee1e7c9e9a; fable hits :45 :110 :154; P9 :28 470 chars; 1a
  substring missing=0 vs cell missing=9 vs green 0. (3) NOT re-run (processes gone). L600 cut: vland600.out, obj600.out.
- NOT RUN this gen: pytest, zero-commit, links (SM's gate).

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| aio [merge-up] 02:15:45Z: words on its TRAP SWEEP g81+82 (L602 after L601, GATE793) | aio | CLOSED: w1 02:17:59Z AMEND on 7684186166 ((1) needs 2>&1); RE-CUT 1 110f1bf4cc, w2 02:21:42Z APPROVE (3/3) |
| self: g90+g91 trap sweep (owed at gen 91's rotation) | alive | CLOSED: L601 30440a2dae, n4 02:51:10Z |
| SM [ack] 01:4xZ 11-17: words on .46.38 CLOSE 0c99ccf81f (GATE791, L600) | SM | CLOSED: w18 01:48:51Z APPROVE (3/3) |
| sp 01:42:45Z: .46.38 F8 as written reads 4 at the build's land | sp | CLOSED: w17 01:45:22Z == sp + aio, my w2 wording owned, the L599 control |
| DG1 merge-up 21:45Z: CLOSE .20.2.1 1b66a547c8 + child 9be315fbac | DG1 | CLOSED: w15 AMEND, w16 APPROVE child (L599) |
| DG1 7a0916a241 build:bin-alarm-spool (the L595 crumb) | DG1 | CLOSED: w14 21:19:22Z APPROVE (L598) |
| SM [ack]s 16:1xZ: words on .46.37 CLOSE e1dec635cd + CHILD 3 20a796a949 | SM | CLOSED: w13 16:19:40Z APPROVE both |
| SM [read]/[word] 15:5xZ-16:0xZ: the .46.37 HOST HALF v2..v6 | SM | CLOSED: w10 NOT YET v4, w11 NOT YET v5, w12 APPROVE v6 |
| SM [ask] 14:5xZ: alarm-id BUILD 42adb9d395 (owed since gen 89) | SM | CLOSED: w8 14:51:14Z APPROVE WHOLE |
| SM 18:52:50Z 11-15 (aio's ask): goal:g5.4.3.1.1 deck A/B arms: SM names runners once TM's measure + pass line is ON the node | SM | OPEN: council words when TM's measure lands |
| older rows (gen 86-91, all CLOSED) | - | in git: grid.py diff doc:card-alive |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 92, 02:06Z 11-17: why THIS version differs. The sweep gen 91 handed on is cut and sent: each of the six traps went to the
skill line that already owns its flow, appended in place, and each rule was RUN on its own incident before the send (one, the
process read, could not be re-run and says so). The one slip this gen, a self-matching pgrep wait, is a rule already held, so it is
named on §4 to drop, not to place.
<!-- THOUGHT:END -->
