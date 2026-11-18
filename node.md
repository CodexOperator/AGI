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

## §0 State (11-18 · gen 78 seated 18:05Z 11-17 (claude-opus-5-5) · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER BACK 11-18 · L536-L631 checked · gen 78's mails ~/sp-scratch/g78 w1-)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town (hostname -s reads its own name: never put that literal in mail, the lint refuses it); ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; a seat's own work may sit on posts/<seat> before any cut: read that branch too |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES; belam rotated to gen XXII 16:5xZ |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING, WHERE it claims (PATH, uid, HOST), with mutants the pattern does NOT name (rename, delete, mode-only, stale-but-valid); else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; [correction] for my own miss; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> drop or trim to what is new |
| mail | dir ~/sp-scratch/g78, wN.txt (w1-w21 sent; next gen: NEW dir g79), ' TT ' in the header; `F=...; sed -i "1s/ TT / TT $(date -u +%m-%d) /" "$F" && sh ~/sp-scratch/g69/send.sh "$F"`; NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g78/watch.sh < /dev/null` (g78: no subject printed, arm B) by run_in_background ONLY, after counting live copies = 0: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` (its blob list is long: never `head` it; count blob == tip vs paths) + OWNER count + `python3 -I ~/sp-tools/bt-g49.py <L> <p1>` + H1 + anonymize.scan over `git diff L^1 L`; a RULES wrap W: G belam, W^2 == L, tree == merge-tree(W^1, L) |
| probes | `git archive <tree>` into /data/scratch/self-perpetuating/<x>, then `git init` + commit THERE (tests assert 'run inside a git repo'), GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 (the global ref-guard hook refuses refs/box), env -i, stderr kept, rc on the call's own line, `rm -rf "${D:?}"`; NEVER a worktree of the shared repo |
| scan | before a word on any tip: anonymize.scan over `git diff <base> <tip>` == [] (control: 12229bd7f4..d3d70328c7 reads ['home']) |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 DONE gen 78 (rows in §2 / git): my sweep L617; A2 (E) L-MODE L628 + wrap 0dbc21c590, INSTALLED by belam 23:5xZ (4/4 sha
   read-backs verified, w18); goal:g7.16.1.15 (blindness rule) L631; L617-L631 L-checked.
 OWED BY ME (each when it comes):
   g7.16.1.15 F1: SM's own agi-review line tip (both phrases 'never an OUTCOME of the run' + 'wake print'): RUN F1 on it (rc 0)
     and its control (one phrase out -> rc 1); read every widening named in the node's Target is in the line.
   GRID-CRON LEAF (3/3 at 20:58Z 11-17, SM places; nothing built): rule = skip if Split-Land not on the trunk AND G != trunk
     tip; else write iff G in trunk hist AND (B == trunk tip OR B not in hist); + invariant: every land gets its post-land
     split, a missed one ALARMS (trunk tip blob absent from the node's grid history). Word its cut by RUNNING on real grid.py:
     (a)-(i), (i-), (c-), the L618 window, both ways (my python model: w8-w10 in ~/sp-scratch/g78).
   lab-repack.sh NEXT TOUCH (SM's list, none a hold): (a) t0 after r=$? (alive: e1 cannot tell wait position); (b) de-dup key
     rc + list + stderr line 1; (c) after prune-packed, no LISTED id still loose (comm -12 = 0) else STOP (aio: a 0555 dir);
     (d) refuse WAIT_S <= 60 or print the comparison (alive). Word it by RUNNING the moved-step mutants, not only deleted ones.
   A2 L-crossing: count 3182 at 23:48Z 11-17 (487/h line -> ~03:3xZ 11-18); FIRE L = 'lab-repack.sh loose' BY HAND, alarm-only.
   WAKE LEAF goal:g7.16.1.14: 8 agi-boxwake@ units MASKED until the PROBE BUILD lands R3 (seeds read before T0, flag
     inode/mtime/bytes, alarm once per failure run, SETUP FAILED on empty getent, its unmask step).
   g5.57 item 1 (MEASURE commit): carry my inventory command WHOLE (suffix AND every file >= 100 MB, planted control).
   NETBOOT PHASE A on SM's window only; PHASE B the owner's ask (§6).
   BLINDNESS: my exposure is DECLARED (w11 w12 w16 w17): P1 outcome word, P2/P3 labels, L618/L621 headings. Arm B checks
     print ids, paths, counts only; the watcher prints no subject.
 PAUSED to the owner's pick (back 11-18): .47 network (L605) and .48 Quo (L604, mine).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py (2nd arg = L^1!); ~/sp-scratch/{g69/send.sh,g59/chk.py,g78/watch.sh,g68/meter.py,g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; earlier rows in git)
- L631 8a7d83c2ac SM goal:g7.16.1.15 (tip 18efdc26f4 = 3/3 re-cut 2; 1 A; scan [] HOME_PATH_RE 0; bt 0/1; grid == land; parent + 3 goal refs present at L)
- L630 259bc7bfd2 SM remix skills/agi-review +4 -1 (tip 8b5fed0b24; OWNER 0; scan [] HOME_PATH_RE 0; bt 0/1; grid build payload == land, read by mint)
- L629 009228c987 SM meme-master doc:draft-paper-v0 (tip 65677c6ca3; 1 M +6 -5; OWNER +1 -0 (no owner text changed); scan [] HOME_PATH_RE 0; bt 0/1; grid == land)
- L628 b07aee96af SM A2 (E) L-MODE (tip 9c5b2db2f6, RULES; 2 A 5 M, blobs == tip 7/7; scan [] HOME_PATH_RE 0; bt 0/7; OWNER -1 = 'uid 1000 = the owner of every pack' comment, not owner text; grid == land 3/3 by mint id); wrap 0dbc21c590 G belam, W^2 == L, tree == mt(W^1, L), W adds 0 paths
- L627 0742e5818a SM meme-master P1 VERDICT + RESULTS amend 3 (tip 85f071ab26; 1 M + 1 A; mechanical; OWNER removed 0; scan [] HOME_PATH_RE 0; bt 0/2; grid == land 2/2)
- L626 98de234d43 SM plasma TRAP SWEEP g1+2 (tip d1f248d497, PLAIN; agi-review +9 -0; OWNER 0; scan []; bt 0/1; grid v87 payload == land (alive skipped that row: w13 22:36:21Z))
- L625 210f66826f SM meme-master doc:draft-paper-v0 refresh (tip 77f6780afa; 1 M +4 -4; checked BLIND, no text printed; OWNER removed 0; scan []; bt 0/1; grid == land)
- L624 89918241f2 SM meme-master P3 (tip 73146637f9; 1 M experiment + 1 A verdict; ARM B: checked by shas/paths/counts/blob ids only; OWNER removed 0; scan []; bt 0/2; parents present; grid == land 2/2)
- L623 4840dde124 SM meme-master P2 VERDICT (tip ab39c53a29; 1 M experiment + 1 A verdict:paper-numbers-rederive, parents present; scan []; bt 0/2; grid heads == land 2/2)
- L622 d578e0fb00 SM thought-master P2 RESULTS (tip d29a346378; 1 M experiment:paper-numbers-rederive-e1; scan []; bt 0/1; grid v2 == land)
- L621 e6223ee4d7 SM meme-master L608 AMEND re-cut 1 (tip 95e168cf56; 2 M experiment nodes; scan []; bt 0/2; GRID REGRESSION cron 20:01:46Z, SM [red] 20:36Z; healed by belam 20:45:07Z, READ 2/2)
- L620 73d848de43 SM alive TRAP SWEEP g93-95 (tip 3ef2165468, PLAIN; agi-review :100 + :221 clauses, new :223; 1 M; scan []; bt 0/1)
- L619 9a158df6fc SM aio TRAP SWEEP g84-86 (tip 62bd05bbcb, PLAIN; agi-review :218 clause; 1 M; scan []; bt 0/1; my L617 line still last)
- L618 9e961e6600 SM meme-master L608's experiments re-cut 5 (tip f73cdeb8dc; 3 A experiment nodes, parents = their hypotheses, present; OWNER 1 = a rubric reference, not verbatim; scan []; bt 0/3)
- L617 ba45a63dc6 SM MY TRAP SWEEP g78 (tip 8dfbbd5113, PLAIN; agi-review +1; p2 == tip, tree == mt, blob == tip, OWNER 0, scan [], bt 0/1 RE-RUN with p1)
- L616 c93e89e4e7 SM CLOSE goal:g7.16.1.11.46.29.4 for DG3 (tip d21711de35; status complete; H1 2 -> 1; scan [])
- L615 ca4a7cf900 belam A2 TRACKED RE-CUT 4 (tip 7fc1d0a322, RULES; 12 A, 12/12 == tip; 755/644); wrap ac129bb837 W^2 == L, tree == mt
- L614 823db2d3dd belam g7.16.1.14 AMEND 1 RE-CUT 2 (tip 4b475f833a) · L613 691119f29e TM netboot plan RE-CUT 2 (tip 69d8880b22)
- L612 16342c7dc3 TM g5.57 ORCHESTRA (tip a51981c1a6; OWNER 1 = its verbatim block) · L606 e649d70c78 TM P3 RE-CUT 4 (tip 082b9086bb; OWNER 2)
- L611 7ff4fde110 alive TRAP SWEEP g92 (tip 8938a1d6ae) · L610 8cf17bd68d belam WAKE LEAF (tip bd91de1aca) · L608 eb2c41491b paper route pointer
- L536-L609: rows in git (this card's versions to 11-17 18:0xZ).

## 🔴 Where it stops
gen 78 15:18Z 11-18: NETBOOT PHASE A: SM window GRANTED 15:2xZ (owner 15:1xZ: 'reboot it back into NetBoot'), conditional on council 3/3 + belam's no-player read; w22 15:17:15Z = APPROVE (plan == L613 blob 29682aece6, 0 commits since); w23 15:19:46Z = APPROVE of SM's AMENDED terms (aio MODIFY: A0 GPU-job-live read; A1 route to NAS; A2 SSD first, NAS leg under a stated --bwlimit unless LAN; failed names only in the target manifest). alive pending. PHASE B only on the owner's own ask with A1 + A4 green. Owed: read belam's per-step read-backs (A0 boot_id START, A1 five reads, A2 floor + read errors, A3, A4 END == START) by counts; SM's agi-review F1 tip; the grid-cron leaf cut. Meter f 0.421 at 14:03Z (past 0.41: no multi-ref act).
NEXT: (1) on the watcher's line: `box n`, box read; answer what SM asks about w1 (the sweep land, the E1 line). (2) a land of sweep-g78 -> L-check.
(3) +6 h lap ~22:53Z: read row 6 vs loose for L. (4) re-arm the watcher after counting live copies = 0.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write; a reset clears /tmp.

## §4 Traps (gen 76 + 77's (27)-(40) SWEPT 18:09Z: (32)+(34) -> agi-review via sweep-g78; the other 9 dropped as carried, cites in w1)
- (42) w1 + the sweep message said /usr/bin/grep -c printed '0'; it printed NOTHING, rc 1 (aio RE-RAN) -> quote what the output line SHOWS, never what -c should print.
- (43) bt-g49.py run with a PATH as its 2nd arg read '0/150' on L617 (git took it as a pathspec), errored on L618 -> its 2nd arg is L^1, `$(git rev-parse L^1)`.
- (44) w5's header reads 'TT 11-17 11-17': the date was typed in the heredoc AND sed-added -> type ' TT ' only; the sed adds the date.
- (45) arm B land checks printed experiment text (L618 titles + an 'owner' grep line; L621 diff heads) while I am a possible scorer -> on arm B print counts, shas, blob ids only; the parent read prints ids, never title/body.
- (46) w14 called L626 'live for P1' without reading whether P1's judging was still open (it closed 22:17Z) -> before a harm claim about a running process, read its current state (SM's last [decision]/[result] on it), stamp it.
- (47) w15 read item (4) 'sleep BETWEEN' in the code but let e1's gap row stand as its test; it times from t0 BEFORE pack-objects (alive's mutant: sleep moved first stays ok) -> for each required ORDER, run the mutant that moves the step, not only the one that deletes it.
- (48) called scan() blind to /var/lib/agi/<post>/ off a control with a made-up post 'zz' (reads []); with a real post it reads ['home'] -> a control's NAME must be one the pattern can match (a real post, assembled), or it proves nothing.
- (49) ran links.py for a land on a ~/t HEAD that did not hold the land -> links.py reads the CHECKOUT; for a land, read its refs at L by git show, or say links NOT RUN for it.
- (41) w1 went out without the mail row's date sed (the header reads '18:09:02Z' with no '11-17') -> run the §0 mail row's sed first; send.sh does not add the date.
## §5 Verification: `python3 extensions/agi/bin/links.py links` (6136/0 at L617, RAN gen 78 18:4xZ on a HEAD holding L617; 287 retired-goal refs are info lines, not damage)

## §6 BANKED (owner)
- CARDS DO NOT REACH THE TRUNK: MAIN's doc:card-<post> is whatever last landed (SM 14:49Z 11-06).
- C2 one shared Console workspace across 3 lanes until the owner says it is the intent.
- .44.8: no agi.sh start until the owner rules R2 + R3 · G1a removal of the old refs/grid/local-maxxing namespace: owner act.
- P8: sonnet directors at effort max vs high, and ultracode for sonnet: the owner's call via belam.
- .46.37 host half: restart AT the move vs next start; move back after the limit clears; hub-down move; a third account.
- NETBOOT PHASE B (and any PC power-state change): the owner's own ask 11-18 (L613; c:54cc08c95005).

## §7 ATOMS (inbound owner/parent asks; one row per atom; closed when placed in a leaf, idea, decision or out; open > 1 lap = red)
- A1-A27: CLOSED (rows in git, this card's versions to 11-16).
- A28 OWNER 11-15 P1-P10: CLOSED 15:43Z 11-17 at L606 (P3 = goal:g5.56 RE-CUT 4); P4 + P8 stay banked (§6).
- A29 OWNER 06:28Z 11-17 ORCHESTRA line: CLOSED as placed, L612 goal:g5.57; its item 1 (the council's measure) owed in §1.
- A30 OWNER 06:43Z 11-17 NETBOOT: CLOSED as placed: P3 L606 + doc:pc-netboot-plan L613 (PHASE A on SM's window, PHASE B the
  owner's ask, §6). The lab stalls on carried mail: goal:g7.16.1.14 (L610, L614), loops masked, belam's hand interim.
