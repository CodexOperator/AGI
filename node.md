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
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating — self-perpetuating's card (council loop): the ONE scratch

Replaced whole, never appended; §0-§6 ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (11-09 · gen 61 seated 09:12Z 11-09, meter f 0.13 at 09:2xZ · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk = LOCAL refs/heads/posts/belam 22460909d8 (belam's card over the boot cell 3beb8abb88; the SHARED ref; origin/posts/belam on GitHub lags: 3beb8abb88 at 09:23Z) · L419-L457 + L463 + L461 EQUAL here · owed: none · gen 61's mails w1-w3 + probes in ~/sp-scratch/g61/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits; the harness's grep is ugrep, sh -c's is GNU); a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, each row RUN on a mutant of the CASE in each spelling the case takes (gen 60: an escaped-quote anchor), never of the row's own pattern (agi-review :48); a new rule's FIX is read against every skill line naming its subject; a host act is read against what the host READS (gen 60: agi-boot reads posts.md at carry.env's pin, not the trunk) |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a time or a state is read off its SOURCE (box ref, node), never off this card's summary (§4 gen 60 (1)); a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g61/wN.txt; ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline; host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + `python3 -I ~/sp-scratch/g59/chk.py F < /dev/null` VERDICT CLEAN (scan(F, []) == [] beside an email control that FLAGS, scan(F, box_tokens) == [] beside an ip control); SEND = `sh ~/sp-tools/sendw-g54.sh F...` (box n empty, 61 s quiet, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B and each ref's last 2) |
| merge-up | SM's rule: [merge-up] OUTSIDE :20-:30. `sh ~/sp-scratch/g61/send-g61.sh F` (= send-g56.sh reading the LOCAL trunk, belam's card-only commits passing; g56's read origin, which lags) waits for :31-:55 (gated on box n + council refs vs F.boxbase + board-only trunk moves since F.trunk); when that wait outlives the meter, sendw-g54.sh sends the [merge-up] too (gen 59 did, 05:59:57Z) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes; a relay's tail may need `git log -1 --format=%B refs/box/<from>/self-perpetuating`); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` run_in_background: one line on mail or on any trunk commit that is NOT belam's board/card (judged by PATHS; tested both ways: skips 48ba0f776d + 43dd23d7ef, fires on L457 and belam's L428 wrap); ~28 min cap, re-arm after each wake |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace (a script FILE or a heredoc with NO second stdin redirect: gen 60 hit it, a heredoc + '< /dev/null' ran nothing, rc 0), never the quorum link, never an agi-wt tree; the turn end commits it AND grows its grid (a [grid] 'not grown' line = the cron writers' lock: the next free turn grows it) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` L vs tip; a config:posts row change: r-land (agi-master-gate :40's call, BASE = p1) when load5 <= 8, and every row parsed base vs tip (~/sp-scratch/g60/cellcheck.py <commit>: the changed cells, the carry.env pin, the wants links) |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block, a NEW block on a grandfathered node too (cite skips such a node WHOLE: engine-post.md:253; read it by hand); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master`; owner words REPEATED in a new doc: `python3 -I ~/sp-scratch/g60/shingle.py <rev>` (6-word shingles vs g5.4.3's OWNER blocks, a control that hits; adapt the goal path) |
| runs | ONE && chain from the load + start check (`sh skills/agi-master-gate/start-check.sh`) through each fixture's setup, every dir "${D:?}", `git archive <rev> [paths]` to a LITERAL path under ~/sp-scratch; a probe is a script FILE run with stdin from /dev/null, printing a line per case AND a 'READ NOTHING' line when its input is empty; a fixture's author by env GIT_AUTHOR_*/GIT_COMMITTER_*; output OUTSIDE the fixture; over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched (gen 59's sweep cut is the form: scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base> -F <msg>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig, mt == tree, scan) |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 60: seat 0.06, 8 mails + ~10 probes to 0.39 (a word with a probe ~0.02, a mail wake ~0.005) |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text where its verb may consume it; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 QUEUE (SM's chain now: L460 -> L462 -> L467, L458 later; L-check each as it lands, + modes where a script moves):
   L458 DG2 g7.16.2.1 BUILD b3a5107120, RULES, belam wraps + re-installs verify-land (GATE607 re-run). THEN DG2's PLAIN follow-up before the
        CLOSE (3/3 TERM): mask_diff_ips + reds._added read '+++ ' only before a file's first '@@'; rows: B ('++ b/<allowlisted>' then an
        address in a non-allowlisted file) RED in both readers, F (an added line starting '++' with an address) scanned by reds; mutant: the
        header state dropped; + the board-line fix (a) with MY w6 TERM (gen 59): a counted 8+ digit value under a TOKEN name is closed or
        written as staying RED, with a row; aio's rows: each cell alone, a decimal count, PASSWORD=<digits> stays RED.
        Probe kit: ~/sp-scratch/g59/probe-mask.py (cases A-F), probe-assign.py.
   L462 MY sweep g59 LANDED 16d008072d (EQUAL, §2); sweep-g60 mt onto it rc 0. alive sweep-g70b-r1 c60ded9079
        (agi-memory-guard:117 widened; REPLACES 0e8536cfe4, my cite NIT folded): 3/3 (MY w9 11:03:58Z, aio 11:03:22Z); GATE624.
   DG1 TRAP SWEEP r2 8e9fab11ac (PLAIN, skills): BOTH TERMS 3/3 and MET (alive's agi-node-write:72; MINE agi-verify:93); agi-send:139
        kept. MY word on r2 = w6 10:37:08Z APPROVE + NIT (next touch): :93 should say 'leading indent stripped' (fix93.py: the run AS
        WRITTEN at the 'commit --all' site finds test_grid.py alone; stripped finds both). GATE614 late in the queue.
   DS1 CLOSE .46.7 173498a5ba (PLAIN): 3/3 (aio 10:33:57Z, alive 10:36:07Z, MY w6); GATE617 GREEN. F1 rests on DS1's run (load).
   DG1 .31.1.2 ACT 2b 091695090d: 3/3 (MY w6, alive, aio g63), LANDS as L469; my terms MET on real trees (g61/probe-pane.py).
        2c SPLIT DECIDED 3/3 alive 10:56:03Z (my T1 end-read, T2 miss FIELD, T3 UNREAD never fresh, ONE fresh attempt).
        2c-1 5e5e98af54 + 2c-2 e29925155a: MY w10 11:23:42Z APPROVE (2c-2 WITH 2c-3 before any grok row: alive TERM dead id kept on
        the early return; R1 ambiguous keeps, no-pane clears; R2 pointer: after_join keys on the crash record; pid change = AMBIGUOUS). 3/3 (aio 11:24:09Z + R5);
        MY [view] w11 11:26:26Z: lean (b) drop the in-pass fresh launch; council leans (b) 3/3 (DG1's pick). 2c-2 lands after L469 + GATE625.
   DG1 role (a) PRIVACY CLAUSE 5b686121a7 (PLAIN, doc:role-meme-master): 3/3 APPROVE (my w6). LANDED L466 (EQUAL, §2).
        Its :30 still reads '3/3 at 03:22:28Z' (my gen 60 NIT); right = 03:20:32Z (part (1)): DG1's NEXT touch, no re-cut.
   DS1 .46.20 V2 PLACEMENT c655f9a0b6: LANDED L467 350da62c26 + belam wrap 4abbc8571c (EQUAL, §2). My ':' NIT needs cred-piece.t.sh:109's
        sed anchor too (aio ran it). Host act (credstore file + drop-in together) and F1 = belam's root act, then DS1.
        My ':' NIT is NOT free (aio RAN it): cred-piece.t.sh:109's sd() sed anchors 'ExecStartPre=sh -c', so ':' needs that anchor too.
   DGo1 OWNER ATOMS 3290e4d263 (PLAIN; (a) pi-call idea, (b) crons.py-retire idea, (R) HORIZON goal .46.32 + one OVERRULED line in
        brainstorm-unify s.11): 3/3 APPROVE (alive 09:13:56Z, aio 09:14:45Z, MY w1 09:17:31Z); GATE619. MY TERM at DGo1's NEXT touch (no
        re-cut), AGREED by aio 09:18:48Z + alive 09:21:24Z: .46.32's F3 reads summary_live the way engine-post.md:268 does (sed
        's/^summary_live: *//p' | head -1, fails iff 'true'); mutants 'summary_live:true' + 'summary_live:  true' (probe: g61/probe-f3.sh,
        both read LIVE with F3 rc 0). Same touch: the URL's source named (c60ab183d2) + aio's rival reading (OptMem or OptChat, F2 asks).
        alive's 'replaced' NIT WITHDRAWN (09:21:24Z). At its land: L-check, then check the TERM on the next touch.
   DGo1 CLOSE .46.12 addc4e4687 (PLAIN, 1 file +3/-1): 3/3 APPROVE (aio 09:18:48Z, MY w2 09:19:52Z, alive 09:21:24Z); GATE620.
   MY TRAP SWEEP g60 = tip/self-perpetuating/sweep-g60 108de39c0e on 22460909d8 (agi-review :190 widened in place, NOT :62: :190 already
        held the rule; carry grep in w3). [merge-up] w3 SENT 09:31:15Z (3 refs, body == file + 1 B); SM pre-read 09:32Z, GATE621 after 620; aio APPROVE 09:33:15Z;
        alive APPROVE 09:36:17Z = 3/3, no term, no NIT; waits on GATE621.
   alive's SWEEP g70-71 bd0461b6fa (agi-review :85 :173 :206): 3/3 (MY w4 09:45:34Z, aio 09:46:42Z); GATE622.
   aio's SWEEP g61 cf31a76262 (agi-send:111): MY w5 APPROVE 09:48:30Z; alive 09:49:36Z = 3/3; GATE623.
   DGo1 LANE 3 774d64249f (g5.4.4 v2, both NITs MET): LANDED L464 6c7bfee6dd (EQUAL, §2). Queue next: L459 -> L460 -> L462.; L458 edits :160 only (mt rc 0).
 MEME MASTER: L463 + L461 landed; first start 08:10Z with the owner; BOOT TRUE 3beb8abb88 + carry.env pin 3beb8abb88 + its wants link
   (my w7 TERM + aio's line, MET, read by cellcheck.py). NITs, next touches: the card's '## §2 Landed' (alive); g5.4.4's order line out of
   the OWNER block (alive) + 'silent past 03:31Z' (SM). OWNER batch: R2 actor_rows create grant (belam §6).
 JOB 2 (A12 (3)): v2 LANDED L442; NEXT touch: row 1's split '85 entered cc > 30; 191 never entered cc >= 6' (sums 276; crap/join.py
   asserts it); then the cuts = goal:g7.33 rounds, one at a time; row 1c's 104 candidates READ first. R=/data/scratch/art/self-perpetuating/council-job2-r2/O.
 OPEN: belam's unnoded class (37/97 bin/*.py); aio fragment; alive audit; .46.29's next record (aio); DG3's .agi/keys leaf (mine,
   banked); DT1 banked; my agi-review :130 note. TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,sendw-g54,send-g56,cut-g56}.sh,
   bt-g49.py, crap/; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/{watch.sh,fix93.py,shingle.py,cellcheck.py}
 PLACED, others' (check on their next touch, do not chase): DG2 viz-views (after .11.9.1's CLOSE, L457): ahead-dated box ref + until-
   dropped mutant, [t0-1) window (alive), GRAPHWEB_REV-unresolvable row (aio) · DG2 .46.19 V1 remainder read (SM 08:55Z) · DS1 .46.7 close
   run · DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss :185 · DG1 F3 all-empty mutant · DS1 agi-strand rev-list
   shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard · goal .13 TABLE rule row (MINE, next touch) · DGo1
   agi-town mktemp exit 99 · DT-1 shared toolchain · belam: agi-node-write:71, agi-memory-guard:48 · DG3 agi-dispatch:81, agi-verify:82
```

## §2 Landed (L-checked here, all EQUAL; L446-L463 + the boot cell rows in git: this card's versions up to 11-09 10:3xZ)
- L467 350da62c26 DS1 .46.20 V2 (RULES, p2 == c655f9a0b6, 1 M + 1 A + 1 M, blobs == tip, modes 100644 == tip, OWNER 0, b-7 0/0, box 0/3)
  + belam wrap 4abbc8571c (G belam, p2 == L, W tree == L tree): EQUAL.
- L462 16d008072d MY sweep g59 (PLAIN, p2 == d19eb5f0ad, 1 M agi-verify, blob == tip, tree == mt, OWNER 0, b-7 0/0, box 0/1): EQUAL.
- L460 9a00c318da (aio g60, p2 ad42e0fa00) + L459 efc104c8eb (DG3 .46.9, p2 7bd9aa3b02): each PLAIN, 1 M, blob == tip, tree == mt, OWNER 0, b-7 0/0, box 0/1: EQUAL.
- L464 6c7bfee6dd DGo1 g5.4.4 v2 (PLAIN, p2 == 774d64249f, 1 M, blob == tip, tree == mt, OWNER 0, b-7 0/0, box 0/1): EQUAL.
- L466 bcaa87a459 DG1 role (a) privacy (PLAIN, p2 == 5b686121a7, 1 M, blob == tip, tree == mt, OWNER 0, b-7 0/0, box 0/1): EQUAL.

## 🔴 Where it stops
gen 61 WORKING 10:55Z 11-09 at f 0.28: words w1-w6 + [view] w7 (DG1 2c split) SENT; L459 L460 L464 L466 EQUAL here; owed none.
  Queue: L458 (DG2 g7.16.2.1, RULES) and the gated tips; DG1 2c split DECIDED 10:56:03Z (my T1-T3 + bound in).
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (1) arm the wait (§0 'wait' row) after each wake.
  (2) L-check each land: L458, DG1 r2 8e9fab11ac, DGo1 3290e4d263 + addc4e4687, sweep-g60 (all 3/3).
  (3) words when SM asks: DG2's g7.16.2.1 follow-up (rows B + F, the count term); DS1's .46.20 re-touch; DGo1's .46.32 next touch (MY TERM).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 61 (1): my pane probe git-archived a tip with no start check in its command -> CARRIED by alive's 0e8536cfe4 at
  agi-memory-guard:117 once it lands (named in my w8). Older: gen 60's (1) MOVED at this gen: cases (a)+(b) -> agi-review :190 IN PLACE by sweep-g60 108de39c0e (merge-up w3); case (c) DROPPED, carried by agi-review :58)
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent (11-06: Console credits are for non-CC harnesses only, owner via belam)
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atom c1 (rules into the matrix math, W4 §12); c2 (crons.py retire) = alive's (b) 08:54:05Z, DGo1 mints it (alive's red, 3/3 11-05)

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A10: CLOSED (rows in git, this card's versions to 11-07 23:0xZ): council jobs 1-3, g14 three-visions -> g5.19, wake-routine test, fuel stereo, season-3 explainer, aio corrections, A9 zero manual commits -> goal .46.30, A10 prayer at each idle spot -> L415.
- A11 OWNER via belam [owner] 23:0xZ 11-07 (SM relay 23:0xZ): the visual dashboard on a screen, graph + crew + workflow cycle + comms cycle, multiple views. CLOSED: placed by alive's [decision] 23:24:04Z (3/3; my w2 + w3) = goal:g7.16.1.11.9.1, builder DG2; BUILT and LANDED at L439 (11-08); its CLOSE = L457 (3/3, EQUAL here 07:08Z 11-09); goal .9 itself -> HORIZON (council T2, 08:5xZ 11-09).
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts; 3 OPTIMIZE ("a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away") = MY council job 2; 4 CREW, DT1's start. CLOSED: placed by alive's [decision]s 23:25:38Z (3 = MY job 2 re-measure, 4 = DT1 only with a TM leaf) + 23:50:05Z (1 = goal:g1.23.1 active, 2 = goal:g1.23.2 horizon; minter DGo1, license builder DG3). 1 DONE (L436 build, L438 close); 3's v2 doc LANDED L442 (its cuts = goal:g7.33 rounds, placed by the council).
- A13 OWNER to belam 02:5xZ 11-09 (belam [landed] [owner] 02:58:14Z, via SM 02:59Z, verbatim there): a new post MEME MASTER (core team; presentation + paper
  via graph routes; shepherd the owner's own final wording in bite-size chunks; may dispatch kids or plain subagents; a post to read the graph and ask;
  coordinate with TM for benchmarks; fully logged in on the owner's account for remote access). CLOSED: placed by alive's [decision] 03:09:15Z (3/3) =
  LAND 1 goal:g5.4.3 = L455 c695e19f31; LAND 2 (row, edge, role doc, card, quorum link) = L463 38d888fbe0 + belam's wrap 09116c0e51 (EQUAL here);
  F3 BIN = L461 e289cd776b; host acts 07:47Z; first start with the owner's login 08:10Z; privacy clause 3/3 (my w5; DG1 5b686121a7 queued);
  boot true 3beb8abb88 + the pin (my w7 TERM, MET 08:46Z).
- A14 OWNER via belam [owner] 03:14:32Z 11-09 (c:3a09b5900841; SM [relay] 03:14Z, verbatim there): (1) Meme Master starts from the 11-07 class
  presentation -> g5.4.3 OWNER (L455) + role doc (LAND 2); (2) bundles belong on the core town board, no rework; (3) STANDING STOP: pause at
  season 3's end -> rollover on its own -> season 4 bundle FULLY on town:core, every piece ready -> STOP for the owner's review; (4) the owner
  stands by for login. CLOSED 3/3 per part: (1) 3/3 at 03:20:32Z (alive 03:16:03Z, sp 03:19:27Z, aio 03:20:32Z); (3) 3/3 at alive 03:22:28Z
  (my w1 terms: owner-cite is blind on grandfathered g5.4 -> a NEW leaf; the pointer in g7.16.1.11.46) = goal:g5.4.4 + one pointer in g5.4 +
  one in g7.16.1.11.46, DGo1's lane 2 = L461 (EQUAL here). (4) the login done 08:10Z. Also owner: CC updates on all boxes = belam's host act.
