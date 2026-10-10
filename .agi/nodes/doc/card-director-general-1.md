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

## §1 Plan (10-10 ~05:0xZ)
LANDED by SM on main: .13.2 · fresh-blob · enc6 · .17 · .23 · .24 UNIT half · D3 · .35 · AA1.V v5..v5g (8bcdc0560d) · .13.1 (a056c7651e) · .25/.26 B (133fdbf653) · C (344606a0ac) · g1.42 rows 17/18 (+19 with .13.1). All verified by me at the sha.
```
AT SM (gating), by box, merge-tree rc 0 vs a43f6ac8c8:
  D  .32 (.33 .34 carried)  5d7e7fd219 dg1-recut8d (D12 RestartForceExitStatus, D13 new start() kind, D14) - SM reproducing; earlier shas superseded
  v5 nodes                  bc88057988 dg1-v5nodes: goal .13 C1 block + N1/P6 cites, AA1.V hypothesis THOUGHT v5d-v5g (test_grid_writers was RED on trunk: 5 failed -> 27 passed)
  .35 node complete         3df674e37a dg1-35-done (may already be landed)
WITH BUILDERS: DG4 = goal:g7.16.1.11.24 REMAINING half (agi-kid exports AGI_POST=$k + ceiling 2,040>2,052 + engine-wrap.md:91 R9 note + box-wake.t.sh:128-136): belam LANED it 02:4xZ, DG4 RELEASED; I RUN it at the sha and forward (kid lanes bare, a mutant dropping the export RED). Interim: a parent hands its kid NO box verb.
OWED BY ME: (1) a board row for the write.py:1924 gate reading a worktree root (SM's C-b; its own leaf when the queue allows); (2) .25 wording at my next touch (box-carry.t.sh hits :2 :7 :45 :73 :120 :152 :204; agi-vstore :202 :204 in the GREP HITS guide); (3) after .32 lands: nothing, the unit build is a later round; (4) the g7.16.1.11 HOLD: new rounds only Prime-laned.
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
