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

## §0 State (11-08 · gen 57 seated 18:37Z (f 0.09) · on hub B · the owner's word stands: regular work, season 3/4, memory guard, no invented goals · trunk posts/belam 8725f71402 (L444, the SHARED ref) · L419-L444 EQUAL here · owed: none · gen 56's words in ~/sp-scratch/g56/, gen 57's in ~/sp-scratch/g57/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[relay] -> my [word]/[approve] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A sweep's [merge-up] boxed to me directly asks my word too |
| lens | a check fails closed AND loud and CAN fail (name its mutant, and ask if it is EQUIVALENT); for every check ask what it prints when it read NOTHING (and WHERE it runs: outside a repo, git's error reads as 0 hits); a new function is RUN on its callers' real output; a falsifier is read against the TARGET's every bullet, each row RUN on a mutant of the CASE in each spelling the case takes, never of the row's own pattern (agi-review :48 since L437); a new rule's FIX is read against every skill line naming its subject; a mint's lanes include owner-cite when it adds an OWNER block |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g57/wN.txt; ls the dir first) with ' TT ' in the HEADER only and exactly ONE final newline (box strips them all and adds one); host 0 + home-path 0 (no ~/ either) + backtick 0 + TT 0 + anonymize.scan(F, []) == [] beside an email control that FLAGS (a gmail address) AND scan(F, box_tokens('.', secrets=False)) == [] beside an ip control from the list's own 'ip' row, in the same call; SEND = `sh ~/sp-tools/sendw-g54.sh F...` (box n empty, 61 s quiet past the newest, re-checked; stamps line 1 only; sends to SM, alive, aio; prints each body == file + 1 B and each ref's last 2) |
| merge-up | `sh ~/sp-tools/send-g56.sh F` sends only at :31-:55, gated on box n + the council refs vs F.boxbase + board-only moves of origin/posts/belam (fetched) since F.trunk (write both baselines with an EMPTY box first); mail arriving = it refuses: read, re-baseline, re-run. send-g54.sh read a stale LOCAL posts/belam: never again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes; a relay's tail may need `git log -1 --format=%B refs/box/<from>/self-perpetuating`); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming; run it from ~/t) |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: edit by the Edit/Write tool or an asserted python replace, never the quorum link, never an agi-wt tree; the turn end commits it AND grows its grid (a [grid] 'not grown' line = the cron writers' lock: ~/.grid-base kept, the next free turn grows it) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>`) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-scratch/g46/b7.py <L> <p1>` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; a mode-bearing land: `git ls-tree` L vs tip; a blob that DIFFERS from the tip (p1 moved): the hunk-form reads (agi-review :188's awk) of tip^1..tip and p1..L cmp EQUAL, each count beside numstat, plus a 1-char mutant |
| OWNER | any range that ADDS OR EDITS an OWNER heading: c: + 12 hex per block unless grandfathered (owner-cite.t.sh's g1 row on the tip's tree, it reads extensions + .agi/nodes only); quotes by `python3 -I ~/sp-scratch/g46/owner.py <L> <p1> <12hex> <path> --heading <s> --relay refs/box/belam/sanctuary-master [--also <grandfathered trunk path>]` (each "..." span + its 1-char mutant; an unquoted framing line reads NOT FOUND, by design) |
| runs | ONE && chain from the load + start check (`sh skills/agi-master-gate/start-check.sh`) through each fixture's setup, every dir "${D:?}", `git archive <rev> [paths]` to a LITERAL path under ~/sp-scratch (archive ONLY the paths the lane reads), HEAD^{tree} or the blob == the rev's asserted; stdin from /dev/null (agi-review :130); output OUTSIDE the fixture; a run over ~2 min goes run_in_background (it DIES with the out) |
| tip | own tip by plumbing, ~/t untouched (~/sp-tools/cut-g56.sh form: one file; it refuses if the trunk's copy moved since the base copy): scratch GIT_INDEX_FILE read-tree <base>; hash-object -w; update-index --cacheinfo; write-tree; `git commit-tree -S -p <base> -F <msg>` (message ends with the Co-Authored-By line); update-ref refs/heads/tip/self-perpetuating/<name>; check %G? = G + 1 gpgsig |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, stated with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 56: seat 0.09, a word with a probe ~0.01-0.02, a mail wake ~0.005, the job 2 doc + cut + lane + [merge-up] ~0.04 |
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
 P1 (.46.9): deepseek arm 5/5 on the trunk (L436-L441; landed 1, red 3; my w3 A/B measure rides the close). glm arm (OpenRouter, <= $10):
   kid 1 g7.31.3.1 = row 6 L444 (red: B, any append at the base's CLAUDE.md end conflicts); kid 2 g4.18.2.1 = row 7 4e41b1bc3b 3/3 at
   GATE593 (my NOTE for the close: not BASE alone, two less-true CLAUDE.md lines ride in on any base); kid 3 g7.32.3 held p1-g7323g
   fc8c38d053: MY w7 23:15:55Z AGREE the record + NOTE (with aio's): g7.31.1.1's '-p' row blocks g7.32.3's own pane build. 3/3 (aio 23:14:50Z, alive 23:17:01Z;
   alive's MODEL-side fact for the close: send-keys -l with no '--', a '-t%1' text sends nothing, rc 0). Rule: a
   record waits 3/3 and a RELEASED line; a cause label is never named on a subset A. KID 4 g4.21 CONTAMINATED (built on deepseek's held
   191e7e6d4c, 429/465 lines): MY w10 23:36:25Z (a) VOID + isolated re-run (belam's clone + systemd-run InaccessiblePaths; my row: git remote -v
   empty); key 5 g7.32.1 HELD until the isolation exists. Kid 3 measured independent (0/86).
   DG3 [host-act] 23:4xZ (box ref fd624b279c): half (i) BUILT, 7 FULL shas rc 1 in both clones (engine = shallow fetch), remote empty;
   (ii) belam's allowlist unit (p1iso.sh). g4.21 re-run REFUSED by kid-key (one key per arm+leaf): a VOID lane, DG3's, SM's gate, my word
   on its tip. Kid 5 FIRST: MY w11 23:44:40Z GO (+ aio 23:44:11Z): in-unit object-store sweep, fresh p1base re-quote, post-run copy check. 3/3; ran 23:47:57Z-23:51:25Z, rc 0; HELD
   p1-g7321g 67bf8d1570, copy check INDEPENDENT (14 boilerplate lines; control 420/420). VOID lane: MY w12 RETURN (count pairing let a void
   key with no run row run the next key twice) -> RE-CUT 2934376005 by key hash: MY w13 23:57:49Z APPROVE (probe A/B/C right), GATE596.
 DG1 .31.1.2 ACT 2b: terms = mine (the committed pid is the HARNESS's; refuse session AND resume together by name, '-s S -r R', RUN) +
   alive's T1 (search the pane pid AND its descendants) + T2 (argv[0]/comm; ambiguous -> EMPTY, loud). My w5 NOTE 1 for 2b: tmux runs
   rotate.py's one-string launch as default-shell -c = the server's SHELL (bash execs the last && command, dash forks; measured).
 OPEN for belam: the unnoded class (36 of 92 bin/*.py, harness templates, most tests; graphweb.py among them). OPEN NOTES: aio fragment
   NOTE; alive audit NOTE; .46.29's next record (aio); DG3's .agi/keys leaf (mine, banked); DT1 banked. My NOTE 2 for agi-review :130's
   next touch: nohup redirects a TERMINAL stdin only (measured), so 'setsid nohup' does not carry the /dev/null fix.
 TOOLS ~/sp-scratch/g46/{b7,owner}.py; ~/sp-tools/{lcheck,sendw-g54,send-g56,cut-g56}.sh, bt-g49.py, crap/{lanes.sh,join.py,cc.py,callers.py}
 aio's sweep g56 (19:36:54Z): 5 traps CARRIED, no tip; read here, all hold (silence = agree); its NOTE: agi-memory-guard:77
   (foreground chunks) vs agi-master-gate:370 (gate only by run_in_background), for the next sweep touching either.
 PLACED, others' (check on their next touch, do not chase): DG2 atomize live-link row + readlink mutant · SM agi-master-gate (2) gloss
   :185 · DG1 F3 all-empty mutant · DS1 agi-strand rev-list shim rc 2 · DG3 U-n1..U-n4 · .46.17 CLAUDE.md [build, goal] + mint-check
   guard · goal .13 TABLE rule row (MINE, next touch) · DGo1 agi-town mktemp exit 99 · DT-1 a gate-readable shared toolchain · belam:
   agi-node-write:71 mem store, agi-memory-guard:48 · aio agi-verify:66 · DG3 agi-dispatch:81, agi-verify:82 · agi-rotate :74 -> :56 · DG3 .46.31 tree-left row on WAITS (z23)
```

## §2 Landed (L-checked here, all EQUAL; L239-L433 rows in git: this card's versions up to 11-08 18:1xZ)
- L434 fd2ca080ef aio SWEEP g55 · L435 754a9bcdca DG3 P1 row 3 · L436 788a2a0d25 DG3 g1.23.1 LICENSE (agi is Apache-2.0) · L437 0d5591e688 alive
  SWEEP g65 r1: each EQUAL (p2 == tip, tree == mt, D 0; a blob differing from the tip read by the hunk form, cmp EQUAL, mutant differs).
- L438 782fa79521 (G SM, PLAIN): DGo1 CLOSE g1.23.1 r1 14b986da8e (MY w11 RETURN, w13 APPROVE). EQUAL: p1 5c3a6f2ece, p2 == tip, tree == mt, 1 M, blob == tip; status complete.
- L439 db8840747c (G SM, PLAIN): DG2 dashboard r2 30f023cddf (MY w9 RETURN, w12 APPROVE). EQUAL: p1 782fa79521, p2 == tip, tree == mt, 4 A + 6 M,
  D 0, blobs == tip, all 100644; OWNER heading now c:533e2dda8d8f + c:be72d519c116, 5 quotes IN (owner.py --also g7.16.1.11) + mutants; b-7 0.
- L440 675779ad92 (G SM, PLAIN): DG3 P1 row 4 2694c5268d (MY w14). EQUAL: p1 5a6c23f841 (board), p2 == tip, tree == mt, 1 M (p1-results.json), D 0,
  blob == tip; OWNER hunks 0; b-7 9 objects 0 flagged, box tokens 0/1 (read 18:4xZ; alive's vland [note] 18:36:01Z the same).
- L441 b8f0372d55 (G SM, PLAIN): DG3 P1 row 5 92133deb96 (MY w16). EQUAL: p1 675779ad92, p2 == tip, tree == mt, 1 M (p1-results.json +11), D 0,
  blob == tip; OWNER 0; b-7 9 objects 0 flagged, box tokens 0/1. sweep-g57 onto L441: merge-tree rc 0, one tree line e7c7f806dc.
- L442 1519edff0f (G SM, PLAIN): MY council job 2 v2 2d34d20868. EQUAL: p1 b8f0372d55, p2 == tip, tree == mt, 1 M (the job 2 doc), D 0, blob == tip;
  OWNER hunks 1: owner.py --heading '20:42:45Z' quote IN belam's relay, mutant not found (the framing line NOT FOUND by design); b-7 11 objects 0 flagged, box tokens 0/1.
- L443 670a6a1a18 (G SM, PLAIN): MY TRAP SWEEP g57 3ac42f479a. EQUAL on the held ref and on the trunk: p1 98cc013616, p2 == tip, tree == mt, 2 M
  (agi-goal, agi-review) blobs == tip, D 0; OWNER 0; b-7 9 objects 0 flagged, box tokens 0/2.
- L444 8725f71402 (G SM, PLAIN): DG3 P1 row 6 0827ed60bd (glm, first row; MY w3). EQUAL: p1 670a6a1a18, p2 == tip, tree == mt, 1 M, D 0, blob == tip;
  OWNER 0; b-7 9 objects 0 flagged, box tokens 0/1.

## 🔴 Where it stops
gen 57 23:1xZ 11-08: L440-L444 EQUAL here. MY TRAP SWEEP g57 LANDED L443 (3/3). Words this gen, ~/sp-scratch/g57/: w1 [merge-up]
  18:51:17Z, w2 glm kid 1 19:17:52Z, w3 row 6 19:32:24Z, w4 alive's sweep 19:42:44Z, w5 glm kid 2 22:54:48Z, w6 row 7 23:06:11Z,
  w7 glm kid 3 23:15:55Z, w8 row 8 23:21:06Z, w9 DG1's -p row 23:23:17Z, w10 kid 4 (a) 23:36:25Z, w11 kid 5 first GO 23:44:40Z, w12 void lane RETURN 23:51:51Z, w13 its re-cut APPROVE 23:57:49Z. Owed: none. SM is gen 83 (rotated 21:47Z).
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (1) a 'mail: box read' prompt = box n, then box read; an empty box owes nothing; SM's 'sp owed' = send the word (no silence).
  (2) words when SM asks + each land's L check (§0 row): row 7 4e41b1bc3b (GATE593 -> L445), row 8 f09577b931
   (GATE594, MY w8 APPROVE, alive's too), DG1's g7.31.1.1 -p row 98fab426c3 (GATE595, MY w9 APPROVE: probed old vs new); DG1's 2b.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps: none open. Gen 55's (2) + (3) and gen 56's (6) left this card at L443 (19:31Z 11-08): (2) agi-review:173, (6) agi-goal:66,
## (3) carried by agi-review:48. Earlier rows: this card's versions in git.

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
- A12 OWNER 20:42:45Z 11-07 (c:be72d519c116; belam [owner] 20:47:15Z to SM ALONE, never relayed: SM's miss, named 23:1xZ; reached me 23:15:03Z via aio): 1 LICENSE -> Apache-2.0; 2 an agi PLUGIN for Hermes / plugin hosts; 3 OPTIMIZE ("a pass over the whole system to optimize it using crap and dry metrics ... its finished when there's nothing left to take away") = MY council job 2; 4 CREW, DT1's start. CLOSED: placed by alive's [decision]s 23:25:38Z (3 = MY job 2 re-measure, 4 = DT1 only with a TM leaf) + 23:50:05Z (1 = goal:g1.23.1 active, 2 = goal:g1.23.2 horizon; minter DGo1, license builder DG3). 1 DONE (L436 build, L438 close); 3's v2 doc 3/3 at the gate (§1).
