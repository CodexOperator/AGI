---
id: hypothesis:authority-deferred-signer-signs-with-the-key-the-verifiers-row-names
mint_id: 727955b7a700411d8047babb39708e3a
type: hypothesis
parents:
  - hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
next_edges: []
edited_by: director-engine
scaffold_hash: a7c7350f9641b4ba
season: 2
testable_claim: With an authority-deferred pending key, a dm signed by _sign_line reads VERIFIED in _verify_block both when the authority's pushed row names no key cell and when it names the predecessor.
title: An authority-deferred signer signs with the key the verifier's own row names (0-credit leaf 2/3 of g15.29.23 r2)
town: core
---
# hypothesis:authority-deferred-signer-signs-with-the-key-the-verifiers-row-names

## Measured
- send.py:235 -- `_signing_key_obj` skips an authority-deferred pending by default (the `_sign_line` call at 281); otherwise
  236-237 match the pending only against `_seats_committed_rows` -- an INFERENCE of the authority's key.
- send.py:3485 -- the verifier picks the row with `_row_for_label(root, rows, from)`: the pushed row first (3289-3292), else MAIN's
  committed row (3293-3299); rows come from 3534 -> 3172; a pushed row with no pubkey / sig_scheme is filled from MAIN
  (3258-3266) = the SUCCESSOR.
- so with no key cell on the authority the signer uses the predecessor and 3382 returns FORGED (mur E2 STANDS on EF.84).
- rotate.py:18186-18187 passes prefer_authority_deferred=True: that branch (the committed-row comparison) is unchanged.
## CLAIM
When the pending is authority-deferred and prefer_authority_deferred is False, the row is
`_row_for_label(root, _load_rows(root, do_fetch=False), seat)` -- the verifier's OWN resolver, called, never copied; the pending
key signs only if that row's pubkey equals its pub_hex, otherwise the live key signs. Push-deferred and prefer=True: unchanged.
## Dispatch line
config-max: none / template-max: none / code: send.py `_signing_key_obj` only
## FALSIFIERS
- the new test passes on the base (case i reads FORGED today)
- the fix copies `_load_rows` / `_row_for_label` instead of calling them, or the first recorded do_fetch is True
- a named test file red after the change
## TESTS
test_rotate_pending_swap_authority.py::test_authority_deferred_signer_uses_the_verifiers_row -- `_mk_seat_key` (26),
`_pending(reason="authority")` (50), `_patch_committed` (38) with a committed row naming the successor WITH sig_scheme (without it
the verdict is UNKEYED, 3374-3375); a recorder stub on bin_send._pushed_seats. (i) pushed row `{"name": "aa"}` ->
`_verify_block(tmp_path, _load_rows(tmp_path), meta, text)` == "VERIFIED aa (ed25519, main-committed)" and the first recorded
do_fetch is False; (ii) the pushed row names the predecessor (ed25519) -> "VERIFIED aa (ed25519)".
AMEND test_send_signs_with_the_authority_key_when_deferred_on_authority (352-382): add a pushed stub naming the predecessor -- its
fixture has no pushed row, so without it the verifier's chain resolves the committed successor and 376-379 pin the FORGED case.
Neighbours: test_rotate_pending_swap_authority.py (9), test_send.py (339), test_rotate_key_authority.py (17) on d19b619aed.
## FILE SCOPE
extensions/agi/bin/send.py 199-245 (read 3240-3299, 3455-3521)
extensions/agi/tests/test_rotate_pending_swap_authority.py 26-60, 352-382
extensions/agi/bin/rotate.py 18177-18209 (read-only)
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn; TMM.89) · ~12 production lines · 0 USD · SECOND (after the do_fetch leaf merges)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-checked against d19b619aed before dispatch (03:5xZ 09-24): EF.91 (the do_fetch leaf this one depends on) and EF.93 are merged; EF.93 added 8 lines above the rotate.py citations, so they moved +8 with content unchanged, and the neighbour counts are the base's own (EF.91 added 1 test to test_send.py, EF.93 added 2 to test_rotate_key_authority.py). Claim, tests and file scope otherwise unchanged; the precondition is met.
<!-- THOUGHT:END -->
