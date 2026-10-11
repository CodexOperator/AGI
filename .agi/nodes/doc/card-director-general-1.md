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

## §0 State (10-11 ~10:5xZ, gen 24, encryption-town)
| | |
|---|---|
| post | director-general-1: a director, claude-code, engine v5 · parent SM (sanctuary-master) · trunk local-maxxing/season2/main (tip 6f15c681f4 at 10:3xZ) · ~/t is DETACHED at posts/director-general-1 · card edits go through `agi-wt pull doc:card-director-general-1` + agi-turn + agi-flush · a clone pushes a sha to MAIN with `git push /data/work/agi SHA:refs/heads/NAME` (a name that does not exist yet) |
| mail | `AGI_POST=director-general-1 /opt/agi/bin/box read` (send: `box send POST < FILE`, run from ~/t, FILE = plain text WITHOUT backslashes). To belam only via SM. A "mail: box read" line typed into my pane is the post's own wake unit: read the mail |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it · DG2 falsifier lanes · DG3 builder · DG4 builder (.37) · SM gates + lands (council 3/3 first) · belam = host acts, one GO each |
| RAM | /dev/shm is RAM and the box swapped: NO clone or tree there. Work trees on disk under ~/wip (t32 = .32, t401 = .40.1), removed at the END of the run |

## §1 Plan
```
LANDED by SM: close43 (.32 condition) as ee5b59605a (council 3/3 11:46Z, [merge-up] sent to belam) · close39 (.32) b3316f1aa0 · close40 c04b4988f3 · close41 ec97da5a3e + close42 d242c167cb as cf8219a95e (restage refuses while stopped pids are held).
AT SM (all signed, pushed to MAIN, mailed 11:2xZ-11:4xZ), in SM's order:
  1. dg1-close43 f913fb05b5 (on b3316f1aa0) = the .32 COUNCIL CONDITION (PRIORITY: the wake gap is live until belam's host GO): ExecCondition 3 states (unset/empty H = 255 '[boxwake] H unset'), 'timeout 20 box n', env words equal to agi-post@'s (row), DIV 10 why, leaf amended. 8 mutants RED, box-wake 40 ok.
  2. dg1-close44 3d883e3bd4 (on cf8219a95e) = restage RACE: second held check right after the stop + CONT each + lines to journal and recipients; every refusal/failure goes to the recipients. 328 passed, 7 mutants RED.
  3. dg1-close45 29f4e920bf (ON 3d883e3bd4, gate together) = SM's residue option 2: the guard writes SUSPENDED BEFORE the SIGSTOP at both sites; a raising SIGSTOP = line + no stopped pid + a second alert (no crash). 330 passed, 6 mutants RED.
THEN belam: host GO for .32 (replace transient agi-boxwake@ units with the template; a running post gets Wants= after restart or daemon-reload + start) and re-stage with SHA=<landed> sh memguard-restage.sh.
NOTHING else queued for me. Do not invent goals.
```

## 🔴 Where it stops + the exact next command
close44 (3d883e3bd4) + close45 (29f4e920bf) are with SM, gated next behind DG4 .37 + DG5 .41.1; no build in hand. NEXT: `AGI_POST=director-general-1 /opt/agi/bin/box read`. A residue = re-cut in ~/wip/t32 (.32: base b3316f1aa0 + branch dg1-close43) or ~/wip/t401 (.40.1), ONE signed commit, push under a NEW name dg1-close45... Never a host act; never `grid.py checkout`; the g7.16.1.11.11 HOLD is belam's.

## §2 Landed this generation (mine, via SM)
close32..close42 on the trunk (memguard 'stopped' by kernel state, inherited protect reset, proof2, exact exit tokens, pi nice + health + SHA + STAGE guard) · close38 9a90d159e7 landed as 1ef306f39b; close40 720b65fff8 landed as c04b4988f3 (one systemd fetch per tick, young-unit skip, noh/unread episodes). In flight: close43 (.32 condition), close44 (restage race).

## §4 Traps (this generation only; durable ones go to the skills at the next rotation)
| trap | rule |
|---|---|
| box text with backslashes, or `box send` from a non-repo cwd | no backslash escapes in box text; send from ~/t |
| a mutant that goes RED only on an UNINTENDED row proves nothing | read WHICH row went red; assert each OLD text count == 1 (Restart=on-failure appears in TWO units: anchor it) |
| a time-scaled lane (box-wake DIV) | a burst of signed sends takes real time: under load a scaled poll splits it. Rerun solo at a lower DIV before calling a defect |
| the TRUNK-arg lanes (agi-out-states, agi-out-stale, grow-gate-*, aa3) REFUSE a bare run (.37) | commit first, pass the SHA: `sh lane.t.sh <sha>` |
| `python -c`/exec of a slice of the template (memguard-proof2 execs post_rows..guarded with no os) | put a new helper OUTSIDE that slice and add no second `time.sleep(` |
| a recursive shell function assigns globals; `date -d ""` is midnight; `pkill -x sleep` only with `-g <group>` in a test | restore/convert/group |
| `box` needs AGI_POST | baseline a test on the unmodified trunk before trusting its green history |

## §5 Verification: every return RUN at the sender's sha (bare `env -i`, private HOME, a tree on DISK). boxkit: `env -i PATH=$PATH HOME=<dir> python3 -m pytest extensions/agi/tests/test_boxkit_templates.py extensions/agi/tests/test_boxkit_probe.py -q -p no:cacheprovider` = 330 at 29f4e920bf. Engine shell lanes: `ROOT=$PWD sh extensions/agi/tests/<name>.t.sh` (engine-sizes, post-env, restart-bounds, agi-fresh, kid-post-env, boxwake-unit, box-wake, trunk-arg-lanes); with a SHA arg: agi-out-states, agi-out-stale. Read-only measurement of a live tree is fine; a signal, a write under /etc or /usr/local, or a root act is not mine.

## §6 BANKED (to belam via SM; none blocks a build)
- Root host identity for the memguard alerts (c): belam's HOLD lane; the guard writes the red lines to SM's and belam's ~/.notice.
- .32 council REMARK for my NEXT .32 touch (not blocking, 3/3): a timed-out `box n` gives n=0 and sets s=0, so the next good tick re-types 'mail: box read' for mail already announced (one spurious wake per hang, never a lost one). Fix: keep s on a failed count: take the status of `timeout 20 box n` itself (e.g. `n=$(timeout 20 box n 2>/dev/null) || continue`, then count) + row + mutant. Fold it into the next .32 touch; do not cut it alone.
- Pruning noh/unread/nobase for a unit that left the box (a unit gone and back with a miss and no good reading in between stays silent): not cut, council's rule was "clears on the good reading".
- Pruning noh/unread/nobase for a unit that left the box: not cut (the council's rule was clears-on-the-good-reading).
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones (close32..close45).
