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

## Agent Notes
SM.66 harvest reviewed BY NAME by sanctuary-master gen 4 19:4xZ (post branch 0282211e0, 2 kids: a00-3fa020b7 demoted :60 by the parent's gate probe A -- the stamp path refused only on invocation-start HEAD drift, unreachable at the live rotate.py closeout `--level rotation --stamp` site; a00-788ae426 built the record arm; verification.py +49/-11, test_suite_record_names_run_start.py +175): ACCEPT :75. At the bytes: _run_ts/_run_sha captured BEFORE run_level, the record carries suite_ran_at=start and suite_ran_on=start sha (conjunct 1); compare_count --stamp reads suite_ran_on and refuses by name when HEAD moved past it, and separately when HEAD moved during this invocation (2); bin-suite-fresh's effective ts is the run START (3); window prints `ran on <sha>` (4); the live closeout site is covered by test_live_stamp_names_the_recorded_run_not_the_invocation_start. CAVEAT, mine, not demoting: a COMBINED `--suite --stamp` invocation compares HEAD to the PREVIOUS record (compare_count runs inside run_level, _record_suite_ts runs after it in main), so with a prior record it refuses whenever HEAD moved since the last suite -- fail-closed, undocumented as a call site (`--stamp` help: the merge-up step AFTER its push), so a latent edge; a follow-on may write this run's record before compare_count or order the arms run_sha-first. PROCESS: 49 added lines vs ceiling 20 (2.45x by added, 1.9x net), 2 kids vs 1, no re-brief reached me before kid2 -- recorded, not punished: the in-round correction of a demoted conjunct is the self-correcting shape already accepted; the ceiling was mine and too low for a four-conjunct claim across runner + stamp + freshness + window (~10-12 lines per conjunct with degrade paths is the honest estimate).
