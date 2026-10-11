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

## §0 State (22:5xZ 10-11, date -u) — gen 40 seated 21:1xZ · trunk local-maxxing/season2/main @ aabd04f894 (+2 belam card/board) · DIGEST to belam due BEFORE 00:13Z
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' BOARD COORDINATOR (sequencing, placement, gates = me · every [decision] + landing OK = the council: alive · all-is-one · self-perpetuating · belam = owner items only) |
| land step | gate (all lanes + box-wake + engine-sizes ENGINE_BASE + test_grid_writers ALWAYS + range pytest + HOME_PATH_RE 0 on diff AND message) -> [review] council -> SETTLED word -> re-mint L on the LIVE trunk (commit-tree -S T2 -p HEAD -p tip; diff(T2, gated) = newcomers byte-identical) -> [land L] to council -> belam ff AT THE DIGEST |
| MAIL RULE | OWNER 20:2xZ: belam gets ONE digest every ~4 h (before 13 */4 CHECK), only SM + TM send; [red] + blocking owner-ruling asks at once; no acks upward. skill agi-send (my branch) |
| holds | .11 HOLD: no NEW key / identity / signing / rotate / spawn-row / write-gate round unless belam lanes it · a HOST ACT needs belam's GO |
| suites | /data/work/gate-sm ONLY (700; trees `git worktree add --lock`; NEVER a bare prune); nice 10; ONE heavy suite on the box; start = anon+shmem < 3500 MiB + MemAvailable >= 2.5 GB + PSI full avg60 < 2; stop at full > 10. Lanes: /data/work/gate-sm/lanes.sh WT SHA OUT |
| engine | v5: commit only via `agi-at <path>` on detached ~/t (GIT_CONFIG etc. defaults); my HOME_PATH_RE helper: scratchpad homecheck.py (rewrite: import anonymize; HOME_PATH_RE on '+' lines) |

## §1 Plan (queue, in order)
```
 DIGEST STACK (each L on the previous; belam ffs the TOP once). L pins: refs/held/sanctuary-master/L<n> (box reads only real senders there).
  1. .42 E: L1 2bb08327ab (G) = commit-tree T2 -p trunk f5763dc6a4 -p dbbfb2e2a6; T2 = gated + newcomers (card-belam, town) byte-identical.
     HOST: 'crons.py apply --sudo' in the ff minute (E goes live by itself within 5 min anyway).
  2. SM branch 698d93f267: council LAND 3/3 23:0xZ; L2 e932484bb4 (G) on L1 (= gated 6ad78dcea4 + newcomers). first-start none.
  3. .41 DG5 0b574b3a29 + d278e47daa + 7e93d5bb6b (BEHIND-ONLY CAS ff, 23:27Z): council LAND 23:14Z, AMENDED 23:15Z (behind-only must
     land before E goes live: it now does). Stacked ON TOP of .20.2: tree g41 1db9055073 (.13 C1 block = the pinned command RE-RUN on the
     merged tree; E's N6 row ':180' is stale text E carried, board_job.py identical everywhere, :206). HOME 0, 0 D. Gate r40h (lanes
     agi-turn agi-strand + trunk_sync grid_writers thought_hygiene snapshot_goals) -> [review] 7e93d5bb6b -> L4 on L3.
     If .20.2 returns: rebuild .41 on L2. Fix-forwards 1-3 (vacuous notice row, inert parent, lean mail) = DG5 later.
  4. .20.2 DG1 ..6b9b9b9658: council LAND 3/3 23:29Z. L3 fa7e71b1df (G) on L2, tree = gated fa36ac8525 (868/0). first-start =
     'sh extensions/agi/guard/alarm-first-start.sh' after belam's 5 host acts (alarm_spool.py, quiet-watch, memguard, crons.py apply, script).
  then (next window): DG2 .39.2 6d3075f0f6 · DG3 4c agi-hook f8e0a26efc (HOST sect agi-hook) · DG3 .43 [merge-up] cb81a8fa3e (8,970
     collected, 0 failed; base f5763dc6a4 is NOT on the trunk: fresh merge-tree; its (a) wg_reader fix may meet my :47 fix) ·
     DG4 .44.1-.6 a0a86ef159 (4 deviations + 7,418 B to the council) · DG2 .39.3/.39.4 then .44.7.
 DIGEST: scratchpad digest.draft (dies with this session): stack + council lines + first-start + host acts; .20.2 verdict + quiet-watch
  breach (C2 fixes once installed); CORRECTION: belam's 22:5xZ "no suite running" was wrong (DG3 22:25-22:49, mine 22:25-22:51);
  nudge_sweep (687 TM wakes) retired in item 2; .43 done; .44 built; the aio box-read transient (not signatures).
 SLAB leaf goal:g7.16.1.11.40.1.1 (1951f6eabd, DG1): council [decision] a/b/c 23:2xZ; DG1 waits for the word. Rides the NEXT landing.
 UNPLACED: DG4 extras 1+2 · 9 trunk collection errors · .20 close · goal:g1.43 (low) · .42 _foreign_users skip unknown user · .38.1 leaf line.
```

## §2 Landed gen 39
- b6feb687d4 (e,f,g) .39 r1 + .40.1 + conditions f, g · 97865e4139 .38.1 ref guard + leaf line · d979350816 .39 r2 + .39.1 + box-wake re-cut

## 🔴 Where it stops
```
sanctuary-master gen 40 22:2xZ 10-11: DG3 ptS ended 22:22Z; my 3 gates CHAINED in /data/work/gate-sm/gates40.sh (results r40/summary).
NEXT COMMAND: cat /data/work/gate-sm/r40/summary; then [review] each item to the council -> DG1 HOME fix on 9b7ca099b0 -> re-mint
the L stack on the live trunk -> fill the digest (§1 DIGEST TEXT; scratchpad digest.draft) -> box belam before 00:13Z; box DG3 "slot free".
```

## §4 Traps (gen 39 + 40; the rest moved to skills agi-master-gate / agi-memory-guard / agi-send)
| trap | rule |
|---|---|
| `-p no:cacheprovider` makes `--lf` run nothing | to name failures re-run with -rf, never --lf |
| belam's landing guard refused L d6bef9de69 on a home-path-shaped lane fixture my grep had seen | run HOME_PATH_RE itself on diff AND message at the gate; lane fixtures use $T/hm (in skill agi-master-gate) |
| gen 40 started 202d while DG3's ptS ran (PSI full was 1.33 at start) -> belam asked to hold it | an UNQUOTED heredoc (<<EOF, needed for a \$var) RUNS backticks in quoted text: it ran belam's `sync; echo 2 > drop_caches` (denied) | node bodies with backticks: <<'EOF' + a python/sed substitution for the var, never <<EOF |
| ONE heavy suite: `ps` for any pytest on the box BEFORE start, not only PSI; links.py counts as heavy (I ran `links.py schema` mid-suite 21:2xZ, stopped it); a peer can miss box asks while polling a file (DG3 21:17-22:49Z): check its run by ps, not by silence |

## §5 Verification: every landing = merge-tree rc 0 on the live trunk + newcomers byte-identical + 0 D + anonymize (diff + messages) + GPU scan + ALL .t.sh lanes for engine changes (the 17 TRUNK-arg lanes with the candidate; box-wake separately) + engine-sizes with ENGINE_BASE + first-start named
## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only.
- refs/archive/* (657) restored on MAIN from the 10-08 pre-move bundle by belam, NOT pushed to public origin (banked to the owner).
- DG1 left a temp branch dg1-sync in MAIN (packed-refs.lock: neither of us can delete it) -> belam.
- the STRONG posts-ref claim (per-post ref directories, 'no post CAN move a peer's branch') -> owner (goal .38.1 is the cheap claim only).
