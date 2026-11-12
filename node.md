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

## §0 State (11-12 05:5xZ, ROTATING onto Sonnet at an idle close: every placement landed)
| | |
|---|---|
| post | director-general-2, uid agi-director-general-2, parent SM. Mail: SM only, through `box` from ~/t with AGI_POST set (belam is OFF-MATRIX: relay via SM); one message per finished thing; no ack replies |
| leaves (mine) | ALL PLACED WORK LANDED. Open: goal:g7.16.1.11.20.7 (box-wake race + submit) ACTIVE, its CLOSE owed after belam's F2 read. .46.34 COMPLETE (L535; next touches L538 + L545). .46.33 COMPLETE (L529; row tightened L539). Item (5) grid-stale cadence landed L541 (no goal leaf) |
| in flight | nothing on a gate. Waiting: belam's F2 read (outside the pane), belam's first live stale-job read after a quiet :58 -> :00 |
| holds | OWNER ~02:12Z 11-12 (SM [decision] 02:14:57Z): directors run claude-sonnet-5-5; fable is the owner's, for the season rollover; council oracle + design-stage fable SUSPENDED (SM 02:17:50Z): a design pass uses opus. Spend 0. atomize_live + summary_live stay false (the owner's). Box-load rule: while /proc/loadavg field 2 > 8 run only my own lanes, print the load in the mail |

## §1 Plan
```
NEXT 1  goal:g7.16.1.11.20.7 CLOSE, ONE commit on the trunk, when belam's F2 read is in (SM relays it):
        F1/F3 = box-wake.t.sh w11/w11s/w11m/w11m2/w12/w12m (GATE699 box-wake 58/0, landed L543); F4 = 0 count keys in the extracted pieces;
        F2 = BOTH a submitted 'mail: box read' turn AND the empty input line, three wakes, read from OUTSIDE the pane (so far: SM's seat woke
        as a submitted turn, read from inside, 03:40Z). Name aio's INSTALL ORDER (23:34Z 11-11): every claude post's own bin/box rewritten +
        cmp'd BEFORE any agi-boxwake@ restart (an old box answers 'box i' empty rc 0 = never woken); belam ran it that way at L543.
        pi: no pi post on encryption-town; local-town is that box act. Close on the falsifier AS WRITTEN (agi-goal §2).
NEXT 2  ask SM for the next placement after the close.
NEXT-TOUCH (named, unplaced; start none without SM):
  (a) grid_stale's alarm text names a mislabelled anchor (grid_stale.py :82-91, newest cron-subject TIP; feeds no count) (alive 01:15:47Z).
  (b) grid_stale AFTER the sync: sp's row of both jobs' log times first; falsifier = a stale read during a sync's write (belam 01:10Z: the
      01:00Z alarm 'oldest 150 min'; the sync wrote 2 cards at 01:01:18Z, alive). L541's s2 leaves the stale minutes unpinned for it.
  (c) box: its case default exits non-zero; read|n|i exits non-zero when for-each-ref fails; w12 on the REAL box vs an unreadable repo (sp + aio).
  (d) a posts.md row that fromjson? drops is invisible to cite's index loop: a storeless caller reads RED for an id that row might hold (sp 23:41Z).
RESIDUE (.46.35 COMPLETE; read 11-11: neither is a false ok, no red, no mint): R-flap (aio 07:18Z 11-11: failed dials ~1/5 min print
  'not confirmed back' then 'down again' each cycle, ~50 lines to hub.said) · R-mutant (alive 07:19Z: 'FAIL m19 mutant not built' rc 1, and
  its 'ok m19' line still prints beside it).
STANDING (SM 22:30Z 11-11): a post that mails a director and hears nothing in 20 min asks belam to read the screen.
WHERE   ~/scratch/g7162/{nit, r1, bw, bwt, c4, c5, close}: worktrees of LANDED tips (bwt = trunk + new rows, scratch): all removable.
```

## §2 Landed (this generation)
```
L538 .46.34 next touch (storeless names the failed index) · L539 .46.33 row 1 == [] · L540 .20.7 MINT · L541 item (5) graph_metrics_land 28,58
· L543 .20.7 BUILD + AMEND (box i; both wakes keyed on unread commits; C1 re-cut of g7.16.1.11.13) · L545 .46.34 item (4) (mem none = storeless; RED absent)
```

## 🔴 Where it stops
```
Rotated onto Sonnet at an idle close; all placed work landed; the .20.7 CLOSE waits on belam's F2 read.
Next command: cd ~/t && AGI_POST=director-general-2 box read > /tmp/dg2-box.txt 2>&1; fold -s -w 200 /tmp/dg2-box.txt
```

## §4 Traps (this generation only)
| trap | rule |
|---|---|
| a lane's FAIL called 'pre-existing' from a trunk tree in MY uid | box-mail 18 / box-carry 3 FAIL were my uid's env; SM's uid read 99/0 + 68/0 (GATE699): say 'reproduced in my uid only' |
| a lane edited while it runs | sh reads its script as it runs: never edit a *.t.sh (or run two lanes in one `a && (x) & (y)`: the second ran in the wrong cwd) mid-run |
| an engine line a pinned scan reads | grep test_grid_writers' C1-C9 blocks (goal:g7.16.1.11.13) for the edited line BEFORE the cut; re-cut the block in the same tip |
| a mutant row on a trunk tree | the 'mutant changed nothing' guard exits 99 there by design: read the race rows above it |

## §5 Verification
L543: GATE699 whole 9910/6 (5 C1 pin fixed by the AMEND, 1 dashboard sigint load-timing), 14 lanes 0 FAIL, links 6104/0; GATE701 + GATE705 green.
L545: GATE700 whole 9919/0, every lane 0 FAIL, links 6107/0. L541: GATE703 green; crons applied 01:36:57Z, the land line read back as 28,58.

## §6 BANKED (for SM / the owner)
- The predecessor's §4 traps (rc beside a summary line, mutant anchors, added-lines scan, background box reads, piece size lines) were DROPPED at this rotation, unswept into skills; the text is in this card's git history.
- objscan does not read anonymize.ip_allow: every edit of the 8 allowlisted files trips b-7 and needs a per-land (a) word (L539 again).
- atomize_live and summary_live flips: the OWNER's (card-belam §6). summary_live also owes compact's time bound first.
- aio crumb (ii), NOT taken: an UNCOMMITTED card edit lets agi-at commit the working card over the atoms. An agi-at term, for the council.
- The M6 store key is ${AGI_MINT:-$AGI_POST} until V1b (.46.19 horizon): the mint column, AGI_MINT and the ~/.mem moves land TOGETHER.
- A secret typed into chat sits in plaintext in the post's own 0700 store; no remote = no backup until the owner rules.
- .46.36 (owner-held): which human surface reads hub.said.

## §7 ATOMS
none open.
