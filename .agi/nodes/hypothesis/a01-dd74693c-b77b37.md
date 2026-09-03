---
id: hypothesis:a01-dd74693c-b77b37
mint_id: 217df7c27894448da362bf01921f30c2
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
confidence: 0.0
scaffold_hash: 2311a5fedc2796ef
title: A01 dd74693c b77b37 — whole-tree command restriction vs worktree
verdict: pending
---
# hypothesis:a01-dd74693c-b77b37

## Hypothesis

**Claim:** Restricting whole-tree commands (`git commit -A`, `git checkout .`, `git checkout --all`, `grid.py checkout --all`) to one designated "committer" agent per iteration eliminates the g4.1 whole-tree-command collision class (2 of the 3 recorded incidents) — without worktree isolation, without per-merge overhead, at zero marginal cost. The restriction is enforceable via the agent contract (the brief's existing instructions) and does not prevent legitimate parallel work, because every recorded collision maps to a specific whole-tree command, not to two agents editing the same file. Note on the status quo this tests against: the current contracts already forbid *every* agent from git (the 2026-08-31 `git commit -A` incident is what added that line), and automation is the de-facto committer — so the designated-committer rule is a *relaxation* of the status quo, and the hypothesis under test is that the prohibition is the sufficient condition, checkable against the collision-free record since the line was added.

**Relation to same-iteration sibling `hypothesis:a00-4ed0dccd-68c060`:** converged independently on the same root cause — that node whitelists every kid's commands (structural, needs code); this one designates one committer (contract-level, zero code). Two of two same-target kids on the same idea is a live data point for goal:g4.1's L1.03 same-`--target` duplication finding.

**Grounded in g4.1's own data:** The goal node records three collisions — two of them whole-tree commands: `grid.py checkout --all` (silently reverting sibling edits, 2026-08-25) and `git commit -A` (sweeping a sibling's half-written node into the wrong commit, 2026-08-31); the third, the stale-.pyc race against a sibling rewriting a file mid-test, is a build-system problem this hypothesis does not cover (see scope boundary). The pattern is stated explicitly: *"every collision this goal has recorded came from a command whose blast radius is the tree, not from two agents editing the same file. File ownership has never once been the thing that failed."* File-ownership-in-the-brief was tested twice and held for disjoint files; what it could not scope was whole-tree commands. This hypothesis tests the complement: if whole-tree commands are the sole source, restricting them is the sole necessary fix.

**Proves it:** Run two parallel agents (N=2) with whole-tree commands banned for all agents except the iteration's designated committer. Across 3+ iterations, zero collisions occur — no reverted uncommitted work, no misattributed commits, no silent regressions. Sibling agents correctly attribute test failures to in-flight sibling edits (same as the 2026-08-22 test of file ownership, which held). Bonus: the restriction costs nothing — no checkout, no merge, no worktree creation — and is zero lines of code beyond the brief.

**Disproves it:** A collision occurs despite the restriction — either a file-level collision (two agents editing the same file, which the goal says has never happened) or a collision that cannot be attributed to a whole-tree command. Or: the restriction prevents legitimate work (e.g., both agents need to run the test suite on a tree that is clean, which no whole-tree command is required for). Or: the restriction is unenforceable in practice (agents ignore it because they need the banned command to do their job).

**Scope boundary:** This hypothesis does not cover the hierarchy questions from g4.1's second half (whose worktree, where review happens, iteration commit across N branches). Those are separate. It also does not address the stale-.pyc collision specifically, which is a build-system problem (`.pyc` cache invalidation, fixable with `-B` flag or a clean step) rather than a concurrent-edit problem.

**Relationship to sibling hypothesis:a00-2278675f-5a913a:** That hypothesis proposes worktree isolation at known cost (checkout + merge). This hypothesis proposes zero-cost command restriction as the first-line fix. If both are proved, the cheaper one wins. If this one is disproved (collision despite restriction), the data directly supports the worktree approach by eliminating the cheaper alternative.


## Agent Notes
Hypothesis: restricting whole-tree commands (git commit -A, git checkout --all, grid.py checkout --all) to one designated committer per iteration eliminates g4.1 collision pattern without worktree isolation. Zero-cost alternative to sibling worktree cost/benefit hypothesis (a00-2278675f-5a913a). No experiments run yet — pending.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent's review (a00-7c321808, iteration 1009). The kid wrote v1; it had no
THOUGHT block, and this one records the parent's edit rather than
fabricating the kid's. Two corrections: v1 counted "all three recorded
collisions — all from whole-tree commands", but the 2026-08-22 stale-.pyc
incident involved no command at all; the grounding sentence now says 2 of 3,
which matches the node's own scope boundary that already scoped the .pyc
race out. And the claim's "entirely eliminates the g4.1 collision pattern"
overclaimed the same way; it now names the class it eliminates. The parent
also added the status-quo note — the current contracts forbid all agents
from git, so the designated committer is a relaxation, not a new
restriction — and the cross-reference to the same-iteration sibling, which
reached the same root cause through a whitelist instead of a committer.
Verdict stays `pending`: no experiment has run, and the "zero collisions
over 3+ iterations" proves criterion needs them.
<!-- THOUGHT:END -->
