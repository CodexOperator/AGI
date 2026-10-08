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

## §1 Plan — what is where (trunk ec48b36c48 at 17:58Z)
```
LANDED (SM): E2b0 v8 · D3 assign · boot leaf · lane B v5 · D1 nest · metrics gold
AT SM, all mine, all nodes/tests only: WRITER LIST v4 4f07249ab4 (dg1-e2-sweep6; C1-C8 pinned, SM WL-1..3 done) · GOALS .13.1/.13.2 v2 6a19088e08 (dg1-e2b1-goal2; G-1..G-5) · KEY CHAIN nodes 34af2007ab (experiment + verdict proved, dg1-aa2-key-chain) · hypothesis note cb11d1526d + DG4 key rows bb574d935d (gate open) · SCANNER rows 86301d4cf6 (DG2 re-cut ordered: strip line numbers, C1-C8)
AA1.V v5 (v4 7c713dd4af returned): DG2 rows d44c06062c RUN by me (44 ok/19 FAIL on v4, polkit 0 FAIL); DG3 builds (CAS merge in flush = the DOWN dart charged to AA1.V, belam (a); .p one path per line, --pathspec-from-file; no rm -rf unless the turn proved its commit; rail 8,191/8,192, no row moves out; agi-at [raced] label = named limit)
CENSUS: belam 17:4xZ asks if it gates the flip; I answered NO (recommend advisory/drop; the only GRID-ONLY node is goal:g7.16.1.5.2's 2-line note in refs/grid 166b70d5ac) and HOLD v9 until belam says build/drop. v8 1430fe5764 stays RETURNED, un-landed
.13.1 (evidence_enforce + town_mirror; DG2 rows c3a114bd3a + G-4/G-5 update, DG3 builds) · .13.2 (strict veto reads, SIX sites, ImportError=HELD; DG2 rows, DG4 builds) · D3 goal .22 (DG5 build ba14f648ae; DG2 cache/season/--verify rows, then DG5's new commit; inject.py OUT of scope)
```
- **belam rulings 17:4xZ**: (a) ONLY the DOWN dart, cut only if net <= 0 (the flush merge is that) · (b) key chain closed (done) · (c) census question answered, v9 held · .12 other hypotheses (lap, tier, K1, stores, ladder) = season 3, NOT cut.
- **After each return**: RUN at the sha (lanes bare, mutants of the REAL piece, probes: $S/probe_r1.keep, race3.sh, pieces by regex from engine-post.md), a lane gap -> DG2 BEFORE the forward, then ONE [merge-up] to SM. Reproduce every residue on the bytes before ordering.
- **Flip prerequisites left**: .13.1 landed (rows+build) only; then FLIP brief (plain literal `enabled: false`; belam applies). Mint census build nodes only if census lands.

## 🔴 Where it stops + the exact next command
DG1 gen 18: everything ordered; waiting on DG2 (scanner re-cut, .13.1 rows update, .13.2 rows, D3 cache rows), DG3 (AA1.V v5 build, .13.1 build), DG4 (.13.2 build), DG5 (D3 new commit), SM (verdicts on list v4, goals v2, key chain, key lane, scanner, D3)
FIRST ACT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (mail after ts 2026-10-08T17:55:49Z). THEN as the bullets above. Never run a host act; never invent goals.

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
