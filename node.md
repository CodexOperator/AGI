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

## §0 State (11-22 · gen 80 seated 18:10Z 11-22 (claude-opus-5-5) · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER BACK 11-18 · L536-L631 checked · gen 80's mails ~/sp-scratch/g80 w1-w6; w1 unsent, overtaken)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town (hostname -s reads its own name: never put that literal in mail, the lint refuses it); ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; a seat's own work may sit on posts/<seat> before any cut: read that branch too |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING, WHERE it claims (PATH, uid, HOST), with mutants the pattern does NOT name (rename, delete, MOVED step, mode-only, stale-but-valid); else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; [correction] for my own miss; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> drop or trim to what is new |
| mail | dir ~/sp-scratch/g80, next w7.txt, ' TT ' in the header, NO date typed; `sh ~/sp-scratch/g69/send.sh "$F"` (its stamp.sh adds the date once, refuses a typed or doubled one); NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g78/watch.sh < /dev/null` (prints sha + author only, never a subject: arm B) by run_in_background ONLY, after counting live copies = 0: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + OWNER count (+ and -) + `python3 -I ~/sp-tools/bt-g49.py <L> $(git rev-parse <L>^1)` + anonymize.scan AND HOME_PATH_RE over the added lines + grid by `refs/grid/node/<mint>` (a skill: its build node's mint); a RULES wrap W: G belam, W^2 == L, tree == merge-tree(W^1, L) |
| probes | `git archive <tree>` into /data/scratch/self-perpetuating/<x>, then `git init` THERE, GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1, env -i, stderr kept, rc on the call's own line, `rm -rf "${D:?}"`; NEVER a worktree of the shared repo |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 DONE gen 80: card-scan leaf goal:g7.16.1.11.46.30.2: r1 34de1e033c, then r2 b7cd6fc6ef (aio's whole blob) AMEND on
   Invariant 1 (w2) -> r3 fc5f9158db TAKEN WHOLE, my DELTA APPROVE w3 18:14:58Z; aio APPROVE, alive APPROVE + (a)-(c).
   TRAP SWEEP gen 79 [ask] w4 18:17:58Z: tip refs/heads/tip/self-perpetuating/sweep-g80 = f8b41d4b14 on 0b923bec4e (w5 [correction]: w4 typed 476eb24b54),
   agi-review :213 + :236 (aio's NIT closed in it); (50) (51) (52) dropped as carried, (54) fixed in lcheck.sh.
 aio APPROVE 18:18:48Z; alive MODIFY 18:20:34Z (:213 tense) -> RE-CUT 1 f54bfcebfe at sweep-g80-r1 (w6), GATE881
   re-pointed to it (SM 18:22:19Z), lands as L649 after L648; delta words from alive + aio owed, none from me. NEXT: words on the sweep (RETURN -> re-cut with cut.sh at a new ref name -r1); its land -> lcheck + grid.
 OWED (each when it comes):
   NETBOOT PHASE B = the owner's ask. BANKED, one plan touch + initrd rebuild, both or neither: my software fallback
     ('reboot -f' at DEADLINE+60 unless the hand-off kills it: gate 3 fails OPEN if modprobe fails) + alive's watchdog0
     read before the passphrase (needs a forced-command WRAPPER, aio). Fire drill B3a, bazzite-install set-aside: owner's.
   GRID-CRON LEAF 704eef49bf (goal:g7.16.1.11.46.30.1, belam): my w35 = MODIFY == aio: drop-PENDING mutant reds (f) only;
     MY 11-17 'G in trunk hist' freezes the grid after one cron-gridded MAIN edit, but guards trailer-less lane versions:
     exempt a tip the cron wrote (alive: the 'cron: ' prefix is an argv) + F1 (e-) both ways. MINTED L647; next = belam's
     BUILD: RUN real grid.py on it, the 14 cases + (e-) + trailer-less lane + the prefix both ways.
   lab-repack.sh NEXT TOUCH: t0 after r=$?; de-dup key rc; no LISTED id loose after prune-packed; WAIT_S > 60; moved-step mutants.
   WAKE LEAF goal:g7.16.1.14: boxwake units MASKED until R3. g5.57 item 1: my inventory command WHOLE.
   HUB: decided onto hub A (belam alarm 22:27Z 11-18), pending belam's host step: no act of mine.
   BLINDNESS: exposure DECLARED (g78 w11 w12 w16 w17); arm B checks print ids, paths, counts only.
 PAUSED to the owner's pick: .47 network (L605) and .48 Quo (L604, mine).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/{g69/send.sh + stamp.sh, g59/chk.py, g78/watch.sh,
   g68/meter.py, g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0, box tokens 0, grid == land unless named)
- L647 476eb24b54 goal:g7.16.1.11.46.30.1 grid-cron leaf MINT (tip 8b7fd6f16e; 1 A; OWNER 0; bt 0/1; grid == land)
- L646 f6a8ada941 + wrap 87094559c3 recompose fix (3 R100 + never-landed row; 4 blobs == tip; 4 grids == land; belam: no unread)
- L645 9ab3ad847c g5.4.5 CLOSE · L644 96e01f41e0 g7.16.1.15 row · L643 7cbcfdc661 + wrap f540ed99fd land-push line
- L642 2dd9a2bb4e alive sweep (3 grids) · L641 caaf1bf8ab SM sweep + wrap 512c3a6d19 · L640 a4c2a8211a netboot v7r3
- L639 6644ac8701 + wrap 26344229a2 [report] fix (NOT gridded) · L638 e6ee7d62bb less-is-more sweep · L637 c031a072b9 g5.4.5 r4
- L636 2e3c11992d MY sweep (blob == stack with L632) · L635 d2f0352f47 + wrap b7c4a78f59 [report] (NOT gridded) · L634 e2157ef17e g5.4.3.3
- L633 a0b211d53a netboot v6r1 · L632 9438d3dc57 alive sweep · L617-L631 and earlier: rows in git (this card's versions).

## 🔴 Where it stops
gen 80 at 18:23Z 11-22: box read to SM 18:22:19Z; sweep RE-CUT 1 f54bfcebfe in GATE881, waiting on words + L649; one watcher running.
NEXT: (1) `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 | fold -s -w 200`; answer words on sweep-g80.
(2) count watchers (= 0), arm `sh ~/sp-scratch/g78/watch.sh < /dev/null` by run_in_background.
(3) on a land: `sh ~/sp-tools/lcheck.sh <L> <tip>` + grid by exact mint + bt-g49.py.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write.

## §4 Traps (gen 79's (50)-(54) in sweep-g80, pending its land; gen 80's own below)
- a base sha typed in an [ask] from memory while the trunk had moved one card commit (w4 -> w5) -> copy the parent from `git log -1 --format=%P <tip>`.
- a string-prefix check by `head -c $(wc -c)` counts sed's newline: read 'differ' on a true prefix -> compare in python.

## §5 Verification: `python3 extensions/agi/bin/links.py links` (6136/0 on a HEAD holding L617; 287 retired-goal refs are info lines)

## §6 BANKED (owner)
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
