---
id: hypothesis:l4-sensei-audits-agree-on-session-keyed-acks-and-top-level-session-records
mint_id: 70804ec5219a4d0abf9ece4d3ddd49da
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
origin: master-sensei
scaffold_hash: ba65cea09d61b0a1
season: 2
testable_claim: "Four conjuncts, all from the SL7.124 review (belam 09:22Z, wf_69d82bb2-c5c): (1) rotate_out_audit (sensei.py:1612) builds hand_paths WITH the session_id exactly as wake_audit threads it (:1192), so a session-keyed ack Read classifies the same in both audits -- the one-wrapper invariant at :976-985 holds; (2) _record_matches_session (:607) matches session_id at the record TOP level as well as under handover.join, mirroring rotate.py _record_join (:6365-6377), so a first-seating record resolves -- today 6 of 8 live session-keyed posts get the named refusal; (3) _is_byhand_read (:780) classifies a cat of seats/<seat>.ack.<sid8>.json as (b) on a path without the sessions segment, not only \\.ack\\.json; (4) P1 (only another session record on disk -> named refusal) and P3 (a prime row carrying a session_id stays on the latest/--gen arm) are COMMITTED tests in test_sensei_wake_audit.py, replacing the ephemeral /tmp/probe_sl7124_parent.py."
thought_session: dissolve-legacy-2026-09-19
title: L4 sensei audits agree on session keyed acks and top level session records
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sensei-audits-agree-on-session-keyed-acks-and-top-level-session-records

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue of SL7.124 (accepted with residue by the Prime, reviewer + refuter agreeing): the session-keyed resolution landed in wake_audit but not in rotate_out_audit; the record matcher reads one of the two places rotate.py writes the session id; the by-hand classifier spells only the legacy ack name; two probes that proved P1/P3 lived in /tmp. One node, four conjuncts, one kid. Dispatch gated on a fresh credit read: $11.89 of $182 at 09:10Z, floor $5.00.
<!-- THOUGHT:END -->
