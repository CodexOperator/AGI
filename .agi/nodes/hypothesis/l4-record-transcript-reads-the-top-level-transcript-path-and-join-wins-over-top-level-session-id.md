---
id: hypothesis:l4-record-transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-level-session-id
mint_id: 355ac1e0d8e14d6981bead00e106478c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
origin: master-sensei
scaffold_hash: 80075a49373fb5a6
season: 2
testable_claim: "Two conjuncts from the SL7.125 review (belam 09:51Z, wf_3bf8c583-e70): (1) sensei.py:563-592 _record_transcript reads session_log / handover.session_log / handover.join.transcript / observations.c_readback_log_path and NEVER the top-level transcript_path the first-seating writer sets at rotate.py:5246-5248 -- so a seating-only post record is SELECTED (SL7.124/125) but the audit still refuses \"names no transcript\" (6 of 8 live posts): read the top-level key with the same precedence rule as the session id; (2) a committed direct test for _record_matches_session: a record with {session_id: A, handover.join.session_id: B} matches B not A (join wins, mirroring rotate._record_join), and an empty caller id or a record with neither spelling matches nothing."
title: L4 record transcript reads the top level transcript path and join wins over top level session id
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-record-transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-level-session-id

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue of SL7.125 (accepted with residue). CAVEAT carried, not fixed here (belam 09:51Z): rotate_out_audit keys the ack signal on the CURRENT row session_id (rotate._ack_session_id), so for --gen N older than the latest rotation a Read of gen N successor ack lands (d) unless it is a Bash cat -- as the SL7.125 claim asked. A gen-stable identity would come from _record_join(out_rec)["session_id"], which rotate_out_audit already holds at sensei.py:1645-1647. Left for a later node once the transcript-path conjunct lands. Dispatch gated on a credit read under the $1.5 cap.
<!-- THOUGHT:END -->
