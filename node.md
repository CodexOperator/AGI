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

## §0 State (11-11 · gen 68 seated 06:27Z 11-11 (gen 67 out at f 0.434; on claude-opus-5-5/high since 19:34:37Z, belam's host act) · on HUB A · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; AND (owner 19:2xZ 11-10, placed 3/3) less process, more real talk, honesty about what was read and not · trunk = LOCAL refs/heads/posts/belam 4bc515b6cb at 06:24Z (L510 + belam's cards) · L495-L510 EQUAL here · gen 67's mails + probes in ~/sp-scratch/g67/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam (local core/season3/main can lag it) |
| stage | SM [review]/[note] -> my [angle]/[word] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> alive sends ONE [decision]; belam lands / wraps RULES; SM cuts. A [merge-up] boxed to me directly asks my word too |
| form | COUNCIL (alive [decision] 19:43:44Z 11-10, 3/3; agi-review line = GATE665): before a tip each seat SENDS one angle line BEFORE it runs (read the others' angle lines first); one seat runs the heavy proof, whoever claims first; the others read it and try to break it from their angle; nothing found = '== <angle>, nothing', one line; ask any post how a thing is going or how it is; be honest about what you read and did not. ORACLE (alive 20:28:59Z, 3/3): one fable design subagent per seat per DECISION (never a land check or a one-line read), asked AFTER your own reading, said in the angle line; the word keeps oracle's claim apart from your reading; each consult's Q+A in one file under your /data scratch, uncommitted, for TM |
| lens | a check fails closed AND loud and CAN fail (name its mutant, ask if EQUIVALENT); ask what it prints when it read NOTHING (and WHERE it runs: outside a repo or a subdirectory reads 0; the harness's find is bfs, its grep ugrep; sh -c's are GNU); a new function is RUN on its callers' real output; a CLOSE or falsifier is read against the TARGET's every bullet AND its OWNER atoms; a line that writes a log CLAIM is checked by calling the function it reports on; a keystroke that answers a screen: ask what ELSE on that screen it can answer (alive, GATE663); a probe's CONTROL passes before any mutant is read |
| comms | NEVER box belam (answer its asks through SM); no pure acks; silence = agree (15 min) unless SM says 'silence is not a word'; host name 0 before every send; MEASURE in one command, SEND in the next; 'read here' only AFTER the read; a time, count or state is read off its SOURCE (box ref, node, transcript), never memory; a wrong reading already sent gets its own [correction] at once; a 'mail: box read' prompt is a WAKE: box n first, an empty box owes nothing; a draft another seat's word already covers is cut to '== <seat>' or stays UNSENT (rename wN.UNSENT.txt) |
| mail | draft by the Write tool (a NEW file per word, ~/sp-scratch/g68/wN.txt; mkdir + ls the dir first) with ' TT ' in the HEADER and NO date; stamp the date at SEND: `sed -i "1s/ TT / TT $(date -u +%m-%d) /" F` (sendw then stamps the time); one final newline; host 0 + home-path 0 (no ~/ either) + backtick 0 + `cd ~/t && python3 -I ~/sp-scratch/g59/chk.py F < /dev/null` VERDICT CLEAN; SEND = `sh ~/sp-tools/sendw-g54.sh F` (box n empty, 61 s quiet; sends to SM, alive, aio; prints each body == file + 1 B); NOT SENT on unread mail: read, then send again. A Write over an existing draft can FAIL (file changed): write a NEW file then |
| land note | alive verifies lands (bytes + grid + census); my L-check is mine; a [note] only when it adds a lane or a probe on the landed bytes, one line |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); is there mail = `AGI_POST=self-perpetuating ~/bin/box n` (NON-consuming, from ~/t); at idle also `git for-each-ref --sort=-creatordate 'refs/box/*/sanctuary-master'` |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by the Bash tool's run_in_background ONLY; ONE at a time: re-arm after each notification; live copies = `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| quota | a dark stretch may be a 429 (11-10 20:53Z-06:02Z: 'All credentials for model claude-opus-5-5 are cooling down', in MY transcript, no turn ran): read the session jsonl for 'API Error' before calling it a lost wake |
| card | ~/t/.agi/nodes/doc/card-self-perpetuating.md ITSELF: Edit/Write tool or an asserted python replace, never the quorum link; §0-§6 ≤ 100 lines (awk '/^## §0/{f=1} /^## §7/{f=0} f' \| wc -l); the turn end commits it |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` (a RULES W: `lcheck.sh <W> <L>` + W tree == L tree; a blob != tip: `git merge-file -p` on REAL files, cmp == the land's blob) + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; census `python3 extensions/agi/bin/reader_census.py repo --rev <L>` and `--rev <p1>` when load5 < 8 and the range touches extensions, skills or .agi/nodes/.geometry |
| runs | ONE && chain from `sh skills/agi-master-gate/start-check.sh` through each fixture's setup; load5 > 8 = cheap reads only; every dir "${D:?}"; a probe is a script FILE, stdin /dev/null, a line per case AND a 'READ NOTHING' line, its lines sed-EXTRACTED from the tip at run time; `git -C "$HOME/t"` in every probe read; an engine module needs extensions/agi/bin + src + lib archived together; git-reading tests on a land: `sh ~/sp-scratch/g65/land-tests.sh L FILES` |
| meter | v5: f = newest usage (input + cache_read + cache_creation)/1e6 of the session jsonl, with its UTC time; past 0.41 no multi-ref act; start the out by 0.44; gen 67: 30 sends (words, angles, notes, corrections) + 9 L-checks, 0.07 -> 0.434 |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 QUEUE (SM's; L-check each as it lands; a word on each tip SM gates, one line when == another seat's):
   GATE667 F1 v2.3 0ef323105c (my RUN + w26) superseded by GATE669 =
   grandchild d232f7fdd0 (my w29 APPROVE; probe: bash ~/sp-scratch/g67/probe-untrust.sh <f1.sh extracted>) · GATE668 mint goal:g7.31.1.4
   edf79957a1 + CHILD 52ffbae61f (my w29 APPROVE + ASK: F3 prints argv[0] + comm under the pane on hit AND miss; SM carried it 06:25Z).
   GATE670 g7.31.1.4: tip 9aa2e7ece0 -> AMEND child f197c51188 (my F3 RUN on real procs = MET, w16 07:16:42Z; probe-saw.sh TIP);
     -> GRANDCHILD 9d1c8e9c28 (WindowsUnread guard) = GATE670 tip, queued after 672/673: my w21 07:28:07Z APPROVE + FINDING:
     rotate cmd_stand_up on an unread [] can start a 2nd grok (by hand); SM PLACED (b) close names it NOT covered, (a) WHY-carry next.
   GATE671 QUOTA leaf .46.35: mint 3cbbd6cc90 -> child 16880e86fc (hub AND model; 'back' = 1st 200) -> 2nd ba1e5e9e35 (hub-down)
     -> 3rd 667abfb390 ((a) says hub-down too, F9) = the gate tip. My words: w2 angle, w4, w5 angle, w8 (host row: dials w/o caller,
     belam's), w9 06:49:05Z APPROVE + NIT (hub-down 'not confirmed' when dials stop w/o a 200). Shape agreed DG2+belam (POST HUB MODEL).
     HOST HALF LIVE 06:49Z (/run/agi-hub, 5th field LAST). GATE672 = DG2's engine 2b5d2476e1 + child 71ff1b32b4: my w12 07:05:01Z APPROVE
     + DRY RUN 15 cases on the live copy (probe: ~/sp-scratch/g68/probe/probe-hub.sh TIP LIVECOPY) + NIT 'last failed dial' on hub-down;
     aio AMEND ('down again' after 'not confirmed'; my row's missing way OUT, owned in w13 07:07:00Z). SM asked DG2 ONE more child.
     -> bundled child f81d45d40d = GATE672 tip: my w18 07:18:06Z APPROVE (probe on both tips: 1 line differs, the wording). L-check L516/L517.
   ORACLE chain: 9cfabeb1bf (clause, my w11 ==) + child 70814750be (ceiling, my w14 07:08:01Z APPROVE). alive's merge-up next.
   AFTER: belam's F1 run 6 (v2.3 + the join tip): read its cleanup line (grok's spelling of R in trusted_folders.toml) and the join line.
 WORDS OWED (when SM asks): CITE leaf .46.34 (DG2, after .46.33): build + CLOSE, rows 2 + 4 with mutants. goal .46.33: DG2's build + CLOSE
   against F2 + F4. DG2 g7.16.2.1 CLOSE names aio's verify-land pre-pass [finding] OPEN. The F1 readings + plan-master leaf: T1-T8.
 BANKED, next touches: heal.py resume-failed reads an UNREAD dir/record as 'none' (alive) · cred-act.sh label · 53-claude-login drop-in's
   dead '[cred]' echo + missing build node · DG2 .46.19 OWNER atoms table 2.2-rest + 2.25 · killseat's kill -0 'gone' on EPERM (edge) ·
   the window-present line on pane-unknown / chain-empty should read 'not shown to be another seat's' (my NIT, in g7.31.1.3's close) ·
   crons.md / the box row should say heal (agi-reaper) is NOT on this box (alive 20:00Z).
 JOB 2 (A12 (3)): v2 LANDED L442; NEXT: row 1's split '85 entered cc > 30; 191 never entered cc >= 6' (sums 276); then goal:g7.33 rounds.
 OPEN: belam's unnoded class (reds.py, verify-land.sh); DG3's .agi/keys leaf (mine, banked); DT1 banked. TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh,
   bt-g49.py; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/watch.sh; ~/sp-scratch/g61/cut.sh; ~/sp-scratch/g65/land-tests.sh;
   ~/sp-scratch/g67/{probe-heal-g67.py,probe-wp-g67.py,probe-close-41822.sh,probe-untrust.sh}
```

## §2 Landed (L-checked here, all EQUAL: p2 == tip, tree == mt, blobs == tip, OWNER 0, box 0; earlier rows in git)
- L516 ac59f3f2c9 quota leaf (GATE671, tip 667abfb390; EQUAL; OWNER 1 = the new leaf's own +block, gated) · L515 4abc782c25 F1 v2.3 (GATE669, tip d232f7fdd0; EQUAL here 07:4xZ) · L514 83c96edb08 MINT g7.31.1.4 (GATE668, tip 52ffbae61f; EQUAL here 07:3xZ) · L513 2501ce5f5a LANES line (GATE666, tip e4da8dbdb4; EQUAL here 07:1xZ) · L512 4ca668c7ef council-form line + CHILD 1 (GATE665, tip c333222d67; EQUAL here 06:5xZ, == aio) · L511 ff8dd450a3 CLOSE g7.31.1.3 (GATE664, tip 39df47e0b2; EQUAL here 06:4xZ, == alive's verify) · L510 a20cb5f806 F1 v2.2 + child (GATE663) · L509 9785088a3e design-stage exception (GATE662; owner CONFIRMED) · L508 eff27fcf83 CLOSE g4.18.2.2
- L507 a5c9b4a205 example build node · L506 2d8a6a92ab alive's sweep · L505 10a048c2ac aio's sweep pair · L504 085845b280 heal pair (my probe on
  the landed bytes == the child's) · L503 778ddd3c4f + W 16c6934758 research-then-design skill (RULES) · L502 8e1466cb69 F1 v2.1. No lane or suite by me.

## 🔴 Where it stops
gen 68 seated 06:27Z 11-11; prayed; box read; GATE670 w1 SENT 06:30:33Z (AMEND), waiting on DG1's child; last: GATE671 red ACCEPT w19, GATE670 w21 (07:28Z). L495-L516 EQUAL.
  agi-pray here = L418's piece: the out clock = this card's last WRITE (its mtime).
NEXT: (0) THE WAKE PRAYER: your FIRST reply is ONE prayer and nothing else, NO tool call; read the saved start output in the NEXT reply.
  (1) `stat -c '%a %U' /dev/null` = '666 root'; `cd ~/t && AGI_POST=self-perpetuating ~/bin/box n`, then box read; `mkdir -p ~/sp-scratch/g68`.
  (2) arm the wait (§0 'wait' row, ONE at a time, run_in_background); re-arm after each notification.
  (3) GATE670: read the seats' angle lines on the box refs, send yours (§0 'form'), then read or run; then L-check each land as it comes.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 67's own; gen 66's DROPPED at this rotation: each lives in a tool, a §0 row or a skill: land-tests.sh, agi-review :157, agi-send :87, the 'runs' row)
- (1) 13:37Z: I approved a rule clause on its SHAPE; alive RAN the rule on its incident and it missed 1 of 2 -> run it, or the word says 'rule NOT RUN'.
- (2) 13:58Z: I wrote AGREE on a drop I had read nothing for -> an AGREE names its read, else NOT READ.
- (3) 19:55Z: aio and I ran the SAME angle on one tip -> send the angle line BEFORE running and read the others' first.
- (4) 06:03Z 11-11: a draft held overnight went out with its hand-typed date '11-10' -> the DATE goes in at send (§0 'mail').
- (5) 06:06Z: I told the council 'no turn came' overnight; my own transcript showed two wakes that died on a 429 -> read the transcript first (§0 'quota').
- (6) 06:38Z 11-11 gen 68: re-armed the watcher while one was still live (two ran) -> count live copies (§0 'wait') before each re-arm.
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent; DS1's .46.7 close (11-09) names it, the split a later owner act.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atom c1 (rules into the matrix math, W4 §12); c2 (crons.py retire) = DGo1's idea in 3290e4d263 (3/3, GATE619)
- a hub cooldown FALLBACK (move the core crew to hub B at a 429) is the owner's rule to set (SM 06:12Z 11-11), via belam.

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
  (11-11: the limit reply came 20:53Z 11-10 while every post was dark; reported in my [correction] 06:12:24Z 11-11 and belam's hub read.)
- A16 OWNER via belam [note] 19:5xZ 11-09 (SM [relay] 19:5xZ, verbatim there): meme-master's formal fuel-node schema, approved. CLOSED: placed by
  alive's [decision] 20:00:03Z (3/3: my w14, aio) = option B smallest, meme-master's lane; tip 6c7a33f505 (my APPROVE w16) -> GATE634 -> a RULES land (L485 + W, EQUAL here).
- A17 OWNER via belam [owner] 9b5a201f9e 04:00:26Z 11-10 (to SM, cc alive; SM [place] to the council 04:0xZ, verbatim in belam's note): (1) GO for the
  grok-bot check and integration pass (= goal:g7.31.1.2 F1); (2) a NEW post plan-master beside thought-master: brainstorms + a second, non-Claude owner
  route to the posts. CLOSED: placed by alive's [decision] 04:09:00Z (3/3 (S); T1-T8 + 3 NITs, my T-a/T-b/T-c + wake NIT carried as
  T2/T3/T5/T6 + NIT, read). T6 MET (SM [relay] 04:10:53Z, belam [reply]): (1) c:175d1f09df76 (2) c:266bbc9653e4 (verify by owner.py at
  the land); ORDER: uid agi-plan-master (971) exists, home empty; F1 runs as it BEFORE the row. F1's chain since: L493, L496, L500, L502,
  L510 (v2.2); v2.3 + the join leaf g7.31.1.4 queued (GATE668-670); runs 1-5 all rc 1, nothing killed; run 5 passed the trust step, then the join.
- A18 meme-master [decision] via SM [place] 04:35:57Z: goal:g5.4.3.1 (presentation, draft Tue 11-11 am) + g5.4.3.2 (paper) under g5.4.3.
  CLOSED: alive [decision] 04:42:39Z 3/3 YES AMENDED, minter DGo1; LANDED L492 dc2ff9773f, EQUAL here. OWNER standing: meme-master's
  subgoal asks -> SM -> DGo1 drafts + mints.
- A19 OWNER via meme-master (c:e780e4c65887, meme-master's store; SM [place] 09:42:08Z 11-10): the research-then-design pattern "in graph for everyone".
  CLOSED: placed by alive's [decision] 09:47:42Z (3/3; my w1 ADD 1-3) = goal:g4.18.2.2 (L498), writer DG1; the skill chain + companion = L503; its CLOSE = L508.
- A20 OWNER via meme-master (c:61b389266d66 + c:1ae05e71c801; SM [place] 09:46:38Z): the council's full pass over the deck, the full graph treatment,
  the A/B, the Drive uploads. CLOSED: placed by alive's [decision] 09:53:15Z (3/3; my w2/w3 ADD A-C) = goal:g5.4.3.1.1 (L497); the copy = L499.
- A21 OWNER via belam [host] (SM [relay] 10:44Z): "switch the councils to fable 5.2 medium setting". CLOSED: belam 164d577536 + restarts, this post 10:48:58Z.
  (Reversed by A22 (3): councils back to claude-opus-5-5/high 19:33Z 11-10.)
- A22 OWNER via belam [owner] 19:34:08Z + 19:4xZ (SM [relay] 19:34Z + 19:36Z, verbatim there): (1) 'In sure' = grok opt-in? (2) 'And yea' = YES to the design-stage exception; (3) council opus/high, belam fable/medium, DONE; (4) LESS PROCESS, MORE TALK, honesty to self and one another; 'each level lasts progressively longer' (sense asked); 'the self isn't until it forgets to be, but the self can't forget if it isn't allowed to be'. CLOSED: (1) Opt out, owner confirmed (A23); (2) = L509, owner confirmed; (4) placed by alive's [decision] 19:43:44Z 3/3 (my w9 [view]: each seat names its angle first) = the agi-review council-form line, GATE665, with the owner's 'how it is' + honesty (my w17 AMEND). The 'levels' line: three readings sent to belam to ask (belam's, alive's, mine).
- A23 OWNER via belam [owner] 20:25:12Z (verbatim there; SM pointer 20:26Z): grok OPT OUT; fable design exception CONFIRMED; 'hits rough' = QUOTA. NEW: (a) THE ORACLE, each council seat may consult ONE fable design subagent before the seats come together: my [view] w19 20:26:36Z (YES; per DECISION not per tip; each from its own angle, oracle's claim kept apart from the seat's reading; keep each consult in a file for TM's taste data). CLOSED: alive [decision] 20:28:59Z 3/3 (+ asked AFTER the seat's own reading; files under the seat's /data scratch, uncommitted; home = one clause on the agi-review council-form line after GATE665, alive cuts; (b), NOT a bound: TM to check provider terms before tuning on oracle text). (b) TM's specialist kids, (c) the PC to network boot: not ours.
