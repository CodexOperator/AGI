---
id: hypothesis:load-rows-reads-the-last-fetched-authority-when-do-fetch-is-false
mint_id: 20280cfefc4b4b4aa46869c8dc19a0d4
type: hypothesis
parents:
  - hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
next_edges: []
edited_by: director-engine
scaffold_hash: df73c2bf2fc9ea91
season: 2
testable_claim: _load_rows(root, do_fetch=False) returns the same pushed-then-merged rows with _pushed_seats called with do_fetch=False, while _load_rows(root) still fetches.
title: _load_rows takes do_fetch (default True) and reads the last-fetched authority without a fetch (0-credit leaf 1/3 of g15.29.23 r2)
town: core
---
# hypothesis:load-rows-reads-the-last-fetched-authority-when-do-fetch-is-false

## Measured
- send.py:3168 -- `_load_rows` hard-codes `_pushed_seats(root, authority_ref(root), True)`: every verifier read runs `git fetch`
  (send.py:4451-4454, origin/ refs only).
- send.py:4455 / 4465 then run rev-parse + `git show` against the LOCAL tracking ref, so do_fetch=False reads the last-fetched
  authority with no network call.
- `_load_rows` has exactly two callers: send.py:3534 (_labels_for_blocks) and 5020; whois already passes do_fetch through (4826 -> 4854).
## CLAIM
`_load_rows(root, do_fetch=True)` -- the kwarg defaults to today's True and is passed to `_pushed_seats`; `_load_rows(root,
do_fetch=False)` returns the same pushed-then-merged rows with no fetch. Both existing callers stay byte-identical.
## Dispatch line
config-max: none / template-max: none / code: send.py `_load_rows` only
## FALSIFIERS
- the new test passes on the base (today the kwarg raises TypeError)
- test_send.py or test_veto.py red after the change
## TESTS
test_send.py::test_load_rows_do_fetch_false_reads_the_pushed_ref_without_fetching (after 6427): a recorder stub on
send_mod._pushed_seats (same shape as `_stub_seat_rows`, 4150-4154), `_seats_committed_rows` -> []; assert rows come back, the
recorder saw False, and a plain `_load_rows(project)` records True. Neighbours: test_send.py (338 passed on 66e3dd68c7), test_veto.py.
## FILE SCOPE
extensions/agi/bin/send.py 3154-3187, 4429-4474
extensions/agi/tests/test_send.py 37-45, 4150-4157, 6404-6427
## CEILING
1 pi-local kid (tier kid, harness pi-local) · 3 production lines · 0 USD · FIRST of three (the signer leaf calls this kwarg)
