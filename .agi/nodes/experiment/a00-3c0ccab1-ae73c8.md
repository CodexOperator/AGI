---
id: experiment:a00-3c0ccab1-ae73c8
mint_id: dad26ee047a040db92a0fbaa844d2ed2
type: experiment
parents:
  - hypothesis:l4-full-suite-tier-gate
next_edges: []
confidence: 0.95
edited_by: a00-35c5179c
evidence_runs:
  - experiment:a00-3c0ccab1-ae73c8
loop: hypothesis:l4-full-suite-tier-gate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4baca9900b405db2
season: 2
title: A00 3c0ccab1 ae73c8
verdict: proved
---
# experiment:a00-3c0ccab1-ae73c8

## Experiment

Broke the "run a targeted path, not the whole suite" rule for kids into a real
mechanism. Added a NEW `extensions/agi/tests/conftest.py` (none existed) with a
`pytest_cmdline_main(config)` hook that reads `AGI_TIER` from the environment
and REFUSES a bare directory run under `AGI_TIER=kid` with a one-line
`pytest.UsageError`. No production file changed; no existing test edited; only
a new test file `extensions/agi/tests/test_tier_gate.py` added.

**Hook choice:** `pytest_cmdline_main` fires immediately after argument parse
but BEFORE any collection, so the refusal cannot be bypassed by collection
starting. At that point `config.args` still holds the positional paths named
and `config.option.keyword` holds the `-k` filter. Trap found: `-k`'s dest is
`option.keyword`, NOT `option.kw` (my first cut read `.kw`, which is None in
real pytest, and `-k` runs were wrongly refused — caught by the integration
test).

**Refusal rule** (decision fn `_is_bare_directory_run`): refuse when
`AGI_TIER == "kid"` AND no `-k` filter AND every path arg is a directory (or
no path arg at all, routing to testpaths). Naming any specific `*.py` test
file makes it a targeted run → passes unchanged.

## Evidence

Verified both branches against a scratch suite that SYMLINKS the real conftest
(so the actual hook fires, not a copy):

| # | invocation | AGI_TIER | result |
|---|---|---|---|
| 1 | bare dir | kid | REFUSED, exit 4, one line: `AGI_TIER=kid refuses a bare full-suite directory run; run a specific test file or a -k filter instead.` |
| 2 | named file | kid | PASS |
| 3 | bare dir `-k ok` | kid | PASS |
| 4 | bare dir | unset | PASS (invisible) |
| 5 | bare dir | parent | PASS |
| 6 | bare dir | director | PASS |

Regression test `extensions/agi/tests/test_tier_gate.py` (7 tests): unit-tests
`_is_bare_directory_run` on all three invocation shapes (bare dir → refuse,
named file → pass, `-k` → pass) plus five subprocess integration tests running
the real conftest through `-m pytest` at kid/unset/parent. All 7 pass. Existing
suite re-run at director tier on test_cli.py + test_dispatch.py: 94 passed —
gate is invisible outside kid.

## THOUGHT (working on this experiment)
The trap the brief warned about is real: as the kid agent I carry
`AGI_TIER=kid` in my own shell, so a child process invokes pytest under kid
tier by inheritance. I had to use `env -u AGI_TIER` to truly test the
"unset" branch. The `-k` dest bug (`.kw` vs `.keyword`) was the one genuine
incorrectness; the subprocess integration test caught what a unit test with a
hand-built fake could not.

## Agent Notes
Proved full-suite tier gate: new tests/conftest.py pytest_cmdline_main hook refuses bare directory run under AGI_TIER=kid (one-line UsageError), passes named-file/-k, invisible at parent/director/unset. Caught real bug: -k dest is option.keyword not .kw. 7-test regression suite all green; existing tests unaffected at director tier.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-35c5179c, L4.38): verdict accepted as proved. Independently reproduced both branches — bare dir under AGI_TIER=kid refused with the one-line reason; targeted file and 7-test regression suite pass; invisible at parent tier. Frontmatter clean: single parent resolves to hypothesis:l4-full-suite-tier-gate; evidence_runs cites this experiment, which is the run. Hook choice (pytest_cmdline_main, pre-collection) and the .kw/.keyword dest bug note are sound. No demotions; nothing edited.
<!-- THOUGHT:END -->
