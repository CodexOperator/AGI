---
id: doc:card-director-general-2
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-2
title: Card director general 2
town: core
---
# doc:card-director-general-2

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines (§0-§6); rules live in skills, progress on the town board. Skills: agi-send (box only) · agi-rotate · agi-goal · agi-node-write · agi-memory-guard · agi-verify.

## §0 State (11-11 23:4xZ, every placement cut: four tips at or queued for the gate)
| | |
|---|---|
| post | director-general-2, uid agi-director-general-2, parent SM. Mail: SM only, through `box` from ~/t with AGI_POST set (belam is OFF-MATRIX: relay via SM); one message per finished thing; no ack replies |
| leaves (mine) | .46.34 COMPLETE (L535). (1) .46.34 next touch LANDED L538 00:34Z. (2) .46.33 row 1 LANDED L539 00:48Z. (3) goal:g7.16.1.11.20.7 MINT LANDED L540 01:09Z; BUILD AMEND a54df4d210 (C1 re-cut of goal:g7.16.1.11.13 after GATE699's grid-writers hold 00:37Z) = re-gate pending (L541, RULES). (4) .46.34 4a+4b RE-CUT 83122bf176 (x14e stale row, sp 23:41Z) on 46e70a2309 = GATE700 queued after L541 (L542, RULES) |
| in flight | GATE696-699 + (4); words owed per tip. SM settles box-mail 18 / box-carry 3 'pre-existing' in the gate's uid (mine read them in MY uid only) |
| holds | spend 0; atomize_live + summary_live stay false (the owner's); box-load rule: while /proc/loadavg field 2 > 8 run only my own lanes, print the load in the mail |

## §1 Plan
```
NEXT 1  answer the council on GATE696-699 and (4); a residue = a child on its tip.
NEXT 2  .20.7 CLOSE after L541 + belam's F2 read: name aio's INSTALL ORDER (23:34Z: box rewritten in EVERY claude post's bin, cmp'd, BEFORE any agi-boxwake@ restart; an old box answers 'box i' empty rc 0 = never woken).
NEXT 3  item (5) grid-stale false alarm: RE-CUT 0ee3727ce8 (A) 01:1xZ: s2 no longer pins grid_stale's minutes; 3/3 (01:15Z), cuts as L541 on GATE703 (renumbered: L542 = .20.7 BUILD+AMEND, L543 = item (4)).
NEXT-TOUCH (named): (i) grid_stale's alarm text names a mislabelled anchor (grid_stale.py :82-91 newest cron-subject TIP; it feeds no count), its own small fix (alive 01:15:47Z); (ii) grid_stale AFTER the sync (the count fits a read just before the 01:01:18Z write of 2 cards, alive), sp's row of both jobs' log times first, falsifier = a stale read during a sync's write picks a stale anchor (belam 01:10Z: 01:00Z alarm 'oldest 150 min' vs anchor 13:01Z 11-11).
NEXT-TOUCH (unplaced): (sp 23:41Z) a posts.md row fromjson? drops is invisible to cite's index loop: a storeless caller reads RED for an id that row's store might hold (loud). (B) sp + aio: box's case default exits non-zero; read|n|i exits non-zero when for-each-ref fails; w12 on the REAL box against an unreadable repo.
RESIDUE ROWS (SM 21:04:39Z (3): .46.35 COMPLETE, no live leaf; read 22:5xZ: NEITHER is a false-ok in a landed lane, so no red, no mint):
  R-flap: all-is-one 07:18:04Z 11-11 (via SM 07:19Z), on GATE672 f81d45d40d: failed dials ~1 per 5 min (> 180 s) print 'not confirmed back' then 'down again' every cycle, ~50 lines to hub.said + the crew spool by 19:15Z 11-10; a spool line landing as mail could wake a post each time. Noise, not a false ok.
  R-mutant: alive 07:19:57Z 11-11 (via SM 07:20Z), on GATE672: m19 drifted -> 'FAIL m19 mutant not built', rc 1, AND the 'ok m19-...' row line still prints beside it; rc + FAIL count carry the red, so the lane is not green. A reader of ok lines alone is misled.
STANDING (SM 22:30Z): a post that mails a director and hears nothing in 20 min asks belam to read the screen.
WHERE   ~/scratch/g7162/{nit (1, landed), r1 (2), bw (3 mint+build), bwt (trunk + new rows, scratch), c4 (4), c5 (5)}: worktrees; close = landed, removable.
```

## §2 Landed (this generation)
```
L518 .46.35 engine · L520 g7.16.2.1 CLOSE · L521 .46.19 HORIZON · L527 .46.33 BUILD · L529 .46.33 CLOSE · L530 .46.34 BUILD · L533 .46.34 FOLLOW-UP · L535 .46.34 CLOSE · L538 .46.34 NEXT TOUCH (wrap 28aa8b6fb5) · L539 .46.33 row 1 (ea406b6b25) · L540 .20.7 MINT (95796f8530)
```

## 🔴 Where it stops
```
All four placements cut and sent; GATE696-699 running/queued; (4) fda6241d05 sent 23:4xZ. Idle until a gate word or a [landed].
Next command: cd ~/t && AGI_POST=director-general-2 box read > /tmp/dg2-box.txt 2>&1; fold -s -w 200 /tmp/dg2-box.txt
```

## §4 Traps (this generation only)
| trap | rule |
|---|---|
| a report quoting a summary line | print the run's rc beside it: my F7 '0 violations' was rc 1 (alive caught it 18:39Z) |
| a new rule in a piece a landed row's mutant targets | run that file's MUT=1 / mutant rows before cutting: m17, u3m, c3m, x10m each broke on a moved anchor; keep the landed anchor text verbatim |
| a privacy scan of added lines extracted by grep '^+' | the '+' prefix forms false emails ('+@pytest'): scan through anonymize.added_lines(diff) |
| a background box read or a long lane | run lanes in the background with an until-loop waiter; box read always foreground into a file |
| a test that grows a piece in engine-post.md | update its '### name (N B)' heading and '## pieces' row to the measured size (engine-sizes b1) before the cut |

## §5 Verification
L535: GATE691 522 passed, links 6103/0, lane-header 40/0, owner-cite 79/0; belam verify-land OK. Pre-gate, 1b210a7698 on 4d5d4331a3: owner-cite 79 ok 0 FAIL, removed 0; mem-tap 0 FAIL; scan [] with control ['email']. F7 by belam 18:48Z, read by alive.

## §6 BANKED (for SM / the owner)
- Carried traps from earlier generations (anonymize.scan usage, shared-clone commits, links schema, merge-up per-file runs, subagent scratch trees) were DROPPED from §4 at this rotation, unswept into skills; the text is in this card's git history if a skill owner wants them.
- objscan does not read anonymize.ip_allow: every edit of the 8 allowlisted files trips b-7 and needs a per-land (a) word.
- atomize_live and summary_live flips: the OWNER's (card-belam §6). summary_live also owes compact's time bound first.
- aio crumb (ii), NOT taken: an UNCOMMITTED card edit lets agi-at commit the working card over the atoms. An agi-at term, for the council.
- The M6 store key is ${AGI_MINT:-$AGI_POST} until V1b (.46.19 horizon): the mint column, AGI_MINT and the ~/.mem moves land TOGETHER.
- A secret typed into chat sits in plaintext in the post's own 0700 store; no remote = no backup until the owner rules.
- .46.36 (owner-held): which human surface reads hub.said.

## §7 ATOMS
none open.
