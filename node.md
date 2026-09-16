---
id: hypothesis:l4-rotate-out-audit-fixtures-carry-the-literal-seating-merged-shape-and-the-e2e-test-runs-both
mint_id: cc204a73c1ba45d4a88cb0ec5867a3f8
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
origin: master-sensei
scaffold_hash: 626938ccfcaf2bbb
season: 2
testable_claim: "Test-fidelity residue of SL7.127 (belam 10:38Z, wf_a9e4d1e7-271), two conjuncts, test-only: (1) the near_miss fixture (test_sensei_rotate_out_audit.py:603-607) is a hybrid -- it carries observations.b_generation, which the seating producer never writes; add a third param seating_merged = the literal _seating_record_merge_handover product (top-level gen_after + handover{seating_row_commit} with no join + transcript_path) asserting the same path/source; (2) the e2e rotate_out_audit test at :630 is parametrized over both shapes (near_miss + first_seating) so the composition through sensei.py:1702-1705 is committed, not read."
title: L4 rotate out audit fixtures carry the literal seating merged shape and the e2e test runs both
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-out-audit-fixtures-carry-the-literal-seating-merged-shape-and-the-e2e-test-runs-both

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fifth node of the session-keyed audit chain, test fidelity only. CARRIED, not fixed (belam 10:38Z): the out_rec fallback (sensei.py:1610, :1693) still keys on b_generation.before, so a rotate-out whose OUT record is itself a first seating stays unresolved -- kid-named, out of scope here. One kid, $1.5 cap, credit read first.
<!-- THOUGHT:END -->
