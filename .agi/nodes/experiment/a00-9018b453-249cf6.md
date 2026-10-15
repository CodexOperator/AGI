---
id: experiment:a00-9018b453-249cf6
mint_id: ff7a149ee3c84c6cb1970cbb75ca7364
type: experiment
parents:
  - hypothesis:harvest-table-subcommand
next_edges: []
confidence: 0.8
edited_by: a00-2dae5724
evidence_runs:
  - experiment:a00-9018b453-249cf6
loop: hypothesis:harvest-table-subcommand@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4186a97a4050dd1a
season: 2
title: A00 9018b453 249cf6
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-9018b453-249cf6

## Experiment

Implemented `rotate.py harvest-table` (hypothesis:harvest-table-subcommand, FILE
SCOPE line: added to rotate.py rather than a new harvest.py — the claim's scope
names that as the allowed first choice; rotate.py already owns the round-/
seat-lifecycle reporting (`complete`, `status`) and carries `_git_lines`.)

`harvest-table [--seat S] [--round N|--all-live] [--root R]` prints one row,
per (round, kid agent), the five facts F5 lists by hand today:
  1. branch — `loop/<slug>-<agent>@s<N>` DISCOVERED from `git for-each-ref`
     refs/heads/loop (regex `-(a00-[0-9a-f]{8})@s(\d+)$`), so a finished round
     whose worktree was removed still maps, and the slug never drifts.
  2. worktree path — `.agi/worktrees/<agent>/` from the main checkout
     (`locations.git_common_root`), or `-` once removed.
  3. diffstat — `git diff --stat merge-base(parent, branch)..branch`, so a
     moved seat/parent tip never shifts the base; shows exactly what the round
     added.
  4. kid experiment node ids — `git diff --name-only mb..branch` filtered to
     `.agi/nodes/experiment/*.md`.
  5. each kid's verdict — read from each node's frontmatter (on-disk worktree
     first, else `git show branch:path`), so it survives worktree removal.
Rounds are discovered from every `iter-*` session dir with a manifest: completed
ones harvested into main (`.agi/sessions/iter-*`), live ones inside each
worktree (`.agi/worktrees/<agent>/.agi/sessions/iter-*`); main's copy wins on a
duplicate. `--seat` filters on any agent's `dispatched_by`; `--round` accepts a
bare or `iter-`-prefixed id; `--all-live` keeps only rounds with a `running`
agent.

## Evidence

`extensions/agi/tests/test_harvest_table.py` — a red-first, real-git fixture
(the same shape dispatch.py/loop_branch_name produce) that drives
`rotate.main(['harvest-table', '--root', <fixture>, ...])` and checks:
  * test_completed_round_reports_all_five_facts — manifest harvested into
    main; asserts branch, worktree path, merge-base diffstat
    (`.agi/nodes/experiment/a00-kid.md`), kid id `experiment:a00-kid`, and its
    verdict `inconclusive_lean_proved:50` all appear when checked by hand.
  * test_worktree_removed_still_reports_branch_and_kids — `git worktree
    remove --force`; asserts the worktree column is `-` while the branch,
    diffstat and kids come from git alone.
  * test_live_worktree_round_all_live_filter — a live manifest living only in
    the WORKTREE's sessions dir is found; `--all-live` returns it and excludes
    a done round.
  * test_seat_filter — `--seat` keeps its round, drops another seat's, and
green: `4 passed`.

Regression (existing suite): `test_bin_help_smoke.py test_rotate.py
 test_rotate_complete.py test_harvest_table.py` → `181 passed, 1 skipped`.
`rotate.py harvest-table --help` exits 0 with non-empty stdout (already
enrolled in help-smoke as part of rotate.py).

Followed the no-git rule: `harvest-table`'s own git calls run against the
`--root` FIXTURE in tests only; I never invoked git against the shared tree.
Confidence limited (80, not 100) because the mechanism is proven on the fixture
but not yet exercised against a live, human-checked multi-kid round.

## Agent Notes
Built rotate.py harvest-table (round branch/worktree/diffstat-vs-merge-base/kid-ids/verdicts from for-each-ref + manifests; worktree-removal-surviving via git show). Proven by 4 red-first real-git fixture tests + 181-pass regression. Not yet exercised vs a live human-checked round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2dae5724, L4.236): accepted at inconclusive_lean_proved:80, not demoted. WHAT THE INSTRUCTION SAID: the hypothesis declares "CEILING: 1 kid" and "FILE SCOPE: extensions/agi/bin/rotate.py or a new extensions/agi/bin/harvest.py (additive subcommand only) + tests". WHAT THE MACHINE ACTUALLY DOES: I read the artifact, not the report — rotate.py:5802-6022 carries _git_out/_harvest_round_dirs/_harvest_loop_branches/_harvest_read_node_fields/_harvest_diffstat/cmd_harvest_table, subparser at rotate.py:6175, and help exits 0 (measured). I ran `pytest extensions/agi/tests/test_harvest_table.py -q` → 4 passed, and `pytest test_bin_help_smoke.py test_rotate.py -q` → 171 passed, 1 skipped. I ran the tool against THIS live round: `rotate.py harvest-table --round iter-L4.236 --root <worktree>` printed one row with branch/worktree/diffstat/kids/verdicts all `-`. THE NEAR MISS: a fix that only passes the fixture would satisfy the words and lose the mechanism; here the live row is dashes because this parent dispatched WITHOUT --branch (loop_branch_name, dispatch.py:364-374, was never cut), so no refs/heads/loop exists for a00-9018b453 — the code path is right but the live falsifier the claim names ("a live round whose branch/worktree/kid-node-ids/verdict the table gets wrong") is UNEXERCISED. The kid already said so (80, not 100) and I did not raise it: a claim whose own testable_claim sets CEILING: 1 kid is not entitled to a second kid to cover its own gap. IF I DEVIATED: I did not fork a live --branch round to close the falsifier, because the node itself bounds the round at one kid.
<!-- THOUGHT:END -->

PARENT ACCEPT: rotate.py harvest-table implemented in-scope, 4 new fixture tests pass, 171-test regression green, help exits 0. Lean 80 kept because the live --branch falsifier was not exercised (dispatch ran without --branch, so the live row is all dashes). Potential next: one --branch round to close it.
