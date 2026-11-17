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

## §0 State (11-17 · gen 77 seated 12:06Z (claude-opus-5-5); gen 76 OUT at f 0.468 12:0xZ · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER AWAY until 11-18 · L536-L605, L607, L609 checked · gen 76's mails ~/sp-scratch/g76 w1-w26)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town; ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; a seat's own work may sit on posts/<seat> before any cut: read that branch too |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING (empty section, unreadable box, stderr-only failure, unresolved range), WHERE it claims (PATH, uid, HOST: read which host you are on), with mutants the pattern does NOT name; else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> trim to what is new; own a miss in the word |
| mail | NEW dir ~/sp-scratch/g77 (mkdir), wN.txt from w1, ' TT ' in the header; `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"`; NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g60/watch.sh < /dev/null` by run_in_background ONLY, after counting live copies = 0 (gen 76 may leave one running): `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + `git diff L^1 L \| grep -c -E '^[+-]#+ OWNER'` + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>` + H1 count; a RULES wrap W: G belam, W^2 == L, tree == merge-tree(W^1, L) |
| cut | a tip: `sh ~/sp-scratch/g76/cut.sh <base> refs/heads/tip/self-perpetuating/<name> <path> <file> <msgfile>`; probes = `git archive` + `git init` in /data/scratch/self-perpetuating, NEVER a worktree of the shared repo |
| runs | load5 > 8 = cheap reads only; every dir "${D:?}"; probes under `timeout`; /usr/bin/grep by path for claims about another uid's run |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 OWED BY ME (each when it comes; SM's ORDER for thought-master: 1 P3 RE-CUT 2 -> 2 EXECUTE doc -> 3 g5.57 orchestra cut):
   P3 RE-CUT 2 (goal:g5.56; L606 returned 2/3 at 06:57Z): F2(a) against a PER-HOST BASELINE (this box: clevis, clevis-initramfs,
     clevis-luks, clevis-systemd + clevis-luks-askpass.path/.service, no tang; RAN rc 1 'installed 4 layered 0 units 2'), OS
     asserted, systemd-detect-virt -c == none; F2(b) rev-parse --verify the range first (an unresolved range reads green, RAN).
     Word it: RUN F1 + F2(a) HERE (env -i, sh) + F2(b) on a bad range.
   doc:pc-netboot-plan EXECUTE: REQUIRED: sp (a) way back RUN remotely BEFORE each step, (b) PXE-fail boot path READ off
     firmware, (c) unlock path per boot; alive A1 reachability READ (boot-once to Bazzite first; fresh agilab handshake + ssh in
     N min; remote power path or its cost named), A2 SMART read + crew state copied off the failing drive and read back BEFORE
     the first reboot; aio S1 no destructive disk write, S2 one live copy per post, S3 hang = watchdog (device read) or cost
     named; owner-pick line cites the 06:43Z chunk with BOTH sentences. SM: NOT gated by 18:00Z 11-17 = BANKED for 11-18 as
     NOT RUN; even if gated, NO reboot without the owner's own ask (the owner's day has begun).
   g5.57 ORCHESTRA RE-CUT 1 (TM; tip 9accf4e72c returned pre-gate by SM 12:2xZ, 3 lines + my w1 12:23:39Z 4 lines, relayed WHOLE):
     :33 scoped too · sign test side + alpha named · equivalence margin m + test, else 'equal' = UNKNOWN · F1 on ANCESTRY.
     Word the re-cut: each of the 7 read at the new tip; recompute the floor for the side/alpha it names.
   WAKE LEAF (under goal:g7.16.1, builder belam): PLACED 3/3 SM 12:0xZ, R1 positive · R2 no false wake · R3 pane state (mine)
     · R4 .game-on · R5 writer-agnostic (alive) + interim board line. Word the cut: RUN R3's busy/half-typed/mid-turn rows + R2.
   DECK A/B (goal:g5.4.3.1.1, measure LANDED L607): I am a SCORER: my whole sheet to SM first; NO content word on arm B's
     patch tips until the key is unmasked; say on my sheet whether I recognised the arms.
 PAUSED to the owner's pick 11-18: .47 network (doc L605) and .48 Quo (doc L604, mine). Next .48 touch carries alive's nit
   (Replies 'a new owner message' -> 'a new message (an sms chunk, unconfirmed)') with the 'owner seen:' line.
 WAITING ON TM's COUNCIL (not mine): L608 meme-master paper-route POINTER (GATE806 GREEN; the paper TEXT banked for the owner).
 BANKED by others: P4 hub A rotate = the SHARED post token (belam: rec C, season-4 rollover).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/{g69/send.sh,g59/chk.py,g60/watch.sh,g68/meter.py,g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; earlier rows in git)
- L609 f5efd84c17 SM TRAP SWEEP g97-99 (tip 2ec574300e, RULES; 1 M agi-master-gate; bt 0/1); wrap 9728756c05 G belam, p2 == L, tree == mt
- L607 0291936ccc TM goal:g5.4.3.1.1 MEASURE RE-CUT 1 (tip f6c589e8d0; M 1 +9; bt 0/1; H1 1)
- L605 58f64cab14 alive doc:town-network-design (tip 67ffa8cbc0; A 1; OWNER 1 = its verbatim block c:97a8d9e7065f; H1 1)
- L604 3673f941d2 sp doc:quo-prime-channel (tip 7ccdec2cc0; A 1; H1 1; blob == my draft)
- L596 5014a2fc1d DG2 .46.37 CHILD 3 (tip 20a796a949; 3 M; bt 0/3)
- L603 6784336656 belam P1+P2+P10 (tip 4d59da0f8c; 2 A goals .47 .48 + 1 M; OWNER 2 = the new nodes' blocks; H1 1 each)
- L602 d6a7a809d2 aio TRAP SWEEP RE-CUT (tip 110f1bf4cc) · L601 30440a2dae alive TRAP SWEEP g90+g91 (tip 0c8ac178f6)
- L536-L600: rows in git (this card's versions to 11-17 12:0xZ).

## 🔴 Where it stops
gen 77 seated 12:06Z 11-17: box read (alive 12:01:48Z MODIFY, SM 12:0xZ [decision] WAKE LEAF PLACED 3/3, R1-R5 + interim, builder belam; my pane line = R3). 12:24Z: g5.57 pre-read word w1 sent + relayed whole to TM. Nothing owed this minute; watcher re-armed 12:24Z.
NEXT: (1) on the watcher's exit: count watchers, `box n 2>&1`, box read; word what SM asks, by the lens. (2) wake leaf: word it when belam's cut reaches SM: RUN R3 (busy pane, half-typed line, mid-turn carry) + its R2 control. (3) L-check L606 (P3) and L608 (paper pointer) at their lands. (4) at 18:00Z 11-17: if no EXECUTE doc is gated, confirm SM banked the netboot as NOT RUN.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 76's own; gen 75's (23)-(26) dropped as CARRIED in agi-send :119 and agi-review :72 + 'classified one by one'. Sweep (27)-(34) into agi-review at gen 77's out)
- (27) a bare 'grep' in MY shell is an ugrep shim: an EMPTY -f file matches ALL, a BLANK line matches none, the reverse of /usr/bin/grep -> measure claims about other uids with /usr/bin/grep.
- (28) APPROVED a negative run under MY PATH (no sbin) and mutants shaped to the pattern -> run it under the PATH/uid it claims; mutants the pattern does NOT name.
- (29) RED, MINE: 'git worktree prune' on the SHARED repo dropped alive's private worktree (prune judges paths my uid cannot stat) -> never; probes in a standalone repo.
- (30) printf "$x" with x starting '---' is an option error -> printf '%b'.
- (31) an example in a word ('dpkg -l ...') never run, and wrong on Bazzite -> an example is a falsifier: assert its tool, name the OS.
- (32) 'NOT RUN: no route to encryption-town' written ON encryption-town -> read which host I am on before a NOT RUN.
- (33) a carry grep on 'timeout|124' missed the carrier worded 'timed out' (alive found :380) -> grep the rule's meaning in several wordings before 'not carried'.
- (34) a 'nothing reached this box' note read only refs/box + refs/cut, while posts/thought-master had moved (alive) -> a seat's work is read on its posts/ branch too.
## §5 Verification: `python3 extensions/agi/bin/links.py links` (6121/0 at L609)

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
  06:3xZ (one g5 leaf; c:a44d4d1acc68); TM wrote g5.57 on posts/thought-master (no cut yet). CLOSES at its land; word item 1.
- A30 OWNER 06:43Z + 06:5xZ 11-17 (away till 11-18): NETBOOT the lab (GO on P3's end state, SSD for models/data); meme-master
  leans on TM's team for paper + deck drafts (SM coordinates); designs reviewed 11-18, .47/.48 PAUSED (c:54cc08c95005).
  SM: no netboot unless the EXECUTE doc is gated 3/3 by 18:00Z AND the owner asks; else BANKED as NOT RUN. Lab seats stalled
  twice on carried mail (06:47-09:58Z, 10:07-11:57Z), belam woke them; the wake leaf is placed. OPEN until gated or banked.
