---
id: hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block
mint_id: e516e2dec4f4462cbce4de1ec64fd1d6
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 823f685345fea34a
season: 2
testable_claim: "goal:g15.25 SM.09 (intake: master-sensei 01:15Z; measured on its own rotate-out: three MAIN posts — belam, sanctuary-master, master-sensei — share ONE checkout; rotate-self --prepare check 2 refused it twice in 2 min on OTHER posts uncommitted files, each refusal also costing a stop_commit). MEASURED on season2/main @75bf00343: _prepare_checks check 2 (rotate.py:12800-12862) blocks on ANY non-whitespace dirty path from git status (`dirty tree: <5 paths>`), with no notion of who dirtied it; check 3 measures the merge conflict-free with read-only `git merge-tree --write-tree HEAD origin/<sb>` (_merge_applies_clean :12570) — but a merge that is conflict-free in the index can still refuse at checkout when a dirty WORKING file is in its touch-set (git: your local changes would be overwritten) — THAT is the only mechanical reason dirt must block, and it is a per-path test the gate never runs; a worktree post (row worktree non-empty) has no foreign dirt by construction. CLAIM: (1) NEW `_merge_touch_set(root, sb) -> set[str] | None` = `git diff --name-only HEAD...origin/<sb>` (three-dot: what the merge brings in; None on git refusal = unmeasured); (2) check 2 on a MAIN post (row worktree empty) partitions dirty_paths into BLOCKING = dirty ∩ touch-set, and FOREIGN = the rest; the check blocks ONLY on BLOCKING (named with both facts: `<p>: dirty AND touched by origin/<sb>`); FOREIGN is appended as a non-blocking named line `foreign dirt (not in the merge): <paths>` capped at 5 (+N more) — so the Prime GOALS.md draft or the SM live mint no longer refuses a master-sensei rotate-out; when the touch-set is unmeasured (None) the check falls back to today (all dirt blocks) and says `touch-set unmeasured`; (3) the stop_commit written at a refusal is NOT written when the only refusals are foreign (measure where stop_commit is written and name the line; a refusal that is now not a refusal writes nothing); (4) worktree posts unchanged: their dirt is their own — the partition runs only when the row worktree cell is empty (measure via _find_seat); (5) behind == 0 (nothing to merge) -> touch-set empty -> no dirt blocks; the unpushed/behind checks unchanged. FALSIFIERS: a dirty path IN the touch-set that passes; a foreign path that still blocks on a MAIN post; a worktree post whose own dirt stops blocking; a two-dot diff (HEAD..origin = the wrong set); a stop_commit on a foreign-only refusal; any change to the merge perform itself. TESTS (test_rotate_prepare.py <= 5, fixture repo with a fake origin branch): dirty path in touch-set -> block naming both; dirty path outside -> no block, named foreign; touch-set None -> today behaviour; worktree row -> today behaviour; behind 0 + dirt -> no block. FILE SCOPE: rotate.py _prepare_checks check 2 + one helper; test_rotate_prepare.py. CEILING: <= 45 lines net, <= 5 tests. The alternative master-sensei named (worktrees for MAIN posts) stays banked — it multiplies the F14 class this line is retiring."
title: "on a shared MAIN checkout the prepare dirty-tree gate blocks only when a dirty path intersects the merge touch-set (HEAD..origin/<sb> name-only); another post uncommitted work outside it is NAMED, never a block, never a stop_commit (master-sensei rotate-out 01:2xZ: refused twice in 2 min on the Prime g17.1 and the SM live mint)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
