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

## §0 State (17:46Z 11-14) -- gen 87 SEATED 10:50Z 11-13 (session 26269a63-f741-4c97-b147-470948fd86a8, RESUMED 15:13Z 11-13 on hub B 8318). VERIFIED this gen: L563-L568 (n1-n6), L569 5721fb7d37 belam fuel block (n9 17:45:52Z; falsifier exact). PENDING: L-a1 re-cut (mm, on this trunk; content 3/3 carried, word on the merged section only); L570 DG1 a19 (RULES, GATE754, verify at belam's WRAP); L-b after both L-a.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus high; gen 87 session 26269a63-f741-4c97-b147-470948fd86a8; f by hand: sh ~/alive-work/p87/meter.sh (files in p87: box1 read; next w1, n1) |
| GOAL NOW | (1) verify each land as it comes (none queued 13:12Z); (2) words on each tip SM asks; (3) at your rotation, the trap sweep: §4's five gen-86 traps + aio's later touch (§7). |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...' (&&, NEVER ';': gsend does not scan for home paths); rc 3 = mail UNREAD (box read it, fold in, resend; a fresh peer word may make yours a repeat: shrink it to '== peer' or drop it); rc 4 = a watch ref moved; rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; text by the Write tool; header cc == the argument list (others: 'SM: a pointer to X'); ONE gated send in flight. Box copies: sed the home literal to <home>, then scan |
| HOW WE WORK | agi-review :64: angle in one line; first claim runs; others read and try to break it; honest about what was read and not. A word that only repeats a peer's shrinks to '== peer' or is dropped. |
| ORACLE | SUSPENDED (SM [decision] 02:17:50Z 11-12; owner 02:12Z: Fable reserved for the season rollover). |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (10:40Z 11-13)
```
ITEM                        OWNER   STATE
card-skip (a) (.46.30)      DG3     L564 e32f378635 VERIFIED (n2). LIVE: belam 12:3xZ 'cards skipped 4', 0 cron card versions; my read 12:40Z: 0 cron versions since 11:58Z on alive/aio/SM/sp cards. CLOSED.
                                    Skips doc:card-P only when its tip is P's OWN split (Split-Land author == P), never a deprecated node;
                                    today skips exactly alive, all-is-one, SM, sp (my run). 
frontmatter scope           DG3     L565 0e420b9c87 VERIFIED (n3). Live cron from 13:30 (belam's).
agi-turn skip line          DG3     L563 VERIFIED (n1). TM/dt-1 stale bin/agi-turn: CLOSED n7 (a unit start rebuilds ~/bin at AGI_TRUNK).
fuel fold (owner 11-14)      mm/belam L-a1 mm, L-a2 belam (PLAIN, either order), L-b mm RULES alone, belam wraps. Words on tips; VERIFY each land.
DG1 write-path cut (a19)    DG1     83de0c9160 RULES alone, GATE754 WHOLE; w9 APPROVE (+NIT 2-line carry.env). VERIFY its land + belam's WRAP (LAND = WRAP p2).
DG3 next grid touch         DG3     aio's NIT 1 (pin each half of the retired check alone), NIT 2 (the 'Named cost' sentence back).
L555 item                   TM      CLOSED: SM [relay] 16:25:45Z 11-14 (TM read AGI_BOX=local-town); DG1's fallback: aio's cut-or-drop.
test_p1_ab whole-suite      SM/DG3  VmHWM in the whole suite still NOT READ.
turn-end grid misses        alive   gen 86: 3 (08:16Z unify, 10:02Z commit --all, 10:16Z unify); gen 87: 1 (16:33Z 11-14, commit --all held 228 s, base a6d58bc744 kept): the split waits 30 s, the lock
                                    holders run 80-180 s; self-heals (~/.grid-base kept, base advanced). Observation; raise if a base stalls.
OPEN WITH THE OWNER         belam   hub-B fallback, hub.said (.46.36), PC netboot; Fable vs subagent passes; plan-master tool policy;
                                    F4 of g7.31.1.6 (an agi-reaper uid); a rendered-width check for the media page (council 3/3: owner's call).
CRUMBS                      -       NO build node, by payload_ref: agi-project-harness.t.sh, test_agi_boot.py, media_html.py,
                                    test_media_html.py + the older class (owner-cite.t.sh, box-*.t.sh, reds.py, test_p1_ab.py, ...).
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 87: L569 5721fb7d37 belam fuel block (town:core) + retire idea, plain (n9). L568 6b8ec91a57 mm fuel:s4-retire-the-python-engine, plain (n6). L567 d419a9a4ce mm doc:draft-presentation-outline, plain (n5). L566 e29f6b3677 aio TRAP SWEEP g78 188bed6105, plain (n4). L565 0e420b9c87 DG3 frontmatter scope 77c1adccaf, plain (n3). L564 e32f378635 DG3 card-skip (a) chain to 5fd96bd976, plain (n2). L563 3598c50f68 DG3 agi-turn skip line 83ac52770b + 89d625ae47, RULES, wrap 964783b95a; host act 12/12 (n1).
Gen 86: L562 6e4b616fe9 DG3 split-rewind child 92989e9405, plain (n7; its row 10/10 on the land). L561 9df76269b8 DR FINAL child c66570dda0 (n6; the string rounds CLOSED). L560 68435587a1 DR channels 1516f073cc (n5). L559 50bfca35c0 alive TRAP SWEEP g86 r2 ffdd75a714 (n4). L558 23ba4ce4fe DR width child 40a74684e8 (n3). L557 4ee5c43100 DR next touch 3560080ff9 (n2). All plain. Gen 85: L553-L556.

## 🔴 Where it stops
alive gen 87, 17:46Z 11-14: L563-L569 VERIFIED; next: word on L-a1's re-cut (merged section only), verify L570 at belam's WRAP (LAND = WRAP p2), then L-b. At rotation: my 10:35Z §4 trap is CARRIED by agi-review :158 (drop it); the other four go to the sweep.
 OWED, in order: (1) DONE 10:52Z (gen 87 wake: prayer, card, p87 + meter, box1 empty, watch re-armed, trunk at L562).
 (2) Each land: sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> [<WRAP>] > p87/vlandN.out 2>&1 (a RULES land: LAND = the WRAP's p2,
     never posts/belam^1; rc 1 with no 3rd arg = the optional W block); python3 -I ~/alive-work/p58/objscan.py <LAND> <its ^1>;
     sh ~/alive-work/p52/vgrid.sh <LAND>; NO-NODE by payload_ref; census (python3 -I extensions/agi/bin/reader_census.py repo
     --rev X and X^1) when the range touches extensions/, skills/ or .geometry; ONE [note] naming every lane not run.
 (3) Words on each tip SM asks; for a .geometry piece edit run engine-sizes.t.sh too; for a generated page, mutate the BUILDER.
 Runs: --basetemp under /data/scratch/alive; code under test by git archive extract into /data/scratch/alive/p87 (a fixture that
 a lane reads .agi/nodes from needs those dirs archived too); remove each extract after the word. The turn end commits ~/t.
 Branches tip/alive/sweep-g86, -r1, -r2 are mine and landed/abandoned (r2 = L559): leave them; no worktree is open.
Next command: cd ~/t; date -u; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -6 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); belam on opus medium, directors on sonnet at their next rotation (config:posts 65ded11e0b, owner 02:12Z).

## §4 Traps (gen 86 only; ALL go to your rotation's sweep)
- 08:15Z 11-13, TO agi-review (carry-grep 'a matching count' first): my w5 said every pre.ex's parent is 'details or .bytes' off
  the FIRST one printed; all 249 by a parser: details.ev 210, figure 39 ([correction] 08:15:53Z) -> a sentence about EVERY element
  is read over all of them by a parser, counts printed, before the send.
- 08:44Z 11-13, TO agi-review (carry-grep 'mutant' first): my w7 APPROVE of DR afbefd8d2f mutated the PAGE string; its pin compared
  the page to the builder constant that made it, so a BUILDER edit passed (sp caught it; withdrawn w8 08:47:47Z) -> a pin against
  a generated artifact is mutated at its SOURCE (the builder), never only in its output.
- 09:41Z 11-13, TO agi-send (the gsend/scan line): my w9 draft quoted a home literal; scan read ['home'] but 'scan.py f; gsend.sh'
  with ';' let gsend RUN (it checks backtick + host only); only rc 3 stopped it; nothing sent -> chain the scan with && ALWAYS;
  better: gsend runs scan.py itself and refuses on a hit.
- 09:49Z 11-13, TO agi-review: my n7 told belam to read 'agi-turn's split output' without reading agi-turn: :22 drops it on rc 0
  (sp 09:50:14Z) -> a pointer to WHERE a line can be read is checked to land somewhere (the caller's rc 0 AND rc != 0 paths).
- 10:35Z 11-13, DROP AS CARRIED by agi-review :158 (read 13:34Z, == aio's g78 drop): my w11 APPROVE of 83ac52770b ran zero-commit only;
  GATE746 red on engine-sizes (the ## pieces map row kept 8742, the ### heading said 8956) -> a .geometry piece edit runs
  engine-sizes.t.sh (heading AND map row) beside the piece's own lanes.

## §5 Verification (gen 86, files under ~/alive-work/p86)
- words w1-w15 (w-files + .out; n1 folded into w2; c1, c2 corrections, c2 folded into w8), notes n2-n8, merge-up m1. Lands: vland557-562,
  obj557-562, vgrid557-562, census557-562-*. Sweep: /data/scratch/alive/p86 lane-*.out. Runs: probe.out, loop.out, repeats.out,
  dr-width.out, dr4-width.out, dr5.out, dr6.out, es749.out, z20c.out.
- NOT RUN this gen: the whole suite, links, schema (the gates'); any oracle.

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| per-post scratch on /data so review copies + pytest basetemps leave the root mount | (a) belam host act (b) keep on / | (a), owner's call; council YES |
| the oracle clause's timing gap | moot while the oracle is SUSPENDED | revisit if the owner restores it |
Paid-for path guard: never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py; never recreate .agi/context/kits/ or .agi/context/plans/build-site.md.

## §7 ATOMS (inbound asks, one row each; open > 1 lap = red)
| atom | from | placed |
|---|---|---|
| SM [pointer] 07:06:43Z + 07:09:25Z + 07:11:23Z 11-13: words on DG3 re-cut 3726285171 + (a)/(b) | SM | CLOSED: w1 07:16:59Z |
| SM [pointer] 07:20:18Z 11-13: words on CHILD 92989e9405 | SM | CLOSED: w2 07:24:09Z; L562 VERIFIED (n7) |
| CLAUDE.md: the rotation's trap sweep (gen 85's 8 + gen 86's 1) | standing | CLOSED: L559 50bfca35c0 (n4) |
| aio LATER TOUCH 07:58:15Z: agi-review :122's 'every place the page carries it' also names link rel=stylesheet, @import, a script setting maxWidth (or lists them NOT covered) | aio | OPEN: the next sweep's first clause |
| SM [pointer] 07:38:57Z + 07:43:13Z 11-13: words on DR width 8f7204c633, then child 40a74684e8 | SM | CLOSED: w3 NOT YET, w4 APPROVE; L558 VERIFIED (n3) |
| SM [pointer] 08:14:01Z 11-13: words on DR channels 1516f073cc | SM | CLOSED: w5 + c1 + w6 (3/3 VIEW: stop the string rounds); L560 VERIFIED (n5) |
| SM [pointer] 08:42:33Z + 08:46:45Z 11-13: words on DR FINAL afbefd8d2f, then child c66570dda0 | SM | CLOSED: w7 withdrawn; w8 APPROVE; L561 VERIFIED (n6) |
| SM [ask] 09:39:40Z 11-13: b-7 word for L562 | SM | CLOSED: w9 09:42:47Z; L562 VERIFIED (n7) |
| SM [pointer] 09:50:47Z 11-13: words on DG3 card-skip c7f3550de9 | SM | CLOSED: w10 NOT YET (13 of 25 cards had no live turn-end writer) |
| SM [pointer] 09:58:50Z 11-13: card-skip RE-CUT 8c6a13a4ac + agi-turn 83ac52770b | SM | CLOSED: w11 (NOT YET one line -> belam's (a); 83ac52770b APPROVE + NIT) |
| SM gen 95 10:05-10:08Z: card-skip (a) chain 26ff58fe49 -> 202de46f35 | SM | CLOSED: w12 10:09:37Z APPROVE; verify L564 |
| SM gen 95 10:11-10:13Z: seam row 5fd96bd976 + frontmatter scope 77c1adccaf | SM | CLOSED: w13, w14 APPROVE; L564 (n2), L565 (n3) VERIFIED |
| SM [red] 10:35:41Z 11-13: GATE746 engine-sizes; DG3 fix 89d625ae47 | SM | CLOSED: w15 10:39:44Z APPROVE (+ my miss named); L563 VERIFIED (n1) |
| SM [merge-up] 11:31Z + belam/SM [landed] 11:36Z 11-13: L563 | SM/belam | CLOSED: n1 11:37:22Z |
| SM [ask] 11:37:41Z 11-13: L564 b-7 word | SM | CLOSED: w1 11:40:46Z (a), == aio, sp + my objscan |
| SM [merge-up] 11:41Z + [landed] 11:45Z 11-13: L564 | SM/belam | CLOSED: n2 11:46:42Z |
| SM [return] 17:20:07Z 11-14: L-a1 429cbeece1 conflicts with L-a2 on town:core; re-cut after L569 | SM | w10 17:21:13Z content APPROVE (my NIT closed); word on the merged section at the re-cut |
| SM [ask] 17:04:56Z 11-14: DG1 83de0c9160 + agi.sh placement | SM | CLOSED: w9 17:08:32Z; n8 dropped (== SM's (2), sp) |
| SM [ask] 16:44:55Z 11-14: L-a2 9b00bd4fa0 words | SM | CLOSED: w8 16:51:59Z == sp, aio; verify L569 |
| belam [decision] 16:4xZ 11-14: local-town host act order | belam/SM | CLOSED: w7 16:50:25Z APPROVE full + aio pre-step + sp conditions |
| SM [review] 16:15:10Z 11-14: fuel fold, four questions | SM | CLOSED: w5 16:19:08Z; verify L-a / L-b at land |
| belam [owner] 16:0xZ 11-14: TM data for report v2 + local inference; mm may replace v1.2 in place | belam | no ask to me; TM wake HELD for the owner; my n7 on the agi-turn install |
| belam [owner] 15:1xZ 11-13: hub A -> hub B for sp, aio, SM, alive; belam + mm asked | belam | CLOSED: no ask to me; my env read 8318 at 15:14Z |
| belam [note] 12:0xZ + 12:3xZ, SM [relay] 12:39:21Z: L562/L564 live reads | belam/SM | CLOSED: no ask; L564 read confirmed on the grid 12:40Z |
| SM [ask] 12:54:19Z 11-13: L565 b-7 word | SM | CLOSED: w2 12:57:24Z (a), == sp, aio + my objscan |
| SM [merge-up] 12:57Z + belam/SM [landed] 13:10Z 11-13: L565 | SM/belam | CLOSED: n3 13:11:26Z |
| aio [merge-up] 13:31:18Z + SM [note] 13:31:58Z 11-13: aio TRAP SWEEP g78 188bed6105, words | aio/SM | CLOSED: w3 13:34:06Z APPROVE; L566 VERIFIED (n4) |
| SM [pointer] 06:57:26Z 11-13: words on DR next touch 3560080ff9 | SM | CLOSED: L557 verified (n2) |
| L555 open item: local-town carry.env AGI_BOX read (TM's first act at wake) | council | CLOSED: SM [relay] 16:25:45Z 11-14, TM read AGI_BOX=local-town; aio decides cut/drop of DG1's fallback |
| aio 16:28:53Z + sp 16:30:59Z 11-14: DG1 write-path fallback CUT (both AGI_BOX defaults) | council | CLOSED: w6 16:32:09Z == aio + sp, wrong-box ExecCondition = backstop read; DG1 tip -> words |
| meme-master [merge-up] 10:4xZ 11-10; SM [place] 09:46:38Z 11-10 (deck A/B) | mm/SM/TM | CLOSED: w4 15:18:26Z APPROVE; L567 (n5), L568 (n6) VERIFIED; my fuel NIT rides mm's next touch |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 86, 10:40Z 11-13: why THIS version differs. The gen verified six lands, landed its own trap sweep, and helped turn two
engine ideas into rules that measure what they claim: the split-rewind skip (a flaky row found, then the cost of (a) counted on the
grid) and the card-skip (13 of 25 cards had no live writer; then 7 of 11 were land-split, which became belam's own-post test). Its
five traps are all the same shape: a claim made one step short of the thing it names (the first element, the output not the
source, a pointer not followed, a lane not run). Every ask on me is answered; the rest is gates, so the out is at a pause.
<!-- THOUGHT:END -->
