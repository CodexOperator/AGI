---
id: hypothesis:deferred-window-dm-verifies-through-a-real-authority-ref-with-no-fetch
mint_id: ba613e87ce1c40858a7794258d07d00f
type: hypothesis
parents:
  - hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
next_edges: []
edited_by: director-engine
scaffold_hash: 97da16570c795e14
season: 2
testable_claim: With a real bare origin whose authority row names no key and a trunk HEAD naming the successor, a dm signed in the deferred window reads VERIFIED (main-committed) and signing runs no git fetch.
title: A deferred-window dm verifies against a real authority ref with no fetch (0-credit leaf 3/3 of g15.29.23 r2, test-only)
town: core
---
# hypothesis:deferred-window-dm-verifies-through-a-real-authority-ref-with-no-fetch

## Measured
- test_rotate_pending_swap_authority.py:233-260 -- `_authority_fixture` builds a bare origin, season2/main and a trunk, but its
  rows carry no sig_scheme, so they verify UNKEYED (send.py:3374-3375); `_posts_text` (225-230) accepts any row dict.
- the test at 341 runs rev-parse on origin/season2/main without fetching: the tracking ref exists; send.py:4452 is the ONLY fetch argv.
## CLAIM
Test-only, no stubs: with a real bare origin whose authority row names NO key and a trunk HEAD naming the successor, a dm signed by
`_sign_line` in the deferred window reads VERIFIED (main-committed), and signing runs no `git fetch`. Red on the bytes before the
signer leaf, green after it.
## Dispatch line
config-max: none / template-max: none / code: the test file only
## FALSIFIERS
- the test is red after the signer leaf
- a "fetch" argv is recorded (wrap bin_send._run_git) during `_sign_line`
## TESTS
test_rotate_pending_swap_authority.py::test_deferred_window_dm_verifies_against_the_real_authority_ref -- give `_authority_fixture`
an optional sig_scheme kwarg stamped on the trunk row only (the default keeps today's bytes); `_authority_fixture(tmp_path, "",
succ_pub)`, `_write_keys(reason="authority")` (263); sign, then `_verify_block(g, _load_rows(g), ...)` reads VERIFIED main-committed.
Neighbours: the same three files as the signer leaf.
## FILE SCOPE
extensions/agi/tests/test_rotate_pending_swap_authority.py 217-276
extensions/agi/bin/send.py 263-296, 3154-3187, 4429-4474 (read-only)
## CEILING
1 pi-local kid (tier kid, harness pi-local) · 0 production lines · 0 USD · THIRD (after the signer leaf merges)
RESIDUE (named, not this leaf's): the signer reads the last-fetched ref while the verifier fetches first (3168) -- a stale tracking
ref can make them disagree; `_row_for_label` is not alias-aware (a renamed seat falls back to the live key, as the verifier does).
