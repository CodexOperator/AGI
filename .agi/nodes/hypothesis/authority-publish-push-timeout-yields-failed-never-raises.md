---
id: hypothesis:authority-publish-push-timeout-yields-failed-never-raises
mint_id: c132c2904fc94ef1aeac7eacd09485b5
type: hypothesis
parents:
  - hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips
next_edges: []
edited_by: director-engine
scaffold_hash: c76522b592ef27d8
season: 2
testable_claim: With the push stubbed to raise TimeoutExpired or OSError, _publish_row_to_authority returns an authority FAILED line naming the push instead of raising, and the EF.84 retry refuses by name with the pending swap deferred and the key byte-identical.
title: "A hanging or unlaunchable authority push yields authority: FAILED and never raises (0-credit leaf 1/2 of g15.29.14 r3)"
town: core
---
# hypothesis:authority-publish-push-timeout-yields-failed-never-raises

## Measured
- rotate.py:10490-10493 -- the push carries timeout=60 but sits in the try at 10473 whose ONLY clause is `finally: os.unlink(idx)`
  (10498-10499): TimeoutExpired / OSError escape, against the docstring's "never raises" (10401).
- rotate.py:10436-10444 -- the fetch guard's shape: `last = f"fetch of authority branch {branch} timed out after {exc.timeout}s"` /
  `f"could not launch git fetch for {branch}: {exc}"`, then `break`; 10522 returns `authority: FAILED -- {last}`.
- the push runs only after a fetch with rc 0 (10445-10448), so the probe at 10508 is skipped and a push failure reaches 10522.
- rotate.py:17594 -- EF.84's retry calls the publish unguarded; cmd_rotate_self calls the retry at 19198.
- baseline (66e3dd68c7): test_rotate_key_authority.py 15 passed.
## CLAIM
The push call alone is wrapped in `except subprocess.TimeoutExpired` + `except OSError`; each sets `last`
(`push of authority branch {branch} timed out after {exc.timeout}s` / `could not launch git push for {branch}: {exc}`) and `break`s;
the finally still unlinks the index; the pending swap stays deferred.
## Dispatch line
config-max: none (60 s matches the literals at 10435 / 10493 / 10512) / template-max: none (the line shapes copy 10438-10443) /
code: the push call at rotate.py:10490-10496, nothing wider
## FALSIFIERS
- the new test is green on the base (66e3dd68c7 or the tip you branch from)
- test_rotate_key_authority.py or test_rotate_pending_swap_authority.py red after the fix
- an edit outside `_publish_row_to_authority` + the test file
## TESTS
test_rotate_key_authority.py::test_publish_push_timeout_fails_and_defers_the_swap -- give `_stub_git_run` (534-548) a `push=None`
kwarg (`if "push" in args and push is not None: return push(args)`); build `_fixture` (34), pass `push=_timeout` (530); assert the
line starts `authority: FAILED`, names "push" and "timed out", carries no SKIPPED; then `_seed_authority_pending` (551) +
`_assert_retry_defers` (567) -- that is the same call cmd_rotate_self makes at 19198, so the rotate-self site is pinned too.
Neighbours: test_rotate_pending_swap_authority.py (baseline 9 passed).
## FILE SCOPE
extensions/agi/bin/rotate.py 10399-10522 (+ read 17491-17497, 17565-17595)
extensions/agi/tests/test_rotate_key_authority.py 1-62, 517-617
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn; TMM.89) · ~9 production lines · 0 USD · runs BEFORE its sibling leaf (same try block)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.89 (owner 02:3xZ via TM: "No more special usd0 runs") retired the pi-local kid lane this CEILING was written for; the round now runs the STANDARD way on the free lane. Only the CEILING harness moved: claim, tests and file scope unchanged.
<!-- THOUGHT:END -->
