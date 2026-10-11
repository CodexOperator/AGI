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
tags: []
title: Card director general 1
town: core
# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## OVERALL GOAL (owner 10-08): finish encapsulation of grid slices (E1), belam on the new engine (E3, DONE), then the season rollover (E5). Progress is read ONLY on town:local-maxxing 'Engine rework trajectory' E1-E5. E2 (grid retirement) is MINE to cut; E4 (g1.41) moves by SM's landings.

## §0 State (10-11 ~10:1xZ, gen 23 rotating out, encryption-town)
| | |
|---|---|
| post | director-general-1: a director, claude-code, engine v5 · parent SM (sanctuary-master) · trunk local-maxxing/season2/main (tip b74649058e at 10:0xZ) · ~/t is DETACHED at posts/director-general-1 (8a63483a8c: all-is-one's lane once moved it and restored it by CAS 10:0xZ, intact) · card edits go through `agi-wt pull doc:card-director-general-1` + agi-turn + agi-flush · a clone pushes a sha to MAIN with `git push /data/work/agi SHA:refs/heads/NAME` (a name that does not exist yet) |
| mail | `AGI_POST=director-general-1 /opt/agi/bin/box read` (send: `box send POST < FILE`, run from ~/t, FILE = plain text WITHOUT backslashes: box read renders them). To belam only via SM |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it · DG2 falsifier lanes · DG3 builder · DG4 builder (.37) · SM gates + lands (council 3/3 first) · belam = host acts, one GO each |
| RAM | /dev/shm is RAM and the box swapped out (belam red 09:5xZ): NO clone or tree there. Work trees live on disk under ~/wip; remove a gate tree at the END of its run |

## §1 Plan
```
AT SM: dg1-close38 9a90d159e7 (ON 959a9cf102): R1 unreadable journal = NOT PROVEN, R2 undo scope = STAGE/a2.since. 315 passed bare, 8 mutants RED. SM gates it.
  Then belam (OWNER GO for A1+A2 given 08:43Z): A0 on the LANDED sha (git show SHA:extensions/agi/boxkit/memguard-a0.sh > ~/memguard-a0.sh; SHA=<sha> sh it), then from B=~/memguard-A0/src/extensions/agi/boxkit:
  sh $B/memguard-a1.undo.sh; sh $B/memguard-a1.sh; sh $B/memguard-a1.proof.sh; sh $B/memguard-a2.sh; SHA=<sha> sh $B/memguard-a2.proof.sh   (exit 0 PROVEN, 1 UNDO via memguard-a2.undo.sh, 3 NOT PROVEN: no undo, send the printed line to the master). A pid older than the window in a WRONG line = a real miss: ask for the lines + PPid.
IN HAND: goal:g7.16.1.11.32 (agi-boxwake@ as an INSTALLED unit; SM queued it, ruled .27 does not block). WORK TREE ~/wip/t32 (a --shared clone checked out at b74649058e, UNCOMMITTED changes; also saved as ~/wip/dg1-32-wip.patch; tools in ~/wip/tools).
  DONE in it: engine-root.md (Wants=agi-boxwake@%i.service in agi-post@.service; new ### agi-boxwake@.service 806 B: PartOf/After the post, User, WorkingDirectory t, EnvironmentFile, AGI_POST (NO AGI_SEAT: post-env u3), ExecCondition gate (brace-free), ExecStart loop `while :;do sleep 5||:`, Restart=on-failure, RestartSec=10s, RestartForceExitStatus), engine-wrap.md (agi-run: both loops `while :;do sleep N||:`, the box-wake line GONE), engine.md (map 47 pieces, agi-project writes the unit and copies each post's h.conf to agi-boxwake@P.service.d/), restart-bounds.t.sh (good shape widened + a row), box-wake.t.sh (kinds unit + both, the production env AGI_POST, w8 gate rows, r6/r7 retargeted, F2 kill-the-sleep rows for unit/inbox/pane-cap, F4b real-box row from agi-project's h.conf, stale r9 p40-p43 retired), NEW boxwake-unit.t.sh (static F1 F3 F4a F5). engine-sizes 0 FAIL, post-env 0 FAIL, restart-bounds 0 FAIL, boxwake-unit 0 FAIL, box-wake run2: 39 ok 1 FAIL = F4b's grep (AGI_BOX is UNQUOTED in h.conf) FIXED since, not rerun.
  TO DO (in order): rerun box-wake; run the other suites on the tree; MUTANTS (each OLD text asserted count == 1, name the row that goes RED): unit without PartOf / Restart / RestartForce / the ${H} brace / AGI_SEAT, agi-run back to `while sleep`, a second `box n` loop in agi-run, the unit loop `while sleep 5`, agi-project not copying h.conf, the Wants= line gone, the gate `claude*` -> `pi*`; then ONE signed commit on the trunk tip (from ~/wip/t32: git -c user.name=director-general-1 -c user.email=director-general-1@agi commit; push as dg1-close39), mail SM. Run `git fetch`-equivalent first: the trunk moves (check the 3 geometry files + the tests still apply).
  TELL SM in that mail (the leaf text is stale in these): AGI_SEAT dropped from the unit; no `AGI_POST=${AGI_POST:-$AGI_SEAT}` fallback (box needs AGI_POST, .37); box-wake.t.sh was ALREADY RED on the trunk (its watcher env had no AGI_POST) and is not in verify; r6's premise (AGI_POST unset) is dead, r9 p40-p43 retired, w8 (the dead pi-x branch) rewritten as the unit's gate; HOST ACTS stay belam's (replace his transient agi-boxwake@ units with the template, start it on running posts).
BANKED / not mine: root host identity (c) = belam's HOLD lane · leaf .40.1 closes after PROOF 2a+2b exit 0 on the live box · SM's close37->close38 history in the mails.
```

## 🔴 Where it stops + the exact next command
gen 23 rotated at the line (502k): close38 is with SM; goal .32 is in ~/wip/t32 with one fixed grep unrun, then suites, mutants, ONE commit.
NEXT: `AGI_POST=director-general-1 /opt/agi/bin/box read` (SM's verdict on close38 / belam's A2 result) THEN `cd ~/wip/t32 && git status --short && (ROOT=$PWD sh extensions/agi/tests/box-wake.t.sh > ~/wip/bw-run3.txt 2>&1; echo rc=$? >> ~/wip/bw-run3.txt)` in the BACKGROUND (~4 min), expect `box-wake: 0 FAIL`. Never run a host act; never invent goals; never `grid.py checkout`; the g7.16.1.11.11 HOLD is belam's.

## §2 Landed this generation (mine, via SM)
close32 b29e5f0740 -> 2fc5c8c91b (memguard 'stopped' by kernel state) · close33 da7a8fc3b9 -> ad90349bec (inherited protect value/nice reset) · close34 10a88a3128 -> f726cb68bc (proof2 on the trunk, reset at tick end, per-unit alerts) · close35/36 c62c8327db + a0ab5fe993 -> 181e2e7063 (the acts + proof on the trunk, exact exit tokens) · close37 959a9cf102 (pi nice, health, SHA, STAGE guard; gated, returned for R1/R2) · close38 9a90d159e7 (sent). Earlier: close23/25/31 on the trunk. A0 done by belam on ad90349bec and A1 installed the OLDER guard (swap with a1.undo + a1).

## §4 Traps (this generation only; the older ones were dropped as stale at this rotation, durable ones proposed to SM for the skills)
| trap | rule |
|---|---|
| box text with backslashes, or `box send` from a non-repo cwd | no backslash escapes in box text; send from ~/t |
| /dev/shm is RAM | trees on disk (~/wip), removed at the end of the run |
| an exit-code `case` with `*1*` | exact tokens `"1 "*\|*" 1"`; test codes that CONTAIN the digit (137 124 127 10) |
| a recursive shell function call assigns globals (start() sets kd, the caller's loop var) | restore after, or pass a different name |
| a mutant that goes RED only on an UNINTENDED row proves nothing | read WHICH row went red (C2a was caught by the low-memory row, not the ordering row: a test-side replace after another replace never matched) |
| `date -d ""` is midnight today | convert only a non-empty value |
| `pkill -x sleep` | only with `-g <setsid group>` in a test, never box-wide |
| `box` needs AGI_POST; box-wake.t.sh had been red on the trunk for ages and is not in verify | run a test BEFORE trusting its green history; baseline it on the unmodified trunk first |

## §5 Verification: every return RUN at the sender's sha (bare `env -i`, private HOME, a tree on DISK; boxkit: `env -i PATH=$PATH HOME=<dir> python3 -m pytest extensions/agi/tests/test_boxkit_templates.py extensions/agi/tests/test_boxkit_probe.py -q -p no:cacheprovider` = 315 at 9a90d159e7). Engine shell lanes: `ROOT=$PWD sh extensions/agi/tests/<name>.t.sh` (engine-sizes, post-env, restart-bounds, agi-fresh, kid-post-env, agi-out-states, agi-out-stale [2 FAIL o7f on the WIP tree: compare with the unmodified trunk before blaming it], boxwake-unit, box-wake). Read-only measurement of a live tree is fine; a signal, a write under /etc or /usr/local, or a root act is not mine.

## §6 BANKED (to belam via SM; none blocks a build)
- Root host identity for the memguard alerts (c): belam's HOLD lane; the guard writes the red lines to SM's and belam's ~/.notice (council).
- Offered, not cut: a one-fetch-per-tick systemctl budget in memguard (residue: a hung systemctl = 10 s per unit after the stops, once per 300 s).
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones (close32..close38 etc).
