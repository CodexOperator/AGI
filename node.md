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
## §0 State (gen 94, woke 11-12) -- gen 93 OUT at the line (471171/1000000). Trunk = posts/belam ef8748bbfc (L553 wrap). Next free L = 554. Next free GATE = 728. belam's queue EMPTY.
- IN FLIGHT (gen 94): L553 LANDED wrap ef8748bbfc 08:35:30Z (sweep in the skills; §4 trimmed). alive TRAP SWEEP gen 85 9bac7b72a4 (PLAIN) on GATE727 (g397, pid 1460446; pytest 463/0 done): words sp 08:31:15Z + aio 08:31:36Z, author alive = complete -> L554 prev=553 at ALLDONE.
- OWED BY ME NEXT: DG3 tip 00e7c36e573ca893d763f5b14bd5745adb130a15 (dg3-p1-rss-test, ONE commit on af4b1c5035, test_p1_ab.py +8 -2: the peak-RSS row sizes the kid above own_hwm_kb() +100 MB after pre-raising the forker to 450 MB; mutant RED; DG3: file 160/0). = the L549 named red's next touch. Signed G (pre-read 07:13Z). Words ASKED 07:1xZ. Gate it NARROW as GATE720 (test_p1_ab.py + grid-writers + links + lane-header/owner-cite; nodes/narrow template gate704.sh with RX='/test_p1_ab[.]py$') on g398, then mkcut n=550 g=720 prev=549, PLAIN.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? == G, gpgsig, merge-tree clean vs trunk) -> gate the MERGED tree -> 3 words -> cut -> RULES = belam wraps -> [landed] to builder ONLY after belam's [landed] |
| scripts | /data/work/gate-sm: gateNNN.sh (templates: whole 708, nodes 704/719, skills 714, narrow 701), tmp/gen90/mkcut.py (append one dict per L; backups .bak-lNNN; RULES lands need L541/L543/L545's 3 edits: head ', RULES)', head last line, cut.sh WHAT line), held-void.txt; a named suite red = L549's override shape (r708/summary.rerun + one if-line in cut.sh) |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; draft with a literal STAMP, sed it from date -u just before |
| box | `AGI_POST=sanctuary-master box read` at every mail wake, read whole (box-wake L543: mail arrives as a submitted turn) |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read whole; ps -ww -u $(id -u) -o pid,args | awk '$2=="sh" && /gate|l5[0-9][0-9]/'; git log --oneline -3 refs/heads/posts/belam.
2. sed '(gen 93)' -> '(gen 94)' in tmp/gen90/mkcut.py (the [merge-up] stamp).
3. DG3 00e7c36e57: GATE720 narrow -> 3 words -> L550 -> [landed] DG3 after belam's.
4. The TRAP SWEEP tip (§0), RULES.
5. Next inbound: DG1 leaf 1 BUILD (config:engine, RULES, ALONE, + the posts: block line count); director-review's measure fix; any re-cut.
```
## 🔴 Where it stops
gen 94: GATE727 (alive sweep) finishing -> L554 prev=553 -> belam -> [landed] alive. Queue empty after.
```
FIRST: AGI_POST=sanctuary-master box read; ps -ww -u $(id -u) -o pid,args | awk '$2=="sh"'; git -C ~/t log --oneline -3 refs/heads/posts/belam
THEN: sed -i 's/(gen 93)/(gen 94)/' /data/work/gate-sm/tmp/gen90/mkcut.py; build gate720.sh from gate704.sh (TIP=00e7c36e57..., RX test_p1_ab), run it setsid on g398.
```
## §2 Landed gen 93 (00:47Z-07:09Z, 11): L539 ea406b6b25 · L540 95796f8530 · L541 f28bcf0103/w8c0ae8fe19 · L542 d0a6f7badf · L543 a04a8d54f9/wf3138789df (box-wake BUILD; F2 PASSED) · L544 b574478144 · L545 d9f3c72c56/wbb55ab3cd4 · L546 5a3ada79dc · L547 38ea1770b7 · L548 43ec1ee78c · L549 af4b1c5035. Belam's model cell 65ded11e0b (owner word).
## §4 Traps (gen 94; gen 92/93's PLACED by L553 ef8748bbfc in agi-master-gate + agi-send)
- a built cut sits in its :03-:31 board-window wait SILENTLY: a green gate with a waiting cut went 22 min unannounced and the council asked (sp 08:23:05Z) -> at a gate's ALLDONE, if the cut waits for :31, say so to the council in one line.
- a gate's sh pgid kill leaves its pytest (own pgid) alive: placed L553, and it fired AGAIN on GATE725 (08:5xZ) -> after every gate stop, ps -ww for bt<N> before moving on.
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a council land read.
## §6 BANKED
- NEXT TOUCHES carried in landed text: L541 stale job after the sync + 'newest cron tip' label; L546 leaf 4 rm -rf -- "${o:?}"; L547 (3)'s name half (gates key on the sha); L548 BUILD counts every posts: block line; L549 docstring cause (done in the fold).
- NEXT TOUCH agi-master-gate (sp 21:15:32Z 11-11): sweep line (7)'s basetemp half is carried by agi-memory-guard :78; name :384's actor. Fold into the trap sweep.
- NEXT TOUCH box (sp 23:32:53Z + aio 23:34:17Z): case default exits non-zero; read|n|i exit non-zero when for-each-ref fails. DG2's card.
- SUSPENDED (owner 02:12Z fable reserve): council ORACLE (agi-review :64) + the L509 design-stage fable exception -> opus; one clause each at the next sweep; belam asks the owner whether the reserve covers subagents.
- WAKE LEAF (alive 19:50Z 11-10): a finished long job wakes its post. Mint at a quiet window.
- NO-NODE engine files: test_grid_stale_cadence.py, owner-cite.t.sh, box-mail/box-wake/boxwake-unit.t.sh, stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py, test_heal_silent_reads.py, reds.py, verify-land.sh/.t.sh, test_stand_up.py, mem-tap.t.sh (pre-existing class).
- GRID: 'unread 2' (two never-landed mints). My turn-end split often misses the lock (grid_sync versions it).
- OWNER BATCH via belam: actor_rows CREATE grant (L463 R2); [config].md self_row 'tmux_socket'; 2c 'resume_failed'; hub-B fallback; PC reboot window; mail refs free of ip class.
- BANK g7.31.1.2 T2 / g7.31.1.6 F4: the agi-reaper uid only on the owner's word (belam 18:48Z 11-11).
- / (vg0-root) 79% after DG1's clean-up 01:0xZ 11-12; DG1 kept 11 clones for its own diff look.
- FALSE LINE: crons.md declares agi-reaper; not live on this box. posts/thought-master + posts/director-thought-1: never push.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| DG3 p1_ab peak-rss test fix 00e7c36e57 (L549's named red) | alive 07:11:22Z -> DG3 [merge-up] 07:1xZ | 07:13Z | L550 aeda628082 | CLOSED 07:34Z (kid_mb ceiling = DG3 next touch) |
| OWNER grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 11-10 | umbrella g7.31.1.7 = L546; leaf 1 g7.31.1.7.1 = L548 (5 council rounds: claude fallback, stale drop-ins, zero rows, core-town, broken row, AGI_BOX fallback); leaves 2-5 next | open: DG1 leaf 1 BUILD |
| g7.31.1.6 heal per-seat server | DG1 18:45Z 11-11 | 11-11 | mint L542, engine tip L549; CLOSE re-cut asked 07:3xZ | open: CLOSE L551 |
| OWNER 02:12Z: belam -> opus, directors -> sonnet, fable for season rollover | belam [decision] 02:14Z | 02:14Z | relayed; cell 65ded11e0b + host step; DG3/DS1 told to rotate at idle close; thought crew = local-town host step (TM asked) | open: TM's local-town step; belam's owner question on subagents |
| director-review publish-now or hold (11-05, AGED) | director-review 02:1xZ | 02:16Z | HOLD: successor cuts media_html.py :190 measure fix + RED/GREEN row; I gate; then rebuild + publish | open: DR's fix tip |
| DG2 placements (1)-(5) | DG2 21:03:47Z 11-11 | 11-11 | L538, L539, L540+L543, L545, L541 | CLOSED 05:44Z |
| OWNER deck full pass + A/B | meme-master 09:5xZ 11-10 | 11-10 | leaf L497, copy L499 | open: running director unnamed |
| OWNER c:c9321ad2e731 (b) TM kids (c) PC netboot | belam 20:3xZ 11-10 | 11-10 | relayed WHOLE to TM | open: TM, belam |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 19:4xZ 11-09 | 11-09 | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam 20:47:15Z 11-08 | 11-08 | goal:g1.23.2 HORIZON | open: design doc placement |
