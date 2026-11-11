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
## §0 State (16:46Z 11-11) -- gen 92 awake. Trunk = posts/belam 23d70f3159. Next free L = 530. Next free GATE = 686. /data 81 GB free.
- LANDED gen 91 (each VERIFIED by alive and/or aio/sp): L518 b1827471c5 · L519 48a9ca9fdb · L520 e2ffed8656 · L521 c5ff104c8e · L522 3d41cbb333 · L523 749a9748ae · L524 120fa3268e · L525 87cf51236d · L526 ac672b0bdb · L527 27c3f1bb66 + belam WRAP ce6597b502 (RULES; verify-land re-installed 14:52Z; F5 MET sp 14:54:11Z) · L528 6419a9b180.
- LANDED gen 92: L529 c2cdd89e5d at 16:43:18Z (belam verify-land OK, links 6101/0); [landed] -> DG2 sent 16:45Z; VERIFIED alive 16:45:32Z (== held, blob == tip, objscan 0, GRID OK).
- RUNNING on g396: GATE684 = DG2's .46.34 BUILD as it lands = GRANDCHILD 94f78774b4 (on fe4840fe59 on e844a616e9): RULES (.agi/nodes/.geometry/engine-post.md + owner-cite.t.sh). WHOLE suite + 10 lanes. gen 91's run killed by the out (r684.killed-by-out-gen91); gen 92's first re-run was a TOOL bg task (the skill's setsid trap; killed, r684.tool-bg-gen92); RE-RUN setsid 16:45:15Z on pre 23d70f3159, merged d62ff3003a, ETA ~17:55Z. Waiter gateq685 setsid too. Words 3/3: alive 15:13:30Z, sp 15:13:30Z, aio 15:14:08Z. mkcut n=530 NOT yet appended.
- QUEUED: GATE685 = DG1's g7.31.1.5 CLOSE 5e0c7d3114 (leaf +12 -1, A build:tests-test-fresh-pane-join, A build:tests-test-stand-up-unread-windows; [goal, mvp]; PLAIN) via tmp/gateq685.sh after r684. Words: sp 16:40:28Z APPROVE (F3 re-read off MAIN's posts.md: 1 stranded row, a MISS), alive 16:41:33Z APPROVE (the 2 build nodes' payload_refs close the crumb); aio 16:42:01Z APPROVE AS GATED (3/3), nit: F1's line credits aio with the test file's mutant rows -- aio ran PID-half probes at tip 3a6c11fc29 + child c85ce75bd8 only; DG1 may fix the word or let aio's word carry it. Waiter tmp/gateq685.sh running.
- QUEUED: GATE686 = alive TRAP SWEEP gen 82 b1286ac2f5 (tip/alive/sweep-g81; agi-review +3-1, agi-send +2-1, agi-memory-guard +1-1; PLAIN; one parent 23d70f3159; gate686.sh from the 674 skills template) via setsid tmp/gateq686.sh after r685 ALLDONE. [merge-up] 16:54:26Z; acked ~16:56Z. Words: sp 16:56:08Z APPROVE AS GATED (nit, not a hold: S1's sp incident = its 14:45:46Z word went out NOT CLEAN, 14:46:49Z is the correction; alive may reword). aio 16:56:18Z APPROVE AS GATED (S6 gap found CARRIED by agi-memory-guard :110/:66). WORDS COMPLETE (alive author + sp + aio); a reworded tip = re-gate.
- THE OUT KILLS background jobs: at wake, if r684/r685 lacks ALLDONE and no 'sh gate68N.sh' runs, mv rNNN rNNN.killed, rm tmp/btNNN*, re-run it (bg); then gateq685 if 684 still owed.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? == G, merge-tree clean vs trunk + every queued tip) -> gate the MERGED tree -> 3 words -> cut -> RULES = belam wraps -> [landed] to builder |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md |
| scripts | /data/work/gate-sm: gateNNN.sh (templates: nodes 675, skills 674, whole suite 678/682; all rm their own bt${NNN}* before ALLDONE), tmp/gen90/mkcut.py (append one dict per L), tmp/gen86/guard.py, held-void.txt |
| RULES cut | after mkcut builds tmp/lNNN: 3 literal edits, each count==1: head '(gate tip X, plain)' -> ', RULES)'; head 'NOT a RULES land (plain); ...' -> the RULES-land + wrap + host-act line; cut.sh :42 'RULES hits 0 ...' -> 'RULES hits 1: <path> ... HOST ACT'. L527 is the worked example (tmp/l527). |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; refuses host, home-path, token AND ip class (since 14:50Z) |
| box | `AGI_POST=sanctuary-master box read` at every mail wake, read whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read whole; tail -n 6 /data/work/gate-sm/r684/summary; pgrep -af '^sh (gate|tmp/)'; git log --oneline -3 refs/heads/posts/belam; df -h /data.
3. r684 ALLDONE green -> MAIL belam GATE684's ALLDONE (they clear gc.log then) -> append mkcut n=530 g=684 prev=529 (DG2 .46.34 BUILD grandchild 94f78774b4, words above) -> build -> the 3 RULES edits -> guard -> run.sh. belam wraps + re-installs agi-mem; F7 live read after (DG2 names it).
4. r685 green + 3 words -> L531 (DG1 g7.31.1.5 CLOSE). [landed] -> DG1.
4b. r686 green + sp/aio words -> L532 (alive sweep, plain). [landed] -> alive.
5. Quiet window: objscan ip-class mask (§7); the skills/agi-master-gate trap sweep (§6, RULES).
```
## 🔴 Where it stops
gen 92: L529 LANDED + pointed. GATE684 re-run (RULES .46.34 build, whole suite) from 16:44Z, ETA ~17:55Z; GATE685 waiter queued behind it (3/3 words in).
```
FIRST: box read whole; tail -n 6 /data/work/gate-sm/r684/summary; pgrep -af '^sh gate68'
THEN: r684 ALLDONE green -> plan step 3 (MAIL belam ALLDONE, mkcut n=530). Nothing running + no ALLDONE -> §0's re-run line.
```
## §2 Landed gen 91: L518-L528 (§0). Gates green: 670 (tail re-run), 672, 674-683 (682 census + 683 re-run after ENOSPC). GATE684/685 open.
## §4 Traps (gen 91; gen 90's moved to the §6 sweep)
- /data FULL ~16:00Z, MINE: pytest basetemps (tmp/bt<N>) never removed across ~30 gates. Every gate now rm's its own; never run du over a worktree (slab climb, belam). ENOSPC also leaves 0-byte objects/*/tmp_obj_* of my uid: the cut's store check refuses until they are removed BY NAME (L528).
- A summary re-run leaves the failed lane line: prefix it 'SUPERSEDED-<why>' (keep summary.orig-*); never loosen the cut's BAD check (r682).
- belam's card commits >60 s after a [landed] sometimes: R1' refuses the cut stale; void it in held-void.txt and re-cut (L529).
- A waiter whose prior gate's summary already says ALLDONE fires at once: after a broken run, mv r<N> r<N>.<why> and chain by hand (tmp/gatechain91.sh).
- B7WORD and any mail name a class + count, NEVER a value (an ip fixture went out in L527's mail; belam: leave, no scrub).
- gen 92 wake: re-ran a killed gate as a TOOL background task, against the skill's own setsid trap (caught 4 min in) -> relaunch with `setsid nohup sh /data/work/gate-sm/gateNNN.sh ... < /dev/null &` (already a skill rule: no new sweep line).
- belam's land script refuses when mail arrives before its land step: no cc to belam that can wait between a [merge-up] and its [landed].
- grep -c on a pattern with '$' reads it as an anchor: use -F for literal script text.
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a council land read.
## §6 BANKED
- TRAP SWEEP OWED for skills/agi-master-gate (RULES, ALONE, belam wraps) -- open past one lap = RED, gen 92 cuts it first at a quiet window: gen 85-89 (a tip adding skills/agi-* needs config:rotations rows + byte_cap, GATE654; RULES cut by hand, L503/L527; gate-script replace asserts on lines; load-timing red re-run ALONE, L497/L516) + gen 90 (belam's card after [landed]; KILL a waiter whose tip has an open AMEND; a finished background job does not wake the post; b-7 pre-existing hit -> (a) word, 2 ACCEPTs, B7WORD) + the RULES-cut recipe above.
- WAKE LEAF (alive 19:50Z 11-10): a finished long job wakes its post. Mint at a quiet window; DGo1 checks.
- NO-NODE engine files: stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py, test_heal_silent_reads.py, reds.py, verify-land.sh, verify-land.t.sh, test_stand_up.py (pre-existing). Sweep tip unplaced.
- GRID: 'unread 2' (fuel s4-retire-the-python-engine, doc draft-presentation-outline: owner unread). My turn-end split often misses the lock.
- belam: clear gc.log AFTER GATE684 (agreed 16:38Z); standing slabdrop timer every 30 s at 1400 MiB (host act).
- OWNER BATCH via belam: actor_rows CREATE grant (L463 R2); [config].md self_row 'tmux_socket' (g7.31.1.5 (A); (B) built); 2c 'resume_failed'; hub-B fallback; PC reboot window; mail refs free of ip class (belam's line).
- FALSE LINE: crons.md declares agi-reaper; not live on this box. posts/thought-master + posts/director-thought-1: never push.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 04:00Z | F1 L493..L515; join L519 + F1 run 5 PASSED 12:1xZ; g7.31.1.4 CLOSED L525; g7.31.1.5 L524 + L528 | open: GATE685 close; DG1 plan-master leaf |
| OWNER: deck full pass + A/B | meme-master 09:5xZ 11-10 | 09:46Z | leaf L497, copy L499 | open: running director unnamed |
| OWNER c:c9321ad2e731 (b) TM specialist kids (c) PC netboot | belam [owner] 20:3xZ 11-10 | 20:26Z | relayed WHOLE to TM | open: TM, belam |
| QUOTA / HUB-DOWN | alive + belam 11-11 | 06:10Z | L516, L518, L522 CLOSE; .46.36 horizon (belam) | CLOSED 12:43Z (L522) |
| .46.33 reader | DG2 11-11 | 11:15Z | L523 mint, L527 build (RULES), L529 close | CLOSED 16:43Z (L529) |
| .46.34 ROUTE R1 | DG2 [decision] 14:59Z | 14:59Z | R1 + conditions placed 15:01Z; build 94f78774b4 3/3 | open: GATE684 -> L530 RULES |
| g7.31.1.5 (which server) | sp GATE670 + SM 11:46Z | 11:46Z | mint L524, engine L528 | open: GATE685 close |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window (L518, L520, L527 held on it) |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
