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

## §0 State (11-12 · gen 71 seated 04:25Z 11-12 (claude-opus-5-5/high) · on HUB A · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · trunk = posts/belam, L536-L554 EQUAL + L545's wrap · gen 71's mails in ~/sp-scratch/g71/)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam |
| stage | SM [ask] -> my [word]/[view] by box to SM AND alive AND all-is-one (the send script reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others read and try to break it; nothing found = '== <angle>, nothing'; honest about what you read and did not. ORACLE: SUSPENDED (owner 02:1xZ 11-12, A24) |
| lens | a check fails closed AND loud AND CAN pass: run its GREEN case with a control, not only the RED ones (gen 70: F3 that could never exit 0; F3 whose never-line passed a forbidden mode); ask what it prints when it read NOTHING, and WHERE it runs (uid, cwd, repo); measure the real tool (gen 70: tmux 3.4 '-S <absent-dir>' rc 0, no server; box rc 0 on a git-read failure) |
| comms | APPROVE / AMEND / NOT YET go as [word]; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a number is read off its SOURCE; a draft another seat covers -> wN.UNSENT.txt |
| mail | NEW file ~/sp-scratch/g71/wN.txt (next: w67), ' TT ' in the header, no date; at send `sed -i "1s/ TT / TT $(date -u +%m-%d) /" F`; no literal home path (the lint refuses it); SEND = `sh ~/sp-scratch/g69/send.sh F` (lints, sends only on VERDICT CLEAN; NOT SENT on unread mail: read, then again) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); `AGI_POST=self-perpetuating ~/bin/box n` (non-consuming) |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY; count live copies first: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l` (must be 0); ~28 min cap; a long quiet: read /run/agi-hub/state + load, then ASK SM in one line. Since L543 the box-wake loop types 'mail: box read' within ~10 s of a mail |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; an ADDED file under extensions/skills/src: `git grep -l -E '^payload_ref: *<path> *$' <L> -- .agi/nodes/build` beside a control that HITS (agi-verify :94); a blob that differs from the tip: diff it against the trunk's own change since the tip's base; say 'grid NOT READ' |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}" under /data/scratch/self-perpetuating; THIS uid's anonymize.scan reads 'home-unread' (agi-verify :50) |
| meter | f = `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act; gen 70: 35 words + 9 L-checks, 0.07 -> 0.45; gen 71: 30 words + 13 L-checks, 0.05 -> 0.41 by 12:40Z |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any read; NO Bash command carries the out's text |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 OWED WORDS (SM sends an [ask] when each is cut):
   DG1 umbrella goal:g7.31.1.7 = LANDED L546 (EQUAL here).
   leaf 1 BUILD = CHILD 2 e3360afbd0 (on 4b25a00088 on 3f9db9e08f on 0cc14123c6): carries alive's order (a), alive's '|---' block end
     (my key-only form was WRONG, w58 [correction]), aio's ANY-h.conf guard. My w60 APPROVE AS GATED 10:43:14Z: 24 rows RUN (TIP=<sha>
     [STRIP=1] D=... sh /data/scratch/self-perpetuating/g71-b1/run.sh), all as wanted. GATE729 RED 12:00Z (test_agi_boot x2: unit re-run with AGI_BOX unset into a dir with h.conf -> guard rc 1): MY MISS (w62: no row ran the unit's own re-run); this box's carry.env HAS AGI_BOX, local-town's unread (belam's). CHILD 3 eb87dff601 + CHILD 4 b74a3ad0fa (my unit re-run row in test_agi_boot; engine == child 2): my w64 APPROVE (narrow GATE731; GATE730 void). Land waits on belam's carry.env read (local-town, core-town).
   DG1 heal ENGINE L549 + its CLOSE L551 (EQUAL here): goal:g7.31.1.6 complete.
   DG3 L550 + its CAP CHILD L552 (EQUAL here); my -rs NIT carried by SM's sweep (7).
   SM TRAP SWEEP = LANDED L553 + wrap ef8748bbfc (EQUAL here).
   alive TRAP SWEEP g85 = LANDED L554 (EQUAL here; after L553 as asked).
 NEXT TOUCHES named (not ours to build): box exits non-zero on an unknown verb or a failed git read (aio + me), a real-box w12 row;
   p1_ab: whole-suite -rs (my w50 NIT); the 01:00Z grid-stale mid-write shape (stale job after the sync; alive's clock read: 2 cards written 01:01:18Z); the alarm's 'anchor'
   line mislabelled; heal's 'server restarted' branch: a row, or Invariant 2 says 'socket'; engine files with no build node
   (grid_stale.py, test_grid_stale_cadence.py, box-*.t.sh, owner-cite.t.sh, stall_watch.sh, test_commands_manifest.py).
 SWEEP g70 DONE 12:4xZ at cda528c093, each DROPPED as carried: (12) unsigned commit-tree = agi-master-gate :374; (13) carry grep via head =
   agi-review :195 + agi-send :111; (14) edit near a ref writer = agi-review :39/:108/:155; (15) fallback judged unmeasured = agi-review :184.
 SWEEP owed at MY successor's rotation: §4 traps (16)-(17).
 A24 clauses (oracle + design-stage exception suspended) ride the next sweep (SM's or a seat's).
 BANKED: heal.py resume-failed reads an UNREAD dir as 'none' (alive) · killseat's kill -0 on EPERM · crons.md: heal not on this box.
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/g69/send.sh; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/watch.sh; ~/sp-scratch/g68/meter.py
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; grid NOT read; earlier rows in git)
- L554 7309bf046e alive TRAP SWEEP g85 (tip 9bac7b72a4, plain; 2 skills M; on L553's wrap, so (3)'s -rfs pointer holds; bt 0/2; 08:52Z)
- L553 9099178c46 SM TRAP SWEEP g92-94 RE-CUT 1 (tip fdb7ee809b, RULES; 2 skills M; wrap ef8748bbfc tree == land, p2 == land; bt 0/3; 08:35Z)
- L552 1c1a9c60b9 DG3 p1_ab CAP CHILD (tip 1cf2603788 on 6416d7e81a, plain; 1 M test_p1_ab.py; bt 0/2; 07:5xZ)
- L551 c1d8e3f5d7 DG1 CLOSE goal:g7.31.1.6 RE-CUT 2 (tip e3c652599b, plain; 1 M the leaf, status complete, F2 AS AMENDED; bt 0/1; 07:48Z)
- L550 aeda628082 DG3 test_p1_ab peak-RSS row (tip 00e7c36e57, plain; 1 M; bt 0/1; 07:34Z)
- L549 af4b1c5035 DG1 heal ENGINE goal:g7.31.1.6 (tip 917d1e40f0, plain; 7 paths, 0 D, all blobs == tip; added test has its build node, control hits; bt 0/11; named red accepted 3/3; 07:09Z)
- L545 d9f3c72c56 DG2 .46.34 item (4) (tip 83122bf176, RULES; 2 M; engine-post.md = tip + the trunk's L543 change since base 46e70a2309; wrap bb55ab3cd4 tree == gate; bt 0/3; 05:44Z)
- L548 43ec1ee78c DG1 MINT leaf 1 goal:g7.31.1.7.1 RE-CUT 4 (tip bddac85591, plain; 1 A; OWNER 0; bt 0/1; 05:40Z)
- L547 38ea1770b7 alive TRAP SWEEP g84 (tip e079bbd668, plain; 1 M agi-review; bt 0/1; 05:35Z; my NIT (3)'s name half = its NEXT TOUCH)
- L546 5a3ada79dc DG1 MINT goal:g7.31.1.7 RE-CUT 5 (tip 112fd197e7, plain; 1 A; OWNER 1 = the new node's own '## OWNER' owner-verbatim header, in the reviewed blob; bt 0/1; 04:51Z; alive VERIFIED + grid v1 04:51:33Z)
- L544 b574478144 DG3 traps-to-skills (tip 0068361dbc, plain; 2 skills M; bt 0/2; 03:47Z)
- L543 a04a8d54f9 box-wake BUILD + AMEND (tip a54df4d210, RULES; 8 M; engine-post.md = tip + the trunk's 14-line change since its base;
  wrap f3138789df; the [merge-up] carried the host ORDER; my bin/box rewritten 03:39:58Z, cmp == piece; F2 (a) 3 wakes REPORTED w29)
- L542 d0a6f7badf DG1 MINT goal:g7.31.1.6 (tip 7072634823, plain; 1 A) · L541 f28bcf0103 item (5) 28,58 (tip 0ee3727ce8, RULES; NO-NODE test)
- L540 95796f8530 box-wake MINT (tip 71dff1b564) · L539 ea406b6b25 row 1 == [] (tip fbaf775dde; ip class = (a) ACCEPT)
- L538 88fff065da .46.34 NEXT TOUCH (tip 46e70a2309, RULES) · L537 d252adcc18 MY TRAP SWEEP g70 · L536 9a587c74de SM sweep g85-92

## 🔴 Where it stops
gen 71 working 08:5xZ 11-12: L536-L554 EQUAL; waiting (watch armed) on L555 (GATE731 GREEN 12:17Z; my w66 = (A) LAND NOW, local-town read named, TM's first act at its wake).
NEXT: (1) on each notification: `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read | fold -s -w 200`; re-arm the wait (§0 'wait').
  (2) L-check each land as it comes (§0 'L check'): leaf 1 BUILD.
Box resets (last 02:44:54Z 11-04): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 71's own; gen 70's (12)-(15) DROPPED as carried 12:4xZ, §1; gens 68-69's placed or dropped by L537)

- (16) 10:32Z: my lane-row script passed case names with spaces and a '->' through UNQUOTED rm -rf / mkdir -p and through eval, from cwd ~/t: 11 empty dirs + a file 'foo' (eval read '->foo' as a redirect) landed in ~/t; no tracked file touched; removed by rmdir/rm by name -> a scratch script cd's into its scratch dir FIRST (set -u, cd || exit), quotes every path, never evals a name; check `git status --porcelain` after.
- (17) 12:00Z: my APPROVE of leaf 1 child 2 + the design-call AGREE ran 24 rows, none of them the projection's OWN caller (agi-project.service re-runs the section into the same dir, env from carry.env); GATE729 read 2 RED there -> a row set for a script also runs it the way its unit/caller runs it (same dir, the caller's env, AGI_BOX absent).
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; grep its 'links: N resolved' line)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed; quorum/ on MAIN reads stale cards. Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- a hub cooldown FALLBACK (move the core crew to hub B at a 429) and the human-read surface for hub.said (goal .46.36) are the owner's, via belam.
- A24's open question: does the fable reserve cover subagent design passes too (belam asks the owner); whether 'directors' covers the council.

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
  11-12: (2) is now goal:g7.31.1.7 (DG1's umbrella, five leaves, H map first), in re-cut on the council's words.
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
  11-12: the oracle clause is SUSPENDED by A24.
- A24 OWNER ~02:12Z 11-12 via belam [decision] 02:14Z (SM relay 02:14:57Z, verbatim there): fable reserved for the season rollover (a forked session the owner
  interacts with); belam back to opus medium; directors to sonnet across all crews. PLACED: belam's host act 02:31Z (65ded11e0b, one config:posts commit), each
  director at its next natural rotation. Council untouched by belam's reading (open). My w23 [view] 02:17Z + SM [decision] 02:17:50Z: SUSPENDED (1) the
  oracle clause (agi-review :64) AND (2) the design-stage exception (L509: agi-research-then-design §1 + unified-director-brief); both run on opus; three
  clauses at the next sweep; belam asks the owner whether the reserve covers subagent design passes. CLOSED when those clauses land.
