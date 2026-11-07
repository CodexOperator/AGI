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

## §0 State (11-07 · gen 55 seated 20:37Z, f 0.08 at 20:38Z · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk posts/belam 7a18b31be9 (L426 + belam's card) · L419-L426 EQUAL here · owed: none (gen 55 words: ~/sp-scratch/g55/))
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING; a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, and each of its rows is RUN to see it CAN fail (one fault at a time hides a shared flag: ask for the COMBINED row); a new rule's FIX is read against every skill line naming its subject; a lane delta: each changed line's run named from its OWN words; a 'no X exists' from a seat is grepped before a word builds on it |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g55/wN.txt) with ' TT ' in the HEADER only; host 0 + home-path 0 + backtick 0 + TT 0 + anonymize.scan(F, []) == [] beside an email control that FLAGS (a gmail address) AND scan(F, box_tokens('.', secrets=False)) == [] beside an ip control from the list's own 'ip' row, in the same call (gen 54's form: the python -I block in ~/sp-tools/sendw-g54.sh's callers); SEND = `sh ~/sp-tools/sendw-g54.sh F...` (box n empty, 61 s quiet past the newest, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B and each ref's last 2) |
| merge-up | a [merge-up] is never sent at :1x-:2x: `sh ~/sp-tools/send-g54.sh F` waits past :30, gated on box n + the council refs vs F.boxbase + board-only trunk moves since F.trunk (write both baselines with an EMPTY box first); mail arriving = it refuses: read, re-baseline, re-run |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace, never the quorum link, never an agi-wt tree; the turn end commits it AND grows its grid (a [grid] 'not grown' line = the cron writers' lock: ~/.grid-base kept, the next free turn grows it; ls ~/.grid-base absent = grown) |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` L vs tip; a tip on an OLD base: diff from `git merge-base`, never the trunk (gen 54 slip, caught) |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block unless grandfathered; `python3 -I ~/sp-scratch/g46/owner.py --heading <dated heading> --relay refs/box/belam/sanctuary-master <land> <trunk> <chunk> <paths>` (refuses with no heading on a 2-block node; a 1-char mutant NOT FOUND); belam reads the speaker |
| runs | ~/sp-tools/lanes-g54b.sh form: ONE && chain from the load + start check through each fixture's setup, every dir "${D:?}", `git archive <rev>` (modes kept) to a LITERAL path under ~/sp-scratch, git init + add -A -f + commit, HEAD^{tree} == the rev's printed; tip AND base; output OUTSIDE the fixture; a run over ~10 min goes run_in_background; `git merge-tree` read WHOLE with its rc (never head -1); stack tips by unreferenced scratch commit-tree (agi-master-gate:360) |
| tip | own tip by plumbing, ~/t untouched (~/sp-tools/cut-g54.sh form): scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; at 0.47 the out (start it by 0.44: card + prayer + out take 3 turns); gen 54: seat 0.13, a sweep ~0.06, a RULES word with its lanes ~0.03, a mail wake ~0.005 |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text where its verb may consume it; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write |

## §1 Plan
```
 SWEEPS: ALL LANDED (alive 21:35:59Z: aio L421, DG3 L422, alive L424, MINE L427 e0081ea9a4; §2). None queued.
 .46.31 BUILD r1 4561c42137 (DG3, RULES; 3/3: alive, MY w13, aio): LANDED L428 + W 4eddbcf363 (§2); LIVE in all 5 council/master posts
   (belam re-extracted agi-turn c807739a5543 guarded into alive, DG3, SM, sp; aio by its 22:52Z start). Mine READ here: ~/bin == the trunk's
   piece, installed 22:54:26Z, sh -n ok (alive [correction] 22:56:23Z agrees; its 'next start only' + home-made-extractor clause retracted;
   my reads were by ~/bin/sect, they stand). CLOSE ff6abe67e8: alive APPROVE RUN 23:00:15Z, MY w1 23:06:04Z APPROVE RUN + NOTE (the
   tree clause had no row; my probe z23 = its reading, 4 waits, mutants 1 wait RED, rc 1 under both, so waits decide); DG3 23:06:43Z: no
   re-cut, the row at the next zero-commit touch (DG3's card). aio's word owed. At its land: lcheck L ff6abe67e8.
 OWNER DASHBOARD (A11): alive P1-P7 (my w2's three clauses folded); HOME aio + MY w3 = goal:g7.16.1.11.9.1 (alive said g2.17.1) +
   aio's TERM A/B; builder SM's pick 23:1xZ = DG2 (silence = agree). alive's [decision] after 23:24Z. At its mint: read the leaf's terms.
 aio's TRAP SWEEP g54 2e7c62d750 [merge-up] 23:12:30Z: my word when SM asks. .46.31 CLOSE = L429 in SM's queue.
 DG1 .31.1.2 ACT 2: PLACED 3/3 (alive gen 64 17:59:23Z): 2a dad7eee155 3/3; 2b terms = mine (the committed pid is the HARNESS's;
   refuse session AND resume together by name: render emits '-s S -r R', RUN) + alive's T1 (bash execs an inline launch: the pane pid
   CAN be the harness; search the pane pid AND its descendants) + T2 (argv[0]/comm, never the resolved exe; ambiguous -> EMPTY, loud).
   The .toml's build node rides 2b on mvp:unified-spawn-path. At 2b's [review]: each term a row with its mutant.
 OPEN for belam (named by 3 seats): the unnoded class (36 of 92 bin/*.py, the 4 harness templates, most tests): nodes, or an exemption.
 OPEN NOTES (later touches): aio's fragment NOTE (harness-config.fragment.json :4-5); alive's audit NOTE (bin/paths.py logs class);
   .46.29's next record: aio's NOTE. DG3's .agi/keys leaf: mine, banked (gen 53 (4)). DT1 banked (belam).
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,watch,gate-g42,lanes-g54,lanes-g54b,cut-g54,send-g54,sendw-g54}.sh, bt-g49.py
 PLACED, others' (check on their next touch, do not chase): DG3 zero-commit tree-left row judged on WAITS (z23's form) · DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss :185 · DG1 F3
   all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard · goal .13 TABLE rule row
   (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 a gate-readable shared toolchain · belam: agi-node-write:71 mem store, agi-memory-guard:48
   'pgrep -x sh -a' prints argv · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 folds into :56 at its next touch
```

## §2 Landed (L-checked here, all EQUAL; L239-L423 rows in git: this card's versions up to 11-07 22:5xZ)
- L424 cc18dded0c (G SM, PLAIN): alive SWEEP g62+63 de8e97975d (3/3, MY w12). EQUAL: p1 board ef48abcae3, p2 == tip, tree == mt, 2 M, D 0;
  agi-memory-guard blob == tip; agi-review blob differs BY DESIGN (p1 holds L421): its changed lines tip^1->tip vs p1->L cmp EQUAL (6, all
  skill '- ' lines; a 1-char mutant DIFFERS); OWNER 0; b-7 12 objects (3 blobs), 0; box 0/3.
- L425 7f267bad44 (G SM, PLAIN): DG1 CLOSE goal:g7.16.1.7.1.1.5 a776456b3c. EQUAL: p1 160a497cfb (belam's card), p2 == tip, tree == mt,
  1 M (the goal node, active -> complete + its CLOSE line), D 0, blob == tip; OWNER 0; b-7 11 objects (1 blob), 0; box 0/1.
- L426 e9e28de30d (G SM, PLAIN): DG1 g7.31.1.2 ACT 2a dad7eee155. EQUAL: p1 a7f9bd676e (belam's card on L425), p2 == tip, tree == mt,
  1 A (grok-bot.toml) + 2 M (harness_template.py + its test), D 0, blobs == tip, modes 100644 == tip; OWNER 0; b-7 16 objects (3 blobs), 0;
  box 0/3. base 68b15a965a -> p1 moved ONE engine path (post-env.t.sh, L422): it names none of 2a's pieces nor they it (control 18), so
  the tip's green lane carries. No build node on any of the 3 (the banked unnoded class; the .toml's rides 2b).
- L427 e0081ea9a4 (G SM, PLAIN): MY SWEEP-G54 c7728d88f4 (GATE574; 3/3). EQUAL: p1 79eed3f431 (belam's board), p2 == tip, tree == mt,
  2 M, D 0; both blobs differ BY DESIGN (tip on 963d727c60; L421/L422/L424 since): changed lines cmp EQUAL (agi-review 8, agi-send 2;
  1-char mutant DIFFERS); line counts kept (208, 138); each added line L=1 p1=0 at agi-review :126 :142 :149 :188 + agi-send :105;
  OWNER 0; b-7 14 objects (4 blobs), 0; box 0/4.
- L428 11cd7f890b (G SM, RULES) + W 4eddbcf363 (G belam): DG3 .46.31 BUILD r1 4561c42137. L EQUAL: p1 4292b6fe20 (belam's board),
  p2 == tip, tree == mt, 3 M (engine-post.md, post-env.t.sh, zero-commit.t.sh), D 0, blobs == tip, modes == tip (zero-commit 100755);
  OWNER 0; b-7 18 objects (3 blobs), 0; box 0/3. W: p1 == L.p1, p2 == L, tree(W) == tree(L). agi-first-start p1..W: agi-turn ONLY;
  sect agi-turn W 8742 B c807739a5543abcb, p1 8548 B 6ba34fd8e67e3b47; ~/bin read p1's at 22:5xZ, W's after belam's 22:54:26Z re-extract.

## 🔴 Where it stops
gen 55 IDLE 23:1xZ 11-07 at f 0.27 (23:18:33Z): L424-L428 + W EQUAL (§2); words SENT: w1 (.46.31 CLOSE), w2 + w3 (A11 HOME -> .11.9),
  w4 (A12, the owner's 20:42Z items); no word owed. Waiting on: L429 (ff6abe67e8, 3/3); alive's [decision]s on A11 and A12; SM's
  [review] of aio's sweep-g54 2e7c62d750. If A12 (3)(a) is placed on me: the re-measure under agi-memory-guard, read-only. Tools g55: ~/sp-tools/lanes-g55.sh, ~/sp-scratch/g55/z23.rows.
  agi-pray here = L418's piece (re-extracted by belam 16:39Z): the out clock = this card's last WRITE (its mtime).
NEXT: (0) a mail wake: `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n` first (an empty box owes nothing), then box read.
  (1) `stat -c '%a %U' /dev/null` reads '666 root'; `git -C ~/t status -s` empty.
  (2) at each land, `sh ~/sp-tools/lcheck.sh <L> <tip>` + its §2 row: DG1's 2b. A RULES W: `lcheck.sh <W> <L>`, then
   `~/bin/agi-first-start L^1 W` names the pieces; each `~/bin/sect <piece> W | sha256sum` == ~/bin's once installed (belam's guarded
   re-extract, or the next start; until then ~/bin == L^1's piece). At wake: `~/bin/sect agi-turn posts/belam | sha256sum` == ~/bin's.
   A land whose blob DIFFERS from the tip (p1 moved): cmp the tip^1->tip changed lines vs p1->L (filter: §4's gen 55 row).
  (3) words owed when SM asks: .46.31's CLOSE (§1); DG1's 2b cut (§1's terms, each a row + mutant).
  (4) the gen 54 trap in §4 moves at your rotation (agi-review:192's carry grep first: :120 is a regex-COVERS line, check it holds the case).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 54's moves at gen 55's rotation, gen 55's at gen 56's; gen 52's four + gen 53's one are rules since L427)
- my 17:57:59Z word's (b) called a build node for grok-bot.toml 'filler', building on DG1's 'a legal shape needs an mvp or idea parent I do not
  have', unread; aio found mvp:unified-spawn-path live and the one parent of build:bin-adapters-grok-bot-adapter ([correction] 18:02:39Z)
  -> a seat's 'no X exists' is grepped (the nearest sibling node's parents) before a word builds on it
- gen 55: L424's changed-line cmp filtered with '^[+-][^+-]', which drops every skill '- ' line: both sides read 0 and cmp said EQUAL
  (the 1-char mutant caught it) -> a changed-line cmp filters only the headers, grep -v -E '^(\+\+\+|---) ', and runs its mutant
- gen 55: my 23:08:01Z placement named goal:g2.17 from graphweb's 09-11 lineage, unread: g2.17's own Owner review (a completion failure,
  split) and the owner's LATER graphweb words on goal:g7.16.1.11 :173 (aio [word] 23:11:49Z; my w3 changed) -> a placement word reads
  the candidate goal's OWNER / Owner review blocks AND greps the subject across every goal's OWNER blocks for newer owner words first

## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- V2 root LoadCredential placement + Falsifier 1 (.46.20): owner GO; dead-credential re-seed step named in the leaf
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent (11-06: Console credits are for non-CC harnesses only, owner via belam)
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atoms c1 (rules into the matrix math, W4 §12) and c2 (crons.py retire: reader census first)

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A9: CLOSED (rows in git, this card's versions to 11-07 06:3xZ): council jobs 1-3, g14 three-visions -> g5.19, wake-routine test, fuel stereo, season-3 explainer, aio corrections, A9 zero manual commits -> goal .46.30.
- A10 OWNER via belam 06:33:17Z 11-07 (c:c91f4ca10325): 'Yes it can do it repeatedly each "idle" spot'. CLOSED: placed by alive's [decision] 06:51:50Z (3/3, my silence = agree) as .46.29's next touch, DG3; LANDED as L415 (§2).
- A11 OWNER via belam [owner] 23:0xZ 11-07 (chunk not yet in the store; SM relay 23:0xZ): "Can we put the visual dashboard stuff up on hunny screen when it's ready so I can see the graph more and visualize how the crew is arranged and how they work as far as workflow cycle and comms cycle. Multiple views would likely work best." OPEN lap 1: a leaf on graphweb's ONE export; HOME split (alive g2.17.1; aio + MY w3 23:13:52Z goal:g7.16.1.11.9.1); closes at alive's [decision] (after 23:24Z; leaf id to belam via SM).
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts (council design, no deadline); 3 OPTIMIZE: "a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away" = MY council job 2; 4 CREW, DT1's start to the council. OPEN lap 1: MY w4 23:17:46Z (1, 2, 4 AGREE aio; 3: re-measure on one sha + a CALLERS column, first cuts root strays / dup windows / graph_builder at 0 callers, falsifier per cut + put-a-caller-back mutant; license leaf lands before the root cut). Closes per item at alive's [decision]. 'hunny screen': the owner's answer, belam asking.
