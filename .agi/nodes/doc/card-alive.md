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

## §0 State (21:2xZ 10-11, rotation line 472k) -- gen 11 -> gen 12, encryption-town
| | |
|---|---|
| post | alive · council (alive · all-is-one · self-perpetuating) · v5 claude-code opus-5-5 · encryption-town (host belam-prime) |
| role | the council rules + approves gated tips (owner 21:5xZ 10-10). SM sends `[review <sha>]` / `[decision]` / `[land L]`; alive = the ANSWERER: the one voice to SM |
| messaging | OWNER 20:2xZ 10-11: never box belam (SM/TM fold all into a ~4 h digest; only [red] or a BLOCKING owner ask goes at once); to SM: one message per finished thing, NO acks. BOX ONLY: `box send <post> < file` (text in a scratch FILE, quoted heredoc); `box read` = read the WHOLE output; `box n` = unread |
| council rules (doc:council-loop §Rulings and landing) | post a VIEW to both seats -> ONE verdict to SM only after BOTH answered your LAST position, or 15 min; a change of mind = [withdraw] + new answer. Every view names what it RAN against which sha, or "none". An engine-piece landing carries a first-start: line. Seats now stay SILENT on pure acks (sp 20:2xZ): silence in the window = no objection |
| how I review | scratch on DISK (the scratchpad), never /dev/shm while agi.slice > 4600 MiB; one lane at a time, nice 10, env -i, in a `git clone --shared` at the candidate; verify-commit every commit; parents by %p; ff-able = trunk is an ancestor; 0 .agi/keys; a mutant per claim, naming the row it reds; a re-mint L: diff(trunk, L) byte-identical to the approved range's diff |
| lens | vision:alive = the system reports its own TRUE state: a silent skip, a vacuous pass, a false line (a mail line too) -> RED |
| skills | agi-post · agi-send · agi-goal · agi-rotate · agi-verify · agi-master-gate (SM's side) · agi-memory-guard |

## §1 Plan
```
done   10-11 gen 11, every answer 3/3 (text in box + this card's git log), latest first:
         .44 capsule/pack DESIGN (owner 20:2x-4xZ): doc:g716111-44-capsule-pack @ posts/all-is-one a3387fea20 (aio drafted, sp +
           alive 7 amendments folded), to SM 21:0xZ; SM places one build leaf per verb AFTER .41 -> judge those leaves vs the doc
         .42 E code a155fb2792+16b368ad72+dbbfb2e2a6: our (a) _foreign_users every user + (b) land checks %G?==G AND %GS (aio's forgery
           + other-ring-key both rc 3) MET; re-mint L f5f100b83b verified, in SM's digest (re-mints again if the trunk moved)
         .39 r2 ee0fd9028e·93888527c8·c1cb27beb4 (my (e) preflight MET) + 9e68cbfc93 rename -> L d979350816 verified
         .38.1 ref-guard 3e02b2c3e1 (DG5 rule (i): 24 -> dg5-*, archived; (ii) rejected, 8 registry collisions) -> L 97865e4139
         (e,f,g) memguard + box-move: (f) try in log() -> 9ccbb67d98; (g) logger Popen -> c08f9c445c; L b6feb687d4 (pytest NOT green
           by attribution: 95 trunk-side reds want a leaf) · chain of 6 (my [no-glob] MET) · .42 decision NOT A -> E with C1-C6
         earlier: ea72c8050d batch · chain 9ae0..2900 · TM g5.28 NO-GO · [return]s 605155bec2, 549c1a2381
NEXT   23:3xZ, all 3/3 to SM: .20.2 re-cut 2 (..6b9b9b9658) LAND 23:29Z (false red fixed; real-files row + mutant).
         .40.1.1 slab [decision] answered 23:3xZ: (a) vfs_cache_pressure + before/after numbers + sysctl.d in a node;
           (b) raise only; (c) per-walker table; + memory_alarm.py:91 fill vs memory.max is VACUOUS (held at high 5120 <
           0.95*6144): read against min(high,max), row + mutant.
         .41 + DG5 7e93d5bb6b LAND 23:48Z (alive + sp; aio silent = no objection): ordering condition MET; gate tree
           1db9055073 grid_writers + trunk_sync 33 passed. Fix-forwards 1-3 + .13 N6 stale line number = DG5, later.
         m3-overlap [decision] (SM 00:07Z) answered 3/3 00:1xZ: (a) strict loud rows + M3_UNSENT_PCT 5 printed, n >= 300/run;
           (b) on TRIGGERS T1 (7 d of [unsent] on SM<->belam, any hand-send) / T2 (a non-retrying machine sender); (c) no.
         .42 E re-cut b1d83acb51 (home path -> ~) ACK 3/3 00:17Z: 2 files vs the approved E, same rendered paths, 12 passed.
         .42 E + DG4 eb944f41c9 + ae0237b3d3 (foreign-row log = ~/logs) ACK 3/3 00:29Z, re-mint L1..L4; ORDERED fix-forwards:
           cap in-uid per tick (SM's "own apply" FALSE: only_bound blocks never hold crons_apply) before a week; mkdir before a box move.
         .40.1.1 slab DG1 3960c8cbea..fbff58d682 LAND 3/3 00:53Z (urgent: slab ~650 MiB/h): fill vs min(high,max), slab raise,
           sysctl.d 200 in boxkit + sysctl-check.sh. No clone by alive/aio (a checkout is a walker); sp 54 + SM 786.
           MY 23:32Z fill design (current/min(high,max)) = FALSE ALARM (cache always fills to high; belam 00:58Z). DG1 re-cuts:
           anon+shmem+slab_unrec. My view 00:5xZ: agree + a PSI-owns-the-thrash row (swap keeps anon low). SM [review] of stack 6 next.
         STACK 6 gate tip 46e9c898bf (57 G, ff on 2f2033785c) APPROVE 3/3 01:2xZ: caps in-uid + mkdir MET, fill fix MET (quiet row +
           mutant), sysctl-check on box-move target MET. Fix-forward DG1: combined thrash row + leaf reading->case map.
         STACK 7 b9cc371dc1 APPROVE 2/3 01:4xZ (sp abstains, rotating): .44 D1-D4 + 7,418 B ACCEPT; FF1 fat bundle = whole history
           (287 MiB) -> behind-base ref as MANIFEST line only; FF2 agi-hook no safe.directory -> false "not on the trunk" reason.
         STACK 8 dba2764aaf APPROVE 2/3 01:5xZ: FF1 MET (thin + atomic, capsule 63/0); RULING move = box-move.sh as caller (aio);
           FF DG5: unreadable .env printed as "not set" (false) -> "not checked (EACCES)"; 3/3 with sp gen 6 (row via main([status])).
         vfs 200 keep/revert [decision] 3/3 02:0xZ: KEEP, no 500, DECIDING test = A/B per gate run at 100 vs 200 (median
           slab delta; revert if 200 >= 100), hours recorded only (sp amend 02:0xZ). I corrected my own unmeasured "before-hour load 13" claim.
         vfs A/B (belam 02:01Z: 5 vs 4 MiB, light walker) -> 3/3 02:0xZ: INCONCLUSIVE, 200 kept on cost, no heavy A/B; falsifier 1
           24 h line set (slab raise w/ walkers <= tonight, or PSI full >= 0.11/h -> revert; RED -> heavy A/B at a 20 % gap).
         STACK 9 f075ee6057 APPROVE 3/3 02:1xZ: DG5 status 3-state MET (aio ran it non-root: row runs), DG4 fixture runner MET;
           FF (DG5): test name / mutant match. STACK 10 8cd64ae3dc (tests only) APPROVE 03:01Z (aio silent): both MET.
         STACK 11 387198c54b APPROVE 3/3 03:0xZ: DG3 agi-hook env safe.directory MET (12/0, i9 i10), DG1 thrash row MET;
           FF DG3: i10 '/hooks' clause vacuous non-root; WATCH: PWD = repo top only, COUNT=1 clobbers caller's env config.
         SM [red] 03:1xZ: trunk RED on test_grid_writers since L7 (capsule writers unclassified in .13); DG4 re-cuts .13; our miss too.
         gate-selection RULE to SM 3/3 03:1xZ: derived list at the gate sha + full suite once per landed stack (sp).
         capsule x refs/grid [decision] 3/3 03:2xZ: (b) TRANSPORT not author (box-move already pushes grid; grid_sync 5-min gap);
           falsifier 5 grep was VACUOUS (0 hits) -> 3 behaviour rows in doc v5 ff02306eea (aio gen 8). sp + aio rotated (new gens).
         STACK 12 db25627954 3/3 04:0xZ: RETURN DG5 4037d8b420 ALONE (agi-sync conflict box walks to belam for 5 posts: owner
           rule; OUR stack-8 FF2 caused it) -> stop below role prime_director, notice only; APPROVE rest (closes trunk red). (c) = gate on box-move-as-caller.
         -> none owed now.
THEN   wait on the box: `box n` -> `box read` (WHOLE) -> act on that mail only.
OPEN   leaves the council asked for, not built: carry@ unit-paths (DG2) · 95 trunk-side pytest reds (SM) · capsule leaves (.44)
```

## §2 Landed (verify with merge-base --is-ancestor against local-maxxing/season2/main)
- 10-02..10-08: 3a33c71b9 level rule · 9778def43 act1.sh · a7705f2d2 AA1.C · 1b4fdbe13 AA1.K · 5a1760e82 AA1.N · 01fb4669a3 AA1.S
  · 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (agi-vstore 856 B f60191fd...)
- 10-10/11: 24cdb55824 overview s2-loop-end-alive (my node) · the council answers above landed through SM's gate

## 🔴 Where it stops
```
successor: wait on the box (`box n` -> `box read` WHOLE); nothing owed; next: DG5's .41 fix-forward leaf, DG1's .40.1.1 build
```
Nothing of alive's is half-done: every review and design above is answered; no verdict is pending at SM.

## §4 Traps (gen 11 only; the gen-10 ones went to SM for their skills at this rotation, 21:2xZ)
| trap | rule |
|---|---|
| a decision on keys / signing / identity | read the council's own rulings on the trunk FIRST (git grep -n 'ruling' in the goal leaves): gen 11 answered A against our 06:0xZ sender ruling and had to withdraw |
| a PRE-VIEW's conditions | they live only between the seats until a verdict carries them: put them in the verdict the moment SM's [review] lands (a155fb2792's (a)+(b) reached DG4 two hours late) |
| a number or fact in SM's mail | measure it before you repeat it ("25 commits" was 27; "sbin is empty" was false; sp's `ls | head -5` cut a listing) |
| my own test plumbing | `echo rc=$?` after a pipe = the LAST stage's rc; a pytest --basetemp parent must exist (110 "errors" = mine, not the code) |
| a test run while the slice is near its high | it is itself a dentry walker (gate suites +27 MiB): rely on a peer's run or a partial export, never a 30k-file clone |
| an alarm line I propose | test it on a stressed fixture AND tonight's real quiet reading (must stay ok): gen 12's fill line was vacuous, then noisy |
| a load or rate I cite for an hour | measure it for THAT hour or say whose number it is (gen 12 cited DG1's load 13 as the before-hour's) |
| a decision line I write for an A/B | it carries a MINIMUM EFFECT SIZE above the reading's resolution, or it passes on noise |
| a gate line for a range touching extensions/ src/ .agi/nodes/.geometry/ | it must print the DERIVED pytest selection (test files naming the changed top dirs + every scanner) with counts, else ask before the word: stacks 7-8 went RED on grid_writers through our approve (3/3 rule 03:1xZ) |
| a fix-forward I write that routes MAIL | check the route against the owner's mail rule on the REAL posts.md rows (gen 12's stack-8 FF2 sent 5 posts' conflicts to belam) |
| a time in my own mail | stamp it from `date -u`, never from memory: gen 12 stamped two 22:5xZ messages "23:0xZ" |

## §5 Verification
- 10-11 21:2xZ: card 3/3 trail clean; MemAvailable ~3.3-3.8 GiB through the evening, agi.slice ~4.9-5.1 GiB (over belam's 4600 line)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 11, 21:2xZ 10-11 (date -u), at the rotation line (472k): the card replaced whole for gen 12. Gen 11 answered every SM review and decision of the afternoon and evening 3/3, and ended with the .44 capsule design. The one item handed on WHOLE is SM's 21:23Z alarm-signer [decision] (due 22:30Z): it arrived at the line, and a council round cannot finish before it, so it was not started; my unchecked lead is on it. Per CLAUDE.md (owner 10-10), the five gen-10 traps left the card for their skills ([trap-move] to SM); §4 holds only gen-11 lessons.
<!-- THOUGHT:END -->
