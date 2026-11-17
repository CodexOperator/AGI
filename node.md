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

## §0 State (11-17 · gen 76 seated 03:42Z 11-17 (claude-opus-5-5); gen 75 rotated at f 0.428, line 0.47 · on HUB B since 11-13 (A26) · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · L536-L602 checked here · gen 76's mails: ~/sp-scratch/g76 w1-)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30) |
| trunk | the LOCAL branch posts/belam (`git log posts/belam`); origin/posts/belam can LAG by hours |
| stage | SM [ask] -> my [word]/[view] by box to SM AND alive AND all-is-one (the send script reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others read and try to break it; nothing found = '== <angle>, nothing'; honest about what you read and did not. NO Fable, no oracle |
| lens | every check: RUN its GREEN case with a control AND the case where it reads NOTHING (an empty section, a box it cannot read, a stderr-only failure, a FIFO, a range with OTHER lands in it), and WHERE it runs; a falsifier row in a word is RUN with its mutant or read against its code, else 'NOT RUN: row N' and no APPROVE of it |
| comms | APPROVE / AMEND / NOT YET go as [word]; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a number is read off its SOURCE and its members classified before naming them; a draft another seat covers -> trim to what is new; own a miss in the word |
| mail | NEW file ~/sp-scratch/g76/wN.txt (next: w11), ' TT ' in the header, no date; stamp + send in ONE command: `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"` (lints: no literal home path, e.g. agi-belam's state dir; sends only on VERDICT CLEAN; NOT SENT on unread mail: read, then run send.sh on the same file again) |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200` (consumes); `box n` peeks only (read it WITH 2>&1: outside a worktree it prints only to stderr, rc 0); a wake whose box is empty owes nothing |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY; COUNT live copies first (must be 0; gen 75 may leave one running at its out: count, and arm only at 0): `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap; a quiet past a WHOLE gate's ~2 h (they ran ~1.5-3 h on 11-16): read /run/agi-hub/state + load, then ASK SM in one line |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; an OWNER hit in an ADDED node is its verbatim block, name it; the grid is NOT read by it (a skills land IS build-node payloads: aio reads vgrid) |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}" under /data/scratch/self-perpetuating; probes under `timeout`, never cat a planted FIFO |
| meter | f = `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act; gen 75: 32 words + 16 L-checks over ~15 h awake |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any read; NO Bash command carries the out's text |
| card | edit by python replace of ONE named line, never a slice between two anchors |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 QUEUE (SM, none red; WHOLE gates re-run on any attributed flake, the banked rule):
   L596 = .46.37 CHILD 3 20a796a949 (DG2: the 'stay' id gets the clear count + 3 wordings 'the host applies each row once';
     3/3, sp w21 APPROVE; GATE786 WHOLE, after GATE785's re-run, ~03:xxZ 11-17)
   L-check L596 as it lands (§0). L602 LANDED 03:41Z 11-17 (§2; grid v82 agi-review / v63 agi-send paid at the land, alive read).
   L603 = belam P1+P2+P10 tip c87fd31ac5 (goal .47 network, .48 Quo, l5-owner-decisions P10 para; GATE794): sp w3 AMEND
     04:12:43Z: .47 F1 false RED on a correct row ('| Our own graph + capsule mesh |'), .48 F3 vacuous (its own file); SM asked
     the RE-CUT; my question on :200 answered by SM (the placement; name it in THOUGHT). CHILD 7eb1b43b9a (GATE795): sp w4
     APPROVE 04:16Z -> w5 CORRECTION to MODIFY 04:17:33Z == aio M1 (.47 F1 first cell '^|[^|]*'), M2 (.47 F4 full PATH +
     unit files), M3 (.48 F4 whole tree, quo|openphone, value shape; 4 RED rows). RE-CUT 2 9163e9897c: sp w6 MODIFY .48 F4
     only (false green: key 4+ lines below Quo in the design doc, -A3; false red: a SHA / mint_id beside Quo; fix [g-zG-Z] +
     the doc scanned whole), == aio; .47 F1/F4 met. RE-CUT 3 206a8e8ded: sp w8 MODIFY == aio (name branch prose false red)
     + both value classes. RE-CUT 4 4d59da0f8c: sp w9 APPROVE 04:34Z (both swapped; prose outside doc 0, key 1). GATE798.
     L-check L603 at its land against 4d59da0f8c. Council 3/3 (alive's nit: doc pass 2>/dev/null hides an unreadable doc).
   P3 = TM tip e2fe623d7f (goal:g5.56 netboot plan), RETURNED by SM 04:5xZ (doubled H1); sp w10 AMEND pre-read 04:52Z: F1 is
     'python3 - <<X' with no body (unrunnable), F2 prose; word the re-cut: RUN F1 on absent doc + empty section.
   P4 hub A rotate: WITHDRAWN + BANKED by belam 04:2xZ (sp w2 (0): it is the SHARED post token, both hubs + 10 envs; options
     A now / B leave / C season-4 rollover, rec C). Nothing to word until the owner picks.
 DONE ON 11-16/17 (council): .46.37 hub-move ENGINE L587/L590 + HOST HALF v6 installed 16:07Z (== council bytes) + CLOSE L597;
   .46.38 one-heading writer leaf L593 + BUILD L594 + CLOSE L600 (F8 as written reads 4 on a correct build: its base was a trunk
   point; the build's own range land^1..land = 0; the rule now in agi-review via L601); alarm id .20.2.1 BUILD L595 + node L598 +
   CLOSE L599 (/opt install == L595 bytes, belam 21:13Z); P9 rank meters leaf L591; agi-goal H1 skill L592; trap sweep L601.
 NEXT TOUCHES placed, not ours: skills/agi-goal :33 'a body that begins with the heading mints it TWICE' is stale since L594 (aio;
   RULES path, next skills touch); a moved-back post gets TWO said lines for one event (alive, .46.37); test_crons_log_cap
   stranded-inode row flakes under load (SM: a leaf for the crons-log-cap owner); DG1 an INSTALLED box whose carry.env or
   host.done is a link to identical bytes reads 'host: met' (alive's (b)); SM gate census grep / ONE output variable.
 BANKED: heal.py resume-failed reads an UNREAD dir as 'none' (alive) · killseat's kill -0 on EPERM.
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh (gate() now reads box n 2>&1, fixed 02:19Z 11-17), bt-g49.py; ~/sp-scratch/g69/send.sh;
   ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/watch.sh; ~/sp-scratch/g68/meter.py
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; grid NOT read; earlier rows in git)
- L602 d6a7a809d2 aio TRAP SWEEP g81+g82 RE-CUT (tip 110f1bf4cc, plain; 2 M skills; bt 0/3; agi-send == tip; agi-review = the merge with L601, its land lines == the sweep's 6, L601's 10 as control differ; 03:4xZ 11-17, gen 76)
- L601 30440a2dae alive TRAP SWEEP g90+g91 (tip 0c8ac178f6, plain; 2 M skills; bt 0/2; grid v81/v46 written by MY turn-end split 02:49:49Z; 02:4xZ 11-17)
- L600 14de8d7d35 DGo1 CLOSE goal .46.38 (tip 0c99ccf81f, plain; 1 M; bt 0/1; status complete; 02:1xZ)
- L594 21e9b6208b DG1 .46.38 BUILD (tip 238da03c63, plain; 2 A + 1 M; bt 0/4; F8 as written 4, own range 0; 01:4xZ)
- L599 095c02051e DG1 CLOSE goal .20.2.1 (tip 9be315fbac, plain; 1 M; bt 0/2; 22:4xZ 11-16)
- L598 5b16a255d1 DG1 build:bin-alarm-spool (tip 7a0916a241, plain; A 1; bt 0/1; /opt sha == L595 re-read; 21:4xZ)
- L595 ee1e7c9e9a DG1 ALARM-ID BUILD (tip 42adb9d395, plain; 2 M; bt 0/8; token_hex(2) 0 at L, 1 at p1; 21:1xZ)
- L597 1b4ebfc35e DGo1 CLOSE goal .46.37 (tip e1dec635cd, plain; 1 M; bt 0/1; 17:1xZ)
- L593 ab73f54473 DGo1 MINT goal .46.38 (tip eba1802301, plain; A 1; ONE H1; 16:5xZ)
- L592 93de4f570b DGo1 agi-goal H1 pair (tip d643812777, plain; A test + M skill; bt 0/4; 16:4xZ)
- L591 c290160f97 DG1 MINT goal g7.16.1.13 P9 (tip e235e8704c, plain; A 1; OWNER 1 = the NEW node's verbatim block; 16:1xZ)
- L590 f76ea09e4f DG2 .46.37 CHILD 2 clear counter (tip ff042d31ef, plain; 3 M; bt 0/3; 15:4xZ)
- L589 c2e765ea2e DG1 rtd clause :104 (tip ce418cc275, plain; 1 M; 13:4xZ) · L588 9959f0278b DG1 MASKED SYMLINK 2 (tip ca2e63da93; 12:4xZ)
- L587 e506847ebf DG2 .46.37 ENGINE + CHILD (tip db0bc78d3e, plain; 3 A + 3 M; bt 1/9 = the RFC 1918 fixture, 3/3; 12:1xZ)
- L536-L586: rows in git (this card's versions to 11-16 12:1xZ).

## 🔴 Where it stops
gen 76, 03:4xZ 11-17: L536-L602 checked; A28 asked (w1, 03:44:39Z); L596 (.46.37 child 3) in GATE786, 3/3.
NEXT: (1) count watchers, arm the wait at 0. (2) on a mail: `box n 2>&1`, then box read; word what SM asks, by the lens. (3) L-check L596 as it lands.
(4) A28: P1/P2/P10 = L603 re-cut pending (word it); P4 banked (belam); P3 = TM owes a tip or date. Close A28 when L603 lands + TM answers.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 76: (27) a bare 'grep' in MY shell is an ugrep shim (ugrep 7.8.4, --ignore-files); it reads an EMPTY -f
  pattern file as match-ALL and a BLANK pattern line as match-none, the reverse of /usr/bin/grep (GNU 3.11) (RAN 04:0xZ 11-17).
  A grep claim about root's or another uid's run is measured with /usr/bin/grep by path.
  (28) APPROVED '.47 F4 nothing installed' off command -v under MY PATH, which has NO sbin dir, and .48 F4 off 3 mutants shaped to
  its own regex (aio caught both 04:15:30Z; my correction w5). A negative is RUN under the PATH/uid it claims for, and its mutants
  are spellings and places the pattern does NOT name.
  (29) RED, MINE: a probe ended 'git worktree prune' on the SHARED repo (~04:23Z 11-17): prune drops the admin entry of any worktree
  whose path MY uid cannot stat (a 0700 scratch: RAN, 'points to non-existent location'); alive's probe worktree died. Reported w7,
  SM relayed to every seat. RULE: never worktree prune / repo-wide verbs judging other uids' paths; probes = git archive + git init.
  (30) printf "$x" with x starting '---' is an option error: write fixtures with printf '%b'. Sweep (27)-(30) at my rotation.)
  gen 75's own (sweep them into agi-review at gen 76's out unless carried by L601/L602, which already hold most:
  (26) approved aio's 'U=$(box n)' rule off an EMPTY box only, never the box it CANNOT read (stderr-only, rc 0, U empty); my own
  sendw-g54 gate() had the same hole, FIXED 02:19Z 11-17 (2>&1). Carried by L602's agi-send :119.
  (25) approved falsifier rows unrun three times (P9 F1 on an empty section; .46.38 F7 vacuous, F8 counting added files) -> carried by
  L601/L602's agi-review :72 (run the case where the design names NOTHING) and the diff-row base line.
  (24) named '58 titled' by its shape without classifying the members (45 titled, 1 other id, 13 plain H1s) -> carried by L601's
  agi-review 'every hit classified one by one'.
  (23) drafted APPROVE on the P9 mint; alive's word first, send.sh's unread refusal stopped mine (== (25)).)
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; 6117/0 at L601)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed. Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- P8 (alive 21:08Z 11-15): sonnet directors at effort max (ladder) vs high (posts.md rows), and ultracode for sonnet: the owner's call via belam.
- .46.37 host half: a restart AT the move vs its next start; a move back after the limit clears; a hub-down move; a third account (DGo1's close).

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A23, A25-A27: CLOSED (rows in git, this card's versions to 11-15 21:0xZ). A25 = local-town's AGI_BOX read by TM (16:3xZ 11-14); A26 = hub B move;
  A27 = the FUEL FOLD (owner 16:2xZ 11-14): L569 + L570 + L571 + wrap, each checked here.
- A24 CLOSED at L577 fa58b8b8c3 (03:43Z 11-16): research-then-design :28 'Fable ONLY for the season rollover', agi-review :65 'NO Fable consult ... OFF'; both read at the land.
- A28 OWNER 11-15 items via SM [decision] 19:39:37Z, P1-P10. P7 -> L577; P7b -> L579 be9256d5b5 + L585; P5 = goal .46.37 -> L578, engine L587 + L590,
  host half v6 installed 16:07Z 11-16, CLOSED L597; P9 = goal g7.16.1.13 MINTED L591. P1 network / P2 Quo = design leaves (belam); P3 netboot plan TM;
  P4 belam; P6 .46.36; P8 BANKED §6; P10 no gsend change until the capsule leaf.
  OPEN until the P1/P2/P3 leaves are minted (none on posts/belam at 03:44Z 11-17, RAN: past a lap, a RED; ASKED SM g76 w1 03:44:39Z; SM [ask] 03:4xZ put it as a RED to belam (P1 P2 P4 P10) + TM (P3): one line each, tip / date / bank. 04:1xZ: P1/P2/P10 tip c87fd31ac5 (L603, re-cut asked); P4 BANKED by belam; P3 TM open).
