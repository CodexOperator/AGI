---
id: hypothesis:context-suite-guards-cost-no-seconds-and-leak-no-standin
mint_id: cbcc64f6a8a14887842e13e5913cd893
type: hypothesis
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
edited_by: director-engine
scaffold_hash: 5aaa02694de4c11e
season: 2
testable_claim: with the conftest suite guards the standins test is not newly red and the hook-trim fixture runs in about a second, not 134 s
title: "The context suite guards cost no seconds and leak no standin (EG.8, TMM.312, assigned: director-engine)"
town: core
---
# hypothesis:context-suite-guards-cost-no-seconds-and-leak-no-standin

## ROUND EG.8 (thought-master TMM.312 00:42Z 09-28: fix rounds, front of queue)
Measured   after the landing d0d126deb the context conftest suite guards (.agi/context/conftest.py, last changed 3b18defba/31d2df851 under the parent hypothesis) regress DT's context suite: +1 red test_model_load_guard::test_standins_never_leak_into_a_later_module, and test_hook_trim_fixture_a00-faa1fb92 goes 0.9 s -> 134 s, so the whole .agi/context run overran 300 s under the osc pythonpath.
CLAIM      with the guards in place the context suite is back to its pre-landing reds and timing: the standins test is not newly red and the hook-trim fixture runs in the order of a second.
Dispatch line  config-max: any guard knob (timeouts, which paths it wraps) is a cell, never a literal · template-max: none · code: the guard's cost / leak, measured first
FIRST ACT  MEASURE before any code: time each guard against both named tests with and without the conftest guard (paste the numbers); name the guard that costs the 133 s and the one that leaks the standin.
FALSIFIERS either named test still regresses against the pre-landing base · a guard is simply removed instead of fixed (the parent hypothesis's claim must still hold)
TESTS      the two named tests + test_declared_suite_guards.py + test_bin_help_smoke.py (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); NEVER run the whole .agi/context tree (row 22: test_standins_never_leak_into_a_later_module can OOM its runner -- run it ALONE under a memory cap)
FILE SCOPE .agi/context/conftest.py · extensions/agi/bin/suite_guards.py · extensions/agi/tests/test_declared_suite_guards.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 20 production lines net · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit
