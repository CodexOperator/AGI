---
id: experiment:a00-392a464e-83efc0
mint_id: 41b5c6cb452f427982cde6adc2dd1423
type: experiment
parents:
  - hypothesis:authority-deferred-signer-signs-with-the-key-the-verifiers-row-names
next_edges: []
confidence: 0.98
edited_by: a00-fb87a660
evidence_runs:
  - experiment:a00-392a464e-83efc0
loop: hypothesis:authority-deferred-signer-signs-with-the-key-the-verifiers-row-names@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 661b1c31022e5736
season: 2
title: Authority-deferred signer follows verifier row
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-392a464e-83efc0

## Experiment

Changed `_signing_key_obj` so an authority-deferred pending is selected by the
verifier's own resolver: `_row_for_label(root, _load_rows(root, do_fetch=False), seat)`.
The `prefer_authority_deferred=True` holder-comparison path and push-deferred path retain
committed-row behavior. The test stub now preserves its pushed row and passes the string
pubkey already returned by `_mk_seat_key`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_pending_swap_authority.py -q`
  -> `10 passed`.
- `python3 -m pytest extensions/agi/tests/test_send.py -q`
  -> `339 passed, 11 warnings` (existing deprecation warnings only).

The targeted test observes one `_pushed_seats` call with `do_fetch=False`, verifies an
unkeyed pushed row against the committed successor, and verifies a pushed predecessor row
against the signature produced by the predecessor key.

## Agent Notes
Authority-deferred signing now resolves the cached verifier row with do_fetch=False; targeted and send suites pass.

probes: auth negative (wrong verifier-row pubkey must not select the pending key; direct _signing_key_obj fixture returned the live private key) PASS; wire check (send.py _signing_key_obj authority-deferred prefer=False calls _row_for_label(root, _load_rows(root, do_fetch=False), seat), and test records do_fetch=False) PASS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to implement the authority-deferred signer resolver and prove the named tests. The machine now does this in send.py _signing_key_obj: prefer=False calls _row_for_label with _load_rows(do_fetch=False), while prefer=True remains on _seats_committed_rows. The near miss was treating the committed successor as the verifier row, which would preserve the old forged result. My auth negative probe supplied a wrong verifier-row pubkey and observed fallback to the live key, so the pending is selected only on an exact match.
<!-- THOUGHT:END -->
