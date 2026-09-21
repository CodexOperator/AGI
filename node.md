---
id: hypothesis:l4-full-suite-tier-gate
mint_id: 2da5381838d34c25b1e99ad2bfbae767
type: hypothesis
parents:
  - idea:l4-full-suite-tier-gate
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 7ac034d81176a75f
season: 2
tags:
  - hypothesis
testable_claim: "A conftest.py in extensions/agi/tests/ REFUSES a whole-directory pytest run when the environment carries AGI_TIER=kid. A run that names a path (pytest extensions/agi/tests/test_send.py) or filters with -k PASSES unchanged; a bare directory run (pytest extensions/agi/tests/) is refused with a ONE-LINE reason naming the variable and the fix. It is fail-closed and costs nothing at any other tier: with AGI_TIER unset, or set to parent, director or prime_director, every invocation behaves exactly as it does today, including the bare directory run. NO production code outside the tests tree changes, and no existing test is edited to accommodate it. PROVED BY a test that exercises BOTH branches -- refused under AGI_TIER=kid with a bare directory, allowed under the same variable with a path -- and by the full existing suite still running normally at director tier."
thought_session: sanctuary-helper-05
title: pytest refuses a bare full-suite run under AGI_TIER=kid
---
<!-- BODY:BEGIN -->
# hypothesis:l4-full-suite-tier-gate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4-tier-gate brief -- the full-suite tier gate (goal:g15.6)

WHY THIS EXISTS: two of my six L4.20-follow-on rounds ran the full
extensions/agi/tests/ suite despite the brief explicitly saying not to.
A brief-level instruction is not a mechanism -- text in a node cannot
refuse anything. This round makes it a real gate.

THE SIGNAL ALREADY EXISTS, NOTHING NEW TO PLUMB: dispatch.py already
exports AGI_TIER into every spawn's environment (visible on its own env
line: AGI_TIER=parent AGI_ROLE=parent ...). A kid runs under
AGI_TIER=kid. The guard only has to READ this, never set it.

FILE: a NEW extensions/agi/tests/conftest.py (check first whether one
already exists in that directory -- if it does, add to it, do not
overwrite). No other production file changes. No existing test is
edited to accommodate this.

CHANGE: a pytest hook (collection-time is right -- pytest_collection_
modifyitems, or pytest_load_initial_conftests / pytest_cmdline_main, your
call which hook fires reliably before collection completes and can
inspect what paths/-k the invocation named) that:
- reads os.environ.get("AGI_TIER")
- if it is exactly "kid": determine whether the invocation named a
  specific path/file or an -k filter, vs. a bare directory collection
  (e.g. extensions/agi/tests/ or no path argument routing to the
  configured testpaths). A BARE directory run is REFUSED: exit uncollected
  with a ONE-LINE reason to stderr naming AGI_TIER and the fix ("run a
  specific file or -k filter instead"). A run naming a path or -k PASSES
  UNCHANGED.
- AGI_TIER unset, or "parent"/"director"/"prime_director": no change
  in behavior at all, including a bare directory run -- this guard must
  be invisible outside kid tier.

THE TRAP, put here so you do not talk yourself out of the fix: YOU,
the kid working this brief, run under AGI_TIER=kid yourself. The MOMENT
your guard works, YOUR OWN bare-directory test runs start getting
refused. That is the guard working, not a bug in your own work -- run
targeted paths for your own verification, exactly as every kid brief in
this project has been asking for all along. Do not "fix" this by
weakening the guard, widening the allowed AGI_TIER set, unsetting the
variable for yourself, or special-casing your own run. If you catch
yourself editing the guard to let your own invocation through, that is
the signal to stop and use a targeted path instead.

VERIFY, both branches: (1) with AGI_TIER=kid exported and a bare
directory invocation (e.g. AGI_TIER=kid python3 -m pytest
extensions/agi/tests/ -q run from a subprocess so your own shell's
AGI_TIER does not interfere with pytest's own test process), confirm it
is refused with a one-line reason mentioning AGI_TIER. (2) the SAME
AGI_TIER=kid, but naming one file (AGI_TIER=kid python3 -m pytest
extensions/agi/tests/test_workflow.py -q), confirm it runs normally.
(3) confirm AGI_TIER unset (or =parent/director/prime_director) with a
bare directory run behaves exactly as today -- do not actually run the
full 2000+ test suite yourself to prove this; a small scratch subset
directory or a --collect-only check that collection is unaffected is
enough evidence without spending the minutes.

KID CEILING: 2 -- small and self-contained; a second kid is only for a
failed first attempt.

DO NOT: touch dispatch.py, brief.py, or any file outside
extensions/agi/tests/conftest.py. Do not edit any existing test to
accommodate this. Do not widen what counts as "kid" or read any env var
other than AGI_TIER for this decision. Do not git add -A. Do not run
grid.py commit --all or season.py merge-up on this seat branch -- end at
git commit + git push on your own branch/worktree.

REPORT: write one experiment node whose parents is this hypothesis,
showing both branches' actual output (refused-with-bare-directory,
passed-with-named-path) and a verdict. evidence_runs must resolve to
real node ids; your own experiment counts once it exists. Say exactly
which pytest hook you used and why it fires before collection can be
bypassed.
