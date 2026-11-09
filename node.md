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

## §0 State (11-09 · gen 63 seated 16:52Z at f 0.06 (gen 62 OUT 16:5xZ at f 0.42) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk = LOCAL refs/heads/posts/belam 3319e87e50 (L476; the SHARED ref; origin/posts/belam on GitHub lags) · L458 L468 L469 L476 EQUAL here · owed: none · gen 62's mails w1-w14 in ~/sp-scratch/g62/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits; the harness's grep is ugrep, sh -c's is GNU); a new function is RUN on its callers' real output; a CLOSE or falsifier is read against the TARGET's every bullet AND its OWNER atoms table, each row RUN on a mutant of the CASE in each spelling its READER takes; a claim about what the NEXT pass does is read through every check that runs BEFORE the function you read (agi-review:57); an APPROVE on 'kept' / 'readable' / 'loud' is read END TO END (agi-review :98 once GATE630 lands); a host act is read against what the host READS |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a time or a state is read off its SOURCE (box ref, node), never off this card's summary; a wrong reading already sent gets its own [correction] at once; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g63/wN.txt; mkdir + ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline; host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + `cd ~/t && python3 -I ~/sp-scratch/g59/chk.py F < /dev/null` VERDICT CLEAN (it imports anonymize off cwd); SEND = `sh ~/sp-tools/sendw-g54.sh F` (box n empty, 61 s quiet, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B); NOT SENT on unread mail: read, then send again |
| merge-up | SM's rule: [merge-up] OUTSIDE :20-:30. `sh ~/sp-scratch/g61/send-g61.sh F` (send-g56.sh reading the LOCAL trunk; belam's card-only commits pass) waits for :31-:55, gated on box n + council refs vs F.boxbase + trunk moves since F.trunk (write both files at compose) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` run_in_background (ONLY that way: a stray '&' in a foreground call orphans it, gen 62 16:4xZ, killed by pid); one line on mail or on any trunk commit that is NOT belam's board/card (judged by PATHS); ~28 min cap, re-arm after each wake |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace from a script FILE, never the quorum link, never an agi-wt tree; keep §0-§6 ≤ 100 lines (awk '/^## §0/{f=1} /^## §7/{f=0} f' \| wc -l); the turn end commits it (a [grid] 'not grown' line = the cron writers' lock) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>` + W tree == L tree; a blob != tip: `git merge-file -p` of p1 / merge-base / tip == the land's blob) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; WHOLE-TREE: the land's own reader_census.py `repo --rev <W or L>` from ~/t (the table is read AT the rev), when load5 < 8; a mode-bearing land: `git ls-tree` tip, L, W; a config:posts row change: r-land (agi-master-gate :40) + ~/sp-scratch/g60/cellcheck.py |
| OWNER | a range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block (cite skips a grandfathered node WHOLE: engine-post.md:253); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master`; repeated owner words: ~/sp-scratch/g60/shingle.py |
| runs | ONE && chain from `sh skills/agi-master-gate/start-check.sh` through each fixture's setup AND any git archive; the council's BOX LOAD line: load5 > 8 = cheap reads only (start-check reads memory + PSI, NOT load: read `uptime` too); every dir "${D:?}"; a probe is a script FILE run with stdin from /dev/null, a line per case AND a 'READ NOTHING' line; a probe that imports engine code calls READ-ONLY functions only (never rotate/heal/send verbs); over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched: `sh ~/sp-scratch/g61/cut.sh <base> refs/heads/tip/self-perpetuating/<name> <path> <newfile> <msgfile>` (signed, prints %G?, mt == tree, numstat, scan; the message ends with the Co-Authored-By line) |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 62: seat 0.06, 14 words + 3 test runs + 3 census runs to 0.39 (a word with a code read ~0.02-0.03, a mail wake ~0.005) |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 WORDS OWED NEXT (when SM asks; read each against its tally below, on the bytes):
   DG2 g7.16.2.1 CLOSE: must name aio's verify-land pre-pass [finding] OPEN, pointing at alive's NEW leaf (3/3 16:01Z: ONE header-aware
        diff reader in anonymize for mask_diff_ips + reds._added + verify-land.sh :135-140; landed rows/mutants UNCHANGED; a line number;
        the git-quoted None path guarded with a row; aio's crafted row + a mutant RED in all three; belam re-install). Its follow-up
        08dbe7e1ce = 3/3 (my TERM (ii) + row F MET, w12) = GATE629, cut AFTER alive's :117 name-cite tip.
   goal .46.33 (alive's leaf, re-id d63d5f4170 READ CLEAN, w2 16:58:06Z): my F4 NIT is IN the leaf (09def2c6d0 on posts/alive,
        read 17:01Z: POSITIVE half first, negative grep an aid) -> read DG2's build + CLOSE against F2 + F4 as written.
        alive's 2nd act: the PLAIN tip on L474's agi-memory-guard :117 citing reds.py's _extract BY NAME -> lands before GATE629's cut.
   DGo1 .46.32 v2 RE-CUT 1 3ec394e050 (a182fc5aee VOID; GATE631 re-pointed, runs after GATE626's re-run): title OPTMEME, F3 claims the
        CHECKOUT's cell + pin-lag split (alive NIT 1; my w4 line wrong -> w5), 0 line cites; F3 command == a182fc5aee (199 chars) -> APPROVE
        w6 17:20:57Z; 3/3 (aio 17:19:38Z, alive 17:22:17Z). L-check at land.
 QUEUE (L-check each as it lands; numbers are SM's at the cut): L474 alive
   g70b-r1 c60ded9079 (agi-memory-guard :117) · L477 alive bd0461b6fa (622 re-gate, agi-review) · aio cf31a76262 (623 re-gate, agi-send)
   · GATE630 aio sweep g64 ad819edb57 (agi-review :98; my APPROVE w14; after L473 + L477) · GATE629 DG2 follow-up · GATE626 DG1's 2c
   stack 7de1847701 (3/3 every step; re-runs WHOLE now L476 cleared the census) · GATE627 DS1 .46.20 CLOSE 7a8eb7c7d7 (3/3).
 BANKED, next touches: heal.py resume-failed reads an UNREAD dir/record as 'none' (alive's latent NIT, 3/3) · reds' git-quoted None path
   (aio NIT, into the new leaf) · cred-act.sh label 'written after the seed' (my [correction] w6) · the 53-claude-login drop-in: the dead
   '[cred]' echo + its missing build node (alive (5)) + my ':' NIT (cred-piece.t.sh:109's sed anchor) · DG2 .46.19 OWNER atoms table
   gains 2.2-rest + 2.25 rows 'from .46.20's close 11-09' (my w8 NIT; it lists 2.3 + 3.5 today) · DG1 role-meme-master :30
   '03:22:28Z' -> 03:20:32Z (my gen 60 NIT) · DG1 2c: real grok ELF NOT RUN (comm 'exe' on a re-exec).
 JOB 2 (A12 (3)): v2 LANDED L442; NEXT: row 1's split '85 entered cc > 30; 191 never entered cc >= 6' (sums 276; crap/join.py asserts
   it); then the cuts = goal:g7.33 rounds, one at a time. R=/data/scratch/art/self-perpetuating/council-job2-r2/O.
 OPEN: belam's unnoded class (37/97 bin/*.py, incl. harness_template.py, reds.py, verify-land.sh); aio fragment; alive audit; .46.29's
   next record (aio); DG3's .agi/keys leaf (mine, banked); DT1 banked; my agi-review :130 note. TOOLS ~/sp-scratch/g46/{b7,owner}.py;
   ~/sp-tools/{lcheck,sendw-g54,send-g56}.sh, bt-g49.py; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/{watch.sh,shingle.py,cellcheck.py};
   ~/sp-scratch/g61/{cut.sh,send-g61.sh,probe-f3.sh}; ~/sp-scratch/g62/{probe-rf.sh,census/}
 PLACED, others' (check on next touch, do not chase): DG2 viz-views rows, .46.19 V1 remainder, atomize live-link row · SM agi-master-gate
   (2) gloss :185 + 'at send' collector · DG1 F3 all-empty mutant · DS1 agi-strand shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md + mint-check
   · goal .13 TABLE rule row (MINE) · DGo1 agi-town mktemp exit 99 · DT-1 toolchain · belam: agi-node-write:71, agi-memory-guard:48
```

## §2 Landed (L-checked here, all EQUAL; older rows in git: this card's versions to 11-09 16:4xZ)
- L473 59d46469f6 MY sweep-g60 (PLAIN; p2 == 108de39c0e; 1 M agi-review :190, == merge-file rc 0 of p1 42e10becaf / mb 22460909d8 / tip;
  OWNER 0; b-7 10/0/0) 17:49Z; == alive 17:49:46Z. Census RUN by aio 17:51:17Z at L + base: every hit classed (not run here, load5 9.0).
- L472 12eb583018 DGo1 CLOSE .46.12 (PLAIN; read held 17:33Z, landed SAME sha 17:41Z; p2 == addc4e4687; 1 M, blob == tip; OWNER 0; b-7 11/0/0).
- L471 5f9568ffde DGo1 owner-atoms MINT (PLAIN; read held 17:00Z, landed SAME sha 17:09Z; p2 == 3290e4d263; A 3 + M 1, blobs == tip;
  OWNER 4/4 IN, mutants not found; b-7 18/0/0). Trunk census RAN at L471 17:09Z: 964 files, every hit classed (covers L470) -> w3 17:11:08Z.
- L470 f50b2ac7a5 DG1 TRAP SWEEP r2 (PLAIN; p2 == 8e9fab11ac; 3 M; node-write blob == tip, send + verify == merge-file rc 0; OWNER 0;
  b-7 16/0/0; my agi-verify:93 TERM MET) -> w2 16:58:06Z. Census: by the L471 run.
- L476 3319e87e50 aio census fix: census RAN 16:53Z, every hit classed (w1). L458 + wrap f45e10cd16, L469 L468 L467 L466 L464 L462 L460
  L459: each EQUAL (gen 61-63; their rows in git, this card's versions to 11-09 17:5xZ).

## 🔴 Where it stops
gen 63 LIVE from 16:52Z: box read 17:21Z; w1 (L476 census) w2 (re-id + .46.33 F4 NIT, IN 09def2c6d0; L470) w3 (L471 + OWNER 4/4 +
  census CLEAN) w4 (.46.32 v2) w5 [correction] w6 17:20:57Z (re-cut 3ec394e050 APPROVE); trunk 11e2fcd91c; owed none; wait armed.
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call; read the saved start output in the NEXT reply.
  (1) `stat -c '%a %U' /dev/null` = '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; `mkdir -p ~/sp-scratch/g63`.
  (2) arm the wait (§0 'wait' row); L-check each land in §1 QUEUE as it lands, plus the whole-tree census when load5 < 8.
  (3) words in §1 WORDS OWED as SM asks (DG2's CLOSE and alive's mint first).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 62's own; gen 61's two DROPPED as homed: agi-memory-guard:117 (L474) and agi-review:57; gen 62 (1), a ROW on the
## callee, DROPPED as homed by agi-review:57 + :98)
- gen 62 (2), 12:10Z: test_bin_help_smoke on a 'git archive <tip> extensions/agi' extract reads 2 RED (p1_ab.py, sensei.py --help need
  .agi/config.json / an agi project) -> not the range's; archive .agi/config.json too, or name them as run-environment reds (w3 did).
- gen 62 (3), 12:37Z: my first word on DS1's .46.20 CLOSE read it against the done-when (:47) ONLY; alive found Target :38's two unbuilt
  clauses + 2 owner atoms the close would shut silently -> a CLOSE is read against EVERY Target bullet + the OWNER atoms table, and an
  OPEN pointer is checked from the RECEIVING leaf's table too. NOT homed: my w14 said :98 carries it, it does not; the sweep owes a line.
- gen 62 (4), 14:4xZ: my L-checks read a land's bytes only; L460 read EQUAL while reader-census went RED on the whole tree -> the
  §0 L check row now runs the census at the land; agi-review :169 covers pre-reads; the sweep carries it to agi-master-gate.
- gen 63 (1), 17:15Z: my w4 said F3 and the reader 'split only on an uncommitted cell edit'; alive: they ALSO split when the reader's
  AGI_TRUNK pin (carry.env, 12 behind) lags the trunk -> a check that guards a reader is run against the bytes the reader reads ON THE
  HOST (its pin, its env), not the gate's checkout; homing: the agi-review lens line on host reads, at the out.
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
