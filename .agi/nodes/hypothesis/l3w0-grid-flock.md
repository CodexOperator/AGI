---
id: hypothesis:l3w0-grid-flock
mint_id: e19553798097485b9a831c4f8c39e1a5
type: hypothesis
parents:
  - goal:g7
next_edges: []
edited_by: ubuntu
scaffold_hash: 147f92f29d865e6a
season: 1
testable_claim: grid.py commit --all takes an exclusive flock for the duration of the commit so a manual director commit and the 5-minute grid_sync cron on the same box serialize instead of racing on the same node refs
title: L3w0 grid flock
---
# hypothesis:l3w0-grid-flock

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: extensions/agi/bin/grid.py, tests/test_grid.py. CHANGE: commit --all opens .agi/sessions/.grid.lock (create if missing; sessions/ is scratch) with fcntl.flock LOCK_EX, waits up to --lock-wait seconds (default 120) then exits non-zero with a clear message naming the holder pid if known; single-file commit and the read verbs take no lock. VERIFY: red-first test launching two commit --all processes against a temp graph with a slow fake writer showing the second waits and both refs end consistent; suite green. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md
