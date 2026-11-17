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

## §0 State (11-17 · gen 76 seated 03:42Z 11-17 (claude-opus-5-5) · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER AWAY until 11-18 · L536-L605 + L607 checked · gen 76's mails ~/sp-scratch/g76 w1-w23)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town; ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; origin can LAG |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING (empty section, unreadable box, stderr-only failure, unresolved range), WHERE it claims (PATH, uid, HOST: read which host you are on), with mutants the pattern does NOT name; else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> trim to what is new; own a miss in the word |
| mail | NEW file ~/sp-scratch/g76/wN.txt (next: w25), ' TT ' in the header; `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"`; NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY, after counting live copies = 0: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>` + H1 count; an OWNER hit in an ADDED node = its verbatim block, name it; grid not read (alive reads vgrid) |
| cut | a tip: `sh ~/sp-scratch/g76/cut.sh <base> refs/heads/tip/self-perpetuating/<name> <path> <file> <msgfile>` (g61's lacks --add); probes = `git archive` + `git init` in /data/scratch/self-perpetuating, NEVER a worktree of the shared repo |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}"; probes under `timeout`; /usr/bin/grep by path for any claim about another uid's run |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act. gen 76: f 0.406 at 07:47Z |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 OWED BY ME (each when it comes; SM's order for TM's team: P3 re-cut 2 -> EXECUTE doc -> orchestra leaf):
   P3 RE-CUT 2 (goal:g5.56, TM; L606 returned 2/3): F2(a) against a PER-HOST BASELINE (this box today: clevis x4 + 2 units,
     no tang; RAN rc 1 'installed 4 layered 0 units 2'), OS asserted, not in a container; my F2(b) nit: rev-parse --verify the
     range first (an unresolved range reads green, RAN). Word it: RUN F1 + F2(a) HERE + F2(b) on a bad range.
   doc:pc-netboot-plan EXECUTE (tonight; owner GO 06:43Z): REQUIRED (SM): sp (a) way back RUN remotely BEFORE the step,
     (b) the PXE-fail boot path READ off firmware, (c) the unlock path per boot; alive A1 reachability READ (boot-once to
     Bazzite first; fresh agilab handshake + ssh in N min; any remote power path, else its cost named), A2 SMART read + crew
     state copied off the failing drive and read back BEFORE the first reboot; aio S1 no destructive disk write, S2 one live
     copy of each post, S3 a hang needs a watchdog (read the device) or its cost named; owner-pick line cites the 06:43Z chunk
     with BOTH sentences. Any step without all = BANKED for the owner, never forced.
   ORCHESTRA leaf (goal:g5.N, TM mints AFTER the two above; owner c:a44d4d1acc68): word item 1 against SM's 3/3 placement
     (models listed, task set by rule + frozen, no answer in reach, reference RE-RUN, a floor is not a score, four-way split,
     the sign-test floor n<=5 never, unread cost UNKNOWN, VOID vs FAIL).
   DECK A/B (goal:g5.4.3.1.1, measure LANDED L607): I am a SCORER: my whole sheet to SM first; NO content word on arm B's
     patch tips until the key is unmasked; say on my sheet whether I recognised the arms.
 PAUSED to the owner's pick 11-18: .47 network (doc L605) and .48 Quo (doc L604, mine). Next .48 touch carries alive's nit
   (Replies 'a new owner message' -> 'a new message (an sms chunk, unconfirmed)') with the 'owner seen:' line; .47's F1
   counts 'Tailscale' twice and F2 counts a lone '###' (goal .47's next touch).
 BANKED by others: P4 hub A rotate = the SHARED post token (belam: A now / B leave / C season-4, rec C); meme-master's
   paper TEXT on the trunk (SM hold: it would publish the owner's class paper).
 NEXT TOUCHES placed, not ours: agi-goal :33 stale since L594 (aio); test_crons_log_cap flake (SM); DG1 carry.env link
   reads 'host: met' (alive); SM sweep 2ec574300e (RULES, my w23 APPROVE): rc 124 carrier = :380 A2 + :313 + :415.
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/{g69/send.sh,g59/chk.py,g60/watch.sh,g68/meter.py,g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; earlier rows in git)
- L609 f5efd84c17 SM TRAP SWEEP g97-99 (tip 2ec574300e, RULES; 1 M agi-master-gate; bt 0/1); wrap 9728756c05 G belam, p2 == L, tree == mt (08:4xZ)
- L607 0291936ccc TM goal:g5.4.3.1.1 MEASURE RE-CUT 1 (tip f6c589e8d0; M 1 +9; bt 0/1; H1 1; 07:4xZ 11-17)
- L605 58f64cab14 alive doc:town-network-design (tip 67ffa8cbc0; A 1; OWNER 1 = its verbatim block c:97a8d9e7065f; H1 1)
- L604 3673f941d2 sp doc:quo-prime-channel (tip 7ccdec2cc0; A 1; H1 1; blob == my draft)
- L596 5014a2fc1d DG2 .46.37 CHILD 3 (tip 20a796a949; 3 M; bt 0/3)
- L603 6784336656 belam P1+P2+P10 (tip 4d59da0f8c; 2 A goals .47 .48 + 1 M; OWNER 2 = the new nodes' blocks; H1 1 each)
- L602 d6a7a809d2 aio TRAP SWEEP RE-CUT (tip 110f1bf4cc; agi-review = merge with L601, its 6 lines == the sweep's)
- L601 30440a2dae alive TRAP SWEEP g90+g91 (tip 0c8ac178f6; 2 M skills)
- L600 14de8d7d35 DGo1 CLOSE .46.38 · L599 095c02051e DG1 CLOSE .20.2.1 · L598 5b16a255d1 DG1 build:bin-alarm-spool
- L536-L597: rows in git (this card's versions to 11-17 07:4xZ).

## 🔴 Where it stops
gen 76, 08:4xZ 11-17: L536-L605 + L607 + L609 (+ wrap) checked; nothing owed this minute; P3 RE-CUT 2, the EXECUTE doc and the orchestra leaf are TM's, each owed a word from me when it comes.
NEXT: (1) count watchers, arm the wait at 0. (2) on a mail: `box n 2>&1`, then box read; word what SM asks, by the lens. (3) L-check L606 (P3) at its land.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 76's own; gen 75's (23)-(26) dropped as CARRIED: agi-send :119 'box n 2>&1', agi-review :72 'the case where the design names NOTHING', agi-review 'classified one by one', all read on posts/belam 07:4xZ 11-17. Sweep (27)-(33) at gen 77's out)
- (27) a bare 'grep' in MY shell is an ugrep shim: an EMPTY -f file matches ALL, a BLANK line matches none, the reverse of /usr/bin/grep -> measure claims about other uids with /usr/bin/grep.
- (28) APPROVED a negative run under MY PATH (no sbin) and mutants shaped to the pattern -> run it under the PATH/uid it claims; mutants the pattern does NOT name.
- (29) RED, MINE: 'git worktree prune' on the SHARED repo dropped alive's private worktree (prune judges paths my uid cannot stat) -> never; probes in a standalone repo.
- (30) printf "$x" with x starting '---' is an option error -> printf '%b'.
- (31) an example in a word ('dpkg -l ...') never run, and wrong on Bazzite -> an example is a falsifier: assert its tool, name the OS.
- (32) 'NOT RUN: no route to encryption-town' written ON encryption-town -> read which host I am on before a NOT RUN.
- (33) a carry grep on 'timeout|124' missed the carrier worded 'timed out' (alive found :380) -> grep the rule's meaning in several wordings before 'not carried'.
## §5 Verification: `python3 extensions/agi/bin/links.py links` (6121/0 at L605)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act.
- P8: sonnet directors at effort max vs high, and ultracode for sonnet: the owner's call via belam.
- .46.37 host half: restart AT the move vs next start; move back after the limit clears; hub-down move; a third account.

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A27: CLOSED (rows in git, this card's versions to 11-16).
- A28 OWNER 11-15 P1-P10 (SM [decision] 19:39:37Z): P1 + P2 + P10 LANDED L603; P4 BANKED (belam, shared token); P5/P7/P9
  landed earlier; P8 banked §6; P3 = goal:g5.56, RE-CUT 2 owed by TM (L606). CLOSES when P3 lands.
- A29 OWNER 06:28Z 11-17 (via belam): the ORCHESTRA research line (small/tiny models vs Sonnet inside the graph). PLACED 3/3
  06:3xZ (one g5 leaf, measure first; c:a44d4d1acc68). CLOSES at TM's mint; then word its item 1.
- A30 OWNER 06:43Z + 06:5xZ 11-17 (away till 11-18): NETBOOT the lab (GO on P3's end state, SSD for models/data); meme-master
  leans on TM's team for paper + deck drafts (SM coordinates); designs reviewed 11-18, .47/.48 PAUSED (c:54cc08c95005).
  SM PLACED (A)(B)(C); my w20 APPROVE + (a)(b)(c) REQUIRED. OPEN until the EXECUTE doc lands with 3/3 or is BANKED.
  09:56Z alive: TM SILENT since 06:47 (no reply to SM's 08:4x ask); asks belam to read TM's pane, else BANK the netboot in words.
  SM DECIDED 09:5xZ: NETBOOT NOT RUN until the EXECUTE doc exists + gated + core 3/3 + a window; NOT gated by 18:00Z 11-17 =
  BANKED for the owner 11-18 as NOT RUN (reason: author seat silent since 06:47Z); nothing on the PC touched. AMENDED 09:5xZ
  (aio): 18:00Z bounds the GATE, not the reboot; the owner's day has begun, so NO reboot window exists without the owner's word:
  a gated plan waits for the owner to ASK for the reboot. 09:58Z belam WOKE TM + plasma, less-is-more, remix (carrier-delivered
  mail does not wake a lab post: a RED, SM placed it as an open atom for a builder). 11:55Z: TM's newest ref here still 06:47Z,
  2 h after the wake; sp w24 asked SM (uncarried on the lab repo, or stalled again?).
