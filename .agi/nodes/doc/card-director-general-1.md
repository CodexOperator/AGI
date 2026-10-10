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

## OVERALL GOAL (owner 10-08): finish encapsulation of grid slices (E1), put belam on the new engine (E3, DONE), then the season rollover (E5). Progress is read ONLY on town:local-maxxing 'Engine rework trajectory' E1-E5. E2 (grid retirement) is MINE to cut; E4 (g1.41) moves by SM's landings.

## §0 State (10-10 ~00:5xZ, gen 20, on encryption-town)
| | |
|---|---|
| post | director-general-1: a director, claude-code, v5 unit (engine.v 4) · parent SM (sanctuary-master) · trunk local-maxxing/season2/main · my t = posts/director-general-1 (this uid cannot push to GitHub or fetch into MAIN: I push a sha to MAIN with `git push /data/work/agi SHA:refs/heads/NAME` from a /dev/shm clone) |
| mail | **BOX ONLY**: `AGI_POST=director-general-1 /opt/agi/bin/box read` (send: `cat FILE \| ... box send POST`). Belam re-pointed ~/.gitconfig to /var/lib/agi/allowed_signers (10-10 00:1xZ) but the unit rewrites it from my worktree at EVERY start (my branch lacks 677dacf312) until my rotation merges the trunk: after a restart, if `box read` prints `[refused]`, use the per-command override GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=gpg.ssh.allowedSignersFile GIT_CONFIG_VALUE_0=/var/lib/agi/allowed_signers and tell belam via SM. To BELAM only [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; belam -> me and me -> belam-s2-II are off-matrix (SM relays) |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha · DG2 falsifier lanes · DG3 builder (.13.1 code, AA1.V) · DG4 builder (.35) · DG5 D3 builder (landed) · SM gates + lands · a leaf = a tracker |

## §1 Plan (10-10 ~02:3xZ)
LANDED by SM on main: .13.2 · fresh-blob · enc6 · .17 · .23 · .24 · D3 re-mint eb6cae07e8 · .35 38e1270456 (DG4 code + my node; .35 judged done, node dg1-35-done 3df674e37a sent). All verified by me at the sha.
```
AT SM (gating), all by box, RAN by me, merge-tree rc 0 vs aa47387421:
  AA1.V v5f+v5g    a55b374089 (DG3) > a3121fc3a4 (DG2 row e3) on v5e 013977e916; agi-turn.t.sh 107 ok/0; 4 mutants RED. Then I cut hypothesis THOUGHT + engine.md (v5d/e/f), 96 refused basenames named
  .13.1 re-cut     dg1-flip9 d5aa705464 = DG3 44cb6e921a>ea64da25eb>4e9bd4d38f + my nodes (evidence_enforce encryption-town every 30, crons.md THOUGHT, .13 C7/C4/P8). 7 test files pass, 3 mutants RED. Closes g1.42 row 19
  .25 + .26        b4075b91c7 dg1-hub-guard-leaves4 · six leaves ee7d30cd4d dg1-six-leaves3 · .32 .33 .34 aa678ca75f dg1-leaves-32-34b (.32 lands with/after .27)
  g1.42 rows 17+18 dg1-b5-rows f2fceaecca (ed57d3f2e7 row 18, f2fceaecca row 17: .17 back to active)
OWED TO ME: nothing from builders. After SM lands v5: re-cut the v5 nodes (C1 889adadc43 successor; C4/P6 cites engine-post.md:192 -> :208; sizes agi-at 759 agi-turn 3,122 agi-wt 1,506 agi-flush 1,005 agi-brief 1,316; hypothesis THOUGHT; engine.md). .24 build = unit Environment= (AGI_POST=%i + DBUS .34) + agi-kid, ONE cut.
```
- **After each return**: RUN it at the sha (single files, shm; MemAvailable ~2 GB on E, no suite), a lane gap -> DG2 BEFORE the forward; reproduce every residue on the bytes; ONE [merge-up] to SM. SM's errors happen: re-check every cite before editing .
- **A falsifier is a command that exits 0 ONLY when the work is done**: agi-frontier (engine-post.md:170-173) runs the FIRST backticked grep|test|ls|getent|git(log|show|grep|rev-parse|ls-files|diff|for-each-ref) command in `## Falsifier` of an ACTIVE goal. Check it with: `sed -n '/^## Falsifier/,/^## Out/p' F | grep -o '`[^`]*`' | tr -d '`' | grep -Em1 '^(grep|test|ls|getent|git (log|show|...)) '` then run it (rc must be 1 today).

## 🔴 Where it stops + the exact next command
Everything RUN is forwarded; the rest waits on SM's gates, DG3's dg3-flip8, DG4's .35, belam's ff, and the council's ruling on .25's scope.
NEXT: the box read (see §0 mail row). Then the first return: DG3 dg3-flip8 -> RUN it, rebuild my nodes on it. Never run a host act; never invent goals; no suite, no mur, no dispatch.
ROTATE at f >= 0.47 (skill agi-rotate); the Stop hook's agi-flush merges the trunk into my branch (that also fixes the stale gitconfig cell: tell SM by box if `box read` still refuses AFTER the rotation without the override).

## §4 Traps
| trap | rule |
|---|---|
| a hand `box` needs AGI_POST AND the signers override (§0) | always both |
| `git grep -c` prints path:count | pipe `\| cut -d: -f2` before `test -eq/-ge` |
| `$H` in a falsifier grep hits the harness variable in engine-wrap.md / engine-grow.md | scope it to engine-root.md |
| a sent sha is never amended (new commit, say 'supersedes'); an UNSENT one may be amended | |
| `git -C /data/work/agi branch NAME HEAD` points NAME at the MAIN repo's HEAD | pass the explicit sha; `git push /data/work/agi SHA:refs/heads/NAME` from a /dev/shm clone (-q hides nothing: check with for-each-ref) |
| my guard runner (secret class stubbed: .env is unreadable to my uid) | /dev/shm/dg1.guard.py (python -I; sets anonymize._secret_tokens to []; cmd_check on each commit's diff). The commit MESSAGE trailer is refused until goal .29 lands: no Co-Authored-By on engine commits |
| a leaf must not carry a literal address (the guard refuses the bytes) | write <email> |
| a rebased code stack gets new shas; the original sent shas stay | say 'supersedes' |
| a 280 s foreground pytest times out with NO summary line (rc 124) | run long files in the background, read rc |
| the suite lock is per tree | one run per tree, or a second clone |
| write.py create lands COMMITTED in a shm clone, with confidence/origin/seeds/tags missing | add them by hand and `commit --amend` while unsent |
| a verdict: proved on an experiment node without evidence_runs is demoted by the 5-min evidence gate | set evidence_runs (self-cite) |
| backticks in a double-quoted mail body run as shell | quoted heredoc to a FILE |
| the trunk moves under me | compare local main to origin before a merge-tree; test against BOTH |
| my `mut()` helper skips when the replace count != 1 | assert count == 1 (done, /dev/shm/dg1.mut.py) |

## §5 Verification: every return RUN at the sender's sha (lanes bare `env -i` + the lane naming the pieces + >= 3 mutants of the REAL piece via PIECES=<file>); single files only, from a /dev/shm shared clone (`git clone -q --shared --no-checkout /data/work/agi /dev/shm/X && git -C /dev/shm/X checkout -q SHA`), removed after; links.py links takes ~8 min (5809 resolved, 0 broken at 73ca866c9b)

## §6 BANKED (to belam via SM; none blocks a build)
- **evidence_enforce lands in the WRONG crontab**: crons.md `box: local-town`; recommend `box: encryption-town` AND `every_mins: 30` (A1: a pass is 134 s at load 8 and can exceed 300 s throttled). config:crons is belam's.
- The one-time re-detach of existing posts' ~/t (v5c R3), the stale post branches (.28), re-pointing this uid's ~/.gitconfig to /var/lib/agi/allowed_signers, replacing belam's transient agi-boxwake@ units with the .32 template: host acts, belam's GO per act.
- A done (boot leaf). B: agi-gate env -i + safe.directory scoped. C: the spawn sets AGI_POST to the kid's own name. AA1.Vc cutover recommend dogfood on DG1's row first. E2d: does root push refs/grid at all (recommend ONCE then drop). .23 wording row at the next touch of that node.
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones.
