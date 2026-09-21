---
id: hypothesis:l4-paid-stream-tests-need-an-explicit-opt-in
mint_id: 18208dace4414e65831e838874da7e2d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-keyless-env-skips-not-fails
next_edges: []
edited_by: sanctuary-master
scaffold_hash: ed9b8d8cd8e51103
season: 2
status: deprecated
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-26: a keyed suite run makes ~36 UNMARKED paid OpenRouter calls (test_stream_master_blind_measure_v2.py:223, test_stream_master_semantic_screen.py:98) because the tests gate on key PRESENCE; and the real-judge benign/control tests PASS on judge outage (src/stream_master/semantic_screen.py:185 fails open). CLAIM: every paid test carries a `paid` marker and runs only under an explicit opt-in env (`AGI_PAID_TESTS=1`), skipping with a named reason otherwise even when a key is present; the real-judge benign/control tests FAIL (or skip with `judge unavailable`) when the judge is unreachable — never pass; a keyed default run makes ZERO outbound calls (asserted with the HTTP seam recorded). TESTS: keyed env without opt-in -> all paid tests skipped, 0 calls; opt-in -> they run; judge outage fixture -> control tests not green. FALSIFIER: one paid call from a default keyed run. CEILING: 2 kids (markers+gate / outage semantics). FILE SCOPE: extensions/agi/tests/test_stream_master_*.py + extensions/agi/src/stream_master/semantic_screen.py (:185 region only). LANE: sanctuary-helper (streaming town). EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: stream tests make paid OpenRouter calls only under an explicit opt-in env, never on key presence; real-judge control tests do not pass on judge outage
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-paid-stream-tests-need-an-explicit-opt-in

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-26: a keyed suite run makes ~36 UNMARKED paid OpenRouter calls (test_stream_master_blind_measure_v2.py:223, test_stream_master_semantic_screen.py:98) because the tests gate on key PRESENCE; and the real-judge benign/control tests PASS on judge outage (src/stream_master/semantic_screen.py:185 fails open). CLAIM: every paid test carries a `paid` marker and runs only under an explicit opt-in env (`AGI_PAID_TESTS=1`), skipping with a named reason otherwise even when a key is present; the real-judge benign/control tests FAIL (or skip with `judge unavailable`) when the judge is unreachable — never pass; a keyed default run makes ZERO outbound calls (asserted with the HTTP seam recorded). TESTS: keyed env without opt-in -> all paid tests skipped, 0 calls; opt-in -> they run; judge outage fixture -> control tests not green. FALSIFIER: one paid call from a default keyed run. CEILING: 2 kids (markers+gate / outage semantics). FILE SCOPE: extensions/agi/tests/test_stream_master_*.py + extensions/agi/src/stream_master/semantic_screen.py (:185 region only). LANE: sanctuary-helper (streaming town). EXCLUDED: everything else.

L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): RETIRE decided -- Falsifier closed under a different flag name: real_judge_skip() (conftest.py:509-521) requires AGI_REAL_JUDGE=1 AND a key, both real-judge classes skipif through it (semantic_screen.py test :102-105, blind_measure_v2 test :227-230), and autouse _no_openrouter (conftest.py:546-599) delenvs both OPENROUTER keys + stubs _openrouter_get on both aliases unless import-time snapshot _REAL_JUDGE_ON (:505); MEASURED grep AGI_PAID_TESTS extensions/ = 0, grep "ModelJudge()" = only the two gated classes + the explicit fail-open unit test (:204). Residual nit only under opt-in: benign test (:123-126) green on outage via semantic_screen.py:167-168/:183-187 judge-busy -> screened_relay :221-224 relay, whil EVIDENCE: f241acd52, 5f44e165b (reader wrote 5f44e165b -- typo, does not resolve), b99ede664; all three ancestors of HEAD 27c87b918 The status flip + move to deprecated/ is HELD by name: verification.py's never-lower node-count gate keys on ACTIVE and has no path for a deliberate retirement (a hand-lowered baseline would be a disarmed guard); it moves when hypothesis:l4-the-never-lower-gate-names-a-deliberate-retirement lands.

Retired at the L4 closeout (Prime retire list 2026-09-17 12:0xZ from survey hypothesis:a00-e1933e6a-176c0e, executed by sanctuary-master gen 7, status deprecated + moved under deprecated/hypothesis, mint id unchanged): falsifier closed by real_judge_skip + no_openrouter.
