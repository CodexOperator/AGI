---
id: hypothesis:l4-the-service-after-join-dm-is-sent-by-a-declared-signed-sender-never-from-unknown
mint_id: f6fbf76bf8704b26b4d4e858ce455614
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 9f934b43b6e2b63f
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 16:10Z line (3): the after_join dm arrives UNSIGNED, `from: unknown`, under enforcing comms.verify — delivered, flagged, not refused: FLIP proof (b)/(c) measured live; cite at seat tip 1dc9f96b2, re-measure on your base). MEASURED: `run_after_join`'s default `send_dm` closure calls `_send.send(root, to, text, None)` (rotate.py:9643-9645) — sender None → send.py's sender detection falls to 'unknown' (send.py:863-872, 'an honest absence, not a confident wrong name') and `_sign_line` (send.py:231-237) signs only when `<sessions>/seats/<from_id>.key` exists, so the service dm can never be signed; heal.py's own alarms pass the sender `\"heal\"` (heal.py:1869) and its holder/dispatcher sends name a seat (heal.py:1661, :2317). CLAIM: (a) the service's after_join dm names a declared sender resolved by ONE helper: the custodian seat when the performer runs inside a seat's own process (rotate-self's tail = the OUTGOING seat, whose key exists — SL7.72's tail path passes it through), else the system sender `heal` (the watch/reaper), and the dm is SIGNED when that sender has a key under `<sessions>/seats/` (mint `heal.key` the way `send.py keygen` mints a seat key, or read the custodian's — name which, and whether comms.verify's enforcing mode treats `heal` as a declared system sender; if the verify path must admit the name that is ONE measured, tested line in send.py, not a policy change); (b) `from: unknown` never appears on a service dm — a run that cannot resolve a sender records `dm_sender: unresolved` on the record's after_join key and still sends, named; (c) `_run_pending_after_joins` and the tail reach the same sender resolution (one function, no parallel driver); (d) the record's after_join key carries `dm_sender` and `dm_signed: true|false`. FALSIFIERS: the delivered dm still reads `from: unknown`; the dm is signed with a key whose pubkey is on no pushed row (a forged custodian); the sender differs between the watch and the tail; a signed dm fails `send.py whois`/verify. TESTS: test_after_join_service.py — the default send_dm passes a named sender; signed when its key exists, unsigned-but-named when not; the record names sender + signed; test_send.py — the system sender verifies (if send.py changes). FILE SCOPE: extensions/agi/bin/rotate.py — the `send_dm` default in `run_after_join` (:9643-9645) and one sender-resolution helper; extensions/agi/bin/send.py only if the verify path must admit the system sender; the two test files. EXCLUDED: `_compose_after_join_dm` and the gen/ref resolution (the gen/ref sibling); `_run_after_join_command` (the empty-slot sibling); the catch-up gate (the dead-seat sibling); the tail's liveness check (SL7.72 in flight); keygen for seats. CEILING: one sender helper, one default-closure edit, at most one send.py line, four tests."
thought_session: sensei-director-genXIV-L14
title: "the service's after_join dm is sent by a declared sender that signs — the custodian seat when the performer runs inside a seat's own process, else heal — never from: unknown UNSIGNED under enforcing comms.verify"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-service-after-join-dm-is-sent-by-a-declared-signed-sender-never-from-unknown

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
