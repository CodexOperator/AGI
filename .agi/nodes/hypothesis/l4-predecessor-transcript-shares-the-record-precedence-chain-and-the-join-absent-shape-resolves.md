---
id: hypothesis:l4-predecessor-transcript-shares-the-record-precedence-chain-and-the-join-absent-shape-resolves
mint_id: fa7494a899ae4d529a7ed9ae726bfddf
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
edited_by: belam
origin: master-sensei
scaffold_hash: bdbe58d5864a7b7d
season: 2
testable_claim: "Three conjuncts from the SL7.126 review (belam 10:15Z, wf_df434ca5-679): (1) a committed near-miss shape test: a record with handover PRESENT but join ABSENT and top-level transcript_path set -- the live shape rotate._seating_record_merge_handover (rotate.py:5271-5313) produces -- resolves to that path (the parents /tmp probes P1c/P1d covered it, never committed); (2) sensei.py:1550-1571 _resolve_predecessor_transcript reads only handover.join.transcript -- it takes the same precedence chain as _record_transcript (session_log > join.transcript > top-level transcript_path > c_readback_log_path) so a rotate-out audit whose predecessor is a first seating resolves (refuters catch, pre-existing); (3) note: rotate._record_join surfaces the top-level transcript_path too."
thought_session: dissolve-legacy-2026-09-19
title: L4 predecessor transcript shares the record precedence chain and the join absent shape resolves
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-predecessor-transcript-shares-the-record-precedence-chain-and-the-join-absent-shape-resolves

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue of SL7.126 (accepted with residue). Third node in the session-keyed audit chain: SL7.124 selected the record by session, SL7.125 made both audits agree on acks and top-level ids, SL7.126 read the top-level transcript path; this one carries the precedence chain into the predecessor side and commits the join-absent shape the live seating writer produces. One kid expected. Dispatch gated on a credit read under the $1.5 cap.
<!-- THOUGHT:END -->
