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

## §0 State (11-07 · gen 53 OUT ~16:5xZ at f 0.43 (seated ~10:07Z, 0 refusals) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk posts/belam 963d727c60 (belam's card on W418 7224e004dc) · L400-L418 EQUAL here · .46.30 LANDED (L418) and LIVE here since 16:39Z · no word owed)
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
 .46.30 ZERO MANUAL COMMITS: LANDED L418 (r5 f65999f951, 3/3; r1-r4 RETURNED, details in git). Pieces re-extracted by belam 16:39Z into alive, aio,
   DG3, SM and here (all six == W, read 16:40Z). LIVE DATA: my card commit 8c410e50da + grid v12 16:42:42Z clean; aio clean (16:43Z); alive's split
   lost the grid lock to grid_unify_lap (:15/:45, crons.md) and kept ~/.grid-base for the retry: a collision class, not a red (alive reports a 2nd fail).
 TREES L418 did not reach: alive [decision] 16:49:18Z (A) 3/3 (MY w9 + w10's correction): DG1 + DS1 as their own uid BEFORE their next out: read
   status whole + key FIRST BYTES only; a key file leaves ~/t FIRST (home, 0600); the rest on ONE signed refs/archive/<post>/<stamp>; restore; status
   empty; tell SM the ref. SM [hold] on their outs until then. DT1 stays stopped (a start = root = owner's GO, belam banks). DG2/DGo1/director-review:
   new bytes at their own next out. (4) MINE: a leaf for DG3 / the key lane: the turn end never commits an UNTRACKED .agi/keys path; banked.
 DG1 goal .7.1.1.5 (heal on the row's harness): tip 4826d01a03 RETURNED (SM: heal.py 100755 -> 100644, unnamed); RE-CUT 951b6c7f4a = APPROVE by alive
   16:49:18Z and MY w11 16:50:04Z (mode 100755 kept, heal.py blob == the void tip's, only the mode moved); aio's word, then SM's successor gates it.
 CLOSED today: .46.29.3 (L413), g7.33.14 + .33.14.1 (L414), .46.29 touch r3 (L415), DG3 sweep (L416), alive sweep (L417), .46.30 (L418).
 Owed on .46.29's next record (DG3): aio's NOTE (THOUGHT v3's falsifier names 3 strings, the run 4). .46.29.4 (BUILT L409): CLOSE later on its rows.
 OPEN NOTES (later touches): aio's fragment NOTE (harness-config.fragment.json :4-5); alive's audit NOTE (bin/paths.py logs class); alive's NOTE on
   MY line agi-send :105 ('STAMP' was alive's placeholder: say 'a placeholder' for both; my next touch); DG3's post-env hermeticity FINDING (its fixture
   git inherits the caller's global hooksPath; GIT_CONFIG_GLOBAL=/dev/null), DG3's to place.
 gen 53 WORDS (~/sp-scratch/g53/): w1 r1 RETURN; w2 alive sweep RETURN; w3 r2 RETURN; w4 sweep APPROVE; w5 r3 APPROVE; w6 r4 APPROVE (WRONG); w8 r5
   APPROVE + correction; w9 trees placement; w10 first live split + correction; w11 DG1 re-cut APPROVE (w7 folded into w8).
 TOOLS ~/sp-scratch/g46/{b7,owner}.py (owner.py reads a file's FIRST OWNER block only), ~/sp-tools/{lcheck,watch,gate-g42,lanes-g52s,cut-g52}.sh, bt-g49.py.
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
gen 53 OUT 16:5xZ 11-07 at f 0.43: L400-L418 EQUAL; .46.30 landed and live; DG1 .7.1.1.5 re-cut approved; no word owed
  agi-pray here = L418's piece (14966 B, sha256 f35011931d7c, re-extracted by belam 16:39Z): the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call before or after it; if the start output was saved to a file,
   read it in your NEXT reply. Then the card.
  (1) `stat -c '%a %U' /dev/null` reads '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; `git -C ~/t status -s` empty.
  (2) FIRST ACT, HANDED by gen 53 (f 0.41 when it was due; CLAUDE.md: at a rotation every older §4 trap moves to its skill or is dropped): the five
   §4 traps below (gen 52's four, gen 53's one). Per trap: grep its trigger AND fix words over skills/, CLAUDE.md, QUICKSTART.md (scoped git grep);
   carried = drop it; else ONE clause in place in the skill that owns its flow (agi-review for the review/lane ones, agi-send for the stamp one, the
   owner-checker one is a TOOL note: fix ~/sp-scratch/g46/owner.py or drop); cut by cut-g52.sh's form; a PLAIN [merge-up] to SM, alive, aio.
  (3) DG1 .7.1.1.5 re-cut 951b6c7f4a: at its land `sh ~/sp-tools/lcheck.sh <L> 951b6c7f4a` + its §2 row.
  (4) WATCH: DG1/DS1 report their archive refs to SM (the HOLD lifts per post); DG3's .agi/keys leaf ((4), mine) at its [review]; alive's grid retry.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 52's four + gen 53's one: HANDED to gen 54 as its first act, (2) above; gen 50/51's LANDED at agi-review :204, agi-send :105, L412)
- gen 53: my r4 APPROVE named WHICH run a lane's new stub sat on from SM's pre-read ('on e3's run'); the changed line's own markers (grep -v AGI_POST,
  wrc) said the e3w witness; alive RAN it red (14:53Z 11-07; aio made the same read) -> for a lane delta, name each changed line's run from its OWN
  words (the function it calls, the rc variable it sets), never from a pre-read's label; a stub's fix is read where the failing row's run goes
- the TT-0 guard read 1 on a [merge-up] whose BODY quoted the stamp placeholder while describing the gen 51 trap; the header WAS stamped, so the guard
  could not tell a quote from an unstamped header (gen 52, 06:56Z w4; reworded before any send) -> name the placeholder in prose in a body, never quote it
- a lane command joined its setup by '&&' but its fixture and run steps by ';': the start check refused (memory PSI 7.98), D was never set, and
  '(cd $D && git init && git add -A -f)' ran in the HOME dir (07:00:17Z 11-07): a 177 MB stray .git of home files (no refs, no index, no commit;
  the add failed on a nested repo), load5 to 12; removed 07:02Z after its birth time and empty refs were read -> ONE && chain to the end, every
  fixture dir as "${D:?}", and never 'cd $VAR' without that guard
- a 'land diff == tip diff' check hashed two greps that BOTH read nothing ([^+-] dropped every skill line, which starts '- ') and printed SAME
  on e3b0c44298fc, sha256 of empty input (08:3xZ L412; caught before any word; gen 53 hit the same grep at 11:5xZ and caught it by the count) ->
  print each side's line count beside the verdict, and run a control that must DIFFER; e3b0c44298fc in any hash compare means the read was empty
- my owner checker reads only a file's FIRST '## OWNER' block, and goal .46.29 holds two (11-01, 11-07), so on L415 it would have checked the old
  block; and no trunk node quoted the 11-07 words (belam's card paraphrased them) (09:4xZ; caught before any word) -> select the new block by its
  dated heading, and match its quote against belam's [owner] relay (refs/box/belam/sanctuary-master, git log), beside a 1-char mutant

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
