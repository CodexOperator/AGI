---
id: hypothesis:l4-the-sensei-audit-verbs-resolve-the-window-by-post-and-record-never-by-b-generation
mint_id: 869ce668e89444caaefebe23056856a7
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 278ca1d291338cda
season: 2
testable_claim: "MEASURED 2026-09-16 11:4xZ (master-sensei): sensei.py rotate-out-audit and wake-audit default and match the window by observations.b_generation (sensei.py:1686 gen = _gen_bounds(records[-1][1])[0]; :1693 out_rec = the record whose _gen_bounds(rec)[0] == gen; --gen on both parsers :1899/:1914). rotate.py:4701-4703 writes b_generation ONLY when gen_before is not None AND the role is prime or None - guard landed in e85a1a797 (SM.243, 2026-09-16) - so every NON-PRIME post rotate-self record carries no b_generation and no gen_before/gen_after at any level (thought-master.20260916T110753Z.json, sensei-director.20260916T104936Z.json: measured, the only gen token is prose inside handover strings), and the verbs refuse: ERR cannot default --gen: the latest record has no b_generation.before (thought-master, 11:1xZ). The master-sensei record 20260916T105216Z still carries it (role None on its path): the keying is inconsistent by call path, not merely absent. Owner 2026-09-13 (doc:l4-owner-decisions): No generations anywhere - label by post + record timestamp. CLAIM, one kid, sensei.py + tests only, rotate.py untouched: both verbs resolve the window by RECORD - default = the post latest rotate-self record; --record <stamp> selects one by the recorded_at stamp in its filename (the same key rotate.py status --record takes); the out-window = the predecessor calls after its last work act up to that record recorded_at; the wake-window = from that record join to the successor first commit; --gen stays as a deprecated alias that resolves to the record whose b_generation.before matches WHEN present and refuses by name otherwise, never the default; every printed line names the record stamp, never a generation. Test, committed: run both verbs on tmp_path copies of (1) a CURRENT non-prime rotate-self record shaped like thought-master.20260916T110753Z.json (genless) and (2) a prime record carrying b_generation, and assert both resolve to the planted transcripts with source lines naming the stamp. Falsifier: sensei.py rotate-out-audit --post thought-master with no flags on the committed 20260916T110753Z record still refuses, or the prime record resolves to a different window than the gen path did. Deviation from the Prime wording (top-level gen_before/gen_after with b_generation fallback), measured reason: a rotate-self record has neither at the top level - only a SEATING record does, and only for prime roles - so that keying would leave TM and SD un-auditable; recorded in THOUGHT."
title: L4 the sensei audit verbs resolve the window by post and record never by b generation
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sensei-audit-verbs-resolve-the-window-by-post-and-record-never-by-b-generation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by master-sensei gen 8 after the SL7.129 landing (ba888a20e), the lane next node belam ACCEPTED 11:43Z with "measure first which commit stopped writing b_generation (name it in the claim)". (1) INSTRUCTION: belam wording was "the verbs key on the record top-level gen_before/gen_after with b_generation as the fallback, plus a committed test on a current rotate-self record". (2) MECHANISM, measured: rotate.py:4701-4703 writes b_generation only for a prime role or role None (guard e85a1a797, SM.243, today); a rotate-self record for a non-prime post carries NO gen_before/gen_after at the top level either - those keys exist only on the SEATING record shape (rotate.py:5263, prime-gated too). Read from the committed records: thought-master.20260916T110753Z.json and sensei-director.20260916T104936Z.json have no gen key at any depth; master-sensei.20260916T105216Z.json has b_generation. (3) NEAR MISS: keying on top-level gen_before/gen_after satisfies the words and loses the mechanism - TM and SD stay un-auditable because the key is not there to read. (4) DEVIATION: the claim keys on post + record stamp (the owner 09-13 order, no generations anywhere) with --gen as a deprecated alias; the writer side is left alone because the missing gens are the owner rule, not the defect.
<!-- THOUGHT:END -->
