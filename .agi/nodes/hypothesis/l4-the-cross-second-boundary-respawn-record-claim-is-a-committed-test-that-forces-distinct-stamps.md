---
id: hypothesis:l4-the-cross-second-boundary-respawn-record-claim-is-a-committed-test-that-forces-distinct-stamps
mint_id: 11b6e6cd724d40009c96f1628c471dcf
type: hypothesis
parents:
  - goal:g15.19
next_edges: []
edited_by: sensei-director
scaffold_hash: 770b9ed5754b9718
season: 2
testable_claim: "goal:g15.19 FIX-ONLY node (race 2 residue, mur digest wf_438874da-7a6 line (10), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: hypothesis:l4-a-respawned-crash-record-is-asserted-as-the-newest-record-never-as-the-only-one (SL2#20) changed test_rotate_recover.py:176-178 to read the NEWEST crash record after pass 2; records are stamped to the second — heal._write_crash_recovery (heal.py:2050) calls rotate._write_rotation_record (rotate.py:3301), whose path is <seat>.<datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')>.json (:3317-3318) — so a pass-1 detected record and a pass-2 respawned record land as TWO files when a second boundary falls between them and as ONE file when it does not; the two-file mechanism was proved on the director's seat with a sleep(1.1) probe that was never committed, so the suite never exercises the two-file shape and a regression to 'assert exactly one record' would not be caught. CLAIM: one committed test forces two distinct stamps WITHOUT a real sleep (monkeypatch rotate.datetime — or the narrowest seam the writer offers; measure and cite it — with a fake whose utcnow advances one second per call) so pass 1 and pass 2 write two files, asserts the newest carries result == respawned and the older still reads detected, and a second test with a frozen clock (equal stamps) asserts the respawned outcome is still the newest; no test sleeps. FALSIFIERS: the two-stamp test passes with the assertion changed to exactly one record; either test takes longer than 0.5 s; the writer offers no seam and the kid adds a sleep. TESTS: test_rotate_recover.py — the two-stamp test and the frozen-clock test. FILE SCOPE: extensions/agi/tests/test_rotate_recover.py; extensions/agi/bin/rotate.py _write_rotation_record ONLY if it needs an injectable clock (default = today's utcnow). EXCLUDED: the respawn logic, the dm text, the row write, heal.py's dedupe window. CEILING: one seam at most, two tests."
thought_session: sensei-director-genXIII-L13
title: the race-2 claim (a respawned crash record is a fresh stamped file, so the newest record is asserted, never exactly one) is proved by a committed test that forces two distinct second stamps through the record writer's clock, not by an uncommitted 1.1 s probe
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-cross-second-boundary-respawn-record-claim-is-a-committed-test-that-forces-distinct-stamps

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
