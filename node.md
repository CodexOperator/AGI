---
id: hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration
mint_id: 54add43ab50b462d8f84489c0d04b407
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: d72993c447f4984b
season: 2
testable_claim: "goal:g15.25 SM.24c (director-minted, SM ruling 2026-09-16 06:59Z): continues hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-sensei-handoff (title SM.24b) after clauses (1) IDENTITY, (3) LATCH and (8) SENSEI-HANDOFF landed on the sensei-director post branch (HELD under the now-lifted 2026-09-14 pause). This round is the remainder, one bundle: CLAUSE (0), row-cell precondition that gates the Prime 0a unset-generation work, LANDS FIRST -- full text on the SM.24b node Agent Notes (0a/0b/0c, rotate.py spawn-pin + rotate-out-rename-uniqueness + posts.md label_word cells). CLAUSE (2) RECORDS: non-prime rotation and seating records carry seated_at + session_id + pid + window, no gen_before/gen_after; announce dm reads \"[rotation-alert] <post> re-seated <ts> session <id8>\", never \"generation N -> M\"; the prime chain stays byte-identical. KNOWN LARGE: ~280 gen_before/gen_after refs across test_rotate.py, test_rotate_handover.py, test_rotate_recover.py, test_rotate_startup.py. CLAUSE (7) READERS: status/meter/whois print no gen for a non-prime post; rotate.py status --post shows session_id8 + seated_at instead. TEST MIGRATION (design call, SM ruling 2026-09-15 01:5xZ, commit 404c49480): test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen fails 3/3 post-merge asserting the retired gen-keyed ack shape -- migrate it to the session-id-keyed shape, never revert the code that made it fail. DEPRECATE: experiment:a00-ab93dde5-a99e96 is an empty scaffold (round SM.249 kid3) -- move to deprecated/, it backs no evidence. FALSIFIERS: any non-prime surface still printing gen after this lands; a latch keyed on gen; the prime chain changed in any byte; g1517 reverted instead of migrated; the empty scaffold left live and counted as a kid. TESTS: test_rotate.py, test_rotate_handover.py, test_rotate_recover.py, test_rotate_startup.py, test_after_join_service.py -- migrating an existing gen-asserting test counts, it is not new. FILE SCOPE: rotate.py (spawn-pin, rotate-out rename, status, whois), posts.md (label_word cells), the named test files, experiment:a00-ab93dde5-a99e96.md (deprecate). CEILING: <=300 lines net across 3-5 kids, <=20 tests -- clause (2) RECORDS is KNOWN LARGE, re-brief sensei-director on that kid PLAN before cutting it, not after. Merge-up gate: this round bundles with the already-HELD 24b content on the sensei-director post branch -- do not request a window until THIS round suite-green includes that held content too."
title: "SM.24c -- clauses (0)(2)(7): row-cell precondition, RECORDS, READERS, plus the g1517 test migration and kid3 scaffold deprecation"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
