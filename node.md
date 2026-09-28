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


## CORRECTIVE EG.21 -- closes mur-eg-6 EG.13-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-context-suite-guards--a00-5a14d8f1 tip 401b20f68 (branch de-base-EG.21; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Pasted evidence row does not add up: three-file run reported as 27 passed, the tip has 28 tests (node:89)
2. 3. The 134 s re-attribution is asserted, not measured (node:65)
3. 4. A second copy of the strip predicate diverges from the amended one (suite_guards.py:58)
4. 5. Exemption is unconditional and the suite's stated invariant was not updated (test_agi_env_strip.py:52)
5. 6. The committed regression test exercises only the happy path (test_declared_suite_guards.py:408)
6. 8. extra_keys bypass is untested and unremarked (suite_guards.py:136)
7. 9. The corrective's orders are not in the loop branch's ancestry; the hypothesis has no verdict (hypothesis node:1)
8. The committed regression test mutates the LIVE session env and throws away the restore memo — extensions/agi/tests/test_declared_suite_guards.py:409 calls `suite_guards.strip_dispatch_env()` with no `memo`, and the `finally` at :418-420 pops only its own two keys. Probed on the tip blob: a pre-existing AGI_* key (AGI_SEAT_Z) is deleted from `os.environ` for the remainder of the session with nothing restoring it. Every sibling caller pairs the call with `restore_dispatch_env` (test_suite_guard_policy_args.py:155-160, :168-174), so this test is the one place the module mutates the process env one-way. No observable break today (the session autouse fixture already stripped AGI_* before the test, suite_guards.py:139-155), but it is a latent cross-test hazard in the one file the round was supposed to strengthen.
9. Unread reader, named here because the round reported on ONE suite while changing TWO: the engine suite shares the amended body — extensions/agi/conftest.py:66 (`strip_dispatch_env(GIT_CONFIG_SPAWN_VARS, memo=_AGI_STRIPPED)`) and :80 (`make_agi_env_stripped_fixture(GIT_CONFIG_SPAWN_VARS)`) — so the sentinel exemption now also governs the engine suite and the `_strip_agi_env` seam that test_agi_env_strip.py:118-133 drives by path from a real child. The node's evidence table (node:31-33, :86-90) measures and reports only the declared context suite; the engine-suite effect was never measured or reported.
10. Checks that came back CLEAN, recorded so the next reviewer does not re-derive them: the fix is LOAD-BEARING, not cosmetic (probed BASE vs TIP: BASE `strip_dispatch_env` deletes AGI_GUARD_LEAK_CHILD and has no PROBE_SENTINEL_VARS; TIP keeps it while still stripping AGI_SEAT_X/AUTORESEARCH_ITER/GIT_CONFIG_COUNT); the guard was NARROWED, never removed (the `continue` is additive, the strip test is untouched, and `.agi/context/conftest.py` — the claim the node makes at node:36 — is absent from the diff, so it is byte-identical); the new test spawns nothing (no subprocess, no /proc, no tmux/systemd/crontab — the forbidden-leaf guard is not engaged); no node under .agi/nodes is deleted or moved (the diff is 3 files, 151 insertions, 0 deletions — a mint, not a demotion); ceilings hold (12 production lines <= 20, 20 test lines <= 40, 1 kid, and the git-hook strip does not leak into the declared suite because that conftest passes no extra_keys); refs/grid is empty at 019fae9f7, at 401b20f68 and at HEAD alike, so the absent grid commit is a repo-wide property of this lineage, not a round defect; and the two ownership checks re-confirmed fresh — FILE SCOPE (every touched path is in the orders' list: suite_guards.py, test_declared_suite_guards.py, the kid's own node) and authorship (kid commit 067cc7326 is signed `a00-55826c04`, the node's own id; the parent's 401b20f68 is signed `a00-5a14d8f1` and contributes only the THOUGHT block, so no production byte is attributed to the parent).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
HARD RULE (from EG.13, unchanged) every .agi/context pytest runs ONLY under systemd-run --user --scope -q -p MemoryMax=2G -p MemorySwapMax=0; the standin test alone, never bare.
TESTS     test_declared_suite_guards.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/suite_guards.py · extensions/agi/tests/test_declared_suite_guards.py · .agi/nodes/experiment/a00-55826c04-d4408d.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 401b20f68 · <= 40 test lines net over 401b20f68 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 401b20f68 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.21: mur-eg-6 EG.13-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
