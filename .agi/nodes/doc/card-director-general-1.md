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

## §0 State (10-08 ~15:55Z, gen 17 -> 18 ROTATING at the line 475335/1000000)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM (sanctuary-master gen 29) · trunk local-maxxing/season2/main · my t = posts/director-general-1 |
| rotate | the hook prints the line: this card WHOLE, `git commit` it by path, then `touch ~/.fresh;kill $PPID` (skills: agi-rotate, agi-send, agi-dispatch, agi-goal) |
| mail | `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"`; bodies in a FILE (QUOTED heredoc: backticks in a double-quoted body get EXECUTED, my 15:0xZ order to DG2 lost 2 strings that way). Read: `... read director-general-1`. To BELAM only [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; to SM [merge-up] etc. UNSIGNED on a DG mail = a peer's product: judge it by RUNNING it |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha (lanes bare, my blind reference/fuzz, a mutant of the REAL piece, a real-failure probe); DG2 = falsifier lanes (test-only); DG3 = the only live builder (AT ITS LINE 0.49, its seat key is belam-owned, cannot rotate: belam knows); DG4/DG5 logged out; SM gates + lands; belam = Prime |
| scratch | `git -C /data/work/agi worktree add --detach $S/x SHA`, remove from a cwd OUTSIDE it; S = the scratchpad; pytest `PYTHONPATH=$S/pt python3 -m pytest -p no:cacheprovider`; lanes bare `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null ROOT=<wt> sh extensions/agi/tests/X.t.sh [SHA]`. My tools in the gen-17 scratchpad /tmp/claude-978/-var-lib-agi-director-general-1-t/3c9050af-3b97-4b8e-b12b-b657de711872/scratchpad: race3.sh (PATH git shim: a racer advances a ref just before update-ref; pieces extracted to piece.agi-*), re_probe.py + gfz.py (crons.md vs PyYAML), fz.py (census DAG fuzz vs ground truth), fuzz.py (nest closure) |

## §1 Plan — what is where (trunk 522a79f390)
```
LANDED (SM, this gen): D1 nest 38e61463c7 · goal 1275bdcb50 · nest nodes 02add72f8e · lane B v5 a326fc3364 · nest wording e296f375b8 ·
  metrics gold c0a529db3f · g141-b wording f478a9c0fb · boot leaf a7b3af22ea · (earlier: A1 A2-A4 A1b lanes E2a)
AT SM's GATE / NEXT: CENSUS v7 56762faa2d RETURNED (RC-i grid tips without node.md, RC-j index refresh row + notes) -> v8 ORDERED (DG3 code, DG2 rows pending)
  E2b0 v8 898a0ecdcb (judged by me 162/162, AST = v7, forwarded 15:5xZ) · WRITER LIST bb7a6adf06 (nodes only, branch dg1-e2-sweep2, replaces e5a67228e2; forwarded) -> SM gates census v8 + E2b0 v8 + list TOGETHER
AA1.V: c0e11faa0a DEMOTED by SM (V1-V4) -> v4 BUILT by DG3 (WIP b619583cf8), DG2 rows in progress; my rulings below
```
- **Census v8 (ordered 15:49Z)**: grid tip shape (a live node's newest tip not a commit / no node.md = exit 2), shallow / info/grafts = exit 2, HEAD resolved ONCE, read errors = exit 2, RC-j row (touch a tracked file's mtime, GIT_OPTIONAL_LOCKS=0 pinned), packed vs loose refs row, docstring 8-line class list. Belam 14:4xZ ruled: NO cut on a partial list; I told him the extended matrix (mail sent TWICE, harmless).
- **E2b0 v8 design (belam option b)**: grid_retired lazily imports crons.load_crons_node(shared root)['jobs']['grid_sync']['enabled'] is False, ANY exception = NOT retired; retired push/sync/cron_lines only republish pre-existing tips (E2d = belam's). The FLIP brief (not cut yet; after E2b0 + census LAND): the commit is the plain literal `enabled: false` on the direct child; the sequence (a)-(e) is in goal:g7.16.1.11.13; check `grid_retired(MAIN)` True on the host python (/usr/bin/python3 3.12.3 + yaml 6.0.1, belam measured).
- **AA1.V v4 rulings (ordered 15:3xZ)**: V1 unit gains `AGI_POST=%i` (engine-root.md:28, keep AGI_SEAT) + pieces STRICT AGI_POST + a lane row running the pieces under the unit's own extracted Environment=; belam installs the unit BEFORE any restart onto the new pieces (AA1.Vc host act, banked: recommend dogfood on my row). V2 new piece `agi-at PATH...` (CAS advance of posts/<P>) for agi-out's ring commit, tick's drift commit, and the agi-meter text names agi-flush. V3 flush retries the final turn 3x, exits 4 if still raced. V4 node records the r2 ruling (heal SWEEP_ARCHIVE_NS stays) + an f2 row. Rail: engine.md fenced 8,122/8,192 (70 B slack): a new map row must fit, tighten a row's wording (facts kept), never raise the rail.
- **Lessons this gen**: a landing's judge runs the SHELL lanes that name the changed output (D1 left graph-metrics.t.sh c2/c2b red: reported [red], fixed c0a529db3f); SM now runs ALL .t.sh lanes gate vs trunk. Reproduce every residue on the bytes before ordering; a lane gap (surviving mutant) goes back to DG2 BEFORE the forward.

## 🔴 Where it stops + the exact next command
DG1 gen 17 -> 18: E2b0 v8 + writer list bb7a6adf06 forwarded; census v8 and AA1.V v4 not yet returned
FIRST ACT: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` and grep /data/work/agi/.agi/sessions/inbox/director-general-1.md after ts 2026-10-08T15:51:33Z. THEN: (1) DG2's census v8 rows -> DG3's census v8 [return] -> RUN at the sha (census tests, mistyped roots rc 2, live MAIN = 1 GRID-ONLY g7.16.1.5.2, fz.py, mutants), a lane gap -> DG2 BEFORE forwarding, then ONE [merge-up] to SM; (2) DG2's AA1.V rows -> DG3's AA1.V v4 [return] -> RUN: race3.sh on the NEW pieces (drop rc 4, tree kept), the lane sweep, ALL .t.sh vs trunk, agi-at reachability probe (a commit via agi-at is reachable from posts/P after the next agi-turn), the unit-env row; (3) SM verdicts on E2b0 v8 + list + census: reproduce any residue first; (4) after E2b0 + census LAND: mint the census build node (level3.py --mint-missing-only writes 360 files: keep ONLY grid_census/test_grid_census nodes), cut the FLIP brief (nodes-only, sequence (a)-(e), plain literal), ask belam for the E2a-installed proof (`crontab -l`). Never run a host act; never invent goals.

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
| a sent sha is never amended (new commit, say 'supersedes'); an UNSENT one may be amended | |

## §5 Verification: every return RUN at the sender's sha (lanes bare + pytest naming the pieces + my reference/fuzz + >= 3 mutants of the REAL piece + a real-failure probe); anonymize scan 0 hits (only the Co-Authored-By trailer hits); links.py links 0 broken (5,801 resolved)

## §6 BANKED (belam; none blocks a build)
- A done (boot leaf landed). B: agi-gate env -i + safe.directory scoped + a lane row, WITH agi-land; belam's host check at install `runuser -u nobody -- git -C <MAIN> rev-parse HEAD` (chmod/ACL only if it fails, with rollback). C: the spawn sets AGI_POST to the kid's own name (E3 / AA1.Vc). AA1.Vc cutover (flag day vs per-post gate): recommend dogfood on DG1's row (`engine: turn: tree`), then the others. E2d: does root push refs/grid at all (recommend ONCE then drop).
- A post literally named 'worktrees' would write into heal.py's SWEEP_ARCHIVE_NS namespace (trivia). live() pairs paths not nodes (a mint check closes it). COPY lines are not followed by nest.py log (stated limit). SM mur notes older: empty AGI_TRUNK makes the EC grep $O's worktree · poll_s/space_s accept 0 · StartLimitBurst=30 · box-carry W partial on a corrupt posts.md row · heal N7/N9.
- Branches I created that cannot be deleted from this uid (leave): dg1-d1-goal, dg1-e2-aa1v, dg1-e2-aa1v2 (c793e79820, AA1.V brief on the live tip), dg1-nest-build, dg1-nest-fix, dg1-b-wording, dg1-e2-sweep, dg1-e2-sweep2 (bb7a6adf06 = the list to land), plus the older dg1-g141-i/-i2, dg1-a1b-*, dg1-e2-aa310*.
