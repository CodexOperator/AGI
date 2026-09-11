---
id: hypothesis:l4-the-belam-cap-record-is-planned-first
mint_id: 8011996b7f8b4e198eea6d5dbde6798b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-rotate-self-keeps-the-numeral-window-reaps-fifo-and-records-before-it-terms
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9720a99f984efa25
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI in the merge-up 28 report, ACCEPTED by the prime 05:47Z as written. p4 (L4.127 parent's caveat, experiment:a00-d768282d-81d4d6): `_reap_belam_oldest` (rotate.py, landed 9b4186086) records `{oldest, window_id, pids, chain, reaped, ps_after}` AFTER the FIFO TERM of the oldest predecessor — harmless today (that TERM never targets rotate.py's own chain) but the same failure shape as (e): if rotate.py dies between the TERM and the write, the reap is unevidenced. CLAIM: the belam-cap record entry is written `{planned: true, oldest, window_id, pids, chain}` BEFORE the first TERM, then best-effort updated with `reaped`/`ps_after` after — exactly the (e) shape `_record_s12_self_reap` now uses; the F1 fixture asserts the planned entry exists when the TERM is interrupted (monkeypatch `_reap_chain` to raise) and the observed entry when it completes; --dry-run text unchanged. FALSIFIER: an interrupted cap reap whose record lacks the belam entry. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_reap_belam_oldest` + its call site ONLY) + extensions/agi/tests/test_rotate_handover.py. SERIAL on rotate.py behind L4.144 (g15-6), 0b-b and g15-8 — cut last in that queue (or fold into whichever of those the point cuts if the prime rules so). EXCLUDED: everything else."
title: The Belam-cap reap writes its planned entry BEFORE the FIFO TERM, the same shape as the s12 own-chain evidence
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-belam-cap-record-is-planned-first

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI in the merge-up 28 report, ACCEPTED by the prime 05:47Z as written. p4 (L4.127 parent's caveat, experiment:a00-d768282d-81d4d6): `_reap_belam_oldest` (rotate.py, landed 9b4186086) records `{oldest, window_id, pids, chain, reaped, ps_after}` AFTER the FIFO TERM of the oldest predecessor — harmless today (that TERM never targets rotate.py's own chain) but the same failure shape as (e): if rotate.py dies between the TERM and the write, the reap is unevidenced. CLAIM: the belam-cap record entry is written `{planned: true, oldest, window_id, pids, chain}` BEFORE the first TERM, then best-effort updated with `reaped`/`ps_after` after — exactly the (e) shape `_record_s12_self_reap` now uses; the F1 fixture asserts the planned entry exists when the TERM is interrupted (monkeypatch `_reap_chain` to raise) and the observed entry when it completes; --dry-run text unchanged. FALSIFIER: an interrupted cap reap whose record lacks the belam entry. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_reap_belam_oldest` + its call site ONLY) + extensions/agi/tests/test_rotate_handover.py. SERIAL on rotate.py behind L4.144 (g15-6), 0b-b and g15-8 — cut last in that queue (or fold into whichever of those the point cuts if the prime rules so). EXCLUDED: everything else.

**PRIME (merge-up 28 review, 3cd6e6bd9):** this node = g15-10 (`:4817 vs :4828` on 9b4186086). ACCEPTED; cut FIRST in the rotate.py queue after L4.144, then g15-11 (`hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap`), then g15-12 (`hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window`).
