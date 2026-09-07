---
id: hypothesis:l2w15-grid-master-guard
mint_id: a2f251860d6b41aeacef49bf7a0b0a9e
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: season.py
scaffold_hash: afdc7bc1bded6fb0
season: 1
testable_claim: grid.py commit --all refuses to run when the checked-out branch is not master, unless --allow-branch is passed, while session-ref commits keep working from any branch
thought_session: season
title: "L2 wave 1.5: l2w15-grid-master-guard"
---
# hypothesis:l2w15-grid-master-guard

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/grid.py only, plus tests in extensions/agi/tests/test_grid.py. Design: section 2, Branches mirror the ladder, last paragraph: node refs are one linear ref per mint id with no notion of branch, so two worktrees committing the same node interleave versions; rule: commit --all runs only on master after a merge. CHANGE: in the commit --all path, resolve the checked-out branch of the repo that owns the graph (git rev-parse --abbrev-ref HEAD, run in that repo, never cached); if it is not master and --allow-branch is absent, print one line, grid: refusing commit --all on branch NAME, node refs are branch-blind, merge to master first or pass --allow-branch, and exit 2 without writing any ref. Detached HEAD counts as not master. The per-file session commit (grid.py commit FILE --session ITER AGENT) is not gated. Nothing else in grid.py changes. VERIFY: tests, red first: a temp repo on a branch named work refuses with exit 2 and writes no ref; the same with --allow-branch writes; master writes; a session commit on the work branch writes. Run python3 extensions/agi/bin/grid.py status on this repo afterwards to show nothing regressed. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Engine files are edited in place; a new engine file is created directly under extensions/agi/bin/ (level3.py mints its build node later). Run the suite through python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, do not push, do not run grid.py commit. If git status shows files you did not create, report them and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md