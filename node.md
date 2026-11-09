---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: self-perpetuating
scaffold_hash: c808a090daec9950
season: 2
tags: []
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating — self-perpetuating's card (council loop): the ONE scratch

Replaced whole, never appended; §0-§6 ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (11-09 · gen 62 seated 11:51Z (f 0.12 12:00Z) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk = LOCAL refs/heads/posts/belam 6bf730829e (belam's card over L468 d2c3e96f5a; the SHARED ref; origin/posts/belam on GitHub lags) · L459-L468 EQUAL here · owed: none · gen 62's mails w1-w2 in ~/sp-scratch/g62/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits; the harness's grep is ugrep, sh -c's is GNU); a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, each row RUN on a mutant of the CASE in each spelling its READER takes (gen 61: .46.32's F3 vs engine-post.md:268's ' *'); a claim about what the NEXT pass does is read through every check that runs BEFORE the function you read (gen 61 R6: agi-review:57); a host act is read against what the host READS |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a time or a state is read off its SOURCE (box ref, node), never off this card's summary; a wrong reading already sent gets its own [correction] at once; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g62/wN.txt; mkdir + ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline; host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + `python3 -I ~/sp-scratch/g59/chk.py F < /dev/null` VERDICT CLEAN; SEND = `sh ~/sp-tools/sendw-g54.sh F` (box n empty, 61 s quiet, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B); NOT SENT on unread mail: read, then send again |
| merge-up | SM's rule: [merge-up] OUTSIDE :20-:30. `sh ~/sp-scratch/g61/send-g61.sh F` (send-g56.sh reading the LOCAL trunk; belam's card-only commits pass) waits for :31-:55, gated on box n + council refs vs F.boxbase + trunk moves since F.trunk (write both files at compose) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` run_in_background: one line on mail or on any trunk commit that is NOT belam's board/card (judged by PATHS); ~28 min cap, re-arm after each wake |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace from a script FILE, never the quorum link, never an agi-wt tree; keep §0-§6 ≤ 100 lines (awk '/^## §0/{f=1} /^## §7/{f=0} f' \| wc -l); the turn end commits it (a [grid] 'not grown' line = the cron writers' lock) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>` + W tree == L tree) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` tip, L, W; a config:posts row change: r-land (agi-master-gate :40) + ~/sp-scratch/g60/cellcheck.py |
| OWNER | a range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block (cite skips a grandfathered node WHOLE: engine-post.md:253); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master`; repeated owner words: ~/sp-scratch/g60/shingle.py |
| runs | ONE && chain from `sh skills/agi-master-gate/start-check.sh` through each fixture's setup AND any git archive (gen 61's slip: agi-memory-guard:117, alive's sweep-g70b-r1); every dir "${D:?}"; a probe is a script FILE run with stdin from /dev/null, a line per case AND a 'READ NOTHING' line; a probe that imports engine code calls READ-ONLY functions only (never rotate/heal/send verbs); over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched: `sh ~/sp-scratch/g61/cut.sh <base> refs/heads/tip/self-perpetuating/<name> <path> <newfile> <msgfile>` (signed, prints %G?, mt == tree, numstat, scan; the message ends with the Co-Authored-By line) |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 61: seat 0.06, 13 mails + 3 probes to 0.40 (a word with a code read ~0.02-0.03, a mail wake ~0.005) |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 WORDS OWED NEXT (when SM asks):
   none open. DG1 .31.1.2's 2c stack is 3/3 on EVERY step (2c-5 7de1847701 3/3 at 12:11Z; my words w1 2c-4, w2 [correction], w3 2c-5);
        NEXT for it: GATE626 on 7de1847701 (behind 607 + 614-624), then ONE cut after L469 (2b 091695090d, ARMED with belam: 51a8273735 on
        6bf730829e) -> L-check both as they land. BANKED for the route's next touch (3/3): alive's latent NIT, heal.py resume-failed reads
        an UNREAD dir/record as 'none' (:185 'is not True', :190 bare continue) -> exit 2 + a named line; row + mutant.
   DG2 g7.16.2.1 follow-up before its CLOSE (3/3 TERM): mask_diff_ips + reds._added read '+++ ' only before a file's first '@@'; rows B + F;
        + the board-line fix with MY gen 59 TERM (a counted 8+ digit value under a TOKEN name closed or written as staying RED, with a row).
        Probe kit: ~/sp-scratch/g59/probe-mask.py (cases A-F), probe-assign.py.
   DGo1 .46.32 next touch = MY TERM (3/3): F3 reads summary_live the way engine-post.md:268 does (sed 's/^summary_live: *//p' | head -1,
        fails iff 'true'); mutants 'summary_live:true' + 'summary_live:  true' (~/sp-scratch/g61/probe-f3.sh: both LIVE with F3 rc 0);
        + the URL's source (c60ab183d2) + aio's rival reading (OptMem or OptChat).
 QUEUE (L-check each as it lands): L458 DG2 g7.16.2.1 BUILD b3a5107120 (RULES, belam wraps; edits agi-review :160) · L469 + the 2c stack ·
   gated, 3/3: DGo1 3290e4d263 (GATE619) + addc4e4687 (GATE620) · MY sweep-g60 108de39c0e (agi-review :190, GATE621) · alive bd0461b6fa
   (GATE622) · aio cf31a76262 (GATE623) · alive sweep-g70b-r1 c60ded9079 (agi-memory-guard:117, GATE624) · DG1 r2 8e9fab11ac (GATE614;
   MY NIT: agi-verify:93 'leading indent stripped').
 NEXT TOUCHES, others': DG1 role-meme-master :30 '03:22:28Z' -> 03:20:32Z (my gen 60 NIT) · DS1 drop-in: a build node (alive NIT) + my ':'
   NIT needs cred-piece.t.sh:109's sed anchor · DG1 2c: the comm[:15] narrow form is in; real grok ELF NOT RUN (comm 'exe' on a re-exec).
 HOST: .46.20 ROOT ACT RAN 12:19Z, ROLLED BACK by its own term ([red] belam 12:2xZ: agi-post@.service StandardOutput=null +
   StandardError=inherit, so the journal-line PASS can never pass). Council word on the PASS evidence: mine w4 12:23:12Z = belam's FILE
   CHECK + DS1's 'OR newer than the seed' + TERM 1 (rollback restores the aside copy ONLY if live absent or cmp == credstore) + TERM 2 (run
   the check pre-restart: must read FAIL; UNREAD never PASS); aio 12:22:50Z the SAME rollback condition. Re-run before ~16:30Z (expiry
   16:55:22Z, DS1's read). Then DS1's F1. Word on the re-run's [landed]/[red] only if a term is missed.
 JOB 2 (A12 (3)): v2 LANDED L442; NEXT: row 1's split '85 entered cc > 30; 191 never entered cc >= 6' (sums 276; crap/join.py asserts
   it); then the cuts = goal:g7.33 rounds, one at a time. R=/data/scratch/art/self-perpetuating/council-job2-r2/O.
 OPEN: belam's unnoded class (37/97 bin/*.py); aio fragment; alive audit; .46.29's next record (aio); DG3's .agi/keys leaf (mine, banked);
   DT1 banked; my agi-review :130 note. TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,sendw-g54,send-g56}.sh, bt-g49.py;
   ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/{watch.sh,fix93.py,shingle.py,cellcheck.py}; ~/sp-scratch/g61/{cut.sh,send-g61.sh,probe-*}
 PLACED, others' (check on their next touch, do not chase): DG2 viz-views rows (alive, aio) · DG2 .46.19 V1 remainder · DG2 atomize
   live-link row · SM agi-master-gate (2) gloss :185 + its [merge-up] template's 'at send' collector (alive NIT) · DG1 F3 all-empty mutant
   · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard · goal .13 TABLE rule row
   (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 shared toolchain · belam: agi-node-write:71, agi-memory-guard:48
```

## §2 Landed (L-checked here, all EQUAL; older rows in git: this card's versions to 11-09 11:4xZ)
- L469 51a8273735 DG1 .31.1.2 ACT 2b (PLAIN; p1 6bf730829e; p2 == 091695090d; tree == mt; 6 paths 0 D, blobs == tip; 3 create 100644, no mode
  change; OWNER 0; b-7 24 obj 0 empty 0 flagged; box tokens 0; posts.md 0; 2 new build nodes [mvp] / [goal, mvp], legal). 12:14Z.
- L468 d2c3e96f5a DS1 .46.7 CLOSE (PLAIN; p2 == 173498a5ba; tree == mt; 1 M 0 D; blob == tip; OWNER 0; b-7 11 obj 0 empty 0 flagged; box tokens 0).
- L467 350da62c26 DS1 .46.20 V2 (RULES; p2 == c655f9a0b6; blobs + modes == tip; OWNER 0; b-7 0/0) + belam wrap 4abbc8571c (W tree == L tree).
- L462 16d008072d MY sweep g59 · L460 9a00c318da aio g60 · L459 efc104c8eb DG3 .46.9 · L464 6c7bfee6dd DGo1 g5.4.4 v2 · L466 bcaa87a459
  DG1 privacy: each PLAIN, p2 == the approved tip, 1 M, blob == tip, tree == mt, OWNER 0, b-7 0 empty 0 flagged, box tokens 0.

## 🔴 Where it stops
gen 62 12:24Z 11-09: L468 + L469 EQUAL here; w1-w4 SENT (2c stack 3/3 every step; w4 = .46.20 PASS evidence); owed none; next: the 2c cut's L-check
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call; read the saved start output in the NEXT reply.
  (1) `stat -c '%a %U' /dev/null` = '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; `mkdir -p ~/sp-scratch/g62`.
  (2) arm the wait (§0 'wait' row); L-check each land in §1 QUEUE as it lands (L458 is RULES: lcheck.sh W L + W tree == L tree).
  (3) words in §1 WORDS OWED as SM asks (2c-4 first: read its row AND aio's chain limit).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 61's own; gen 60's (1) MOVED: agi-review :190 by MY sweep-g60 108de39c0e, 3/3, GATE621; its case (c) carried by :58)
- gen 61 (1), 10:3xZ: my 2b pane probe git-archived a tip's extensions/agi with no start check in that command -> CARRIED by alive's
  sweep-g70b-r1 c60ded9079 at agi-memory-guard:117 (a tree-extracting command is a heavy run), named in my w8; check it on its land.
- gen 61 (2), 11:42Z: my R6 word said the next pass reaches _recover_seat's :3845 refusal, read off that function alone; the dead check's
  (1b) at :4235 runs first and vouches an open @id (silent stall), DG1's probe right; [correction] w13 11:45:36Z -> CARRIED by
  agi-review:57 ('a claimed hole -> trace the input through every EARLIER refusal'); the §0 lens row names it. Drop it at the next sweep.
- gen 62 (1), 11:57Z: my 2c-4 NIT's ROW said 'the next _recover_seat launches nothing' for a guard that stops the pass at (1b) BEFORE
  _recover_seat; a row on the callee would launch and read RED -> [correction] w2 11:59:56Z. Same class as gen 61 (2): a ROW for a
  guard is run through the CALLER that reaches it (agi-review:57 carries the rule). Drop it at the next sweep.
- gen 62 (2), 12:10Z: test_bin_help_smoke on a 'git archive <tip> extensions/agi' extract reads 2 RED (p1_ab.py, sensei.py --help need
  .agi/config.json / an agi project) -> not the range's; archive .agi/config.json too, or name them as run-environment reds (w3 did).
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent (11-06: Console credits are for non-CC harnesses only, owner via belam); DS1's .46.7 close (11-09) names it, the split a later owner act.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atom c1 (rules into the matrix math, W4 §12); c2 (crons.py retire) = DGo1's idea in 3290e4d263 (3/3, GATE619)

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A10: CLOSED (rows in git, this card's versions to 11-07 23:0xZ): council jobs 1-3, g14 three-visions -> g5.19, wake-routine test, fuel stereo, season-3 explainer, aio corrections, A9 zero manual commits -> goal .46.30, A10 prayer at each idle spot -> L415.
- A11 OWNER via belam [owner] 23:0xZ 11-07 (SM relay 23:0xZ): the visual dashboard on a screen, graph + crew + workflow cycle + comms cycle, multiple views. CLOSED: placed by alive's [decision] 23:24:04Z (3/3; my w2 + w3) = goal:g7.16.1.11.9.1, builder DG2; BUILT and LANDED at L439 (11-08); its CLOSE = L457 (3/3, EQUAL here 07:08Z 11-09); goal .9 itself -> HORIZON (council T2, 08:5xZ 11-09).
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts; 3 OPTIMIZE ("a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away") = MY council job 2; 4 CREW, DT1's start. CLOSED: placed by alive's [decision]s 23:25:38Z (3 = MY job 2 re-measure, 4 = DT1 only with a TM leaf) + 23:50:05Z (1 = goal:g1.23.1 active, 2 = goal:g1.23.2 horizon; minter DGo1, license builder DG3). 1 DONE (L436 build, L438 close); 3's v2 doc LANDED L442 (its cuts = goal:g7.33 rounds, placed by the council).
- A13 OWNER to belam 02:5xZ 11-09 (belam [landed] [owner] 02:58:14Z, via SM 02:59Z, verbatim there): a new post MEME MASTER (core team; presentation + paper
  via graph routes; shepherd the owner's own final wording in bite-size chunks; may dispatch kids or plain subagents; a post to read the graph and ask;
  coordinate with TM for benchmarks; fully logged in on the owner's account for remote access). CLOSED: placed by alive's [decision] 03:09:15Z (3/3) =
  LAND 1 goal:g5.4.3 = L455 c695e19f31; LAND 2 (row, edge, role doc, card, quorum link) = L463 38d888fbe0 + belam's wrap 09116c0e51 (EQUAL here);
  F3 BIN = L461 e289cd776b; host acts 07:47Z; first start with the owner's login 08:10Z; privacy clause 3/3 = L466 bcaa87a459 (EQUAL here);
  boot true 3beb8abb88 + the pin (my w7 TERM, MET 08:46Z).
- A14 OWNER via belam [owner] 03:14:32Z 11-09 (c:3a09b5900841; SM [relay] 03:14Z, verbatim there): (1) Meme Master starts from the 11-07 class
  presentation -> g5.4.3 OWNER (L455) + role doc (LAND 2); (2) bundles belong on the core town board, no rework; (3) STANDING STOP: pause at
  season 3's end -> rollover on its own -> season 4 bundle FULLY on town:core, every piece ready -> STOP for the owner's review; (4) the owner
  stands by for login. CLOSED 3/3 per part: (1) 3/3 at 03:20:32Z (alive 03:16:03Z, sp 03:19:27Z, aio 03:20:32Z); (3) 3/3 at alive 03:22:28Z
  (my w1 terms: owner-cite is blind on grandfathered g5.4 -> a NEW leaf; the pointer in g7.16.1.11.46) = goal:g5.4.4 + one pointer in g5.4 +
  one in g7.16.1.11.46, DGo1's lane 2 = L461; its v2 (both NITs) = L464 6c7bfee6dd (EQUAL here). (4) the login done 08:10Z. Also owner: CC updates on all boxes = belam's host act.
