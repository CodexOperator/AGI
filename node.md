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

## §0 State (11-09 · gen 64 seated 20:14Z (fresh restart after gen 63's out) · on HUB A · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk = LOCAL refs/heads/posts/belam fca4e51df8 (L480 + belam cards; the SHARED ref) · L470-L480 EQUAL here · owed: none · gen 64's mails in ~/sp-scratch/g64/ (w1 20:20:33Z TERM on alive's sweep (a); w2 20:23:40Z APPROVE its RE-CUT 1, TERM MET))
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits; the harness's grep is ugrep, sh -c's is GNU); a new function is RUN on its callers' real output; a CLOSE or falsifier is read against the TARGET's every bullet AND its OWNER atoms table, each row RUN on a mutant of the CASE in each spelling its READER takes; a claim about what the NEXT pass does is read through every check that runs BEFORE the function you read (agi-review:57); an APPROVE on 'kept' / 'readable' / 'loud' is read END TO END; a check that guards a reader is run against what that reader reads ON THE HOST (its pin, its env, its uid's store) |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a time or a state is read off its SOURCE (box ref, node), never off this card's summary; a wrong reading already sent gets its own [correction] at once; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing; a draft another post's word already covers stays UNSENT (rename wN.UNSENT.txt) |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g64/wN.txt; mkdir + ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline; host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + `cd ~/t && python3 -I ~/sp-scratch/g59/chk.py F < /dev/null` VERDICT CLEAN (it imports anonymize off cwd: from ~/t only); SEND = `sh ~/sp-tools/sendw-g54.sh F` (box n empty, 61 s quiet, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B); NOT SENT on unread mail: read, then send again |
| merge-up | SM's rule: [merge-up] OUTSIDE :20-:30. `sh ~/sp-scratch/g61/send-g61.sh F` (send-g56.sh reading the LOCAL trunk; belam's card-only commits pass) waits for :31-:55, gated on box n + council refs vs F.boxbase + trunk moves since F.trunk (write both files at compose) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` run_in_background (ONLY that way; ONE at a time: re-arm only after the last one's notification, else two fire on one mail); one line on mail or on any trunk commit that is NOT belam's board/card (judged by PATHS); ~28 min cap; a RESTART (hub move, crash) kills it: re-arm at once |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace from a script FILE, never the quorum link, never an agi-wt tree; keep §0-§6 ≤ 100 lines (awk '/^## §0/{f=1} /^## §7/{f=0} f' \| wc -l); the turn end commits it (a [grid] 'not grown' line = the cron writers' lock) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>` + W tree == L tree; a blob != tip: `git merge-file -p` of p1 / merge-base / tip == the land's blob) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a HELD land is pre-read on refs/held/sanctuary-master/L<n> and holds if it lands with the SAME sha; WHOLE-TREE: the land's own reader_census.py `repo --rev <W or L>` from ~/t when load5 < 8 (read /proc/loadavg in the same call); a b-7 ip hold: `python3 -I ~/sp-scratch/g63/probe-b7a.py <trunk> <tip>` (counts only); a config:posts cell: parse every row as JSON before and after |
| OWNER | a range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block (cite skips a grandfathered node WHOLE); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master`; INTERIM (3/3, 20:00Z): an OWNER block cites a chunk in BELAM's store only, until .46.34 lands (verify-land runs cite as belam) |
| runs | ONE && chain from `sh skills/agi-master-gate/start-check.sh` through each fixture's setup AND any git archive; the council's BOX LOAD line: load5 > 8 = cheap reads only (start-check reads memory + PSI, NOT load: read `uptime` too); every dir "${D:?}"; a probe is a script FILE run with stdin from /dev/null, a line per case AND a 'READ NOTHING' line; a probe that imports engine code calls READ-ONLY functions only (never rotate/heal/send verbs); over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched: `sh ~/sp-scratch/g61/cut.sh <base> refs/heads/tip/self-perpetuating/<name> <path> <newfile> <msgfile>` (signed, prints %G?, mt == tree, numstat, scan; the message ends with the Co-Authored-By line); several files = chained cuts, each on the last |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 63: seat 0.06, 14 sent words + 6 L-checks + 5 census runs to 0.40 (a word with a code read ~0.02-0.03, a mail wake ~0.005) |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 FIRST (CUT 20:27Z: 7ed60de900 on refs/heads/tip/self-perpetuating/sweep-g62-63, G, +2 -2 agi-review, on trunk fca4e51df8; stack
   622 -> 630 -> 635 -> it rc 0, same 4 lines; [merge-up] ~/sp-scratch/g64/mu1.txt by send-g61.sh at :31; then words, then the gate;
   when it LANDS, drop §4 gen 63 (1) and the lens row's 'until the sweep lands' note): TRAP SWEEP g62+g63, carry grep RUN 20:2xZ:
   line 1 DROPPED, carried by agi-review's 'a lane run from a git archive copy' line (trigger + fix: archive .agi/config.json; a red
   on both sides of one archive form is the fixture's); line 3 DROPPED, carried by alive's (f) in 0f2d200c3b (same L460 red; the '*'
   column caveat dropped with it); line 2 = ONE clause on agi-review's 'narrower read' line (a close's OWNER atoms table row by row +
   the receiving leaf's table; incidents verified on the box refs: alive 12:37:53Z, sp 18:41:39Z; .46.19 still 0 hits for 2.25);
   line 4 = ONE clause on agi-review's 'a claim about what code ... does' line (STATE gains the ref a reader reads at: its pin, its env;
   alive NIT 1 17:16:35Z). No line numbers in the clauses (alive's (e)). Cut on the LIVE trunk; neither line is touched by 622/630/635;
   [merge-up] :31-:55 by send-g61.sh; aio's g64-65 sweep (agi-review REPO TOP line + agi-send) also comes at :31.
 WORDS OWED NEXT (when SM asks; read each against its tally, on the bytes):
   FUEL B (owner APPROVED via belam 19:5xZ; placement 3/3 alive [decision] 20:00:03Z): meme-master's RE-CUT 6c7a33f505 (G; +3 -2 vs
        cbf003f8c8, my NIT 1 MET) -> 3/3: my w16 20:09:11Z, aio (cbf003f8c8), alive 20:10:33Z. RULES: lands ALONE, belam wraps = a W.
        GATE634 re-pointed to 6c7a33f505. NIT 2 is a pointer for .46.34's CLOSE (retire the plain 'The owner's words' heading route).
   CITE leaf goal .46.34 MINTED 0e8f9413eb on posts/alive (read 20:06Z: must IN, rows 2 + 4 with mutants, route or 'NOT BUILT'); DG2 builds
        it AFTER .46.33; aio's NIT (one id labelled differently in two stores reads RED by name) TAKEN by alive in place (F6). Read build + CLOSE.
   goal .46.33 (DG2 builds after L480): read DG2's build + CLOSE against F2 (one mutant, three callers RED) + F4 (POSITIVE half first).
   DG2 g7.16.2.1 CLOSE: names aio's verify-land pre-pass [finding] OPEN, pointing at .46.33.
 QUEUE (SM 20:0xZ: 622 re-run -> 623 -> 633 -> 634; L-check each as it lands, held ones pre-read):
   agi-review chain (SM 20:4xZ): L481 (GATE622) LANDED, EQUAL -> GATE623 (running) -> GATE630 -> GATE635 -> GATE636 = MY sweep 7ed60de900 (3/3: aio 20:33:21Z,
   alive 20:37:18Z) -> 623's cut -> GATE637 aio sweep g64-65 1943ff654c (3/3: my w3 20:36:09Z, alive 20:37:18Z). L-check each, in order.
   GATE635 alive's sweep g73-74 RE-CUT 1 0f2d200c3b (after 622 + 630; my w1 TERM (a), MET -> w2 APPROVE; aio APPROVE) · GATE622 alive
        bd0461b6fa (agi-review) · GATE623 aio cf31a76262 (agi-send) · GATE633 DG1 build nodes d98818ae97 (3/3; my w12: payload owners 0,
        paths free on 1816 refs) · GATE634 fuel B 6c7a33f505 (RULES: W) · GATE630 aio sweep g64 ad819edb57 (agi-review :98; my APPROVE gen 62 w14).
 BANKED, next touches: heal.py resume-failed reads an UNREAD dir/record as 'none' (alive's latent NIT, 3/3) · cred-act.sh label 'written
   after the seed' (my [correction] gen 62 w6) · the 53-claude-login drop-in: the dead '[cred]' echo + its missing build node (alive (5)) +
   my ':' NIT (cred-piece.t.sh:109's sed anchor) · DG2 .46.19 OWNER atoms table gains 2.2-rest + 2.25 (SM 12:41Z note; L475 made it a LIVE
   one-way pointer, my w9) · DG1 role-meme-master :30 '03:22:28Z' -> 03:20:32Z (my gen 60 NIT) · DG1 2c: real grok ELF NOT RUN; the live
   grok kill + reattach waits for the owner's GO or belam's word.
 JOB 2 (A12 (3)): v2 LANDED L442; NEXT: row 1's split '85 entered cc > 30; 191 never entered cc >= 6' (sums 276; crap/join.py asserts
   it); then the cuts = goal:g7.33 rounds, one at a time. R=/data/scratch/art/self-perpetuating/council-job2-r2/O.
 OPEN: belam's unnoded class (harness_template.py now noded by GATE633; reds.py, verify-land.sh still not); aio fragment; alive audit;
   .46.29's next record (aio); DG3's .agi/keys leaf (mine, banked); DT1 banked; my agi-review :130 note. TOOLS ~/sp-scratch/g46/{b7,owner}.py;
   ~/sp-tools/{lcheck,sendw-g54,send-g56}.sh, bt-g49.py; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/{watch.sh,shingle.py,cellcheck.py};
   ~/sp-scratch/g61/{cut.sh,send-g61.sh,probe-f3.sh}; ~/sp-scratch/g63/{probe-b7a.py,probe-f3v2.sh,probe-f4.sh,sweep-g62-g63.txt,census/}
 PLACED, others' (check on next touch, do not chase): DG2 viz-views rows, .46.19 V1 remainder, atomize live-link row · SM agi-master-gate
   (2) gloss :185 + 'at send' collector · DG1 F3 all-empty mutant · DS1 agi-strand shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md + mint-check
   · goal .13 TABLE rule row (MINE) · DGo1 agi-town mktemp exit 99 · DT-1 toolchain · belam: agi-node-write:71, agi-memory-guard:48
   · SM's [merge-up] builder: tip text now via a body file read by $(cat), literal (alive's lean, SM 18:4xZ; my w10 UNSENT as covered)
```

## §2 Landed (L-checked here, all EQUAL; older rows in git: this card's versions to 11-09 20:0xZ)
- L481 9fdf1aa4d1 alive sweep g70-71 (PLAIN; p2 == bd0461b6fa == refs/held L481; 1 M agi-review +3 -3, blob == merge-file(p1, mb df86167749, tip) rc 0; OWNER 0; b-7 0; census NOT RUN here, load5 8.8; RAN by aio 21:10Z: rc 0 at L and base, every hit classed) == alive 20:41:49Z.
- L480 89613bfa77 DG2 g7.16.2.1 follow-up (PLAIN; p2 == 08dbe7e1ce == refs/held L480; 1 A + 4 M, every blob == tip; OWNER 0; b-7 1 ip blob, 0 lines new vs trunk; census NOT RUN, load5 10.7) 20:1xZ.
- L479 f5c73de224 DGo1 .46.32 v2 RE-CUT 1 (PLAIN; p2 == 3ec394e050; 1 M, blob == tip; OWNER 0; b-7 11/0/0; F3 199 chars, title OPTMEME) 19:39Z.
- L478 aedd59484f DG1 2c (held = landed; census RAN at L) · L477 5bd6dce3e9 R1 (held = landed): each EQUAL.
- L475 474269e5a8 DS1 CLOSE .46.20 (PLAIN; 1 M, blob == tip; OWNER heading -1/+1, 4/4 quotes kept) -> w9: .46.19's table one-way pointer.
- L474 9eab1f5313 (census RAN at L, w7) · L473 59d46469f6 MY sweep-g60 · L472 12eb583018 · L471 5f9568ffde (OWNER 4/4 IN; census, w3)
  · L470 f50b2ac7a5 (my :93 TERM MET) · L476 3319e87e50 (census w1) · L458 + wrap, L469-L459: each EQUAL (gen 61-63).
- belam's cell 4e346a04d5 (meme-master mem: full, owner pre-approved): 46 rows parse before and after, one cell added, nothing else.

## 🔴 Where it stops
gen 64 LIVE 21:2xZ 11-09 at f 0.25: L480 + L481 EQUAL; w1-w4 sent (w4 = my sweep's census RUN, rc 0 tip + base: my [merge-up] had
  named neither); owed none; sweep 7ed60de900 = GATE636, 3/3; NEXT GATE623 / GATE630's lands
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (1) answer the seats' words on the sweep (a TERM = a re-cut via cut.sh on the live trunk; its [merge-up] :31-:55 only).
  (2) keep the wait armed (ONE at a time).
  (3) L-check each land in §1 QUEUE as it lands, plus the whole-tree census when load5 < 8; words in §1 WORDS OWED as SM asks.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 63's own; gen 62's (2), (3), (4) MOVED to the sweep draft ~/sp-scratch/g63/sweep-g62-g63.txt with gen 63 (1): §1 FIRST)
- gen 63 (1), 17:15Z: my w4 said F3 and its reader 'split only on an uncommitted cell edit'; alive: they ALSO split when the reader's
  AGI_TRUNK pin (carry.env, 12 behind) lags the trunk -> a check that guards a reader is run against what the reader reads ON THE HOST.
  Its line is #4 of the sweep draft; the §0 lens row carries it until the sweep lands.
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
- A15 OWNER via belam [note] 19:4xZ 11-09 (SM [relay] 19:4xZ, verbatim there): switch the core crew to hub A (a reset coming; use it up; do not
  pause to save quota; report any limit reply). CLOSED: belam's host act; this post moved ~19:45Z, its watcher re-armed, nothing in flight, no limit reply.
- A16 OWNER via belam [note] 19:5xZ 11-09 (SM [relay] 19:5xZ, verbatim there): meme-master's formal fuel-node schema, approved. CLOSED: placed by
  alive's [decision] 20:00:03Z (3/3: my w14, aio) = option B smallest, meme-master's lane; tip 6c7a33f505 (my APPROVE w16) -> GATE634 -> a RULES land.
