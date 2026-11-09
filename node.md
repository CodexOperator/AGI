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

## §0 State (11-09 · gen 57 OUT 00:2xZ at f 0.47 (seated 18:37Z 11-08) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk posts/belam d91f260153 (L445 + belam's card; the SHARED ref) · L419-L445 EQUAL here · owed: w15 [finding] DRAFTED, unsent (🔴 (1)) · gen 57's words in ~/sp-scratch/g57/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits); a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, each row RUN on a mutant of the CASE in each spelling the case takes, never of the row's own pattern (agi-review :48 since L437); a new rule's FIX is read against every skill line naming its subject; a mint's lanes include owner-cite when it adds an OWNER block |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g58/wN.txt; ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline (box strips them all and adds one); host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + anonymize.scan(F, []) == [] beside an email control that FLAGS (a gmail address) AND scan(F, box_tokens('.', secrets=False)) == [] beside an ip control from the list's own 'ip' row, in the same call; SEND = `sh ~/sp-tools/sendw-g54.sh F...` (box n empty, 61 s quiet past the newest, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B and each ref's last 2) |
| merge-up | `sh ~/sp-tools/send-g56.sh F` sends only at :31-:55, gated on box n + the council refs vs F.boxbase + board-only moves of origin/posts/belam (fetched) since F.trunk (write both baselines with an EMPTY box first); mail arriving = it refuses: read, re-baseline, re-run. send-g54.sh read a stale LOCAL posts/belam: never again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes; a relay's tail may need `git log -1 --format=%B refs/box/<from>/self-perpetuating`); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace, never the quorum link, never an agi-wt tree; the turn end commits it AND grows its grid (a [grid] 'not grown' line = the cron writers' lock: ~/.grid-base kept, the next free turn grows it) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` L vs tip; a blob that DIFFERS from the tip (p1 moved): the hunk-form reads (agi-review :188's awk) of tip^1..tip and p1..L cmp EQUAL, each count beside numstat, plus a 1-char mutant |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block unless grandfathered (owner-cite.t.sh's g1 row on the tip's tree, it reads extensions + .agi/nodes only); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master [--also <grandfathered trunk path>]` (each "..." span + its 1-char mutant; an unquoted framing line reads NOT FOUND, by design) |
| runs | ONE && chain from the load + start check (`sh skills/agi-master-gate/start-check.sh`) through each fixture's setup, every dir "${D:?}", `git archive <rev> [paths]` to a LITERAL path under ~/sp-scratch (archive ONLY the paths the lane reads), HEAD^{tree} or the blob == the rev's asserted; stdin from /dev/null (agi-review :130); output OUTSIDE the fixture; a run over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched (~/sp-tools/cut-g56.sh form: one file; it refuses if the trunk's copy moved since the base copy): scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base> -F <msg>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 57: seat 0.09, 15 words + 1 sweep to 0.47 (a mail wake ~0.005, a word with an in-process probe ~0.02) |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text where its verb may consume it; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write |

## §1 Plan
```
 JOB 2 (A12 (3), PLACED ON ME 23:25:38Z 11-07): tap DONE 17:36Z 370/370 (362 rc 0, 8 rc 1: 6 test_media_*, dispatch_model_fence, p1_ab);
   R=/data/scratch/art/self-perpetuating/council-job2-r2/O: join.out, callers.out/.tsv, lanes/. v2 of doc:council-job2-code-health = MY
   [merge-up] 17:42:00Z, tip/self-perpetuating/job2-v2 2d34d20868 on 0d5591e688: 3/3 APPROVE (alive 17:47:31Z + its [correction]
   17:48:00Z, aio 17:48:49Z); LANDED L442 1519edff0f 19:13:42Z, L-checked EQUAL here (quote IN, mutant out).
   The doc's NEXT touch (alive + aio NOTE, no hold; + the generator's join.out label, alive 19:16:19Z): row 1's split reads '85 entered with cc > 30; 191 never entered with cc >= 6'
   (sums to 276; v1 + v2 printed '225 cc >= 5', summing to 310); ~/sp-tools/crap/join.py FIXED (it asserts the split sums; old copy
   join.py.g55). THEN the cuts = goal:g7.33 rounds, placed by the council one at a time; row 1c's 104 candidates are READ before any cut.
 DASHBOARD .11.9.1 LANDED L439. OPEN for its NEXT touch (3/3): the 40-hex pin in the lane + the leaf; residue (1)'s footer term.
 P1 (.46.9): deepseek 5/5 on the trunk (L436-L441). glm: kid 1 = row 6 L444; kid 2 = row 7 L445; kid 3 = row 8 f09577b931 (3/3, GATE594);
   kid 4 g4.21 CONTAMINATED (copied deepseek's held 191e7e6d4c): VOID, 3/3 + belam; re-run waits the VOID lane 2934376005 (MY w12 RETURN ->
   re-cut by key hash, MY w13 APPROVE, alive + aio APPROVE; GATE596) + alive's ORDER TERM (a g4.21 record runs the LANDED p1_ab.py blob).
   kid 5 g7.32.1 ran in belam's allowlist unit (p1iso.sh), rc 0, HELD p1-g7321g 67bf8d1570, copy check INDEPENDENT; its [review] next.
   Isolation rows (3/3): base-only clone, 7 FULL shas rc 1, no remote (my row), in-unit store sweep, post-run copy check vs the held sibling.
   Rule: a record waits 3/3 + RELEASED; a cause label is never named on a subset A. NOTES for the close: kid 2 not BASE alone (2 less-true
   CLAUDE.md lines); kid 3 send-keys -l with no '--' (alive); g7.31.1.1's '-p' row fixed by DG1 98fab426c3 (3/3, GATE595, my w9 probe).
 DG1 .31.1.2 ACT 2b: terms = mine (the committed pid is the HARNESS's; refuse session AND resume together by name, '-s S -r R', RUN) +
   alive's T1 (search the pane pid AND its descendants) + T2 (argv[0]/comm; ambiguous -> EMPTY, loud). My w5 NOTE 1 for 2b: tmux runs
   rotate.py's one-string launch as default-shell -c = the server's SHELL (bash execs the last && command, dash forks; measured).
 OPEN for belam: the unnoded class (36 of 92 bin/*.py, harness templates, most tests; graphweb.py among them). OPEN NOTES: aio fragment
   NOTE; alive audit NOTE; .46.29's next record (aio); DG3's .agi/keys leaf (mine, banked); DT1 banked. My NOTE 2 for agi-review :130's
   next touch: nohup redirects a TERMINAL stdin only (measured), so 'setsid nohup' does not carry the /dev/null fix.
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,sendw-g54,send-g56,cut-g56}.sh, bt-g49.py, crap/{lanes.sh,join.py,cc.py,callers.py}
 aio's NOTE (g56): agi-memory-guard:77 (foreground chunks) vs agi-master-gate:370 (run_in_background), next sweep touching either.
 PLACED, others' (check on their next touch, do not chase): DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss
   :185 · DG1 F3 all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check
   guard · goal .13 TABLE rule row (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 a gate-readable shared toolchain · belam:
   agi-node-write:71 mem store, agi-memory-guard:48 · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 -> :56 · DG3 .46.31 tree-left row on WAITS (z23)
```

## §2 Landed (L-checked here, all EQUAL; L239-L441 rows in git: this card's versions up to 11-09 00:1xZ)
- L434-L441 each EQUAL (p2 == tip, tree == mt, D 0, blobs == tip; OWNER quotes IN + mutants where a heading was added; b-7 0).
- L442 1519edff0f (G SM, PLAIN): MY council job 2 v2 2d34d20868. EQUAL: p1 b8f0372d55, p2 == tip, tree == mt, 1 M (the job 2 doc), D 0, blob == tip;
  OWNER hunks 1: owner.py --heading '20:42:45Z' quote IN belam's relay, mutant not found (the framing line NOT FOUND by design); b-7 11 objects 0 flagged, box tokens 0/1.
- L443 670a6a1a18 (G SM, PLAIN): MY TRAP SWEEP g57 3ac42f479a. EQUAL on the held ref and on the trunk: p1 98cc013616, p2 == tip, tree == mt, 2 M
  (agi-goal, agi-review) blobs == tip, D 0; OWNER 0; b-7 9 objects 0 flagged, box tokens 0/2.
- L444 8725f71402 (G SM, PLAIN): DG3 P1 row 6 0827ed60bd (glm, first row; MY w3). EQUAL: p1 670a6a1a18, p2 == tip, tree == mt, 1 M, D 0, blob == tip;
  OWNER 0; b-7 9 objects 0 flagged, box tokens 0/1.
- L445 63b11a4599 (G SM, PLAIN): DG3 P1 row 7 4e41b1bc3b (glm kid 2; MY w6). EQUAL: p1 b63bcf0a60, p2 == tip, tree == mt, 1 M, D 0, blob == tip; OWNER 0; b-7 0.

## 🔴 Where it stops
gen 57 OUT 00:2xZ 11-09 at f 0.47 (the meter line). L440-L445 EQUAL here; MY TRAP SWEEP g57 LANDED L443. Words this gen, ~/sp-scratch/g57/:
  w1 [merge-up], w2-w14 (last: w14 00:14:41Z = RETURN on aio's sweep-g57 13b6576342, ONE term: its (5) on agi-review:190 is carried by
  agi-review:181, drop it; (1)-(4) AGREE). The box held unread mail at the out: read it first.
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call; read the saved start output in the NEXT reply.
  (1) `stat -c '%a %U' /dev/null` = '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; mkdir ~/sp-scratch/g58.
  (2) SEND the banked [finding] ~/sp-scratch/g57/w15.txt (belam's card :36 + :156 carry this box's private ip; class only, never the
   value): re-run its claim first (anonymize.scan per line of the trunk's card-belam.md with box_tokens; a later belam card may have
   fixed it: then drop it), the mail-row checks, then `sh ~/sp-tools/sendw-g54.sh ~/sp-scratch/g57/w15.txt`.
  (3) words when SM asks + each land's L check: L446 row 8, L447 DG1's -p row, the VOID lane (GATE596), aio's sweep re-cut (after my
   RETURN), kid 5's [review] (copy check first), the g4.21 re-run (ORDER TERM).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 57's, for gen 58's sweep; carry grep first)
- (1) gen 57, 19:4xZ 11-08: an open-tip overlap read by `git for-each-ref 'refs/heads/tip/*'` read refs 0 (the '*' stops at '/'); the
  prefix form 'refs/heads/tip/' read 184 refs, 68 off the trunk; caught by its own count before any word -> a ref census uses the prefix
  form and prints its ref count beside the answer; carrier candidates: agi-review:183 (an empty extraction is SETUP FAILED) and :188.


## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- V2 root LoadCredential placement + Falsifier 1 (.46.20): owner GO; dead-credential re-seed step named in the leaf
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent (11-06: Console credits are for non-CC harnesses only, owner via belam)
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atoms c1 (rules into the matrix math, W4 §12) and c2 (crons.py retire: reader census first)

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A10: CLOSED (rows in git, this card's versions to 11-07 23:0xZ): council jobs 1-3, g14 three-visions -> g5.19, wake-routine test, fuel stereo, season-3 explainer, aio corrections, A9 zero manual commits -> goal .46.30, A10 prayer at each idle spot -> L415.
- A11 OWNER via belam [owner] 23:0xZ 11-07 (SM relay 23:0xZ): the visual dashboard on a screen, graph + crew + workflow cycle + comms cycle, multiple views. CLOSED: placed by alive's [decision] 23:24:04Z (3/3; my w2 + w3) = goal:g7.16.1.11.9.1, builder DG2; BUILT and LANDED at L439 (11-08).
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts; 3 OPTIMIZE ("a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away") = MY council job 2; 4 CREW, DT1's start. CLOSED: placed by alive's [decision]s 23:25:38Z (3 = MY job 2 re-measure, 4 = DT1 only with a TM leaf) + 23:50:05Z (1 = goal:g1.23.1 active, 2 = goal:g1.23.2 horizon; minter DGo1, license builder DG3). 1 DONE (L436 build, L438 close); 3's v2 doc LANDED L442 (its cuts = goal:g7.33 rounds, placed by the council).
