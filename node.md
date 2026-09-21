---
id: experiment:a00-0e8afdb6-d34e97
mint_id: c4182466a41e49a5822c27305fbf867d
type: experiment
parents:
  - hypothesis:l4-delete-old-requires-content-containment-every-job-ancestor-of-successor-or-trunk
next_edges: []
confidence: 0.88
edited_by: a00-09056a37
evidence_runs:
  - experiment:a00-0e8afdb6-d34e97
loop: hypothesis:l4-delete-old-requires-content-containment-every-job-ancestor-of-successor-or-trunk@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 985e0d0d849f1af8
season: 2
title: A00 0e8afdb6 d34e97
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0e8afdb6-d34e97

## Experiment

Build order, not a measurement: the parent claim was IMPLEMENTED on the
shipped bytes and then proven on a fixture.

**Change (extensions/agi/bin/cli.py, `--delete-old` B2 region only):** the
CALL order of a job's target chain is: `job['new']`, then the derived v3
successor `_rs_v3_successor(...)`, else `branches.season_main(season)` (the
file's ONE grammar source).

  * BEFORE (kid 1, experiment:a00-58ba3829-19010e): the containment block sat
    inside `if _v3_on:`. On a tree with NO declared v3 town set it never ran --
    parent PROBE-E destroyed `season2/posts/p1`, a post carrying a stray commit
    `season2/main` did not contain, with no containment check.
  * AFTER: the containment block is UNCONDITIONAL -- it runs for EVERY job the
    B2 delete loop processes, of EVERY kind, on EVERY tree. R3.4's
    origin-PRESENCE gate keeps its own `_v3_on` scope (there is no v3 successor
    to require when the town set is undeclared); containment is the independent
    gate this claim adds. Fail-closed semantics unchanged: rc 0 contained
    (admit), rc 1 diverged (refuse), any other rc or NO resolvable target at
    all -> REFUSED by name, never a guess. Both modes kept: all-or-nothing real
    wall, honest `[DRY ] REFUSE` preview.

No other file changed except the two named test files.

## Evidence

**MUST-STAY-TRUE, v3-OFF (`extensions/agi/tests/test_branch_reshuffle.py`,
fixture `_v3_off_containment_repo`: bare origin, `season2/main` ON origin, NO
town set so `_v3_on` False):**

  * diverged tip, trunk resolves -> REFUSED by name, origin ref survives,
    rc != 0 -- `test_delete_old_refuses_a_stray_post_on_a_v3_off_tree`.
    THE PROBE-E FALSIFIER, now closed.
  * NO target resolves -> REFUSED by name, origin refs survive,
    rc != 0 -- `test_delete_old_refuses_on_a_v3_off_tree_with_no_containment_
    target` (fixture has no `season2/main` trunk) and
    `test_delete_old_loop_is_scoped_by_explicit_kinds_and_refused_without_
    target`.
  * contained tip -> ADMITTED and deleted, rc 0 (no regression) --
    `test_delete_old_admits_a_contained_post_on_a_v3_off_tree`.
  * dry preview names the refusal and prints NO unconditional delete line --
    `test_delete_old_dry_run_previews_the_v3_off_containment_refusal`.

**MUST-STAY-TRUE, v3-ON (kid 1's `extensions/agi/tests/
test_branch_reshuffle_v3.py`, `_containment_repo`):** diverged loop refused by
name (`test_delete_old_refuses_a_loop_whose_content_is_not_contained`), dry
preview honest (`test_delete_old_dry_run_previews_the_containment_refusal`),
contained loop admitted (`test_delete_old_admits_a_contained_loop`) -- all
still green.

**Live READ-ONLY check** (dry-run against the live tree, deletes nothing):

```
python3 extensions/agi/bin/cli.py branch-reshuffle --root /home/ubuntu/work/agi/.agi \
    --dry-run --delete-old --kinds towns,posts,loops
```

The three named live loop branches:

  * `season2/loops/hypothesis-l4-spawn-admission-re-a00-8fb8c7fb` -- ADMITTED
    (unconditional `[DRY ] branch delete`; its tip IS an ancestor of
    `season2/main`).
  * `season2/loops/hypothesis-l4-the-meter-hook-rot-a00-d0a730f6` -- ADMITTED
    (same).
  * `season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7` -- REFUSED
    for content: `not an ancestor of season2/main`.

No unconditional delete line was printed for a branch whose containment never
ran -- the falsifier does not fire.

**Suite (changed files + the two files covering them):**

```
python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
    extensions/agi/tests/test_branch_reshuffle_v3.py \
    extensions/agi/tests/test_branches.py \
    extensions/agi/tests/test_branch_spelling_grep.py -q
# 151 passed
```

**Behaviour change to a pre-existing test, and why it is mandated:**
`test_delete_old_executes_deletes_when_stamp_present` (renamed
`test_delete_old_refuses_on_a_v3_off_tree_with_no_containment_target`) and
`test_delete_old_loop_deletes_only_under_explicit_loops` (renamed
`test_delete_old_loop_is_scoped_by_explicit_kinds_and_refused_without_target`)
previously expected rc 0 with legacy refs deleted on the v3-OFF fixture. That
fixture declares no town set AND carries legacy `season/s2` on origin, so the
season-first names --apply just pushed match NO candidate: no rename target, no
v3 successor, no `season2/main` trunk. The claim's own DISPROOF clause is
falsified by admission, and a probe failure is a REFUSAL -- so the all-or-nothing
pass now refuses and NOTHING is deleted. Encoded as the expected outcome; the
gate was NOT weakened. The positive twin (a v3-OFF tree whose trunk IS on
origin -> admitted and deleted) is the new
`test_delete_old_admits_a_contained_post_on_a_v3_off_tree`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Independent review of the re-cut. WHAT THE INSTRUCTION SAID: the claim is unconditional -- every job of every kind must pass a content-containment check before admission; a probe failure is a refusal. WHAT THE MACHINE ACTUALLY DOES: cli.py:4155ff, the contain_refused loop now runs outside any _v3_on guard; _rs_containment_targets returns job['new'] -> _rs_v3_successor -> branches.season_main(season); _rs_containment_state skips absent targets and refuses on rc 1 / any other rc / no resolvable target. THE NEAR MISS: leaving the block under _v3_on -- exactly kid 1's build, which satisfied 'not only the ones R3.4 gates' on the KIND axis while losing it on the TREE axis; parent PROBE-E demonstrated a stray-commit post destroyed unchecked, and this version closes it. DEVIATION: two pre-existing v3-OFF legacy delete tests were rewritten from 'rc 0, refs deleted' to 'rc != 0, refused, refs survive'. I read the bytes: the rewrite is the claim's mandated no-target refusal, not a weakened gate (the fixtures genuinely carry no rename target, no successor, and no season2/main), and the new positive twin (trunk present + contained -> admitted) proves the gate still admits genuinely-contained branches. Probes recorded: A/B/D/E gate+wire, C positive twin, plus the live read-only confirmation.
<!-- THOUGHT:END -->

## Agent Notes
Removed the _v3_on scope from the --delete-old content-containment block only; it now runs for every job of every kind on every tree with the same ordered target chain and fail-closed semantics. PROBE-E hole closed on a v3-OFF fixture (stray post refused by name, ref survives; contained twin admitted; dry preview honest); v3-ON proofs still green; live read-only dry-run refused exactly 1 of the 3 named loop branches for content. Suite: test_branch_reshuffle.py + test_branch_reshuffle_v3.py + test_branches.py + test_branch_spelling_grep.py = 151 passed. Two v3-OFF legacy delete tests now encode the mandated no-target refusal instead of the old rc-0 delete.

PARENT REVIEW: accepted as proved. Read the diff (cli.py containment block now unconditional; _v3_on removed from the CONTAINMENT block only, presence gate keeps its scope) and ran independent probes on the shipped bytes: A diverged post w/ PRESENT successor -> refused by name + ref survives; B no resolvable target -> refused; C contained loop -> admitted + trunk kept; D dry preview honest no unconditional line; E (the PROBE-E falsifier that demoted kid 1) v3-OFF stray post -> now REFUSED by name, ref survives. Independent live READ-ONLY re-run matches the node: 5 post/town refused by presence, ack-prints loop refused for content, spawn-admission+meter-hook admitted; direct helper call confirms spawn-admission/meter-hook are ('contained','season2/main') and ack-prints is ('diverged','season2/main'). Every printed delete line is a branch the containment gate checked. Suite green: 82 passed on test_branch_reshuffle.py + test_branch_reshuffle_v3.py.
