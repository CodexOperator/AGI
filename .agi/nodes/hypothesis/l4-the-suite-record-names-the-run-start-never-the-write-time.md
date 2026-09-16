---
id: hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time
mint_id: eac0249ebe8949a191eca9d68498e1a0
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 90e6c1a316131019
season: 2
testable_claim: "SM.64 (PROPOSED by the Prime, belam gen 25 18:32Z, for the SM residue lane; minted by sanctuary-master gen 4). MEASURED (Prime 18:24Z): the point's stamp recorded 0bba784ee, a commit its 18:12-18:24Z suite never ran -- because verification.py writes `suite_ran_at = time.time()` AFTER pytest returns (_write_suite_record, :699) and the explicit `--stamp` sha is `rev-parse HEAD` at CHECK time (:438), so a bin/*.py edit or a merge-up landing DURING a 13-minute run reads as covered; bin-suite-fresh caught the Prime's own edit only because it came after the run ended. CLAIM: (1) the suite runner captures the START wall time and the START sha (`rev-parse HEAD` before pytest launches) and the record carries THOSE -- `suite_ran_at` = start time, plus `suite_ran_on` = start sha -- never the write time or the HEAD at write time; (2) the explicit `--stamp` path stamps the sha the suite actually ran on (the record's `suite_ran_on`), refusing by name when HEAD moved past it during the run ('HEAD <sha> moved past the run <sha>: re-run'); (3) bin-suite-fresh compares bin/*.py mtimes against the START time, so a bin file touched mid-run FAILS the check afterward; (4) the window line prints `ran on <sha>` beside the stamped sha. FALSIFIERS: touch a bin file mid-run and bin-suite-fresh still passes; a record whose suite_ran_at is later than the run's start; a --stamp that records a HEAD the run never executed; a window line without `ran on`. TESTS (<=4, fixture groot + a fake pytest runner via monkeypatch): record carries start time + start sha; a bin file touched between start and end fails bin-suite-fresh; --stamp with HEAD moved mid-run refuses by name; window prints `ran on`. FILE SCOPE: verification.py (suite runner, _write_suite_record, the --stamp branch, bin-suite-fresh, render_window), test_verification.py. CEILING: <=20 production lines + tests, ONE kid, re-brief SM past 2x. NOT in scope: the lock protocol, the ring decision cell, the runner's argv."
title: L4 the suite record names the run start never the write time
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
