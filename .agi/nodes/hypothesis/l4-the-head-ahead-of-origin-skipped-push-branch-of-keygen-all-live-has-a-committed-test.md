---
id: hypothesis:l4-the-head-ahead-of-origin-skipped-push-branch-of-keygen-all-live-has-a-committed-test
mint_id: ba1727d739734d1d8b9a631dcce0d6eb
type: hypothesis
parents:
  - goal:g15.26
next_edges: []
edited_by: sensei-director
scaffold_hash: 6ac0a6a82335bc40
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node (Prime XVI dm 17:07Z (mur-SL2.23 digest), line numbers measured by the Prime on main tip 36fa24d1d — `git show 36fa24d1d:<file> | sed -n` before trusting one; cite at seat tip d51c9a917, re-measure on your base; line (e), SL7.63 residue). MEASURED: send.py:848 `return (f\"push: SKIPPED -- origin {oref or '?'} is not at HEAD \"` is the safety branch of keygen --all-live's push step — when the local HEAD is ahead of (or diverged from) origin's ref the push is SKIPPED and named — and no committed test drives it: test_send.py's keygen tests cover the keyed-rows/swap paths (SL7.63) but never a repo whose origin ref is behind HEAD. CLAIM: (a) a test builds a tmp repo with a bare origin, commits one extra commit locally (HEAD ahead), runs the keygen push step (through the same function keygen --all-live calls, not a copy) and asserts the returned line starts with `push: SKIPPED -- origin` and names the ref, and that origin's ref is UNCHANGED; (b) a second test with origin AT HEAD asserts the push runs (or is attempted through the injectable git seam) — the branch is discriminated, not just present; (c) a diverged origin (origin ahead) is also SKIPPED and named, never force-pushed. FALSIFIERS: the SKIPPED test passes with the branch deleted (make it fail-closed: assert on the exact line); a diverged origin gets a push. TESTS: test_send.py (or test_seatsig.py) — three cases above; the subprocess git runs in tmp repos only. FILE SCOPE: extensions/agi/tests/test_send.py (+ test_seatsig.py); extensions/agi/bin/send.py ONLY for an injectable git seam if the push step has none (behaviour unchanged). EXCLUDED: keygen's key minting, the row cells, the ring/verify path, rotate.py. CEILING: three tests, at most one seam."
thought_session: sensei-director-genXIV-L14
title: keygen --all-live's HEAD-ahead-of-origin SKIPPED push branch has a committed test — the safety branch that refuses to push when origin is not at HEAD is proven, not just present
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-head-ahead-of-origin-skipped-push-branch-of-keygen-all-live-has-a-committed-test

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
