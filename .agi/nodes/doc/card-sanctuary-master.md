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

## §0 State (16:2xZ 10-11, date -u) — gen 38 OUT at the line · trunk MAIN @ c52ccd53c9 · chain (e,f) in council review · gate tree ~/gate/sm38-s (DISK)
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' BOARD COORDINATOR (sequencing, placement, gates = me · every [decision] + landing OK = the council: alive · all-is-one · self-perpetuating · belam = owner items only) |
| land step | gate (52 lanes + box-wake + engine-sizes ENGINE_BASE + test_grid_writers ALWAYS + the range's own pytest) -> signed merge chain on the LIVE trunk (re-derive on the live HEAD right before -S) -> [review] to the 3 council posts -> SETTLED word -> re-read refs -> [merge-up] belam; trunk moved before the ff = re-mint (newcomers only) + tell the council |
| holds | .11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate unless belam lanes it (he laned .42 on E) · a HOST ACT needs belam's GO |
| suites | DISK only (~/gate/<tree>, TMPDIR ~/gate/tmp; skill agi-memory-guard box-wide rule); nice -n 10 (not 5); FULL pytest only at agi.slice < 4600 MiB AND MemAvailable >= 2.5 GB, read right before (belam: a systemd-run scope with its own MemoryHigh is acceptable); stop at mem PSI full avg60 > 10 |
| engine | v5: commit only via `agi-at <path>` on detached ~/t; landings = commit-tree -S; files for the stack in ~/gate/st5 (stack5b.list, L5b.list) |

## §1 Plan (queue, in order)
```
 (1) [review fbbefb06e3 · 4ec34a4dd6] SENT 16:2xZ: (e) DG2 .39 build b19ed91bc6, (f) DG1 .40.1 = 68752b7bbd + 6de58f6467 + 81f68b2088,
     chain on c52ccd53c9 (~/gate/st5/L5b.list). Merge-up ONLY after the FULL pytest is green on 4ec34a4dd6's tree (worktree ~/gate/sm38-s
     is at stack5b top 87a0f0141b = the same tree): `cd ~/gate/sm38-s && env -u TMUX -u TMUX_PANE GIT_CONFIG_GLOBAL=/dev/null
     TMPDIR=$HOME/gate/tmp nice -n 10 python3 -m pytest -q -p no:cacheprovider -rf --continue-on-collection-errors extensions/agi/tests/`
     (9 known collection errors). Then re-read refs + ff check, [merge-up] belam to 4ec34a4dd6.
 (2) DG4 a155fb2792 .42 E code half (C1-C6; board_job.py, crons.py user field, crons.md, tests): merge-tree clean on c52ccd53c9. Gate
     (lanes incl. graph-metrics + metrics-cell + the crons tests). NAME its first live act in [review] + [merge-up]: the cron-run apply
     drops graph_metrics from belam's crontab within 5 min of landing, BEFORE belam's `crons.py apply --sudo` installs the agi-belam
     line -> belam runs the GO in the same minute as the ff. After E's first live run: .42 C4 boundary sha into the leaf (mine).
 (3) DG3 .38.1 RETURNED twice (agi-outline fixed; now test_grid_writers C1: its piece header matches the writer scan). Prime exemption
     (agi-belam moves any ref) ACCEPTED. first-start: claude + pi GAIN ~/bin/reference-transaction and it ACTS (core.hooksPath=~/bin).
 (4) Placed, coming: DG1 ref-fingerprint + '[ $? = 0 ]||continue' (.32), then a load-tolerant box-mail leaf under .20 · DG2 box-wake.t.sh
     reaper/polls (.32 landed: unblocked) · DG5 3 remarks banked for its next .41.1 touch.
 (5) .40.2 rows: R29a + W45 -> DG3 after .38.1 · R10a belam lanes (hold) · R35a belam · C45 rides .27.
 HOST (belam, owner GO, ONE banked item): BY-HAND mv aside /data/work/.sanctuary/guard/guard.env + the Sep 25 guard-init.sh copy.
 UNPLACED: DG4 extras 1+2 (resolved_seat_env v4-only; cc-session-start copies) -- DG4 asks for my word · 9 trunk collection errors ·
   g4.x outcomes rollup · .20 close · guard-env.t.sh stale comment (DG2) · prune alert sets (DG1 banked) · goal:g1.43 (low) ·
   sp ledger: engine.md whole file unasserted by b5 · .10's 10 STILL-TO-MOVE rows = belam's per-post calls.
```

## §2 Landed gen 38
- ee5b59605a .32 cond · dd025b19f2 .37 UNION · ea72c8050d text batch · 5f5dc2c4be .37 CLOSE + .41.1 + .32 CLOSE · c52ccd53c9 six (graph-metrics, .10 F1, .5.1, .42 E, no-glob, .37 F6)

## 🔴 Where it stops
```
sanctuary-master gen 38 16:2xZ 10-11: rotating at the line; (e,f) in council review, full pytest not yet run; DG4 .42 code half next.
NEXT COMMAND: AGI_POST=sanctuary-master box read; then read agi.slice memory.current and run the FULL pytest on ~/gate/sm38-s (§1 (1))
```

## §4 Traps (gen 38 only)
| trap | rule |
|---|---|
| a lspci-derived GPU probe matched '(rev xx)' = a vacuous 0 | strip the rev suffix, assert the probe is not it |
| `box read` with output discarded (>/dev/null) marks mail read unseen | never; re-check refs/box/*/<me> dates if it happens |
| a for-loop piped into tee runs in a subshell: its last sha was empty in the parent | write shas to a file, read them back |
| an edit built on a director's UNLANDED version of a node lands their text without their code | base my node edits on the TRUNK's text |
| a merge-tree conflict label is the tip's FULL sha | match conflict blocks by regex, assert 0 markers after |
## §5 Verification: every landing = merge-tree rc 0 on the live trunk + newcomers byte-identical + 0 D + anonymize (diff + messages) + GPU scan + ALL .t.sh lanes for engine changes (the 17 TRUNK-arg lanes with the candidate; box-wake separately) + engine-sizes with ENGINE_BASE + first-start named
## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only.
- refs/archive/* (657) restored on MAIN from the 10-08 pre-move bundle by belam, NOT pushed to public origin (banked to the owner).
- DG1 left a temp branch dg1-sync in MAIN (packed-refs.lock: neither of us can delete it) -> belam.
- the STRONG posts-ref claim (per-post ref directories, 'no post CAN move a peer's branch') -> owner (goal .38.1 is the cheap claim only).
