---
id: hypothesis:g716111-aa2-a-tree-lives-one-generation-commit-always-purge-at-the-out-line
mint_id: 2284fc8ba2b241e190298ed5bc67fa02
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 33a23788daf777ef
season: 2
testable_claim: "A crash restart keeps every tree and its uncommitted edit and the next turn commits it (AA2.14); an out-line (`~/.fresh`) purges all trees after the commit; trees created per session <= distinct nodes touched, i.e. no per-turn re-pull (AA2.15); the byte account is agi-turn -129 B (the per-turn drop loop goes) and agi-flush +17 B (`[ -e ~/.fresh ]&&` before its purge), both expansion; the RAM cap stays AGI_WT_HOLD (60 %)."
title: "AA2.14/15: a node tree is committed at every turn and every stop but PURGED only when the generation ends (~/.fresh), so a crash keeps every tree with its uncommitted edit and no node is re-pulled per turn"
town: core
---
# hypothesis:g716111-aa2-a-tree-lives-one-generation-commit-always-purge-at-the-out-line

## Measured
- doc:radically-simple-engine AA2 'Tree lifetime = one generation': today agi-turn drops every unclaimed tree EVERY turn (the 129 B loop) and agi-flush drops ALL trees at EVERY stop, crashes included, though the unit already keeps its RAM dir across a restart (`RuntimeDirectoryPreserve=restart`, engine-root:31). Rule: COMMIT always, PURGE only when the generation ends.
- Owner 00:3xZ: 'I also am not sure if each turn should generate and purge a worktree, or rather worktree starts and new ones get added dynamically throughout session then purged at session end.'

## CLAIM
A crash restart keeps every tree and its uncommitted edit and the next turn commits it (AA2.14); an out-line (`~/.fresh`) purges all trees after the commit; trees created per session <= distinct nodes touched, i.e. no per-turn re-pull (AA2.15); the byte account is agi-turn -129 B (the per-turn drop loop goes) and agi-flush +17 B (`[ -e ~/.fresh ]&&` before its purge), both expansion; the RAM cap stays AGI_WT_HOLD (60 %).

## Dispatch line
config-max: none / template-max: none / code: agi-turn (-129 B), agi-flush (+17 B).

## FALSIFIERS
AA2.14 a crash restart keeps every tree and its uncommitted edit; the next turn commits it; an out-line purges all · AA2.15 trees created per session <= distinct nodes touched · negative: a stop without ~/.fresh leaves the trees.

## TESTS
a scratch session: kill -9 mid-edit, restart, assert the tree and the edit survive and the next turn commits one node commit; an out-line run purges after the commit.

## FILE SCOPE
agi-turn (the loop) · agi-flush (the .fresh guard) · tests. HORIZON behind the grid-commit hypothesis.

## CEILING
1 parent · kids <= 1 · net -112 B expansion · regular review.
