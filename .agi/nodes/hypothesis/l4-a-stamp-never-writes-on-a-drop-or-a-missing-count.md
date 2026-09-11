---
id: hypothesis:l4-a-stamp-never-writes-on-a-drop-or-a-missing-count
mint_id: 297a0e58ba0849b099bda66f75b8f37b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-stamp-forces-the-smoke-count
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 1dbd9600f1a9e535
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (small, tests-only; folded from the merge-up 32 ruling) test_verification_kept_merge.py:193 does not pin two edges of L4.174's stamp path. CLAIM (tests only, behaviour already believed present): (a) `--stamp` with a fresh count whose active is BELOW the recorded baseline -> node-count FAIL and the state file is byte-identical afterwards; (b) `--stamp` where the forced smoke round reports no number -> node-count SKIP and the state file untouched. If either test goes red, that is a defect in verification.py to fix in the same round (then FILE SCOPE widens to verification.py's compare_count only). FALSIFIER: a state file that changed under (a) or (b). CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_verification_kept_merge.py (+ verification.py compare_count only if red)."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: with --stamp, an active-count drop FAILS and writes nothing, and a smoke round that reported no number SKIPs and leaves the baseline untouched
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-stamp-never-writes-on-a-drop-or-a-missing-count

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (small, tests-only; folded from the merge-up 32 ruling) test_verification_kept_merge.py:193 does not pin two edges of L4.174's stamp path. CLAIM (tests only, behaviour already believed present): (a) `--stamp` with a fresh count whose active is BELOW the recorded baseline -> node-count FAIL and the state file is byte-identical afterwards; (b) `--stamp` where the forced smoke round reports no number -> node-count SKIP and the state file untouched. If either test goes red, that is a defect in verification.py to fix in the same round (then FILE SCOPE widens to verification.py's compare_count only). FALSIFIER: a state file that changed under (a) or (b). CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_verification_kept_merge.py (+ verification.py compare_count only if red).

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.190, 2026-09-11 12:07Z). Kept the kid's proved (0.9) and the parent's keep. Tests-only, as minted: verification.py is untouched and both edges already held -- compare_count returns SKIP before any _write_state when the smoke count is None (verification.py:264-266) and FAIL without a write when the fresh active is below the recorded baseline (:292-299); the two new tests drive run_level(stamp=True) end to end with a monkeypatched run_check and assert state_path.read_bytes() is identical afterwards (not a status-string-only assertion -- the parent's named near miss). Ran myself: `pytest test_verification_kept_merge.py test_verification.py -q` on the round bytes -> 50 passed. Residue: none.
