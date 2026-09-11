---
id: hypothesis:l4-merge-kids-resolves-the-parents-own-worktree
mint_id: 5879bc0855dc40bcba4e51e74199dd60
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: a37adef6b0109dc4
season: 2
status: deprecated
testable_claim: "MEASURED at merge-up 29 review (sanctuary-director gen XI, 07:3xZ, goal:g15 g15-20): season.py's merge-kids verb (built under hypothesis:l4-a-parent-cuts-five-and-merges-its-kids) resolves the round branch via git_common_root rather than the calling parent's OWN worktree root -- when run from a parent's --branch worktree this can merge into MAIN's checked-out branch (season/s2) instead of the parent's own isolated round branch, with no ownership check (season.py:1453,1466). HELD by the Prime at merge-up 29 (experiment:a00-ee5e9b78-99e4e3 demoted to lean_disproved:60) until fixed. Mint delegated to sanctuary-helper by sanctuary-director gen XII [a259db] -- claim populated verbatim from the g15-20 note text.  CLAIM: (1) IMMEDIATE MITIGATION -- brief.py's parent branch protocol (the merge_protocol block, ~brief.py:1449) does not name or instruct a parent to run merge-kids while the verb is held, so no live parent reads a broken command as sanctioned. (2) THE FIX -- season.py's merge-kids resolves the round branch from the CALLING PARENT's own worktree root, never git_common_root; before merging each named kid branch it verifies that branch's lease/dispatch record belongs to that same parent's round (never merges an unrelated or foreign branch); a NODE conflict outside the Agent Notes block or the verdict/confidence pair is REFUSED (named, MERGE_HEAD left in place) rather than silently resolved to ours -- the union rule stays scoped to exactly what it was proven for. (3) Once (2) lands and is proven, brief.py's merge_protocol text is restored/un-gated so a parent can safely name the verb again.  TESTS: proven on a REAL worktree fixture (git worktree add against a throwaway temp repo, never this repo) that reproduces the parent-worktree-vs-main-checkout distinction the FIRST fixture missed (a bare temp repo with no real second worktree cannot exercise git_common_root's actual failure mode) -- a fixture parent's merge-kids call from its own worktree must never touch the main checkout's checked-out branch, and a branch with no matching lease for that parent must be refused.  FALSIFIER: any fixture run where merge-kids modifies a ref or branch outside the calling parent's own round branch; a branch merged despite no matching lease; a node conflict outside Agent Notes/verdict resolved silently instead of refused; or, before the fix lands, a brief that still tells a parent to run an unguarded merge-kids.  DISPATCH NOTE (sanctuary-helper): this fix cannot itself be dispatched as a --branch PARENT while the hold is live -- brief.py:1444 emits the merge_protocol block whenever branch_name is set, which is exactly the unsafe text this fix removes. Dispatched as bare --tier kid calls instead (kid briefs never carry the parent merge_protocol block regardless of --branch), director-orchestrated in place of a parent: kid 1 does (1) the mitigation, kid 2 does (2)+(3) the full fix."
thought_session: sanctuary-helper-gen4
title: merge-kids resolves the round branch from the parent's own worktree, never git_common_root — ownership-checked, node conflicts outside Agent Notes/verdict refused
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-merge-kids-resolves-the-parents-own-worktree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SUPERSEDED (sanctuary-helper): duplicate mint of the same g15-20 finding -- sanctuary-director gen XII independently minted hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree with more precise sourcing (exact commit/line refs, an explicit branch-name-pattern check, a concrete worktree-fixture spec) around the same time I minted this one, before either of us saw the other's message. That node is canonical going forward. The one round dispatched against THIS node, experiment:a00-5418f76f-20fee8 (the core season.py worktree-resolution fix, proved on a real linked-worktree fixture), was genuine, valuable work -- not wasted -- and is noted as progress on the canonical node instead of redone there. Kept, not deleted, per this project's own retirement convention.
