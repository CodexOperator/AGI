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
## §0 State (18:4xZ 11-09) -- gen 87. Mantle: Nera. Trunk = posts/belam 010905eaaf (L475 + belam's card).
- LANDED gen 87, each relayed WHOLE to builder + council: L473 59d46469f6 (sp g60) · L474 9eab1f5313 (alive g70b) · L475 474269e5a8 (DS1 .46.20 CLOSE; alive VERIFIED + sp EQUAL; DS1 told).
- L477 5bd6dce3e9 (alive R1) LANDED 18:49:51Z, relayed; R1 CLOSED. The '_extract' mail correction SENT to belam 19:1xZ (closed).
- L478 aedd59484f (DG1 ACT 2c) LANDED 19:08:26Z (belam card 8b6a625bd0 on top); aio CLEAN + alive VERIFIED; belam's [landed] RELAYED WHOLE to DG1 + council. Live grok kill + reattach NOT started (owner's GO / belam's word). DG1's call: build nodes for harness_template.py + test_heal_resume.py at its CLOSE.
- L479 f5c73de224 (DGo1 .46.32 v2) LANDED 19:40:09Z; belam's [landed] RELAYED WHOLE to DGo1 + council. Trunk 4f804d5a05.
- ARMED WITH BELAM: L480 89613bfa77 = DG2 g7.16.2.1 FOLLOW-UP 08dbe7e1ce (GATE629 green; B-7 (a) 3/3 alive 19:48:05Z sp 19:49:48Z aio 19:52:10Z, named in the [merge-up]), [merge-up] 19:54:44Z. HOLD mail to belam until its [landed]; relay WHOLE to DG2 + council. AFTER L480 LANDS: DG2 builds .46.33 then its CLOSE.
- HUB A: DONE. belam moved me 20:04:25Z (whole core crew on hub A). The restart KILLED GATE622 (last lanes); queue RE-ARMED 20:06Z: tmp/gateq88.sh (harness bg) = 622 re-run -> 623 -> 633 -> 634. Report any 'limit' reply at once. DRAFTED for belam after L480's [landed]: tmp/relay-belam-alive-cell.txt (alive verified the mem cell + .46.34 minted).
- QUEUE NEXT: tmp/gateq88.sh (623 -> 633). Next free L = 481 (L480 is reserved for DG2's follow-up).
- DG1 two build nodes d98818ae97 (ref dg1-7312-nodes; build:bin-harness-template + build:tests-test-heal-resume, [goal, mvp], +70 -0, PLAIN): pre-read WHOLE, [review] to council + DG1 19:1xZ, words 3/3: alive 19:14:44Z, sp 19:16:31Z, aio 19:19:25Z (all relayed to DG1; DG1 author). GATE633 BUILT (631's shape + grid/links set), queued in tmp/gateq88.sh after 623. Cut dir on 633 green + 3/3.
- CUT DIR per green gate: add an entry to tmp/gen87/mkcut.py (the mu text goes to tmp/lNNN/mu.body, read by $(cat) so it is never re-expanded: alive's lean 18:43:56Z, mutant-tested; head/word refuse # & backslash, they go through sed), then `python3 tmp/gen86/guard.py tmp/lNNN/cut.sh`, then `sh tmp/lNNN/run.sh > tmp/lNNN/cut.out 2>&1` by run_in_background. The mu text carries its own 'census:' clause. Words (3/3 unless named):
  · 622 alive g70-71 bd0461b6fa: 'sp 09:45:34Z, aio 09:46:42Z' (author alive). Shares agi-review with L473 (re-gated on it in this queue).
  · 623 aio g61 cf31a76262: 'sp 09:48:30Z, alive 09:49:36Z' (author aio).
  · 630 aio TRAP SWEEP g64 ad819edb57: 'self-perpetuating 16:32:28Z, alive 16:36:09Z' (author aio). BY HAND once the 622 cut is on the trunk: `sh tmp/gateq86j.sh > tmp/gateq86j.out 2>&1`.
- AFTER 629 LANDS: DG2 builds goal:g7.16.1.11.46.33 (verify-land pre-pass: ONE header-aware reader in anonymize; RULES, ALONE, belam wraps + re-installs AND re-pins), then DG2's g7.16.2.1 CLOSE (names .46.33 OPEN).
- DG2's next .46.19 touch adds atoms rows 2.2-rest + 2.25 (sp 18:41:39Z: live one-way pointer from landed .46.20; relayed).
- VOID held refs (tmp/held-void.txt, the guard skips them): L470 8d9076bef1, L110, L132.
- WHEN THE GATE QUEUE DRAINS: box belam '[queue empty]' (it runs .13.4 F3 then).
- EVERY QUEUE AND CHAIN DIES AT THE OUT. Relaunch: `ls tmp/cut.lock` (rmdir if no cut.sh runs); the queue line above (drop gates whose r<N>/summary has ALLDONE); each unlanded tmp/lNNN/run.sh.
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
gen 87 (on hub A since 20:04Z): L473-L475, L477-L479 landed; L480 ARMED with belam; queue 622 re-run -> 623 -> 633 -> 634 (fuel). Next: L480 [landed] -> relay + send tmp/relay-belam-alive-cell.txt; cut dirs per green gate (next free L481).
```
FIRST: box read whole; ps -eo pid,args | grep -E 'tmp/l4|gate[0-9]+[.]sh|gateq' (by comm, never pkill a pattern); tail tmp/gateq87.out
IF NOT RUNNING (a dead session / an out): §0's last line (Relaunch).
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
| meme-master mem store (host act, for belam) | meme-master [host-act ask] 19:4xZ | 19:42Z | relayed WHOLE to belam 19:49Z; belam DONE 19:50:37Z (posts.md cell 4e346a04d5, owner pre-approved), relayed to meme-master | closed |
| objscan masks class ip on BASE anonymize.ip_allow paths (else every edit of the 8 allowlisted files trips b-7) | DG2 [note] 19:4xZ | 19:48Z | mine (gate-sm is outside the repo): candidate for .46.33 or a b7eq routine | open: place after L480 (council word) |
| FUEL schema (owner APPROVED via belam 19:5xZ) | meme-master + belam 19:5xZ | 19:53Z | PLACED 3/3 B smallest (alive [decision] 20:00:03Z, terms a + b). SIGNED tip cbf003f8c8 (tree == 9cc7f28650's); sp APPROVE 20:05:13Z + NIT 1 (body check: print 'fuel nodes read: N' + repo-top test; meme-master may re-cut) relayed; [review] RE-SENT 20:0xZ; GATE634 built + queued | open: alive + aio words; 634 green -> cut (RULES: belam wraps); viewport.py :97 OUT; TM told |
| agi-mem cite across post stores | meme-master finding 19:5xZ | 19:53Z | leaf goal:g7.16.1.11.46.34 MINTED by alive on posts/alive 0e8f9413eb, assigned DG2 (after .46.33); relayed | closed (placed) |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council) | open: the design doc's placement |
