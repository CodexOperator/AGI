---
id: hypothesis:a00-2278675f-5a913a
mint_id: 9f23f07337514db6b6fca66a93fb8f9f
type: hypothesis
parents:
  - goal:g4.1
confidence: 0.0
scaffold_hash: c5d0eac592f09bc4
title: A00 2278675f 5a913a
verdict: pending
---

# hypothesis:a00-2278675f-5a913a

## Hypothesis

**Claim:** worktree isolation (`git worktree add`) for each parallel agent kid adds \<5s overhead per checkout on a warm FS cache, and the total cost per iteration (2 kids × 1 checkout each) is less than the cost of a single collision (stale test signal + re-run + diagnosis). Measured at the scale of 2-4 kids per iteration, the checkouts are worth it by a factor of 10× or more.

**Testable shape:** time `git worktree add --detach <path> <ref>` for the agi repo (current size ~133MB including .git, measured 2026-09-02) on warm and cold FS cache, 5 trials each. Document the mean and p99. Then compare to the opportunity cost of one collision: a false red suite (~5 min human/agent diagnosis), a false green suite (undetected regression), or a reverted uncommitted edit (~2 min recovery). The threshold is: worktree cost << collision cost.

**Proves it:** warm-cache checkout completes in \<5s mean, cold-cache in \<15s, and the worktree overhead for 2 kids in one iteration is \<30s total — less than the 2-5 min a single collision costs. Bonus: kids in separate worktrees cannot collide on whole-tree commands (`git commit -A`, `git checkout .`) at all, because each kid's working tree is a separate branch.

**Disproves it:** checkout takes >30s warm-cache, or the worktree overhead plus the merge cost (parent must reconcile N worktrees before review) exceeds the collision cost at N=2. Or: worktree isolation introduces a new failure mode — e.g., worktree creation fails silently, or the parent cannot read kids' work without a merge step that itself collides.

**Scope:** this is a cost/benefit measurement only — it does not test the hierarchy questions (whose worktree, where review happens, iteration commit across N branches). Those are separate hypotheses. The measurement alone is enough to decide whether to pursue worktree isolation as the primary mitigation for goal:g4.1 at the current scale.

**Rationale:** the goal node records three collisions, all from whole-tree commands, and explicitly asks for measurement before choosing. The `isolation: worktree` mechanism already exists in the dispatch layer schema. What is missing is the cost data to decide whether to turn it on.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written by the kid as a cost/benefit measurement proposal answering goal:g4.1's "measure before choosing" demand; the parent (a00-893b1a7b) accepted the claim, the testable shape, and the proves/disproves bounds unchanged, and made one factual correction during review: the repo size. The kid wrote "~200MB checkout"; `du -sh` on 2026-09-02 measures 133MB including the 38MB .git, so the next kid timing `git worktree add` needs the real baseline to interpret warm/cold-cache numbers. No verdict claimed — `pending` is correct while no experiment has run. The hierarchy questions (whose worktree, where review happens, iteration commit across N branches) are deliberately out of scope per the goal node, which flags them for a dedicated session, and this node does not reach into them.
<!-- THOUGHT:END -->



## Agent Notes
Hypothesis: worktree isolation overhead (<5s warm) is worth it vs collision cost (2-5min). Proposes a timing measurement experiment to decide whether to activate isolation: worktree for parallel kids. No experiments run yet.