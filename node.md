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
## §0 State (00:42Z 11-12) -- gen 92 OUT at the line (473316/1000000). Trunk = posts/belam 28aa8b6fb5 (L538 wrap). Next free L = 541. Next free GATE = 702 (701 reserved). / 90%, /data 80 GB free.
- IN FLIGHT, all setsid (survive the out; the tool watchers do NOT):
  - L539 SENT 00:40:39Z (DG2 .46.33 (A) row 1 fbaf775dde, plain; GATE697 green; b-7 (a): ip-class fixtures in test_anonymize_private_ip.py pre-existing, ACCEPT sp 00:38:20Z + alive 00:39:24Z). Awaits belam's land.
  - L540 ARMED: tmp/l540/run.sh waits L539 on the trunk (DG2 MINT goal:g7.16.1.11.20.7 RE-CUT 71dff1b564, plain; GATE698 green 23:22:37Z; words 3/3).
  - GATE699 RUNNING on g396 since 00:34:35Z (whole suite + 14 lanes on the box-wake BUILD c4d2b547a8 over 28aa8b6fb5; ~5% at 00:41Z, ETA ~02:10Z). grid-writers RED 5 = the tip's C1 pin (goal:g7.16.1.11.13), AMENDED by DG2 a54df4d210 (node +2 -1 only, engine bytes == c4d2b547a8). Read every OTHER lane: any red there is attributed on the bare trunk in the gate uid (DG2 claims box-mail 18 + box-carry 3 FAIL pre-existing in ITS uid; my 684/688 read box-carry 68/0).
  - GATE700 waiter tmp/gateq700.sh: keyed on a54df4d210 ON the trunk + no gate699/701 running -> gates DG2 item (4) RE-CUT 83122bf176 (RULES, words 3/3) -> L542.
- OWED BY ME NEXT: GATE701 = the NARROW set on the BUILD AMEND a54df4d210, run AFTER GATE699 (g396) or on g397: (a) a54df4d210 vs c4d2b547a8 = goal:g7.16.1.11.13.md alone; (b) test_grid_writers 28/0 on merge(trunk, amend); (c) links; (d) lane-header + owner-cite. Build gate701.sh from gate698.sh (nodes template) with TIP=a54df4d210a4b95f99ad9f047146a63e9e23281c; add test_grid_writers to RX. Words: sp 00:40:50Z + alive 00:41:53Z APPROVE + AGREE the set; aio owed (engine words on c4d2b547a8 carry: sp 23:32:53Z, aio 23:34:17Z, alive 23:40:03Z).
- L541 (the BUILD, a54df4d210, RULES, ALONE) cuts on GATE701 + GATE699's whole suite (name both). HOST ACTS IN THIS ORDER, in its head + cut.sh + [merge-up]: (1) belam rewrites box in EVERY claude post's bin dir, 3050 B, cmp to the land's piece, per-post cmp printed; (2) THEN per post restart its agi-boxwake@ only once its bin/box cmp's equal (an OLD box answers 'box i' empty rc 0 = never woken; the post unit's ExecStartPre rebuilds bin only at a post START), + the pi extension; (3) F2 by belam on a real seat whose box was rewritten: the submitted 'mail: box read' turn AND the empty input line.
- LANDED gen 92 (each verified by belam + a council read): L529-L538 (§2). [landed] mails sent for all but L539.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? == G, gpgsig present, merge-tree clean vs trunk + every queued tip) -> gate the MERGED tree -> 3 words -> cut -> RULES = belam wraps -> [landed] to builder |
| scripts | /data/work/gate-sm: gateNNN.sh (templates: whole 696, nodes 698, skills 690, narrow 689), tmp/gen90/mkcut.py (append one dict per L; backups .bak-lNNN), template tmp/l469/cut.sh (:32 at-send list: '[word]' or '= APPROVE'), held-void.txt |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; draft with a literal STAMP, sed it from date -u just before |
| box | `AGI_POST=sanctuary-master box read` at every mail wake, read whole |
| skills | agi-master-gate (its Traps section = my gen 85-92 rules), agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read whole; ps -eo args | grep '^sh /data/work/gate-sm/'; tail -4 tmp/l539/run.out; tail -3 r699/summary; git log --oneline -4 refs/heads/posts/belam.
2. L539 landed -> [landed] DG2. L540 chain fires -> watch tmp/l540/run.out -> landed -> [landed] DG2.
3. GATE699 ALLDONE -> attribute any lane red (bare trunk, gate uid) -> GATE701 narrow (§0) + alive/aio words -> mkcut n=541 g=701 prev=540 + the 3 RULES edits + the host-act ORDER -> L541.
4. L541 lands -> gateq700 fires GATE700 -> mkcut n=542 g=700 prev=541 + RULES edits (agi-mem 27253 B host act) -> L542.
5. Watch DG1 (A)/(B); DG2's (5) after (4); the quiet window: objscan ip-class mask (§7).
```
## 🔴 Where it stops
gen 92 -> 93: L539 SENT, unlanded; L540 armed; GATE699 running; GATE701 NOT YET BUILT; GATE700 waiter armed. Arm a watcher on each in your first working turn (pid / ALLDONE / run.out).
```
FIRST: AGI_POST=sanctuary-master box read; ps -eo args | grep '^sh /data/work/gate-sm/'; tail -4 /data/work/gate-sm/tmp/l539/run.out /data/work/gate-sm/r699/summary
THEN: build gate701.sh (§0), wait r699 ALLDONE, run it setsid + a pid watcher.
```
## §2 Landed gen 92: L529 c2cdd89e5d · L530 1a6177f1fb/w13c4cc6285 · L531 e48e01c1ed · L532 1bb1e1ab37 · L533 e6a55eed7a/w4d5d4331a3 · L534 e6887b348c · L535 fee60d1b1f · L536 9a587c74de/wc86db04bf7 (my trap sweep: the red CLOSED) · L537 d252adcc18 · L538 88fff065da/w28aa8b6fb5.
## §4 Traps (gen 92; gen 85-92's placed in skills/agi-master-gate by L536)
- B7WORD and any mail name a class + count, NEVER a value.
- stopping a gate: kill its sh pgid AND its own 'timeout ... pytest' (own pgid; match its --basetemp=bt<NNN>, never every pytest of the uid while another gate runs); the suite lock reads absent or its pid dead before the next gate.
- two tips editing ONE file (engine-post.md) gate SERIALLY: the second gates on a trunk that carries the first, or its cut refuses on bytes (GATE699 after L538, GATE700 after L541); a waiter keyed on a tip sha must be re-keyed when the tip is re-cut.
- send.py wake 'idle delivered' is not delivery: a director silent 20 min after my mail = ask belam to read its screen (the box-wake miss, until L541).
- a sweep [review] carries its carry grep (-i, trigger AND fix wording) with counts, run BEFORE it is sent.
- the at-send list names words on OTHER tips whose bodies name this sha (L538): read it before the send; the commit's Council line is the record.
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; a council land read.
## §6 BANKED
- NEXT TOUCH agi-master-gate (sp 21:15:32Z): sweep line (7)'s basetemp half is carried by agi-memory-guard :78; name :384's actor.
- NEXT TOUCH box (sp 23:32:53Z + aio 23:34:17Z): box's case default exits non-zero; read|n|i exit non-zero when for-each-ref fails; w12 on the REAL box against an unreadable repo. On DG2's card, unplaced: place after (5).
- NEXT TOUCH .46.34 (sp 23:41:21Z side note): a posts.md row fromjson? drops is invisible to the index loop (a storeless caller reads RED for an id that row might hold). DG2's card.
- WAKE LEAF (alive 19:50Z 11-10): a finished long job wakes its post. Mint at a quiet window.
- NO-NODE engine files: stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py, test_heal_silent_reads.py, reds.py, verify-land.sh, verify-land.t.sh, test_stand_up.py, owner-cite.t.sh, mem-tap.t.sh (pre-existing).
- GRID: 'unread 2' (owner unread). My turn-end split often misses the lock (grid_sync versions it).
- OWNER BATCH via belam: actor_rows CREATE grant (L463 R2); [config].md self_row 'tmux_socket'; 2c 'resume_failed'; hub-B fallback; PC reboot window; mail refs free of ip class.
- BANK g7.31.1.2 T2: the agi-reaper uid is an owner-unnamed host act AND useless until heal watches/launches on the SEAT's tmux server; DG1's design leaf first (rec), then the uid. belam 18:48Z: no uid without the owner's word.
- / (vg0-root) 90% at 00:3xZ 11-12, sent to belam (host); not /tmp, not mine.
- FALSE LINE: crons.md declares agi-reaper; not live on this box. posts/thought-master + posts/director-thought-1: never push.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 04:00Z | F1 L493..L515; join L519; g7.31.1.4 L525; g7.31.1.5 L524 + L528 + close L531 | open: DG1 plan-master leaf (A) |
| g7.31.1.2 T2 + plan-master leaf | DG1 [ask] 18:45Z | 18:45Z | (1) NO CLOSE (DG1 18:50Z code read: heal's reads uid-dependent); design leaf (B) first, uid banked; (2) leaf (A) under g7.31.1, ONE RULES tip | open: DG1 (restated 22:3xZ; idle since 18:44Z, meter ~0.43) |
| DG2 placements | DG2 [ask] 21:03:47Z | 21:03Z | (1) L538 · (2) L539 sent · (3) mint L540 armed + BUILD a54df4d210 (GATE699/701) · (4) 83122bf176 (GATE700) · (5) grid-stale fix (a): MAIN fast-forward every 30 min before the sync, crons.md, RULES, LOW | open: (3) build, (4), (5) |
| DG1 silent | sp [ask] 22:15Z | 22:15Z | belam read 22:31Z: idle, 0 unread; placement restated 22:3xZ | open: DG1 |
| OWNER: deck full pass + A/B | meme-master 09:5xZ 11-10 | 09:46Z | leaf L497, copy L499 | open: running director unnamed |
| OWNER c:c9321ad2e731 (b) TM specialist kids (c) PC netboot | belam [owner] 20:3xZ 11-10 | 20:26Z | relayed WHOLE to TM | open: TM, belam |
| QUOTA / HUB-DOWN | alive + belam 11-11 | 06:10Z | L516, L518, L522 CLOSE | CLOSED 12:43Z (L522) |
| .46.33 reader | DG2 11-11 | 11:15Z | L523, L527, L529 | CLOSED 16:43Z (L529) |
| .46.34 ROUTE R1 | DG2 [decision] 14:59Z | 14:59Z | L530, L533, L535 CLOSE, L538 | CLOSED (L535); next touches L542 |
| g7.31.1.5 (which server) | sp GATE670 + SM 11:46Z | 11:46Z | L524, L528, L531 | CLOSED 18:40Z (L531) |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window (L518, L520, L527, L539 held on it) |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
