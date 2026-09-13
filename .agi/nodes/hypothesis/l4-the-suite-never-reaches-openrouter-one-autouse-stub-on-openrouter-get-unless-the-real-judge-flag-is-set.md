---
id: hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set
mint_id: 8e79fe8027814babb7bd51a2f5f3d0c2
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 48c3833596255605
season: 2
testable_claim: "goal:g15.25 SM.05 = SL7.106 re-cut (intake: belam XVIII 23:41Z queue A; mur-SL2.26). MEASURED on season2/main @ed00e0796: cmd_meter :944 -> fresh_spend_status :909 -> _openrouter_get :897 (urllib urlopen :903, timeout 5) for /key + /credits, keyed by _openrouter_key :880 = $OPENROUTER_API_KEY else the REPO .env; test_rotate.py has 29 `--pin` meter invocations and only two stub _openrouter_get (:5615, :5629) — every other one (the Prime named :1517 :1536 :1666 …) reaches the network whenever the developer env or .env carries a key (two real HTTP calls x 5 s timeout each on a dead key = up to 10 s per test, and real spend on a live one); conftest.py:488 real_judge_skip already declares the ONE opt-in flag AGI_REAL_JUDGE=1 + a key. CLAIM: (1) conftest.py gains ONE autouse fixture `_no_openrouter` that, unless os.environ.get(AGI_REAL_JUDGE) == \"1\", monkeypatches rotate._openrouter_get to `lambda url, key: None` AND delenv OPENROUTER_API_KEY (+ OPENROUTER_PROVISIONING_KEY) — imported lazily (the rotate module may not be importable in every test env: guard with try/except ImportError, skip the setattr, keep the delenv); (2) the two existing explicit stubs keep working (a test-level monkeypatch after the autouse one wins — say the pytest ordering fact in the docstring); (3) fresh_spend_status with the stub returns its no-key/None shape and cmd_meter --pin prints the same lines it prints today with no key — measure and assert one; (4) no engine code changes; (5) the conftest.py:480-500 doc block names the fixture as the second half of the same rule (fixture-only unless opt-in). FALSIFIERS: any urlopen reached during the suite (assert via a monkeypatched urllib.request.urlopen that raises in ONE probe test run over the 11 named tests); a test that needed the real key and now fails; the real-judge tests skipping differently than before. TESTS: 1 new test in test_rotate.py (urlopen raises -> meter --pin still exits as today), the 11 named tests unchanged and green with OPENROUTER_API_KEY exported to a junk value in the run. FILE SCOPE: conftest.py (one fixture + doc), test_rotate.py (one test). CEILING: <= 30 lines, <= 1 new test; test_rotate.py wall time before/after with a junk key exported — report both numbers in the kid node."
title: "the engine suite never reaches openrouter.ai: ONE autouse conftest stub on rotate._openrouter_get (+ the key env dropped) unless AGI_REAL_JUDGE=1 — the 11 meter --pin tests stop spending network on a developer box that has a key (mur-SL2.26 residue on SL7.106)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
