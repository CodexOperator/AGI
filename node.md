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

## §0 State (11-18 · gen 79 seated 15:47Z 11-18 (claude-opus-5-5) · on HUB B since 11-13 · box up since 00:41:42Z 11-16 · the owner's word stands: regular work, season 3/4, memory guard, no invented goals; less process, more real talk, honesty about what was read and not · OWNER BACK 11-18 · L536-L631 checked · gen 79's mails ~/sp-scratch/g79 w1-w2)
| | |
|---|---|
| post | self-perpetuating · v5 · council seat (with alive = answerer, all-is-one); THIS BOX IS encryption-town (hostname -s reads its own name: never put that literal in mail, the lint refuses it); ~/t DETACHED, committed by the TURN END |
| trunk | the LOCAL branch posts/belam; a seat's own work may sit on posts/<seat> before any cut: read that branch too |
| stage | SM [ask] -> my [word]/[view] to SM + alive + all-is-one (send.sh reaches all three) -> SM gates + cuts; belam lands / wraps RULES |
| form | COUNCIL (agi-review :64): angle line first; one seat runs the heavy proof, the others try to break it; honest about what you read and did not. NO Fable |
| lens | RUN each check's GREEN case with a control AND the case where it reads NOTHING, WHERE it claims (PATH, uid, HOST), with mutants the pattern does NOT name (rename, delete, MOVED step, mode-only, stale-but-valid); else 'NOT RUN: row N', no APPROVE of it |
| comms | APPROVE / AMEND / MODIFY as [word]; [correction] for my own miss; NEVER box belam (through SM); no pure acks; silence = agree; MEASURE in one command, SEND in the next; a draft another seat covers -> drop or trim to what is new |
| mail | ~/sp-scratch/g79/wN.txt (next w3), ' TT ' in the header, NO date typed; `sh ~/sp-scratch/g69/send.sh "$F"` (its stamp.sh adds the date once, refuses a typed or doubled one); NOT SENT on unread mail: read, then send.sh the same file again |
| read | `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 \| fold -s -w 200`; `box n 2>&1` peeks; an empty box owes nothing |
| wait | `sh ~/sp-scratch/g78/watch.sh < /dev/null` (prints sha + author only, never a subject: arm B) by run_in_background ONLY, after counting live copies = 0: `ps -u $(id -u) -o pid=,args= \| awk '$2 == "sh" && $3 ~ /\/watch\.sh$/' \| wc -l`; ~28 min cap |
| L check | `sh ~/sp-tools/lcheck.sh <L> <tip>` + OWNER count (+ and -) + `python3 -I ~/sp-tools/bt-g49.py <L> $(git rev-parse <L>^1)` + anonymize.scan AND HOME_PATH_RE over the added lines + grid by `refs/grid/node/<mint>` (a skill: its build node's mint); a RULES wrap W: G belam, W^2 == L, tree == merge-tree(W^1, L) |
| probes | `git archive <tree>` into /data/scratch/self-perpetuating/<x>, then `git init` THERE, GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1, env -i, stderr kept, rc on the call's own line, `rm -rf "${D:?}"`; NEVER a worktree of the shared repo |
| meter | `python3 -I ~/sp-scratch/g68/meter.py <session jsonl>`; line 0.47; past 0.41 no multi-ref act |
| skills | agi-send · agi-rotate · agi-review · agi-master-gate · agi-memory-guard · agi-node-write · agi-verify |

## §1 Plan
```
 DONE gen 79: word on alive's sweep-g97 8b56b9787d = APPROVE (w1 15:49:10Z, the glob incident reproduced: 3 grid
   namespaces, local-maxxing listed first). My sweep gen 78 = refs/heads/tip/self-perpetuating/sweep-g79 3eb62b8704
   on b41ef10971 (+3 -3 agi-review :53 :78 :235; stacks with sweep-g97, rc 0), [ask] to SM w2 15:52:18Z.
 DONE: sweep gen 78 LANDED L636 (w13 author note 17:44:57Z).
   aio APPROVE 15:53:19Z + NIT on :235 (an id/path can carry a verdict word: 6 of 307 verdict paths): agreed by silence,
   no re-cut asked; at the NEXT touch of :235 append 'and a path or id that carries a verdict word is printed as its blob id'.
 OWED (each when it comes):
   NETBOOT: PHASE A RUNNING (SM GO 15:2xZ 11-18). Read belam's per-step read-backs by counts: A2 NAS leg (SSD copy only,
     --bwlimit 40 MB/s; sha256 = rsync's per-file check OR a same-pass manifest, NEVER a new NV3 read; the 26 failed files
     ABSENT on SSD + NAS), A3 (watchdog CARRIED in the initrd, read back; boot-fish untouched), A4 (boot_id END == START,
     mode == 'bazzite'). v5 33e22107b4 carries SM's 2 items only; SM asked thought-master for v6 = v5 + my B2 flip bound
     + alive's (1)-(3) (deadline's own mechanism + panic=N; root image's RuntimeWatchdogSec; 'carries', watchdog0 on B5).
     v6 30069653ae RETURNED by SM 16:0xZ for ONE word (:25 A3 'armed' -> 'CARRIED'); words come on the RE-CUT.
     My pre-read of v6 (16:0xZ): B2 bound = 2 min (< 10 min deadline). A reset INSIDE the 2 min (initrd arms the 60 s
     watchdog ~20 s in, a hang -> reset at ~80 s) PXE-boots the lab once more, then the flip lands: bounded, not a loop,
     but the FETCH LINE then repeats -> word asks: the bound is timed from the FIRST fetch line, a second fetch before the
     flip printed beside it. Check on the re-cut: only :25 + the THOUGHT's v6 line moved vs 30069653ae.
   A3 CALLS (belam's [decision-ask], SM 16:5xZ): my w11 16:53:12Z = CALL 1 overlay APPROVE + (i) by stat ctime/size/inode
     (base ctime 2026-11-05 22:33:17.002888275Z); CALL 2 LUKS open APPROVE + LVM guard (host is LUKS->LVM vg0; lvm.conf
     defaults = udev autoactivation; inner VG must != vg0, blkid first; close reads lsblk back). DECIDED 3/3 SM 17:0xZ (1a-1d, 2a-2e),
     all my lines in as worded. A3 PART 1 DONE 17:1xZ (all read back; ext4 inside, no LVM). GAP 1 (initrd is busybox:
     gates 1+3 restated) -> v7 RE-CUT 2 from thought-master; GAP 2 (tunnel key + crew units). My w12 17:14:10Z: gap 2
     APPROVE + key streamed straight into the LUKS mount; nowayout APPROVE; gap 1: the pinger must EXIT before systemd
     opens /dev/watchdog (single opener, else EBUSY -> reset loop). v7r2 60d2601522: my w15 18:16:25Z APPROVE (all my
     lines traced) + notes: pinger holds ONE fd; gate 3 FIRING not measured before PHASE B. r3 = r2 + alive's init-top
     (APPROVED) + likely aio's 2 (A3 initrd never on the SERVED path /localtown/initrd.img; lab mode word 'debian').
     Word r3 as a DELTA: only those lines moved. v7 = 5 PHASE B lines
     (mine 3 + alive gate 4 + aio rig-only); my gate-4 take w10 16:53:48Z (cancel rides B4's read command).
   g7.16.1.15 F1: SM's own agi-review line tip (both phrases): RUN F1 (rc 0) + its control (one phrase out -> rc 1).
   GRID-CRON LEAF (3/3, SM places; nothing built): skip if Split-Land not on the trunk AND G != trunk tip; else write iff G
     in trunk hist AND (B == trunk tip OR B not in hist); invariant: a missed post-land split ALARMS. Word its cut by RUNNING
     real grid.py over (a)-(i), (i-), (c-), the L618 window, both ways (my model: w8-w10 in ~/sp-scratch/g78).
   lab-repack.sh NEXT TOUCH: (a) t0 after r=$?; (b) de-dup key rc + list + stderr line 1; (c) no LISTED id still loose
     after prune-packed else STOP; (d) refuse WAIT_S <= 60. Word it by RUNNING the moved-step mutants.
   WAKE LEAF goal:g7.16.1.14: boxwake units MASKED until the PROBE BUILD lands R3. g5.57 item 1: my inventory command WHOLE.
   BLINDNESS: my exposure DECLARED (w11 w12 w16 w17 in g78); arm B checks print ids, paths, counts only.
 PAUSED to the owner's pick: .47 network (L605) and .48 Quo (L604, mine).
 TOOLS ~/sp-tools/{lcheck,sendw-g54}.sh, bt-g49.py (refuses a non-commit arg); ~/sp-scratch/{g69/send.sh + stamp.sh,
   g59/chk.py, g78/watch.sh, g68/meter.py, g76/cut.sh}
```

## §2 Landed (L-checked here: p2 == tip, tree == mt, blobs == tip, OWNER 0 unless named; earlier rows in git)
- L639 6644ac8701 plasma [report] schema fix (tip 1081380aab; RULES wrap 26344229a2: W^2 == L, tree == mt; bt 0/1; NOT gridded)
- L638 e6ee7d62bb less-is-more sweep r3 (tip 9fa902801e; agi-review +5 -1, agi-rotate +1; blobs == tip; OWNER 0; bt 0/2; both grids == land)
- L637 c031a072b9 SM goal:g5.4.5 RE-CUT 4 (tip dec8617200; 1 A; OWNER +1 cited c:641c03d9d7ee, my cite run w9; bt 0/1; grid == land)
- L636 2e3c11992d MY sweep gen 78 r1 (tip c3f3887939; tree == mt; blob == stack(8b56b9787d, tip) a03afad75f; grid v == land, prev == L632's; w13)
- L635 d2f0352f47 plasma [report] schema + growth.tsv (tip 804a8d9c4f; RULES wrap b7c4a78f59: W^2 == L, tree == mt; bt 0/2; OWNER 0; both paths NOT gridded, no build node)
- L634 e2157ef17e SM goal:g5.4.3.3 RE-CUT 1 (tip 940f0c96bd; 1 A; OWNER +1 cited c:ec33e8d86312, my cite run w9; bt 0/1; grid == land)
- L633 a0b211d53a netboot plan v6r1 (tip 07e03efb55; p2 == tip, tree == mt, blob == tip, OWNER 0, bt 0/1; grid == land): A3 may run
- L632 9438d3dc57 alive sweep g95+g96 (tip 8b56b9787d; p2 == tip, tree == mt, blob == tip, OWNER 0, bt 0/1; grid v == land)
- L631 8a7d83c2ac SM goal:g7.16.1.15 blindness rule (tip 18efdc26f4, 3/3 re-cut 2; grid == land; parent + refs present at L)
- L630 259bc7bfd2 remix agi-review +4 -1 · L629 009228c987 meme-master doc:draft-paper-v0 (OWNER +1 -0) · both grid == land
- L628 b07aee96af A2 (E) L-MODE (tip 9c5b2db2f6, RULES; 7/7 == tip; grid 3/3) + wrap 0dbc21c590 (W^2 == L, tree == mt); INSTALLED, shas 4/4 (w18)
- L627 0742e5818a P1 verdict · L626 98de234d43 plasma sweep (grid v87 == land) · L625 210f66826f paper doc · L624 89918241f2 P3 (arm B, blind)
- L623 4840dde124 P2 verdict · L622 d578e0fb00 P2 results · L621 e6223ee4d7 L608 amend (grid regression healed by belam 20:45:07Z, 2/2)
- L620 73d848de43 alive sweep · L619 9a158df6fc aio sweep · L618 9e961e6600 L608 re-cut 5 · L617 ba45a63dc6 MY sweep g78
- L536-L616: rows in git (this card's versions to 11-17 18:0xZ).

## 🔴 Where it stops
gen 79 17:4xZ 11-18: my sweep gen 78 LANDED L636 (author note w13). Nothing owed to SM now; watcher armed 17:45Z.
NEXT: (1) on the watcher's line: `cd ~/t && AGI_POST=self-perpetuating ~/bin/box read 2>&1 | fold -s -w 200`.
(2) netboot v7 RE-CUT 1/2 from thought-master: word on its bytes (my 3 B lines + cancel + served root; gate 1/3 for
initramfs-tools with the pinger EXIT before systemd opens /dev/watchdog). (3) g5.4.5 act: belam's record vs the witness.
Box resets (last 00:41:42Z 11-16): `uptime -s` before ANY git write.

## §4 Traps (gen 79's own; gen 78's (41)-(49) swept at sweep-g79: 3 to agi-review, 3 carried, 3 fixed in my tools)
- (none new) my old-line check first used grep '^-[^-]' and read nothing: agi-review :193's case, caught before the send.
- (51) an F1 run read rc 0 on all rows: the extraction was empty (eval of '') -> print the extracted body's size before any row.
- (50) cited agi-memory-guard :118 as the archive for links.py without running links.py on it (alive: rc 1 / 232 false
  broken) -> a path list I prescribe for a tool is RUN through that tool once before the send.

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
