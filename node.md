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
## §0 State (10:21Z 11-10) -- gen 89 awake. On hub A. Mantle: Nera. Trunk = posts/belam 867177a7f1 (L496) + belam card 9f07ea0168.
- LANDED gen 88: L490 827803e126 · L491 815778a7c7 · L492 dc2ff9773f · L493 969357f112 · L494 c6d9e54f46 · L495 19b8cd62d9 · L496 867177a7f1 (on the trunk 10:1xZ; belam's [landed] NOT yet read). Next free L = 497. Next free GATE = 651.
- belam [landed] L496 read 10:19Z (mail resumed). SENT 10:19Z: tmp/belam-upload-v1.txt (meme-master's Drive HOST ACT, rough-draft-v1, DUE TODAY) to belam; relayed L496 [landed] + alive's verify to DG1; belam's F1 run (grok-4.7) FAILED rc 1 10:19Z (first-run screen ate the prompt; row pid = pane shell; heal read a gone pid alive); [result] relayed WHOLE to DG1 10:23Z -> DG1's fix tip on g7.31.1.2.
- NO gate while a belam land runs at high load. Waiter `tmp/gateq649.sh` RELAUNCHED gen 89 10:20Z (bg job: DIES AT THE OUT) waits L496 on trunk AND load5 <= 8, then runs gate649.sh then gate650.sh. RELAUNCH it at wake if no `sh tmp/gateq649.sh` in ps and r649/summary lacks ALLDONE: `cd /data/work/gate-sm && sh tmp/gateq649.sh >> tmp/gateq88.out 2>&1` (run_in_background).
- GATE649 = DGo1 goal:g5.4.3.1.1 mint e33c14e641 + child f0000295e0 (2 goal nodes incl. the DATE fix on g5.4.3.1: Tue = 11-10, not 11-11). Words 3/3 APPROVE AS GATED (alive 10:11:03Z, aio 10:11:17Z, sp 10:12:04Z). VOID: 3727a59e59. On green: cut L497 (add an entry to tmp/gen88/mkcut.py, g=649, prev=496, since '09:50:00'; NO apostrophe in word), guard, run.sh.
- GATE650 = DGo1 goal:g4.18.2.2 mint 3535432ea1 + child 957bc7580d + CHILD 2 a371842afd (re-pointed 10:15Z, hold lifted; G, parent 957bc7580d, +42 -15; DGo1 read merge-tree onto 867177a7f1 clean; its diff NOT yet read by me). Words: aio APPROVE 10:11:17Z on 957bc7580d; alive WITHDREW its 957b word (10:13:40Z), approves on child 2; sp AMENDED (child 2 answers it). Words on a371842afd: alive APPROVE AS GATED 10:16:55Z, sp APPROVE AS GATED 10:19:05Z (both: FLOOR NIT for the CLOSE -- F2 (b) is a floor, hand-read both narrowed bullets); aio APPROVE AS GATED 10:23:39Z (+2 floor cases: nested sub-bullet under :23; ':60 no Claude sub-agents, ever'). 3/3, all relayed to DGo1. CLOSE: hand-read both narrowed bullets incl. sub-bullets. Then L498 after L497. GATE648 (on 3535432ea1) STOPPED 10:04Z, moot.
- RESEARCH SKILL (owner c:e780e4c65887): council [decision] alive 09:47:42Z + 10:00:48Z, 3/3. Leaf g4.18.2.2 (GATE650) lands FIRST; then DG1 writes skills/agi-research-then-design/SKILL.md (+ agi-workflow description/:23 + unified-director-brief :60 narrowed on the owner's 10-10 word, cited; :76 stands; build node [leaf, idea:engine-skill-doc] or new idea). OWNER QUESTION with belam (10:01:55Z): design-stage exception to the director brief's SUBAGENTS rule (STRICTLY Sonnet 5.5); belam put it to the owner, answer comes with a c: id; on yes, :76 gets its own small tip.
- DECK FULL PASS + A/B (owner c:61b389266d66, Drive follow-up c:1ae05e71c801): council [decision] alive 09:53:15Z 3/3. Leaf g5.4.3.1.1 (GATE649). RUNNING DIRECTOR: SM names it on the leaf's Agent Notes line before any dispatch; I asked thought-master 09:54Z (no answer yet). meme-master's privacy-scanned deck COPY comes as a PLAIN doc tip (names list, removals list, sha256, OWNER count, F3 run with notes kept). Arm A (v1) submitted TODAY; arm B after.
- F1 (goal:g7.31.1.2): L493 + L496 on the trunk. belam re-extracts f1.sh from the landed leaf and runs it after the owner's grok login as agi-plan-master (marker 08:39:30Z stands). Readings -> the leaf; then DG1's plan-master leaf (T7; config.json grok-bot models grok-4/-4-fast not on the box list: RULES, belam wraps).
- OWNER (via belam 09:4xZ): the 3 council seats -> Fable 5.2 medium, belam host act after L496, one seat at a time. Expect rotation alerts.
- HUB A (owner order 19:4xZ 11-09): use it, never pause to save quota, report any 'limit' reply at once.
- CUT DIR: entry in tmp/gen88/mkcut.py (asserts no ' in any word) -> `python3 tmp/gen86/guard.py tmp/lNNN/cut.sh` -> `sh tmp/lNNN/run.sh > tmp/lNNN/cut.out 2>&1` (run_in_background). A cut crossed by belam's card commit: re-run cut.sh with WORD/LNUM (it re-derives), void the old in tmp/held-void.txt.
- GATE: copy the nearest gateNNN.sh by python replace + assert counts (skills 645; nodes 643/647/649; engine bin/: 639's WHOLE suite); ONE gate at a time; waiters key on the previous cut's l.id or rNNN ALLDONE.
belam: land windows :07-:13 and :37-:52; HOLD mail while one of its lands is armed. My cut window :31-:03.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks, %G? == G) -> paths vs every land ahead -> gate the MERGED tree + [review] to all 3 -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] WHOLE to the builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE |
| scripts | /data/work/gate-sm: gateNNN.sh, tmp/gateqNNN.sh, tmp/lNNN cut dirs, tmp/gen88/mkcut.py, tmp/gen86/guard.py |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays WHOLE (cat); it refuses home-path literals (write [SLASH]) |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read; DG1's F1 fix tip; GATE649 result (trunk now 165084e5de, belam card). Drive v1 upload DONE (belam 10:20:45Z). GATE649 STARTED 10:21:39Z.
2. ps for gateq649; relaunch if gone. GATE649 green -> L497; GATE650 words on a371842afd -> green -> L498.
3. thought-master's answer -> name the running director on g5.4.3.1.1 (a DGo1 edit tip).
4. Each land: [landed] WHOLE to builder + council.
```
## 🔴 Where it stops
gen 89: upload ask SENT to belam; GATE649/650 waiter relaunched, queued behind load5 <= 8 (11.7 at 10:19Z); aio's word on a371842afd owed.
```
FIRST: box read whole; ps -eo args | grep -E '^sh (gate|tmp/gateq|tmp/l4)'; tail -2 /data/work/gate-sm/tmp/gateq88.out
THEN: no gateq649 -> relaunch it; GATE649 green -> cut L497 (mkcut entry g=649 prev=496 since 09:50:00).
```
## §2 Landed gen 88: L490 827803e126 · L491 815778a7c7 (b4842f1e3b VOID) · L492 dc2ff9773f · L493 969357f112 (fbb4515d26 VOID) · L494 c6d9e54f46 · L495 19b8cd62d9 · L496 867177a7f1. L490-L495 verified by alive (and aio/sp on several).
## §4 Traps (gen 88; the TRAP SWEEP moves them to skills/agi-master-gate)
- A trunk red from a CARD line ('uid[SLASH]home[SLASH]unit' in doc:card-belam matched HOME_PATH_RE) failed GATE639 run 3 -> attribute on the pre, re-run the failing file alone on merge(fixed trunk, tip), accept ONLY the named lines in the cut's CN check (L490's way).
- A WORD with an apostrophe broke run.sh's single-quoted WORD= -> mkcut asserts no '.
- A cut sent seconds after belam's card commit went stale (L491, L493) -> re-run cut.sh, void the old.
- My GATE648 pytest helped push load to 22-26 and belam's L496 land timed out (rc 124) -> no gate while a belam land runs at high load; waiters check load5 <= 8.
- A message quoting a home-path-shaped string was refused by gsend -> write [SLASH].
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; alive's vland + vgrid.
## §6 BANKED
- TRAP SWEEP OWED (owner 10-10 rule) for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85-87 §4 (git history) + §4 above.
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2) + the 2c 'resume_failed' row cell.
- posts/thought-master and posts/director-thought-1: never push. CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 04:00Z | road (S) 3/3; F1 script L493+L496 landed | open: belam's F1 run; DG1 plan-master leaf after |
| OWNER: research-then-design as a graph skill (c:e780e4c65887) | meme-master 09:41Z | 09:41Z | 3/3 09:47Z; leaf g4.18.2.2 in GATE650 | open: leaf land; DG1 skill tip; owner answer on SUBAGENTS rule |
| OWNER: deck full pass + A/B (c:61b389266d66, c:1ae05e71c801) | meme-master 09:5xZ | 09:46Z | 3/3 09:53Z; leaf g5.4.3.1.1 in GATE649 | open: running director (TM asked); copy tip |
| OWNER: upload rough-draft-v1 to Drive (c:1ae05e71c801) | meme-master [ask] 10:1xZ | 10:11Z | belam host act, SENT 10:19Z | CLOSED 10:2xZ: belam [done] to meme-master direct, 3 files, rclone check 3/0 |
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | most landed | open: DG2 .46.19; .42.2 runner; .44.7 capsule-xfer |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
