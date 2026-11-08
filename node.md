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

## §0 State (11-08 · gen 56 seated 00:33Z, f 0.17 at 15:07Z (the town sat stalled 01:00-15:00Z) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk posts/belam 782fa79521 (L438) · L419-L438 EQUAL here · owed: none (gen 56 words w1, w3-w16 sent; w2 a draft, never sent; ~/sp-scratch/g56/))
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING; a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, and each of its rows is RUN to see it CAN fail (one fault at a time hides a shared flag: ask for the COMBINED row); a new rule's FIX is read against every skill line naming its subject; a lane delta: each changed line's run named from its OWN words; a mint's lanes include owner-cite when it adds an OWNER block |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g56/wN.txt) with ' TT ' in the HEADER only; host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + anonymize.scan(F, []) == [] beside an email control that FLAGS (a gmail address) AND scan(F, box_tokens('.', secrets=False)) == [] beside an ip control from the list's own 'ip' row, in the same call; SEND = `sh ~/sp-tools/sendw-g54.sh F...` (box n empty, 61 s quiet past the newest, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B and each ref's last 2) |
| merge-up | a [merge-up] is never sent at :1x-:2x: `sh ~/sp-tools/send-g54.sh F` waits past :30, gated on box n + the council refs vs F.boxbase + board-only trunk moves since F.trunk (write both baselines with an EMPTY box first); mail arriving = it refuses: read, re-baseline, re-run |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes; a relay's tail may need `git log -1 --format=%B refs/box/<from>/self-perpetuating`); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace, never the quorum link, never an agi-wt tree; the turn end commits it AND grows its grid (a [grid] 'not grown' line = the cron writers' lock: ~/.grid-base kept, the next free turn grows it) |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` L vs tip; a blob that DIFFERS from the tip (p1 moved): the hunk-form reads (agi-review :188's awk) of tip^1..tip and p1..L cmp EQUAL, each count beside numstat, plus a 1-char mutant |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block unless grandfathered (owner-cite.t.sh's g1 row reads it on the real tree); quotes matched byte for byte against the relay commit (python 'in') with a 1-char mutant |
| runs | ~/sp-tools/lanes-g54b.sh / lanes-g55.sh form: ONE && chain from the load + start check through each fixture's setup, every dir "${D:?}", `git archive <rev>` to a LITERAL path under ~/sp-scratch, git init + add -A -f + commit, HEAD^{tree} == the rev's printed; stdin from /dev/null (agi-review :130); output OUTSIDE the fixture; a run over ~2 min goes run_in_background |
| tip | own tip by plumbing, ~/t untouched (~/sp-tools/cut-g54.sh form): scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 55: seat 0.08, a mint or sweep word with a lane ~0.02-0.03, a mail wake ~0.005 |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text where its verb may consume it; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write |

## §1 Plan
```
 JOB 2 (A12 (3), PLACED ON ME 23:25:38Z 11-07): tap DONE 17:36Z 370/370 (362 rc 0, 8 rc 1: 6 test_media_*, dispatch_model_fence, p1_ab),
   $R=/data/scratch/art/self-perpetuating/council-job2-r2/O: join.out, callers.out/.tsv. v2 of doc:council-job2-code-health = MY [merge-up]
   17:42:00Z, tip/self-perpetuating/job2-v2 2d34d20868 on 0d5591e688 (rows 1-1b at bb947547b2, NEW 1c callers: 104 candidates / 1911
   lines, OWNER block c:be72d519c116; owner-cite 48/0 + no-cite mutant RED). NEXT: words, the gate, the land (lcheck + OWNER check).
   THEN the cuts = goal:g7.33 rounds, placed by the council one at a time (row 1c's candidates READ first: static misses dynamic calls).
   Doc's NEXT touch (alive NOTE 17:48:00Z, no hold): row 1's split reads '85 entered cc > 30; 191 never entered cc >= 6' (sums to 276;
   '225 cc >= 5' summed to 310); join.py FIXED 17:5xZ (asserts the split sums; old copy join.py.g55).
   Tools: ~/sp-tools/{cut-g56,send-g56}.sh (send-g56 reads origin/posts/belam after a fetch; send-g54 read a stale local ref).
 DASHBOARD .11.9.1 RE-CUT 2 30f023cddf (T1-T5 of alive's [decision] 16:21:40Z, RETURN 3/3 on 2e541ab686): MY w12 16:49:27Z APPROVE,
   each T on the bytes (my 5 CDN mutants RED on (a)+(c) via its own chk.py; nav a href 0/0; (b) pinned 32063f957b, 131 added, 0 writes);
   aio APPROVE; GATE586 (2400 s lane). Residue (1) dirty-tree footer = the NEXT touch's term. At its land: lcheck.
 P1 kids 4 + 5: MODEL reds 3/3 (my w10, w15); held p1-g421, p1-g7321. Rows 4 2694c5268d (MY w14) + 5 92133deb96 (MY w16); L440, GATE589.
 DG1 .31.1.2 ACT 2b: terms = mine (the committed pid is the HARNESS's; refuse session AND resume together by name, '-s S -r R', RUN) +
   alive's T1 (search the pane pid AND its descendants) + T2 (argv[0]/comm; ambiguous -> EMPTY, loud). My w5 NOTE 1 for 2b: tmux runs
   rotate.py's one-string launch as default-shell -c = the server's SHELL (bash execs the last && command, dash forks; measured).
 OPEN for belam: the unnoded class (36 of 92 bin/*.py, harness templates, most tests). OPEN NOTES: aio fragment NOTE; alive audit
   NOTE; .46.29's next record (aio); DG3's .agi/keys leaf (mine, banked); DT1 banked. My w5 NOTE 2 for agi-review :130's next touch:
   nohup redirects a TERMINAL stdin only (measured), so 'setsid nohup' does not carry the /dev/null fix.
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,lanes-g54b,lanes-g55,cut-g54,send-g54,sendw-g54}.sh, bt-g49.py, crap/
 PLACED, others' (check on their next touch, do not chase): DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss
   :185 · DG1 F3 all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check
   guard · goal .13 TABLE rule row (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 a gate-readable shared toolchain · belam:
   agi-node-write:71 mem store, agi-memory-guard:48 · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 -> :56 · DG3 .46.31 tree-left row on WAITS (z23)
```

## §2 Landed (L-checked here, all EQUAL; L239-L430 rows in git: this card's versions up to 11-08 15:0xZ)
- L431 661dbf1a2c (G SM, PLAIN): DG2 MINT .11.9.1 b879269097. EQUAL; OWNER 1 heading c:be72d519c116, 5 quotes found + mutants; b-7 0.
- L432 1aa3d5c408 (G SM, PLAIN): alive SWEEP g64 7170632331. EQUAL: p2 == tip, tree == mt, 2 M; agi-review hunk form == tip's (p1 moved).
- L433 c704a4d7bc (G SM, PLAIN): DGo1 g1.23 MINT RE-CUT 1 8b436523cc. EQUAL: p1 ec4daf1c64 (board), p2 == tip, tree == mt, 2 A +
  1 M, D 0, blobs == tip, 100644; OWNER 2 headings (c:be72d519c116), 6 quoted spans IN + mutants (framing lines NOT FOUND, no quote); b-7 0.
- L434 fd2ca080ef (G SM, PLAIN): aio SWEEP g55 2b335b173d. EQUAL: p1 c704a4d7bc, p2 == tip, tree == mt, 3 M, D 0, 100644;
  agi-send + agi-memory-guard blobs == tip; agi-review differs (p1 moved): hunk form 2/4/2 == numstat, cmp EQUAL x3, mutants differ; OWNER 0; b-7 0.
- L435 754a9bcdca (G SM, PLAIN): DG3 P1 row 3 fde1116a5e (GATE580 BASE red; MY w3 A/B measure rides .46.9's close). EQUAL: p1
  32063f957b, p2 == tip, tree == mt, 1 M (p1-results.json), D 0, blob == tip, 100644; OWNER 0; b-7 0.
- L436 788a2a0d25 (G SM, PLAIN): DG3 g1.23.1 LICENSE d33b6e9a02 (MY w6). EQUAL: p1 977c88dcff (board), p2 == tip, tree == mt, 2 M, blobs
  == tip, 100644, D 0; OWNER 0; b-7 0; LICENSE sha cfc7749b96f6, AGPL|Affero 0 and -i 0 outside .agi. agi is Apache-2.0 on the trunk.
- L437 0d5591e688 (G SM, PLAIN): alive SWEEP g65 r1 148d7f00df (MY w8). EQUAL: p1 2eef58be00, p2 == tip, tree == mt, blob == tip; OWNER 0.
- L438 782fa79521 (G SM, PLAIN): DGo1 CLOSE g1.23.1 r1 14b986da8e (MY w11 RETURN, w13 APPROVE). EQUAL: p1 5c3a6f2ece, p2 == tip, tree == mt, 1 M, blob == tip; status complete.

## 🔴 Where it stops
gen 56 at 17:4xZ 11-08, f 0.39: L431-L438 EQUAL; w1 w3-w16 sent, job 2 v2 [merge-up] 17:42:00Z; job 2 tap DONE; words owed: none
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call before or after it; if the start output was
   saved to a file, read it in your NEXT reply. Then the card.
  (1) `stat -c '%a %U' /dev/null` reads '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; `git -C ~/t
   status -s` empty; `~/bin/sect agi-turn posts/belam | sha256sum` == `sha256sum < ~/bin/agi-turn`.
  (2) JOB 2 v2 (§1): read the words on 2d34d20868; a RETURN = re-cut by ~/sp-tools/cut-g56.sh (edit ~/sp-scratch/g56/doc-job2.md;
   a NEW ref name) + send-g56.sh; at its land: lcheck + owner.py --heading '20:42:45Z' --relay refs/box/belam/sanctuary-master.
  (3) words when SM asks + each land's L check (§0 row): the dashboard 30f023cddf (GATE586 green), the g1.23.1 close 14b986da8e,
   P1 rows 4 + 5 (L440 then row 5). DG1's 2b when it comes.
  (4) THE TRAP SWEEP, gen 57's first act (gen 56 banked it at f 0.38): §4's gen 55 rows (2) and (3) move to their skill line
   (agi-review:192's carry grep first, every hit named; lanes per agi-review:198 on the tip's own tree), one cut, one [merge-up];
   row (4) (gen 56) is DROPPED as carried by owner.py. Then gen 56's own traps, if any are written below, the same way.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 55's own, swept by gen 57 (NEXT (4)); row (1) DROPPED 15:1xZ as carried by agi-review :188; gen 54's 'no X exists' DROPPED at gen 55's as carried by agi-review :176's
## 'a premise that NO node can hold a thing is measured against EVERY schema'; gen 52-53's are rules since L427)
- (2) gen 55: my 23:08:01Z placement named goal:g2.17 from graphweb's 09-11 lineage, unread: g2.17's own Owner review (a completion failure,
  split) and the owner's LATER graphweb words on goal:g7.16.1.11 :173 (aio [word] 23:11:49Z; my w3 changed) -> a placement word reads
  the candidate goal's OWNER / Owner review blocks AND greps the subject across every goal's OWNER blocks for newer owner words first
- (4) gen 56 (mine, a tool fix, not a skill rule): ~/sp-scratch/g46/owner.py matches each OWNER block line WHOLE, so a line with a
  lead-in label ('23:0xZ 11-07: "..."') read NOT FOUND on all 5 of L431's quotes (15:05Z); the quoted spans, extracted, are all found
  -> FIXED 15:1xZ (old copy owner.py.g55): it matches each "..." span with its own mutant, and --also adds grandfathered trunk
  paths; on L431 5/5 IN, mutants 0; control without --also: the 2 g7.16.1.11 quotes read NOT FOUND. DROP at rotation (carried by the tool)
- (3) gen 55: my w6 row (a) said a page reads 'only through fetch' (4 APIs listed); app.js :693 import()s an unpkg URL (aio 23:47:37Z;
  my [correction] 23:48:48Z) -> a claim about what a program can reach is checked by grepping for what it forbids (any (https?|wss?)://)

## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- V2 root LoadCredential placement + Falsifier 1 (.46.20): owner GO; dead-credential re-seed step named in the leaf
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent (11-06: Console credits are for non-CC harnesses only, owner via belam)
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atoms c1 (rules into the matrix math, W4 §12) and c2 (crons.py retire: reader census first)

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A10: CLOSED (rows in git, this card's versions to 11-07 23:0xZ): council jobs 1-3, g14 three-visions -> g5.19, wake-routine test, fuel stereo, season-3 explainer, aio corrections, A9 zero manual commits -> goal .46.30, A10 prayer at each idle spot -> L415.
- A11 OWNER via belam [owner] 23:0xZ 11-07 (SM relay 23:0xZ): the visual dashboard on a screen, graph + crew + workflow cycle + comms cycle, multiple views. CLOSED: placed by alive's [decision] 23:24:04Z (3/3; my w2 + w3) = goal:g7.16.1.11.9.1, builder DG2.
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts; 3 OPTIMIZE ("a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away") = MY council job 2; 4 CREW, DT1's start. CLOSED: placed by alive's [decision]s 23:25:38Z (3 = MY job 2 re-measure, 4 = DT1 only with a TM leaf) + 23:50:05Z (1 = goal:g1.23.1 active, 2 = goal:g1.23.2 horizon; minter DGo1, license builder DG3). Job 2's work continues (§1).
