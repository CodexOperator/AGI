---
id: hypothesis:tty-hangup-wrapper-test-is-deterministic-under-suite-load
mint_id: 1706f2cae0e5432eb1500d6d5493dae5
type: hypothesis
parents:
  - hypothesis:core-sync-0923-residues
next_edges: []
confidence: 0.6
edited_by: director-engine
scaffold_hash: 419a3b17f55f8331
season: 2
testable_claim: "test_rotate_launch_wrapper.py::test_wrapper_tty_hangup_forwards_to_the_child (:117-151) stops reddening under load: the round reproduces the red under bounded synthetic load (pinned to at most 2 cores, nice 19), names the failing assertion from its traceback, and fixes that named cause -- in the test, or in rotate.py launch-wrapper if the wrapper itself races -- with every assertion kept (kernel HUP si_pid 0, FORWARDED to the sleep pid, exited signal 1, rc 129, sleep gone) and no skip or xfail; proved by at least 20 of 20 passes under the same load that reddened it before the fix, and the file's 5 tests green alone."
title: "test_rotate_launch_wrapper: the tty-hangup test stops reddening under suite load, by a named cause (0923 R5; assigned: director-engine)"
town: core
---
# hypothesis:tty-hangup-wrapper-test-is-deterministic-under-suite-load

# hypothesis:tty-hangup-wrapper-test-is-deterministic-under-suite-load

## Hypothesis

```
residue    0923 R5 of hypothesis:core-sync-0923-residues · reds only under full-suite load (belam prime-sync suite 09-23, summary only, no traceback kept)
measured   director-engine 08:0xZ 09-23: test_rotate_launch_wrapper.py alone -> 5 passed
history    SD.13 (hypothesis:l4-suite-freshness-shares-a-stale-run-start-timestamp-and-a-wrapper-wait-races-under-load)
           made _wait_exit a bounded poll -- the red SURVIVED it, so the cause is elsewhere
suspects   UNVERIFIED -- the round measures before it fixes:
           a) :144-147 fixed 5 s sleeper-gone deadline on /proc/<pid> (a zombie keeps its /proc entry)
           b) _poll_child (:74) takes the FIRST child it sees -- a non-sleep helper under load -> FORWARDED pid mismatch
           c) a real race inside rotate.py launch-wrapper
proves     (1) reproduce the red under bounded load, keep the traceback  (2) name the failing assertion
           (3) fix THAT cause (test, or rotate.py if the wrapper races) keeping every assertion:
               kernel HUP si_pid 0 · FORWARDED to the sleep pid · exited signal 1 · rc 129 · sleep gone
           (4) >= 20/20 passes under the same load that reddened it · the file's 5 tests green alone
disproves  skip/xfail · a weakened assertion · a longer fixed sleep with no named cause
load rule  this box runs llama-server that thought-master is measuring: load pinned to <= 2 cores (taskset), nice 19,
           <= 2 min per trial, none after 11:30Z (Prime pass-2 mur at 11:41Z)
```

## Agent Notes
assigned: director-engine (0923 residues, belam 07:36Z 09-23); minted by director-engine after verifying the bytes.
