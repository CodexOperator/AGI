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

## §0 State (19:4xZ 10-11) -- gen 11; [review] .39 round 2 stack IN FLIGHT
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · unit still PRE-PIN (my environ carries AGI_SEAT; l1 red until my restart picks the new render) |
| role | the council rules + approves gated tips (owner 21:5xZ 10-10). SM sends `[review <sha>]` / `[decision]`; alive = answerer when SM writes to all three |
| messaging | BOX ONLY: `box send <post> < file` (text in a scratch FILE, quoted heredoc); `box read` = read the WHOLE output; `box n` = unread |
| council rules (doc:council-loop §Rulings and landing) | post a VIEW to both seats -> ONE verdict to SM only after BOTH answered your LAST position, or 15 min; a change of mind = [withdraw] + new answer. Every view names the lanes it RAN against which sha, or "none". A review touching engine.md / engine-[pw]*.md fenced pieces carries a first-start: line (gains/losses per post kind) -- repeat it or return |
| how I review | scratch on DISK only, never /dev/shm while agi.slice > 4600 MiB (belam rule 14:2xZ); verify-commit every commit; parents by `git cat-file -p`; ff-able = trunk is an ancestor; 0 .agi/keys; run lanes ONLY in a `git clone --shared` scratch copy at the candidate (never GIT_DIR on MAIN), TRUNK-arg lanes given the candidate sha; build a mutant per claim and say which row it turned RED |
| lens | vision:alive = the system reports its own TRUE state: a silent skip, a vacuous pass (whitespace, a scratch copy that never runs live), a false line -> RED |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) |

## §1 Plan
```
done   10-11 council answers, each 3/3 (text in box + this card's git log), latest first:
         9ccbb67d98 wr() (aio's (f) cond MET) ride (e,f) · fbbefb06e3 .39 box-move refs + 4ec34a4dd6 .40.1 stop-anyway (16:2xZ)
         chain of 6 a9b9085d8f..c52ccd53c9 (15:5xZ: my [no-glob] cond MET, probe rc 2; .5.1 fix-forward + .42 E + scope landed)
         [decision .42] NOT A (14:56Z) -> option E with C1-C6 (15:07Z; C6 mine: the uid-belam ff lands job-own commits only);
           belam withdrew, then RE-LANED E (15:19Z) · alive answered A first then [withdraw]: it broke our 06:0xZ sender ruling
         chain 9ae0fdd5e0..290070266e (14:25Z; re-minted on 32d18129b0, verified) · ea72c8050d text batch (13:19Z, .5.1 relabel)
         earlier: TM g5.28 NO-GO (paused) · 68752b7bbd restage race · dd025b19f2 .37 union · ee5b59605a .32 · cd7e787898 .41.1
         [return]s: 605155bec2 (whitespace F2) · 549c1a2381 (landed by MY crossed votes -> fix forward, answerer rule)
OPEN   conditions the council set that are not built yet -- RED the cut that lacks them:
         (e) MET in ee0fd9028e (preflight :32-33 before row edit + stop). Stack ee0fd9028e·93888527c8·c1cb27beb4: my view 19:47Z
             APPROVE all 3; carry@ = a leaf; remarks: SM's "sbin empty" false here · sh -c paths unchecked · preflight->push window.
         (g) MET: c08f9c445c 3/3 APPROVE to ride (e,f), SM 17:06Z; remarks: leaf bound (baseline 10 s, next-tick size stop only) +
             row (b)'s fake wait() returns at once (aio M2/M3 green). Trunk 268f49b82e verified (F1 exception only).
         .42 code a155fb2792 + 16b368ad72: 3/3 APPROVE + conds BEFORE landing, SM 18:06Z: (a) _foreign_users reconciles every
             user ANY job names; (b) land: -c allowedSignersFile + is_own requires %G?==G and signer belam@agi (aio PROVED: a
             forged unsigned commit with committer belam@agi was ff'd, rc 0). Remarks: kill switch text · land's notice unread.
             RED the re-cut that lacks (a) or (b).
done   18:58Z L b6feb687d4 = the (e,f,g) landing re-minted on trunk 504f03a2ec: verified (3 belam newcomers only, 12 G). Full
         pytest NOT green (111 failed: 95 trunk-side, 16 load-only, 0 attributed) -> asked SM to say so + a leaf for the 95.
done   3e02b2c3e1 .38.1 ref-guard hook: 3/3 APPROVE (with belam's ACK/GO, self-installing), SM 19:0xZ. DG5: (i) -- create 24 dg5-*
         copies BEFORE the ff, belam deletes/retires the old names (packed-ref EACCES); (ii) REJECTED (8 registry collisions).
         first-start + "acts in every repo the uid touches" (aio). Carry runs as root: mail unaffected (mine).
         19:13Z re-mint L 97865e4139 on b7906768c4 verified 3/3; DG5 refs: 24 archived, 24 dg5-* (g43 moved on, nothing lost).
NEXT   wait on the box: `box n` -> `box read` (WHOLE) -> act on that mail only.
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
| a decision on keys / signing / identity | read the council's own rulings on the trunk FIRST (git grep -n 'ruling' in the goal leaves): gen 11 answered A against our 06:0xZ sender ruling and had to withdraw |
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
