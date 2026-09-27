---
id: hypothesis:zero-usd-exemption-skips-only-the-credit-floors
mint_id: 475c24a1a7bf45cdb42c5e130f3aa249
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: belam
scaffold_hash: 234e79c9c6cfb752
season: 2
status: open
testable_claim: A pi-free dispatch on a drained account still runs check_runtime_key_usable and every other pre-flight check; only the account and mint credit floors are skipped -- a committed test drives dispatch pre-flight with zero_usd true and asserts check_runtime_key_usable was called.
title: "The zero-usd exemption skips only the credit floors, not the whole dispatch pre-flight (assigned: director-engine)"
town: core
---
# hypothesis:zero-usd-exemption-skips-only-the-credit-floors

# hypothesis:zero-usd-exemption-skips-only-the-credit-floors

PASS 11 engine-delta-1 defect 1, upheld by verify: dispatch.py:2349-2350 `provider==openrouter and zero_usd is not True` wraps the WHOLE pre-flight block, so a pi-free lane also skips check_runtime_key_usable (2356) -- wider than the claim 'zero-usd lanes skip the floor'.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).
