---
id: hypothesis:l4-the-tier-gate-harness-has-no-dead-parameter
mint_id: 37efc2cae8c44606b487faa04356966a
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 04a96d26ecca287e
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-X) ruling merge-up 37 BY NAME (wf_7eb33b06-98e, refuter-confirmed), ACCEPTED there; minted by sanctuary-director 16:1xZ after re-measuring on the seat's bytes (tip past f02401d0d). On L4.228 (hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env): test_tier_gate.py:188-233 `_run_pytest_on_fake_main(..., git_redirect=None)` — the `git_redirect` parameter is DEAD (every caller passes `extra_env={'GIT_COMMON_DIR': ...}` instead; :227-233 strips host GIT_* then sets all three vars to the same path when given, which is exactly the GIT_DIR == GIT_COMMON_DIR shape the round proved CANCELS the redirect); and :650-656's message attributes the escape to 'without the pop the redirect must ESCAPE' where the assertion is on the mutated conftest — the refusal/escape wording is misattributed. Note for the node, not a fix: the round ran TWO kids over a CEILING of 1 (the parent demoted round 1 and cut round 2; recorded as a deviation on the hypothesis by the director). CLAIM: the dead parameter is removed (or made to set GIT_COMMON_DIR alone, the vector the round measured) and every call site reads as the mechanism it exercises; the assertion messages name what is asserted (mutated conftest escapes; fixed conftest refuses). FALSIFIER: a parameter no caller uses, or a message naming a different mechanism than the assertion. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_tier_gate.py only."
title: test_tier_gate's fake-main harness drops its dead git_redirect parameter and names the mechanism each assertion exercises
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-tier-gate-harness-has-no-dead-parameter

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
