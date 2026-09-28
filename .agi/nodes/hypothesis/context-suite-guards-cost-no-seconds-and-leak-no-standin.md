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

## CORRECTIVE EG.13 -- re-runs EG.8 (kid a00-783f8ea0 + parent a00-4b4b4b90 each killed at its OWN scope cap, 01:04:56Z + 01:08:15Z; 0 commits, no harvest)
BASE      CUT FROM the post-branch tip 019fae9f7 (branch de-base-EG.13; EG.8's loop branch carries 0 commits). No merge. Never rebase.
Measured  (EG.8 parent probes, iter-EG.08/a00-4b4b4b90) test_hook_trim_fixture_a00-faa1fb92.py ALONE: 31 passed 3 xfailed in 0.35 s without the guards and 0.38 s WITH them -- the 134 s does NOT reproduce alone. test_standins_never_leak_into_a_later_module was run with no cap of its own (against this node's TESTS line): the kid's scope hit its memcg cap at 01:04:56Z, the parent's at 01:08:15Z (kernel: constraint=CONSTRAINT_MEMCG both times -- the scope caps held, the box was never at risk); the round died with 0 commits. A pytest inside a round has no cap of its own: only the round's scope cap stops it, and that kills the round.
HARD RULE test_standins_never_leak_into_a_later_module runs ONLY as: systemd-run --user --scope -q -p MemoryMax=2G -p MemorySwapMax=0 -- env -u TMUX -u TMUX_PANE timeout 600 python3 -m pytest <that one test> -q -p no:cacheprovider --basetemp=/tmp/<short> -- never bare, never with another module, never under the whole .agi/context tree. An OOM under the cap is a MEASUREMENT (paste it), not a reason to lift the cap. The same cap wraps every .agi/context pytest this round runs.
1. The 134 s: reproduce it at MODULE scope -- the fixture's own directory (.agi/context/local-maxxing/pi/) with and without the guards, under the cap above; paste both timings. Not reproduced there either -> the claim's 134 s is a whole-tree attribution artefact: say so on your node with both runs pasted, and the timing half of the CLAIM closes as not-reproduced (no code).
2. The standin leak: run the one test under the cap with and without .agi/context/conftest.py's guards (the parent hypothesis's guards, 3b18defba/31d2df851); paste both. Newly red WITH the guards -> name the guard and fix it inside FILE SCOPE; the parent hypothesis's claim must still hold.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     the two named tests (each under the cap above) + test_declared_suite_guards.py + test_bin_help_smoke.py (timeout 900, --basetemp under /tmp)
FILE SCOPE .agi/context/conftest.py · extensions/agi/bin/suite_guards.py · extensions/agi/tests/test_declared_suite_guards.py · the kid's own node
CEILING   HARD CAP: 1 kid · <= 20 production lines net · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE, CEILING and the HARD RULE verbatim into the kid brief; YOU run no .agi/context pytest outside the cap either; COMMIT every kid edit AND every node edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.13: EG.8-parent-oom EG.8-oom residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
