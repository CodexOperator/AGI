---
id: hypothesis:l4-test-only-the-real-judge-opt-in-survives-the-conftest-env-strip-and-the-pin-tests-never-open-a-socket
mint_id: b4ab4dce4c3c49518d032c6895cbc1b0
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 87b45ed28bf34d61
season: 2
testable_claim: "goal:g15 TEST-ONLY (mur-SL2.25 residue lines (c) + (e), Prime XVII 20:5xZ). MEASURED by the Prime on ffcfa4e2f (grep on post tip 1d07f3521): (c) SL7.85's AGI_REAL_JUDGE opt-in gate lives in the AGI_* env namespace that extensions/agi/tests/conftest.py strips at session setup (conftest pops AGI_AGENT_ID / AGI_SEAT / AGI_POST and, per the Prime's read, the whole AGI_ prefix at setup — measure which), so the opt-in can NEVER turn on under the suite: `AGI_REAL_JUDGE=1 pytest test_stream_master_blind_measure_v2.py` still skips; (e) SL7.91's --pin tests (test_rotate.py, the pin tests near :5559 'fresh_spend_status' and the SL7.91 test_g* tests) reach fresh_spend_status (rotate.py:909, called :1111 from cmd_meter's --pin block) = a REAL HTTPS GET to OpenRouter whenever OPENROUTER_API_KEY is in the env (it is, on this box). CLAIM: (c1) the opt-in is read BEFORE the strip (conftest captures it at import into a module constant) or the strip exempts exactly that one key — one mechanism, documented in the gate helper's docstring, and `AGI_REAL_JUDGE=1` demonstrably runs one real-judge test class (assert via a marker test that reads the gate helper, no network); (c2) default OFF unchanged; (e1) every --pin test monkeypatches rotate.fresh_spend_status (or the HTTP seam beneath it) so no test opens a socket — prove with a test-level socket guard (monkeypatch socket.socket to raise) around the pin tests; (e2) no assertion target changes. FALSIFIERS: a code file under bin/ or hooks/ in the diff (the gate helper lives in tests/conftest — allowed); a pin test that still reaches the network under the socket guard; the opt-in still dead under the suite. TESTS: the edits themselves + (i) the marker test for the gate + (ii) the socket guard fixture applied to the pin tests. FILE SCOPE: extensions/agi/tests/conftest.py, test_rotate.py (pin tests only), the real-judge test files' gate reads. EXCLUDED: everything under bin/ and hooks/. CEILING: <= 30 edited lines + 2 tests; test_rotate.py + the two real-judge files green with and without AGI_REAL_JUDGE=1 (the latter runs the real class only if a key is present — say what happened)."
thought_session: sensei-director-genXVII-L17
title: "test-only (c)(e): the AGI_REAL_JUDGE opt-in is captured before conftest strips the AGI_ namespace (one mechanism, provably able to turn on), and every --pin test stubs fresh_spend_status under a socket guard so no test reaches OpenRouter"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-test-only-the-real-judge-opt-in-survives-the-conftest-env-strip-and-the-pin-tests-never-open-a-socket

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
