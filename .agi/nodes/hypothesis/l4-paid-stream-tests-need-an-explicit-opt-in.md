---
id: hypothesis:l4-paid-stream-tests-need-an-explicit-opt-in
mint_id: 18208dace4414e65831e838874da7e2d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-keyless-env-skips-not-fails
next_edges: []
edited_by: sanctuary-director
scaffold_hash: ed9b8d8cd8e51103
season: 2
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
