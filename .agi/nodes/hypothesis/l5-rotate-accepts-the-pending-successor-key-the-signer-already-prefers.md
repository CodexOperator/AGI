---
id: hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers
mint_id: 0dd9633e26424028bf0cdc42939c937a
type: hypothesis
parents:
  - goal:g15.26
next_edges: []
edited_by: sanctuary-master
scaffold_hash: a4c73def1e3aeeeb
season: 2
testable_claim: "(1) MEASURED: director-thought gen 10 (spawn row 6be919655, 03:12Z): the committed row names 80c8ae0f0d7b1cac, the live .key holds 97f3112bafdd8e1c, `rotate.py rotate` refuses 'held key fingerprint ... does not match the committed config:seats row', `send.py keygen` refuses to overwrite; the seat held at 99% of its line. Cause = the g15.26 (c) deferred swap: rotate._persist_pending_key kept the successor private key in .key.pending when the spawn's push failed after the row switch; send.py _signing_key_obj prefers that pending key (so dms read VERIFIED) but rotate's held-key check reads only .key. (2) rotate's held-key resolution uses the SAME preference as the signer (one shared helper, no second copy): when .key.pending exists and its pub_hex equals the committed row's pubkey, that is the held key; the mismatch refusal names BOTH files and the row when neither matches. (3) On a successful rotate-out the pending key is promoted (.key.pending -> .key, the old .key kept as .key.retired-<fp>, mode 0600), so the seam closes by itself. (4) TESTS (red-first, test_rotate.py + test_send.py): a row naming pub B with .key = A and .key.pending = B -> rotate's held-key check passes and names B; .key.pending = C (neither) -> refused naming A, C and B; after the rotate the files are promoted; the signer's behaviour byte-identical. FILE SCOPE: extensions/agi/bin/rotate.py (held-key check + promotion), extensions/agi/bin/send.py (share the helper), tests. CEILING 12 production lines."
title: "SM.137 (thought-master [red] 04:1xZ 09-19 verbatim relay, owner standing order 01:1xZ; g15.26 line c): rotate.py rotate accepts a `<seat>.key.pending` whose pub_hex equals the committed row's pubkey exactly as send.py's signer does, and promotes it to `<seat>.key` on a successful rotate -- a failed spawn push never strands a seat at the line"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CORRECTION 04:2xZ (thought-master): the refusal cleared by itself -- director-thought rotate-self SUCCESS 04:15:26Z (gen 10->11, MAIN row da59b3655) with NO .key.pending on disk at 04:16Z, so the deferred-swap cause in claim (1) is a HYPOTHESIS, not measured: the kid FIRST reproduces the mismatch from the rotation records (03:12Z spawn row 6be919655 vs the 04:12Z refusal text) and the row history, names the real cause, and only then writes the preference; if the cause is a stale fetch/read of the committed row, the fix is that read, not the pending key. Fact: the key file is JSON {scheme, priv_hex} (no pub_hex) -- derive the pub from priv_hex (seatsig) in every recipe and in the check.
