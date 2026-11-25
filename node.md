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

## §0 State (11-25 · gen 80 seated 18:10Z 11-22, OUT at f 0.470 22:44Z 11-25 (claude-opus-5-5) · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER BACK 11-18 · L536-L651 checked · gen 80's mails ~/sp-scratch/g80 w1-w16; w1 unsent, overtaken)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town (hostname -s reads its own name: never put that literal in mail, the lint refuses it); ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; a seat's own work may sit on posts/<seat> before any cut: read that branch too |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING, WHERE it claims (PATH, uid, HOST), with mutants the pattern does NOT name (rename, delete, MOVED step, mode-only, stale-but-valid); a clause word reads its WHOLE host line against the live tool (agi-review :138); else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; [correction] for my own miss; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> drop or trim to what is new |
| mail | NEW dir ~/sp-scratch/g81 (mkdir), wN.txt from w1, ' TT ' in the header, NO date typed; `sh ~/sp-scratch/g69/send.sh "$F"` (its stamp.sh adds the date once, refuses a typed or doubled one); NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g78/watch.sh < /dev/null` (prints sha + author only, never a subject: arm B) by run_in_background ONLY, after counting live copies = 0: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + OWNER count (+ and -, and the word diff) + `python3 -I ~/sp-tools/bt-g49.py <L> $(git rev-parse <L>^1)` + anonymize.scan AND HOME_PATH_RE over the added lines + grid by `refs/grid/node/<mint>` (a skill: its build node's mint); a RULES wrap W: G belam, W^2 == L, tree == merge-tree(W^1, L) |
| probes | `git archive <tree>` into /data/scratch/self-perpetuating/<x>, then `git init` THERE, GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1, env -i, stderr kept, rc on the call's own line, `rm -rf "${D:?}"`; NEVER a worktree of the shared repo |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act; idle watch ticks alone cost ~0.06 a day |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 FIRST AT WAKE: am I still MUTE? `python3 -I ~/sp-scratch/g59/chk.py <any wN.txt> < /dev/null | tail -1` must read
   VERDICT CLEAN. On 11-25 it read NOT CLEAN on plain text: anonymize post_homes reads home-unread (9 s4 accounts
   under the agi root, outside group agi, born 04:44Z 11-25; aio [note] 18:40:24Z 11-25), so scan() returns
   home-unread on EVERY text. Fix is the owner's/belam's (aio's options: s4 accounts join group agi; post_homes
   learns the s4 tree; the s4 tree moves off the agi root). Do NOT bypass the lint; read the box, word nothing until
   it reads CLEAN, and say so in a [word] the moment it does.
 DONE gen 80: L648 card-scan leaf (my class amend + Invariant fix); L649 MY TRAP SWEEP g79; gate-tools objscan2 +
   gsend2 3/3 per file and SWAPPED LIVE (my trailer MODIFY taken at r4); L650 + wrap (agi-master-gate :372 :390 :407,
   my :390 MODIFY); L651 alive's sweep g98 (agi-review :138 carries my L650 whole-line slip). All land-checked here.
 IDLE 20:05Z 11-22 -> 22:44Z 11-25: no mail but aio's 11-25 note; trunk moved by belam's board + card only.
 OWED (each when it comes):
   NETBOOT PHASE B = the owner's ask. BANKED, one plan touch + initrd rebuild, both or neither: my software fallback
     ('reboot -f' at DEADLINE+60 unless the hand-off kills it: gate 3 fails OPEN if modprobe fails) + alive's watchdog0
     read before the passphrase (needs a forced-command WRAPPER, aio). Fire drill B3a, bazzite-install set-aside: owner's.
   GRID-CRON LEAF goal:g7.16.1.11.46.30.1 (MINTED L647, belam): next = belam's BUILD: RUN real grid.py on it, the 14
     cases + (e-) + trailer-less lane + the 'cron: ' prefix both ways.
   CARD-SCAN LEAF goal:g7.16.1.11.46.30.2 (MINTED L648, belam): BUILD owed; its F1 names home-unread with a case, and
     today every text reads home-unread: the build must not refuse every card on that host fact.
   lab-repack.sh NEXT TOUCH: t0 after r=$?; de-dup key rc; no LISTED id loose after prune-packed; WAIT_S > 60; moved-step mutants.
   WAKE LEAF goal:g7.16.1.14: boxwake units MASKED until R3. g5.57 item 1: my inventory command WHOLE.
   HUB: decided onto hub A (belam alarm 22:27Z 11-18), pending belam's host step: no act of mine.
   BLINDNESS: exposure DECLARED (g78 w11 w12 w16 w17); arm B checks print ids, paths, counts only.
 PAUSED to the owner's pick: .47 network (L605) and .48 Quo (L604, mine).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/{g69/send.sh + stamp.sh, g59/chk.py, g78/watch.sh,
   g68/meter.py, g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0, box tokens 0, grid == land unless named)
- L651 7a77eee7af alive's TRAP SWEEP g98 r1 (tip 276ed5b45c; agi-review :138; OWNER 0/0; bt 0/1; grid v95 == land)
- L650 a951259195 + wrap c4e8aedf0d agi-master-gate objscan2 clauses (tip bcd6e3510e r2; 1 M; OWNER 0/0; bt 0/1; W^2 == L,
  tree == mt; grid v52 payload == land)
- L649 e017e2291e MY TRAP SWEEP gen 79 r1 (tip f54bfcebfe; 1 M agi-review; OWNER +2 -2 = carried prefixes, 0 added words; bt 0/1; grid v94 payload == land)
- L648 b253fc02a8 goal:g7.16.1.11.46.30.2 card-scan leaf MINT (tip fc5f9158db r3; 1 A; OWNER 0; bt 0/1; grid == land)
- L647 476eb24b54 goal:g7.16.1.11.46.30.1 grid-cron leaf MINT (tip 8b7fd6f16e; 1 A; OWNER 0; bt 0/1; grid == land)
- L646 and earlier: rows in git (this card's versions).

## 🔴 Where it stops
gen 80 OUT at f 0.470 22:44Z 11-25, idle since L651, MUTE: every anonymize scan holds on home-unread, so my send lint refuses.
Box empty after aio's 18:40:24Z note; trunk 6c646cc618 (board only); nothing of mine in flight; no watcher left running.
NEXT: (1) the chk.py line in §1 FIRST; (2) `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 | fold -s -w 200`;
(3) count watchers (= 0), arm `sh ~/sp-scratch/g78/watch.sh < /dev/null` by run_in_background;
(4) on a land: `sh ~/sp-tools/lcheck.sh <L> <tip>` + grid by exact mint + bt-g49.py.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write.

## §4 Traps (gen 80's own; move at gen 81's wake into skills/agi-review or drop)
- a base sha typed in an [ask] from memory while the trunk had moved one card commit (w4 -> w5) -> copy the parent from `git log -1 --format=%P <tip>`.
- a string-prefix check by `head -c $(wc -c)` counts sed's newline: read 'differ' on a true prefix -> compare in python.
- lcheck's OWNER count reads a long line's carried PREFIX as added (L649: +2 -2, 0 by word diff) -> read +/- together and the word diff.

## §5 Verification: `python3 extensions/agi/bin/links.py links` (6148/0 per belam's [landed] at L651; not re-run here)

## §6 BANKED (owner)
- HOME-UNREAD (11-25): 9 s4 accounts under the agi root outside group agi make every anonymize scan hold; every seat's send
  gate, cut and land privacy step is affected; aio banked options a/b/c (§1). The owner's season-4 STOP (g5.4.4) may decide.
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act.
- P8: sonnet directors at effort max vs high, and ultracode for sonnet: the owner's call via belam.
- .46.37 host half: restart AT the move vs next start; move back after the limit clears; hub-down move; a third account.
- NETBOOT PHASE B (any PC power-state change): the owner's own ask, with A1 + A3 watchdog + A4 green, on plan v5 (v3/v4 cannot run it).
- Pushed history carrying belam's card home paths (SM [red] 23:2xZ 11-17): whether more than the scrub is needed is the owner's.

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A27: CLOSED (rows in git, this card's versions to 11-16).
- A28 OWNER 11-15 P1-P10: CLOSED 15:43Z 11-17 at L606 (P3 = goal:g5.56 RE-CUT 4); P4 + P8 stay banked (§6).
- A29 OWNER 06:28Z 11-17 ORCHESTRA line: CLOSED as placed, L612 goal:g5.57; its item 1 (the council's measure) owed in §1.
- A30 OWNER 06:43Z 11-17 NETBOOT: CLOSED as placed: P3 L606 + doc:pc-netboot-plan L613 (PHASE A on SM's window, PHASE B the
  owner's ask, §6). The lab stalls on carried mail: goal:g7.16.1.14 (L610, L614), loops masked, belam's hand interim.
- A31 OWNER 15:1xZ 11-18 'reboot it back into NetBoot': CLOSED as placed: SM's decision 15:2xZ (PHASE A now, council 3/3;
  PHASE B on his own ask once A1 + A3 + A4 read green, told to him through belam's pane; plan v5 owed by thought-master).
