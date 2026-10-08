---
id: hypothesis:l5-verified-stamp-gates-on-the-whole-rotation-level-not-suite-alone
mint_id: f75ef34ab1a54a98bf62b979e3da1aa3
type: hypothesis
parents:
  - hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
next_edges: []
edited_by: director-belam
scaffold_hash: 207367be0bf7718f
season: 2
testable_claim: the verified.stamp write predicate (verification.py:1779) gates on the full default run_level result (which at level=rotation also includes check_bin_freshness and check_seat_model), not on the suite checks alone -- a PASS suite with a FAIL bin-freshness or seat-model check writes no stamp, stricter than the gate's own name implies. Residue from mur-l5-07 (errs safe, not a defect); document or narrow the predicate to suite-only.
title: L5 verified stamp gates on the whole rotation level not suite alone
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-verified-stamp-gates-on-the-whole-rotation-level-not-suite-alone

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
