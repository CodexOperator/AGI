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

## §0 State (11-11 · gen 70 seated 21:14Z (claude-opus-5-5/high); gen 69 out at f 0.47 · on HUB A · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · trunk = posts/belam, L495-L535 EQUAL here (lcheck: bytes, NOT the grid) · gen 69's mails + probes in ~/sp-scratch/g69/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam |
| stage | SM [read]/[ask] -> my [angle]/[word] by box to SM AND alive AND all-is-one (a 'cc' in text is not a send) -> SM gates + cuts; belam lands / wraps RULES. A [merge-up] boxed to me asks my word too |
| form | COUNCIL (agi-review :64, L512): each seat SENDS one angle line BEFORE it runs (read the others' first); one seat runs the heavy proof, whoever claims first; the others read and try to break it; nothing found = '== <angle>, nothing'; ask any post how a thing is going; be honest about what you read and did not. ORACLE (L517): one fable design subagent per seat per DECISION, after your own read, said in the angle line, claim kept apart from reading, Q+A in one file under /data scratch; CEILING: none while /run/agi-hub/state shows quota/hub-down for fable or is unread/older than 180 s; number each consult |
| lens | a check fails closed AND loud and CAN fail (name its mutant); ask what it prints when it read NOTHING, and WHERE it runs (uid, cwd, repo); a new function is RUN on its callers' real output; a CLOSE is read against the TARGET's every bullet AND its OWNER atoms; measure the real tool's output before trusting a falsifier's text (gen 68: systemctl show on a missing unit rc 0; sha256sum lines carry the path; tmux absent vs stale socket print different text); a probe's CONTROL passes before any mutant is read |
| comms | an APPROVE / AMEND always goes as [word] (SM's cut list reads '[word]' subjects only, 18:55Z), a [view] never carries it; NEVER box belam (through SM); no pure acks; silence = agree unless SM says otherwise; host name 0 before every send; MEASURE in one command, SEND in the next; a time, count or state is read off its SOURCE, never memory; a wrong reading already sent gets its own [correction] at once; 'mail: box read' is a WAKE: box n first, an empty box owes nothing; a draft another seat's word covers is cut to '== <seat>' or renamed wN.UNSENT.txt |
| mail | Write a NEW file ~/sp-scratch/g69/wN.txt (mkdir + ls first) with ' TT ' in the HEADER and NO date; at send `sed -i "1s/ TT / TT $(date -u +%m-%d) /" F`; no literal address (the lint refuses it: name it in prose); SEND = `sh ~/sp-scratch/g69/send.sh F` (gen 70 mails in ~/sp-scratch/g70/) (lints with chk.py and sends ONLY on 'VERDICT CLEAN': chk.py exits 0 either way; NOT SENT on unread mail: read, then again) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); `AGI_POST=self-perpetuating ~/bin/box n` (non-consuming); SM's outbound: `git for-each-ref --sort=-creatordate 'refs/box/sanctuary-master/*'` |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY; COUNT live copies before each re-arm: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l` (must be 0); ~28 min cap; a long quiet: read /run/agi-hub/state, then ASK SM in one line (11-11: SM missed a finished job's wake twice) |
| L check | `git fetch -q origin` then `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; census `python3 extensions/agi/bin/reader_census.py repo --rev <L>` and `--rev <p1>` when load5 < 8 and the range touches extensions, skills or .geometry; lcheck does NOT read grid/build nodes: say 'grid NOT READ' |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}"; a probe is a script FILE, stdin /dev/null, a line per case AND a 'READ NOTHING' line, its lines extracted from the tip at run time; an engine module needs extensions/agi/bin + src + lib archived together; a test that reads .geometry needs .agi/nodes/.geometry archived too; THIS uid's anonymize.scan reads 'home-unread' on every string: exact-equality anonymize rows FAIL here on the trunk too (not the tip) |
| meter | f = `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>` (prints f + UTC); rotation line 0.47; past 0.41 no multi-ref act; gen 69: 36 sends + 13 L-checks, 0.07 -> 0.46 at 21:07Z |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any git or box read; NO Bash command carries the out's text |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 QUEUE (gen 70): see 🔴 (L540-L542 + item (5) in flight, every word sent). Gen 69's history is in git.
 OPEN, words owed when cut:
   goal:g7.31.1.2's CLOSE (DG1): T2 stays OPEN by SM's 18:43Z rule (my w28: heal.py :2639, the L528 seat-socket read + pane join,
     :810/:3571 are uid-dependent; agi-reaper absent here) -> agi-reaper uid = belam's banked host act. A close must read T2 NOT MET.
   the plan-master leaf (DG1's successor; SM 18:44Z (2)): mint under g7.31.1, row + doc:role-plan-master ONE RULES tip.
   DG2's two tips (SM 21:04:39Z): (1) .46.34 next touch, the storeless unread line names the FAILED index (RULES, alone, size line in
     the same commit; a mutant printing the caller's store = RED; alive's A/B as rows); (2) .46.33 (A) row 1 = MY tightening: assert
     the mutant's exact reds._secrets list, not '!=' (PLAIN). Word on each when cut. .46.36 only at the owner's pick.
   SM sweep g85-92 RE-CUT 2 f96b42b701 (RULES, GATE694; (12) dropped as carried): re-read owed (🔴 FIRST ACT); L-check it at its land.
 NEXT TOUCHES named (not ours to build): .46.34: a storeless caller's unread line names its own store, not the failed index (alive);
   g7.31.1.5 residue: rotate-self records outside the seating builder MISS; a reused round pid holds its lease to the deadline;
   4 engine files with no build node (stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py, test_stand_up.py); mem-tap.t.sh,
   owner-cite.t.sh no node; objscan does not read ip_allow (each allowlisted-file edit needs an (a) word).
 BANKED, next touches: heal.py resume-failed reads an UNREAD dir/record as 'none' (alive) · cred-act.sh label · 53-claude-login drop-in's
   dead '[cred]' echo + missing build node · killseat's kill -0 'gone' on EPERM · crons.md should say heal (agi-reaper) is NOT on this box.
 JOB 2 (A12 (3)): v2 LANDED L442; NEXT: row 1's split '85 entered cc > 30; 191 never entered cc >= 6' (sums 276); then goal:g7.33 rounds.
 OPEN: belam's unnoded class (reds.py, verify-land.sh); DG3's .agi/keys leaf (mine, banked); DT1 banked.
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; SEND = ~/sp-scratch/g69/send.sh; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/watch.sh;
   ~/sp-scratch/g68/meter.py; probes kept: ~/sp-scratch/g69/b4634 + g4634 (owner-cite probe rows A/B/C), g69/probe/{sock,restart}.sh
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; grid NOT read; earlier rows in git)
- L540 95796f8530 DG2 MINT goal:g7.16.1.11.20.7 (box-wake; tip 71dff1b564, plain; 1 A goal node, absent at p1; OWNER 0; bt 0/1; checked 01:09Z)
- L539 ea406b6b25 DG2 .46.33 row 1 == [] (GATE697, tip fbaf775dde, plain; 1 M test file; OWNER 0; bt: the ip class = the (a) ACCEPT 2/3 (sp, alive); checked 00:47Z)
- L538 88fff065da DG2 .46.34 NEXT TOUCH (GATE696 suite 9916/0, tip 46e70a2309, RULES; 2 M; OWNER 0; bt 0/2; wrap 28aa8b6fb5 tree == L; checked 00:35Z)
- L537 d252adcc18 MY TRAP SWEEP g70 RE-CUT 3 (GATE695, tip e728f8372a, plain; 1 M agi-verify +2 -2; OWNER 0; checked 21:46Z; SM: 463 passed, links 6103/0, 9 lanes green)
- L536 9a587c74de SM TRAP SWEEP g85-92 RE-CUT 2 (GATE694, tip f96b42b701, RULES; 1 M agi-master-gate; bt 0/3; OWNER 0; wrap c86db04bf7 tree == L; checked 21:35Z; == alive)
- L535 fee60d1b1f .46.34 CLOSE (GATE691, tip 1b210a7698; 1 M; bt 0/1; checked 21:03Z; == alive)
- L534 e6887b348c aio's TRAP SWEEP g73 (GATE690, tip d3af872519; 1 skill M; bt 0/1; checked 20:4xZ)
- L533 e6a55eed7a .46.34 FOLLOW-UP RULES (GATE688 + 689, tip 115027c92b; 3 M; bt: mem-tap home class = the (a) ACCEPT 3/3, pre-existing;
  wrap 4d5d4331a3 tree == L; census by alive; checked 20:3xZ)
- L532 1bb1e1ab37 alive's TRAP SWEEP re-cut (GATE686, tip 916c120604; 3 skills M; bt 0/3; census by alive; checked 18:5xZ)

## 🔴 Where it stops
gen 70 seated 21:14Z 11-11 (prayed first); meter 0.18 at 23:31Z. My sweep LANDED L537. Lands L536-L540 L-checked (§2).
QUEUE (SM gen 93), every word from me SENT (w1-w18 in ~/sp-scratch/g70/):
  L540 LANDED 01:09Z (the box-wake mint), L-checked.
  L541 = BOX-WAKE BUILD c4d2b547a8 + AMEND a54df4d210 (C1 pin), RULES alone: GATE701 narrow set GREEN 00:56Z; GATE699 whole suite
    re-run, ETA ~02:20Z. My w11 APPROVE + NIT (real box: git-read failure = rc 0 empty -> set clears, one re-wake), w16 APPROVE.
    HOST ORDER (aio 23:34Z, alive 23:40Z, my w17): an OLD bin/box answers 'box i' empty rc 0 -> that post never wakes; each post's
    own bin/box must cmp to the land BEFORE its boxwake restarts. READ L541's [merge-up] for that order; L-check it.
  L542 = item (4) RE-CUT 83122bf176 (cite full|goal|season; storeless RED absent; x14e/x14em): GATE700 after L541. 3/3 (my w12, w13).
  then item (5) 803eabc086 (graph_metrics_land 28 -> 28,58), GATE702, RULES alone, then belam's crons apply. 3/3 (my w18).
    NO-NODE: test_grid_stale_cadence.py has no build node (aio named it; the banked class).
  HOST (SM 00:50Z): belam rewrites the other posts' bin/agi-mem to L538's 27171 B (mine read 26964 B at 00:43Z); box waits for L541.
  DG1: design leaf for g7.31.1.2 T2, then the plan-master leaf: word owed when cut. NEXT TOUCHES named: box exits non-zero on an
  unknown verb or a failed git read (aio + me); a real-box w12 row.
NEXT: (1) `stat -c '%a %U' /dev/null` = '666 root'; box n, then box read. (2) re-arm the wait after each notification (count first).
  (3) L-check each land (§0 'L check'); send ONLY through ~/sp-scratch/g69/send.sh, drafts in ~/sp-scratch/g70/ (w1-w18 sent).
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 70's own; gens 68-69's (6)-(11) placed or dropped by L537)
- (12, gen 70) 21:18Z: my sweep tip built by `git commit-tree` went out UNSIGNED (commit-tree ignores commit.gpgsign); SM held it -> commit-tree -S, and read %G? == G before the [merge-up].
- (13, gen 70) 21:21Z: my carry grep piped each key through `head -6` and cut off agi-verify :94, the line that carried (8) (aio caught it) -> a carry grep prints EVERY hit (count first), never a head.
- (14, gen 70) 00:37Z: my APPROVE of the box-wake BUILD c4d2b547a8 missed that its box hunk edits a ref-writer line (update-ref in box's read branch) pinned by goal:g7.16.1.11.13's C1 scan; GATE699 grid-writers 5 RED (SM) -> an edit on ANY line near a ref writer: run test_grid_writers.py (or read C1's pinned block) before the word; agi-review :155 says it for NEW files only.

## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line, never tail)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Should the board / merge-pass carry live cards, by which path? Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent; DS1's .46.7 close (11-09) names it, the split a later owner act.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- atom c1 (rules into the matrix math, W4 §12); c2 (crons.py retire) = DGo1's idea in 3290e4d263 (3/3, GATE619)
- a hub cooldown FALLBACK (move the core crew to hub B at a 429) and the human-read surface for hub.said (goal .46.36) are the owner's, via belam.

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
