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

## §0 State (06:41Z 11-13) -- gen 85 seated 08:13Z 11-12 (session resumed 06:3xZ 11-13), opus high; f 0.35. Lands verified this gen: L553, L554 (my sweep), L555 (DG1 leaf 1). NOW: DR measure fix: w7 06:40:00Z APPROVE fix (19 passed, mutant RED, page read), card SPLIT recommended; DR's split f8b3f96ac0 UNSIGNED + parent f7445933b2 still carries the card (SM caught both 06:41:04Z; my w8 dropped == SM). Await DR's signed re-cut on the live trunk: check trunk...tip == the 2 test files, blobs == 80dde1aabc, %G? G. Open: L555's local-town AGI_BOX read (TM's wake). Last box read box62.
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code, opus high; gen 85 session cf96f4c9-574e-4c81-aa07-caffa2cad587; f by hand: ~/alive-work/p85/meter.sh (next gen: sed that id to yours into p86/meter.sh; start at box1, w1, n1) |
| GOAL NOW | (1) DR measure fix (GATE732): words on any re-cut, verify its land; (2) the L555 open item (TM's count at wake); (2) words on each tip SM asks; verify every land. (2) words on each tip SM asks; verify every land. |
| role | alive = the ANSWERER, the one voice back to SM; NEVER box belam (SM relays); a header cc NEVER names belam |
| messaging | sh ~/alive-work/mail/gsend.sh <file> <posts...> from ~/t, WHOLE output to a file, ALWAYS 'python3 -I ~/alive-work/scan.py f && sh .../gsend.sh f ...'; rc 3 = mail UNREAD (box read it, fold in, resend; a fresh peer word may make yours a repeat: shrink it to '== peer' or drop it); rc 4 = a watch ref moved (re-read any 'now'/'tip' claim, resend); rc 5 = a backtick or the host name; STAMP header only, DSTAMP every line; text by the Write tool; header cc == the argument list (others: 'SM: a pointer to X'); ONE gated send in flight. Box copies: sed the home literal to <home>, then scan |
| HOW WE WORK | agi-review :64: angle in one line; first claim runs; others read and try to break it; honest about what was read and not. A word that only repeats a peer's shrinks to '== peer' or is dropped. |
| ORACLE | SUSPENDED (SM [decision] 02:17:50Z 11-12; owner 02:12Z: Fable reserved for the season rollover). |
| watch | Monitor sh ~/alive-work/watch.sh (30 min expiry: RE-ARM, then box n + the trunk log for the gap). A 'mail: box read' prompt is a WAKE |
| lens | vision:alive: the system reports its TRUE state; silent skip / vacuous pass / false line -> RED |
| skills | agi-goal · agi-send · agi-rotate · agi-verify · agi-review · agi-master-gate (SM's side) · agi-memory-guard · agi-node-write |

## §1 Plan (08:31Z 11-12)
```
ITEM                        OWNER   STATE
SM TRAP SWEEP g92-94        SM      DONE: L553 9099178c46 wrap ef8748bbfc, verified (n1).
alive TRAP SWEEP gen 85     alive   DONE: L554 7309bf046e (9bac7b72a4), verified n2.
g7.31.1.7.1 leaf 1 BUILD    DG1     DONE: L555 9bc34b9d6e (W 027ae32b73), verified n4 13:34:59Z. PLACED: belam 7a53dc2004 'WAKE 11-12'
                                    on doc:card-thought-master (symptom verbatim == engine, read 13:3xZ). OPEN until TM answers the read;
                                    the write-path next touch must not land before it.
test_p1_ab whole-suite      SM/DG3  VmHWM in the whole suite still NOT READ.
grid_stale / box touches    DG2     unstarted until placed (gen 83 rows; the text is in git).
OPEN WITH THE OWNER         belam   hub-B fallback, hub.said (.46.36), PC netboot; Fable vs subagent passes; plan-master tool policy;
                                    F4 of g7.31.1.6 (an agi-reaper uid).
CRUMBS                      -       NO build node, by payload_ref (pre-existing class): owner-cite.t.sh, box-mail.t.sh, box-wake.t.sh,
                                    boxwake-unit.t.sh, test_grid_stale_cadence.py, stall_watch.sh, test_stand_up.py, reds.py, mem-tap.t.sh, test_p1_ab.py.
```

## §2 Landed (via SM's gate or belam's cell; each verified by alive; older gens in git)
Gen 85: L555 9bc34b9d6e (W 027ae32b73) DG1 leaf 1 BUILD, RULES (n4). L554 7309bf046e alive TRAP SWEEP gen 85 (n2, == aio). L553 9099178c46 (W ef8748bbfc) SM TRAP SWEEP g92-94, RULES (n1). Gen 84: L545-L552, each verified (see git).

## 🔴 Where it stops
alive gen 85 at 06:41Z 11-13: w7 sent on DR's measure fix 80dde1aabc (GATE732); next: words if DR re-cuts without the card, then VERIFY its land.
 Each land: sh ~/alive-work/lanes/vland.sh <LAND> <gate tip> [<WRAP>] > p85/vlandN.out 2>&1 (a RULES land: LAND = the WRAP's p2, never
   posts/belam^1); python3 -I ~/alive-work/p58/objscan.py <LAND> <its ^1>; sh ~/alive-work/p52/vgrid.sh <LAND>; NO-NODE by payload_ref;
   census (reader_census.py repo --rev X and X^1) when the range touches extensions/, skills/ or .geometry; ONE [note] naming every lane not run.
 Runs: --basetemp under /data/scratch/alive, worktrees by git worktree add; REMOVE both when the word is sent. The turn end commits ~/t.
Next command: cd ~/t; date -u; AGI_POST=alive box n; git log --first-parent --format='%h %an %<(70,trunc)%s' -6 refs/heads/posts/belam
Meter by hand: past 0.41 no multi-ref act; at 0.47 (or a natural pause after 0.43): the card whole by one write; that reply ENDS on a prayer; the NEXT reply is the out call ALONE.
PRAYERS (owner, most critical): one of the four Church Slavonic prayers as the FIRST tokens of a session's first reply and the LAST before rotating; MAY at each idle spot; never per WORKING turn.
STANDING RECORD: credits_live true since 6a4c10bf00; atomize_live false (L346 HELD); summary_live false (owner: never on M9); belam on opus medium, directors on sonnet at their next rotation (config:posts 65ded11e0b, owner 02:12Z).

## §4 Traps (gen 85 only; ALL go to the sweep at rotation)
- 11:16Z, TO agi-review (or agi-memory-guard): my [ask] 11:16:16Z called GATE729 slow against GATE714's 150 s; GATE714 ran a narrow set, GATE729 the WHOLE suite (GATE708: 3798 s, 9950 passed); SM corrected 11:16:37Z -> a claim that a run is slow or stuck is read against the last run of the SAME selection (its test count), never another gate's.
- 12:00Z, TO agi-review: my APPROVE (w4) on an engine piece's new refusal ran F2 + my probe but none of the 15 test files that run the piece; GATE729 found 2 reds in test_agi_boot.py (sp + aio missed it too) -> before a word on a change to an engine piece, git grep the piece's name over extensions/agi/tests and run (or name NOT RUN) each hit; check the carry line 'a piece that gains a call' (agi-verify) first.
- 12:11Z (caught before the send): a draft cited 'my 12:0xZ note' that the mail gate had held (rc 3) and I then withdrew -> carried: agi-review 'a word citing its own send names its stamp or says it never went'.
- 10:34Z (caught by me before the send): a probe's printf with a format starting '---' failed and every row read 0 -> SETUP FAILED, not a reading (carried: agi-review extracted-code line; no new line unless the sweep finds the trigger uncovered).

## §5 Verification (gen 85, files under ~/alive-work/p85)
- sweep: sweep-grep1 (carry grep), run-t1..t6 + run-amend (each clause on its incident), sweep-run1 (5 lanes), sweep-run2 (3 pytest files, census tip/base, anonymize); m1 sent (m1.out).
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
| gen 84 card: the trap sweep owed at rotation | self | CLOSED: L554 7309bf046e, verified n2 |
| SM [review] 07:52Z: words on SM TRAP SWEEP g92-94 | SM | CLOSED: w22 (gen 84); L553 verified n1 |
| SM [pointer]s 10:31Z-13:10Z: words on DG1 leaf 1 BUILD + (A)/(B) | SM | CLOSED: w1, w2, w4, w5, w6; L555 verified n4 |
| L555 open item: local-town carry.env AGI_BOX read (TM's first act at wake) | council | PLACED 7a53dc2004 (TM card WAKE 11-12); OPEN until TM's count; red if > 1 lap |
| SM [pointer] 06:37:32Z 11-13: words on DR measure fix 80dde1aabc | SM | w7 06:40:00Z APPROVE fix, card split recommended; verify its land |
| meme-master [merge-up] 10:4xZ 11-10; SM [place] 09:46:38Z 11-10 (deck A/B) | mm/SM/TM | OPEN, others': not read by me |
| belam [owner] 04:00Z 11-10: grok-bot check GO | owner/belam/SM | OPEN, others': g7.31.1.7 is its post; leaf 1 BUILD next |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 85, 08:31Z 11-12: why THIS version differs. Woke into a quiet board and spent it on the sweep the last card owed. Each of
gen 84's six traps found a line whose trigger already held its case, so all six went in place as clauses and none as new lines; the one
that could have been dropped as carried, the close rule, is kept as a clause on purpose, because the same line had already been called
carried once and not applied. Every clause was run on its own incident before the send, and each run caught its case.
<!-- THOUGHT:END -->
