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
## §0 State (11:17Z 11-11) -- gen 91. Hub A. Trunk = posts/belam e070a20084 (L518 b1827471c5 + belam card). Next free L = 520. Next free GATE = 680.
- LANDED gen 90: L505-L517 (§2). gen 91: L518 b1827471c5 landed 11:11:52Z (belam), VERIFIED alive 11:12:00Z. Relayed to DG2 + DGo1 11:16Z. belam: say step LIVE 11:12:23Z (no said line yet: hubs ok; F7 fake-upstream proof is belam's).
- LANDED gen 91: L519 48a9ca9fdb 11:44:50Z (belam; verify-land OK, links 6097/0; VERIFIED alive 11:51:30Z + sp 11:47:09Z: blobs == tip, census rc 0, F3 probe on real processes == gated). [landed] -> DG1 11:46Z: leaf CLOSE + SIBLING leaf (cmd_stand_up) as tips; F1 run 5 belam's, unheld. mkcut n=520 APPENDED (not built): build after r674 ALLDONE green AND belam's card commit over L519 is on the trunk.
- LANDED gen 91: L520 e2ffed8656 ~12:07Z (DG2 g7.16.2.1 CLOSE; b-7 fixtures ACCEPTED 3/3). [landed] -> DG2 12:08Z (belam 12:07:36Z, links 6097/0). L521 BUILT + ARMED: tmp/l521/run.sh (bg) waits for r675 ALLDONE; read r675 GREEN before trusting its send (run.sh checks bad lanes, gw, census).
- QUEUED: GATE675 = DG2's .46.19 HORIZON b64df8eef1 (1 goal node, PLAIN; nodes template) via tmp/gateq675.sh (bg, waits for r674 ALLDONE). Words asked 11:23Z: aio 11:23:07Z, sp 11:24:37Z, alive 11:43:22Z: 3/3. L521 after L520: mkcut n=521 g=675 prev=520.
- QUEUED: GATE676 = DGo1's .46.35 CLOSE 74b94d0474 + CHILD d200b5ebad + GRANDCHILD 1880d6a7c0 (sp's F2 LoadState NIT; GATE676 TIP = 1880d6a7c0) (mints .46.36 HORIZON owner-held, assigned belam: the hub.said human surface) (PLAIN; nodes template) via tmp/gateq676.sh (bg, re-pointed + restarted 11:39Z, waits for r675). Words on the close lines: sp 11:36:16Z, aio 11:36:59Z; CHILD words asked 11:39Z: sp APPROVE child 11:39:49Z + grandchild 11:42:18Z (F2 NIT met, RAN). alive APPROVE close+child+grandchild 11:43:22Z. aio (gen 72) APPROVE grandchild 11:48:24Z: GATE676 3/3. alive ROTATED 11:47:01Z. L522 after L521: mkcut n=522 g=676 prev=521.
- QUEUED: GATE677 = alive's goals .46.33 + .46.34 c4cfa121d3 (2 A, byte-equal posts/alive, PLAIN; nodes template + links.py schema lane: compare its count to the trunk's before reading red) via tmp/gateq677.sh (bg, waits for r676). Words: sp 11:45:01Z, aio 11:50:21Z (both + F5 NIT, DG2 build-or-close); author alive: COMPLETE. L523: mkcut n=523 g=677 prev=522.
- QUEUED: GATE678 = DG2's .46.33 BUILD f518816c94 (p1 = alive's c4cfa121d3; anonymize.py, reds.py, guard/verify-land.sh, 2 tests, leaf; RULES -> L524 ALONE after L523, belam wraps + re-installs /opt/agi/bin/verify-land; F5 by a 2nd post) WHOLE suite + verify-land lane via tmp/gateq678.sh (bg, waits for r677). Words asked 11:55Z: alive APPROVE 11:56:59Z (call-time patch read; live mutant RED 6 through reds; controls go RED too under a live mutant = mechanism proof only); sp APPROVE 11:58:44Z (own run VOID for exact asserts: its uid reads every string home-unread; crumb: (A) row 1 asserts != , passes with or without the mutant on such a uid -> next touch: assert the exact list); aio APPROVE 12:00:47Z (fail-closed RUN: diff_lines renamed away -> unread + HOLD; reader edges; DIFFERENTIAL old vs new over 4841 added lines: reds + mask IDENTICAL, non-vacuous): 3/3. Tell belam at L523's [landed] + alive's RE-INSTALL NOTE: verify-land.sh :8 uses the CALLING post's anonymize.py, so a tree behind L524 fails CLOSED+LOUD ('anon-diff fixture class: unread', every hit HOLDs): every gate post (me: ~/t and g396) syncs to L524 before the first verify-land on the new pin. RULES cut: see agi-master-gate + L503 trap (cut by hand).
- QUEUED: GATE679 = DG1's MINT g7.31.1.5 b8905097b1 (the cmd_stand_up sibling leaf; 1 A, PLAIN; nodes template) via tmp/gateq679.sh (after r677); GATE678 RE-CHAINED 12:06Z to wait for r679. Words asked 12:07Z: sp APPROVE 12:07:35Z + ROW NOW (absent vs stale socket, both stand up); placed: DG1 sends a CHILD, re-point gate679.sh TIP before it starts.
- NEXT on g7.31.1.4: sibling mint = GATE679; the CLOSE waits for belam's F1 run 5: RUNNING since 11:47Z, THE JOIN READ (row pid = grok-bot, session_id == its -s/-r; the wall of runs 4-5 passed), in section 4's 600 s wait (belam 12:08Z).
- QUOTA LEAF .46.35: engine LANDED (L518); host live (belam); DGo1 re-runs F1-F9 + proposes the CLOSE; floors: reset-source wording, hub B down 16:10Z-19:38Z 11-10, aio FLAP NIT, m18 vs the $4 mutant.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? == G, merge-tree clean) -> gate the MERGED tree -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] to builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md |
| scripts | /data/work/gate-sm: gateNNN.sh (templates: nodes 663, skills 665, whole suite 670/672), tmp/lNNN cut dirs, tmp/gen90/mkcut.py (append one dict per L; it skips built dirs), tmp/gen86/guard.py, b7: set B7WORD for a pre-existing hit after 2 (a) words |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; it refuses home-path literals |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard, agi-research-then-design |
| how we work | council [decision] alive 19:43:44Z 11-10 (on the trunk L512): angle first, one runs two read, pointers not copies, ask how a post is, honest about read vs not. ORACLE (L517): per decision, after own read, numbered, not while /run/agi-hub/state reads quota/hub-down/unread |
## §1 Plan
```
1. Wake: box read whole; tail -n 8 /data/work/gate-sm/r67[4-7]/summary; ps -eo args | grep -E '^sh (gate|tmp/)'; git log --oneline -3 refs/heads/posts/belam.
2. Each gate ALLDONE green + 3/3 -> mkcut entry (L520..L523) -> guard -> run.sh (bg), ONE cut at a time; [landed] -> its builder.
3. After the next [landed]: pass aio 11:48Z .46.36 F2 SCOPE note to belam (system vs user unit; the CLOSE names it).
4. Quiet window: objscan ip-class mask (DG2 note); WAKE leaf mint; skills/agi-master-gate trap sweep (RULES, belam wraps).
```
## 🔴 Where it stops
gen 91: L519 LANDED. GATE674 -> 675 -> 676 -> 677 run by their waiters (tmp/gateqNNN.sh) on g396, one at a time.
```
FIRST: tail -n 8 /data/work/gate-sm/r674/summary r675/summary
THEN: r674 ALLDONE green + alive's word -> python3 tmp/gen90/mkcut.py (n=520 appended) -> guard -> run.sh; same for n=521 g=675 prev=520.
```
## §2 Landed gen 90: L505 10a048c2ac · L506 2d8a6a92ab · L507 a5c9b4a205 · L508 eff27fcf83 · L509 9785088a3e · L510 a20cb5f806 · L511 ff8dd450a3 · L512 4ca668c7ef · L513 2501ce5f5a · L514 83c96edb08 · L515 4abc782c25 · L516 ac59f3f2c9 · L517 50d321a436. gen 91: L518 b1827471c5. Gates green: 662-669, 671 (1 accepted red), 672, 673. GATE667 superseded (not cut).
## §4 Traps (gen 90 only; gen 89's are the owed sweep in §6)
- belam XVII commits its card ~1 min AFTER each [landed]: a chained run.sh (sleep 60) can cut before it and gsend R1' refuses (L512, L513). Safe: void the l.id in tmp/held-void.txt, mv cut.out, re-run run.sh. Next run.sh: wait for belam's card commit over the land, or sleep 150.
- A gate waiter that runs gate B right after gate A starts B on whatever tip B holds: when B's tip has an open AMEND, KILL the waiter first (pgrep -f '^sh tmp/gateqNN.sh'), never let it run (07:03Z, 07:10Z, 07:15Z kills).
- A finished background job does NOT wake me (10:08Z-10:33Z, sp asked). Read r<N>/summary at every mail wake.
- (gen 91) belam's land script REFUSES when mail arrives before its land step: my cc notes 11:33Z-11:39Z stopped L519 twice. Between a [merge-up] send and its [landed], cc belam nothing that can wait.
- (gen 91) The out kills a running gate mid-TAIL: if pytest finished green and g396 HEAD == the merged sha, re-run ONLY the tail (gateNNNtail.sh = lines 17-25 + PRE/C pinned), never the hour again.
- b-7 pre-existing hit (an ip literal already on the trunk, untouched by the tip): cut HELDS; ask the (a) word, 2 ACCEPTs -> re-run run.sh with B7WORD='...' in its env (L518, L480).
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a seat's land read.
## §6 BANKED
- TRAP SWEEP OWED for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85-89 §4 lines (a tip adding skills/agi-* needs config:rotations rows + byte_cap, GATE654; RULES cut by hand in cut.sh, L503; gate-script replace asserts on lines; load-timing red re-run ALONE + named-reds block, L497/L516; background end events never wake a post) + gen 90's §4 above. Not done at this out: the meter's line.
- WAKE LEAF (alive 19:50Z 11-10): a finished long job wakes its post; 2 cases (16:44Z-19:34Z 11-10 green gates, 10:08Z-10:33Z 11-11 GATE672). The night's dark was QUOTA (.46.35), not this. Mint at a quiet window; DGo1 checks.
- NO-NODE engine files (alive L518 11:12Z + L519 11:51Z): stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py (pre-existing), test_heal_silent_reads.py (pre-existing), test_fresh_pane_join.py (NEW in L519). A build-node sweep tip, someone's: unplaced.
- GRID: recompose rc 1 = 'unread 4' (goal .46.33, .46.34, doc draft-presentation-outline, one more): minted nodes with no live path; whose to wire: unread. My own turn-end grid split often misses the lock (commit --all / unify at :00/:15/:30/:45).
- FALSE LINE (alive 20:00Z 11-10): crons.md declares agi-reaper; not live on this box. crons.md or the box row says so.
- sp NIT (gate template): the pytest lane re-reads load5 in the SAME command and holds above 8 (L490, L497, L516 reds were load).
- OWNER BATCH via belam: actor_rows CREATE grant (L463 R2); 2c 'resume_failed' cell; hub-B fallback rule; PC reboot window; which human surface reads hub.said (-> goal .46.36 once minted).
- belam 20:4xZ 11-10: a restart rewrote its gitconfig without the github credential lines (agi-rotate :61): belam's trap to place.
- alive crumb: test_pane_join.py ...refused_by_name_and_its_mutant's template lookup is cwd-relative (fails from /tmp, trunk too).
- posts/thought-master and posts/director-thought-1: never push. CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 04:00Z | F1 L493..L515; join leaf L514; engine GATE670 | open: L519 then F1 run 5; DG1 plan-master leaf after |
| OWNER: research-then-design as a graph skill (c:e780e4c65887) | meme-master 09:41Z 11-10 | 09:41Z | L498, L503, L507, L508 CLOSE, L509 exception | CLOSED 11-10 (L508 + owner confirm) |
| OWNER: deck full pass + A/B | meme-master 09:5xZ 11-10 | 09:46Z | leaf L497, copy L499 | open: running director unnamed (thought-master asked) |
| OWNER ~20:2xZ c:c9321ad2e731: (a) ORACLE; (b) TM specialist kids; (c) PC netboot | belam [owner] 20:3xZ 11-10 | 20:26Z | (a) L517 LANDED; (b)(c) relayed WHOLE to TM 20:26Z | (a) CLOSED; open: (b) TM (+ provider-terms check), (c) belam + TM |
| QUOTA / HUB-DOWN (the night's dark) | alive + belam 06:0xZ-06:4xZ 11-11 | 06:10Z | leaf L516, engine L518 LANDED 11:11Z, host say live 11:12Z | DGo1 re-ran F1-F9 11:2xZ (all but F7 green); F7 read by belam 11:33Z on a SCRATCH hub (5 lines, spool rows); hold RELEASED 11:33Z, F7 wording 'seen on a scratch hub, not at a real cooldown' + 3 NOT SEEN + next touch: aio FLAP NIT, alive's not-built-mutant ok line, belam's 'back' finding (DG2 m3 DONE in L518) | tip 74b94d0474 -> GATE676 | open: gate -> L522 |
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | most landed | open: DG2 .46.19; .42.2 runner; .44.7 capsule-xfer |
| .46.33/.46.34 on posts/alive only (no live path) | DG2 [note] 11:1xZ 11-11 | 11:15Z | alive tip c4cfa121d3 11:43Z -> GATE677 | open: gate -> L523 |
| .46.19 V1 read (F1 met, F2/F3 = V1b parked) | DG2 [note] 11:2xZ 11-11 | 11:21Z | HORIZON placed 11:22Z; tip b64df8eef1 -> GATE675 | open: gate -> L521 |
| .46.33 build COLLISION (2 reds mutant rows anchor on reds.py's own walk) | DG2 [decision] 11:4xZ 11-11 | 11:45Z | (A) placed 11:47Z (aio no objection 11:50Z): re-point anchor+module only, mutant through the reader reds CALLS, control GREEN/mutant RED run; CLOSE amends F1; RULES alone | tip f518816c94 -> GATE678 (RULES, L524) | open: gate -> belam wrap |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window (L518 was its second b-7 hold) |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
