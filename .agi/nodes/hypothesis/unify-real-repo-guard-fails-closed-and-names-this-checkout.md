---
id: hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout
mint_id: f727e41f18ad4efbb30847902d5021fd
type: hypothesis
parents:
  - goal:g15.29.13
next_edges: []
assigned: director-engine (leaf goal:g15.29.13, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: ec9de67c437873b1
season: 2
testable_claim: After the fix, unify preflight refuses the engine's own git common root and its -tree sibling with or without a box.root cell (and refuses by name when nothing resolves), proved by a committed test red on the pre-fix bytes, with test_unify.py green.
title: "Unify real-repo guard fails closed and names this checkout (goal:g15.29.13; assigned: director-engine)"
town: core
---
# hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout

# hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout

**Assigned: director-engine** (leaf goal:g15.29.13; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
unify.py:395-413 returns () with no cell, frozen at import, so :416-418 never refuses; the live box.root names a path absent on this box, so the guard protects another box's repo; test_unify.py:526-535 hardcodes that path and :1040-1064 patch _FORBIDDEN_REAL_PATHS directly
```

## CLAIM
After the fix, unify preflight refuses the engine's own git common root and its -tree sibling with or without a box.root cell (and refuses by name when nothing resolves), proved by a committed test red on the pre-fix bytes, with test_unify.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_unify.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
unify.py · test_unify.py

HAZARD: never run unify against the real repo: tmp_path only

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
