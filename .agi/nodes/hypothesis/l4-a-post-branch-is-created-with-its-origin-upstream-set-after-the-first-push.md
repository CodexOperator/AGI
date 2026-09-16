---
id: hypothesis:l4-a-post-branch-is-created-with-its-origin-upstream-set-after-the-first-push
mint_id: a24182f6c8994236a308cbdd3a086174
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: d9baf0c8521feec8
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (SM lane, 11:51Z) and verified on MAIN 28acb3459: all three live post worktree branches (core/season2/posts/<post>/main) had NO upstream -- sanctuary-director paid 5 calls hunting its own branch name; master-sensei set `git branch -u origin/<b>` on the three by hand today (shared .git/config). branches.py:266-309 cuts the NAME only; no creation or first-push path in branches.py/rotate.py sets an upstream (grep: zero `-u`/`--set-upstream` sites). CLAIM: the path that creates a post (or loop) branch and pushes it the first time sets the branch's upstream to origin/<b> in the same step (git push -u, or branch -u after a proved push), idempotently, so `git status -sb` / `rev-parse --abbrev-ref @{u}` resolve on a fresh post worktree with no hand step; an existing upstream is left as is. FALSIFIERS: a freshly created post branch whose @{u} does not resolve after its first push; a creation path that overwrites an upstream already set; a `-u` set before the push is proved (an upstream to a ref that does not exist on origin). TESTS (<=4, fixture bare origin + worktree, no live push): fresh post branch -> @{u} == origin/<b> after the first push; existing upstream untouched; push failure -> no upstream set, refusal by name; the SM.25b local-only post contract (mirror ref, no origin head) stays green -- if the post head is local-only by contract, the upstream is set on the MIRROR push path only when a head exists, else the claim narrows to loop/town branches and says so in the node. FILE SCOPE: branches.py (creation helper), rotate.py (the first-push call site), their tests. CEILING: <=25 production lines, 1 kid -- re-brief SM past 2x."
title: L4 a post branch is created with its origin upstream set after the first push
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-post-branch-is-created-with-its-origin-upstream-set-after-the-first-push

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
