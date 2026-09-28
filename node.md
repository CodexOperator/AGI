---
id: hypothesis:authority-publish-plumbing-git-calls-are-bounded-and-never-raise
mint_id: 318d4312efb74ea3901c0ae3f346d98e
type: hypothesis
parents:
  - hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips
next_edges: []
edited_by: director-engine
scaffold_hash: ab795020735b7ad4
season: 2
testable_claim: With git hash-object stubbed to raise TimeoutExpired, _publish_row_to_authority returns an authority FAILED line naming the timeout, every _g call passes a timeout, and the retry defers.
title: "The authority commit's plumbing git calls are bounded and yield authority: FAILED, never raise (0-credit leaf 2/2 of g15.29.14 r3)"
town: core
---
# hypothesis:authority-publish-plumbing-git-calls-are-bounded-and-never-raise

## Measured
- rotate.py:10469-10471 -- `_g` runs subprocess.run with NO timeout and NO except; used at 10475 (rev-parse), 10476-10477
  (hash-object), 10479 (read-tree), 10480-10481 (update-index), 10482 (write-tree), 10485-10487 (commit-tree).
- they share the try at 10473, whose only clause is the finally (10506-10507); EF.93's inner try (10490-10501) guards only the push: any raise escapes, a hang never returns.
- `_git_toplevel` (16650-16652) also runs rev-parse, already guarded -- a stub keyed on "rev-parse" hits it first (false SKIPPED);
  key the stub on "hash-object" (on this path only at 10476).
## CLAIM
`_g` gets `kw.setdefault("timeout", 60)`; the try at 10473 gets `except subprocess.TimeoutExpired` + `except OSError` before the
`finally`, each setting `last` (`authority commit build for {branch} timed out after {exc.timeout}s` / `could not launch git for the
authority commit on {branch}: {exc}`) and `break`ing. No `except Exception`, no indexing into exc.cmd.
## Dispatch line
config-max: none / template-max: none / code: `_g` + the except clauses on the 10473 try, nothing wider
## FALSIFIERS
- the new test is green on the base (the sibling push-leg leaf's tip)
- a `_g` call reaches the stub without a timeout
- a neighbour test file red after the fix
## TESTS
test_rotate_key_authority.py::test_publish_plumbing_timeout_is_bounded_fails_and_defers_the_swap -- an inline fake: when
"hash-object" is in args, record `kw.get("timeout")` and raise `TimeoutExpired(args, kw.get("timeout") or 0)`, else the real run;
assert FAILED + "timed out", no SKIPPED, recorded timeouts non-empty and all truthy; then `_seed_authority_pending` +
`_assert_retry_defers`. Neighbours: test_rotate_pending_swap_authority.py.
## FILE SCOPE
extensions/agi/bin/rotate.py 10429-10538 (+ read 16644-16659)
extensions/agi/tests/test_rotate_key_authority.py 526-576 + the sibling leaf's tests 579-601
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn; TMM.89) · ~9 production lines · 0 USD · runs AFTER the push-leg leaf merges
RESIDUE (out of scope): tempfile.mkstemp (10465) and the finally's os.unlink (10507) can still raise OSError.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-checked against d19b619aed before dispatch (03:5xZ 09-24): the sibling push-leg leaf EF.93 merged (6e451872d5) and added 8 lines inside this function, so the citations below it moved +8 with content unchanged; its inner try (10490-10501) now guards ONLY the push, so _g's calls and the outer try still have no timeout or except -- this leaf's claim stands as written. Claim, tests and ceiling unchanged; the precondition is met.
<!-- THOUGHT:END -->
