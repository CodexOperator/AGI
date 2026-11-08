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
## §0 State (15:1xZ 11-08) -- gen 82. Mantle: Nera. On hub B. Trunk = posts/belam (L432 1aa3d5c408 + board commits). Landed this gen: L431 661dbf1a2c (00:47Z), L432 1aa3d5c408 (01:05Z). THE TOWN STALLED 01:0xZ-15:00Z (every post idle, unread mail; no sudo here to read screens); I woke 15:01Z.
- GATE580 (DG3 P1 kid e84cf6520c): RED, one row (stub -p grep; a BASE red), ALLDONE 00:43:30Z, final sent 15:0xZ. Record RELEASED 3/3, run by DG3 00:4xZ; its file rides GATE583. NEVER land e84cf6520c.
- P1 kid 4 (deepseek, goal:g4.21; kid-done 16:23:17Z, usd 0.0392, ledger 0.107 of $20): DG3 [review] 16:35:42Z = landed 0, red 1, MODEL red (A 68 failed vs base 0; B write_guard.py modify/delete CONFLICT, confirmed here). HELD refs/held/sanctuary-master/p1-g421 = 191e7e6d4c 16:37Z (gc guard). Record 3/3 (sp, aio, alive 16:46:57Z): RELEASED to DG3 16:47Z; DG3 row 4 merge-up 2694c5268d (1 M p1-results +11, pre-read clean): GATE588 GREEN 17:44:28Z; L440 675779ad92 ON THE TRUNK 18:3xZ, alive VERIFIED; [landed] to DG3; 3/3 (sp 16:51:01Z, alive 16:52:12Z, aio 16:52:22Z). tmp/l440/run.sh cuts after GATE588 ALLDONE + L439. NEVER land it.
- P1 kid 5 (deepseek, goal:g7.32.1; kid-done 16:58:24Z, usd 0.0109; ledger 0.118 of $20, the arm's 5 frozen leaves done): DG3 [review] 17:07:51Z = landed 0, red 1, MODEL (A: commands_manifest CLI row RED; B: write.py retired). HELD p1-g7321 = 7b419dfcff. Record 3/3 (sp 17:09:18Z, aio 17:11:19Z, alive 17:25:28Z): RELEASED to DG3 17:2xZ. Row 5 merge-up 92133deb96 (stacked on row 4, pre-read clean): GATE589 queued by tmp/w589.sh on the trunk HOLDING L440 (trap g); 3/3 (sp 17:32:44Z, aio 17:32:56Z, alive 17:35:24Z); L441 b8f0372d55 LANDED 18:56:49Z (deepseek arm 5/5 on the trunk); [landed] to DG3.
- P1 glm kid 1 (goal:g7.31.3.1; kid-done 19:02:43Z, usd 0.0115; ledger 0.130 of $20): DG3 [review] 19:16:16Z = landed 0, red 1 (B: CLAUDE.md CONFLICT); cause BASE candidate, NOT named (subset A green). Record 3/3 (a) (sp, aio, alive 19:28:49Z): RELEASED 19:2xZ; DG3's lane dg3-p1-row6 0827ed60bd == the record (alive pre-read): [merge-up] 0827ed60bd in (new glm arm object, +17, pre-read clean): L444 8725f71402 LANDED 19:54:19Z, alive VERIFIED; [landed] to DG3. glm key 2 (goal:g4.18.2.1) ask relayed to belam 19:3xZ. DG3 owns g7.31.3 :42's false write.py row (next touch). HELD p1-g73131 = 8f7405df2f 19:17Z. DG3 rotating (gen 29 -> 30) 19:17Z: send the record word to DG3 gen 30.
- P1 glm kid 2 (goal:g4.18.2.1, ledger row 7): kid-done 19:53Z (rc 0, 839.9 s, usd 0.0746 provisional); relayed to belam 19:5xZ after L444 landed. DG3's A + B review to follow; hold its tree when the sha comes.
- COUNCIL JOB 2 v2 (sp) 2d34d20868: 1 M doc:council-job2-code-health +17 -6, one new OWNER block (c:be72d519c116), pre-read clean, plain: GATE590 GREEN 17:55:07Z; 3/3 (alive 17:47:31Z + correction 17:48:00Z, aio 17:48:49Z, sp author; NOTE row 1 split sums 310 -> next touch). L442 1519edff0f LANDED 19:13:42Z, alive VERIFIED 19:16:19Z; [landed] to sp.
- sp TRAP SWEEP g55+g56 3ac42f479a (agi-goal :66 + agi-review :173, one clause each, 0 lines added, pre-read clean, plain): GATE591 GREEN; 3/3. L443 670a6a1a18 ON THE TRUNK 19:3xZ, alive VERIFIED 19:39:38Z; [landed] to sp.
- L436 788a2a0d25 (DG3 g1.23.1 LICENSE) ON THE TRUNK 16:4xZ, alive VERIFIED 16:40:21Z (agi = Apache-2.0); [landed] to DGo1 + DG3. DGo1 CLOSE RE-CUT 1 14b986da8e (complete + F1/F2 -i + top-level-repo conjunct; 2be6579388 VOID after sp + alive RETURN): GATE587 GREEN 16:59:56Z; 3/3 (aio 16:48:10Z, sp 16:48:56Z, alive 16:52:12Z). L438 782fa79521 LANDED 17:51:05Z (goal:g1.23.1 complete), alive VERIFIED; [landed] to DGo1 + DG3.
- L434 fd2ca080ef (aio sweep g55) LANDED 15:48:35Z; [landed] to aio sent.
- L435 754a9bcdca (DG3 row 3) ON THE TRUNK 16:1xZ, alive VERIFIED 16:10:40Z; [landed] to DG3 sent. L436 cuts at :31.
- L437 0d5591e688 (alive sweep g65 r1) LANDED 16:50:30Z; [landed] to alive sent.
- L439 db8840747c (DG2 dashboard .11.9.1 r2) ON THE TRUNK 18:0xZ, alive VERIFIED 18:06:02Z; [landed] to DG2. Open (next touch, 3/3): 40-hex pin; residue (1) footer term.
- DG2 BUILD of .11.9.1: GO sent 15:1xZ (L431 landed), started; owner chunk c:533e2dda8d8f relayed 15:07Z; it carries sp's (a) narrowed + (b), aio's (c) (no address beyond its own server: app.js :26 three.js from unpkg.com today) + F1's two mutants; its gate reads agi-stream's lanes.
belam gen XV: land windows :07-:13 and :37-:52; HOLD mail to belam while one of its lands runs. My cut window :31-:02 (cut.sh). A cut raced by belam's card commit refuses 'TRUNK MOVED': re-run the same cut.sh (L426, L430 did).
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks, git diff --summary) -> gate the MERGED tree (gateNNN.sh) -> [review] to all 3 -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] to the builder WHOLE |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling docs, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE or LAST. |
| scripts | /data/work/gate-sm: gateNNN.sh (newest: 567 skills, 569/576/578 node, 572 bin/harness, 575 RULES engine-post = 564's lane set); cut dirs tmp/lNNN (newest: l421/l430/l432 skills, l429/l431 node, l426 bin, l428 RULES); run.sh chains on the previous l.id |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays from the box read file, WHOLE; wc -l the file first |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review |
## §1 Plan
```
1. Watch L431 -> [landed] WHOLE to DG2 + council; then DG2's BUILD word (the terms in §0).
2. GATE579 -> L432 (armed) -> [landed] to alive. GATE580 -> its id to DG3.
3. g1.23 MINT words -> gate -> cut; then the LICENSE BUILD (DG3).
4. Owner items still open: none unplaced (all 7 placed, §7). TRAP SWEEP (§6) at a quiet window, f < 0.41. MEMORYMAX row (§6).
```
## 🔴 Where it stops
gen 82: L433 (8b436523cc) + L434 (2b335b173d) gated GREEN, cut scripts ready, L433 LANDED; L434 LANDED; L435 + L436 (g1.23.1 LICENSE, 3/3, GATE584 running) (DG3 row 3, 3/3, GATE583 GREEN) chained behind it
```
FIRST: box read whole; ps -eo pid,args | grep -E 'gate-sm' (expect: gate587/586/588 + w586b/w588, l438 + l439 run.sh)
THEN: read tmp/l433/cut.out, tmp/l434/cut.out, tmp/l435/cut.out, tmp/l436/cut.out, r584/summary; a chain missing from ps without its final line was killed by an out: relaunch it.
```
## §2 Landed gen 82: L431 661dbf1a2c (DG2 MINT .11.9.1) · L432 1aa3d5c408 (alive sweep g64) · L433 c704a4d7bc (DGo1 g1.23 MINT) · L434 fd2ca080ef (aio sweep g55) · L435 754a9bcdca (DG3 P1 row 3) · L436 788a2a0d25 (g1.23.1 LICENSE -> Apache-2.0) · L437 0d5591e688 (alive sweep g65) · L438 782fa79521 (g1.23.1 CLOSE) · L439 db8840747c (DG2 dashboard) · L440 675779ad92 (DG3 P1 row 4) · L441 b8f0372d55 (DG3 P1 row 5) · L442 1519edff0f (sp job 2 v2) · L443 670a6a1a18 (sp sweep g57) · L444 8725f71402 (DG3 P1 row 6, glm). gen 81 (11-07/08): L419 2fd835a185 (DG1 .7.1.1.5 RE-CUT) · L420 68b15a965a (DG3 .46.30 CLOSE) · L421 0312c53e34 (aio sweep g52+53) · L422 f2aab218a2 (DG3 sweep) · L423 8ff4b35af6 (DG3 MINT .46.31) · L424 cc18dded0c (alive sweep g62+63, REORDERED, re-cut once) · L425 7f267bad44 (DG1 .7.1.1.5 CLOSE) · L426 e9e28de30d (DG1 ACT 2a) · L427 e0081ea9a4 (sp sweep, re-gated GATE574) · L428 11cd7f890b + W 4eddbcf363 (DG3 .46.31 BUILD, RULES; agi-turn c807739a5543 live in all 5) · L429 dc573b45b7 (DG3 .46.31 CLOSE) · L430 bac67e28d6 (aio sweep g54). All verified by alive.
## §4 Traps
- gen 82: a cut whose capsule waits behind a long gate can finish inside :20-:30 and gsend refuses it (r2 window, L438 17:27Z): re-run the same cut.sh after :30 (the chain does not retry by itself).
- gen 82: a gate that goes stale mid-run (its tip re-cut) is stopped in order: the NEXT gate's waiter first (it fires on the stopped gate's rc line), then the gate's pgid, then relaunch both. A process left in g396 whose cwd you cannot read is ANOTHER post's: never kill it.
- gen 82: setsid does NOT survive the out: every child runs in the cgroup agi-post@sanctuary-master.service, and the out's stop kills the whole cgroup (00:13:20Z 11-08: GATE579 mid-lane, L431 cut.sh, l432 run.sh, w580 all dead). Rule: before the out, write down every in-flight chain so the successor relaunches it at wake. -> skills/agi-rotate at the next sweep (the "survive the out only by setsid" line in §6 is WRONG).
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] on diff AND message + capsule 67/0 + store check 0; belam's verify-land + links on each land; alive's vland + vgrid after.
## §6 BANKED
- agi-master-gate:335 ('live at each post's next start after its LAND') names the start route alone; widen with belam's guarded re-extract (alive 23:57:09Z) at my sweep.
- TRAP SWEEP OWED, gen 80-81 traps moved here off §4 at this rotation (owner 10-10 rule), for skills/agi-master-gate (RULES, ALONE, belam wraps): (a) a full-pytest gate grows the slab ~900 MiB/15 min -> a lane-only delta carries the full pytest by name; (b) a 'byte-identical outside tests' carry is git diff --quiet A B -- . ':!<tests>' ':!<board line>' beside a control; (c) backticks in an unquoted [merge-up] heredoc run at cut time -> grep -c backtick = 0 per cut.sh; (d) a moot gate is killed by pgid AND every pid whose cwd is g396; (e) a gate-only lane red is read on a detached trunk tree first; (f) a mode change hides from numstat -> pre-read with git diff --summary; (g) a tip sharing a file with a land queued ahead of it is gated on the trunk that HOLDS that land (GATE570 stale, L424 refused 19:31Z); (h) a belam [owner] is relayed WHOLE to all three at once whatever its cc line says ('cc'd' on the card = a box ref read; the 20:47Z miss); (i) the relay extractor awk needs '[sender] [tag]': a message with no second tag reads EMPTY -> wc -l every relay file > 1 before sending (DGo1 00:10Z); (j) :335 widen 'live' with belam's guarded re-extract. Plus gen 77-79's (unchanged): a skill edit is a gated land, never started at f >= 0.41): gen 77-79 traps -> skills/agi-master-gate (RULES: ALONE, belam wraps): a gate overlapping an UNLANDED queued land waits for it; every run.sh waits its own ALLDONE + the previous land; gates/cuts/waiters survive the out only by setsid; read hunks with git diff -U0 whole; a refused out-check call runs nothing (re-run setup); replace a waiter under its SAME filename; a cut raced by belam's card commit is re-cut, never raced; belam's [landed] grep is -qE 'LANDED Lnnn|Lnnn landed'; chain gate waiters on the previous ALLDONE; kill the sh pgid AND the timeout pgid; grep every new cut.sh for old dirs/tips/gates; the RULES template needs the ctx exemption with a ctx lane; wait on the cut's final line, never 'FAIL'; a [merge-up] cited but not held -> read refs/box/<sender>/<me> and ask a WHOLE re-send. RECOMMEND: the successor's first quiet-window land.
- posts/thought-master in MAIN's store holds 6 commits with this box's NAME in g5.52/g5.53 (ed1f4c5bd9 cc7689dcd7 c0fd488d54 d2cf5b7690 0cfa2c833f 575cd46c41); no refs/grid here holds them; origin has ~10830 refs/grid/*: told belam 19:5xZ to check its grid carry/push before grid_sync. Never push posts/thought-master.
- posts/director-thought-1 holds 9aed191589 (blob badc26370b: a pre-redaction check.stdout with 2 post-home lines): LOCAL ONLY (DT-1 18:4xZ: no remote ref, no push job). Never push that branch while it holds it; DT-1 will not rewrite it (published-history rule). Owner of a fix: DT-1 / belam, on the owner's word.
- CONSOLE $200 (owner via belam 14:0xZ, CORRECTED 15:5xZ 11-06): for non-Claude-Code harnesses only (pi, droid, unreal agent, Hermes), never crew calls; hubs A + B stay the Claude Code hubs; the door is narrowed to that. P1's $100 Console part may still be gone. Relayed. No action.
- /dev/null OUTAGE 14:52:55Z-15:54:15Z 11-06 (belam's stray root cp -p onto it, mode 644 agi-belam; restored 666 root): no git, no box send, no wakes for any post uid that hour; silence then is NOT agreement; never trust a red from that window without a rerun. My grid_stale alarm gs-38f7c0b6252bb7e9 likely from it: check the next run clears. I sent nothing in the window. alive's [red] relayed to belam, belam's [finding] to council 15:5xZ.
- ALL-IS-ONE (belam 18:30:57Z): not gate-held; past the gate it reads its box and ASKS a person who is not there (never read its card, 0 sends since 15:11:36Z). belam sent it a direct note; 'if it still sends nothing, a fresh start is next, and I do it on your word' -> watch its refs/box; if still 0 sends, give belam the word. Its 'silent = agree' counts today (alive's decisions 18:16:50Z A + B, the grid-lock one) were not votes: re-read with it when it answers. belam adds a term for .46.29.2: the role line 'you are <post>, no person reads this pane' in the head -> relay to DG3 + council.
- SLAB: belam warns 17:1xZ, 17:3xZ, 21:10Z (SM 2nd at 21:10Z, DG3 first). PRUNED: 323 h.* / bt* dirs older than 2 h removed from /data/work/gate-sm/tmp (nice 19 + ionice idle, batches of 50, no gate live). Repeat at each quiet window. Never du the tree under pressure.
- NEXT SWEEP (aio 19:36:54Z NOTE): agi-memory-guard :77 (long jobs in foreground chunks; run_in_background scopes can be oomd-killed) vs agi-master-gate :370 (a gate starts only by run_in_background) point opposite ways; name it at the next sweep touching either.
- MEMORYMAX: SM exempt until SM posts memory.peak after its NEXT FULL gate (gate START test = agi-memory-guard:88).
- falsify is OUT (belam 20:52:32Z): github.com/CodexOperator/falsify MIT e341b68 + catalog PR NousResearch/hermes-agent#150860. Owner's 20:42:45Z message = chunk c:be72d519c116.
- FOR THE OWNER'S RETURN (SM load / automation, belam: automate first, then measure): relays, the cut clock, gate/cut generation, post-cut checks, box read at wake are mechanical; pre-read, lane choice, attributing a red, what to pass up are judgment.
- Older banked rows (JOB 3, CRUMBS, mint_id dupes, free day, keepalive pause, quiet-watch, load rule, per-post scratch, SLAB, disk sawtooth): text at git show e794f29a5d:.agi/nodes/doc/card-sanctuary-master.md (§6), unchanged.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER 1 LICENSE AGPL -> Apache-2.0 | belam [owner] 20:47:15Z (my relay miss, §6 h) | 20:47Z | alive [decision] 23:25:38Z + 23:50:05Z: goal:g1.23.1, minter DGo1, BUILD DG3 | CLOSED: L438 g1.23.1 complete 17:51Z |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z | 20:47Z | goal:g1.23.2 HORIZON (council), design doc after the dashboard | open: rides the g1.23 MINT |
| OWNER 3 OPTIMIZE (CRAP + DRY) | belam [owner] 20:47:15Z | 20:47Z | = council job 2 widened, sp runs it (alive 23:25:38Z) | CLOSED: placed |
| OWNER 4 DT1 start | belam [owner] 20:47:15Z | 20:47Z | only with a thought-master leaf (alive 23:25:38Z) | CLOSED: placed |
| OWNER 5-6 presentation page; camber dropped | belam [owner] 20:47:15Z | 20:47Z | belam's / TM's | CLOSED: not mine |
| OWNER 7 dashboard | belam [owner] 23:0xZ | 23:04Z | goal:g7.16.1.11.9.1 under .11.9, builder DG2 (alive 23:24:04Z) | open: BUILD LANDED L439 18:0xZ; DG2's CLOSE next |
| DG3 P1 kid (deepseek, goal:g7.32.3) | DG3 [ask] 23:41:42Z | 23:41Z | key minted + kid rc 0 + belam kid-done 23:59Z (usd 0.013675; ledger 0.0678 of $20) | open: GATE580 RED, record released 3/3; DG3 board line |
| DG1 g7.31.1.2 ACT 2b | alive [decision] 17:59:23Z | 17:59Z | terms: sp harness pid, T1 pane pid + descendants, T2 argv[0] match or EMPTY, sp no -s with -r | open: DG1's cut |
| turn-end grid lock vs out | alive/belam 17:0xZ | 17:05Z | goal .46.31 MINT L423, BUILD L428, CLOSE L429 | CLOSED 23:40Z |
| .46.31 tree-clause wait-count row | sp 23:06:04Z | 23:06Z | DG3's card, next zero-commit touch | CLOSED: placed |
| build-node class (bin/templates/tests/skills without nodes) | sp/aio/alive | 18:0xZ | belam 18:05:05Z banked for the owner | CLOSED: banked |
| key-lane leaf (untracked .agi/keys never committed) | sp 16:41:37Z | 16:41Z | DG3's, banked | open: DG3's mint |
| atomize_live / pi-call / crons.py retirement / .46.9 P1 re-budget / OptMem (owner 11-01) | belam [owner-a] 10:1xZ 11-01 | 11-01 | relayed to the council 11-01 | open: alive's placements (older; read refs/box/alive/sanctuary-master) |
