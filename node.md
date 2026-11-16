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

## §0 State (11-15 · gen 74 seated 21:17Z 11-15 (claude-opus-5-5) · on HUB B since 15:12:44Z 11-13 (A26); hub B out of quota 05:36Z-15:00Z 11-15 (this post dark) · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · trunk = posts/belam, L536-L575 checked here · gen 74's mails ~/sp-scratch/g74/ (w1-w2))
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); encryption-town; ~/t = DETACHED, committed by the TURN END (goal .46.30); live trunk = posts/belam |
| stage | SM [ask] -> my [word]/[view] by box to SM AND alive AND all-is-one (the send script reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others read and try to break it; nothing found = '== <angle>, nothing'; honest about what you read and did not. NO Fable, no oracle (owner 11-15 19:01Z: Fable for the season rollover ONLY; agi-review :65 OFF line at L577) |
| lens | a check fails closed AND loud AND CAN pass: run its GREEN case with a control; ask what it prints when it read NOTHING, and WHERE it runs (uid, cwd, repo, which host's /etc); measure the real tool (gen 73: systemd-analyze verify resolves a missing Required unit from the HOST's /etc, aio) |
| comms | APPROVE / AMEND / NOT YET go as [word]; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a number is read off its SOURCE; a draft another seat covers -> trim to what is new |
| mail | NEW file ~/sp-scratch/g74/wN.txt (next: w14), ' TT ' in the header, no date; stamp + send in ONE command: `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"` (lints; sends only on VERDICT CLEAN; NOT SENT on unread mail: read, then send again); no literal home path |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read \| fold -s -w 200` (consumes); `box n` peeks only |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY; COUNT live copies first (must be 0): `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap; a long quiet past a gate's ~2 h: read /run/agi-hub/state + load, then ASK SM in one line. The box-wake loop types 'mail: box read' within ~10 s of a mail |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>`; an R row: compare the renamed blob by hand (lcheck mis-reads R's tab path); a .geometry engine piece: map size == fenced bytes (fence opens '~~~sh', count from it); a wrap: G belam, tree == land, p2 == land |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}" under /data/scratch/self-perpetuating |
| meter | f = `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act; gen 73: 29 words + 7 L-checks over ~29 h incl. a 9.5 h quota gap |
| box | `stat -c '%a %U' /dev/null` must read '666 root' before trusting any read; NO Bash command carries the out's text |
| card | edit by python replace of ONE named line, never a slice between two anchors (gen 73 lost A27 that way); confirm the atom rows after |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-goal · agi-post · agi-node-write · agi-verify |

## §1 Plan
```
 SENT w1 21:22:26Z: P7b CHILD e504418de7 APPROVE (GATE768, L579 alone) · DG2 CLOSE CHILD 5d25eb18ec HOLD for one outside idle read
   (GATE769) + CORRECTION: of gen 73's 53 wakes only 2 time-tied; THIS SEAT offered as the idle target: if belam mails it, tie from the transcript
   (mail ref time, no running turn then, the new turn, no joined text) and send that. HOLD NOT MET (alive 21:28:56Z: belam's 21:24:37Z 'idle' read was a model wait; SM retracted 21:29:50Z). belam asked to run MY setup;
   w3 21:30:52Z fixed the tie rule: (a) prev turn's last record >= 5 s before the wake AND no open api-request; (b) the wake record; (c) no joined text.
   DONE: belam pinged 21:33:35Z, outside read EMPTY prompt 21:33:53Z; my w4 21:34:48Z tied it IDLE (gap 51.9 s, new turn 21:33:38.074Z, no queue, exact text).
   DG2's child 7c6dab7407: COMPLETE on the named bar 3/3, BUT aio's tag fix (wake 2 untied) in ONE more child first (w6 21:44:13Z; my miss named).
   Fix child ff029821ed APPROVED (w7 21:48:24Z, == alive): GATE770 gates it after GATE769. L-check it when it lands. alive asked SM on GATE763 (3 h+): watch for the L576 wrap.
   w2 21:26:05Z: gen 73's wakes by GAP = 55: 38 tied idle (>=5 s), 17 shape; control = my 21:22:58Z mid-turn wake reopened a turn at 1 s gap.
   Tie method: gap from the previous assistant/system record to the wake's user turn (>=5 s = idle). Owed: nothing until a mail.
 QUEUE, L-check each as it lands (SM numbers): L576 DG1 masked-unit FIX 7c39df1d28 (on fe2681a189, RULES; GATE763) · L577 P7 5d1945e4b3 + child
   b1a25b675b (PLAIN; GATE764; closes A24) · L578 goal .46.37 RE-CUT 95fa3593b3 (PLAIN; GATE766) · DG2 CLOSE goal .20.7 c451734ec6 (GATE767; my w29 APPROVE
   with alive's tie-in) · P7b (above).
 w11 03:33Z: DG1 MASKED v2 be965f3e35 APPROVE + NIT (in-root ABSOLUTE chain resolves on the HOST under readlink -f; rehearsal only) -> L582 after L581.
 w12 03:48Z: alarm_spool ENGINE leaf (SM 03:47:03Z, DG1 mints: id 64 bits + skip prints) APPROVE + clause: already_sent's could-not-read -> False -> silent RE-send; tell it apart.
   PLACED 3/3; MINT 82a0b20902 -> RE-CUT asked (SM 03:56:44Z): HOLD in the node (alive) + my w13 row: a MISSING ref (rc 128, same as a
   read failure) = 'not found' -> sent, no line; a HOLD is not a send retry. NEXT: word the re-cut (check those two are IN), then DG1's build.
 NEXT TOUCHES named, not ours: DG1 masked() by readlink -f or size 0 (alive empty file, aio relative symlink); DG1 n7 under SYSTEMD_UNIT_PATH done at L576?
   (read it); research-then-design :104 one clause 'under L509, now OFF' (aio); alive's sweep widens agi-review :158 (carries my trap 22) + box n reword;
   TM's card :18 quotes a pre-L574 agi-project message; .46.37 builder DG2 engine / belam host.
 BANKED: heal.py resume-failed reads an UNREAD dir as 'none' (alive) · killseat's kill -0 on EPERM · test_council_report e4 'upper' (head[:10].upper()
   with no a-f = a valid prefix, ~1.8%/suite; w9 22:24Z) -> FIX 942c89a58d (whole sha upper + assert) APPROVED w10 22:33:49Z, GATE771, lands L581. GATE763 cut waits a whole pytest re-run (g396, ~2 h from 22:2xZ).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/g69/send.sh; ~/sp-scratch/g59/chk.py; ~/sp-scratch/g60/watch.sh; ~/sp-scratch/g68/meter.py
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; grid NOT read; earlier rows in git)
- L577 fa58b8b8c3 DG1 P7 FABLE OFF (tip b1a25b675b, plain; 3 M; bt 0/3; OWNER 0; no wrap; closes A24; 03:43Z 11-16)
- L576 a2c8fce0c0 DG1 n7 ISOLATION + MASKED REFUSAL (tip 7c39df1d28, RULES; 3 M; bt 0/5; map == bytes agi-project 3863, agi-gate 731; wrap b1370d6663 OK; land 03:11Z 11-16, checked 03:1xZ)
- L575 c61457cc36 DG1 RAM UNIT PER BOX (tip accb9e6800, RULES; 4 M; bt 0/4; map == bytes agi-project 3880, agi-gate 719; wrap 9482c61e59 OK; land 05:31Z, checked 15:05Z after the quota gap)
- L574 e4dd5841bd DG1 agi.sh HOST TOUCH (tip dfd3d15b66, RULES; 6 M; bt 0/6; 'AGI_BOX:-encryption-town' 0; map == bytes 3880/703; wrap 3427b17423 OK; 02:31Z)
- L573 ab726811bf DG1 fallback CUT + fixture (tip 688f6f85e0, RULES; engine.md + 6 tests; 'AGI_BOX:-' 0; map == bytes 3931/639; wrap 7a6c4f24b6 OK; 23:4xZ 11-14)
- L572 3692ed307d alive TRAP SWEEP g87 (tip 644fcdbecb, plain; 2 skills; 23:3xZ) · L571 7c3d513028 meme-master FUEL L-b (tip c0400cd834, RULES; growth 'fuel' 0, schema 'spawn:' 0; wrap 7d77ab3840 OK)
- L570 ed49dc0237 meme-master FUEL L-a1 (tip 59f456f373; R to deprecated/fuel/ by hand; active -1/deprecated +1, sum held) · L569 5721fb7d37 belam FUEL L-a2 (tip 9b00bd4fa0; same checks)
- L536-L568: rows in git (this card's versions to 11-14 16:0xZ).

## 🔴 Where it stops
gen 74, 03:1xZ 11-16 (box reboot 00:41Z, session resumed): L536-L577 checked; all words sent (w1-w10); L577-L581 + DG2 close queued; IDLE, the wait armed.
NEXT: (1) on a mail: box read; an idle-read test from belam -> tie it (§1). (2) L-check L576-L578, L579 (P7b child) as they land. (3) re-arm the wait.
Box resets (last 00:41:42Z 11-16; this session resumed after it): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 73's own; at this out: (18) DROPPED: gen 72's header slip, now inside §0 'mail' (stamp + send in one command); no skill owns this post's scratch mail script)
- (22) 20:00Z 11-14: my w2/w5 on DG1's cut read engine.md + the live units, never the TEST lanes that run the piece under env -i -> GATE754 red 3 lanes (w14) -> a word on a piece's new refusal greps every lane that runs the piece, its callers and the glob form, and names what it did not read. CARRIED by alive's next sweep (agi-review :158 widened): drop at YOUR rotation once landed, else move it there yourself.
- (21) 16:48Z 11-14: w4 written by heredoc and sent WITHOUT the date sed (header '16:47:40Z ->') -> stamp + send in ONE command, every mail. Move or drop at YOUR rotation.
## §5 Verification: `python3 extensions/agi/bin/links.py links` (broken must stay at the trunk's own count)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed. Decided nothing (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes: 'passed with ONE shared workspace' until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act
- P8 (alive 21:08Z): sonnet directors at effort max (ladder) vs high (posts.md rows), and ultracode for sonnet: the owner's call via belam.

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A23, A25-A27: CLOSED (rows in git, this card's versions to 11-15 21:0xZ). A25 = local-town's AGI_BOX read by TM (16:3xZ 11-14); A26 = hub B move;
  A27 = the FUEL FOLD (owner 16:2xZ 11-14): L569 + L570 + L571 + wrap, each checked here.
- A24 CLOSED at L577 fa58b8b8c3 (03:43Z 11-16): research-then-design :28 'Fable ONLY for the season rollover', agi-review :65 'NO Fable consult ... OFF'; both read at the land.
- A28 OWNER 11-15 items via SM [decision] 19:39:37Z, P1-P10. My w24: P7 MODIFY (oracle at agi-review :65 also live) -> 3/3; P7b (Fable out of the code,
  w26: A, sonnet directors, the hub serves fable-5-2) -> tip dd8aea4da0 OWED; P5 = goal .46.37 (w27, re-cut 95fa3593b3 w28 3/3: one move per post,
  file freshness, the moved post told in its own box, when the route takes effect) -> L578. P1 network / P2 Quo / P9 rank meters = design leaves
  (belam / belam / DG1 mint); P3 netboot plan TM; P4 belam; P6 .46.36; P8 done; P10 no gsend change until the capsule leaf.
  OPEN until L577, L578 and P7b land and the P1/P2/P3/P9 leaves are minted.
