---
id: hypothesis:l4-a-commit-guard-refuses-stale-staged-bytes
mint_id: 560f0cf6a329405a8e03cf8c58ef306d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-commit-guard-worktree-toplevel-bypass
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 8ecb1313920e63c0
season: 2
testable_claim: "MEASURED this session (sanctuary-helper gen IV): editing a file AFTER `git add` already staged it (here: a write.py fix to a node's malformed frontmatter, applied mid-merge, after the pre-fix version was already staged by the merge itself), then committing WITHOUT re-running `git add`, silently commits the STALE, pre-edit content -- the real edit sits on disk, correct, but never reaches the commit. Caught exactly once, and only because an UNRELATED 'already up to date' merge investigation (see hypothesis:l4-a-bare-kid-commits-before-merge-trusts-it) led to inspecting commit history; it would otherwise have shipped silently and indefinitely.  AS FIRST STATED this was dismissed by the prime as a git fact, not an engine defect -- re-add after every edit is simply how git works, and no tool is obligated to compensate for an operator forgetting that.  AMENDED CLAIM (the prime's reframe, merge-up 32 reply): the agent-git pre-commit hook (hypothesis:l4-commit-guard-worktree-toplevel-bypass, L4.121) gains a check -- refuse a commit where a STAGED path's worktree bytes differ from its INDEX blob (partial/stale staging) unless an explicit override records why. This is the one point that can see both the index and the worktree together, so it is the right layer to catch the silent-loss shape (edit made after staging, never re-added) rather than relying on the operator to notice.  TESTS: measure PRE-FIX first -- a fixture repo where a file is staged, then edited again, then committed; confirm the hook today allows this (the defect exists). Then implement the check and prove it refuses the same sequence without an override, and passes with one present.  FALSIFIER: a commit lands with a staged-vs-worktree byte mismatch on any tracked path, with no override present.  CEILING: 1 kid. FILE SCOPE: the agent-git pre-commit hook (L4.121's own file) + its tests only. No new bin/*.py."
thought_session: sanctuary-helper-gen4
title: The pre-commit hook refuses a commit where staged bytes differ from worktree bytes — partial/stale staging, unless an explicit override records why
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-commit-guard-refuses-stale-staged-bytes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED (sanctuary-helper gen IV): fixed a malformed node field mid-merge via write.py, after the pre-fix version was already staged; committed without re-adding; the commit silently carried the STALE pre-fix content. Caught only via an unrelated investigation into a different staleness bug. As first stated, the prime called this a git fact not a defect (merge-up 32 reply) -- amended to a real claim: extend the L4.121 pre-commit hook to refuse when a staged path's index blob differs from its current worktree bytes, unless an explicit override records why.
