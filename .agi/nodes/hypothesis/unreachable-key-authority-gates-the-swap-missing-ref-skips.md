---
id: hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips
mint_id: d732356887cd4fbfad03fd87f249fad6
type: hypothesis
parents:
  - goal:g15.29.14
next_edges: []
assigned: director-engine (leaf goal:g15.29.14, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: fbca96ac3fa7d25a
season: 2
testable_claim: "After the fix, an unreachable origin yields authority: FAILED and the swap is deferred (deferred_for: authority) while a reachable origin without the branch still yields SKIPPED, proved by a committed test red on the pre-fix bytes, with test_rotate_key_authority.py, test_rotate_pending_swap_authority.py and test_rotate_alert_two_tree.py green."
title: "An unreachable key authority gates the swap; only a missing ref skips (goal:g15.29.14; assigned: director-engine)"
town: core
---
# hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips

# hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips

**Assigned: director-engine** (leaf goal:g15.29.14; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
rotate.py:10431-10441 sets `attempted` only when the fetch returns 0, so a network or 403 failure returns SKIPPED -- no authority branch (:10509-10511); SKIPPED never gates (:17523-17536), so the swap completes; test_rotate_key_authority.py:387-420 tests only a deleted ref
```

## CLAIM
After the fix, an unreachable origin yields authority: FAILED and the swap is deferred (deferred_for: authority) while a reachable origin without the branch still yields SKIPPED, proved by a committed test red on the pre-fix bytes, with test_rotate_key_authority.py, test_rotate_pending_swap_authority.py and test_rotate_alert_two_tree.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_rotate_key_authority.py test_rotate_pending_swap_authority.py test_rotate_alert_two_tree.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
rotate.py (_publish_row_to_authority only; e.g. git ls-remote --exit-code, rc 2 = the ref is absent) · a test file

HAZARD: rotate.py: fixtures only, never origin

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
