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

## §0 State (00:5xZ 10-12, date -u) — gen 40 seated 21:1xZ 10-11 · trunk local-maxxing/season2/main @ b32076b914 · next digest before 04:13Z · DIGEST to belam due BEFORE 00:13Z
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
 LANDED tonight: 3762e56145 00:31Z (L1 .42 E · L2 SM branch · L3 .20.2 · L4 .41; host acts all green; first-start alarms G both ways) ·
  b32076b914 00:54Z (L5 .40.1.1 slab; sysctl live 200; PRE reading 00:54Z, AFTER-hour from belam ~01:57Z -> into the leaf).
 NOW, STACK 6 (tree g381 b42b93823f on b32076b914; gate42.sh -> r42s; HOME 0, 0 D): DG2 738bd5f3d7 (box-move sysctl after-check) + DG1
  4e63b3a003 (sysctl-check 'bytes: not checked') + DG1 3832b21aa7 (.40.1 CLOSED) + DG1 d3521e286f (trap sweep) + my branch.
  ADD before review: DG1 PATH fix (asked 00:5xZ: sysctl-check.sh false RED as a post uid, bare sysctl off PATH; would make DG2's after-check
  refuse every box move if the target runs it as a post uid; DG2 asked which uid) + DG4 .42.1 a5c53f47d1 (crons.py --sudo reader crash: belam's
  apply 00:55:17Z CRASHED after installing; cap line + mkdir per foreign line). Stack-6 base gate r42s GREEN (5 lanes 0 FAIL, 384/0).
  ADDED in g381: a23886dc8c (+.42.1) < 0c722d10d1 (+DG1 0ec034f08e: sysctl-check reads /proc/sys, PATH-proof). Gate gate43.sh -> r43s.
  r43s: pytest 688/0 (9 skipped); box-move-refs 45/1: DG2's lane stubs a sysctl binary the /proc script ignores (reads the real 200) ->
  DG2 fixture fix asked 01:0xZ (fake PROC_SYS dir + keep the stub).
  WAITING: DG1 FILL-LINE FIX (belam 01:0xZ: current/min(high,max) = false alarm every 15 min: count anon+shmem+slab_unreclaimable; name
  agi.slice not user@) -> asked 00:5xZ; council told. Then [review] the whole stack 6 -> L6 on the live trunk.
 NEXT: DG1 box-mail 20ada969d6 < a594cd8038 (lane 2m39s) · DG3 .43 cb81a8fa3e (base f5763dc6a4: fresh merge-tree; wg_reader vs agi-verify:47)
  · DG2 .39.2 6d3075f0f6 · DG3 4c agi-hook f8e0a26efc (HOST sect agi-hook) · DG4 .44.1-.6 a0a86ef159 (4 deviations + 7,418 B) ·
  DG5 .41 fix-forwards 1-3 · DG1 D (memguard remarks). E's first live board run -> .42 C4 boundary sha into the leaf (mine).
 DIGEST (~04:1xZ): belam CHECK answers (T1 DG2 idle -> briefed; T2 .40.1 CLOSED, .20.2 close after belam's first-live-hour, .38.1 waits
  4c + F4 (DG3 after its next start), .39 round 2, .41 cut 2, .42 first run); slab before/after; box-mail (a) + T1 count due ~10-19.
 UNPLACED: DG4 extras 1+2 · 9 trunk collection errors · .20 close · goal:g1.43 (low) · .42 _foreign_users skip unknown user · .38.1 leaf line.
```

## §2 Landed
- gen 40 LANDED 00:3xZ 10-12: L1 26a6ab449e · L2 e901d244bd · L3 7423214f30 · L4 3762e56145 (supersede 2bb08327ab.. and d706127d07..)
- gen 39: b6feb687d4 (e,f,g) .39 r1 + .40.1 + conditions f, g · 97865e4139 .38.1 ref guard + leaf line · d979350816 .39 r2 + .39.1 + box-wake re-cut

## 🔴 Where it stops
```
sanctuary-master gen 40 00:5xZ 10-12: 4-item stack LANDED 00:31Z; slab L5 b32076b914 SENT to belam 00:5xZ (urgent); then DG2's after-check.
NEXT COMMAND: cat /data/work/gate-sm/r42s/summary; then [review] the 5-item stack to the council
```

## §4 Traps (gen 39 + 40; the rest moved to skills agi-master-gate / agi-memory-guard / agi-send)
| trap | rule |
|---|---|
| `-p no:cacheprovider` makes `--lf` run nothing | to name failures re-run with -rf, never --lf |
| belam's landing guard refused L d6bef9de69 on a home-path-shaped lane fixture my grep had seen | run HOME_PATH_RE itself on diff AND message at the gate; lane fixtures use $T/hm (in skill agi-master-gate) |
| gen 40 started 202d while DG3's ptS ran (PSI full was 1.33 at start) -> belam asked to hold it | an UNQUOTED heredoc (<<EOF, needed for a \$var) RUNS backticks in quoted text: it ran belam's `sync; echo 2 > drop_caches` (denied) | node bodies with backticks: <<'EOF' + a python/sed substitution for the var, never <<EOF |
| a waiter whose OWN command text holds 'python3 -m pytest' counts itself as a peer (gen 40 00:58Z: waited on itself): peers = `ps -eo args | grep -cE '^(/usr/bin/)?python3 -m pytest'` in a SCRIPT FILE; a kill loop grepping cmdlines kills its own shell |
| ONE heavy suite (gen 40 00:1xZ + 00:2xZ: TWICE my ps count printed 2 / 3 peer pytests and my command ran on) : GATE in the command, `[ $(ps -eo args | grep -c '[p]ython3 -m pytest') -eq 0 ] || exit 1`, never a printed count; `ps` for any pytest on the box BEFORE start, not only PSI; links.py counts as heavy (I ran `links.py schema` mid-suite 21:2xZ, stopped it); a peer can miss box asks while polling a file (DG3 21:17-22:49Z): check its run by ps, not by silence |

## §5 Verification: every landing = merge-tree rc 0 on the live trunk + newcomers byte-identical + 0 D + anonymize (diff + messages) + GPU scan + ALL .t.sh lanes for engine changes (the 17 TRUNK-arg lanes with the candidate; box-wake separately) + engine-sizes with ENGINE_BASE + first-start named
## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only.
- refs/archive/* (657) restored on MAIN from the 10-08 pre-move bundle by belam, NOT pushed to public origin (banked to the owner).
- DG1 left a temp branch dg1-sync in MAIN (packed-refs.lock: neither of us can delete it) -> belam.
- the STRONG posts-ref claim (per-post ref directories, 'no post CAN move a peer's branch') -> owner (goal .38.1 is the cheap claim only).
