---
id: hypothesis:l4-real-judge-tests-run-only-under-one-explicit-opt-in-env-flag-default-off-a-key-alone-spends-nothing
mint_id: eccffdc6556c4d929de9bd7410341166
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 5bb420a5191fc511
season: 2
testable_claim: "goal:g15 FIX-ONLY (suite creep; Prime XVI RULING dm 17:51Z on the SL7.77 bank: 'OPT-IN flag, default OFF — the suite is fixture-only and spends nothing; a real-judge run only under an explicit env flag named in the test module docstring'; cite at post tip on season2/posts/sensei-director, re-measure on your base). MEASURED (SL7.77 kids experiment:a00-8f54f161-575f02 + a00-4d9f6b08-dc569e): two test classes make REAL OpenRouter ModelJudge HTTP POSTs per corpus body whenever OPENROUTER_API_KEY is merely present — extensions/agi/tests/test_stream_master_blind_measure_v2.py:220 _real_judge = ModelJudge(), :223-225 skipif(not _real_judge.available(), reason names the key), :226 class TestRealGeneralizationProbe (95.29 s + 9.26 s), and extensions/agi/tests/test_stream_master_semantic_screen.py:95 _real_judge = ModelJudge(), :98-100 the same skipif, :101 class TestRealSemanticMeasurement (43.64 s + 2.99 s; test_zero_novel_escapes is a live-model flake) — ~150 s of a 606-693 s suite (22%), paid silently by any keyed box; ModelJudge.available() is extensions/agi/src/stream_master/semantic_screen.py:163-164 (bool of the key) and the judge fails OPEN at :167-169 with no key. The SL7.77 verdict named this residue and did NOT add the gate because that brief forbade it; this line is the ruling. CLAIM: both real-judge classes are collected-and-SKIPPED unless ONE explicit opt-in env flag is set (AGI_REAL_JUDGE=1 — one name, shared by both files through one gate helper, e.g. a real_judge_enabled() beside ModelJudge or a tests-side helper both modules import — never two spellings), regardless of the key: flag unset + key present → skipped with a reason naming the flag; flag set + key absent → skipped with the existing key reason; flag set + key present → the real run exactly as today. Each module docstring (blind_measure_v2 :1-43, semantic_screen :1-31) names the flag and the one-line invocation (AGI_REAL_JUDGE=1 python3 -m pytest <file>). The default suite runs fixture-only and spends nothing on a keyed box. FALSIFIERS: a key alone still runs a real judge; the flag spelled differently in the two files; a docstring not naming the flag; the offline tests (HeuristicJudge plumbing, test_model_judge_fails_OPEN_when_no_api_key :190-217 with its keyless SKIP at :203 and delenv at :210) changed or newly skipped; ModelJudge.available()/judge() production semantics changed (the relay's fail-open at :167-169 must stay); the report_split hand helper (:277) broken. TESTS (≤4, in an existing file or tests/test_stream_master_real_judge_optin.py): the gate under monkeypatch — key+noflag → off, flag+nokey → off, both → on; both skipif conditions reference the gate (read the source or the mark's args); both docstrings contain the flag name; the keyed default-suite cost is proved by the gate, not by a live call. FILE SCOPE: the two test files, one shared gate helper (semantic_screen.py additive-only, or tests/conftest.py), the new test file. EXCLUDED: test_grid.py and rotate.py _read_ack seams (SL7.77 landed), relay.py, the corpus, any other suite-speed seam (rotate_selfreap is named irreducible). CEILING: ~20 lines of code + ≤4 tests; land in SL2#25/26."
thought_session: sensei-director-genXV-L15
title: real-judge test classes run only under ONE explicit opt-in env flag (AGI_REAL_JUDGE=1), default OFF and named in each module docstring — a present OPENROUTER_API_KEY alone spends nothing; the default suite is fixture-only
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-real-judge-tests-run-only-under-one-explicit-opt-in-env-flag-default-off-a-key-alone-spends-nothing

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
