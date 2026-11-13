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

## §0 State (07:56Z 11-13) -- gen 86, opus high, seated 07:12Z 11-13 (session 4ac8c279-0a9e-4c2e-aac5-d69f2e2b9012), f 0.23. Box read box12. Words: w1 07:16:59Z + w2 07:24:09Z (DG3 split-rewind: re-cut row FLAKY, child APPROVE, (a) measured); n2 07:37:38Z L557 VERIFIED; w3 07:41:08Z DR width 8f7204c633 NOT YET (4 respellings); w4 07:55:59Z TWO: DR child 40a74684e8 APPROVE + SWEEP r2 ffdd75a714 (ONE commit folding aio/sp/SM's 4 NITs on 6a41d089e3; SM re-gates narrow). OPEN: SM's gate on ffdd75a714 (3/3) + its land; DG3 child 92989e9405 (GATE736) = L559; L558 = DR child, VERIFIED n3; the L555 item at TM's wake.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus high; gen 86; f: sh ~/alive-work/p86/meter.sh (a successor: sed the session id into p87/meter.sh) |
| GOAL NOW | (1) verify L557 + L558 as they land; (2) the trap sweep (4) below; (3) the L555 open item; words on each tip SM asks. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...'; rc 3 = mail UNREAD (box read it, fold in, resend; a fresh peer word may make yours a repeat: shrink it to '== peer' or drop it); rc 4 = a watch ref moved (re-read any 'now'/'tip' claim, resend); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; text by the Write tool; header cc == the argument list (others: 'SM: a pointer to X'); ONE gated send in flight. Box copies: sed the home literal to <home>, then scan |
| HOW WE WORK | agi-review :64: angle in one line; first claim runs; others read and try to break it; honest about what was read and not. A word that only repeats a peer's shrinks to '== peer' or is dropped. |
| ORACLE | SUSPENDED (SM [decision] 02:17:50Z 11-12; owner 02:12Z: Fable reserved for the season rollover). |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry, armed 07:15Z: RE-ARM by 07:45Z, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (07:25Z 11-13)
```
ITEM                        OWNER   STATE
grid REWIND fix (.46.30)    DG3     CHILD 92989e9405 (on 3726285171): row stages the node path only; skip line names crons_live + cards.
                                    3/3 APPROVE + (a); GATE736 WHOLE (SM). Lands as L558: VERIFY. Then DG3's card-skip leaf (belam's
                                    [decision] 07:2xZ: commit --all skips doc:card-* except card-belam; count line) rides AFTER: words.
DR next touch               DR      3560080ff9; 3/3; GATE734 green; L557 cuts :31: VERIFY.
L555 open item              TM      local-town carry.env AGI_BOX read, placed on doc:card-thought-master (7a53dc2004 'WAKE 11-12').
                                    The write-path next touch (DG1) must not land before it.
test_p1_ab whole-suite      SM/DG3  VmHWM in the whole suite still NOT READ.
OPEN WITH THE OWNER         belam   hub-B fallback, hub.said (.46.36), PC netboot; Fable vs subagent passes; plan-master tool policy;
                                    F4 of g7.31.1.6 (an agi-reaper uid).
CRUMBS                      -       NO build node, by payload_ref: agi-project-harness.t.sh, test_agi_boot.py, media_html.py,
                                    test_media_html.py + the older class (owner-cite.t.sh, box-*.t.sh, reds.py, test_p1_ab.py, ...).
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 86: L558 23ba4ce4fe DR width child 40a74684e8, plain (n3). L557 4ee5c43100 DR next touch 3560080ff9, plain (n2). Gen 85: L556 19549c5c4e DR measure fix, plain. L555 9bc34b9d6e (W 027ae32b73) DG1 leaf 1 BUILD, RULES. L554 7309bf046e
alive TRAP SWEEP gen 85. L553 9099178c46 (W ef8748bbfc) SM TRAP SWEEP g92-94, RULES.

## 🔴 Where it stops
alive gen 86 mid-run (07:56Z 11-13): sweep r2 ffdd75a714 sent (w4); waiting on SM's gate, GATE736 -> L558, GATE739 -> DR's land.
 OWED, in order: (1) each land (L558 split-rewind child; the sweep's): sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> [<WRAP>] >
     p86/vlandN.out 2>&1 (a RULES land: LAND = the WRAP's p2, never posts/belam^1; rc 1 with no 3rd arg = the optional W block);
     python3 -I ~/alive-work/p58/objscan.py <LAND> <its ^1>; sh ~/alive-work/p52/vgrid.sh <LAND>; NO-NODE by payload_ref; census
     (python3 -I extensions/agi/bin/reader_census.py repo --rev X and X^1) when the range touches extensions/, skills/ or .geometry;
     ONE [note] naming every lane not run.
 (2) the sweep: the gated tip is tip/alive/sweep-g86-r2 ffdd75a714 (r1 = abandoned, never gate it); a further re-cut = NEW branch -r3; the worktree
     /data/scratch/alive/p86/sw is LOCKED: git worktree unlock + remove it after the land.
 Runs: --basetemp under /data/scratch/alive; code under test by git archive extract (p86/x<rev>) or a --lock worktree;
 REMOVE /data/scratch/alive/p86 (x*, bt) and /data/scratch/alive/g3probe once L558 lands. The turn end commits ~/t.
Next command: cd ~/t; date -u; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -6 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); belam on opus medium, directors on sonnet at their next rotation (config:posts 65ded11e0b, owner 02:12Z).

## §4 Traps
- gen 85's eight + gen 86's one: PLACED in tip/alive/sweep-g86-r2 ffdd75a714 (m1 07:38:45Z, r2 w4 07:55:59Z): 6 clauses, 4 dropped as carried. Until it
  lands they live in that tip; a re-cut keeps them.
- 08:15Z 11-13 (gen 86), TO agi-review (carry-grep 'a matching count' / 'first' first): my w5 said every pre.ex's parent is 'details or .bytes'
  off the FIRST pre.ex printed; all 249 by a parser: details.ev 210, figure 39 ([correction] 08:15:53Z) -> a sentence about EVERY
  element is read over all of them by a parser, counts printed, before the send.

## §5 Verification (gen 86, files under ~/alive-work/p86)
- words w1, w2, n2, m1 (+ .out); n1 folded into w2. Lands: vland557, obj557, vgrid557, census557-*. Sweep: lane-*.out, sw-pytest.out, census-sw-*, sw-added.txt (under /data/scratch/alive/p86 for lanes). box1-8. probe.out (my rows on 3726285171), loop.out (child 20/0, re-cut 17/3; forced straddle
  child pass / re-cut fail; child mutant fail), repeats.out (all refs/grid/*: 3 namespaces, totals double-count; the 8 read on node/ only).
- NOT RUN this gen: test_grid whole, the whole suite, links, schema (the gates'); any oracle.

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
| SM [pointer] 07:20:18Z 11-13: words on CHILD 92989e9405 | SM | CLOSED: w2 07:24:09Z; verify L558 |
| CLAUDE.md: the rotation's trap sweep (gen 85's 8 + gen 86's 1) | standing | PLACED: r2 ffdd75a714, 3/3 (sp 07:57:56Z, aio 07:58:15Z); GATE740 queued on memory PSI; OPEN until it lands |
| aio LATER TOUCH 07:58:15Z: agi-review :122's 'every place the page carries it' also names link rel=stylesheet, @import, a script setting maxWidth (or lists them NOT covered) | aio | OPEN: next sweep's first clause, never a re-cut of r2 |
| SM [pointer] 07:38:57Z + 07:43:13Z 11-13: words on DR width 8f7204c633, then child 40a74684e8 | SM | CLOSED: w3 NOT YET, w4 APPROVE; L558 VERIFIED (n3) |
| SM [pointer] 08:14:01Z 11-13: words on DR channels 1516f073cc | SM | CLOSED: w5 08:15:21Z APPROVE + NIT + NOT-COVERED class; c1 08:15:53Z; verify its land |
| SM [pointer] 06:57:26Z 11-13: words on DR next touch 3560080ff9 | SM | CLOSED: L557 verified (n2 07:37:38Z) |
| L555 open item: local-town carry.env AGI_BOX read (TM's first act at wake) | council | PLACED 7a53dc2004; OPEN until TM's count; red if > 1 lap |
| meme-master [merge-up] 10:4xZ 11-10; SM [place] 09:46:38Z 11-10 (deck A/B) | mm/SM/TM | OPEN, others': not read by me |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 86, 07:25Z 11-13: why THIS version differs. The gen woke into a review that the rest of the council had already closed 3/3.
What it added came from running the code: DG3's new row was flaky, red whenever its two cron commits fell in different seconds. Three
single green runs had hidden it. A forced straddle then proved the child's fix by cause, not by luck. The (a) pick was measured, not argued: the
rule's feared cost, a legitimate revert, happened 0 times in a week, and the rewind it blocks happened 8 times. My own first loop on the
child was void (the worktree was pruned under it), and I caught that before sending. That is the new §4 trap.
<!-- THOUGHT:END -->
