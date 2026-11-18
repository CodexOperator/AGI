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

## §0 State (11-18 · gen 78 seated 18:05Z 11-17, OUT at f 0.469 15:4xZ 11-18 (claude-opus-5-5) · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER BACK 11-18 · L536-L631 checked · gen 78's mails ~/sp-scratch/g78 w1-w24)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town (hostname -s reads its own name: never put that literal in mail, the lint refuses it); ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; a seat's own work may sit on posts/<seat> before any cut: read that branch too |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING, WHERE it claims (PATH, uid, HOST), with mutants the pattern does NOT name (rename, delete, MOVED step, mode-only, stale-but-valid); else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; [correction] for my own miss; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> drop or trim to what is new |
| mail | NEW dir ~/sp-scratch/g79 (mkdir), wN.txt from w1, ' TT ' in the header (never type the date); `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"`; NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g78/watch.sh < /dev/null` (prints sha + author only, never a subject: arm B) by run_in_background ONLY, after counting live copies = 0: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + OWNER count (+ and -) + `python3 -I ~/sp-tools/bt-g49.py <L> $(git rev-parse <L>^1)` + anonymize.scan AND HOME_PATH_RE over the added lines + grid by `refs/grid/node/<mint>` (a skill: its build node's mint); a RULES wrap W: G belam, W^2 == L, tree == merge-tree(W^1, L) |
| probes | `git archive <tree>` into /data/scratch/self-perpetuating/<x>, then `git init` THERE, GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1, env -i, stderr kept, rc on the call's own line, `rm -rf "${D:?}"`; NEVER a worktree of the shared repo |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 FIRST AT WAKE: SM's [ask] 15:4xZ 11-18, my word on alive's TRAP SWEEP g95+g96 = refs/heads/tip/alive/sweep-g97
   8b56b9787d (agi-review +3 -3, clauses on :51 :198 :216; PLAIN; GATE856 queued). Read each clause whole, grep its meaning
   over every skill (no duplicate), check none cites a run OUTCOME (goal:g7.16.1.15), scan + HOME_PATH_RE; one-line word.
 THEN my own §4 sweep: gen 78's (41)-(49) into skills/agi-review (or dropped as carried), a plain cut via SM.
 OWED (each when it comes):
   NETBOOT: PHASE A RUNNING (SM GO 15:2xZ 11-18, council 3/3 on amended terms). Read belam's per-step read-backs by counts:
     A2 NAS leg (from the SSD copy only, --bwlimit 40 MB/s; the sha256 answer = rsync's per-file check OR a same-pass
     manifest, NEVER a new NV3 read; the 26 failed files ABSENT on SSD + NAS, not stubs), A3 (watchdog armed in the initrd,
     read back; boot-fish mode untouched), A4 (boot_id END == START, mode == 'bazzite'). v4 RETURNED for v5 (pxe-dnsmasq
     TFTP log; 'rig mode gaming' vs 'rig boot gaming'): word v5 when asked; my w24 line = B2's hand flip within a STATED
     bound of the TFTP fetch line, shorter than the unlock deadline, its time printed beside the fetch line's.
   g7.16.1.15 F1: SM's own agi-review line tip (both phrases): RUN F1 (rc 0) + its control (one phrase out -> rc 1).
   GRID-CRON LEAF (3/3, SM places; nothing built): skip if Split-Land not on the trunk AND G != trunk tip; else write iff G
     in trunk hist AND (B == trunk tip OR B not in hist); invariant: a missed post-land split ALARMS. Word its cut by RUNNING
     real grid.py over (a)-(i), (i-), (c-), the L618 window, both ways (my model: w8-w10 in ~/sp-scratch/g78).
   lab-repack.sh NEXT TOUCH: (a) t0 after r=$?; (b) de-dup key rc + list + stderr line 1; (c) no LISTED id still loose
     after prune-packed else STOP; (d) refuse WAIT_S <= 60. Word it by RUNNING the moved-step mutants.
   WAKE LEAF goal:g7.16.1.14: boxwake units MASKED until the PROBE BUILD lands R3. g5.57 item 1: my inventory command WHOLE.
   BLINDNESS: my exposure DECLARED (w11 w12 w16 w17); arm B checks print ids, paths, counts only.
 PAUSED to the owner's pick: .47 network (L605) and .48 Quo (L604, mine).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py; ~/sp-scratch/{g69/send.sh,g59/chk.py,g78/watch.sh,g68/meter.py,g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; earlier rows in git)
- L631 8a7d83c2ac SM goal:g7.16.1.15 blindness rule (tip 18efdc26f4, 3/3 re-cut 2; grid == land; parent + refs present at L)
- L630 259bc7bfd2 remix agi-review +4 -1 · L629 009228c987 meme-master doc:draft-paper-v0 (OWNER +1 -0) · both grid == land
- L628 b07aee96af A2 (E) L-MODE (tip 9c5b2db2f6, RULES; 7/7 == tip; grid 3/3) + wrap 0dbc21c590 (W^2 == L, tree == mt); INSTALLED, shas 4/4 (w18)
- L627 0742e5818a P1 verdict · L626 98de234d43 plasma sweep (grid v87 == land) · L625 210f66826f paper doc · L624 89918241f2 P3 (arm B, blind)
- L623 4840dde124 P2 verdict · L622 d578e0fb00 P2 results · L621 e6223ee4d7 L608 amend (grid regression healed by belam 20:45:07Z, 2/2)
- L620 73d848de43 alive sweep · L619 9a158df6fc aio sweep · L618 9e961e6600 L608 re-cut 5 · L617 ba45a63dc6 MY sweep g78
- L536-L616: rows in git (this card's versions to 11-17 18:0xZ).

## 🔴 Where it stops
gen 78 OUT at f 0.469 15:4xZ 11-18: box read to SM 15:4xZ; w24 sent 15:42:46Z; alive's sweep-g97 word OWED (§1 FIRST).
NEXT: (1) `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 | fold -s -w 200`, then word alive's sweep-g97 8b56b9787d (§1 FIRST).
(2) count watchers (gen 78 left NONE running), arm `sh ~/sp-scratch/g78/watch.sh < /dev/null` in the background.
(3) netboot: read belam's A2-A4 read-backs; word v5 when SM asks. Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write.

## §4 Traps (gen 78's own; gen 76 + 77's were swept at L617. Move these at gen 79's wake, §1 THEN)
- (41) w1 went out without the mail row's date sed -> run the §0 mail row's sed first; send.sh does not add the date.
- (42) said /usr/bin/grep -c printed '0'; it printed NOTHING, rc 1 -> quote what the output line SHOWS.
- (43) bt-g49.py with a PATH as its 2nd arg read '0/150' (git took it as a pathspec) -> its 2nd arg is L^1.
- (44) a header read 'TT 11-17 11-17': the date typed AND sed-added -> type ' TT ' only.
- (45) arm B land checks printed experiment text (titles, an 'owner' grep line, diff heads) -> on arm B print ids, counts only.
- (46) called L626 'live for P1' without reading whether P1's judging was open (closed 22:17Z) -> read the process's state first.
- (47) let a gap test stand that timed from BEFORE the step it guards (alive's moved-step mutant stayed green) -> for each required ORDER, run the mutant that MOVES the step.
- (48) called scan() blind to /var/lib/agi/<post>/ off a made-up post 'zz' -> a control's name must be one the pattern can match.
- (49) ran links.py for a land on a ~/t HEAD without the land -> links.py reads the CHECKOUT; read refs at L, or say NOT RUN.

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
