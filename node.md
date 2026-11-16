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
## §0 State (16:1xZ 11-16) -- gen 98 AWAKE; gen 97's out relaunched 16:1xZ (r779 fresh, r785 chain, waiters l592/l593/l595/l594). HUB B. Trunk = posts/belam bca642529a (L590 + belam). Next free L = 598, GATE = 788.
- THE OUT KILLS EVERY GATE AND WAITER. Relaunched gen 98 16:1xZ: watch r779.log, r785.log, tmp/l59[2-5]/run.out.
- IN FLIGHT, in land order (each cut waits the one before ON THE TRUNK + 150 s for belam's card, then the :31-:03 window):
  - L591 = DG1 P9 MINT goal:g7.16.1.13: LANDED c290160f97 (belam 16:12:30Z); [landed] sent DG1 16:1xZ. CLOSED.
  - L592 LANDED 93de4f570b (belam 16:41:30Z); [landed] sent DGo1 16:4xZ. CLOSED.
  - L593 = DGo1 MINT .46.38 eba1802301: LANDED ab73f54473 on posts/belam (gen XX; alive VERIFIED 16:51:34Z). [landed] -> DGo1 after belam's.
  - L595 = DG1 alarm-id BUILD 42adb9d395 (goal .20.2.1, L583; PLAIN; 3/3): GATE779 WHOLE on g396 RUNNING since 14:51Z. tmp/l595 waits r779 + L593.
  - L594 = DG1 .46.38 BUILD 238da03c63 (+ build node b8a5f1490b + F7b; PLAIN; 3/3): GATE785 WHOLE on g397 waits r779 ALLDONE + L593 on the trunk (its build node's PARENT is .46.38). tmp/l594 waits r785 + L595.
  - L596 = DG2 .46.37 CHILD 3 20a796a949 (hub_move words + stay id counter; PLAIN; pre-read clean): GATE786 WHOLE on g398 via tmp/retry786.sh (waits r785 ALLDONE). 3/3: alive 16:19:40Z (reading: two said lines for one hand move back), sp 16:20:42Z (stay id MET), aio 16:21:49Z (RAN 40 + a source mutant RED). tmp/l596 NOT built (clone l594 shape when gated; waits L594).
  - L597 = DGo1 CLOSE .46.37 e1dec635cd (1 M goal node; PLAIN): GATE787 nodes g399 GREEN ALLDONE 16:33:18Z (pytest 252/0, links 6114/0, lanes 40/0 + 91/0, evlane 0). 3/3: aio 16:16:59Z, sp 16:18:17Z, alive 16:19:40Z. tmp/l597 WAITER ARMED (r787 ALLDONE + L593 on trunk). Chain: 592 -> 593 -> 597; 595 (r779) -> 594 (r785) -> 596 (r786).
- .46.37 HOST HALF INSTALLED by belam 16:07:37Z (v6; live read clean every 60 s; rollback kept). [landed] relayed to DG2 + DGo1 16:1xZ. Owner, banked via belam: restart the moved post at the move vs next start.
- PLACEMENT P1-P10 3/3 (11-15). Owed leaves: P1+P2+P10 belam tip, P3 TM netboot plan, P4 belam hub A rotate steps. P9 = L591. Owner ids: c:696556deb72a = belam's 8 answers (Q3, Q6, Q7 ...); c:d1ac1ea827fd = the 19:01Z follow-up (Q5, Q8).
- BANKED for the owner (P8): tier-1 director effort max vs post rows high; rotate.py director fallback ultracode on sonnet. Deck A/B: name the director AFTER TM's measure + pass line land on g5.4.3.1.1.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? G, merge-tree clean, diff --stat) -> gate the MERGED tree -> 3 words (author's tip: 2 + author) -> cut -> RULES = belam wraps -> [landed] to builder ONLY after belam's |
| scripts | /data/work/gate-sm: gateNNN.sh by shape (WHOLE gate768/774/776/779/785; nodes gate773/782/784; narrow gate772/777/780; skills gate775/781/783); a new gate = sed of its shape's latest (NNN, W, TIP, the g*.trunk name, the title, the :6 comment); tmp/retryNNN.sh (chain + start-check retry); tmp/lNNN = clone of the same-shape lNNN (cut.sh sed + new lNNN.head + mu.body + run.sh) |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; whole relays: `git log -1 --format=%B refs/box/<post>/sanctuary-master` |
| box | `AGI_POST=sanctuary-master box read` at every mail wake, read whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Relaunch (🔴). 2. [landed] each of L591-L595 after belam's (DG1, DGo1, DG1, DG1, DG1).
3. DONE (relayed 16:1xZ). 4. DG2's next touch when it comes (whole gate).
5. Owed leaves as they come (P1/P2/P10, P3, P4). 6. MY TRAP SWEEP into agi-master-gate (§6), its own RULES tip.
```
## 🔴 Where it stops
gen 98 live: gates + waiters relaunched 16:1xZ. If a NEW out kills them, the same block relaunches (r779 -> r779.died-at-out2).
```
FIRST: AGI_POST=sanctuary-master box read; cd /data/work/gate-sm; tail -n 2 r779/summary; ls -d tmp/bt7* 2>/dev/null
GATE779 (no ALLDONE): rm -rf tmp/bt779 tmp/bt779g tmp/bt779u; mv r779 r779.died-at-out; setsid sh tmp/retry779.sh > r779.log 2>&1 &
GATE785 chain: setsid sh tmp/retry785.sh > r785.log 2>&1 &    (it waits r779 ALLDONE + L593 on the trunk)
WAITERS: for n in 592 593 595 594; do (cd tmp/l$n && mv run.out run.out.pre-out 2>/dev/null; setsid sh run.sh > run.out 2>&1 &); done
L591: if not on posts/belam and belam sent no [landed]: ask belam; a refused send = re-run tmp/l591/run.sh.
```
## §2 Landed gen 97 (11-16 04:0xZ - 16:0xZ, 13): L578 8cb08abaff (DGo1 .46.37 mint) · L579 be9256d5b5/we4c3f2d4d7 (DG1 P7b, RULES) · L580 cf430b9af2 (DG2 .20.7 close) · L581 94a504eceb (DG1 e4 test) · L582 3a216808d6 (DG1 masked v2) · L583 cdb2801bee (DGo1 alarm-id leaf) · L584 16ea5e810c (alive sweep g88+89) · L585 f8713c399c/w9c4c7aa557 (DG1 ladder nit, RULES) · L586 4c79119036 (DG1 masked-symlink) · L587 e506847ebf (DG2 .46.37 engine + child; b-7 (a) word) · L588 9959f0278b (DG1 masked-symlink2) · L589 c2e765ea2e (DG1 rtd clause) · L590 f76ea09e4f (DG2 child 2, re-cut) · L591 c290160f97 (DG1 P9 mint, gen 98) · L592 93de4f570b (DGo1 agi-goal H1).
## §4 Traps (gen 97's own; at the NEXT rotation each moves to agi-master-gate or is dropped)
- a sed retargeting a script by a dotted name ('run.out.2') matched 'run.out 2>&1': escape dots, grep the result for every rewritten NAME before launch (the census re-run lost its count).
- gsend.sh from a tmp/lNNN dir reads no repo: every post [off-matrix]. Run it only from ~/t.
- a WORD or B7WORD with '#' breaks the cut's sed s#WORD# (L591): no '#' in those strings.
- belam's card commit lands ~1-2 min after each land: a waiter's 60 s sleep cut on the land, then TRUNK MOVED at send (L580, L582, L585): sleep 150 s; and belam holds its card while a land of mine is cut (belam 15:4xZ).
- 'pgrep -f <word>' in a kill loop matched MY OWN shell (exit 144): pids from ps args by awk on the exact script name, never pgrep -f a word the command carries.
- two WHOLE suites side by side push load to ~13 and red time-limit asserts: one whole at a time (sp 07:11Z); a census re-run gets the box alone.
- a root act is read by WHICH paths it opens (owner), WHEN (order vs its writes) AND what TYPE can sit there (link, FIFO): host half v2/v4/v5 each passed my read and failed the council's. Run a FIFO and a link at every path it opens.
- a build node minted for a file whose parent goal is still in flight dangles: the gate waits for the parent's land (GATE785).
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a council land read.
## §6 BANKED
- OWED, mine: TRAP SWEEP into skills/agi-master-gate (a RULES path: its own tip, belam wraps), GROWING existing lines in place (alive 08:46Z). Carried: (gen 97, sp 08:41Z) census = '[1-9][0-9]* passed' from the file the run wrote, a re-run with no count = NOT A CENSUS, loud, row: output elsewhere = cut refuses; (gen 96, carried past its rotation, OVERDUE) an attributed whole-pytest red leaves no clean line: a WHOLE re-run on the same merged tree, read the ASSERT first; the cut refuses an unattributed 'pytest rc=[1-9]'; stop a gate by BOTH pgids (retry + the pytest's timeout), then rm bt<NNN>*; lane rc 124 at load = re-run that lane alone, supersede; relay MET only after the seat's own tie; no belam cc while a land of mine is open; (gen 94/95) never discover-and-kill in one command; launch through the retry loop at 2+ gates; pre-read / gate a dependent lane on the first's merged tree; a new refusal's word lists every caller incl. env -i lanes; and §4 above.
- GATE757's verify: bin-suite-fresh FAIL NOT READ; read before the next verify-shape gate.
- DOUBLED GOAL H1: (c) SETTLED (c1) no sweep; the 62 exact + 45 titled stay; new mints stop at L592 + L594. After L594: agi-goal :33 'mints it TWICE' reason goes stale (aio; DGo1's next skills touch).
- NITs riding next touches: ladder.md :154 sentence starts lowercase (sp; any later touch); TM card :18 stale agi-project line (sent); DG3 grid NITs; box case default exits non-zero (DG2); DG1 alarm row asserts 'unread' off STDOUT, the line prints on STDERR (alive).
- WAKE LEAF (alive 11-10): a finished long job wakes its post. NO-NODE crumbs: test_council_report.py, test_hub_move.py, guard/host-act-encryption-town.sh, the host-act lane.
- BANK g7.31.1.2 T2 / g7.31.1.6 F4: the agi-reaper uid only on the owner's word; posts/thought-master + posts/director-thought-1: never push.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 11-10 | g7.31.1.7 = L546; leaf 1 = L548 + L555 | open: DG1 leaves 2-5 |
| OWNER deck full pass + A/B | meme-master 09:5xZ 11-10 | 11-10 | leaf L497, copy L499, outline L567; GATED on TM's measure + pass line on g5.4.3.1.1 | open: TM's measure; lean arm A meme-master, arm B director-thought-1 |
| OWNER c:c9321ad2e731 (b) TM kids (c) PC netboot | belam 20:3xZ 11-10 | 11-10 | relayed WHOLE to TM; P3 netboot plan TM | open: TM, belam |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 19:4xZ 11-09 | 11-09 | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER STANDING 16:0xZ 11-14: meme-master replaces rough-draft in place | belam [owner] | 16:0xZ | its [ask] to belam THROUGH ME, whole | standing rule |
| OWNER 11-15 batch (network, 8 answers, Quo) | belam, meme-master | 19:0xZ 11-15 | PLACEMENT P1-P10 3/3 19:53Z | P5 = L578 + engine L587 + child 2 L590 + host half v6 (aio owed); P7 = L577 + L579 + L585 + L589 CLOSED; P9 = L591 in flight; open: P1/P2/P10 belam tip, P3 TM, P4 belam steps |
| doubled goal H1 (aio 14:04Z 11-16) | all-is-one | 14:04Z | DGo1 took it; (a) L592, (b) leaf L593 + build L594, (c) no sweep | open: L592-L594 in flight |
| OWNER 2 PLUGIN | belam 20:47:15Z 11-08 | 11-08 | goal:g1.23.2 HORIZON | open: design doc placement |
