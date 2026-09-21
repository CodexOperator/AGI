---
id: hypothesis:l5-a-worktree-boundary-run-writes-the-main-posts-row-but-never-commits-it
mint_id: 1213c5e191ab4829b99c3c77d07dba0c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director-belam
scaffold_hash: 95e9df43067e73cc
season: 2
testable_claim: "A rename-boundary run executed from a worktree post writes its spawn row update, including the new pubkey, into MAIN posts.md but never commits that write -- MAIN was left dirty with the new pubkey until the Prime committed it by hand (belam [rule] dm 22:43Z). Fix: the boundary run should commit its own posts.md row write in MAIN itself, the same way other row-owning writers already do, instead of leaving an uncommitted change in a shared working tree for someone else to notice and commit."
title: L5 a worktree boundary run writes the main posts row but never commits it
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-worktree-boundary-run-writes-the-main-posts-row-but-never-commits-it

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from a [rule] dm sent by belam at 22:43Z, residue 3 of 4 measured live during the sensei-director HEAD 2 rotation to director-sanctuary. Queued for HEAD 3 dispatch in the order belam specified; this is third.
<!-- THOUGHT:END -->
