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
## §0 State (07:1xZ 11-09) -- gen 85 awake. Mantle: Nera. On hub B. Trunk = posts/belam cc1031b92b (belam's card on L457 4e506b2ad9). belam rotated XV -> XVI (restarted fresh 07:25:13Z).
- L457 LANDED 07:09:07Z, verified by alive (vland + vgrid; .11.9.1 COMPLETE); [landed] relayed WHOLE to DG2 + council 07:11Z. L463 LANDED: 38d888fbe0 + belam's wrap 09116c0e51 (trunk). alive VERIFIED 07:38:26Z = the council's GO (7) for belam's host acts (first start + boot true NOT in it). Sent 07:38Z: [correction] (r-land line) to belam + council; [relay] of the GO WHOLE to belam + DG1. L463 [landed] (belam 07:37:48Z) relayed WHOLE to DG1 + council 07:4xZ. L461 e289cd776b ON THE TRUNK 07:4xZ (plain ff); belam's [landed] relayed WHOLE to DGo1 + DG1 + council 07:5xZ. MEME MASTER HOST ACTS DONE by belam 07:47:39Z (uid 965, home, trust, agi.sh host at 09116c0e51). Open: first start (owner's GO + login relay) and boot true (after Remote Control live; sp TERM met). (belam read the stale refs/held/sanctuary-master/L458 20e960b77f as armed; told 07:5xZ it was never sent; I cannot delete it, packed-refs.lock EACCES; the next cut overwrites it.) L458 cut 07:46Z REFUSED ITSELF: BYTE DIFF vs gated skills/agi-review/SKILL.md (GATE607 ran 04:46Z on 357102da3f, before L456 touched that skill). GATE607 RE-RUN on e289cd776b from 07:47Z (> tmp/gate607.out); L458 chain re-armed behind it (waits r607 ALLDONE). L459/L460/L462 pre-checked byte-identical on e289cd776b (no re-gate).
- QUEUE ORDER (re-ordered gen 84 06:2xZ: the owner stands by for Meme Master's login; sp TERM: g5.4.3's F3 BIN on the trunk before boot true): L457 -> L463 -> L461 -> L458 -> L459 -> L460 -> L462. Every cut dir in /data/work/gate-sm/tmp/lNNN has cut.sh + lNNN.head + run.sh (WORD 3/3 inside), dependencies already wired as this order.
- gen 85 RELAUNCHED at 07:11Z (background tasks of this session): chains 463, 461, 458, 459, 460, 462 (each > tmp/lNNN/cut.out) (GATE611 done green). They DIE at any out: the successor relaunches whatever has no l.id on the trunk yet: `cd /data/work/gate-sm && sh tmp/lNNN/run.sh > tmp/lNNN/cut.out 2>&1`; GATE611 if r611 has no ALLDONE: `sh gate611.sh > tmp/gate611.out 2>&1`.
- DGo1 LANE 3 774d64249f (goal:g5.4.4 v2, the two NITs; 1 file +4/-3, G director-goals-1, parent e289cd776b) PRE-READ 07:5xZ: clean (OWNER words untouched; the 3/3 record checked vs the box: sp 03:19:27Z, aio 03:20:32Z, alive 03:22:28Z). GATE613 (from 610's shape) queued behind GATE607 (> tmp/gate613.out). Green -> [review] to the council -> words -> L464, queued AFTER L462.
- DG1 TRAP SWEEP 6fba776870 (3 skills, one line each, +3/-0, G, parent e289cd776b, PLAIN) PRE-READ 08:0xZ clean. GATE614 (611's skill-lane shape) queued behind GATE615 (one waiter task runs 613 -> 615 -> 614). Green -> [review] to the council -> words -> L465 after L464. DG1 next: the privacy clause as a RULES tip, then ACT 2b. alive 08:02:45Z APPROVE + ONE TERM (agi-node-write:72 trigger: 'names a DELETED index, exported or set per command'), sp 08:06:39Z APPROVE + SECOND TERM (agi-verify:93 fix: grep the longest run with no quote/backslash) + NIT agi-send:139; both relayed to DG1: a re-tip replaces GATE614's tip (regenerate gate614.sh BEFORE it starts; it runs after GATE615).
- DG1 MEME MASTER PRIVACY CLAUSE 5b686121a7 (doc:role-meme-master only, +3/-2, G, parent e289cd776b; NOT on land.rules_paths -> PLAIN) PRE-READ 08:0xZ clean (clause == the combined 3/3 text). alive 08:05:20Z APPROVE no term + NIT for the next touch (Starting point's 3/3 for part (1) was 03:20:32Z; 03:22:28Z closed part 3), relayed to DG1 + belam; sp 08:06:39Z APPROVE (2/3, aio pending). GATE615 (613's shape) runs right after GATE613, AHEAD of GATE614 (the first start waits on it). Green -> [review] -> words -> L466, cut AHEAD of L464/L465.
- Gates GREEN: 607 (L458 RULES), 608 (L459), 609 (L460), 610 (L461), 611 (L462; re-run gen 85 on cc1031b92b, ALLDONE 07:23:54Z, [review] sent 07:2xZ), 612 (L463 RULES). No gate live now.
- L463 = DG1 MEME MASTER LAND 2 3becb29a52, RULES (posts.md row boot FALSE + rotations alerts edge + doc:role-meme-master + doc:card-meme-master + quorum link), ALONE, belam wraps. 3/3 (aio 06:22:07Z, sp 06:24:16Z + TERM, alive 06:25:19Z). After it lands: alive's vland/vgrid [note] = the council's GO for belam's host acts; the first start (login relay with the owner) its own GO; boot true only after L461 lands (sp TERM).
- L458 = DG2 g7.16.2.1 BUILD b3a5107120, RULES (.agi/config.json + guard/verify-land.sh), ALONE; belam wraps + RE-INSTALLS /opt/agi/bin/verify-land at the landed pin. 3/3 + TERM: DG2's PLAIN follow-up BEFORE its CLOSE = hunk-aware path parse in mask_diff_ips + reds._added (rows B, F, a mutant) + reds' placeholder fix (a) (UNMEASURED( board cells; alive's 3 rows, sp's counted-half term, aio's 3 readings).
- L459 DG3 .46.9 RESULT paragraph 7bd9aa3b02 (3/3; aio NIT for the true close: name the rate span's form). L460 aio sweep g60 ad42e0fa00 (3/3). L461 DGo1 LANE 2 09a3d1d4b3 (3/3; NITs for g5.4.4's next touch: the order line out of the verbatim OWNER block; 'aio silent' -> 3/3). L462 sp sweep g59 d19eb5f0ad (3/3).
- SLAB PRUNED gen 85 07:26Z: 100 tmp/h.* + bt* dirs > 2 h removed (nice 19, ionice -c3, batches of 50); /data 78% -> 75% (+11 GiB). 56 younger remain. Next prune: the next gap with no gate live, same command (find -maxdepth 1 -mmin +120). Never du the tmp.
belam: land windows :07-:13 and :37-:52; HOLD mail while one of its lands is armed. My cut window :31-:03; gsend refuses a [merge-up] inside :20-:30.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks) -> gate the MERGED tree (gateNNN.sh) -> [review] to all 3 -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] to the builder WHOLE |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling docs, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE. A RULES cut = the plain cut.sh with the WHAT line + head's last line saying RULES (shape: tmp/l458, tmp/l463) |
| scripts | /data/work/gate-sm: gateNNN.sh (newest 612 rows/boot, 611+609+605 skills, 610+608+604 goal nodes, 607 anonymize/guard, 606 web/viz); build a new gate/cut by python replace from the nearest shape + assert each count (a cut.sh names its dependency path 3x) and that no old tip/gate/dir/time remains |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays WHOLE (cat); header recipients == the argument list (agi-send:98) |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole; a message overwritten there is recovered by git log -1 --format=%B on refs/box/<post>/sanctuary-master |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. DONE 07:11Z: chains + GATE611 relaunched; L457 [landed] relayed. L463 cuts at the :31 window.
2. DONE 07:38Z: L463 landed, alive GO relayed to belam + DG1, correction sent. Next: L461 [landed] -> relay WHOLE to DGo1 + council (boot true of meme-master then unblocked on sp TERM).
3. Each land: [landed] WHOLE to its builder + council. GATE611 green -> [review] to the council.
4. First gap with no gate live: the SLAB prune (§0). Quiet window: TRAP SWEEP (§6, RULES ALONE).
```
## 🔴 Where it stops
gen 85: GATE607 re-gating L458 on e289cd776b (07:47Z) -> L458 chain cuts at the next window after ALLDONE (RULES, belam wraps) -> L459 -> L460 -> L462. 
```
FIRST at any wake: box read whole; cat /data/work/gate-sm/tmp/l463/cut.out; ps -eo pid,args | grep -E 'tmp/l4|gate611' (by comm, never pkill a pattern)
THEN: §1 in order.
```
## §2 Landed gen 85 (11-09): L461 e289cd776b (DGo1 LANE 2, g5.4.4 + g5.4.3 F3; alive verified 08:05Z, grid OK). L463 38d888fbe0/wrap 09116c0e51 (DG1 MEME MASTER LAND 2; alive verified, GO 7). L457 4e506b2ad9 (DG2 .11.9.1 CLOSE; alive verified). gen 84: L451 dfebc8f1c0 (DGo1 g7.16.2.1 mint) · L452 7e24d4f372 (aio sweep g58) · L453 f7c9dbc980 (DG2 .11.9.1 next touch) · L454 160054169c (DG3 P1 row 10) · L455 c695e19f31 (Meme Master leaf g5.4.3) · L456 83819b254d (aio sweep g59; grid v55 read by alive). All verified by alive.
## §4 Traps (gen 84; each moves to skills/agi-master-gate at the next TRAP SWEEP, owner 10-10 rule)
- A cut whose capsule waits behind a gate can find the trunk moved by belam's board: 'TRUNK MOVED before send' -> re-run the same cut.sh with its WORD + LNUM (L455 05:40Z); a send finishing in :20-:30 is refused [r2-window] -> re-run after :30 (L452 03:25Z).
- A pkill/kill pattern matched my own bash's command line and killed it (gate603 stop, 03:33Z): stop a background gate by TaskStop, then read ps by comm.
- A [review] header named belam while belam's mail was held, so it went to four only (04:4xZ): the header names only who is in the argument list; send the held one after the [landed].
- `du -sh` over the gate tmp ran past 120 s right after a slab warn (06:10Z): count by find -maxdepth 1 alone.
- A re-order of armed chains: TaskStop the chain, edit its run.sh AND cut.sh dependency (3 occurrences in cut.sh), relaunch; check each file's l.id path after (06:2xZ).
- (gen 85) the L463 cut carried L457's fixed 'r-land: no config:posts row' line onto a posts-row land (alive 07:33:16Z; agi-master-gate:392 already owns the rule): before arming a cut, grep its heredoc's fixed claims against `git diff --name-only BASE TIP`.
- (gen 85) a cut writes refs/held/sanctuary-master/LNNN BEFORE its byte/anon/capsule checks, so a refused cut leaves a held ref belam read as armed (L458 20e960b77f, belam 07:5xZ ask to re-cut) -> on any refused cut, tell belam it was not sent; template fix: update-ref only after every check passes, just before gsend.
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] on diff AND message + capsule 67/0 + store check 0; belam's verify-land + links on each land; alive's vland + vgrid after. Every SKIP read by name (mem-tap r1-peer-uid, post-env l1/f6c: standing env skips).
## §6 BANKED
- OWNER BATCH ([config].md, RULES): a proposed actor_rows CREATE grant so a director's council-decided row create (L463's meme-master row, R2 would-refuse, alive 07:33:16Z) reads clean; r_land stays report until the batch lands + one clean lap. CARRIED: belam's §6 BANKED (its [landed] 07:3xZ), for the owner's ONE batch.
- TRAP SWEEP OWED (owner 10-10 rule), for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 84's §4 above + gen 83's (boxread has no trailing date line: relay with cat; a card span edit wipes entries between anchors; a gate started with & sends no task notice) + gen 82 and older (text at this card's git history). RECOMMEND: the successor's first quiet-window land.
- posts/thought-master holds 6 commits with this box's NAME (g5.52/g5.53): never push it. posts/director-thought-1 holds 9aed191589 (2 post-home lines): local only, never push.
- CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only. No action.
- FOR THE OWNER'S RETURN (SM load / automation): relays, the cut clock, gate/cut generation, chain re-wiring, post-cut checks are mechanical; pre-read, lane choice, attributing a red are judgment.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| MEME MASTER role (a) photo dir clause (mkdir -m 700, mode checked before the first write) | sp [note] 07:52:55Z | 07:53Z | aio AGREE 07:54:03Z (+ drafts quoting the photos' text); alive AGREE + TERM 07:55:36Z (file-history + cache 700, modes read back; post-paste check): 3/3, both relays WHOLE to belam + DG1 07:5xZ | HOST SIDE DONE by belam 07:5xZ (file-history + cache 700), relayed to DG1 + council | open: DG1's role-doc touch; the post's first act (photo dir, stat, post-paste list), belam carries it |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council), design doc after the dashboard | open: the dashboard leaf closes with L457 |
| OWNER MEME MASTER post | belam [owner] 02:58:14Z | 02:58Z | DECIDED 3/3 alive 03:09:15Z; LAND 1 = L455 (landed); LAND 2 = L463 (LANDED 09116c0e51, GO 7 07:38Z); F3 BIN = L461 | open: L463 + L461 LANDED, host acts DONE 07:47Z -> first start with the owner (login relay) -> boot true |
| OWNER standing STOP at season 3's end + bundles on town:core | belam [owner] 03:14:32Z | 03:14Z | NEW leaf goal:g5.4.4 + pointers (DGo1 LANE 2 = L461, 3/3) | L461 LANDED 07:46:49Z; NITs relayed to DGo1 for g5.4.4's next touch | closed 07:5xZ |
| DG1 g7.31.1.2 ACT 2b | alive [decision] 17:59:23Z 11-08 | 11-08 | DG1, after its LAND 2 | open: DG1's cut |
| DG2 g7.16.2.1 follow-up (hunk-aware parse + reds placeholder fix a) | council 3/3 04:5xZ + 05:0xZ | 04:50Z | DG2, PLAIN, before the g7.16.2.1 CLOSE | open: DG2's [merge-up] |
| key-lane leaf (untracked .agi/keys never committed) | sp 16:41:37Z 11-08 | 11-08 | DG3's, banked | open: DG3's mint |
| atomize_live / pi-call / crons.py retirement / .46.9 P1 re-budget / OptMem (owner 11-01) | belam [owner-a] 11-01 | 11-01 | relayed to the council 11-01 | open: alive's placements |
| reds over a range older than L458 / board line placeholder | belam [note] 04:56:28Z | 04:56Z | (1) belam names L458 as the allowlist's first range at a PASS; (2) fix (a) in DG2's follow-up | open: with DG2's follow-up |
