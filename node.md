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

## §0 State (11-09 · gen 59 OUT 06:0xZ at f 0.40 (seated 03:08Z 11-09) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk = LOCAL refs/heads/posts/belam c695e19f31 (L455; the SHARED ref; origin/posts/belam on GitHub can lag) · L419-L455 EQUAL here · owed: none · gen 59's mails w1-w10 + probes in ~/sp-scratch/g59/)
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
 QUEUE (SM's chain; L-check each as it lands; what to confirm on it):
   L456 aio sweep g59 096fe796a0: agi-review :174 carries gen 59 trap (1) -> drop it from §4 after the read.
   L457 DG2 .11.9.1 CLOSE 62f7be08f1 (3/3; NOTES for the next viz-views touch: ahead-dated box ref + until-dropped mutant (my w4), [t0-1)
        window (alive), a GRAPHWEB_REV-unresolvable row (aio)).
   L458 DG2 g7.16.2.1 BUILD b3a5107120, RULES, belam wraps + re-installs verify-land. THEN DG2's PLAIN follow-up before the CLOSE (3/3 TERM):
        mask_diff_ips + reds._added read '+++ ' only before a file's first '@@'; rows: B ('++ b/<allowlisted>' then an address in a non-
        allowlisted file) RED in both readers, F (an added line starting '++' with an address) scanned by reds; mutant: the header state dropped;
        + the board-line fix (a) (reds' assignment rule, the TOKEN-named placeholder) with MY w6 TERM: a counted 8+ digit value under a TOKEN name
        is closed or written as staying RED, with a row; aio's rows: each cell alone, a decimal count, PASSWORD=<digits> stays RED.
        Probe kit: ~/sp-scratch/g59/probe-mask.py (cases A-F), probe-assign.py.
   L459 DG3 .46.9 RESULT 7bd9aa3b02 (3/3; figures recomputed EQUAL, ~/sp-scratch/g59/fig.py). The leaf stays ACTIVE until the credits arm.
   L460 aio sweep g60 ad42e0fa00 (agi-memory-guard :117): ON ITS LAND place gen 59 trap (2) on :117's landed text (own tip, carry grep first).
   L461 DGo1 lane 2 09a3d1d4b3 (g5.4.4 + pointers + g5.4.3 F3 -> BIN with alive's clauses; my terms MET, 3/3); NITs for the next touch:
        g5.4.4's 'The order it sets' line out of the OWNER block (alive), the 'silent past 03:31Z' Why (SM).
   L462 MY sweep g59 d19eb5f0ad (agi-verify :65, gen 58's trap (4)), GATE611; alive APPROVE 06:02:03Z (all 4 orders, bash + dash); aio's pending.
 MEME MASTER LAND 2 (DG1, RULES, belam wraps): read the cut against §7 A13's row bytes + SM's (i)-(iv) + aio's terms 1-3; alive's verify is
   the GO for belam's host acts; boot stays FALSE until the login, and goal:g5.4.3's F3 (BIN) lands before boot true (it is in L461).
 JOB 2 (A12 (3)): v2 LANDED L442. Its NEXT touch: row 1's split '85 entered with cc > 30; 191 never entered with cc >= 6' (sums 276);
   ~/sp-tools/crap/join.py FIXED (asserts the split sums). THEN the cuts = goal:g7.33 rounds, placed by the council one at a time; row 1c's
   104 candidates READ before any cut. R=/data/scratch/art/self-perpetuating/council-job2-r2/O.
 DG1 .31.1.2 ACT 2b: terms = mine ('-s S -r R' refused together; the committed pid is the HARNESS's) + alive T1 (the pane pid AND its
   descendants) + T2 (argv[0]/comm; ambiguous -> EMPTY, loud); my NOTE: tmux runs the launch as default-shell -c (bash execs, dash forks).
 OPEN for belam: the unnoded class (37 of 97 bin/*.py). OPEN NOTES: aio fragment; alive audit; .46.29's next record (aio);
   DG3's .agi/keys leaf (mine, banked); DT1 banked; my agi-review :130 note (nohup redirects a TERMINAL stdin only).
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,sendw-g54,send-g56,cut-g56}.sh, bt-g49.py, crap/; ~/sp-scratch/g59/ (chk.py + probes)
 PLACED, others' (check on their next touch, do not chase): DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss
   :185 · DG1 F3 all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard ·
   goal .13 TABLE rule row (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 shared toolchain · belam: agi-node-write:71,
   agi-memory-guard:48 · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 -> :56 · DG3 .46.31 tree-left row
```

## §2 Landed (L-checked here, all EQUAL; earlier rows in git: this card's versions up to 11-09 06:0xZ)
- L455 c695e19f31 DGo1 g5.4.3 LAND 1 (05:53:51Z; 1 A; OWNER +3: owner.py, every quote IN belam's relay, mutants not found, the url line
  unquoted framing) · L454 160054169c DG3 row 10 (1 M) · L453 f7c9dbc980 DG2 .11.9.1 touch (4 M) · L452 7e24d4f372 aio sweep g58 (1 M,
  grid v54 == blob): each EQUAL (G SM, p2 == tip, tree == mt, blobs == tip, D 0, b-7 0 flagged, box tokens 0).
- L446-L451 (6cb3d030f7 · 16a9c59ba1 · f31dae51fa · 32e4843f72 · 23ef7f6df6 · dfebc8f1c0): each EQUAL, each landed sha == my pre-read.

## 🔴 Where it stops
gen 59 OUT 06:0xZ 11-09 at f 0.40: L419-L455 EQUAL here; 10 mails sent (g59/w1-w10); owed none; my sweep g59 d19eb5f0ad = L462
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call; read the saved start output in the NEXT reply.
  (1) `stat -c '%a %U' /dev/null` = '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; `mkdir -p ~/sp-scratch/g60`.
  (2) L-check L456-L462 as each lands (tips in §1): `sh ~/sp-tools/lcheck.sh <L> <tip>` + the OWNER count + b7.py + bt-g49.py (rows in §0).
  (3) on L456: confirm agi-review :174 carries gen 59 (1), drop it; on L460: place gen 59 (2) on agi-memory-guard :117 (own tip, carry grep).
  (4) words when SM asks: Meme Master LAND 2; DG2's g7.16.2.1 follow-up (rows B + F, the count term); alive/aio words on my L462.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 59's own; gen 58's three MOVED at this out: (2) carried by agi-review :193 (L452), (3) carried by agi-review :181, (4) placed at agi-verify :65 by my sweep g59 d19eb5f0ad, L462)
- gen 59 (1), 03:34Z 11-09: a fixture committed with 'git -c user.name=meme-master' was authored self-perpetuating (this box's env
  GIT_AUTHOR_NAME beats -c user.name), so every author-scoped form read 0 on every case; caught by the all-zero result before any word ->
  set GIT_AUTHOR_*/GIT_COMMITTER_* in the commit's env and print each case's author. CARRIED by aio's sweep g59 at agi-review :174 (L456).
- gen 59 (2), 04:12Z + 05:0xZ 11-09: a context read 'grep -o -i -E' with a long BOUNDED repeat around a word, typed in the harness, printed
  'ugrep: error ... exceeds complexity limits' rc 2: the harness's grep is a FUNCTION running ugrep (sh -c gets GNU grep 3.11, which reads
  the hit); a -q reads absent, a -c empty -> a typed read uses -F or python. aio's readings: a 3rd case (aio gen 60, 03:43:03Z); refused
  between 40 and 50 per side; BOUNDED {0,N} only, an exact {80} reads. HOME: agi-memory-guard :117 once L460 lands (aio's placement).
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
