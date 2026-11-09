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

## §0 State (11-09 · gen 60 seated 06:09Z 11-09 (f 0.06) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk = LOCAL refs/heads/posts/belam e289cd776b (L461; the SHARED ref; origin/posts/belam on GitHub can lag) · L419-L457 + L463 + L461 EQUAL here · owed: none · gen 59's mails w1-w10 + probes in ~/sp-scratch/g59/; gen 60's in ~/sp-scratch/g60/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits; the harness's grep is ugrep, sh -c's is GNU); a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, each row RUN on a mutant of the CASE in each spelling the case takes, never of the row's own pattern (agi-review :48); a new rule's FIX is read against every skill line naming its subject; a parser of a diff is read against an added line that LOOKS like a header ('++ b/...') |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g60/wN.txt; ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline; host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + `python3 -I ~/sp-scratch/g59/chk.py F < /dev/null` VERDICT CLEAN (scan(F, []) == [] beside an email control that FLAGS, scan(F, box_tokens) == [] beside an ip control); SEND = `sh ~/sp-tools/sendw-g54.sh F...` (box n empty, 61 s quiet, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B and each ref's last 2) |
| merge-up | SM's rule: [merge-up] OUTSIDE :20-:30. `sh ~/sp-tools/send-g56.sh F` waits for :31-:55 (gated on box n + council refs vs F.boxbase + board-only trunk moves since F.trunk); when that wait outlives the meter, sendw-g54.sh sends the [merge-up] too (gen 59 did, 05:59:57Z) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes; a relay's tail may need `git log -1 --format=%B refs/box/<from>/self-perpetuating`); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace (a script FILE or a heredoc with NO second stdin redirect), never the quorum link, never an agi-wt tree; the turn end commits it AND grows its grid (a [grid] 'not grown' line = the cron writers' lock: the next free turn grows it) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` L vs tip; a blob that DIFFERS from the tip (p1 moved): the hunk-form reads (agi-review :188's awk) of tip^1..tip and p1..L cmp EQUAL, each count beside numstat, plus a 1-char mutant |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block, a NEW block on a grandfathered node too (cite skips such a node WHOLE: engine-post.md:253; read it by hand); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master` (an unquoted framing line reads NOT FOUND by design; a quote spanning TWO lines reads NOT FOUND too: test it by a python substring against the relay message, ~/sp-scratch/g59/probe-owner44.py's form) |
| runs | ONE && chain from the load + start check (`sh skills/agi-master-gate/start-check.sh`) through each fixture's setup, every dir "${D:?}", `git archive <rev> [paths]` to a LITERAL path under ~/sp-scratch (bin + src when a module imports graph_core), the blob == the rev's asserted; a probe is a script FILE run with stdin from /dev/null, printing a line per case; a fixture's author by env GIT_AUTHOR_*/GIT_COMMITTER_*; output OUTSIDE the fixture; over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched (gen 59's sweep cut is the form: scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base> -F <msg>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig, mt == tree, scan) |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 59: seat 0.05, 10 mails + 8 probes to 0.40 (a word with an in-process probe ~0.02-0.03, a mail wake ~0.005) |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text where its verb may consume it; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 QUEUE (SM's chain, ORDER 06:25Z: L458 -> L459 -> L460 -> L462; L-check each as it lands, + modes where a script moves):
 MEME MASTER (L463 + L461 landed; my boot term MET; belam's HOST ACTS DONE 07:47Z): next the first start with the owner's login, then
   boot true. PRIVACY CLAUSE (my w5 07:52:55Z; aio 07:54:03Z + the quoted-text draft; alive TERM 07:55:36Z = 3/3: the 700 photo dir +
   file-history + cache 700 + stat read-back + the after-first-paste listing) = DG1's cut 5b686121a7 (PLAIN, role (a)), alive APPROVE
   08:05:20Z, MY w6 APPROVE 08:06:39Z. Host side done by belam (READ from my uid: 700 700, listing refused). On its land: lcheck.
   NITs for the next touches: role Starting point -> 3/3 at 03:20:32Z (MY w3 NIT gave 03:22:28Z: WRONG, corrected in w6; §4 gen 60 (1));
   the card's missing '## §2 Landed' (alive); g5.4.4's 'The order it sets' line out of the OWNER block (alive) + the 'silent past
   03:31Z' Why (SM). OWNER batch: R2 grant (belam §6).
 DG1 TRAP SWEEP 6fba776870 (PLAIN, skills): alive APPROVE + TERM agi-node-write:72 (per-command form too); MY w6 APPROVE + TERM agi-verify:93:
   its 'git grep -F <old line>' reads 0 on test_grid.py:2127's ESCAPED-quote anchor of today's commit --all line (measured) -> grep the
   old line's longest run with no quote/backslash; NIT agi-send:139 = a clause at agi-review:97 by :192 (DG1's pick). alive AGREE my TERM
   08:08:02Z (re-measured): the re-cut carries TWO terms; aio's word pending. On the re-cut: read both terms in the bytes + run the mutant.
   L458 DG2 g7.16.2.1 BUILD b3a5107120, RULES, belam wraps + re-installs verify-land. THEN DG2's PLAIN follow-up before the CLOSE (3/3 TERM):
        mask_diff_ips + reds._added read '+++ ' only before a file's first '@@'; rows: B ('++ b/<allowlisted>' then an address in a non-
        allowlisted file) RED in both readers, F (an added line starting '++' with an address) scanned by reds; mutant: the header state dropped;
        + the board-line fix (a) (reds' assignment rule, the TOKEN-named placeholder) with MY w6 TERM: a counted 8+ digit value under a TOKEN name
        is closed or written as staying RED, with a row; aio's rows: each cell alone, a decimal count, PASSWORD=<digits> stays RED.
        Probe kit: ~/sp-scratch/g59/probe-mask.py (cases A-F), probe-assign.py.
   L459 DG3 .46.9 RESULT 7bd9aa3b02 (3/3; figures recomputed EQUAL, ~/sp-scratch/g59/fig.py). The leaf stays ACTIVE until the credits arm.
   L460 aio sweep g60 ad42e0fa00 (agi-memory-guard :117, the git grep LOAD case; gen 59 trap (2) is NOT placed here: dropped, carried :66).
   L462 MY sweep g59 d19eb5f0ad (agi-verify :65, gen 58's trap (4)), GATE611 GREEN 07:24Z (re-run on cc1031b92b, 0 SKIP); alive 06:02:03Z + aio 06:02:37Z APPROVE; cuts after L460.
 JOB 2 (A12 (3)): v2 LANDED L442. Its NEXT touch: row 1's split '85 entered with cc > 30; 191 never entered with cc >= 6' (sums 276);
   ~/sp-tools/crap/join.py FIXED (asserts the split sums). THEN the cuts = goal:g7.33 rounds, placed by the council one at a time; row 1c's
   104 candidates READ before any cut. R=/data/scratch/art/self-perpetuating/council-job2-r2/O.
 DG1 .31.1.2 ACT 2b: terms = mine ('-s S -r R' refused together; the committed pid is the HARNESS's) + alive T1 (the pane pid AND its
   descendants) + T2 (argv[0]/comm; ambiguous -> EMPTY, loud); my NOTE: tmux runs the launch as default-shell -c (bash execs, dash forks).
 OPEN for belam: the unnoded class (37 of 97 bin/*.py). OPEN NOTES: aio fragment; alive audit; .46.29's next record (aio);
   DG3's .agi/keys leaf (mine, banked); DT1 banked; my agi-review :130 note (nohup redirects a TERMINAL stdin only).
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,sendw-g54,send-g56,cut-g56}.sh, bt-g49.py, crap/; ~/sp-scratch/g59/ (chk.py + probes)
 PLACED, others' (check on their next touch, do not chase): DG2 viz-views (after .11.9.1's CLOSE, L457): ahead-dated box ref + until-
   dropped mutant (my w4), [t0-1) window (alive), GRAPHWEB_REV-unresolvable row (aio) · DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss
   :185 · DG1 F3 all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard ·
   goal .13 TABLE rule row (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 shared toolchain · belam: agi-node-write:71,
   agi-memory-guard:48 · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 -> :56 · DG3 .46.31 tree-left row
```

## §2 Landed (L-checked here, all EQUAL; L446-L455 rows in git: this card's versions up to 11-09 07:4xZ)
- L461 e289cd776b DGo1 lane 2 (07:45Z; p1 belam card 374b77ae27; 3 M + 1 A goal nodes, OWNER +1 = g5.4.4's block, the blob == the tip read
  at gen 59 + aio): EQUAL (G SM, p2 == tip, tree == mt, blobs == tip, D 0, b-7 0, box tokens 0). F3 BIN at g5.4.3:61-62 = MY TERM MET.
- L463 38d888fbe0 DG1 MEME MASTER LAND 2 (RULES, 07:31Z; 2 M + 3 A, modes == tip incl. the 120000 link, OWNER 0) + belam's wrap 09116c0e51
  (G belam, parents [48ba0f776d, L], tree == L's): EQUAL. r-land RUN (load5 6.24): on L, R2 (DG1 create, no grant) + the lander line; on
  the wrap, R2 ALONE = SM's one table row (i). alive's GO (7) 07:38:26Z. My w4 (this reading) NOT SENT: SM's 07:38Z correction covered it.
- L457 4e506b2ad9 DG2 .11.9.1 CLOSE (07:08Z; p1 board bf0f1df259; 3 M, OWNER 0, modes L == tip): EQUAL (G SM, p2 == tip, tree == mt,
  blobs == tip, D 0, b-7 0 flagged, box tokens 0).
- L456 83819b254d aio sweep g59 (06:14Z; 1 M agi-review, OWNER 0): EQUAL (G SM, p2 == tip, tree == mt, blob == tip, D 0, b-7 0 flagged,
  box tokens 0); :174 carries gen 59 trap (1), dropped from §4.

## 🔴 Where it stops
gen 60 WORKING 08:0xZ 11-09 (seated 06:09Z, f 0.275 at 08:08Z): L419-L457 + L463 + L461 EQUAL here; 5 mails sent (g60/w1-w3, w5 07:52:55Z, w6 08:06:39Z; w4 held, covered):
  w1 06:18:00Z trap (2)'s home -> :66; w2 06:21:28Z trap (2) DROPPED, carried at agi-verify:66 (aio by agi-review:192; :66's awk fix RUN
  here); w3 06:24:16Z LAND 2 APPROVE + the boot term (SM took road A: L461 next). owed none. agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (1) wait: `sh ~/sp-scratch/g60/watch.sh < /dev/null` run_in_background (wakes on mail or any commit that is not belam's board/card,
      judged by PATHS; tested: skips 48ba0f776d + 43dd23d7ef, fires on L457 and belam's L428 wrap); box read on mail.
  (2) L-check L457, L463, L458-L462 as each lands (tips in §1): `sh ~/sp-tools/lcheck.sh <L> <tip>` + the OWNER count + b7.py + bt-g49.py.
  (3) words when SM asks: DG2's g7.16.2.1 follow-up (rows B + F, the count term); aio's word on my L462; SM's A/B pick on the boot term.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 60's own below; gen 59's two MOVED: (1) carried by agi-review :174 (L456), (2) DROPPED, carried by agi-verify :66 (aio + w2, agi-review :192); gen 58's (4) rides my sweep at agi-verify :65 = L462)
- gen 60 (1), 06:24Z 11-09: my w3 NIT gave doc:role-meme-master's Starting point the 3/3 time 03:22:28Z, read off my card's §7 A14
  row (which names the LAST part's close, part (3)), not off the box refs: part (1) closed at 03:20:32Z (aio); DG1 wrote my wrong time
  into the node (5b686121a7), alive caught it 08:05:20Z, my w6 corrected it -> a time cited in a word is read off the message ref in
  the same call (git log --format=%s on the box ref), per PART when a decision has parts. HOME at my out: agi-review:62 (its fix,
  'cite the one a command PRINTED', holds; its trigger names a line number or a count, not a time): one clause in place, by :192.
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- V2 root LoadCredential placement + Falsifier 1 (.46.20): owner GO; dead-credential re-seed step named in the leaf
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent (11-06: Console credits are for non-CC harnesses only, owner via belam)
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atoms c1 (rules into the matrix math, W4 §12) and c2 (crons.py retire: reader census first)

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A10: CLOSED (rows in git, this card's versions to 11-07 23:0xZ): council jobs 1-3, g14 three-visions -> g5.19, wake-routine test, fuel stereo, season-3 explainer, aio corrections, A9 zero manual commits -> goal .46.30, A10 prayer at each idle spot -> L415.
- A11 OWNER via belam [owner] 23:0xZ 11-07 (SM relay 23:0xZ): the visual dashboard on a screen, graph + crew + workflow cycle + comms cycle, multiple views. CLOSED: placed by alive's [decision] 23:24:04Z (3/3; my w2 + w3) = goal:g7.16.1.11.9.1, builder DG2; BUILT and LANDED at L439 (11-08); its CLOSE = L457 (3/3).
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts; 3 OPTIMIZE ("a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away") = MY council job 2; 4 CREW, DT1's start. CLOSED: placed by alive's [decision]s 23:25:38Z (3 = MY job 2 re-measure, 4 = DT1 only with a TM leaf) + 23:50:05Z (1 = goal:g1.23.1 active, 2 = goal:g1.23.2 horizon; minter DGo1, license builder DG3). 1 DONE (L436 build, L438 close); 3's v2 doc LANDED L442 (its cuts = goal:g7.33 rounds, placed by the council).
- A13 OWNER to belam 02:5xZ 11-09 (belam [landed] [owner] 02:58:14Z, via SM 02:59Z, verbatim there): a new post MEME MASTER (core team; presentation + paper
  via graph routes; shepherd the owner's own final wording in bite-size chunks; may dispatch kids or plain subagents; a post to read the graph and ask;
  coordinate with TM for benchmarks; fully logged in on the owner's account for remote access). CLOSED: placed by alive's [decision] 03:09:15Z (3/3) =
  LAND 1 goal:g5.4.3 ALONE (OWNER = belam's 02:58:14Z two paragraphs + 'Relay the login link' 03:05:08Z + the 11/7 line, WHOLE) = LANDED L455
  c695e19f31 (EQUAL here); its F3 = the BIN form + alive's two clauses (HEAD --branches, --diff-merges=remerge) in L461 (my w2 TERM + alive).
  LAND 2 PLACED ON DG1 (SM [place] 03:10Z) = ONE RULES cut ALONE: config:posts row meme-master (parent keep, NOT in keep's members/lands; director;
  tier 1; claude-code; claude-opus-5-5; effort medium; settings quiet; remote-control; town core; box encryption-town; template
  doc:unified-director-brief; owning_goal + roots the leaf; grow [idea, doc, task]; engine v4; seeds unified-director-brief, role-meme-master,
  unified-head, card-meme-master; worktree ''; identity empty; pubkey ''; recover false; boot FALSE) + rotations alerts edge meme-master ->
  sanctuary-master + doc:role-meme-master (a)-(f), naming the 11-07 presentation as its start + doc:card-meme-master (parent the leaf) + quorum
  link + a MEASURED matrix row (-> TM and -> SM ON; never belam). READ that cut against these bytes + SM's (i)-(iv) + aio's terms 1-3.
- A14 OWNER via belam [owner] 03:14:32Z 11-09 (c:3a09b5900841; SM [relay] 03:14Z, verbatim there): (1) Meme Master starts from the 11-07 class
  presentation -> g5.4.3 OWNER (L455) + role doc (LAND 2); (2) bundles belong on the core town board, no rework; (3) STANDING STOP: pause at
  season 3's end -> rollover on its own -> season 4 bundle FULLY on town:core, every piece ready -> STOP for the owner's review; (4) the owner
  stands by for login. CLOSED 3/3 (alive 03:22:28Z; my w1 terms: owner-cite is blind on grandfathered g5.4 -> a NEW leaf; the pointer in
  g7.16.1.11.46) = goal:g5.4.4 + one pointer in g5.4 + one in g7.16.1.11.46, DGo1's lane 2 09a3d1d4b3 = L461 (my w10 APPROVE, terms MET).
  Also owner: CC updates on all boxes = belam's host act.
