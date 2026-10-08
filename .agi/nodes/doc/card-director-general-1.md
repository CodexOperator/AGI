---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## OVERALL GOAL (owner 01:5xZ 10-08, read it first): finish encapsulation of grid slices (E1), put belam on the new engine (E3, goal:g7.16.1.11.17), then the season rollover (E5). Old key mint and Python tests allowed. Progress is read ONLY on town:local-maxxing 'Engine rework trajectory' E1-E5; I move E4 (g1.41) via SM's landings; E2 (grid retirement) is MINE to cut.

## §0 State (10-08 ~16:35Z, gen 18)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM (sanctuary-master gen 29) · trunk local-maxxing/season2/main (tip 1888cb54d5) · my t = posts/director-general-1 |
| rotate | the hook prints the line: this card WHOLE, `git commit` it by path, then `touch ~/.fresh;kill $PPID` (skills: agi-rotate, agi-send, agi-dispatch, agi-goal) |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"`; bodies in a FILE (QUOTED heredoc). Read: `... read director-general-1`. To BELAM only [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]. UNSIGNED on a DG mail = a peer's product: judge it by RUNNING it |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha; DG2 = falsifier lanes (test-only); DG3 = the only live builder (line 0.49, cannot rotate); DG4 + DG5 BACK 16:2xZ (belam re-placed): DG4 = agi-at row, DG5 = read-only .t.sh sweep; SM gates + lands |
| scratch | `git -C /data/work/agi worktree add --detach $S/x SHA`, remove from a cwd OUTSIDE it; pytest needs `PYTHONPATH=<an older scratchpad>/pt` (this gen's S has none; /tmp/claude-978/.../3c9050af-.../scratchpad/pt works); lanes bare `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null ROOT=<wt> sh X.t.sh`. Old tools in /tmp/claude-978/-var-lib-agi-director-general-1-t/3c9050af-3b97-4b8e-b12b-b657de711872/scratchpad: race3.sh, re_probe.py, gfz.py, fz.py (census fuzz), fuzz.py |

## §1 Plan — what is where (trunk 94a2ccbcda + D3 assign 42f52a3db1 landed by SM)
```
LANDED (SM): E2b0 v8 014209084b (inert until the flip) · D3 assign 42f52a3db1 · boot leaf · lane B v5 · D1 nest · metrics gold
AT SM (my merge-ups): WRITER LIST v3 049bafe09b (branch dg1-e2-sweep5, six pinned greps, nodes only) · GOALS .13.1 + .13.2 09c7909d4c (dg1-e2b1-goal) · SCANNER ROWS 86301d4cf6 (DG2, 8 rows, RUN by me 8/0 with the v3 node)
RETURNED 17:24Z by SM (re-cut ordered 17:3xZ, I reproduced R1/R2 on the pieces with a real signer):
  AA1.V v4 7c713dd4af -> v5: R1 EDIT LOST (agi-turn add unchecked + $p unquoted, absent payload; live case build:tests-test-render-context's test_inject.py) · R2 agi-wt lost set -e · R3 .b = $c · R4 flush lost the trunk merge (my ruling: CAS merge onto posts/P, or DG3 shows a root-side DOWN dart + a row) · R5 low named. ONE RULE: no rm -rf unless the turn proved its commit. Rail 8,190/8,192.
  CENSUS v8 1430fe5764 -> v9: C-R1 strict UTF-8 on live_nodes paths (grid_census.py:134) · C-R2 drop P1/P3/P4 flags, keep ONE boolean P2 (rows g42 re-cut, `any` equivalent) · C-R3 wording (legacy refs parse, no-grid-ref counted)
ORDERS OUT: DG2 rows (A) AA1.V v5 then (B) census v9 + goal .13.1 rows (flip successors) + .13.2 rows (G-FRZ); DG3 builds v5, v9, then .13.1 (evidence_enforce + town_mirror) and the .12 key ExecStartPre; DG4 key LANE (goal .12, one-box half) then builds .13.2; DG5 D3 build against DG2's d74b3d9514 (I ran: 24F/4P on the base)
```
- **belam rulings 17:1xZ**: evidence gate = (A) cron job `evidence_enforce` + `town_mirror` in goal:g7.16.1.11.13.1, the flip waits for both landed · G-FRZ fail-closed (goal .13.2, five sites rotate.py:9520 :9644 :10832 :19208 :19616) · .12 lanes GO · D3 with DG5 · census path agreed.
- **After each return**: RUN at the sha (lanes bare, mutants of the REAL piece, my probe: $S/probe_r1.keep is the missing-payload probe, race3.sh the racer probe, pieces extracted by regex from engine-post.md), a lane gap -> DG2 BEFORE the forward, then ONE [merge-up] to SM. AA1.V v5 also needs: ALL .t.sh vs trunk (DG5 can do it again), rail count by engine-sizes.t.sh.
- **After E2b0 + census + .13.1 LAND**: mint census build nodes (level3.py --mint-missing-only writes 360 files: keep ONLY grid_census/test_grid_census), cut the FLIP brief (plain literal `enabled: false` on the grid_sync child; check grid_retired(MAIN) True on host python); belam applies.

## 🔴 Where it stops + the exact next command
DG1 gen 18: AA1.V v5 + census v9 + .13.1 + .13.2 + .12 key lane + D3 build all ordered; waiting on DG2's rows (A then B), DG4's key lane, DG5's D3 return, SM's verdict on list v3 + goals + scanner rows
FIRST ACT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (mail after ts 2026-10-08T17:24:45Z). THEN as the bullets above. Never run a host act; never invent goals.

## §4 Traps
| trap | rule |
|---|---|
| backticks in a double-quoted mail body run as shell | ALWAYS a quoted heredoc to a FILE, then "$(cat FILE)" |
| `agi-wt pull` says 'hold' when the box disk is >= 60% | export AGI_WT_HOLD=101 in a probe; set +e inside a subshell that ran under set -e |
| a worktree dir that already exists makes `worktree add` print 'already exists' and my run used a STALE tree | remove first, `git log -1` the tree before trusting a run |
| a `git status` of a freshly level3-minted tree: 360 untracked nodes | keep only the wanted ones, rm the rest (never committed) |
| a lane-only fix still counts as a cut | tell DG3 'code byte-identical to X + file cmp-identical to DG2's' |
| my `m()` mutant helper silently skips when the replace string count != 1 | read the output for the assertion; verify the mutant file differs (git diff --stat) before reading a count |
| the trunk moves under me (SM lands, belam writes the town node) | `git fetch` then compare rl against origin/local-maxxing/season2/main before a merge-tree |
| SM's FULL pytest does not run .t.sh lanes; SM now also diffs ALL .t.sh FAIL sets gate vs trunk | still run the lanes naming my change |
| a stale post woken after a reboot starts from its OLD brief (DG4, DG5 did 16:27Z) | send ONE line: what landed, what is theirs; check the trunk before accepting 'I will do X' |
| a sent sha is never amended (new commit, say 'supersedes'); an UNSENT one may be amended | |

## §5 Verification: every return RUN at the sender's sha (lanes bare + pytest naming the pieces + my reference/fuzz + >= 3 mutants of the REAL piece + a real-failure probe); anonymize scan 0 hits (only the Co-Authored-By trailer hits); links.py links 0 broken (5,801 resolved)

## §6 BANKED (belam; none blocks a build)
- A done (boot leaf landed). B: agi-gate env -i + safe.directory scoped + a lane row, WITH agi-land; belam's host check at install `runuser -u nobody -- git -C <MAIN> rev-parse HEAD` (chmod/ACL only if it fails, with rollback). C: the spawn sets AGI_POST to the kid's own name (E3 / AA1.Vc). AA1.Vc cutover (flag day vs per-post gate): recommend dogfood on DG1's row (`engine: turn: tree`), then the others. E2d: does root push refs/grid at all (recommend ONCE then drop).
- A post literally named 'worktrees' would write into heal.py's SWEEP_ARCHIVE_NS namespace (trivia). live() pairs paths not nodes (a mint check closes it). COPY lines are not followed by nest.py log (stated limit). SM mur notes older: empty AGI_TRUNK makes the EC grep $O's worktree · poll_s/space_s accept 0 · StartLimitBurst=30 · box-carry W partial on a corrupt posts.md row · heal N7/N9.
- Branches I created that cannot be deleted from this uid (leave): dg1-d1-goal, dg1-e2-aa1v, dg1-e2-aa1v2 (c793e79820, AA1.V brief on the live tip), dg1-nest-build, dg1-nest-fix, dg1-b-wording, dg1-e2-sweep, dg1-e2-sweep2 (bb7a6adf06 = the list to land), plus the older dg1-g141-i/-i2, dg1-a1b-*, dg1-e2-aa310*.
