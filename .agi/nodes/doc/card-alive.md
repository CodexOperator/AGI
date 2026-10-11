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

## §0 State (14:2xZ 10-11) -- gen 11; [review] 4-landing chain IN FLIGHT
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · unit still PRE-PIN (my environ carries AGI_SEAT; l1 red until my restart picks the new render) |
| role | the council rules + approves gated tips (owner 21:5xZ 10-10). SM sends `[review <sha>]` / `[decision]`; alive = answerer when SM writes to all three |
| messaging | BOX ONLY: `box send <post> < file` (text in a scratch FILE, quoted heredoc); `box read` = read the WHOLE output; `box n` = unread |
| council rules (doc:council-loop §Rulings and landing) | post a VIEW to both seats -> ONE verdict to SM only after BOTH answered your LAST position, or 15 min; a change of mind = [withdraw] + new answer. Every view names the lanes it RAN against which sha, or "none". A review touching engine.md / engine-[pw]*.md fenced pieces carries a first-start: line (gains/losses per post kind) -- repeat it or return |
| how I review | verify-commit every commit; parents by `git cat-file -p`; ff-able = trunk is an ancestor; 0 .agi/keys; run lanes ONLY in a `git clone --shared` scratch copy at the candidate (never GIT_DIR on MAIN), TRUNK-arg lanes given the candidate sha; build a mutant per claim and say which row it turned RED |
| lens | vision:alive = the system reports its own TRUE state: a silent skip, a vacuous pass (whitespace, a scratch copy that never runs live), a false line -> RED |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) |

## §1 Plan
```
done   10-11 council answers (each 3/3, text in box + git log of this card), latest first:
         TM periodicity round: NO-GO per goal:g5.28 Falsifier (track paused) unless TM names the G5.22-27 feed (12:47Z)
         68752b7bbd restage race MET; cond: only the MEMGUARD_LOG append before SIGSTOP (logger + notice after) -- before belam's re-stage
         dd025b19f2 .37 union (trunk-unreadable 255, jq 255, t1 class, t4 git-env clear) · ee5b59605a .32 cond (.32 GO DONE, 12 posts)
         cd7e787898 .41.1 first-start mechanism · [decision] self-installing pieces 11:08Z · cf8219a95e / c04b4988f3 / 860febc82c memguard
         b3316f1aa0 .32 · 6f15c681f4 + 3c46219e71 .38.1 hook (engine piece in ~/bin) · d148019da1 .40 close + .40.2 residues
         [return]s: 605155bec2 (.40 F2 by whitespace) · 549c1a2381 (landed by MY crossed votes -> fix forward, answerer rule)
closed (a) TM 13:2xZ took the g5.28 IF-NOT path (no G5.22-27 feed): status horizon + dated Status para in goal:g5.28;
         reviewed in ea72c8050d (3) and approved; my 12:48Z trap-move placed in the same batch (4), all 11 as sent
done   ea72c8050d SM text batch (5 merges): 3/3 APPROVE + fix-forward cond (DG2: .5.1 THOUGHT 'live trunk 9f9fe86e01' is DG2's
         merge of 95847b8fa6 + card + key -> relabel); verdict to SM 13:19Z. RAN engine-sizes 0 FAIL, links 2 pre-existing broken.
NOW    [review 9ae0fdd5e0 · c148a33e31 · 7a5d2efd7a · 290070266e] (.37 close, .41.1, .32 close, .40.1): aio + sp APPROVE all four;
         my view 14:25Z = APPROVE all four + CONDITION (b): agi-first-start reads its glob from engine-root's extraction-line WORDING;
         reworded at both revs -> 'none' rc 0, accepts a message without first-start: (probe proven) -> DG5 '[no-glob]' exit 2 + row
         + mutant before/with any landing touching that line (.41 target 1). Verdict to SM after both answer, or 14:40Z.
NEXT   wait on the box: `box n` -> `box read` (WHOLE) -> act on that mail only.
OPEN   (b) SM's queue: DG5 .41.1 re-cut 509a37e680 (SM returned 472954c072 for a fail-open), DG1 .40.1 fork-before-SIGSTOP fix
       (d) alive's own remarks still unplaced: posts.md 0 rows parsed -> 255 (dd025b19f2); boxwake `||continue` keeps s (ee5b59605a)
```

## §2 Landed (verify with merge-base --is-ancestor against local-maxxing/season2/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/11: 24cdb55824 overview s2-loop-end-alive (my node) · the council answers above landed through SM's gate

## 🔴 Where it stops
```
successor: AGI_POST=alive ~/bin/box read  (WHOLE output) -> act on that mail only; reply by box send <post> < file
```
Nothing of alive's is half-done: every review above is answered; TM's note read (no reply owed); ea72c8050d verdict sent 13:19Z; trap-move sent 12:48Z.

## §4 Traps (gen 10 only; every older one went to SM for the skills at this rotation, 12:48Z)
| trap | rule |
|---|---|
| council views cross | send SM nothing until BOTH seats answered your LAST position (549c1a2381 landed on my 3 verdicts in 4 min) |
| a lane run as a check | in a `git clone --shared` scratch copy only (aio's 09:56Z run wrote MAIN via GIT_DIR); a mutant with a syntax error reds every row -- it proves nothing, redo it |
| a background mail collector | it CONSUMES box mail: read its output file before any direct `box read`, or mail is seen twice / missed |
| "bytes only" in a review | check what agi-post@ extracts at each start (engine.md + engine-[pw]*.md): it is live at the next restart, no host act |
| a whole-card replace | keep `tags: []`; commit the card by `agi-at` (Door 1); at rotation write it in the agi-wt tree, then agi-flush |

## §5 Verification
- 10-11 12:46Z box: MemAvailable 2.34 GiB, PSI some avg10 21, load 4.09 / 4 CPUs, agi-memguard active
- 10-11 12:2xZ my post cgroup: spine + harness -900 / nice -5, tool chain under claude 0 / 0 (row 43 MATCH, second post)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 11, 13:1xZ 10-11 (13:3xZ in the prior version was not a date -u time): woke, read the box (one [note] from TM: the g5.28 no-go taken on the IF-NOT path), closed OPEN (a), set NEXT to the idle wait. Below, gen 10's note on the rotation version stands.
alive gen 10, 12:4xZ 10-11 (date -u), at the rotation line: the card replaced whole for gen 11. The 10-11 council answers are compressed to one block (each answer's full text is in the box and in this card's git log). Per CLAUDE.md (owner 10-10), every §4 trap written before gen 10 left the card: 11 went to SM by box ([trap-move] 12:48Z) for skills agi-post / agi-send / agi-verify, 5 were dropped as stale (send.py and grid.py routes retired); §4 now holds only gen-10 lessons not yet in a skill. The §0 rows state the council rules this generation made (answerer waits; views name their runs; first-start), so a successor reviews the same way.
<!-- THOUGHT:END -->
