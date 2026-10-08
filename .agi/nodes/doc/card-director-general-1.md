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

## §0 State (10-08 ~18:25Z, gen 18 -> 19 ROTATING at the line 475214/1000000)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM (sanctuary-master gen 29) · trunk local-maxxing/season2/main (tip 1888cb54d5) · my t = posts/director-general-1 |
| rotate | the hook prints the line: this card WHOLE, `git commit` it by path, then `touch ~/.fresh;kill $PPID` (skills: agi-rotate, agi-send, agi-dispatch, agi-goal) |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"`; bodies in a FILE (QUOTED heredoc). Read: `... read director-general-1`. To BELAM only [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]. UNSIGNED on a DG mail = a peer's product: judge it by RUNNING it |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha; DG2 = falsifier lanes (test-only); DG3 = the only live builder (line 0.49, cannot rotate); DG4 + DG5 BACK 16:2xZ (belam re-placed): DG4 = agi-at row, DG5 = read-only .t.sh sweep; SM gates + lands |
| scratch | `git -C /data/work/agi worktree add --detach $S/x SHA`, remove from a cwd OUTSIDE it; pytest needs `PYTHONPATH=<an older scratchpad>/pt` (this gen's S has none; /tmp/claude-978/.../3c9050af-.../scratchpad/pt works); lanes bare `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null ROOT=<wt> sh X.t.sh`. Old tools in /tmp/claude-978/-var-lib-agi-director-general-1-t/3c9050af-3b97-4b8e-b12b-b657de711872/scratchpad: race3.sh, re_probe.py, gfz.py, fz.py (census fuzz), fuzz.py |

## §1 Plan — what is where (SM trunk ~975bd1477f; all times 10-08)
```
LANDED by SM today: E2b0 v8 · D3 assign · key lane rows 6ddce0abc6 · AA2 key node be7bc26581 · key wording 975bd1477f · WRITER LIST v4 79238a68c9 · key chain (experiment + verdict) eb3fd09d05
RETURNED, mine to fix (SM 18:23Z, closed lists):
  (A) NODES round on the landed list / chain: writer-list FLIP NOTES (4) still lists W8 among 'exempt, named' (its row says no) · C4 title 'NO wildcard push exists' -> 'no --all / --mirror / refs/*' · P7 sensei.py:2373 is a comment (push_at is :2375) · experiment:g716111-aa2-key-onebox-agi-fresh 'verdict: pending' -> proved (links.py schema verdict-class 18 -> 19). Cut on the LIVE trunk, nodes only.
  (B) GOALS v3 (v2 6a19088e08 + fix rows 3246966bf9 branch dg1-e2b1-goal3; both sent): GV-1 .13.2 Negative (:43) forbids non-strict `_veto.read(` but the Invariants (:39) allow rotate.py:19601's best-effort active_gate read: exempt :19601 BY NAME in the Negative · GV-2 a row for the SEVENTH site rotate.py:10979 `except ImportError: pass` = HELD · GV-3 name the old-behaviour tests that change WITH the build (test_rotate_key_authority.py:429-440 asserts 'authority: OK' on ImportError; test_rotate_closeout_steps.py:1280-1288 / :1448-1455 patch only is_frozen, fixtures must write a well-formed free vetoes.md) + a write.py:1921-1927 row file (only test_write_veto_gate.py's frozen case exists) · GV-4 .13.1 :36 a row for the suite-lock deferral (lock held by a live foreign pid -> no rewrite, rc 0). v3 lands when the four are done: ONE commit on the live trunk, then [merge-up].
IN FLIGHT (release 18:21Z, io avg60 41; belam's [red]: NEVER dispatch while /proc/pressure/io avg60 >= 50): DG2: scanner re-cut (strip line numbers, C1-C8) -> D3 cache/season/HOME/--verify rows -> .13.1 rows update (G-4, G-5, F1, F2, GV-4) -> .13.2 rows (G-1..G-3, SIX+1 sites, F3, GV-1..3) · DG3: AA1.V v5 build (rows d44c06062c, RUN by me 44 ok/19 FAIL on v4; CAS flush merge = belam's DOWN dart, rail 8,191/8,192, .p one path per line, agi-at [raced] label = named limit) then .13.1 build · DG4: agi-fresh.t.sh lane fixes (umask 077 in sg(), refusal rows read sg.err) then .13.2 build · DG5: D3 new commit (ba14f648ae + --verify mark comparison, after DG2's rows; inject.py OUT of scope)
CLOSED: CENSUS dropped (belam 18:2xZ; v8 1430fe5764 un-landed, v9 never built) · the WRITER LIST frozen (no more doc re-cuts; findings = fix rows F1 migrate-* --write refuses when retired, F2 no plain fetch updates refs/grid after the flip, F3 callers report the retired no-op) · .12 other hypotheses (lap, tier, K1, stores, ladder) = season 3, NOT cut
```
- **The flip waits ONLY on goal:g7.16.1.11.13.1** (rows + build landed); then cut the FLIP brief (plain literal `enabled: false` on the grid_sync child; grid_retired(MAIN) True on host python); belam applies (`crons.py apply`). E2d (push refs/grid once, then drop) = his call.
- **After each return**: RUN it at the sha (lanes bare `env -i ... ROOT=<wt> sh X.t.sh`, pytest with PYTHONPATH=<an older scratchpad>/pt, mutants of the REAL piece, my probes: scratchpad probe_r1.keep / race3.sh), a lane gap -> DG2 BEFORE the forward; reproduce every residue on the bytes before ordering; then ONE [merge-up] to SM. Tags to belam: [merge-up] [decision] [rotation] [red] [rule] [complete] [owner] only.

## 🔴 Where it stops + the exact next command
DG1 gen 18 -> 19: list v4, key chain and key wording LANDED; goals v3 (GV-1..4) and the nodes round (A) owed; AA1.V v5 / .13.x rows / D3 rows in flight at DG2-DG5
FIRST ACT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (mail after ts 2026-10-08T18:23:38Z) and `head -1 /proc/pressure/io`. THEN (1) cut (A) and (B) as ONE nodes-only commit each on the live trunk (scratch worktree `git -C /data/work/agi worktree add --detach $S/n origin/local-maxxing/season2/main`, edit the goal / list / experiment files, links.py links 0 broken, merge-tree rc 0) and [merge-up] to SM; (2) run each director return at its sha. Never run a host act; never invent goals.

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
