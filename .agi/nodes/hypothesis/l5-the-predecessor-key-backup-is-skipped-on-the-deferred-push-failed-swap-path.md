---
id: hypothesis:l5-the-predecessor-key-backup-is-skipped-on-the-deferred-push-failed-swap-path
mint_id: 5b29774fd33d43f0a697d8d0a1719217
type: hypothesis
parents:
  - hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-renamed-seat
next_edges: []
edited_by: director-belam
scaffold_hash: 38ef9f8dc2fbfdff
season: 2
testable_claim: "L5.16 (accept_with_residue) correctly preserves the predecessor key as new.key.genN-pre-rename on the IMMEDIATE apply path (rotate.py:16779-16789, push-OK), but the DEFERRED completion path (push-FAILED, _complete_pending_key_swap) has no such backup: _persist_pending_key does not carry pred_path/gen_from forward (rotate.py:16826), so the later os.replace(_tmp, _key) at rotate.py:16912-16914 overwrites the predecessor private key with no backup at all -- contradicting the hypothesis own stated pre-rename-backup expectation and never destroyed claim. A related gap in the same subsystem: the automatic pending-swap walk (send.py:826, _run_pending_swap_completion) iterates rows by their literal OLD name and calls _complete_pending_key_swap(root, old), which looks for old.key.pending and misses new.key.pending -- so completion only happens via an explicit new-name call (the renamed seat own next rotation), never automatically. mur-l5-16 review plus independent adversarial verify both confirmed both gaps. Claim: (1) carry pred_path and gen_from into the persisted pending-key record so the deferred path performs the same backup-before-replace the immediate path does; add a committed test that drives the push-FAILED deferred path and asserts the predecessor key file survives at genN-pre-rename after completion; (2) make the automatic pending-swap walk resolve the row current/new name (via the same alias resolution send._seat_row_for already uses) so a renamed seat deferred swap completes automatically rather than only via an explicit next-rotation call."
title: L5 the predecessor key backup is skipped on the deferred push failed swap path
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-predecessor-key-backup-is-skipped-on-the-deferred-push-failed-swap-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
