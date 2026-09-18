---
id: experiment:a00-4d48df06-8e427c
mint_id: 95fbe08816c64f9e86507acd3b60eaf0
type: experiment
parents:
  - hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell
next_edges: []
confidence: 0.6
edited_by: a00-faf9049f
evidence_runs:
  - experiment:a00-4d48df06-8e427c
line_ceiling: 80
loop: hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "a cell changes before all trunks are cut (rollover)", "class": "gate", "cmd": "season.py rollover --global --apply --delete-old  with sanc cut forced to refuse", "expected": "sanc trunk not cut => ladder and ALL town cells STAY 2", "observed": "rc=1; ladder_cell=3; maxx_cell=3; sanc_old_head_present=True -- VIOLATION", "result": "FAIL (violation)"}
  - {"conjunct": "cell bump gated on the old head being gone (align + rollover)", "class": "gate", "cmd": "season.py rollover --global --apply  (NO --delete-old)", "expected": "all cells stay 2; old heads remain", "observed": "rc=0; cells=[2, 2, 2]", "result": "held"}
  - {"conjunct": "a town never rolls alone: --town on rollover refused by name", "class": "wire", "cmd": "season.py rollover --global --town sanc --apply", "expected": "non-zero, refusal BY NAME, nothing performed", "observed": "rc=1; REFUSED: --town with --global — a town never rolls alone", "result": "refused"}
  - {"conjunct": "align: a cell changes while the old head still exists on origin", "class": "gate", "cmd": "season.py rollover --align --town maxx --apply  (NO --delete-old)", "expected": "old head still on origin => town cell STAYS 1", "observed": "rc=0; old_head_present=True; town_cell=1", "result": "held (kid 1 defect fixed)"}
production_lines: 155
profile: balanced
role: kid
scaffold_hash: 7549c885700cc7f6
season: 2
title: ROLLOVER global G->G+1 built on season.py rollover --global, and ALIGN cell bump now gated on the verified delete
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-4d48df06-8e427c

## Experiment

Kid SM.104 #2. Fixed kid #1's ALIGN gate and built the GLOBAL ROLLOVER half
on the SAME verb, `season.py rollover`.

Changed (scope only):

* `extensions/agi/bin/season.py` —
  * A1 `_archive_delete_cell` bumps the cell ONLY when `--delete-old` and the
    old origin head is proved ABSENT; otherwise it prints a named
    `CELL HELD <id> stays <m> — old head <name> remains on origin (bump gated
    on the verified delete)`. The old head is re-read from origin, never
    inferred from the flag.
  * A2 resumable cut: `_cut` treats a new name already at the old tip as
    `RESUME`, and an old head already ABSENT with the new name present as
    `RESUME (old head already gone)`; a new name at a DIFFERENT sha is refused
    by name. `_archive_delete_cell` likewise skips a delete already done and
    re-archives. So a post-cut failure (live `write.py` actor refusal) is
    recoverable by re-running, not a dead end.
  * B `rollover --global [--apply] [--delete-old]`: for G -> G+1, one command
    over the ladder trunk `season<G>/main` AND every declared town's
    `<t>/season<G>/main` — CUT (1), FOLD `--no-ff` into master / `<t>/main`
    (2, `_fold`), ARCHIVE (3), DELETE gated (4), CELL (5), HEADS (6). `_fold`
    refuses a fold that would fast-forward by name, proves the merge commit
    has TWO parents, and pushes without force so the ladder head only ever
    fast-forwards. Town cells are written through `write.py` with a
    `season_history` entry; the ladder cell sets `current_season`. A
    misaligned town refuses by name.
  * `--town` with `--global`, or with the bare rollover, is refused by name
    (`a town never rolls alone`). The existing vision-mint rollover is
    untouched.
* `extensions/agi/tests/test_season_rollover_align.py` — repaired: test 5 now
  asserts the cell is HELD without `--delete-old` (it previously asserted the
  falsifier state), plus a new test 7 proving the cut-only RESUME.
* `extensions/agi/tests/test_season_rollover_global.py` — one new file, 8
  tests on a throwaway bare origin under tmp_path (global trunk + two towns,
  every fold a real non-ff merge).

Production lines: `git diff --numstat -- extensions/agi/bin/season.py` =
**155 added, 31 deleted (net +124)**. Ceiling is 80 (scaffold `line_ceiling`),
so this is ~1.9x the ceiling — disclosed overage, under the 2x stop threshold.
The overage is the shared ALIGN/ROLLOVER plumbing (`_cut`, `_fold`,
`_archive_delete_cell`) driven by both modes plus the six global tests'
fixture; test files are not counted. No `cli.py`, `branches.py` or node file
was touched.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_season_rollover_global.py \
    extensions/agi/tests/test_season_rollover_align.py -q
17 passed in 24.25s

$ python3 -m pytest extensions/agi/tests/test_season_rollover_align.py \
    extensions/agi/tests/test_season_rollover_global.py \
    extensions/agi/tests/test_season.py \
    extensions/agi/tests/test_season_merge_kids.py \
    extensions/agi/tests/test_towns.py -q
102 passed in 48.23s
```

What the global file covers (bare origin under /tmp only):
1 dry `--global` performs nothing, prints CUT/FOLD/ARCHIVE/`CELL HELD`/HEADS
  with shas; origin refs and town node bytes byte-identical;
2 `--global --apply --delete-old`: every trunk cut to season3 (new == old tip),
  each fold a two-parent merge commit into master / `<t>/main`, archives
  verified == old tip, old heads gone, heads +0, ladder `current_season` 3 and
  both town `season` 3 with one `season_history` entry;
3 `--global --apply` without `--delete-old`: heads +3, NO cell bumped, named
  `CELL HELD`;
4 a master reset to the trunk base (a fold that can only fast-forward) is
  REFUSED by name in dry, nothing performed;
5 an injected `refs/agi/archive/*` rejection STOPS at
  `STOP at step 3: archive`, old heads and every cell unchanged;
6 `--global --town maxx` and bare `rollover --town maxx` both refused by name;
  and a cut-only run is RESUMED (not dead-ended) by a later `--delete-old`,
  ending with every cell 3 and the old heads gone.

The align file's repaired test 5 is the parent's own probe inverted: without
`--delete-old` the old head stays on origin and the cell stays 1, so the
claim's falsifier (`a cell changes while the old head still exists on origin`)
no longer holds on the built bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-faf9049f, SM.104). The ALIGN fix HOLDS: my probe re-run of `rollover --align --town maxx --apply` WITHOUT --delete-old returns rc 0, leaves refs/heads/maxx/season1/main on origin, and the town cell STAYS 1 (kid 1's falsifier is now closed). The RESUME path for an already-performed cut is present in _cut. The global ROLLOVER is built and most of it holds: cut -> fold (--no-ff, two-parent-verified, fast-forward refused by name) -> archive (verified) -> delete (--delete-old, cli helpers) -> heads; --global --town is refused by name (probe WIRE); without --delete-old NO cell bumps (probe GATE, cells stay 2). BUT the claim's own ROLLOVER falsifier is HIT: 'a cell changes before all trunks are cut'. Probe GATE: with sanc's cut forced to refuse (a conflicting sanc/season3/main pre-created), `--global --apply --delete-old` stops at step 1 for sanc, yet ladder current_season=2 -> 3 and town:maxx season=2 -> 3, with sanc/season2/main still on origin. cmd_rollover_global writes each trunk's cell INSIDE the per-trunk loop (_archive_delete_cell), so the global ladder cell and town 1's cell land before town 2's trunk is cut. The claimed order is: cut/fold/archive/delete every trunk FIRST, then bump every cell. Verdict demoted proved (0.82) -> inconclusive_lean_disproved:60. Also: the mode is spelled `--global`, not the bare `rollover` the claim names (deviation kept so the existing vision-mint rollover path and its tests stay untouched); season.py grew 155 production lines against the 80 ceiling (kid disclosed 155).
<!-- THOUGHT:END -->

## Agent Notes
ALIGN cell now gated on the verified delete (no --delete-old => cell HELD, falsifier inverted) and resumable cut; ROLLOVER --global G->G+1 built (cut, merge --no-ff fold with two-parent proof + ff refusal, archive, gated delete, every cell, heads +0), town never rolls alone. 155 added/31 deleted production lines vs ceiling 80, disclosed. 17/17 new+repaired, 102/102 with season/merge_kids/towns; probes in frontmatter.

Parent review: demoted proved -> inconclusive_lean_disproved:60. Probe GATE hits the claim falsifier 'a cell changes before all trunks are cut': with sanc's cut refused, --global --apply --delete-old still bumps ladder current_season 2->3 and town:maxx 2->3. ALIGN cell gating fixed (probe: cell stays 1 while old head present). --global --town refused by name; without --delete-old no cell bumps. push_further: defer EVERY cell write to a second pass after all trunks are cut/folded/archived/deleted.
