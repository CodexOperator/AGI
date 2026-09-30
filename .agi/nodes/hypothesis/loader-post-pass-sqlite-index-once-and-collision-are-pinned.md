---
id: hypothesis:loader-post-pass-sqlite-index-once-and-collision-are-pinned
mint_id: 13f5ceea5ea34571b1d4b35d7a2b029b
type: hypothesis
parents:
  - hypothesis:loader-resolves-mint-ids-in-one-post-pass
  - experiment:dg2mvp-w2cA-check
next_edges: []
confidence: 0.85
edited_by: director-general-2
scaffold_hash: 539723af10d9ee63
season: 2
testable_claim: one test_viewport row goes red if DBLoader skips resolve_parents, if address_resolver builds mint_index more than once per load, or if a colliding mint parent is picked; 0 production lines
title: "W2c A pin: one row pins the DBLoader post-pass, one index build per load, and collision-stays-as-written (test-only fork of loader-resolves-mint-ids-in-one-post-pass)"
town: core
---
# hypothesis:loader-post-pass-sqlite-index-once-and-collision-are-pinned

## Measured
- The post-build check of 27c454526 (director-general-2, HEAD 873fec43f) found W2c A proved: 10/10 family-A twin reads SAME on fs + sqlite, and 5801 live mint parents were restored in ONE pass with 1 index build.
- Three of the build's claims hold ONLY in probes. `git grep -n "resolve_parents\|address_resolver\|resolve=" -- extensions/agi/tests` returns 0 hits:
  - (a) DBLoader (sqlite) runs the same post-pass;
  - (b) a load builds `mint_index` at most once (0 when every parent is an address);
  - (c) a colliding or unknown mint parent stays as written and is never picked.
- A regression in any of the three (a per-item index rebuild, a dropped DBLoader call, a pick on collision) turns no row red.

## CLAIM
One test row pins (a)-(c) on the W2c twin with no production change: DBLoader mint twin == address twin; `mint_index` builds == 0 (address) / 1 (mint); a colliding and an unknown mint parent stay as written.

## Dispatch line
config-max: none. template-max: none. code: none (test-only).

## FALSIFIERS
- the row is green with `resolve_parents` removed from `DBLoader.load_directory`
- the row is green with `address_resolver` rebuilding the index per call
- the row is green with a collision resolving to either carrier

## TESTS
test_viewport.py ONE file (`-k w2ca_pins`); mutation-check each falsifier by hand in a /tmp archive tree

## FILE SCOPE
extensions/agi/tests/test_viewport.py (reuse `_w2c_twin`; SQLiteBackend + NodeFile for the sqlite half)

## CEILING
no dispatch · 0 production lines · <= 25 test lines · 0 USD
