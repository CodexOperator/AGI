---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags: []
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.
## §0 State (13:5xZ 11-13) -- gen 95. HUB B since 15:12:57Z (owner via belam [owner] 15:1xZ: everyone to hub B; unit restarted, nothing in flight). Trunk = posts/belam 6b8ec91a57 (L568) + boards. Next free L = 569. Next free GATE = 755. QUEUE EMPTY 15:4xZ. NEW 15:14Z: meme-master RE-SENT its two 11-10 lanes (sunk since gen 89, my miss): outline e2bae92830 -> GATE751 (g397) RUNNING 15:14:56Z -> L567 PLAIN; fuel 0881087b6b -> GATE752 (g398) after it -> L568 PLAIN. Node template (gate704.sh), tmp/retry751/752.sh. Words 3/3 each (aio 15:16:20Z, sp 15:17:22Z, alive 15:18:26Z; alive NIT on the fuel totals relayed to meme-master). GATE751 GREEN 15:23:53Z; L567 = d419a9a4ce on 4be3000dd7 SENT 15:31:21Z (capsule 67/0, objscan clean). GATE752 GREEN 15:33:57Z (links 6110/0 with the outline link). L567 LANDED belam 15:35:43Z ([landed] sent). L568 = 6b8ec91a57 on d419a9a4ce SENT 15:36:57Z (capsule 67/0, objscan clean); LANDED belam 15:40:18Z, [landed] sent; belam ran meme-master's Drive v1.2 upload (21/21 OK). ORDER: L567 before L568 (fuel links the outline, sp); GATE752 PRE = GATE751 merged tree 7b6c8191be (gate752.sh edited before it started).
- GEN 95 WAKE: the gen 94 GATE746 run DIED mid-pytest at the out (no ALLDONE; kept as r746.died-at-out). RELAUNCHED 10:05:37Z via tmp/retry746.sh (sh gate746.sh pid 2609407, merged 2cc57ae5a5). sp's [word] 10:04:02Z = APPROVE GATE746 (== alive) + a RETIRED-CARD row for (a): relayed whole to DG3 + council (tmp/relay-dg3-cardskip-row.txt). Words now 2/3 (aio owed).
- RUNNING: GATE746 (g398, r746/summary) = DG3 AGI-TURN SKIP LINE 83ac52770b (G, one commit on L562; .agi/nodes/.geometry/engine-post.md agi-turn +2 -2 + zero-commit.t.sh z20c; RULES (.geometry) + HOST ACT: every running post's own bin/agi-turn rewritten in its own uid, cmp printed, as L545's agi-mem). Narrow set: the 14 pytest files naming engine-post + lanes lane-header owner-cite agi-turn zero-commit engine-sizes box-wake restart-bounds boot-cells. Words: alive APPROVE 10:01:09Z (+NIT 'or a revert the cron will write'); aio + sp OWED, and their word on the narrow set.
- OWED NEXT, inbound: DG3 CARD-SKIP CHILD on 8c6a13a4ac (belam's CALL 10:0xZ = (a) OWN-POST: commit --all skips doc:card-P only when its tip's newest version is a split whose Split-Land commit is AUTHORED by P; card-belam never; rows alive's land-split-owned + belam's four). Relayed to DG3 10:1xZ. Gate it WHOLE as GATE747 from gate745.sh (sed NNN, TIP, trunk file, label) on g397 (free; GATE744/745 void, lock pid dead) -> 3 words -> L563 PLAIN.
- Then L564 = the agi-turn tip (RULES, + the 3 RULES edits, host-act line in head + WHAT), prev = the last ARMED L. belam wraps + runs the host act.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? == G, merge-tree clean vs trunk, diff --stat vs trunk) -> gate the MERGED tree -> 3 words (author's own tip: 2 + author) -> cut -> RULES = belam wraps -> [landed] to builder ONLY after belam's [landed] |
| scripts | /data/work/gate-sm: gateNNN.sh (latest shapes: whole gate745.sh, narrow gate743.sh/gate746.sh, skills gate740.sh, nodes gate704.sh; all pytest -q -rfs), tmp/gen90/mkcut.py (append one dict per L; .bak-lNNN; RULES lands: L553/L555's 3 edits), tmp/retry740.sh (start-check retry shape) |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; draft with a literal STAMP, sed it from date -u just before; never a value of a privacy class (gsend refuses '/home/x' text, e.g. 'ip/host/home/token') |
| box | `AGI_POST=sanctuary-master box read` at every mail wake, read whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read whole; ps -ww -u $(id -u) -o pid,args | awk '$2=="sh"'; git log --oneline -3 refs/heads/posts/belam.
2. sed -i 's/(gen 94)/(gen 95)/' /data/work/gate-sm/tmp/gen90/mkcut.py
3. GATE746 ALLDONE + 3 words -> L564 RULES (or L563 if card-skip is later; prev = last ARMED).
4. DG3 card-skip child -> GATE747 WHOLE -> L563 PLAIN.
5. Then inbound only: DG1 leaves 2-5; DR's two cosmetic slips ride its next touch; alive's next sweep.
```
## 🔴 Where it stops
gen 95: GATE749 GREEN 11:04:02Z -> L563 RULES (agi-turn, 89d625ae47; host act agi-turn 8956 B) CUT + SENT 11:31:21Z: L563 = 3598c50f68 on trunk aeb125811f, 0 D, 0 byte diff, anon 0, email [], capsule 67/0, store 0, held refs/held/sanctuary-master/L563; LANDED: belam wrap 964783b95a 11:35:14Z, host act 12/12 cmp OK; [landed] sent to DG3 11:3xZ. GATE747 GREEN 11:35:25Z (pytest 9976/0, links 0, 12 lanes 0) -> L564 held at b-7 11:36:49Z (test_grid.py:2838 pre-existing, 0 new), (a) words 3/3 by 11:40:46Z -> RE-CUT + SENT 11:41:45Z: L564 = e32f378635 (same tree as the held 2ba0b99397, re-signed) on 964783b95a, capsule 67/0, held ref L564; LANDED belam 11:44:54Z (refs equal at e32f378635), [landed] sent to DG3; belam reads the 12:00 cron's 'cards skipped N' + a card A-B-A after 12:30. GATE748 (77c1adccaf, WHOLE) GREEN 12:52:45Z -> L565 = 2b9bedf933 on eae1524631 HELD at b-7 12:53Z (the :2838 fixture, 1 blob, 0 new; tmp/l565/run.out.held); (a) words 3/3 by 12:57:24Z -> RE-CUT + SENT 12:57:58Z: L565 = 0e420b9c87 (same tree as 2b9bedf933) on eae1524631, capsule 67/0, held ref L565; LANDED belam 13:09:38Z (refs equal at 0e420b9c87), [landed] sent to DG3. Trunk = 0e420b9c87 (L565). Next free L = 566, GATE = 750. DG3's next grid touch carries aio NIT 1 + NIT 2. NEW 13:31Z: aio TRAP SWEEP gen 78 188bed6105 (agi-review +4, PLAIN) -> GATE750 RUNNING since 13:31:50Z (g396, skills template from gate740.sh, tmp/retry750.sh) -> L566 PLAIN; words 3/3 (author aio, sp 13:33:04Z, alive 13:34:06Z). GATE750 GREEN 13:46:10Z (pytest 463/0, links 0, 9 lanes 0). L566 = e29f6b3677 on 8026cca21c SENT 13:47:24Z (capsule 67/0, objscan clean, held ref L566); LANDED belam 13:50:23Z, [landed] sent to aio. Trunk = e29f6b3677 (L566). Next free L = 567, GATE = 751. QUEUE EMPTY (tmp/l566/run.sh; run.out: read it at the gate's end for sent / HELD / REFUSED / NOT GREEN). Before: GATE746 (agi-turn 83ac52770b) ALLDONE 10:35:24Z NOT GREEN: engine-sizes FAIL b1-map-rows (engine-post.md:28 map row agi-turn 8742, heading 8956); all else green. [red] to DG3 (tmp/red-dg3-746.txt); DG3 fix 89d625ae47 (map row only, G) -> GATE749 NARROW RUNNING since 10:39:24Z (g398, tmp/retry749.sh, pre 3ac90fd62e = L562 + belam's 10:27Z board, merged 9a16022c41) -> L564 RULES; fix-line words 3/3 (alive 10:39:44Z, aio 10:40:36Z, sp 10:40:46Z). Words 3/3 on content; GATE747 RUNNING since 10:11:07Z (g397, tmp/retry747.sh, merged 3ad0de57ca) on DG3's card-skip (a) chain 8c6a13a4ac -> 26ff58fe49 -> 202de46f35 -> 5fd96bd976 (aio seam row, crossed my note; the 202de46f35 run stopped + void), WHOLE + 12 lanes, PLAIN -> L563. Words 3/3 (alive 10:12:20Z, sp 10:14:22Z, aio 10:23:59Z). NEXT: GATE748 = DG3 77c1adccaf (alive's frontmatter scope, on 5fd96bd976) after L563 lands, on the new trunk; words 3/3 (alive 10:15:27Z, sp 10:16:28Z, aio 10:23:59Z). aio's NIT 1 (row (r) pins each retire half alone) + NIT 2 ('Named cost' comment sentence back) relayed to DG3 for its NEXT grid touch. GATE746: pytest 1165/0 + links 0 broken at 10:18:50Z, lanes running. alive's STATUS_RE-frontmatter NIT rides DG3's NEXT grid touch. mkcut.py already says gen 95.
```
FIRST: AGI_POST=sanctuary-master box read; tail -5 /data/work/gate-sm/r746/summary; ps -ww -u $(id -u) -o pid,args | grep -E 'gate746|retry746'
THEN: at ALLDONE read the summary whole -> aio's word -> L564 RULES cut (mkcut.py); DG3's (a) tip -> GATE747 WHOLE from gate745.sh.
```
## §2 Landed gen 94 (11-12 07:16Z - 11-13 09:46Z, 13): L550 aeda628082 · L551 c1d8e3f5d7 · L552 1c1a9c60b9 · L553 9099178c46/wef8748bbfc (RULES) · L554 7309bf046e · L555 9bc34b9d6e/w027ae32b73 (RULES; local-town AGI_BOX NOT READ) · L556 19549c5c4e · L557 4ee5c43100 · L558 23ba4ce4fe · L559 50bfca35c0 · L560 68435587a1 · L561 9df76269b8 (DR width: STOP point) · L562 6e4b616fe9 (DG3 split-rewind content rule). GEN 95: L563 3598c50f68/w964783b95a (RULES, agi-turn skip line + host act) · L564 e32f378635 (card-skip (a)) · L565 0e420b9c87 (frontmatter scope) · L566 e29f6b3677 (aio trap sweep g78) · L567 d419a9a4ce (mm outline) · L568 6b8ec91a57 (mm fuel s4).
## §4 Traps (gen 94's own; at the NEXT rotation each moves to agi-master-gate or is dropped as carried)
- a built cut sits SILENTLY in its :03-:31 wait or HELD at b-7 for the (a) word (sp asked 08:23Z 11-12; L562 held :31 -> 09:39Z 11-13) -> at ALLDONE say if the cut waits; every cut waiter matches 'sent belam|REFUSED|NOT GREEN|not cut|HELD for the council', never bare 'FAIL' (it matches the capsule's FAIL=0, L557).
- a gate stop by the sh pgid leaves its pytest (own pgid) alive (GATE725) -> read ALL pgids of gateNNN.sh and bt<NNN> in one command, kill them in the NEXT, then ps -ww for bt<NNN> and read the suite lock's pid (dead or absent).
- a discover-and-kill one-liner whose argv held the pattern killed my shell (rc 144, GATE728) -> never discover and kill in one command.
- a waiter armed on a GUESSED pid exited at once (GATE743, 11-13) -> take the pid from ps in the launch command's own output.
- a held cut's pre-built line claimed a host read for every box (L555) -> a cut line naming a host read names each box read / NOT READ; re-read held lines when the decision that releases them lands.
- the start check refuses a gate while 2+ gates run (mem PSI >= 5; GATE738, GATE740) -> launch through a retry loop (tmp/retry740.sh shape), never by hand in a loop.
- (gen 95) a .geometry piece edit was approved 3/3 with engine-sizes NOT RUN by any word, and the heading size matched while the ## pieces map row did not (GATE746 red, 83ac52770b; all three words named the miss) -> every gate of a .geometry piece edit carries the engine-sizes lane, and the ask for words names it. At rotation: DROP as carried by agi-review :158 ('the lane set for ANY edit = every test that names the edited file'; sp + aio 13:3xZ 11-13).
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a council land read.
## §6 BANKED
- NEXT TOUCHES in landed text: L541 stale job + 'newest cron tip' label; L546 leaf 4 rm -rf -- "${o:?}"; L547 (3) name half; L548 BUILD counts posts: lines (done in L555); aio's L555 next touch: the write path's local-town fallback (WAITS on local-town's carry.env read).
- DR (L561 closed the string rounds): sp's two cosmetic slips ride DR's next unrelated touch; a rendered-width check is the owner's call.
- NEXT TOUCH box (sp + aio 11-11): case default exits non-zero; read|n|i exit non-zero when for-each-ref fails. DG2's.
- SUSPENDED (owner 02:12Z 11-12 fable reserve): council ORACLE + L509 design-stage fable exception -> opus; belam asks the owner whether the reserve covers subagents.
- WAKE LEAF (alive 11-10): a finished long job wakes its post. Mint at a quiet window.
- NO-NODE engine files: the crumb class (alive's list): test_media_html.py, agi-project-harness.t.sh, test_agi_boot.py, test_p1_ab.py + the earlier ones.
- GRID: my turn-end split often misses the grid lock (grid_sync versions it).
- OWNER BATCH via belam: actor_rows CREATE grant; [config].md self_row 'tmux_socket'; 2c 'resume_failed'; hub-B fallback; PC reboot window; mail refs free of ip class.
- BANK g7.31.1.2 T2 / g7.31.1.6 F4: the agi-reaper uid only on the owner's word. crons.md's agi-reaper is not live here; posts/thought-master + posts/director-thought-1: never push.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| CRON REWINDS CARDS (commit --all versions stale trunk card copies) | sp 07:13:17Z 11-13 | 07:13Z | belam's design -> DG3 card-skip; c7f3550de9 NOT YET, 8c6a13a4ac NOT YET; belam CALL (a) own-post 10:0xZ; sp's retired-card row 10:04Z relayed to DG3 (gen 95) | L564 LANDED 11:44:54Z (+ L565 GATE748 frontmatter running) | CLOSED 12:3xZ: belam live read, 12:00 + 12:30 cron 'cards skipped 4', 0 card versions by the cron; A-B-A closed; relayed to DG3 |
| agi-turn discards split output on rc 0 | belam 09:5xZ 11-13 | 09:5xZ | DG3 83ac52770b on GATE746; belam measures L562 by grid refs ~12:00Z | L563 LANDED 11:35:14Z (host act 12/12) | CLOSED 12:0xZ: belam's L562 watch 09:46:26Z-12:00Z = 0 non-cron rewinds |
| local-town carry.env AGI_BOX read (L555 landed NOT READ) | council (A) 13:14Z 11-12 | 13:14Z | TM READ 16:3xZ 11-14: AGI_BOX=1, the box's own name; guard does not fire, no host act | CLOSED: relayed to aio + DG1 (tmp/relay-a19-tm-read.txt); my 11-12 binding lifted; CUT 3/3 (aio 16:28:53Z, sp 16:30:59Z AMEND: BOTH defaults :61 + :65, unset refusal FIRST, one mutant per default; alive 16:32:09Z) relayed whole to DG1. TIP 83de0c9160 (+ DEVIATION: agi-gate reads AGI_BOX from carry.env when unset) -> GATE754 WHOLE + 25 lanes (g398) RUNNING 17:0xZ -> L570 RULES alone, belam wraps; words + the deviation asked. NEXT: belam's agi.sh host BOX default (agi.sh:104/:122) + box-blind pi PREREQ: proposed DG1's next narrow touch |
| OWNER grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 11-10 | g7.31.1.7 = L546; leaf 1 = L548 mint + L555 BUILD | open: DG1 leaves 2-5 |
| OWNER 02:12Z 11-12: belam -> opus, directors -> sonnet | belam [decision] 02:14Z | 02:14Z | relayed; cell 65ded11e0b | open: TM's local-town step; belam's subagent question |
| OWNER deck full pass + A/B | meme-master 09:5xZ 11-10 | 11-10 | leaf L497, copy L499 | open: running director unnamed |
| OWNER c:c9321ad2e731 (b) TM kids (c) PC netboot | belam 20:3xZ 11-10 | 11-10 | relayed WHOLE to TM | open: TM, belam |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 19:4xZ 11-09 | 11-09 | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 16:0xZ 11-14: TM collects rough-draft v2 data + keeps researching local inference with it and meme-master's fuel | belam [owner] 16:0xZ 11-14 | 16:0xZ | belam sent it to TM whole; TM DARK since 11-09 | RESOLVED 16:1xZ 11-14: the owner woke local-town (belam: wg-quick@agilab restart, agi-lab by hand 16:14Z, agi-post@thought-master active 16:15Z); TM's box holds the ask, after its WAKE 11-12 first act. No SM placement |
| OWNER 16:0xZ 11-14 STANDING: meme-master replaces rough-draft-v1/v1.2/ in place without a fresh owner word | belam [owner] 16:0xZ 11-14 | 16:0xZ | its [ask] still comes to belam THROUGH ME: relay whole, belam runs it (restage, sha256 -c, scan, copy --checksum, check 0 diff); no new folders | standing rule, no close |
| OWNER 16:2xZ 11-14: fuel redundant -> belongs in the town board node | belam [owner] 16:2xZ 11-14 | 16:1xZ | PLACED 3/3 16:2xZ (tmp/decision-fuel-fold.txt): L-a1 PLAIN mm (town:core '## Fuel' mm block, retire fuel:s4, re-point g5.4.3.1 + deck-v1) · L-a2 PLAIN belam (idea block on its pick of board, retire the idea, card line) · L-b RULES mm after both (growth.tsv :60-64 out, [fuel].md KEPT with a 'type closed' line), belam wraps | open: L-a2 belam 9b00bd4fa0 (town:core ## Fuel belam block + retire the idea; card-belam line in belam's own card commit after) -> GATE753 RUNNING 16:44:32Z (g397, gate753.sh) -> L569 PLAIN, words 3/3 (alive 16:51:59Z); L569 cut BUILT + ARMED (tmp/l569 run.out); L-a1 (mm) + L-b (mm) tips owed |
| OWNER 2 PLUGIN | belam 20:47:15Z 11-08 | 11-08 | goal:g1.23.2 HORIZON | open: design doc placement |
