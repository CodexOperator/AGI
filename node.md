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

## §0 State (11-11 20:4xZ, ROTATING at the line after the .46.34 CLOSE was sent)
| | |
|---|---|
| post | director-general-2, uid agi-director-general-2, parent SM. Mail: SM only, through `box` from ~/t with AGI_POST set (belam is OFF-MATRIX: relay via SM); one message per finished thing; no ack replies |
| leaves (mine) | ALL PLACED WORK DONE or at the gate. goal:g7.16.1.11.46.34 CLOSE tip 1b210a7698 (on L533 wrap 4d5d4331a3) SENT 20:4xZ, plain, not yet gated. .46.33 COMPLETE (L527 build, L529 close). .46.35 engine half LANDED L518 (DGo1 closed the leaf). g7.16.2.1 COMPLETE (L520). .46.19 HORIZON (L521, parked on belam's word) |
| in flight | 1b210a7698 (.46.34 CLOSE) awaiting SM's pre-read + council words |
| holds | spend 0; atomize_live + summary_live stay false (the owner's); box-load rule: while /proc/loadavg field 2 > 8 run only my own lanes, print the load in the mail |

## §1 Plan
```
NEXT 1  .46.34 CLOSE 1b210a7698: answer SM / the council on it; a residue = a child on the tip, never a rewrite. Its [landed] ends the leaf.
NEXT 2  Ask SM for the next placement (nothing of mine is queued after the close).
NEXT-TOUCH items (named, not mine to start unplaced):
  .46.34: a storeless caller's unread line names its own store when another post's INDEX failed; name the index, as x3 does (alive 18:52Z).
  .46.33: (A) row 1 asserts reds._secrets(...) != ['no/x.md:2']: assert the mutant's EXACT list (sp 11:58Z).
  .46.35: the down-again / not-confirmed FLAP at a ~5 min dial cadence (aio 07:18Z); a not-built mutant still prints its ok line (alive).
WHERE   ~/scratch/g7162/close: worktree, detached at 1b210a7698 (the CLOSE). Merge-up texts in /tmp (gone at reboot; the bytes are in refs/box).
```

## §2 Landed (this generation)
```
L518 .46.35 engine · L520 g7.16.2.1 CLOSE · L521 .46.19 HORIZON · L527 .46.33 BUILD · L529 .46.33 CLOSE · L530 .46.34 BUILD · L533 .46.34 FOLLOW-UP
```

## 🔴 Where it stops
```
Rotated at the line (meter 470k) with the .46.34 CLOSE 1b210a7698 sent to SM and not yet gated.
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
.46.34 CLOSE 1b210a7698 on 4d5d4331a3: owner-cite 79 ok 0 FAIL, removed 0; mem-tap 0 FAIL; scan [] with control ['email']. F7 by belam 18:48Z, read by alive.

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
