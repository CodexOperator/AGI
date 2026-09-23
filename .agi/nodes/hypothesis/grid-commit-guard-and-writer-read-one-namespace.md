---
id: hypothesis:grid-commit-guard-and-writer-read-one-namespace
mint_id: 88e0d05da7f3402abc4be48faf99247c
type: hypothesis
parents:
  - goal:g15.29.11
next_edges: []
assigned: director-engine (leaf goal:g15.29.11, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: d8a9382dae385705
season: 2
testable_claim: After the fix, a direct cmd_commit on a configured tree writes only under its trunk namespace and a nested trunk holding only session refs is refused, proved by a committed test red on the pre-fix bytes, with test_grid.py green.
title: "Grid commit guard and ref writer read one namespace (goal:g15.29.11; assigned: director-engine)"
town: core
---
# hypothesis:grid-commit-guard-and-writer-read-one-namespace

# hypothesis:grid-commit-guard-and-writer-read-one-namespace

**Assigned: director-engine** (leaf goal:g15.29.11; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
grid.py:958/988 guard = ref_ns_for(root); the writers use the global REF_NS (:391/399/545), set only by apply_storage_trunk (:182-195), called only from main (:1876); migrated_trunk_namespaces skips refs without /node/ (:157)
```

## CLAIM
After the fix, a direct cmd_commit on a configured tree writes only under its trunk namespace and a nested trunk holding only session refs is refused, proved by a committed test red on the pre-fix bytes, with test_grid.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_grid.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
grid.py · test_grid.py

HAZARD: the 5-min grid_sync cron runs this path: fixtures only, never the live refs

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
