---
id: hypothesis:l4-the-kept-merge-test-has-no-vacuous-assert-and-the-docstring-is-true
mint_id: bf58f23152364a02bd031ea1a2e546e2
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9d27b73c0d33b041
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-31: test_verification_kept_merge.py:142-146 has a vacuous `assert True`; verification.py:221's docstring says an uncommitted MAIN read is 'not kept' while the mechanism checks HEAD ancestry against origin only; the merge-up procedure line `--level quick --stamp` was a silent no-op (quick has no smoke/node-count — measured by the point 07:49Z, corrected to `--level rotation --stamp` in the seat scratchpad; the prime's brief says `verification.py --stamp` after the push). CLAIM: (1) the vacuous assert is replaced by the real assertion of that test's stated intent (or the test is removed with the reason in the node); (2) the docstring and the mechanism agree — either the docstring states 'kept = on the integration branch AND HEAD reachable from origin' or the check also refuses a dirty tree (state which, with the reason); (3) `--stamp` without `--level` stamps (the stamp step does not depend on which level ran) and prints one line naming what it stamped. TESTS: the fixed test; a `--stamp` run at level quick stamps in a fixture; the docstring test if any. FALSIFIER: `assert True` still present, or `--level quick --stamp` still stamping nothing. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/verification.py + extensions/agi/tests/test_verification_kept_merge.py + test_verification.py. EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: test_verification_kept_merge.py carries no vacuous assert and verification.py's kept-merge docstring states exactly what the check does
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kept-merge-test-has-no-vacuous-assert-and-the-docstring-is-true

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-31: test_verification_kept_merge.py:142-146 has a vacuous `assert True`; verification.py:221's docstring says an uncommitted MAIN read is 'not kept' while the mechanism checks HEAD ancestry against origin only; the merge-up procedure line `--level quick --stamp` was a silent no-op (quick has no smoke/node-count — measured by the point 07:49Z, corrected to `--level rotation --stamp` in the seat scratchpad; the prime's brief says `verification.py --stamp` after the push). CLAIM: (1) the vacuous assert is replaced by the real assertion of that test's stated intent (or the test is removed with the reason in the node); (2) the docstring and the mechanism agree — either the docstring states 'kept = on the integration branch AND HEAD reachable from origin' or the check also refuses a dirty tree (state which, with the reason); (3) `--stamp` without `--level` stamps (the stamp step does not depend on which level ran) and prints one line naming what it stamped. TESTS: the fixed test; a `--stamp` run at level quick stamps in a fixture; the docstring test if any. FALSIFIER: `assert True` still present, or `--level quick --stamp` still stamping nothing. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/verification.py + extensions/agi/tests/test_verification_kept_merge.py + test_verification.py. EXCLUDED: everything else.
