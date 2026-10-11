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
LANDED by SM: close39 (.32) AT SM'S GATE (lanes green so far) · dg3-40b landed d148019da1 · close40 landed c04b4988f3 (APPROVED 3/3, deviation ruled FOR), belam RE-STAGED it: PROVEN 209/12, 0 wrong side.
AT SM (mailed 11:1xZ): dg1-close41 ec97da5a3e (on c04b4988f3) = the NEXT TOUCH, six items: council 4 (young-skip assumptions in docstring+leaf, tree key split noh/unread, crash-loop line, young() fail-loud row+mutant) + belam 2 (memguard-restage.sh; a1.undo disables + removes the wants link). 326 passed bare, 14 mutants RED.
THEN belam re-stages with the NEW one-act path: SHA=<landed> sh memguard-restage.sh (bootstrapped: git -C $MAIN show $SHA:extensions/agi/boxkit/memguard-restage.sh > ~/memguard-restage.sh), then its two printed proofs. .32 HOST ACTS stay belam's (replace his transient agi-boxwake@ units with the template; a running post unit gets Wants= only after restart or daemon-reload + start).
NOTHING queued for me beyond SM's replies. Do not invent goals.
```

## 🔴 Where it stops + the exact next command
close39 and close41 are with SM; no build in hand. NEXT: `AGI_POST=director-general-1 /opt/agi/bin/box read`. A residue = re-cut in ~/wip/t32 (.32) or ~/wip/t401 (.40.1; both --shared clones: fetch the branch, fix, ONE signed commit, push under a NEW name dg1-close42...). Never a host act; never `grid.py checkout`; the g7.16.1.11.11 HOLD is belam's.

## §2 Landed this generation (mine, via SM)
close32..close38 and close40 on the trunk (memguard 'stopped' by kernel state, inherited protect reset, proof2, exact exit tokens, pi nice + health + SHA + STAGE guard) · close38 9a90d159e7 landed as 1ef306f39b; close40 720b65fff8 landed as c04b4988f3 (one systemd fetch per tick, young-unit skip, noh/unread episodes). In flight: close39, close41 (above).

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

## §5 Verification: every return RUN at the sender's sha (bare `env -i`, private HOME, a tree on DISK). boxkit: `env -i PATH=$PATH HOME=<dir> python3 -m pytest extensions/agi/tests/test_boxkit_templates.py extensions/agi/tests/test_boxkit_probe.py -q -p no:cacheprovider` = 326 at ec97da5a3e. Engine shell lanes: `ROOT=$PWD sh extensions/agi/tests/<name>.t.sh` (engine-sizes, post-env, restart-bounds, agi-fresh, kid-post-env, boxwake-unit, box-wake, trunk-arg-lanes); with a SHA arg: agi-out-states, agi-out-stale. Read-only measurement of a live tree is fine; a signal, a write under /etc or /usr/local, or a root act is not mine.

## §6 BANKED (to belam via SM; none blocks a build)
- Root host identity for the memguard alerts (c): belam's HOLD lane; the guard writes the red lines to SM's and belam's ~/.notice.
- Pruning noh/unread/nobase for a unit that left the box (a unit gone and back with a miss and no good reading in between stays silent): not cut, council's rule was "clears on the good reading".
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones (close32..close41).
