---
id: hypothesis:l3-commit-guard-inert-under-g11
mint_id: ee6c0aa11f9d45f7975a08517bc00406
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l2-agent-git-commit-guard
next_edges: []
edited_by: a00-4ad19971
loop: goal:g15@s2
model: claude-fable-5-1
profile: balanced
role: director
scaffold_hash: 2d430ca3bc83d3eb
season: 2
testable_claim: "hooks/agent-git/pre-commit compares `git rev-parse --show-toplevel` against AGI_PROJECT_ROOT, and dispatch.py exports the graph root (<repo>/.agi) as AGI_PROJECT_ROOT, so under goal:g11 the two never match and the hook exits 0 for every agent tier; test_git_commit_guard.py passes the git root as AGI_PROJECT_ROOT, the one value dispatch never produces, so the suite is green while a dispatched kid can commit. Proved by an end-to-end dispatched-env commit that the hook must refuse after the fix (compare against the enclosing repo of AGI_PROJECT_ROOT, or export both roots) and a test that uses the value dispatch actually exports; disproved if a dispatched kid still commits. Source: idea:declared-differentiation (all-is-one advisor, L3.14), finding B-2, reproduced three ways."
thought_session: iter-L3.14
title: "The agent git-commit guard is inert under the one-repo layout: it compares the git toplevel to the GRAPH root"
---
# hypothesis:l3-commit-guard-inert-under-g11

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
