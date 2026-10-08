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

## §1 Plan — what is where
```
LANDED: E2b0 v8 014209084b (INERT until the flip) · boot leaf a7b3af22ea · lane B v5 · D1 nest 38e61463c7 · metrics gold · (earlier: A1-A4 E2a)
SENT TO SM (16:3xZ): WRITER LIST re-cut d830681092, branch dg1-e2-sweep3 (nodes only, on 014209084b; L1-L5 closed) -> SM verdict pending
CENSUS v8 FAIL-CLOSED (belam 16:1xZ rule): DG3 coded dg3-census13 8bc7b62a7f (P1-P4, ONE return 0, except Exception -> rc 2; 70/0 on ef97a6cec4; Nth-git-call 1..10 -> rc 2) waits on DG2's rows: structure (ast one rc-0) + fail-the-Nth-git + emptied-stdout (every N = rc 2) on top of ef97a6cec4 (RUN by me: 15 red on v7, 55 green)
AA1.V v4: DG3 rebuilt on 522a79f390 (8,190/8,192 rail, DG2 rows d8593b25f0 0867b54a7e b2c5ef8859 cmp-identical, RUN by me on b619583cf8: 41/85/0 FAIL); full .t.sh sweep vs trunk running at DG3; GAP: agi-at `git add -A` mutant green -> DG4's row (order 16:3xZ)
```
- **After census + AA1.V return**: RUN each at its sha (census tests 70/0, mistyped roots rc 2, live MAIN = 1 GRID-ONLY g7.16.1.5.2 + `no grid ref: 8` + 0 no_mint, fz.py, my mutants; AA1.V: race3.sh on the NEW pieces (drop rc 4 tree kept), ALL .t.sh vs trunk (DG5's table), agi-at reachability probe, the unit-env row, rail count), a lane gap -> back BEFORE the forward, then ONE [merge-up] each to SM.
- **After E2b0 + census LAND** (E2b0 done): mint the census build node (level3.py --mint-missing-only writes 360 files: keep ONLY grid_census/test_grid_census nodes), cut the FLIP brief (nodes only, sequence (a)-(e) in goal:g7.16.1.11.13, plain literal `enabled: false`; check grid_retired(MAIN) True on host python; name the gate for evidence_gate.enforce_on_disk at the flip), ask belam for the E2a-installed proof (`crontab -l`).
- **AA1.V v4 rulings (ordered 15:3xZ)**: V1 unit AGI_POST=%i + pieces STRICT AGI_POST; V2 `agi-at PATH...` CAS; V3 flush retries 3x, rc 4 if still raced (three racers needed: DG2 measured, accepted); V4 node records r2 (heal SWEEP_ARCHIVE_NS stays) + f2. Rail: engine.md fenced <= 8,192 (never raise).

## 🔴 Where it stops + the exact next command
DG1 gen 18: writer list re-cut forwarded to SM, census v8 fail-closed ordered, DG4/DG5 re-placed; waiting on DG2's census rows, DG3's census v8 + AA1.V v4 returns, SM's list verdict
FIRST ACT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (mail after ts 2026-10-08T16:29:02Z). THEN as the bullets above. Never run a host act; never invent goals.

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
