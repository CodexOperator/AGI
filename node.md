---
id: hypothesis:l4-a-post-branch-is-created-with-its-origin-upstream-set-after-the-first-push
mint_id: a24182f6c8994236a308cbdd3a086174
type: hypothesis
parents:
  - goal:g25.legacy-direct
next_edges: []
edited_by: belam
scaffold_hash: d9baf0c8521feec8
season: 2
status: deprecated
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (SM lane, 11:51Z) and verified on MAIN 28acb3459: all three live post worktree branches (core/season2/posts/<post>/main) had NO upstream -- sanctuary-director paid 5 calls hunting its own branch name; master-sensei set `git branch -u origin/<b>` on the three by hand today (shared .git/config). branches.py:266-309 cuts the NAME only; no creation or first-push path in branches.py/rotate.py sets an upstream (grep: zero `-u`/`--set-upstream` sites). CLAIM: the path that creates a post (or loop) branch and pushes it the first time sets the branch's upstream to origin/<b> in the same step (git push -u, or branch -u after a proved push), idempotently, so `git status -sb` / `rev-parse --abbrev-ref @{u}` resolve on a fresh post worktree with no hand step; an existing upstream is left as is. FALSIFIERS: a freshly created post branch whose @{u} does not resolve after its first push; a creation path that overwrites an upstream already set; a `-u` set before the push is proved (an upstream to a ref that does not exist on origin). TESTS (<=4, fixture bare origin + worktree, no live push): fresh post branch -> @{u} == origin/<b> after the first push; existing upstream untouched; push failure -> no upstream set, refusal by name; the SM.25b local-only post contract (mirror ref, no origin head) stays green -- if the post head is local-only by contract, the upstream is set on the MIRROR push path only when a head exists, else the claim narrows to loop/town branches and says so in the node. FILE SCOPE: branches.py (creation helper), rotate.py (the first-push call site), their tests. CEILING: <=25 production lines, 1 kid -- re-brief SM past 2x."
thought_session: goal-glom-2026-09-19
title: L4 a post branch is created with its origin upstream set after the first push
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-post-branch-is-created-with-its-origin-upstream-set-after-the-first-push

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): RETIRE decided -- The named mechanism (a first head push of a post/loop branch) does not exist in the bytes: `_stops_push` resolves `mirror_ref_for_branch` for post AND loop kinds (branches.py:395-398) and returns after `mirror_and_prove` without ever pushing a head (rotate.py:16669-16682, MEASURED sed); pre-existing origin post heads are slated for deletion (`_drop_origin_post_head` rotate.py:3913-3928); owner ruling 2026-09-13 18:3xZ 'never pushed as heads' (doc/l4-owner-decisions.md:757); the node's own fallback narrowing to loop/town is empty -- loops are mirrored by the same helper and the only town-trunk creation path already pushes `-u` (cli.py:4402,:4434, MEASURED grep; no `checkout -b`/`worktree add` EVIDENCE: rotate.py:16669-16682,:3913-3928; branches.py:378-399; cli.py:4402,:4434; doc/l4-owner-decisions.md:757; experiment a00-6ded7d52-9ebf6c:15 The status flip + move to deprecated/ is HELD by name: verification.py's never-lower node-count gate keys on ACTIVE and has no path for a deliberate retirement (a hand-lowered baseline would be a disarmed guard); it moves when hypothesis:l4-the-never-lower-gate-names-a-deliberate-retirement lands.

Retired at the L4 closeout (Prime retire list 2026-09-17 12:0xZ from survey hypothesis:a00-e1933e6a-176c0e, executed by sanctuary-master gen 7, status deprecated + moved under deprecated/hypothesis, mint id unchanged): mechanism absent; post branches are never pushed as heads (owner).
