---
id: hypothesis:a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-grace
mint_id: 1f637e3f1f2b4d82aa01d7bc6b231b13
type: hypothesis
parents:
  - hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session
next_edges: []
edited_by: director-engine
scaffold_hash: daab7507787f175f
season: 2
testable_claim: _reap_chain kills a chain of N TERM-ignoring members within one config chain deadline (plus a small constant), never N x term_grace_s; its docstring matches the resolver defaults.
title: "a reap chain is bounded by one chain deadline, never N x the per-pid TERM grace (assigned: director-engine)"
town: core
---
# hypothesis:a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-grace

# hypothesis:a-reap-chain-is-bounded-by-one-chain-deadline-not-per-pid-grace

## Measured
- PASS 8 row (hypothesis:pass8-0926-residue-batch L47): `rotate.py` `_reap_chain` (~L11462-11530) gives EACH pid its own
  `wait_secs = reaper.term_grace_s` (default 15 s) after TERM, so a 3-member chain that ignores TERM waits up to 3 x
  15 s before the last SIGKILL -- there is no chain deadline.
- Its docstring says "default 15 s" and, two lines later, quotes "wait up to 5 s per pid" (L4.118/R2) -- contradictory.
- parent review a00-2fa1fab0-b7d2a0.md:166 records a config write that had not happened (row 47, third clause).

## CLAIM
`_reap_chain` is bounded by ONE chain deadline read from a config cell (`reaper.chain_deadline_s`, resolver default
stated once), shared by every member: a chain of N TERM-ignoring stand-ins is fully SIGKILLed within that deadline
(+ a small constant), never N x term_grace_s; the docstring states one number per knob and matches the code; the
experiment node a00-2fa1fab0-b7d2a0's config-write line is corrected in place with a THOUGHT.

## Falsifiers
1. Three stand-ins that ignore SIGTERM (`python3 -c 'import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)'`)
   with term_grace_s=2, chain_deadline_s=3 take > 4 s to all be gone -> disproved.
2. A member that exits on TERM still gets SIGKILL or is waited past its exit -> disproved.
3. The docstring's numbers disagree with the resolver defaults -> disproved.
4. test_rotate*.py tests touching _reap_chain regress -> disproved.
