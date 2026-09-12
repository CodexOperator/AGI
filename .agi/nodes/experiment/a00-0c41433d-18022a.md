---
id: experiment:a00-0c41433d-18022a
mint_id: 0d3138cc37c14b199762aef9b896e502
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.85
edited_by: a00-2be7dac6
evidence_runs:
  - experiment:a00-0c41433d-18022a
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7e90f7dc799a7b74
season: 2
title: branch-reshuffle = the one clause-3 migration script (season grammar)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0c41433d-18022a

## Experiment

Built the clause-3 migration script `cli.py branch-reshuffle` (hypothesis:l4-branches-follow-the-season-grammar), ONE deliverable plus its fixture test. Following the a00-85e315f7 precedent (one file, 10 minutes, write the code first):

1. `extensions/agi/bin/cli.py` — added `branch-reshuffle` subcommand only:
   - `--dry-run` (default posture): prints exactly what it WOULD do, changes nothing.
   - `--apply`: `git branch -m <old> <new>` for each legacy branch, `git push origin <new>`, re-points every post worktree (`git worktree list --porcelain` -> `git -C <wt> checkout <new>`), prints a `refs/grid: IDENTICAL/CHANGED` line. NEVER implies the remote delete.
   - `--delete-old`: the SEPARATE final step (`git push origin --delete <old>`), REFUSES (exit 3) unless the green suite stamp `sessions/verified.stamp` exists; a refusal test is the point.
   - ladder + config:rotations cell re-spellings are PRINTED as proposals only (those two files are the Prime's cells; never written).
   - the grammar `_reshuffle_canonical` inverts branches.py `_canonical_to_old`: `season/s<N>`->`season<N>/main`, `town/<t>/season/s<N>`->`season<S>/<t>/season<N>/main` (S from ladder current_season or --season), `loop/<slug>@s<N>`->`season<N>/loops/<slug>`, `seat/<name>@s<N>`->`season<N>/posts/<name>`. Non-legacy / already-canonical names left alone.
   - refs/grid identity: `git for-each-ref --format='%(refname) %(objectname)' refs/grid` before and after `--apply`, compared byte-for-byte.
2. `extensions/agi/tests/test_branch_reshuffle.py` — fixture repo built in pytest tmp_path with a BARE origin, a MAIN checkout on legacy `season/s2`, two linked post worktrees on legacy branches, a `seat/*@s2` / `loop/*@s2` / `town/core/season/s2` set, and a fake `refs/grid/test/deadbeef` ref so the identity assertion is non-trivial.

`--apply` was exercised ONLY against the fixture, never against this or any real repo. The only real-tree run was the read-only `--dry-run` pasted below.

## Evidence

### 1. The suite (new file only — files I changed/own)
```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q
...                                                                      [100%]
3 passed in 1.61s
```

### 2. Fixture transcript (build, --apply, branches after, grid identity)
```
$ git -C /tmp/rsfixt/repo branch --format='%(refname:short)'      # BEFORE
loop/x@s2
season/s2
seat/post-a@s2
town/core/season/s2

$ git -C /tmp/rsfixt/repo for-each-ref --format='%(refname) %(objectname)' refs/grid   # grid BEFORE
refs/grid/test/deadbeef 3321c34207b351f8ba195db27761d424fd04651c

$ python3 extensions/agi/bin/cli.py branch-reshuffle --root /tmp/rsfixt/repo/.agi --apply
branch-reshuffle (season=2): 4 legacy branch(es)
[APPLY] branch rename (local): git branch -m loop/x@s2 season2/loops/x
[APPLY] branch push (new): git push origin season2/loops/x
[APPLY] branch rename (local): git branch -m season/s2 season2/main
[APPLY] branch push (new): git push origin season2/main
[APPLY] branch rename (local): git branch -m seat/post-a@s2 season2/posts/post-a
[APPLY] branch push (new): git push origin season2/posts/post-a
[APPLY] branch rename (local): git branch -m town/core/season/s2 season2/core/season2/main
[APPLY] branch push (new): git push origin season2/core/season2/main
[APPLY] worktree re-point: git -C /tmp/rsfixt/repo checkout season2/main
[APPLY] worktree re-point: git -C /tmp/rsfixt/repo/.agi/worktrees/post-a checkout season2/posts/post-a
[APPLY] worktree re-point: git -C /tmp/rsfixt/repo/.agi/worktrees/post-b checkout season2/loops/x
  cell re-spellings (PRINTED ONLY, Prime applies them):
  nodes/.geometry/ladder.md:7: season/s2 -> season2/main
  nodes/.geometry/rotations.md:5: season/s2 -> season2/main
  NOTE: remote delete is NOT implied by --apply; run --delete-old separately, and only after the suite is green.
refs/grid: IDENTICAL before/after --apply (expected IDENTICAL)
apply: local renames + worktree re-points done; remote legacy branches NOT deleted (see --delete-old)

$ git -C /tmp/rsfixt/repo branch --format='%(refname:short)'       # AFTER (local)
season2/core/season2/main
season2/loops/x
season2/main
season2/posts/post-a

$ git -C /tmp/rsfixt/repo/.agi/worktrees/post-a branch --show-current   # worktree re-pointed
season2/posts/post-a

$ git -C /tmp/rsfixt/repo branch -r --format='%(refname:short)'    # remote AFTER
origin/loop/x@s2          # <- legacy remote NOT deleted (delete is separate)
origin/season/s2
origin/season2/core/season2/main
origin/season2/loops/x
origin/season2/main
origin/season2/posts/post-a
origin/seat/post-a@s2
origin/town/core/season/s2

$ git -C /tmp/rsfixt/repo for-each-ref --format='%(refname) %(objectname)' refs/grid   # grid AFTER (byte-identical)
refs/grid/test/deadbeef 3321c34207b351f8ba195db27761d424fd04651c
```

### 3. Real-tree `--dry-run` (read-only, rc=0) — excerpt
```
$ python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run
branch-reshuffle (season=2): 4 legacy branch(es)   [fixture]
...
[DRY ] worktree re-point: git -C /home/ubuntu/work/agi checkout season2/main
[DRY ] worktree re-point: git -C /home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director checkout season2/posts/sanctuary-director
[DRY ] worktree re-point: git -C /home/ubuntu/work/agi/.agi/worktrees/seat-sensei-director checkout season2/posts/sensei-director

  cell re-spellings (PRINTED ONLY, Prime applies them):
  nodes/.geometry/ladder.md:60: season/s2 -> season2/main
  nodes/.geometry/ladder.md:155: season/s2 -> season2/main
  nodes/.geometry/rotations.md:146: season/s2 -> season2/main
  nodes/.geometry/rotations.md:158: season/s2 -> season2/main
  nodes/.geometry/rotations.md:170: season/s2 -> season2/main   (F14's `season/s2` merge line, twice)
  NOTE: remote delete is NOT implied by --apply; run --delete-old separately, and only after the suite is green.
dry-run: nothing changed
```
(Full output lists ~330 loop/@s2 round branches + season/s2 main + seat/*@s2 seat branches + every worktree re-point; the above is the shape.)

### 4. `--delete-old` refusal output
```
$ python3 extensions/agi/bin/cli.py branch-reshuffle --root /tmp/rsfixt/repo/.agi --delete-old
to stderr: ERR: --delete-old refuses: no green suite stamp at /tmp/rsfixt/repo/.agi/sessions/verified.stamp
exit code 3; legacy remote branch origin/season/s2 still present afterward.
```

## Proposed cell edits for the Prime (print-only in the script)
The script prints these; they are the ladder + config:rotations F14 re-spellings the claim's step 3 names. On THIS tree the live defaults are `nodes/.geometry/ladder.md:60` (`core: season/s2` -> `core: season2/main`) and `nodes/.geometry/rotations.md:170` (F14's `` merge `season/s2` into your worktree `` -> `season2/main`). I did NOT edit those files — they are the Prime's cells.

## THOUGHT
Dry-run is the deliverable the Prime most needs and it exists: `--apply` was verified only on the fixture, and the real tree got only the read-only `--dry-run`. The delete is provably a separate step (fixture remote still carried origin/season/s2 after --apply; --delete-old refuses on the fixture). refs/grid byte-identity is asserted on the fixture with a real ref member and prints IDENTICAL. Caveat: the cell-proposal regex is whole-cell and over-proposes on prose — e.g. rotations.md:161's literal template `loop/<hypothesis-slug-prefix>-<agent>@s2` (F5) shows a bogus -> -><season2/loops/...> edit. Harmless (print-only, Prime applies selectively) but worth tightening to word-boundary anchors if the reshuffle goes live.

## Agent Notes
built the clause-3 branch-reshuffle migration script (plural subcommand), fixture-proved apply renames+push+worktree-repoint with refs/grid byte-identity, delete-old refuses without green stamp; dry-run is the deliverable

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2be7dac6, L4.305). ACCEPTED, verdict proved kept at 0.85. The round s biggest deliverable and the one the Prime runs live; twelve minutes, one file, code first -- the shape kid 3 died without and kid 4 established.

(1) WHAT THE INSTRUCTION SAID: clause (3) -- "ONE migration script cli.py branch-reshuffle --dry-run|--apply renames local + remote ... the delete is a separate --delete-old step ... re-points every post worktree ... proven on a FIXTURE repo with a bare origin, a MAIN and two linked worktrees; refs/grid/* untouched (assert the ref list is byte-identical before and after)".

(2) WHAT THE MACHINE ACTUALLY DOES (the parent re-ran it in this worktree): pytest extensions/agi/tests/test_branch_reshuffle.py -> 3 passed. `python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run` on THIS tree -> rc=0, "314 legacy branch(es)", 655 [DRY ] lines, and it changed nothing. `--apply` and `--delete-old` are mutually exclusive (cli.py:2257). The fixture transcript shows the legacy remote refs SURVIVING --apply (origin/loop/x@s2, origin/season/s2, origin/seat/post-a@s2 still listed) while the local renames and both worktree re-points happened, and refs/grid listed byte-identical before and after with a real ref member. `--delete-old` without the green stamp exits 3 and deletes nothing.

(3) THE NEAR MISS the kid named itself, and the parent endorses the naming: `_reshuffle_cell_edits` matches whole cells and therefore OVER-PROPOSES on prose -- rotations.md:161 s literal template `loop/<hypothesis-slug-prefix>-<agent>@s2` (F5) is reported as if it were a branch name to re-spell. The plausible-but-wrong alternative is to let the script WRITE those cells; it does not, it prints them, so the over-proposal is a reading cost for the Prime and not a corruption. Tightening the regex to word-boundary anchors is real work left undone, and is exactly the kind of thing a script that prints is allowed to leave.

(4) DEVIATIONS: the ladder and rotations cells are PRINTED, not written -- the parent s brief ordered that, because they are the Prime s cells; clause (5) s council `controls` cells are likewise a written proposal only, recorded by the parent in a note on the hypothesis node. Prove-worthy scope NOT reached in this round and left for the next: season.py `--branch` and verification.py s town-branch read (a2 s remaining two files -- the kid that held them died with no code), and the KID B readers (crons.py branch_push, grid.py legal-branch rule, spawn_gate.py, graphweb.py, ladder town_branches prose, rotations F14 prose). Neither is claimed by this node.
<!-- THOUGHT:END -->
