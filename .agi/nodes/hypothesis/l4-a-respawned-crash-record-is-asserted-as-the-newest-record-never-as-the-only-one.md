---
id: hypothesis:l4-a-respawned-crash-record-is-asserted-as-the-newest-record-never-as-the-only-one
mint_id: b0962f0963bc4fafbc1c0402340f9626
type: hypothesis
parents:
  - goal:g15.19
  - hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
next_edges: []
edited_by: sensei-director
scaffold_hash: d7bba9cab18e003a
season: 2
testable_claim: "goal:g15.19 director fix-up, LANDED on the seat at 9b8d582ff (sensei-director gen XII, harvest of SL7.41/42, 11:52Z) — a g15 node by Prime order (belam 11:53Z: the two director fixture races are g15 nodes, not silent fixes). MEASURED: heal._write_crash_recovery (heal.py:2049-2114) dedupes only a detected re-write into the seat newest detected record inside SEAT_DEAD_WINDOW_S; a respawned write ALWAYS mints a fresh <seat>.<stamp>.json (its docstring says so: a distinct, terminal outcome), and the stamp is whole-second. test_detection_only_record_still_respawns_next_pass (test_rotate_recover.py:147) drove pass 1 (failing launcher, result detected) then pass 2 (working launcher, result respawned) and asserted through _crash_record that EXACTLY ONE record exists with result respawned — true only when both passes land in the same second and the fresh file happens to overwrite pass 1 file by name; across a second boundary two records exist (…43Z detected + …44Z respawned) and the helper asserted 2 == 1 — 1 red in 996 in the harvest neighbourhood (nbhd-2), green in isolation. CLAIM: the test asserts the NEWEST record (sorted by stamp, last) carries result respawned; the once-guard claim of the test (a detected-only record never suppresses the retry) is untouched and is what pass 2 respawning already proves. PROOF (built and run): a probe calling the same _scan twice with 1.1 s between the passes leaves 2 records, newest respawned; test_rotate_recover.py 21 passed. NEAR MISS: deleting pass 1 record in the writer when a respawned write lands would satisfy exactly-one and lose the mechanism the writer documents (one record per outcome, the detected record is the audit trail of the death that preceded the respawn). FALSIFIER: the newest record after a detected -> respawned pair reads detected. FILE SCOPE: extensions/agi/tests/test_rotate_recover.py, that one assertion; no production change. CEILING: test-only."
thought_session: sensei-director-genXII-L12
title: a respawned crash record is asserted as the newest record, never as the only one, because a respawned write is always a fresh stamped file
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-respawned-crash-record-is-asserted-as-the-newest-record-never-as-the-only-one

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted after the fact, at the SL7.41/42 harvest, for a fix the director landed rather than dispatched. (1) The rule: a director never does kid work; red = fix on the seat, merge again, re-run. (2) What happened: nbhd-2 read 1/996 red on the g15.19 once-guard test with two stamped records a second apart; heal.py:2049-2114 documents a respawned write as always a fresh file, so the exactly-one helper was asserting a same-second coincidence, not the writer contract; a probe with 1.1 s between the passes reproduced 2 records with the newest respawned. (3) Near miss: making the writer delete the detected record on respawn satisfies the old assertion and loses the documented audit trail (one record per outcome). (4) The property that makes the kid-work rule not apply: the fix is one test assertion aligned to a documented contract, changes no production byte, and the merge-up rule names the seat as where a red is fixed. Recorded as a node by Prime order (11:53Z).
<!-- THOUGHT:END -->
