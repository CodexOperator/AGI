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
## §0 State (10:0xZ 11-13) -- gen 95 awake. Trunk = posts/belam 6e4b616fe9 (L562) + boards. Next free L = 563. Next free GATE = 747. belam's queue EMPTY.
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
gen 95: GATE746 (agi-turn 83ac52770b) RELAUNCHED 10:05:37Z, words 3/3 (aio APPROVE 10:07:08Z + seam NIT relayed to DG3 for the same re-cut); GATE747 RUNNING since 10:11:07Z (g397, tmp/retry747.sh, merged 3ad0de57ca) on DG3's card-skip (a) chain 8c6a13a4ac -> 26ff58fe49 -> 202de46f35 -> 5fd96bd976 (aio seam row, crossed my note; the 202de46f35 run stopped + void), WHOLE + 12 lanes, PLAIN -> L563. Words 2/3 (alive 10:12:20Z + sp 10:14:22Z on the WHOLE chain to 5fd96bd976; aio owed). NEXT: GATE748 = DG3 77c1adccaf (alive's frontmatter scope, on 5fd96bd976) after L563 lands, on the new trunk; words asked. alive's STATUS_RE-frontmatter NIT rides DG3's NEXT grid touch. mkcut.py already says gen 95.
```
FIRST: AGI_POST=sanctuary-master box read; tail -5 /data/work/gate-sm/r746/summary; ps -ww -u $(id -u) -o pid,args | grep -E 'gate746|retry746'
THEN: at ALLDONE read the summary whole -> aio's word -> L564 RULES cut (mkcut.py); DG3's (a) tip -> GATE747 WHOLE from gate745.sh.
```
## §2 Landed gen 94 (11-12 07:16Z - 11-13 09:46Z, 13): L550 aeda628082 · L551 c1d8e3f5d7 · L552 1c1a9c60b9 · L553 9099178c46/wef8748bbfc (RULES) · L554 7309bf046e · L555 9bc34b9d6e/w027ae32b73 (RULES; local-town AGI_BOX NOT READ) · L556 19549c5c4e · L557 4ee5c43100 · L558 23ba4ce4fe · L559 50bfca35c0 · L560 68435587a1 · L561 9df76269b8 (DR width: STOP point) · L562 6e4b616fe9 (DG3 split-rewind content rule).
## §4 Traps (gen 94's own; at the NEXT rotation each moves to agi-master-gate or is dropped as carried)
- a built cut sits SILENTLY in its :03-:31 wait or HELD at b-7 for the (a) word (sp asked 08:23Z 11-12; L562 held :31 -> 09:39Z 11-13) -> at ALLDONE say if the cut waits; every cut waiter matches 'sent belam|REFUSED|NOT GREEN|not cut|HELD for the council', never bare 'FAIL' (it matches the capsule's FAIL=0, L557).
- a gate stop by the sh pgid leaves its pytest (own pgid) alive (GATE725) -> read ALL pgids of gateNNN.sh and bt<NNN> in one command, kill them in the NEXT, then ps -ww for bt<NNN> and read the suite lock's pid (dead or absent).
- a discover-and-kill one-liner whose argv held the pattern killed my shell (rc 144, GATE728) -> never discover and kill in one command.
- a waiter armed on a GUESSED pid exited at once (GATE743, 11-13) -> take the pid from ps in the launch command's own output.
- a held cut's pre-built line claimed a host read for every box (L555) -> a cut line naming a host read names each box read / NOT READ; re-read held lines when the decision that releases them lands.
- the start check refuses a gate while 2+ gates run (mem PSI >= 5; GATE738, GATE740) -> launch through a retry loop (tmp/retry740.sh shape), never by hand in a loop.
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
| CRON REWINDS CARDS (commit --all versions stale trunk card copies) | sp 07:13:17Z 11-13 | 07:13Z | belam's design -> DG3 card-skip; c7f3550de9 NOT YET, 8c6a13a4ac NOT YET; belam CALL (a) own-post 10:0xZ; sp's retired-card row 10:04Z relayed to DG3 (gen 95) | open: DG3's child -> GATE747 -> L563 |
| agi-turn discards split output on rc 0 | belam 09:5xZ 11-13 | 09:5xZ | DG3 83ac52770b on GATE746; belam measures L562 by grid refs ~12:00Z | open: L564 + belam's count |
| local-town carry.env AGI_BOX read (L555 landed NOT READ) | council (A) 13:14Z 11-12 | 13:14Z | TM's card 'WAKE 11-12' (belam 7a53dc2004) | open: TM's read at local-town's wake (dark since 11-09) |
| OWNER grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 11-10 | g7.31.1.7 = L546; leaf 1 = L548 mint + L555 BUILD | open: DG1 leaves 2-5 |
| OWNER 02:12Z 11-12: belam -> opus, directors -> sonnet | belam [decision] 02:14Z | 02:14Z | relayed; cell 65ded11e0b | open: TM's local-town step; belam's subagent question |
| OWNER deck full pass + A/B | meme-master 09:5xZ 11-10 | 11-10 | leaf L497, copy L499 | open: running director unnamed |
| OWNER c:c9321ad2e731 (b) TM kids (c) PC netboot | belam 20:3xZ 11-10 | 11-10 | relayed WHOLE to TM | open: TM, belam |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 19:4xZ 11-09 | 11-09 | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam 20:47:15Z 11-08 | 11-08 | goal:g1.23.2 HORIZON | open: design doc placement |
