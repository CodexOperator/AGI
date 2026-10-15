---
id: hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
mint_id: 593be558c8324bb48023e44fb42fec73
type: hypothesis
parents:
  - goal:g15.29.23
next_edges: []
assigned: director-engine (leaf goal:g15.29.23, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 028c6f1e68aee161
season: 2
testable_claim: After the fix, an authority-deferred pending completes exactly when a later authority publish of that row succeeds (a retried publish at the next rotate or push-OK site), and until then send signs with the key whose pub the authority row holds, never the pending one, proved by committed tests red on the pre-fix bytes, with test_rotate_pending_swap_authority.py, test_rotate_key_authority.py and the send signing tests green.
title: "An authority-deferred key swap completes at the next successful publish (goal:g15.29.23; assigned: director-engine)"
town: core
---
# hypothesis:authority-deferred-key-swap-completes-at-the-next-publish

# hypothesis:authority-deferred-key-swap-completes-at-the-next-publish

**Assigned: director-engine** (leaf goal:g15.29.23; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
after EF.67 (44df35443f): rotate.py:10676 is the only authority_line caller (the re-key leg, after HEAD advances); the direct pre-mint completion (~19101/19128) and the push-OK sites refuse an authority-deferred pending, so it never completes; the next rotation's _rotate_successor_key reads the predecessor .key; send._signing_key_obj (send.py:216-227) returns the .key.pending whenever its pub_hex matches the committed row
```

## CLAIM
After the fix, an authority-deferred pending completes exactly when a later authority publish of that row succeeds (a retried publish at the next rotate or push-OK site), and until then send signs with the key whose pub the authority row holds, never the pending one, proved by committed tests red on the pre-fix bytes, with test_rotate_pending_swap_authority.py, test_rotate_key_authority.py and the send signing tests green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_rotate_pending_swap_authority.py test_rotate_key_authority.py test_send*.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
rotate.py · send.py (_signing_key_obj) · a test file

HAZARD: rotate.py + send.py signing: fixtures only, never a real key or origin; dispatch AFTER g15.29.14 lands (same functions)

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
