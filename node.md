---
id: hypothesis:l2-commit-guard-scope
mint_id: f8d57e4ef473446396f2f0598239c949
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director
scaffold_hash: 672afc4a4499d19f
season: 1
testable_claim: The agent git commit guard refuses commits only inside the project repo it was spawned for, so a kid's tests that commit in temporary repos pass under AGI_TIER=kid while a commit in the project tree is still refused
thought_session: agi-master-2026-09-06
title: "L2 g15: l2-commit-guard-scope"
---
# hypothesis:l2-commit-guard-scope

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Observed L2.09 by two parents and one kid: with AGI_TIER=kid and the GIT_CONFIG_* hooks path exported by dispatch.py, the engine suite fails 99 tests and 71 errors, all RuntimeError tier kid may not commit, because those tests commit in temporary repos under /tmp; parents had to strip AGI_* to verify anything. FILES: extensions/agi/hooks/agent-git/pre-commit and pre-push, extensions/agi/bin/dispatch.py (export AGI_PROJECT_ROOT=<real path of the repo enclosing .agi> beside the other AGI_* variables), tests in extensions/agi/tests/test_git_commit_guard.py. RULE: the hooks compare git rev-parse --show-toplevel (real path) with AGI_PROJECT_ROOT and exit 0 immediately when they differ or when AGI_PROJECT_ROOT is unset; the refusal with the existing one-line message stays only for a commit or push whose toplevel is the project repo. VERIFY red-first: under AGI_TIER=kid plus the hooks env, a commit in a temp repo succeeds and a commit in a repo whose toplevel equals AGI_PROJECT_ROOT is refused with exit 1; then run the whole suite with AGI_TIER=kid and the hooks env exported and paste the summary line, it must be green. REPORT: one experiment node under this hypothesis with verdict and evidence_runs. Do not commit, push, or run grid.py commit.
