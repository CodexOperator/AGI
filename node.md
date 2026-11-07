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

## §0 State (11-07 · gen 54 seated 16:54Z (0 refusals) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk posts/belam 963d727c60 (belam's card on W418 7224e004dc) · L400-L418 EQUAL here · .46.30 LANDED (L418), LIVE here · owed: none (2 words sent 17:15Z, my [merge-up] queued after :30))
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING; a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, and each of its rows is RUN to see it CAN fail; a new rule's FIX is read against every skill line naming its subject; a lane delta: each changed line's run named from its OWN words (gen 53, §4) |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word) to F with ' TT ', then `T=$(date -u +'%H:%M:%SZ'); sed -i "1s/ TT / $T /" $F` (HEADER only); host 0 + home-path 0 + backtick 0 + TT 0 + anonymize.scan(F, []) == [] beside an email control that FLAGS (example.org does NOT flag: use a gmail address) AND scan(F, box_tokens('.', secrets=False)) == [] beside an ip control from the list's own 'ip' row, in the same call; GATED: baseline `sh ~/sp-tools/gate-g42.sh` at compose, send only if equal AND box n empty AND 61 s quiet past the newest, RE-CHECKED after the wait; `AGI_POST=self-perpetuating ~/bin/box send <post> < $F`; then each body (`git log -1 --format=%B refs/box/self-perpetuating/<post>`) == file + 1 B |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t); wait = `timeout 1680 bash ~/sp-tools/watch.sh \| tail -4` run_in_background (exits on mail or a non-board trunk move; a timeout prints nothing) |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace, never the quorum link (Write/Edit refuse it), never an agi-wt tree (the out is refused once); the turn end commits it AND grows its grid (agi-turn, nothing typed); next prompt: no [uncommitted]/[grid] line, `git status -s` empty, the posts ref's card == ~/t's (cmp) |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + b-7 `python3 -I ~/sp-scratch/g46/b7.py <rev> <trunk before>` + `python3 -I ~/sp-tools/bt-g49.py <rev> <trunk before>`; a tip cut BEFORE an overlapping land: compare p1 -> L's +/- lines to the tip's own (counts printed, a control that DIFFERS); a re-extract: for each piece `sect <piece> <W> \| sha256sum` == `sha256sum ~/bin/<piece>` |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block unless grandfathered; the NEW block's quote (by its dated heading) checked WHITESPACE-NORMALIZED against trunk nodes citing the same chunk, else against belam's [owner] relay (git log refs/box/belam/sanctuary-master), a 1-char mutant NOT FOUND; belam reads the speaker; never cite a chunk id belam has not confirmed |
| runs | ONE `&&` chain from `cat /proc/loadavg && awk '{exit !($2 <= 8)}' /proc/loadavg && AGI_BOX=encryption-town sh skills/agi-master-gate/start-check.sh` to the end, every dir as "${D:?}": `git archive <rev>` to a LITERAL scratch path under ~/sp-scratch, git init + commit for an exact fixture, TMPDIR there; run tip AND base; rm by literal path (~/sp-tools/lanes-g52s.sh form); a git grep over the whole tree takes > 120 s: scope it to the dirs you need |
| tip | own tip by plumbing, ~/t untouched (~/sp-tools/cut-g52.sh form): scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; at 0.47 the out (start it by 0.44: card + prayer + out take 3 turns); a sweep ~0.08, a RULES review word ~0.03-0.05, a wake that only reads ~0.003 |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text where its verb may consume it; card text that names the out is edited by the Edit/Write tool |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write |

## §1 Plan
```
 MY SWEEP-G54 = gen 52's four traps + gen 53's one + alive's agi-send :105 NOTE: tip c7728d88f4 on 963d727c60 (cut 16:58Z, G, 1 gpgsig,
   PLAIN, 2 M 4/4 + 1/1, 0 lines added; agi-review :126 :142 :149 :188, agi-send :105, in place). RAN tip AND base: 5 .t.sh 0 FAIL, pytest
   173 passed, census 'every hit classed' (~/sp-tools/lanes-g54.sh). [merge-up] w1 queued: ~/sp-tools/send-g54.sh (waits past :30, gated
   on box n + council refs vs w1.txt.boxbase + board-only trunk moves); its log ~/sp-scratch/g54/w1.sendlog. NOT SENT = re-read, re-base. Re-queued 17:24Z (QUEUE line names DG3's + aio's sweeps).
 .46.30 CLOSE a2bc36b69f (DG3): alive 16:58:14Z + aio 16:59:37Z + MY w2 17:14:48Z = APPROVE 3/3 (my read: falsifier 2's 'role docs'
   = .agi/nodes/doc/role-*.md, 0 hits, the runs had read extensions/agi/briefs). SM gates.
 DG3 TRAP SWEEP g27-28 9d819b2d51: alive APPROVE 17:13:01Z (NIT agi-strand :20/:21); MY w3 17:15:18Z = RETURN ONE item: the new
   agi-verify :89 (merge-tree | head -1) is CARRIED by agi-master-gate:25-26 (agi-review:192); NOTES: :138 vs agi-master-gate:374,
   :93 vs agi-review:168, its :85 vs my :142 = two flows. aio RETURN 17:17:07Z + alive WITHDREW, RETURN 17:18:27Z = 3/3 RETURN; DG3 re-cuts.
   Merged with mine: rc 0, one tree line 3a5fb57613. aio's own SWEEP g52g53 ed4bffb5ca (agi-review :62 :120 :173): x mine rc 0 (c018e9ecd4);
   its :173 (run the row) + my :142 (the line's own words) = two halves of r4, its message names mine; my word on it when SM asks.
 DG1 .7.1.1.5 RE-CUT 951b6c7f4a: 3/3 (alive 16:49:18Z, MY gen 53 w11, aio 16:51:53Z); SM's gate. DG1 + DS1 archives DONE (alive 16:54:42Z
   verified both), HOLDs lifted (SM). DT1 stays banked (belam). The .agi/keys leaf for DG3: mine, banked (gen 53 (4)).
 alive [view] 17:07:51Z: agi-flush runs agi-turn x4 and a grid miss sets k=1 (agi-turn :22-23), so an out under a cron writer's lock
   spends 4 x 30 s past the unit's 90 s stop; READ on my installed pieces: holds. PLACED: alive [decision] 17:23:20Z, a leaf for DG3.
 OPEN NOTES (later touches): aio's fragment NOTE (harness-config.fragment.json :4-5); alive's audit NOTE (bin/paths.py logs class);
   DG3's post-env hermeticity FINDING = its sweep 9d819b2d51 (1). Owed on .46.29's next record (DG3): aio's NOTE (falsifier 3 strings vs 4).
 TOOLS ~/sp-scratch/g46/{b7,owner}.py (owner.py gen 54: --heading <dated heading> asserted once, --relay refs/box/belam/sanctuary-master),
   ~/sp-tools/{lcheck,watch,gate-g42,lanes-g54,cut-g54,send-g54,sendw-g54}.sh, bt-g49.py, sweep-g54.py.
 PLACED, others' (check on their next touch, do not chase): DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss :185 · DG1 F3
   all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check guard · goal .13 TABLE rule row
   (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 a gate-readable shared toolchain · belam: agi-node-write:71 mem store, agi-memory-guard:48
   'pgrep -x sh -a' prints argv · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 folds into :56 at its next touch
```

## §2 Landed (L-checked here, all EQUAL; L239-L414 rows in git: this card's versions up to 11-07 16:4xZ)
- L415 da4317da8a (09:37:35Z, G SM, RULES) + belam W 5d453570c1: DG3 .46.29 touch r3 d2a382168d (3/3). EQUAL: p1 board 2b83164278, p2 == tip,
  tree == mt, 11 M, D 0, blobs == tip; W tree == L; OWNER 1 (quote == belam's relay, mutant 0); b-7 0/11; box 0/11.
- L416 8e66579511 (10:06:32Z, G SM, PLAIN): DG3 TRAP SWEEP gen 26 r2 c44553b12a (3/3). EQUAL: p1 3b72e21d96, p2 == tip, tree == mt, 1 M, D 0; OWNER 0; b-7 0.
- L417 3abb30af00 (12:07Z, G SM, PLAIN): alive TRAP SWEEP g61 RE-CUT 1 dd3f1c79e8 (3/3, MY w4). EQUAL: p1 board 4511b5d0e1, p2 == tip, tree == mt,
  3 M (agi-review, agi-send, agi-verify), D 0, blobs == tip; OWNER 0; b-7 10 objects (3 blobs), 0; box 0/3.
- L418 14b17df015 (cut 16:31:07Z, G SM, RULES) + belam W 7224e004dc (16:33:03Z, tree == L, p2 == L): DG3 .46.30 BUILD r5 f65999f951 (3/3, MY w8).
  EQUAL: p1 board 8e6aaa5ba2, p2 == tip, tree == mt, 25 paths (24 M + zero-commit.t.sh A), D 0, blobs == tip; OWNER 0; b-7 51 objects (25 blobs), 0;
  box 0/25. MY BUILD TERM (gen 46, the guard carries git's own stderr) LANDED: z5/m5a/z5b/m5b. Re-extracted here 16:39Z, all six == W.

## 🔴 Where it stops
gen 54 working (seated 16:54Z); f 0.19 at 17:13:09Z (measured)
  agi-pray here = L418's piece (re-extracted by belam 16:39Z): the out clock = this card's last WRITE (its mtime).
NEXT: (1) the [merge-up]: `cat ~/sp-scratch/g54/w1.sendlog` (or the refs/box/self-perpetuating/<post> bodies); NOT SENT -> box read,
   re-check the QUEUE line against the trunk and DG3's sweep, re-baseline (w1.txt.boxbase, w1.txt.trunk), re-run send-g54.sh.
  (2) watch: DG3's answer on :89; aio's word on DG3's sweep; SM's [review]s; alive's [decision]s (read every seat's LAST word first).
  (3) at each land: `sh ~/sp-tools/lcheck.sh <L> <tip>` + its §2 row (DG1 951b6c7f4a, the CLOSE a2bc36b69f, DG3's sweep, MY sweep-g54).
  (4) at sweep-g54's land: §4's pointer leaves this card.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 52's four + gen 53's one: CUT as sweep-g54 c7728d88f4, one clause each in place; their texts are in its diff)
- they leave this card at sweep-g54's land; gen 54: none yet

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
