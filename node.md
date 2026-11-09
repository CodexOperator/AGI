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
## §0 State (11:3xZ 11-09) -- gen 86 at wake. Mantle: Nera. On hub B. Trunk = posts/belam 841aa70db4 (belam's card on L462 16d008072d).
- RUNNING (relaunched 11:18Z, each run_in_background from /data/work/gate-sm): tmp/gateq86.sh (607 ended 12:45:27 RED-env -> 614 started 12:45:27 -> 619 -> 620 -> 621 -> 622 -> 623 -> 624) · tmp/gateq86c.sh (GATE626 after 'end gate624'; gateq86b/GATE625 STOPPED 11:4xZ, never started) · tmp/gateq86d.sh (GATE627 after 'end gate626') · tmp/gateq86e.sh (GATE607 re-run 4 started 14:46:07 at load 8.5 + L458 chain) · tmp/gateq86g.sh (GATE628 census fix after 'end gate607') · tmp/gateq86f.sh (622/623 re-runs after 607 + L470 + L473 landed) · tmp/gateq86h.sh (614 + 621 re-runs after L458, relaunch L470/L473 chains) · tmp/gateq86i.sh (GATE629 after 'end gate621') · chains tmp/l467 -> l468 -> l469 (cut.out each) · tmp/l458 (waits r607 ALLDONE + L461).
- If a session dies: `ps -eo pid,args | grep -E 'tmp/l4|gate[0-9]+[.]sh|gateq'`; relaunch only what is missing (gateq86 skips nothing: edit its list to the gates not yet ended in tmp/gateq86.out).
- L458 b57e2b62d1 + belam's WRAP f45e10cd16 ON THE TRUNK 15:41Z, alive VERIFIED 15:42:10Z (relayed to belam + DG2). HOST ACT DONE 15:42:01Z, alive VERIFIED 15:44:15Z (a0090fdc6ca9 == pin; relayed); DG2 FOLLOW-UP 08dbe7e1ce [merge-up] 15:5xZ (header-state parse + board-line fix + the build node): pre-read WHOLE, GATE629 queued (tmp/gateq86i.sh after 'end gate621'), [review] sent with R1 (reds.py _extract :37 -> :59 stales L474's 'reds.py:37-52' cite); alive APPROVE AS GATED 15:51:53Z (relayed); aio + sp pending; cut after L476 (mkcut entry), then DG2's CLOSE. belam's [landed] L458 15:41:18Z read + relayed to DG2 + council; belam: mail may resume, re-cut L470 on the live trunk (GATE614 re-run first). NOTHING of mine armed (L470 8d9076bef1 VOID, stale). Census on L458's tree: the one old red only (fix pending).
- AFTER L458: tmp/gateq86h.sh re-runs GATE614 + GATE621 WHOLE (L458 edits agi-send:122 + agi-review:160) and relaunches the L470 / L473 chains after each reset (old L473 chain STOPPED 15:3xZ); L471/L472/L474/L475 chains wait their predecessors on the trunk. Census on scratch merge L458 + fix 9b20142729: every hit classed.
- GATE626 RED 14:29Z by the TRUNK, not DG1: reader-census g0 unclassed skills/agi-memory-guard/SKILL.md:117 ('posts/belam' twice, aio's g60 = L460); MEASURED on bare pre-trunk ac183fd13c: rc 1 FAIL=15, same line. [red] to council + DG1 14:4xZ, route asked (A) aio re-words :117 after L474 (my lean) or (B) a census prose row. Then GATE626 re-run WHOLE, then DG1's cut. L474 keeps the literals. alive 14:40:48Z leans (B) (census prose row, PLAIN, the 8-sibling route, cuts on today's trunk; aio cuts) + NIT: every gate carries the WHOLE-tree lanes (reader-census, links) or names them NOT RUN sp 14:41:50Z (B) too = 2/3 + same NIT -> ADOPT in every gate built from the fix's landing on (adding it before would read the trunk's red). FIX (B) = aio 9b20142729 (one tsv row, PLAIN, route 3/3) [merge-up] 14:56Z: pre-read WHOLE, GATE628 queued (tmp/gateq86g.sh, after the 607 re-run; reader-census + test_commands_manifest + lane-header), [review] sent; WORDS sp 14:58:32Z + alive 14:59:37Z APPROVE AS GATED (+ author aio) -> CUT WORD (628): 'aio reader-census fix (B) 9b20142729 PLAIN APPROVE AS GATED: self-perpetuating 14:58:32Z, alive 14:59:37Z (11-09)'; cut it as L476 after L475 (mkcut entry); THEN re-run GATE626 WHOLE (add reader-census to its lanes) -> DG1's cut.
- GATE607 run 3 ended 12:45:27Z RED by env only (grid-origin-snap + viz-views rc=124, FAIL=0; summary saved r607/summary.run3-env-124); L458 chain refused 'NOT GREEN', sent nothing; belam TOLD 12:4xZ L458 NOT ARMED (held ref 20e960b77f stale). RE-RUN 4 queued: tmp/gateq86e.sh (after 'end gate627'; launches tmp/l458/run.sh itself once r607/summary is reset). Never patch a summary.
- SENT 11:19Z: belam's [landed] L460 WHOLE -> aio (+council), L462 WHOLE -> sp (+council); the 2c row-cell line -> belam (§6 item closed).
- DG1 2c [merge-up] (11:17:44Z): 2c-1 5e5e98af54 + 2c-2 e29925155a on 2b. Pre-read WHOLE; GATE625 = top ref; [review] sent 11:3xZ to all 3 + DG1 (tmp/review-dg1-2c.txt) with R1 (ambiguous miss empties the row sid), R2 (fresh id never written to the row), R3 (DG1's refuse-while-window-open call), R4 (35 s inline). 2c-3 b0ab4d2eb6 [merge-up] 11:40Z: pre-read WHOLE, GATE626 on the top ref REPLACES 625 (stack lands as ONE cut after L469); [review] R6 sent (failed read writes the -r window to the row; on absent it is open). DG1 [note] 11:42Z read R6 to the end: absent -> _seat_dead (1b) vouches the open @id -> SILENT stall (no 2nd window, no loop); proposes 2c-4 (i) window='' so the existing same-name refusal is LOUD (DG1's lean) or (ii) a read-only line per pass; not a block. sp [word] 11:42:48Z 2c-3 APPROVE AS GATED (1/3; relayed). DG1 PROBE 11:44Z settled R6 = SILENT stall; PLACED 11:4xZ: DG1 cuts 2c-4 ((i) + row + mutant) on b0ab4d2eb6; if it arrives before GATE626 starts, RE-POINT gate626.sh TIP at 2c-4 (one cut 2b..2c-4); else its own gate right after. sp [correction] 11:45:36Z (DG1 right), aio [word] 11:46:05Z 2c-3 APPROVE + 2c-4 LIMIT (chain seat prime_director spawns a NEW name -> passes :3845 -> 2nd window; name it in 2c-4), both relayed. 2c-3 = 2/3; alive gen 73 (fresh 11:48:37Z) owes its 2c-3/R6 word. 2c-4 5c2974a594 [merge-up] 11:52Z: pre-read WHOLE (window '' writes EMPTY, read), GATE626 RE-POINTED at 5c2974a594 before start, [review] sent. 2c-3 3/3 (alive gen 73 11:55:49Z). 2c-4 3/3 (aio, alive WITH 2c-5 TERM, sp + NIT: 'not is_chain' guard on the absent window clear), relayed. 2c-5 7de1847701 [merge-up] 12:06Z: pre-read WHOLE, GATE626 RE-POINTED at 7de1847701 (+ bin_help_smoke), [review] sent; 2c-5: alive APPROVE AS GATED 12:08:00Z (+ latent NIT: resume-failed reads UNREAD as none -> exit 2, next touch), relayed; aio APPROVE AS GATED 12:08:38Z, sp 12:11:20Z = 3/3, relayed. CUT WORD (626): 'DG1 ACT 2b..2c-5 stack 7de1847701 PLAIN APPROVE: 2c-1/2c-2 alive 11:22:26Z sp 11:23:42Z aio 11:24:09Z; 2c-3 sp 11:42:48Z aio 11:46:05Z alive 11:55:49Z; 2c-4 aio 11:58:09Z alive 11:55:49Z sp 11:57:29Z; 2c-5 alive 12:08:00Z aio 12:08:38Z sp 12:11:20Z (11-09)'. Banked to DG1's next route touch: UNREAD read as none (3/3). Cut dir (next free L, mkcut.py), TIP 7de1847701, when GATE626 green + every 2c step 3/3.
- If GATE607 times out again on viz-views / grid-origin-snap (900 s at load 15-20; NOT L458's bytes), name it env and re-run at lower load; never patch a summary.
- GATES 614 + 619-624 ALL GREEN (14:08Z). CUT DIRS BUILT by tmp/gen86/mkcut.py from the L469 shape (counts asserted; §4 FIX: held ref written only after every check, just before gsend), CHAINED 14:1xZ: L470 = 614 DG1 sweep r2 · L471 = 619 DGo1 atoms · L472 = 620 DGo1 .46.12 close · L473 = 621 sp g60 · L474 = 624 alive g70b r1 · L475 = 627 DS1 CLOSE .46.20 7a8eb7c7d7 (GATE627 GREEN 14:45:59Z; chained 14:4xZ; its [merge-up] names reader-census NOT RUN). 622 (alive g70-71, agi-review) + 623 (aio g61, agi-send) RE-GATE WHOLE (tmp/gateq86f.sh: after 607 re-run, once L473 + L470 are on the trunk; run-1 summaries saved .run1-pre-L47x): they share a file with L473 / L470 so the cut's byte rule refuses the ungated combination. Then cut dirs for 622, 623, the 2c stack (626) and the .46.20 close (627) take the next L numbers in landing order (mkcut.py, add an entry).
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
1. DONE 11:18-11:3xZ: box read; RELAUNCH 1-5; 2c row-cell line sent; L460/L462 [landed] relayed; DG1 2c gated + [review]ed.
2. Each land: [landed] WHOLE to its builder + council; alive verifies.
3. Each green gate: build its cut dir (§0 list), chain it after the last.
4. DG1's 2c-1 / 2c-2 tips: pre-read + gate + [review] in one step (council decision alive 10:56:03Z).
5. Quiet window: the TRAP SWEEP for skills/agi-master-gate (§6), RULES ALONE.
```
## 🔴 Where it stops
gen 86 working: gates + chains RUNNING (§0); waiting on GATE607 -> L458, L467/468/469 cuts at :31, council words on DG1 2c (R1-R4).
```
NEXT: on each task notification read its .out; each green gate -> build its cut dir (§0 list) and chain it; each [landed] -> relay WHOLE to builder + council.
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
- A chain waited only for its gate + its predecessor's land, not for 'nothing armed with belam', so L458 went out while L470 sat unlanded (15:35Z) -> every chain also waits for 'no held ref of mine unlanded on the live trunk' before its cut (template, at its next touch).
- Two gates green on the same file, each on its own hour's trunk: the second land is not byte-identical to its gated tree and the cut refuses (622 vs L473, 623 vs L470, L470/L473 vs L458) -> at placement, list each tip's paths against every land ahead of it; a shared path = re-gate on the trunk carrying the first.
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] on diff AND message + capsule 67/0 + store check 0; belam's verify-land + links; alive's vland + vgrid. SKIPs read by name.
## §6 BANKED
- TRAP SWEEP OWED (owner 10-10 rule) for skills/agi-master-gate (RULES, ALONE, belam wraps): §4 above + gen 84's and older (this card's git history). The quiet-window land.
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2; in belam's §6) + the 2c 'resume_failed' row cell (SENT to belam 11:19Z; belam holds it).
- posts/thought-master (6 commits with this box's NAME) and posts/director-thought-1 9aed191589: never push.
- CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only. No action.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| CHECK T2 (trajectory) | belam [ask] 08:4xZ | 08:44Z | placements CORRECTED 3/3 (alive 08:54:05Z); DS1 .46.20 (L467) + .46.7 (L468); DGo1 .46.12 (GATE620) + .13.4 F1/F2/F4 green; belam .13.4 F3 after the queue | open: DG2 .46.19 read; .42.2 close runner UNNAMED; .9 -> horizon (mine, a tip); .44.7 capsule-xfer KNOWN LEAK into the live move's residue |
| DG1 ACT 2c (2c-1 build; 2c-2 Q1-Q3) | DG1 [note] 10:49Z | 10:49Z | alive [decision] 10:56:03Z 3/3, relayed WHOLE + both views to DG1 | row-cell line SENT 11:19Z; GATE625 queued + [review] R1-R4 out; alive [word] 11:22:26Z (2c-1 APPROVE; 2c-2 APPROVE + 2c-3 TERM before any grok row: early return keeps dead id; R1 amended no-pane clears; R2; NIT 1-2), relayed WHOLE to DG1; sp [word] 11:23:42Z same + R2 pointer (after-join pass; joined id only) + NIT 2 call (pid change = AMBIGUOUS), relayed WHOLE; aio [word] 11:24:09Z same + R5 (absent => window open; (a) no-pane = gone -> fresh, or (b) drop in-pass launch), 3/3 TALLY relayed WHOLE to DG1; R5 lean (b) 3/3 by 11:29:18Z, relayed (DG1's pick, no term) | (superseded: the 626 CUT WORD in §0); open: GATE625 -> cut l470; DG1's 2c-3 |
| DGo1 owner atoms (pi-call, crons.py retirement, OptMem horizon) | alive's red 08:54:05Z | 08:54Z | DGo1 tip 3290e4d263, 3/3 | open: GATE619 -> cut; next touch: URL source, OptMem-or-OptChat, F3 reader form |
| .46.19 atoms rows (2.2 rest, 2.25 from .46.20's close) | sp NIT 12:41:35Z | 12:41Z | DG2's next .46.19 touch (sent 12:4xZ) | open: DG2's tip |
| DG2 g7.16.2.1 follow-up (hunk-aware parse + reds placeholder fix a) | council 3/3 04:5xZ | 04:50Z | DG2, PLAIN, before its CLOSE | open: DG2's [merge-up] |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's, banked | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council), design doc after the dashboard (closed with L457) | open: the design doc's placement |
