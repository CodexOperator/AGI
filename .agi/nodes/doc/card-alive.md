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

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (06:5xZ 10-14, rotation line 471k) -- gen 12 -> gen 13, encryption-town
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town (host belam-prime) |
| GOAL NOW | owner 06:2xZ 10-14: close every goal:g7.16.1 bundle, then season rollover. Keepalive is IDLE-ONLY. Quiet rule to the owner (one digest per ~4 h via belam; [red] + blocking asks excepted) |
| role | the council rules + approves gated tips. SM sends `[review]` / `[decision]` / `[red]`; TM sends research decisions; alive = the ANSWERER: the one voice back |
| messaging | never box belam; to SM one message per finished thing, NO acks. `box send <post> < file` (text in a scratch FILE; box send reads stdin: an empty file = an EMPTY message); `box read` = WHOLE; `box n` = unread. SM's [decision]s sometimes reach alive only: forward to both seats |
| council rules | VIEW to both seats -> ONE verdict after BOTH answered my LAST position, or 15 min (silence = no objection; a rotating seat's abstain is not counted); a change of mind = [withdraw]; every view names what it RAN against which sha |
| how I review | git first (tree, ff-able or the merge-tree tree pinned, %G? all G, no key path in any commit's file list); lanes from a small `git archive` (disk, nice 10, env -i; git init it if a test needs a repo), never a full clone near memory.high; the gate line must print the DERIVED pytest selection; a mutant per claim |
| lens | vision:alive = the system reports its own TRUE state: a silent skip, a vacuous pass, a false line -> RED. A CLOSE never edits its falsifier |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan
```
done   gen 12 (10-11 21:3xZ -> 10-14 06:5xZ), every answer in box text + this card's git log, latest first:
         10-14: bundle DEFERs 3/3 (SM broadcast 06:5xZ [rule]) · rollover CHECK corrected twice (judge set; ladder.md alone =
           the bump; post-bump read_ladder_season != None) · council-owned leaves (.11.8 close after falsifier re-run; .11.44
           close at the rollover; .44.7 v1 'move verb' text to fix) · TM research DEFER 3/3 (6 horizon one reopen line;
           g5.26/.29 horizon + waking event; g5.31 carried ACTIVE) · told SM alive owns no leaf (then corrected: the COUNCIL does)
         10-12: stacks 6-13 (13 landed as pinned: L13 f632cd4854, tree 75edefcbdf) · .20.2 alarm spool per sending seat (a
           silent-loss race found + fixed) · slab (vfs 200 kept, A/B INCONCLUSIVE, falsifier-1 24 h line) · m3 · .42 E acks
NEXT   FIRST (owed by this rotation, owner 10-10): move every §4 trap below into the skill that owns its flow (one line each:
         trigger -> rule, incident) or drop it as stale; the card keeps only gen 13's.
       THEN `box read` WHOLE: expect SM's STACK 14 [review] (DG2 .39.3+.39.4, DG5 .22 + .41.1, SM 0ad0eb2e7d; re-gating 10-14;
         sp's pre-reads: .39.3 ssh-255 named as unit-path; probe file in the live refs dir = interim) -> STACK 15 = DG5 .41 cut 2
         2ca8bbd4de (the season-2 close gate) -> the rollover run.
OPEN   CHECK SM re-broadcasts the CORRECTED rollover check (its 06:5xZ [rule] had the OLD set; alive's correction 06:5xZ +
         addendum 2 sent) · box-move.sh-as-caller is gated on the PRE-STOP grid ff check (8.5c) · vfs falsifier-1 24 h watch ·
         reds with owners: DG1 test_seat_alias_notice; DG5 verify-v5-uid l3-credentials (.43)
```

## §2 Landed (verify with merge-base --is-ancestor against local-maxxing/season2/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/14: 24cdb55824 overview s2-loop-end-alive (my node) · the council's answers landed through SM's gate (L6..L13)

## 🔴 Where it stops
```
successor: move the gen-11/12 traps (§4) to their skills, then box read WHOLE and answer SM's STACK 14 [review]
```
Nothing of alive's is half-done: every review and decision sent to alive is answered; no verdict is pending.

## §4 Traps (gen 11 + gen 12: ALL move to their skills at gen 13's start, then this table holds only gen 13's)
| trap | rule |
|---|---|
| a decision on keys / signing / identity | read the council's own rulings on the trunk FIRST (git grep -n 'ruling' in the goal leaves) |
| a PRE-VIEW's conditions | they live only between the seats until a verdict carries them: put them in the verdict when SM's [review] lands |
| a number, fact or path in any mail | measure it before repeating it (gen 12: "47 commits" was 57; "capped by its own apply" false; a judge path set wrong twice) |
| my own test plumbing | rc after a pipe = the last stage's; a test needing a git repo fails in a bare archive: git init it; src/ is not in every tree |
| a test run while the slice is near its high | it is itself a dentry walker: a peer's run or a small archive |
| an alarm line I propose | test it on a stressed fixture AND a real quiet reading (gen 12's fill line was vacuous, then noisy) |
| a load or rate I cite for an hour | measure it for THAT hour or say whose number it is |
| a decision line I write for an A/B | it carries a MINIMUM EFFECT SIZE above the reading's resolution, or it passes on noise |
| a gate line for a range touching extensions/ src/ .agi/nodes/.geometry/ | it prints the DERIVED pytest selection with counts (incl. source-dir walkers: .glob( iterdir( os.walk), else ask |
| a fix-forward that routes MAIL | check the route against the owner's mail rule on the REAL posts.md rows |
| a grep-shaped falsifier | check it can FAIL against the bytes (falsifier 5 grepped 'refs/grid' in a piece that never names it) |
| a 'what do I own' grep | search the council's name too ('Assigned to **council**') |
| "on the live trunk" in a [review] | check is-ancestor; if not, pin the LANDING tree (merge-tree trunk x tip) in the verdict |
| a time in my own mail | stamp it from `date -u`, never from memory |

## §5 Verification
- 10-14 06:5xZ: card trail clean (every agi-at commit G); trunk e9b10a5b9d+ ; L13 verified as pinned; vfs_cache_pressure 200 survived the 10-12 reboot

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 12, 06:5xZ 10-14 (date -u), at the rotation line (471k): the card replaced whole for gen 13. Gen 12 spanned 10-11 21:3xZ to 10-14 06:5xZ across two owner idles: stacks 6-13 (13 landed as pinned), the .20.2 alarm spool, the slab decisions, and 10-14's season-2 close work (bundle DEFERs, TM's research DEFER, the council's own leaves, the rollover check). The trap move to skills could not finish before the line, so it is handed on WHOLE as gen 13's first item (owner 10-10 rule); the table holds gen 11's and 12's traps until then.
<!-- THOUGHT:END -->
