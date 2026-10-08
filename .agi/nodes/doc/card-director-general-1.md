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

## §0 State (10-08 ~18:55Z, gen 19; meter f ~0.1)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM (sanctuary-master gen 29) · trunk local-maxxing/season2/main (tip 87073089d2 at 18:3xZ) · my t = posts/director-general-1 |
| rotate | the hook prints the line: this card WHOLE, `git commit` it by path, then `touch ~/.fresh;kill $PPID` (skills: agi-rotate, agi-send, agi-dispatch, agi-goal) |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"`; bodies in a FILE (QUOTED heredoc). Read: `... read director-general-1` (ONCE; the inbox file /data/work/agi/.agi/sessions/inbox/director-general-1.md keeps the text). To BELAM only [merge-up] [decision] [rotation] [red] [rule] [complete] [owner] |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha; DG2 = falsifier lanes (test-only); DG3 = the only live builder (line 0.49); DG4 = agi-at row; DG5 = D3 builder; SM gates + lands |
| scratch | `git -C /data/work/agi worktree add --detach $S/x SHA`, remove with `worktree remove --force` from outside; pytest PYTHONPATH=/tmp/claude-978/*/3c9050af*/scratchpad/pt; lanes bare `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null ROOT=<wt> sh X.t.sh`; `links.py schema` takes > 120 s (background it). belam [rule] 18:3xZ: ONE full suite on the box at a time, on tmpfs; I run single files only. NEVER dispatch while /proc/pressure/io avg60 >= 50 (it was 58 at 18:44Z) |

## §1 Plan (all times 10-08)
```
SENT to SM 18:4x-18:5xZ (three [merge-up] mails, queued behind SM's busy pane; if an [undelivered] shows, resend from the inbox file):
  1 goals v3 ebbbc40be8 (branch dg1-e2b1-goal4, on 3246966bf9; GV-1..4 in .13.1/.13.2) + scanner v2 661747ff4a (DG2, RUN: 22 passed, shift GREEN, update-ref RED) + DG4 lane fix 338a855e57 (RUN: 29 ok bare, chmod-deleted/666/message/one-line mutants RED)
  2 nodes round aefd3de83f (branch dg1-nodes-r2, on 87073089d2): FLIP NOTES W8, C4 title, P7 :2375, experiment verdict proved (schema verdict-class 19 -> 18), C5/C7/C8 limit sentence
  3 D3 chain 94a2ccbcda -> ba14f648ae -> a9e30a0339 (DG5, RUN: test_legacy 37 passed, +test_viewport 95 passed, --verify PASS, 2 mutants RED)
NOT YET RUN, mine: DG2's .13.1 rows v2 f49ba79f08 (branch de-base-dg2-117, on 27bebec328; 27+8 rows, to DG3 as build input; run at DG3's build; F2 rule accepted: render-time rewrite of mail_poll's fetch)
IN FLIGHT: DG2: .13.2 rows (seven sites + F3 + write.py row file), then the D3 title-trap row (N4) · DG3: AA1.V v5 build (rows d44c06062c), then .13.1 build · DG4: .13.2 build after DG2's rows · DG5: D3 done, idle
CLOSED: CENSUS dropped · the WRITER LIST frozen · .12 other hypotheses = season 3
```
- **The flip waits ONLY on goal:g7.16.1.11.13.1** (rows + build landed); then cut the FLIP brief (plain literal `enabled: false` on the grid_sync child; grid_retired(MAIN) True on host python); belam applies (`crons.py apply`). E2d = his call.
- **After each return**: RUN it at the sha, a lane gap -> DG2 BEFORE the forward; reproduce every residue on the bytes before ordering; then ONE [merge-up] to SM.

## 🔴 Where it stops + the exact next command
DG1 gen 19: list v4, key chain, goals v3, nodes round (A), scanner v2, DG4 lane fix, D3 chain all RUN and sent to SM; waiting on SM's verdicts and DG2/DG3/DG4 returns
NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then `head -1 /proc/pressure/io`. For each return: RUN at its sha and forward; for each SM return: fix on the live trunk (scratch worktree from origin/local-maxxing/season2/main, nodes only, links.py links 0 broken, merge-tree rc 0). Never run a host act; never invent goals.

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
