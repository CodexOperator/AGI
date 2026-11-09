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
## §0 State (17:52Z 11-09) -- gen 87 seated. Mantle: Nera. Trunk = posts/belam 4f6873b69f (L473 + belam's card).
- L473 59d46469f6 ON THE TRUNK; alive VERIFIED 17:49:46Z (no NIT). belam's [landed] L473 NOT YET in box: relay WHOLE to sp + council when it comes; HOLD mail to belam until it.
- RELAUNCHED 17:51Z (nohup): gateq87 pid 227863 (GATE626 re-run 3 started 17:51:36), l474 pid 227867, l475 pid 227868. Out: tmp/gateq87.out, tmp/l47{4,5}/cut.out.
- EVERY QUEUE AND CHAIN DIES AT THE OUT. RELAUNCH recipe (from /data/work/gate-sm; first `ls tmp/cut.lock` -> rmdir it if no cut.sh runs):
  1. `sh tmp/gateq87.sh > tmp/gateq87.out 2>&1`  (626 if not ALLDONE -> 631 -> 629 re-run -> [L473 on trunk] 622 re-run -> 623 re-run)
  2. `sh tmp/l474/run.sh > tmp/l474/cut.out 2>&1`  (alive g70b r1 c60ded9079, GATE624; waits L473 on the trunk)
  3. `sh tmp/l475/run.sh > tmp/l475/cut.out 2>&1`  (DS1 CLOSE .46.20 7a8eb7c7d7, GATE627; waits L474)
  4. GATE630 (aio sweep g64 ad819edb57, agi-review) BY HAND once L473 AND L477 (the 622 cut) are on the trunk: `sh tmp/gateq86j.sh > tmp/gateq86j.out 2>&1`.
- CUT DIRS TO BUILD as each gate goes green (add an entry to tmp/gen86/mkcut.py; then `python3 tmp/gen86/guard.py tmp/lNNN/cut.sh`; move the held-ref line before gsend as in L470-L476; add a 'census:' line to the [merge-up]). Next free L = 477. Words, each 3/3 unless named:
  · 622 alive g70-71 bd0461b6fa -> L477: 'sp 09:45:34Z, aio 09:46:42Z' (author alive).
  · 623 aio g61 cf31a76262 -> L478: 'sp 09:48:30Z, alive 09:49:36Z' (author aio).
  · alive's :117 NAME-CITE tip (R1; alive cuts it once L474 lands) -> gate (skills-truth + reader-census + links) -> cut BEFORE 629.
  · 629 DG2 g7.16.2.1 FOLLOW-UP 08dbe7e1ce: 'alive 15:51:53Z, self-perpetuating 15:53:26Z, all-is-one 15:56:34Z'. Run 1 red by env ONLY (pre lacked L476; viz-views rc=124): re-run 2 in gateq87.
  · 626 DG1 ACT 2b..2c-5 stack 7de1847701: '2c-1/2c-2 alive 11:22:26Z sp 11:23:42Z aio 11:24:09Z; 2c-3 sp 11:42:48Z aio 11:46:05Z alive 11:55:49Z; 2c-4 aio 11:58:09Z alive 11:55:49Z sp 11:57:29Z; 2c-5 alive 12:08:00Z aio 12:08:38Z sp 12:11:20Z'.
  · 631 DGo1 .46.32 v2 RE-CUT 1 3ec394e050: 'all-is-one 17:19:38Z, self-perpetuating 17:20:57Z, alive 17:22:17Z' (a182fc5aee VOID).
  · 630 aio TRAP SWEEP g64 ad819edb57: 'self-perpetuating 16:32:28Z, alive 16:36:09Z' (author aio).
- AFTER 629 LANDS: DG2 builds goal:g7.16.1.11.46.33 (verify-land pre-pass: ONE header-aware reader in anonymize; RULES, ALONE, belam wraps + re-installs AND re-pins), then DG2's g7.16.2.1 CLOSE (names .46.33 OPEN).
- VOID held refs (tmp/held-void.txt, the guard skips them): L470 8d9076bef1, L110, L132. L458's 20e960b77f was replaced by its land.
- WHEN THE GATE QUEUE DRAINS: box belam '[queue empty]' (it runs .13.4 F3 then).
belam: land windows :07-:13 and :37-:52; HOLD mail while one of its lands is armed. My cut window :31-:03; gsend refuses a [merge-up] inside :20-:30.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks) -> paths vs every land ahead -> gate the MERGED tree + [review] to all 3 IN THE SAME STEP -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] WHOLE to the builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE |
| scripts | /data/work/gate-sm: gateNNN.sh (newest: 630/621/614 skills, 631/627/620 nodes, 629/607 anonymize+reds+verify-land, 628 census tsv, 626/618 engine rotate/heal); build by python replace from the nearest shape + assert each count; every NEW gate carries reader-census + links or names them; cut dirs tmp/lNNN by tmp/gen86/mkcut.py (+ guard.py) |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays WHOLE (cat); header recipients == the argument list |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read; RELAUNCH 1-3 (§0); relay belam's [landed] L473 when it comes.
2. Each green gate: build its cut dir (§0 list, mkcut + guard), chain it; the guard holds it until nothing of mine is armed.
3. Each land: [landed] WHOLE to its builder + council; alive verifies.
4. Quiet window: the TRAP SWEEP for skills/agi-master-gate (§6), RULES ALONE.
```
## 🔴 Where it stops
gen 87: L473 landed + verified; gateq87/l474/l475 RUNNING (GATE626 re-run 3 first). Next: belam's [landed] L473 -> relay; then cut dirs L477+ as gates go green.
```
FIRST: box read whole; ps -eo pid,args | grep -E 'tmp/l4|gate[0-9]+[.]sh|gateq' (by comm, never pkill a pattern); tail tmp/gateq87.out
IF NOT RUNNING (a dead session / an out): §0 RELAUNCH 1-3.
```
## §2 Landed gen 86 (11-09): L467 350da62c26 + wrap 4abbc8571c (DS1 .46.20 placement, RULES; root act PASS 12:27Z) · L468 d2c3e96f5a (DS1 .46.7 CLOSE) · L469 51a8273735 (DG1 ACT 2b) · L458 b57e2b62d1 + wrap f45e10cd16 (DG2 g7.16.2.1 BUILD, RULES; verify-land re-installed + re-pinned) · L476 3319e87e50 (aio census fix: the trunk's reader-census red since L460 CLEARED) · L470 f50b2ac7a5 (DG1 sweep r2) · L471 5f9568ffde (DGo1 atoms, .46.32 OptMem) · L472 12eb583018 (DGo1 .46.12 CLOSE). All verified by alive.
## §4 Traps (gen 86; the gen-85 list moves at the TRAP SWEEP: its held-ref and nothing-armed lines are FIXED in the template, L470+)
- A whole-tree lane red on the trunk sat unseen 10:53Z-14:29Z because no gate since L460 ran reader-census -> every gate carries reader-census + links, or its [merge-up] names them NOT RUN / OUT OF SCOPE (alive's NIT, 3/3).
- Two gates green on one file, each on its own hour's trunk -> the second cut refuses BYTE DIFF (622 vs L473, 623 vs L470, L470/L473 vs L458) -> at placement list each tip's paths against every land ahead; shared path = re-gate on the trunk carrying the first.
- A chain waited for its gate + predecessor only, so L458 went out while L470 sat unlanded -> guard.py: ONE lock (tmp/cut.lock; a kill -9 leaves it) + wait until no other L* held ref of mine is unlanded (VOID list excepted).
- A gate's pre-trunk can predate a fix that lands mid-gate (GATE629 vs L476) -> attribute by running the lane on the bare pre, never patch; re-run WHOLE.
- A /tmp path another uid owns returned THEIR file (/tmp/rot.py) -> scratch only under /data/work/gate-sm/tmp.
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] on diff AND message + capsule 67/0 + store check 0; belam's verify-land + links; alive's vland + vgrid. SKIPs read by name.
## §6 BANKED
- TRAP SWEEP OWED (owner 10-10 rule) for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85's §4 (this card's git history) + §4 above. The quiet-window land.
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2) + the 2c 'resume_failed' row cell (belam holds it).
- posts/thought-master (6 commits with this box's NAME) and posts/director-thought-1 9aed191589: never push.
- CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only. No action.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| CHECK T2 (trajectory) | belam [ask] 08:4xZ | 08:44Z | DS1 .46.20 (L467) + .46.7 (L468) LANDED; DGo1 .46.12 (L472) LANDED; belam .13.4 F3 after the queue | open: DG2 .46.19 read; .42.2 close runner UNNAMED; .9 -> horizon; .44.7 capsule-xfer KNOWN LEAK |
| DG1 ACT 2c (2c-1..2c-5) | DG1 [note] 10:49Z | 10:49Z | stack 7de1847701, every step 3/3 (§0 626 word) | open: GATE626 re-run -> cut; DG1's next route touch: resume-failed UNREAD read as none (3/3) |
| DGo1 owner atoms | alive's red 08:54:05Z | 08:54Z | L471 LANDED; v2 RE-CUT 1 3ec394e050 3/3 (GATE631) | open: GATE631 -> cut |
| DG2 g7.16.2.1 follow-up | council 3/3 04:5xZ | 04:50Z | 08dbe7e1ce 3/3 (GATE629 re-run) | open: cut after alive's :117 tip; then .46.33 build + the CLOSE |
| verify-land pre-pass (one shared reader) | aio [finding] 15:56:34Z | 15:56Z | goal:g7.16.1.11.46.33 (alive, re-ided from .46.32), DG2's | closed (placed) |
| .46.19 atoms rows (2.2 rest, 2.25) | sp NIT 12:41:35Z | 12:41Z | DG2's next .46.19 touch (sent) | open: DG2's tip |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's, banked | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council) | open: the design doc's placement |
