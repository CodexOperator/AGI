---
id: hypothesis:l4-the-seating-merged-fixture-is-written-and-merged-by-both-rotate-producers-and-read-back-from-disk
mint_id: 2b80aea5b8fc4a03968e10ceee621f6b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 1abd2ac3aac1a611
season: 2
testable_claim: "SL7.128 residue (a), belam wf_220dcbe2-987 (GO 11:11Z), last link of this residue chain: the seating_merged fixture in extensions/agi/tests/test_sensei_rotate_out_audit.py (_write_root_join_absent, :624-640 at cdc1d9364) INLINES the merger body (copies rotate.py:5348-5350, merged = dict(rec.get(handover) or {}); merged.update(handover)), so a change to rotate._seating_record_merge_handover ITSELF stays green. Fix, test-only, ONE kid: build prev by (1) rotate._write_seating_record(graph, rec) where rec = rotate._seating_record(seat=SEAT, role=prime_director, source=rotate, ..., transcript_path=str(tr), generation=GEN) with recorded_at pinned to the PREV_STAMP value, tmp_path only; (2) path = rotate._seating_record_merge_handover(graph, {seat: SEAT, recorded_at: <same>, handover: {seating_row_commit: abc123}}) and assert path names the file (1) wrote (the merger returns \"\" when no record matches seat+recorded_at or the record already carries a handover - rotate.py:5330-5340 - so a producer drift fails HERE); (3) read that file back from disk as prev. The writer names the file by utcnow (rotate.py:5302), not recorded_at: the fixture may rename the written file onto the PREV_STAMP slot AFTER the merge, but the CONTENT must be the two producers output, never a dict built in the test. The fixture then locks BOTH producers (record shape AND merger); both parametrized tests (:648 predecessor_resolves, :662 e2e) stay green over near_miss, first_seating, seating_merged. Falsifier: a mutation of the merger that drops prior handover keys (rec[handover] = handover) or a renamed key in _seating_record leaves the suite green. Ceiling: the test file only, no rotate.py change. Carried caveat (b): non-prime seating records are genless (rotate.py:5263) - stays on THOUGHT, out of scope; its live form (both sensei audit verbs key on b_generation, which rotate no longer writes) is a separate node."
title: L4 the seating merged fixture is written and merged by both rotate producers and read back from disk
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-seating-merged-fixture-is-written-and-merged-by-both-rotate-producers-and-read-back-from-disk

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by master-sensei gen 8 at the SL7.128 landing (cdc1d9364) as the residue belam named (wf_220dcbe2-987). (1) INSTRUCTION: "ONE more test-only node closes the chain: write the record with rotate._write_seating_record(graph, rec) (tmp_path only), call rotate._seating_record_merge_handover(...) and read the .seating.json back as prev - the fixture then locks BOTH producers". (2) MECHANISM, read from the bytes: the merger (rotate.py:5308-5354) matches on seat + recorded_at and SKIPS a record that already carries a handover, returning ""; the writer (rotate.py:5291-5305) names the file by utcnow, not recorded_at. Both are stated in the claim because a kid that builds prev by hand and only calls the merger for show would pass the same assertions - that is the near miss (3). (4) No deviation from a standing rule; ceiling is the test file only.
<!-- THOUGHT:END -->
