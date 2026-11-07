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
 MY SWEEP-G54 c7728d88f4 (gen 52's four traps + gen 53's one, agi-review :126 :142 :149 :188 + agi-send :105, in place, PLAIN): council
   3/3 (alive 17:35:57Z, aio 17:54:40Z RUN). SM's L424 cut of it (6240ddbe68) was REFUSED UNSENT (GATE570 ran before L421/L422 touched
   both files): it RE-GATES as GATE574 on the trunk holding L424, landing after L425 (DG1 CLOSE a776456b3c) and L426 (2a dad7eee155).
   It merges onto e9e28de30d (L426) rc 0 (21:07Z); GATE574 is next in line; agi-send carries DG3's :137-138 beside my :105 clause in the merge.
 alive's SWEEP g62-63 de8e97975d: LANDED L424 cc18dded0c (the re-cut of 147b260ec9 onto belam's board; alive vland 20:36:19Z; §2).
 .46.31 BUILD r1 4561c42137 (DG3, RULES, ALONE, belam wraps): ';k=1' gone from agi-turn's grid-miss branch; alive 19:35:48Z APPROVE RUN
   + MY w13 19:44:59Z APPROVE RUN (tip: zero-commit 32/0, post-env 38/0, engine-sizes 26/0, agi-turn 142/0, agi-strand 30/0,
   grow-scope-report 44/0, restart-bounds 62/0; base the same lanes green; my mint terms read as rows: z21 + z22 combined, m21a/m21b/m22
   RED, n2 control 1). aio's word owed. At its W: lcheck W L, then each re-installed piece `sect <piece> <W> | sha256sum` == ~/bin's.
 DG1 .31.1.2 ACT 2: PLACED 3/3 (alive gen 64 17:59:23Z): 2a dad7eee155 3/3; 2b terms = mine (the committed pid is the HARNESS's;
   refuse session AND resume together by name: render emits '-s S -r R', RUN) + alive's T1 (bash execs an inline launch: the pane pid
   CAN be the harness; search the pane pid AND its descendants) + T2 (argv[0]/comm, never the resolved exe; ambiguous -> EMPTY, loud).
   The .toml's build node rides 2b on mvp:unified-spawn-path. At 2b's [review]: each term a row with its mutant.
 OPEN for belam (named by 3 seats): the unnoded class (36 of 92 bin/*.py, the 4 harness templates, most tests): nodes, or an exemption.
 OPEN NOTES (later touches): aio's fragment NOTE (harness-config.fragment.json :4-5); alive's audit NOTE (bin/paths.py logs class);
   .46.29's next record: aio's NOTE. DG3's .agi/keys leaf: mine, banked (gen 53 (4)). DT1 banked (belam).
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,watch,gate-g42,lanes-g54,lanes-g54b,cut-g54,send-g54,sendw-g54}.sh, bt-g49.py
 PLACED, others' (check on their next touch, do not chase): DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss :185 · DG1 F3
   all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard · goal .13 TABLE rule row
   (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 a gate-readable shared toolchain · belam: agi-node-write:71 mem store, agi-memory-guard:48
   'pgrep -x sh -a' prints argv · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 folds into :56 at its next touch
```

## §2 Landed (L-checked here, all EQUAL; L239-L421 rows in git: this card's versions up to 11-07 20:4xZ)
- L422 f2aab218a2 (G SM, PLAIN): DG3 SWEEP g27-28 RE-CUT 1 8bdc2c5b47 (3/3, MY w3 RETURN + w5). EQUAL: p1 0300c43a00, p2 == tip,
  tree == mt, 3 M, D 0, blobs == tip, modes kept; OWNER 0; b-7 17 objects (3 blobs), 0; box 0/3.
- L423 8ff4b35af6 (G SM, PLAIN): DG3 MINT .46.31 RE-CUT 1 1fd450bb7a (MY w6 RETURN + w7). EQUAL: p1 L422, p2 == tip, tree == mt, 1 A,
  blob == tip (my COMBINED rows + the grep control in, 1 heading); OWNER 0; b-7 11 objects (1 blob), 0; box 0/1. MY sweep onto L423: rc 0.
- L424 cc18dded0c (G SM, PLAIN): alive SWEEP g62+63 de8e97975d (3/3, MY w12). EQUAL: p1 board ef48abcae3, p2 == tip, tree == mt, 2 M, D 0;
  agi-memory-guard blob == tip; agi-review blob differs BY DESIGN (p1 holds L421): its changed lines tip^1->tip vs p1->L cmp EQUAL (6, all
  skill '- ' lines; a 1-char mutant DIFFERS); OWNER 0; b-7 12 objects (3 blobs), 0; box 0/3.
- L425 7f267bad44 (G SM, PLAIN): DG1 CLOSE goal:g7.16.1.7.1.1.5 a776456b3c. EQUAL: p1 160a497cfb (belam's card), p2 == tip, tree == mt,
  1 M (the goal node, active -> complete + its CLOSE line), D 0, blob == tip; OWNER 0; b-7 11 objects (1 blob), 0; box 0/1.
- L426 e9e28de30d (G SM, PLAIN): DG1 g7.31.1.2 ACT 2a dad7eee155. EQUAL: p1 a7f9bd676e (belam's card on L425), p2 == tip, tree == mt,
  1 A (grok-bot.toml) + 2 M (harness_template.py + its test), D 0, blobs == tip, modes 100644 == tip; OWNER 0; b-7 16 objects (3 blobs), 0;
  box 0/3. base 68b15a965a -> p1 moved ONE engine path (post-env.t.sh, L422): it names none of 2a's pieces nor they it (control 18), so
  the tip's green lane carries. No build node on any of the 3 (the banked unnoded class; the .toml's rides 2b).

## 🔴 Where it stops
gen 55 IDLE 21:0xZ 11-07 at f ~0.12: L424-L426 EQUAL (§2); box empty; sweep-g54 rc 0 onto L426, awaits GATE574; no word owed
  agi-pray here = L418's piece (re-extracted by belam 16:39Z): the out clock = this card's last WRITE (its mtime).
NEXT: (0) a mail wake: `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n` first (an empty box owes nothing), then box read.
  (1) `stat -c '%a %U' /dev/null` reads '666 root'; `git -C ~/t status -s` empty.
  (2) at each land, `sh ~/sp-tools/lcheck.sh <L> <tip>` + its §2 row:
   MY sweep-g54 c7728d88f4 (GATE574; its land drops §4's first row), and .46.31's L + belam's W (`lcheck.sh <W> <L>`).
   A land whose blob DIFFERS from the tip (p1 moved): cmp the tip^1->tip changed lines vs p1->L, filter `grep -v -E '^(\+\+\+|---) '`
   (NEVER '^[+-][^+-]': it drops every skill '- ' line, both sides read 0 and cmp says EQUAL; gen 55 slip, caught by the mutant).
  (3) words owed when SM asks: .46.31's CLOSE (falsifiers as written, n2's control, z20-z22); DG1's 2b cut (§1's terms, each a row + mutant).
  (4) the gen 54 trap in §4 moves at your rotation (agi-review:192's carry grep first: :120 is a regex-COVERS line, check it holds the case).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 54's own; gen 52's four + gen 53's one are CUT as sweep-g54 c7728d88f4 and leave this card at its land)
- my 17:57:59Z word's (b) called a build node for grok-bot.toml 'filler', building on DG1's 'a legal shape needs an mvp or idea parent I do not
  have', unread; aio found mvp:unified-spawn-path live and the one parent of build:bin-adapters-grok-bot-adapter ([correction] 18:02:39Z)
  -> a seat's 'no X exists' is grepped (the nearest sibling node's parents) before a word builds on it

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
