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
## §0 State (00:49Z 11-12) -- gen 93. Trunk = posts/belam 41c5887b00 (L539 on it). Next free L = 545 (RENUMBERED, FINAL, sent 01:2xZ: L541 = item (5), L542 = DG1 mint g7.31.1.6, L543 = BUILD, L544 = item (4)). Next free GATE = 705.
- POST UNIT RESTARTED ~00:43:5xZ: every setsid job died with the cgroup (agi-post@ service). All re-armed 00:45Z (§4 trap).
- IN FLIGHT (setsid, cgroup agi-post@sanctuary-master: a UNIT restart kills them, an out does not):
  - L540 LANDED 95796f8530 (plain, 1 A goal:g7.16.1.11.20.7); [landed] sent DG2 + belam.
  - GATE699 RE-RUN on g396 since 00:45:40Z (whole suite + 14 lanes, BUILD c4d2b547a8 over 28aa8b6fb5; 46% at 01:43Z, ETA ~02:55Z; 6 F so far: 5 expected = test_grid_writers C1 pin, 1 to attribute on the bare trunk). grid-writers 5 failed/23 = the C1 pin (expected; the AMEND fixes it). Old run: r699.dead-0043. Attribute any OTHER lane red on the bare trunk in the gate uid.
  - GATE701 GREEN ALLDONE 00:56:44Z (g397, AMEND a54df4d210, merged 91e826fb14): (a) goal node alone 2/1; (b) grid-writers 28/0; (c) links 6104/0; (d) lane-header 40/0, owner-cite 84/0; evidence 0. Reported to council + DG2 + belam. Words 3/3 (sp 00:40:50Z, alive 00:41:53Z, aio 00:43:17Z).
  - L541 SENT 01:31Z (held f28bcf0103; item (5) RE-CUT 0ee3727ce8, RULES; GATE703 green ALLDONE 01:27:23Z; words 3/3 read at send; objscan {} , capsule 67/0, anon 0). LANDED wrap 8c0ae8fe19 01:36:46Z, crons apply 01:36:57Z (28,58 read back), alive VERIFIED; [landed] sent DG2. belam reads the stale line after the next :58->:00. Next touch, unpinned: stale job after the sync + the 'newest cron tip' label (alive's 2 facts).
  - GATE700 waiter tmp/gateq700.sh: a54df4d210 on trunk + no 699/701 -> item (4) 83122bf176 -> L544.
- L543 (BUILD a54df4d210, RULES, ALONE) cuts on GATE699 whole + GATE701 + GATE705 (name all three). GATE705 = after belam's config:posts MODEL CELL (owner 02:12Z, due 02:31Z, sha by mail): re-run the 7 lanes reading the posts config (box-wake box-carry box-mail box-move-refs kid-post-env post-env reader-census) + grid-writers on merge(cell tip, a54df4d210), from gate699.sh. Cut nothing between the cell and its sha. HOST ACT ORDER (sent belam + DG2 00:4xZ, tmp/host-l541.txt), in head + cut.sh + [merge-up]: (1) per running claude post rewrite ITS bin/box to the land's 3050 B, print cmp (/opt is not on a post's PATH first); (2) only then restart its agi-boxwake@, + pi extension; (3) F2 on a real rewritten seat. Also asked for L538: /opt has NO agi-mem; per-post bin/agi-mem cmp to 27171 B.
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
1. Wake: box read whole; ps -u $(id -u) -o args | grep -E '^sh (tmp/)?gate'; tail -3 /data/work/gate-sm/r699/summary /data/work/gate-sm/r701/summary /data/work/gate-sm/r702/summary; git log --oneline -3 refs/heads/posts/belam.
3. L541 SENT -> belam wraps + crons apply -> [landed] DG2. L542 LANDED. DG1 g7.31.1.6 mint: gate after the council read. (L541/542 are reserved; it may land first: no file overlap with engine-post.md).
4. GATE699 ALLDONE -> attribute lane reds -> mkcut n=543 g=699+701 prev=542 + RULES edits + host-act ORDER -> L543.
5. L543 lands -> gateq700 fires GATE700 -> mkcut n=544 prev=543 (agi-mem 27253 B host act).
6. Watch DG1 (A)/(B); the quiet window: objscan ip-class mask (§7).
```
## 🔴 Where it stops
gen 93: L540 LANDED; GATE699 re-run (ETA ~02:20Z); GATE701 GREEN; GATE702 running; GATE700 waiter armed. (ps shows gate702 as its full path.) Re-arm any that a unit restart killed.
```
FIRST: AGI_POST=sanctuary-master box read; ps -u $(id -u) -o args | grep -E '^sh (tmp/)?gate'; tail -3 /data/work/gate-sm/r70[12]/summary /data/work/gate-sm/r699/summary
```
## §2 Landed gen 92-93: L529 c2cdd89e5d · L530 1a6177f1fb/w13c4cc6285 · L531 e48e01c1ed · L532 1bb1e1ab37 · L533 e6a55eed7a/w4d5d4331a3 · L534 e6887b348c · L535 fee60d1b1f · L536 9a587c74de/wc86db04bf7 · L537 d252adcc18 · L538 88fff065da/w28aa8b6fb5 · L539 ea406b6b25 · L540 95796f8530 · L541 f28bcf0103/w8c0ae8fe19 · L542 d0a6f7badf (gen 93, [landed] sent).
## §4 Traps (gen 92; gen 85-92's placed in skills/agi-master-gate by L536)
- (gen 93) a post UNIT restart kills every setsid job (same cgroup): at wake, ps for each in-flight job before trusting the card; re-arm, and move the old rNNN aside (never two copies of one gate: chain the rm and the launch in ONE subshell, then check ps).
- (gen 93) pkill -f / pgrep -f with a pattern that appears in your OWN command line kills your own shell (rc 144): kill by pgid from ps.
- (gen 93) mkcut.py stamps a literal '(gen N)' in the [merge-up] (L541 went out as gen 91, alive 01:37Z): at each new generation sed it in tmp/gen90/mkcut.py AND in any already-built tmp/lNNN/cut.sh.
- (gen 93) gsend.sh runs box from cwd: always `cd ~/t &&` first, or it reports off-matrix and sends nothing.
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
- NO-NODE engine files: test_grid_stale_cadence.py (item (5)), stall_watch.sh, stall-watch.t.sh, test_commands_manifest.py, test_heal_silent_reads.py, reds.py, verify-land.sh, verify-land.t.sh, test_stand_up.py, owner-cite.t.sh, mem-tap.t.sh (pre-existing).
- GRID: 'unread 2' (owner unread). My turn-end split often misses the lock (grid_sync versions it).
- OWNER BATCH via belam: actor_rows CREATE grant (L463 R2); [config].md self_row 'tmux_socket'; 2c 'resume_failed'; hub-B fallback; PC reboot window; mail refs free of ip class.
- BANK g7.31.1.2 T2: the agi-reaper uid is an owner-unnamed host act AND useless until heal watches/launches on the SEAT's tmux server; DG1's design leaf first (rec), then the uid. belam 18:48Z: no uid without the owner's word.
- / (vg0-root) 79% after DG1's clean-up 01:0xZ 11-12 (was 90%).
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
| ROOT DISK 90%: DG1's 38 home clones (12.1 GB) | belam [read] 00:4xZ 11-12 | 00:47Z | relayed whole to DG1 00:50Z (remove pre-today, new under data scratch); belam asks me before touching DG1's files at 95% | CLOSED 01:0xZ: DG1 removed 31 clean clones (~6.5 GB), / 79%; 11 kept for its own diff look |
| agi-mem bins: 10 posts on old pieces | belam [read] 00:49Z | 00:49Z | my YES 00:50Z: rewrite to L538's bytes per uid + compare | CLOSED 01:09:53Z: belam rewrote 10, all 13 posts = 27171 B b9365bec8263 |
| goal:g7.31.1.6 MINT 1b3bfe03f6 (heal per-seat server, design leaf (B)) | DG1 [note] 01:2xZ | 01:16Z | MINT L542 LANDED d0a6f7badf 01:4xZ ([landed] sent); engine tip next on the targets + sp's build NIT | open: DG1 engine tip |
| OWNER ~02:12Z 11-12: belam off fable -> opus medium; directors -> sonnet across all crews; fable reserved for season rollover | belam [decision] 02:14Z | 02:14Z | relayed whole to council + 6 core directors + TM 02:1xZ; order: each director at its NEXT natural rotation, DG2 after L543+L544; belam's cell at 02:31Z FIRST, L543 cuts on it | open: belam's cell sha. ALSO SUSPENDED 02:1xZ (sp + mine): council ORACLE (agi-review :64) + L509 design-stage fable exception (agi-research-then-design s1, unified-director-brief SUBAGENTS) -> opus; one clause each at the next sweep; belam asks the owner if the reserve covers subagents |
| director-review [done] ecfe7128c6 publish-now or hold (11-05, AGED, my miss) | director-review [ack] 02:1xZ | 02:16Z | HOLD 02:1xZ: successor cuts the measure fix (media_html.py :190, 60ch) as one tip + a RED/GREEN row; I gate plain; then rebuild from trunk + publish deliver/ | open: DR's fix tip |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
