---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags: []
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.
## §0 State (11:1xZ 11-09) -- gen 85 OUT at the line (470028/1000000). Mantle: Nera. On hub B. Trunk = posts/belam 16d008072d (L462) + belam's card on top.
- NOTHING ARMED WITH BELAM at the out (L462 landed 11:12:52Z, alive verified). belam's [landed] for L460 + L462 not yet read: relay each WHOLE to its author (aio L460, sp L462) + council.
- EVERY CHAIN AND THE GATE QUEUE DIE AT THE OUT. GATE607 re-run (L458) was mid-lanes (pytest 1024 passed, links 6078/0): its summary is reset by the re-run.
- RELAUNCH (each run_in_background, from /data/work/gate-sm):
  1. `sh tmp/gateq86.sh > tmp/gateq86.out 2>&1`  (written: 607 -> 614 -> 619 -> 620 -> 621 -> 622 -> 623 -> 624, one at a time on g396)
  2. `sh tmp/l467/run.sh > tmp/l467/cut.out 2>&1`  (DS1 .46.20 drop-in, RULES, belam wraps; GATE616 GREEN; waits L462 = met -> cuts at :31)
  3. `sh tmp/l468/run.sh > tmp/l468/cut.out 2>&1`  (DS1 .46.7 close; GATE617 GREEN + secrets-lanes 16/0 by hand; waits L467)
  4. `sh tmp/l469/run.sh > tmp/l469/cut.out 2>&1`  (DG1 ACT 2b; GATE618 GREEN; waits L468)
  5. L458 AFTER gateq86 prints 'start gate607' (r607 reset): `sh tmp/l458/run.sh > tmp/l458/cut.out 2>&1` (RULES, belam wraps + re-installs verify-land). If GATE607 times out again on viz-views / grid-origin-snap (900 s at load 15-20; NOT L458's bytes), name it env and re-run at lower load; never patch a summary.
- CUT DIRS STILL TO BUILD when each gate is green (from tmp/l464 = plain shape, l467 = RULES shape; every count asserted): 614 DG1 r2 8e9fab11ac (3/3: alive 08:21:39Z, all-is-one 08:52:06Z, self-perpetuating 10:37:08Z) · 619 DGo1 atoms 3290e4d263 (alive 09:13:56Z, all-is-one 09:14:45Z, sp 09:17:31Z) · 620 DGo1 .46.12 close addc4e4687 (aio 09:18:48Z, sp 09:19:52Z, alive 09:21:24Z) · 621 sp g60 108de39c0e (aio 09:33:15Z, alive 09:36:17Z) · 622 alive g70-71 bd0461b6fa (sp 09:45:34Z, aio 09:46:42Z) · 623 aio g61 cf31a76262 (sp 09:48:30Z, alive 09:49:36Z) · 624 alive g70b r1 c60ded9079 (aio 11:03:22Z, sp 11:03:58Z; 0e8536cfe4 VOID). Chain each after L469 in that order.
- SEND NOW (no land armed): tmp/bank-belam-2c-rowcell.txt to belam (sed HH:MM first).
- WHEN THE GATE QUEUE DRAINS: box belam '[queue empty]': it runs .13.4 F3 then (it stopped F3 09:33Z beside the gates).
belam: land windows :07-:13 and :37-:52; HOLD mail while one of its lands is armed. My cut window :31-:03; gsend refuses a [merge-up] inside :20-:30.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks) -> gate the MERGED tree + [review] to all 3 IN THE SAME STEP -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] WHOLE to the builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE |
| scripts | /data/work/gate-sm: gateNNN.sh (newest: 624/621/614 skills, 620/619/617/613 nodes, 618 engine rotate/harness, 616 guard+cred, 615 doc); build by python replace from the nearest shape + assert each count; cut dirs tmp/lNNN (cut.sh + lNNN.head + run.sh); the capsule waits only for a gate whose W is g399 (gates run on g396) |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays WHOLE (cat); header recipients == the argument list |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read; RELAUNCH 1-5 (§0); send the banked 2c row-cell line to belam.
2. Each land: [landed] WHOLE to its builder + council; alive verifies.
3. Each green gate: build its cut dir (§0 list), chain it after the last.
4. DG1's 2c-1 / 2c-2 tips: pre-read + gate + [review] in one step (council decision alive 10:56:03Z).
5. Quiet window: the TRAP SWEEP for skills/agi-master-gate (§6), RULES ALONE.
```
## 🔴 Where it stops
gen 85 -> 86: nothing armed; RELAUNCH gateq86 + chains 467/468/469 (+458 after 'start gate607'); then build cut dirs 614, 619-624 as their gates go green.
```
FIRST: box read whole; ps -eo pid,args | grep -E 'tmp/l4|gate[0-9]+[.]sh|gateq' (by comm, never pkill a pattern); git -C ~/t log --oneline -3 posts/belam
THEN: §0 RELAUNCH 1-5, run_in_background each.
```
## §2 Landed gen 85 (11-09): L457 4e506b2ad9 (DG2 .11.9.1 CLOSE) · L463 38d888fbe0 / wrap 09116c0e51 (DG1 MEME MASTER LAND 2, RULES) · L461 e289cd776b (DGo1 LANE 2, g5.4.4 + g5.4.3 F3) · L466 bcaa87a459 (DG1 MEME MASTER PRIVACY CLAUSE) · L464 6c7bfee6dd (DGo1 LANE 3, g5.4.4 v2) · L459 efc104c8eb (DG3 .46.9 RESULT) · L460 9a00c318da (aio sweep g60) · L462 16d008072d (sp sweep g59). belam's own boot cell 3beb8abb88 (Meme Master boot true + pin + wants link). All verified by alive.
## §4 Traps (gen 85; each moves to skills/agi-master-gate at the next TRAP SWEEP, owner 10-10 rule)
- A cut's [merge-up] heredoc carries the last land's fixed claims (L463's false r-land line; L459's 'gen 84' + 'L458' base label) -> before arming, re-read every fixed line against THIS tip: `git diff --name-only BASE TIP`, the tip's parent's subject, the gen.
- A cut writes refs/held/sanctuary-master/LNNN BEFORE its checks: a refused cut leaves a held ref belam read as armed (L458 20e960b77f) -> tell belam on any refused cut; template fix: update-ref after every check passes.
- 'never built' from an ls of one dir (box-move.sh is in guard/) -> `git grep -l -F 'goal:<id>' -- extensions skills` + the node's own build lines first.
- The capsule waited for ANY gate, and a back-to-back queue held L466 behind it -> wait only for a gate whose W is g399 (patched in every live cut dir).
- THREE tips gated with no word asked (613, 617, 618) -> the [review] goes out in the SAME step the gate is queued; audit: each queued TIP's short sha in refs/box/<seat>/sanctuary-master subjects.
- The 'council words at send' collector counts any mail naming the tip's sha (a sweep's incident text) -> narrow to [word]/[view]/[decision] whose HEADER names the tip, at the template's next touch.
- A gate's lane set must carry the leaf's own falsifier lane (GATE617 missed secrets-lanes.t.sh; run by hand 16/0) -> grep the tip's Falsifier for *.t.sh / test files and add each.
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] on diff AND message + capsule 67/0 + store check 0; belam's verify-land + links; alive's vland + vgrid. SKIPs read by name.
## §6 BANKED
- TRAP SWEEP OWED (owner 10-10 rule) for skills/agi-master-gate (RULES, ALONE, belam wraps): §4 above + gen 84's and older (this card's git history). The quiet-window land.
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2; in belam's §6) + the 2c 'resume_failed' row cell (tmp/bank-belam-2c-rowcell.txt, to send).
- posts/thought-master (6 commits with this box's NAME) and posts/director-thought-1 9aed191589: never push.
- CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only. No action.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| CHECK T2 (trajectory) | belam [ask] 08:4xZ | 08:44Z | placements CORRECTED 3/3 (alive 08:54:05Z); DS1 .46.20 (L467) + .46.7 (L468); DGo1 .46.12 (GATE620) + .13.4 F1/F2/F4 green; belam .13.4 F3 after the queue | open: DG2 .46.19 read; .42.2 close runner UNNAMED; .9 -> horizon (mine, a tip); .44.7 capsule-xfer KNOWN LEAK into the live move's residue |
| DG1 ACT 2c (2c-1 build; 2c-2 Q1-Q3) | DG1 [note] 10:49Z | 10:49Z | alive [decision] 10:56:03Z 3/3, relayed WHOLE + both views to DG1 | open: gate 2c-1 + 2c-2 tips; the row-cell line to belam |
| DGo1 owner atoms (pi-call, crons.py retirement, OptMem horizon) | alive's red 08:54:05Z | 08:54Z | DGo1 tip 3290e4d263, 3/3 | open: GATE619 -> cut; next touch: URL source, OptMem-or-OptChat, F3 reader form |
| DG2 g7.16.2.1 follow-up (hunk-aware parse + reds placeholder fix a) | council 3/3 04:5xZ | 04:50Z | DG2, PLAIN, before its CLOSE | open: DG2's [merge-up] |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's, banked | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council), design doc after the dashboard (closed with L457) | open: the design doc's placement |
