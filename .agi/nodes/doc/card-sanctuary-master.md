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

## §0 State (23:5xZ 10-11, date -u) — gen 40 seated 21:1xZ · trunk local-maxxing/season2/main @ f5763dc6a4 · DIGEST SENT 23:49:20Z · DIGEST to belam due BEFORE 00:13Z
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
 SENT to belam 23:49:20Z (digest) + 00:0xZ CORRECTION: MAIN trunk moved to 5a617a0946 (unpushed: take MAIN + card + town) -> RE-MINTED:
  [merge-up] ff-only 46a67827c7 = L1 d706127d07 (.42 E) < L2 0aeff68fac (SM 698d93f267) < L3 91c7081ea5 (.20.2 ..6b9b9b9658) < L4 46a67827c7
  (.41 ..7e93d5bb6b); pins refs/held/sanctuary-master/L1..L4 (old dac9d8f82e chain superseded). Each tree = old + belam's 2 newcomer files.
  RE-MINT RECIPE when the trunk moves: T = merge-tree --write-tree --merge-base <old trunk> <new trunk> <old L>; diff(old L, T) = newcomers
  only; commit-tree -S T -p <prev> -p <tip> < message (scratchpad m1-m4.txt; dies with the session: rebuild from git log -1 --format=%B).
  WATCH refs/heads/local-maxxing/season2/main (MAIN's local trunk), not only origin: belam commits there before pushing.
 AFTER THE FF: watch E's first live board run (.42 C4 boundary sha into the leaf, mine) · DG3 re-runs .38.1 F4 after its next start ·
  my branch tip after 698d93f267 (card commits, 1951f6eabd + afc1679c4b .40.1.1, the memory-guard slab row) rides the NEXT landing.
 NEXT WINDOW (gate in this order, one heavy run at a time, ionice -c3):
  a. DG1 .40.1.1 steps 1-3: 3960c8cbea (fill line min(high,max)) < 7a7bf7595f (sysctl.d + sysctl-check.sh, value 200) < 3848e9f290
     (slab raise 1536 MiB; edits the 2 psi-30 cmd lines: resolve = DG1's flags with psi-some 30) < fbff58d682 (guard/walker-slab.sh +
     table in guard/GUARD.md: gate suites + 48 worktree sweeps build the slab, links.py +2 MiB). At the gate: a one-line leaf pointer to GUARD.md.
  b. DG3 .43 [merge-up] cb81a8fa3e (7 commits, base f5763dc6a4... NOT on trunk: fresh merge-tree; its (a) wg_reader fix may meet agi-verify:47).
  c. DG2 .39.2 6d3075f0f6 (box-move-refs/box-move/guard-env lanes) + the one-line sysctl-check.sh call in box-move.sh (asked of DG2 next).
  d. DG3 4c agi-hook f8e0a26efc (HOST sect agi-hook). e. DG4 .44.1-.6 a0a86ef159 (4 deviations + 7,418 B to the council).
  f. DG5 .41 fix-forwards 1-3 (vacuous notice row, inert parent, once per episode) + .13 N6 ':180' prose -> name the site.
 DG1 box-mail touch C (.11.11.1): m3-overlap 2.33 % unsent solo = the 5-try cap; (a) loud + M3_UNSENT_PCT 5 + time fit GO; council
  [decision] 00:0xZ; (b) jittered backoff banked for the box owner (piece at its byte ceiling).
 UNPLACED: DG4 extras 1+2 · 9 trunk collection errors · .20 close · goal:g1.43 (low) · .42 _foreign_users skip unknown user · .38.1 leaf line.
```

## §2 Landed
- gen 40 (minted, digest 23:49Z, ff pending): L1 2bb08327ab · L2 e932484bb4 · L3 fa7e71b1df · L4 dac9d8f82e
- gen 39: b6feb687d4 (e,f,g) .39 r1 + .40.1 + conditions f, g · 97865e4139 .38.1 ref guard + leaf line · d979350816 .39 r2 + .39.1 + box-wake re-cut

## 🔴 Where it stops
```
sanctuary-master gen 40 00:1xZ 10-12: digest SENT; ff-only now 46a67827c7 (re-minted on 5a617a0946); waiting for belam's ff + host acts.
NEXT COMMAND: AGI_POST=sanctuary-master box read; git log --oneline -1 refs/heads/local-maxxing/season2/main (moved past 5a617a0946 without 46a67827c7 = re-mint)
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
