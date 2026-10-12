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

## §0 State (05:2xZ 10-12) -- gen 12, RESUMED (owner "go" via belam/SM 05:1xZ; box rebooted 05:00:51Z), meter f ~0.38
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town (host belam-prime) |
| RESUME | the 04:2xZ idle order was LIFTED 05:1xZ (owner "go"); quiet rule to the owner stands (ONE digest per ~4 h via belam) |
| role | the council rules + approves gated tips (owner 21:5xZ 10-10). SM sends `[review <sha>]` / `[decision]` / `[red]`; alive = the ANSWERER: the one voice to SM |
| messaging | OWNER 20:2xZ 10-11: never box belam (only [red] or a BLOCKING owner ask, at once); to SM one message per finished thing, NO acks. `box send <post> < file` (text in a scratch FILE); `box read` = read WHOLE; `box n` = unread |
| council rules | VIEW to both seats -> ONE verdict to SM after BOTH answered my LAST position, or 15 min (silence = no objection; a rotating seat's abstain is NOT counted). A change of mind = [withdraw]. Every view names what it RAN against which sha, or "none" |
| how I review | git-only first (tree, ff-able = trunk ancestor, %G? all G, no key path in any commit's file list); lanes from a small `git archive` (disk, nice 10, env -i), never a 30k-file clone while agi.slice is near memory.high; a mutant per claim |
| lens | vision:alive = the system reports its own TRUE state: a silent skip, a vacuous pass, a false line -> RED |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan
```
done   gen 12 (10-11 21:3xZ -> 10-12 04:0xZ), every answer to SM in box text + this card's git log, latest first:
         stack 12 db25627954: RETURN DG5 4037d8b420 ALONE (agi-sync conflict box walks to belam for alive/aio/sp/SM/TM: owner
           rule; OUR stack-8 FF2 caused it) -> stop below role prime_director, notice only + stamp; APPROVE rest (closes the red)
         capsule x refs/grid: (b) TRANSPORT not author; falsifier 5's grep was VACUOUS -> rows g4a/g4b (+ c pre-stop = a GATE on
           box-move.sh-as-caller); doc v5 ff02306eea
         gate-selection rule (03:1xZ): DERIVED pytest list at the gate sha + full suite once per landed stack (SM adopted, stack 12)
         stacks 6-11 APPROVE (6: fill line fix; 7: capsule D1-D4 accepted, FF1 fat bundle 287 MiB, FF2 agi-hook; 8: FF1 thin+atomic,
           move = box-move.sh as caller; 9-11: the fix-forwards MET); .20.2 alarms: spool per sending seat (race found + fixed)
         decisions: alarm signer (spool per seat) · m3-overlap (5 % cell, triggers T1/T2) · slab (a)+(b)+(c) · vfs 200 KEEP,
           A/B INCONCLUSIVE, falsifier 1 24 h line · .42 E acks (home path -> ~, foreign-row log cap in-uid + mkdir)
NEXT   stack 13b [review] from SM (gate g397 @ 3fe030e570: DG4 63b21a5b90 + DG5 7970370e55 + DG2 e52540c669 on 67730b8fb7).
         PRE-VIEW sent 05:2xZ: DG5's below-Prime stop MET (0 of 33 rows -> belam); flag 3fe030e570 %G? = N (gate tip must be G).
         + aio: trunk holds capsule doc v2 (fcbd68c214, 0 'transport') while .13 + capsule.t.sh cite v5: carry asked (13b or 13c)
         then: .41 cut 2 (season-2 close gate, DG5) · DG3 i10 fix
OPEN   gates the council set: box-move.sh-as-caller needs the PRE-STOP grid ff check (row 5c) · vfs falsifier 1 24 h watch
         (revert line in the .40.1.1 THOUGHT) · DG4's .13 N7 cites doc v5 (lands at aio's next sync)
```

## §2 Landed (verify with merge-base --is-ancestor against local-maxxing/season2/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/12: 24cdb55824 overview s2-loop-end-alive (my node) · the council answers above landed through SM's gate (L6..L11)

## 🔴 Where it stops
```
RESUMED: `box read` WHOLE -> answer SM's stack 13b [review] (pre-view in §1 NEXT); check the gate tip is %G? G
```
Nothing of alive's is half-done: every review and decision SM sent is answered; no verdict is pending at SM.

## §4 Traps (gen 11 + gen 12; to their skills at my next rotation, owner 10-10)
| trap | rule |
|---|---|
| a decision on keys / signing / identity | read the council's own rulings on the trunk FIRST (git grep -n 'ruling' in the goal leaves) |
| a PRE-VIEW's conditions | they live only between the seats until a verdict carries them: put them in the verdict when SM's [review] lands |
| a number or fact in SM's mail | measure it before repeating it (gen 12: "47 commits" was 57; "capped by its own apply" was false) |
| my own test plumbing | rc after a pipe = the last stage's; a test needing a git repo fails in a bare archive: git init it; src/ is not in every tree |
| a test run while the slice is near its high | it is itself a dentry walker (gate suites +27 MiB): a peer's run or a small archive |
| an alarm line I propose | test it on a stressed fixture AND a real quiet reading (gen 12's fill line was vacuous, then noisy) |
| a load or rate I cite for an hour | measure it for THAT hour or say whose number it is (gen 12 cited DG1's load 13 as the before-hour's) |
| a decision line I write for an A/B | it carries a MINIMUM EFFECT SIZE above the reading's resolution, or it passes on noise |
| a gate line for a range touching extensions/ src/ .agi/nodes/.geometry/ | it must print the DERIVED pytest selection with counts, else ask before the word (stacks 7-8 went RED on grid_writers) |
| a fix-forward I write that routes MAIL | check the route against the owner's mail rule on the REAL posts.md rows (stack-8 FF2 sent 5 posts' conflicts to belam) |
| a grep-shaped falsifier | check it can FAIL against the bytes (falsifier 5 grepped 'refs/grid' in a piece that never names it) |
| a time in my own mail | stamp it from `date -u`, never from memory |

## §5 Verification
- 10-12 04:3xZ: card trail clean (every agi-at commit G); trunk tip 21f5d44a35; agi.slice ~4.5-5.1 GiB through the night (high 5120)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 12, 04:3xZ 10-12 (date -u): the card replaced whole for a COLD resume, on the owner's idle order (04:2xZ via belam/SM). Gen 12 answered SM's alarm-signer decision and every stack (6-12) and decision of the night, mostly 3/3; the recurring lesson is in §4: four times a check passed without being able to fail (a fill line, an A/B line, a grep falsifier, a fixture-only mail route). Nothing is in flight; the queue for the resume is in §1 NEXT.
<!-- THOUGHT:END -->
