---
id: hypothesis:l4-the-runner-identity-pop-is-pinned-by-a-test-and-the-detect-sender-docstring-states-the-built-order
mint_id: 1018fec0bf5847b7af03f6ec18eef1db
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 00bc6339501d9b58
season: 2
testable_claim: "goal:g15 FIX-ONLY node, mur-SL2.16 (Prime XV 08:06Z, by name) line (6) — the conftest runner-identity pop (680f07be2, landed SL2#16). Cite lines at 2451606d0; re-measure on your base. MEASURED: (i) `extensions/agi/tests/conftest.py` `pytest_cmdline_main` now pops `AGI_AGENT_ID`, `AGI_SEAT`, `AGI_POST` beside the GIT_* pops — measured 81/274 red in test_send.py from a rotate-self-spawned seat window and 75/274 from a dispatched kid before it — but NO committed test pins the pop: a future edit that drops one name re-opens the red silently; (ii) send.py `_detect_sender` docstring (738, 742-743) says an explicit `--from` \"beats both fallbacks\" while the code (and the DESIGN — identity is SUPPLIED by the harness env, never CLAIMED by a flag; hypothesis:l4-authority-verified-against-the-graph-not-the-message) puts `--from` LAST: the docstring is wrong, the code is right. CLAIM: (a) `test_conftest_guard.py` gains a test that runs a pytest subprocess (the same pattern the file already uses for the tier gate) with `AGI_SEAT=x AGI_POST=y AGI_AGENT_ID=z` exported and a one-test file asserting all three are ABSENT from `os.environ` at test time — proving the pop end-to-end, and a second case asserting `monkeypatch.setenv` inside a test still works after the pop (a test may set what it needs); (b) the `_detect_sender` docstring is rewritten to state the ORDER as built and WHY (env-supplied identity beats the flag by design; `--from` is the fallback for a hand-run shell with no exported identity; `unknown` last), with the two hypothesis ids; (c) no behaviour change to `_detect_sender`; every send test byte-identical in assertion. FALSIFIERS: the pop can be removed with the suite still green; the docstring still claims `--from` beats the env; any send test assertion changes. TESTS: test_conftest_guard.py test_send.py test_tier_gate.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase; the pop list is the three names, no more (AGI_TIER stays — the tier gate reads it). FILE SCOPE: tests/test_conftest_guard.py, send.py `_detect_sender` docstring only. EXCLUDED: conftest.py logic (the pop itself is landed), rotate.py, every send.py function body. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: "the conftest runner-identity pop (AGI_AGENT_ID/AGI_SEAT/AGI_POST) is pinned by an end-to-end test and send._detect_sender's docstring states the order as built: env-supplied identity beats --from by design"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-runner-identity-pop-is-pinned-by-a-test-and-the-detect-sender-docstring-states-the-built-order

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
