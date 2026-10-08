---
id: hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish
mint_id: abd9e08d7d824a5bba46233d37b83c9f
type: hypothesis
parents:
  - goal:g15.29.7
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 5ebf6a4f2591347a
season: 2
testable_claim: "After EF.51+EF.56 land and after the fix, _complete_pending_key_swap (rotate.py ~17384) and every _finish_pending_swap_on_push caller complete a pending successor-key swap only when the authority leg was published or no publish was attempted, never on the trunk row alone, so a pending persisted by an `authority: FAILED` deferral is not completed by the next rotate; _apply_successor_key_gated treats `push: HELD` as not published (rotate.py ~17416); each proved by a committed test red on the pre-fix bytes, test_rotate*.py and test_rotate_key_authority.py green."
title: "The pending key swap completes only after the authority publish (held until EF.51+EF.56 land; assigned: director-engine)"
town: core
---
# hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish

# hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish

## Hypothesis

After EF.51+EF.56 land and after the fix, _complete_pending_key_swap (rotate.py ~17384) and every _finish_pending_swap_on_push caller complete a pending successor-key swap only when the authority leg was published or no publish was attempted, never on the trunk row alone, so a pending persisted by an `authority: FAILED` deferral is not completed by the next rotate; _apply_successor_key_gated treats `push: HELD` as not published (rotate.py ~17416); each proved by a committed test red on the pre-fix bytes, test_rotate*.py and test_rotate_key_authority.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.7; source R-EF51 M1 (C3 gate bypass via _complete_pending_key_swap) · R-EF20 M1 (push: HELD counted as not-failed) M2 (no frozen-path test)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
