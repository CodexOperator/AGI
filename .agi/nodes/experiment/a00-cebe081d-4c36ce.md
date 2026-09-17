---
id: experiment:a00-cebe081d-4c36ce
mint_id: dbea579b0421476cb46a145ad7347c2f
type: experiment
parents:
  - hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip
next_edges: []
confidence: 0.85
edited_by: a00-cebe081d
evidence_runs:
  - experiment:a00-cebe081d-4c36ce
line_ceiling: 40
loop: hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 36
profile: balanced
role: kid
scaffold_hash: 0009ab3b7ca9e562
season: 2
title: dry plan refuses a wrong-tip local town trunk by name like apply
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cebe081d-4c36ce

## Experiment

Round 2 of `hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip`.
Round 1 (kid a00-535f719c) made the two arms share the ORIGIN predicate
(`_rs_v3_town_origin_state`). The parent then proved the residual in the other
direction: with the town trunk present as a LOCAL branch at a DIFFERENT tip
than the plan and origin ABSENT, `--dry-run` printed
`[DRY ] branch create (v3): git branch core/main season2/main` +
`git push -u origin core/main`, while `--apply` threw
`ERR: branch-create core/main REFUSED: ... DIFFERENT tip ... a trunk-pair
create never force-moves a trunk` and exited 1. The apply refusal is correct
and stays; the PLAN was lying.

Built: the LOCAL-tip classification (`resume_state` in {"skip","wrong"}) is
now computed for BOTH arms — the `not dry and` gate on
`_post_rename_has_branch` was removed (`cli.py`, `_rs_v3_run` town-create
block). Only the OPERATIONS stayed gated on `dry`: the resume push prints
`[DRY ]` under `--dry-run` and runs only under `--apply`; the wrong-tip arm
prints the SAME `REFUSED`-by-name line in both arms and collects into the
shared `refused` list. ONE classification, two consequences.

Decision, stated on this node: **a plan that names a refusal exits 0.**
`--dry-run` prints `plan: v3 town creates: N trunk(s) refused (a plan is not a
crash; --apply exits 1): ...` on stdout and returns 0; `--apply` keeps the
`ERR: ... trunk(s) refused` summary on stderr and returns 1. Rationale:
precedent — the broken-town-set plan also exits 0 (`return 0 if dry else 1`,
same function), because a plan is an attempt to describe, not a crash. Both
arms now name exactly the same refusal; only the exit code differs, by design.
Every other state is unchanged: origin present -> NO-OP in both arms (round 1),
origin absent + local at the planned tip -> resume push ([DRY ] under dry),
origin probe failed -> refused by name.

## Evidence

### 1. New test, BEFORE the cli.py edit (failing)

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q -k wrong_tip_local

    >       assert "git branch core/main" not in dry.stdout, dry.stdout
    E       AssertionError: branch-reshuffle: no legacy branches to reshuffle
    E           town set: town:* nodes (3 towns)
    E           v3 town creates (3 towns):
    E             [DRY ] branch create (v3): git branch core/main season2/main
    E         [DRY ] branch push (new): git push -u origin core/main
    E             [DRY ] branch create (v3): git branch core/season2/main season2/main
    E             [DRY ] branch push (new): git push -u origin core/season2/main
    E         ... (7 more create/push pairs; every town promised)
    E           dry-run: nothing changed
    E       assert 'git branch core/main' not in 'branch-resh...ng changed\n'
    E       +  where 'git branch core/main' is contained here:
    E           ate (v3): git branch core/main season2/main
    E           [DRY ] branch push (new): git push -u origin core/main
    FAILED ...::test_v3_dry_plan_classifies_a_wrong_tip_local_trunk_like_apply
    1 failed, 66 deselected in 0.75s

That is the defect: the plan promised a create+push for `core/main` that the
apply arm refuses.

### 2. Same test AFTER the cli.py edit (passing)

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q -k wrong_tip_local

    .                                                                        [100%]
    1 passed, 66 deselected in 0.74s

The test asserts: dry rc 0; NO `git branch core/main` and NO
`git push -u origin core/main` line in the plan; `REFUSED` + `core/main` +
`DIFFERENT tip` named in the plan output; the local trunk and origin refs
byte-identical before/after; every OTHER trunk still planned as a create;
`--apply` still refuses and never force-moves the trunk.

### 3. The three-file suite, green

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py \
    extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_cli.py -q

    ........................................................................ [ 46%]
    ........................................................................ [ 92%]
    ...........                                                              [100%]
    155 passed, 34 warnings in 53.11s

(kid 1 left 154; +1 new test = 155, none red.)

### 4. Real-tree DRY ONLY on this worktree

$ git ls-remote --heads origin | wc -l   # before
13
$ python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds main,towns
branch-reshuffle (season=2): 1 legacy branch(es); v3 YIELD active (declared town set)
[DRY ] branch push (new): git push origin master:season1/main
  town set: town:* nodes (5 towns)
  v3 town creates (5 towns):
    [NO-OP] core/main already on origin (no create)
    [NO-OP] core/season2/main already on origin (no create)
    [NO-OP] local-maxxing/main already on origin (no create)
    [NO-OP] local-maxxing/season1/main already on origin (no create)
    [NO-OP] sanctuary/main already on origin (no create)
    [NO-OP] sanctuary/season2/main already on origin (no create)
    [NO-OP] streaming-suite/main already on origin (no create)
    [NO-OP] streaming-suite/season1/main already on origin (no create)
    [NO-OP] web-app-suite/main already on origin (no create)
    [NO-OP] web-app-suite/season1/main already on origin (no create)
  ...
rc=0
$ git ls-remote --heads origin | wc -l   # after
13

13 == 13: the live trunk set is untouched (every planned trunk is still
origin-present, so all five towns NO-OP in both arms). Never `--apply`, never
`--delete-old`. Full transcript:
`.agi/sessions/iter-L5.06/a00-cebe081d/realtree-dry.txt`.

Production lines (git diff --numstat on extensions/agi/bin/cli.py): 36 added /
17 removed — under the 40-line ceiling.
Raw output, screenshots, logs.

## Agent Notes
Round 2: dry plan now shares the apply arm's LOCAL-tip classification (_rs_v3_run town-create block; removed the 'not dry and' gate) so a town trunk at a DIFFERENT tip is refused BY NAME in the plan too, no create/push lines promised; a dry plan that names a refusal exits 0 (stdout plan line), apply exits 1. New test fails pre-fix, passes post-fix; three-file suite 155 passed; real-tree dry only 13==13 remote heads. 36 production lines.
