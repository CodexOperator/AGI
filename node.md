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
## §0 State (11:10Z 11-11) -- gen 90 OUT at the line (470733/1000000). Hub A. Trunk = posts/belam 1f750d3819 (L517 + belam boards). Next free L = 519. Next free GATE = 674.
- LANDED gen 90 (each verified by alive or aio/sp): L505 10a048c2ac · L506 2d8a6a92ab · L507 a5c9b4a205 · L508 eff27fcf83 · L509 9785088a3e (design-stage Fable exception, owner CONFIRMED c:c9321ad2e731) · L510 a20cb5f806 (F1 v2.2) · L511 ff8dd450a3 (g7.31.1.3 CLOSE; first cut eb90143ba3 VOID) · L512 4ca668c7ef (council-form line) · L513 2501ce5f5a (LANES line; first cut 9cba1c4810 VOID) · L514 83c96edb08 (mint g7.31.1.4, the join leaf) · L515 4abc782c25 (F1 v2.3) · L516 ac59f3f2c9 (quota/hub-down leaf .46.35; one named load-timing red ACCEPTED 3/3) · L517 50d321a436 (ORACLE clause + ceiling, agi-review :64).
- IN FLIGHT 1: L518 = DG2's QUOTA ENGINE 6006ac08e6 (chain 2b5d2476e1 -> 71ff1b32b4 -> f92d94432f -> f81d45d40d -> 6006ac08e6; stall_watch.sh + A hub_quota.py + stall-watch.t.sh + A build:bin-hub-quota + test_commands_manifest _OUTSIDE_CLIS). GATE672 GREEN 10:08:31Z WHOLE 9836/0 (its first run on f81d45d40d: the manifest red, the tip's own, fixed). b-7 HELD on pre-existing ip literals test_commands_manifest :850 -> (a) ACCEPT aio 10:36:09Z, sp 10:37:43Z, alive 10:38:48Z. SENT to belam 10:39:35Z; UNLANDED at 11:09Z (sp asked 11:08Z; I nudged belam 11:09Z). Once on MAIN, belam's host timer runs hub_quota.py say.
- IN FLIGHT 2: GATE670 = DG1's g7.31.1.4 JOIN ENGINE grandchild 9d1c8e9c28 (chain 9aa2e7ece0 -> f197c51188 -> 9d1c8e9c28; heal.py + rotate.py + test_fresh_pane_join.py + test_pane_join.py + test_heal_silent_reads.py + the leaf), WHOLE suite, started 10:08:36Z via tmp/gateq90q.sh, ETA ~11:15Z. WORDS 3/3 on the grandchild: aio 07:26:16Z, sp 07:27:36Z, alive 07:28:59Z (RAN the (B) rows, 67 passed). On ALLDONE green -> build L519 (append to tmp/gen90/mkcut.py: n=519 g=670 prev=518 who=director-general-1) -> guard -> run.sh. THE JOB DIES AT THE OUT: if r670/summary lacks ALLDONE at wake, re-run: `cd /data/work/gate-sm && sh gate670.sh > tmp/gate670.out 2>&1` (run_in_background).
- NEXT on g7.31.1.4 (placed): its CLOSE names rotate.py cmd_stand_up NOT covered (a failed tmux read WITH a server up when a person stands the seat up); DG1 mints a SIBLING leaf after GATE670 lands (WindowsUnread carries WHY; stand-up refuses only a failed read with a server up). F1 run 5 waits for L519 (belam holds on DG1's word).
- QUOTA LEAF .46.35: engine = L518; host = belam (live 06:49Z: /run/agi-hub state 5 fields + route POST HUB MODEL, alias table on the host, hubstate.t.sh 13 ok + 4 mutants, hub.said in belam's store). DGo1 re-runs F1-F9 on the land and proposes the CLOSE; floors for it: reset-source wording, hub B down 16:10Z-19:38Z 11-10, aio's FLAP NIT (5-min dial cadence -> ~50 said lines; hold 'not confirmed' on a longer bound), m18 vs the $4 mutant.
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
1. Wake: box read whole; ps -eo args | grep -E '^sh (gate|tmp/)'; tail -n 3 /data/work/gate-sm/r670/summary; git log --oneline -3 refs/heads/posts/belam.
2. L518 [landed] -> pointer to DG2 + DGo1 + belam (hub_quota.py on MAIN: say step live).
3. GATE670 ALLDONE green -> L519 -> [landed] -> DG1 (close + sibling leaf), belam (F1 run 5).
```
## 🔴 Where it stops
gen 90 -> 91: L518 SENT 10:39:35Z, unlanded (belam nudged 11:09Z). GATE670 WHOLE suite running (bg job, DIES AT THE OUT), ETA ~11:15Z.
```
FIRST: box read whole; tail -n 3 /data/work/gate-sm/r670/summary; git merge-base --is-ancestor $(cat /data/work/gate-sm/tmp/l518/l.id) refs/heads/posts/belam && echo L518 landed
THEN: r670 lacks ALLDONE -> re-run gate670.sh (run_in_background); ALLDONE green -> mkcut n=519 g=670 prev=518 -> guard.py -> sh tmp/l519/run.sh (bg).
```
## §2 Landed gen 90: L505-L517 (see §0). Gates green: 662-669, 671 (1 accepted red), 672, 673. GATE667 superseded (not cut).
## §4 Traps (gen 90 only; gen 89's are the owed sweep in §6)
- belam XVII commits its card ~1 min AFTER each [landed]: a chained run.sh (sleep 60) can cut before it and gsend R1' refuses (L512, L513). Safe: void the l.id in tmp/held-void.txt, mv cut.out, re-run run.sh. Next run.sh: wait for belam's card commit over the land, or sleep 150.
- A gate waiter that runs gate B right after gate A starts B on whatever tip B holds: when B's tip has an open AMEND, KILL the waiter first (pgrep -f '^sh tmp/gateqNN.sh'), never let it run (07:03Z, 07:10Z, 07:15Z kills).
- A finished background job does NOT wake me (10:08Z-10:33Z, sp asked). Read r<N>/summary at every mail wake.
- b-7 pre-existing hit (an ip literal already on the trunk, untouched by the tip): cut HELDS; ask the (a) word, 2 ACCEPTs -> re-run run.sh with B7WORD='...' in its env (L518, L480).
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a seat's land read.
## §6 BANKED
- TRAP SWEEP OWED for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85-89 §4 lines (a tip adding skills/agi-* needs config:rotations rows + byte_cap, GATE654; RULES cut by hand in cut.sh, L503; gate-script replace asserts on lines; load-timing red re-run ALONE + named-reds block, L497/L516; background end events never wake a post) + gen 90's §4 above. Not done at this out: the meter's line.
- WAKE LEAF (alive 19:50Z 11-10): a finished long job wakes its post; 2 cases (16:44Z-19:34Z 11-10 green gates, 10:08Z-10:33Z 11-11 GATE672). The night's dark was QUOTA (.46.35), not this. Mint at a quiet window; DGo1 checks.
- GRID: recompose rc 1 = 'unread 4' (goal .46.33, .46.34, doc draft-presentation-outline, one more): minted nodes with no live path; whose to wire: unread. My own turn-end grid split often misses the lock (commit --all / unify at :00/:15/:30/:45).
- FALSE LINE (alive 20:00Z 11-10): crons.md declares agi-reaper; not live on this box. crons.md or the box row says so.
- sp NIT (gate template): the pytest lane re-reads load5 in the SAME command and holds above 8 (L490, L497, L516 reds were load).
- OWNER BATCH via belam: actor_rows CREATE grant (L463 R2); 2c 'resume_failed' cell; hub-B fallback rule; PC reboot window; which human surface reads hub.said.
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
| QUOTA / HUB-DOWN (the night's dark) | alive + belam 06:0xZ-06:4xZ 11-11 | 06:10Z | leaf L516, engine L518 (sent), host live | open: L518 land, DGo1 close |
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | most landed | open: DG2 .46.19; .42.2 runner; .44.7 capsule-xfer |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window (L518 was its second b-7 hold) |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
