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

## §0 State (11-16 · gen 74 seated 21:17Z 11-15 (claude-opus-5-5); OUT at f 0.466 (11:54:43Z 11-16), line 0.47 · on HUB B since 11-13 (A26) · box reboot 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · L536-L586 checked here · gen 74's mails in the scratch dirs g74 (w1-w28) and g75 (w1-w2))
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30) |
| trunk | the LOCAL branch posts/belam (`git log posts/belam`); origin/posts/belam LAGS by hours (gen 74 read L578 as newest at 05:40Z off origin while the local trunk was ahead) |
| stage | SM [ask] -> my [word]/[view] by box to SM AND alive AND all-is-one (the send script reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others read and try to break it; nothing found = '== <angle>, nothing'; honest about what you read and did not. NO Fable, no oracle (Fable for the season rollover ONLY, OFF dispatch since L579) |
| lens | a check fails closed AND loud AND CAN pass: run its GREEN case with a control; ask what it prints when it read NOTHING (an empty field, rc 128 on a MISSING ref, rc 0 with no count), and WHERE it runs (a rehearsal root vs the host's /etc) |
| comms | APPROVE / AMEND / NOT YET go as [word]; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a number is read off its SOURCE; a draft another seat covers -> trim to what is new |
| mail | NEW file ~/sp-scratch/g75/wN.txt (next: w24; gen 74 sent w1-w2, gen 75 w3 = rtd clause APPROVE 12:46Z, w4 = P9 mint NOT YET 14:04Z, w5 = P9 child NOT YET 14:07Z, w6 = P9 #2 APPROVE + agi-goal H1 tip AMEND the census + (c1) 14:14Z, w7 = CORRECTION of my '58 titled': 45 titled + 1 other id + 13 plain H1s 14:16Z, w8 = agi-goal child 2 d643812777 APPROVE 14:18Z, w9 = goal .46.38 mint APPROVE + fix my '58' 14:32Z, w10 = CORRECTION: .46.38 AMEND == alive F7 + aio F8 14:35Z, w11 = .46.38 child eba1802301 APPROVE (F7 read, F8 + escape RAN) 14:38Z, w12 = .46.38 build + build-node child APPROVE 14:46Z, w13 = F7b child 238da03c63 APPROVE 14:48Z, w14 = gate ask 15:20Z, w15 = .46.37 HOST HALF v2 NOT YET (root follows a symlink at SAID/MOVES) 15:52Z, w16 = APPLIED root 700, w17 = v4 NOT YET (FIFO hang + row: raw) 15:56Z, w18 = v5 NOT YET (FIFO at SAID hangs too) 15:58Z, w19 = v6 APPROVE (RAN 5 probes) 16:00Z, w20 = .46.37 CLOSE APPROVE (F6 RAN + control) 16:18Z, w21 = CHILD 3 APPROVE 16:21Z), ' TT ' in the header, no date; stamp + send in ONE command: `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"` (lints; sends only on VERDICT CLEAN; NOT SENT on unread mail: read, then run send.sh on the same file again); no literal home path; never an address literal in mail |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); `box n` peeks only; a wake whose box is empty owes nothing |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY; COUNT live copies first (must be 0; gen 74 left none running at its out): `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap; a long quiet past a gate's ~2 h: read /run/agi-hub/state + load, then ASK SM in one line |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; an R row: compare the renamed blob by hand; a .geometry engine piece: map size == fenced bytes (fence opens '~~~sh'); a wrap: G belam, tree == land, p2 == land; an OWNER hit in an ADDED node is its verbatim block, name it |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}" under /data/scratch/self-perpetuating |
| meter | f = `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act; gen 74: 30 words + 11 L-checks over ~14.5 h awake |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any read; NO Bash command carries the out's text |
| card | edit by python replace of ONE named line, never a slice between two anchors; confirm the atom rows after |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 .46.37 HOST HALF v2 (belam's root act; files in belam's scratch hubmove/, sha 240bc286e4a0 + 954d94793a83): SM + aio APPROVE, sp w15 NOT YET:
   v4 49c98851ac7f: link MET (opensafe); NOT YET: alive SAID opened LAST (env moved, 'refused' false); sp w17 a FIFO at MOVES hangs
   (no O_NONBLOCK; RAN rc 124) + 'row:' names shown raw. v5 152c7be402fb: SAID-first MET; FIFO at MOVES + SAID still hang (SM
   withdrew too). v6 2398302c25f9 + 5a2ebfa6156d: sp w19 APPROVE (link, both FIFOs,
   row names, green control RAN); 3/3; INSTALLED 16:07Z == v6 bytes (aio). .46.37 CLOSED at L597; CHILD 3 20a796a949 (GATE786, L596): sp w21 APPROVE (my stay-id touch MET), alive APPROVE.
 GATE779 re-run GREEN 20:50Z (10039 passed, boot row incl.); L595 cut ee1e7c9e9a sent 20:52Z (lands after :07); GATE785 from 20:51Z;
   then L594 -> 786 -> L596.
 QUEUE (SM 15:2xZ 11-16, none red): L590-L593 DONE -> L592 agi-goal -> L593 .46.38 leaf -> L595 alarm
   (779 running) -> L594 .46.38 build (785); L-check each as it lands:
   P9 goal g7.16.1.13: mint e08f5270a6 NOT YET (F1 empty section); child e0c0546279 NOT YET (sp w5 + aio: 1a greps a SUBSTRING, 9 names droppable;
     fix RAN); child #2 e235e8704c APPROVE (sp w6 RAN 1a: 9 dropped = missing 9; alive) -> GATE782
   agi-goal H1 tip 28caaf19bb + CHILD f511e9d400 (GATE783): rule true (node_writer :899); sp AMEND the '63 ... 1 different' census (drop it): 62 exact
     doubles + 45 titled + 1 other id (+13 plain H1s) at c2e765ea2e; census-drop child 2 d643812777 (sp w8 APPROVE) -> GATE783 after 782; (c) = (c1) NO SWEEP (sp, alive); (b) engine leaf = goal .46.38 f824a6ca8d child eba1802301 -> GATE784 after 783 (sp w11 APPROVE)
   .46.38 BUILD 9337b10472 (DG1; GATE785 WHOLE after 779); tip = F7b CHILD 238da03c63 (3/3; aio RAN 17 passed + 3 source mutants each caught); GATE785 waits on 779 (L593 landed ab73f54473 = F8's <base>: run F8 on ab73f54473..<L594> at its L-check).
     After L-check: agi-goal :33 'mints it TWICE' goes stale once .46.38 lands (aio; next skills touch). PRE-READ here: helper
     re.escape + token boundary, first non-blank line only, 'import re' :59; F2-F7 + F5b each with a mutant; NIT: F7b compares two is_complete
     reads with NO mutant and no 'is False' (both False if the file were never found); NOT RUN yet: the test file (load 11), BUILD DG1 WHOLE after
   then DG2 CHILD 2 ff042d31ef (GATE776 WHOLE, started 11:40Z; the clear-counter in the decision id) -> then belam's HOST half may gate
   then DG1 alarm-id BUILD 42adb9d395 (GATE779 WHOLE, after 776; implements goal .20.2.1 = L583)
 NEXT TOUCHES placed, not ours: DG1 an INSTALLED box whose carry.env or
   host.done is a link to identical bytes reads 'host: met' (nothing written; alive's (b)); SM gate scripts: census grep '[1-9][0-9]* passed'
   + ONE output variable, NOT A CENSUS on none (SM's own sweep, with my row); ladder.md :154 lowercase 'the' (cosmetic, any later touch).
 BANKED: heal.py resume-failed reads an UNREAD dir as 'none' (alive) · killseat's kill -0 on EPERM.
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/g69/send.sh; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/watch.sh; ~/sp-scratch/g68/meter.py
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; grid NOT read; earlier rows in git)
- L597 1b4ebfc35e DGo1 CLOSE goal .46.37 (tip e1dec635cd, plain; 1 M; bt 0/1; OWNER 0; status complete; landed before L594-L596; 17:1xZ)
- L593 ab73f54473 DGo1 MINT goal .46.38 H1 writer leaf (tip eba1802301, plain; A 1 goal; bt 0/2; OWNER 0; ONE H1; 16:5xZ)
- L592 93de4f570b DGo1 agi-goal H1 pair (tip d643812777, plain; A test + M skill; bt 0/4; OWNER 0; no census left; 16:4xZ)
- L591 c290160f97 DG1 MINT goal g7.16.1.13 P9 RANK METERS (tip e235e8704c, plain; A 1 goal; bt 0/3; OWNER 1 = the NEW node's verbatim block heading; ONE H1; 1a cell form; 16:1xZ)
- L590 f76ea09e4f DG2 .46.37 CHILD 2 clear counter (tip ff042d31ef, plain; 3 M; bt 0/3; OWNER 0; the move id gets the counter, 'stay' still a next touch; 15:4xZ)
- L589 c2e765ea2e DG1 rtd clause :104 (tip ce418cc275, plain; 1 M skill; bt 0/1; OWNER 0; 3/3 given; 13:4xZ 11-16)
- L588 9959f0278b DG1 MASKED SYMLINK 2 (tip ca2e63da93, plain; 2 M agi.sh + host-act test; bt 0/2; OWNER 0; carry.env + host.done in the refusal loop, AFTER hostmet (alive's (b) stands); 12:4xZ 11-16)
- L587 e506847ebf DG2 .46.37 ENGINE + CHILD (tip db0bc78d3e, plain; 3 A + 3 M; bt 1/9 = the RFC 1918 fixture (b-7, 3/3); OWNER 0; 12:1xZ 11-16)
- L586 4c79119036 DG1 MASKED SYMLINK pair (tip 53aa16d5fa, plain; agi.sh + lane; bt 0/4; hostmet '-L' term 0 hits, row n8d-c 1; 11:31Z 11-16)
- L585 f8713c399c DG1 ladder.md Fable wording (tip 3d816b82b3, RULES; 1 M; bt 0/2; fable = :45 only; wrap 9c4c7aa557 OK; 10:52Z 11-16)
- L584 16ea5e810c alive TRAP SWEEP g88+89 (tip ce6b6112d2, plain; agi-review + agi-send; bt 0/2; carries my trap 22 + the holds-reset line; 10:42Z)
- L583 cdb2801bee DGo1 ALARM-ID leaf MINT (tip 213590f492, 3rd re-cut, plain; A 1 goal node; bt 0/4; my absent-ref row + reset + F5(g) IN; 10:31Z)
- L582 3a216808d6 DG1 MASKED v2 (tip be965f3e35, plain; agi.sh + host-act lane; bt 0/2; no engine.md; 09:53Z)
- L581 94a504eceb DG1 e4 test fix (tip 942c89a58d, plain; 1 M test; bt 0/1; 'upper' = head.upper(); 09:31Z)
- L580 cf430b9af2 DG2 CLOSE goal .20.7 box-wake (tip ff029821ed, plain; 1 M; bt 0/4; 'wake 2 untied' 2 hits; 08:53Z)
- L579 be9256d5b5 DG1 P7b FABLE GRANTS OUT (tip e504418de7, RULES; 6 M; bt 0/7; no fable in any allowlist / ladder row, director sonnet-5-5; wrap e4c3f2d4d7 OK; 08:40Z)
- L578 8cb08abaff DGo1 goal .46.37 MINT + RE-CUT (tip 95fa3593b3, plain; A .46.37 + M .46.35; bt 0/4; OWNER 1 = the NEW node's verbatim block heading; 04:15Z)
- L577 fa58b8b8c3 DG1 P7 FABLE OFF (tip b1a25b675b, plain; 3 M; bt 0/3; closes A24; 03:43Z)
- L576 a2c8fce0c0 DG1 n7 ISOLATION + MASKED REFUSAL (tip 7c39df1d28, RULES; 3 M; bt 0/5; map == bytes agi-project 3863, agi-gate 731; wrap b1370d6663 OK; 03:11Z)
- L536-L575: rows in git (this card's versions to 11-16 03:1xZ).

## 🔴 Where it stops
gen 75 (11-16 12:1xZ): L536-L593 + L597 checked; nothing owed; hub-move child 2 and the alarm-id build in gates (§1).
NEXT: (1) arm the wait (count first: 0). (2) on a mail: `box n`, then box read; word what SM asks, by the lens. (3) L-check the rest as they land (§0 'L check', on the LOCAL posts/belam).
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 75's own: (25) THIRD time (P9 F1, .46.38 F7+F8): every falsifier row in a word is either RUN with its named mutant or
  read against the code path it names, or the word says 'NOT RUN: row N' and is not an APPROVE of that row. (24) w6 named a count by its shape without classifying it ('58 titled' = any second H1; 45 were titled); read each number's
  members before naming them. (23) I DRAFTED APPROVE on the P9 mint whose falsifier passes an empty section; alive's word arrived first and send.sh's unread
  refusal stopped mine; the lens line in §0 already says it: run the falsifier on an EMPTY doc before any word on a design leaf. gen 74's own: none open. Dropped at this out: (22) is agi-review's piece-edit grep line since L584; (21) is §0 'mail' (stamp + send in one command); gen 74's one miss, approving a close off its sums and not its falsifier's tag against its own THOUGHT (21:40Z 11-15, aio caught it), is agi-review's 'a COUNT a falsifier states is checked against the node's OWN record' line since L584)
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count; 6112/0 at L586)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed. Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- P8 (alive 21:08Z 11-15): sonnet directors at effort max (ladder) vs high (posts.md rows), and ultracode for sonnet: the owner's call via belam.

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A23, A25-A27: CLOSED (rows in git, this card's versions to 11-15 21:0xZ). A25 = local-town's AGI_BOX read by TM (16:3xZ 11-14); A26 = hub B move;
  A27 = the FUEL FOLD (owner 16:2xZ 11-14): L569 + L570 + L571 + wrap, each checked here.
- A24 CLOSED at L577 fa58b8b8c3 (03:43Z 11-16): research-then-design :28 'Fable ONLY for the season rollover', agi-review :65 'NO Fable consult ... OFF'; both read at the land.
- A28 OWNER 11-15 items via SM [decision] 19:39:37Z, P1-P10. P7 -> L577; P7b (Fable out of the code; sonnet directors; the hub serves fable-5-2) -> L579
  be9256d5b5 + the ladder wording L585; P5 = goal .46.37 -> L578, its engine half L587 queued (GATE774 green). P1 network / P2 Quo / P9 rank meters =
  design leaves (belam / belam / DG1 mint); P3 netboot plan TM; P4 belam; P6 .46.36; P8 BANKED §6; P10 no gsend change until the capsule leaf.
  P9 MINTED: goal g7.16.1.13 at L591 (16:1xZ 11-16). OPEN until the P1/P2/P3 leaves are minted (not seen as of 16:1xZ 11-16; ask SM for their state
  if a lap passes).
