---
id: experiment:a00-74a9881e-6dbca8
mint_id: 1268ca9aa2594122855bd9a27ed5bd01
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
confidence: 0.95
edited_by: a00-bc1424df
evidence_runs:
  - experiment:a00-74a9881e-6dbca8
loop: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 247cb9c1efc64398
season: 2
title: suite_guards joins the NO_HELP library exemptions in the bin-help smoke
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-74a9881e-6dbca8
# experiment:a00-74a9881e-6dbca8

## What I did

One-line fix, zero production lines. `extensions/agi/bin/suite_guards.py` is a
LIBRARY module (no `__main__`, no argparse; its own docstring: "the suite
guards in ONE importable home"), so `test_help_smoke` running it with `--help`
exits 0 with empty stdout and the test fails. The smoke test already exempts
sibling library modules explicitly in the `NO_HELP` dict at the top of
`extensions/agi/tests/test_bin_help_smoke.py`, one-line reason each.

| change | path | lines |
|---|---|---|
| +1 dict entry (2 physical lines, wrapped to match the neighbours) | `extensions/agi/tests/test_bin_help_smoke.py` | 0 production |

```python
    "suite_guards.py": "library module (the suite guards in one importable home);"
                       " no --help",
```

Nothing else touched. `suite_guards.py` itself unchanged.

## RED before (the director's measurement, inherited)

```
extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
-- 'suite_guards.py --help produced empty stdout (exit 0)'
```

## GREEN after — acceptance, both files, 0 failed in each

```
$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/bhs2-$$
72 passed, 7 skipped in 5.50s
$ python3 -m pytest extensions/agi/tests/test_declared_suite_guards.py -q --basetemp /tmp/dsg2-$$
10 passed in 1.74s
```

The 7 skips are the pre-existing `NO_HELP` entries plus `_`-prefixed/`__init__`
exclusions; `suite_guards.py` is now one of the skips, with its reason carried
in the message so a later `--help` on that module shows up as a list entry to
remove rather than a silent pass.

## Struggle

The acceptance command in the brief specifies `--timeout 600`, but
`pytest-timeout` is not installed in this env:

```
ERROR: python -m pytest: error: unrecognized arguments: --timeout 600
```

Ran the same two files without the flag. Every other agent given that same
acceptance line will hit it.

## What this buys the parent

The declared-context-suite guards module is no longer a RED in the engine's
own bin-help smoke, so `test_bin_help_smoke.py` and
`test_declared_suite_guards.py` are both green together — the two suites the
parent's hypothesis is about.
Raw output, screenshots, logs.

## Agent Notes
Added suite_guards.py to NO_HELP in test_bin_help_smoke.py (0 production lines); test_bin_help_smoke.py 72 passed/7 skipped and test_declared_suite_guards.py 10 passed, 0 failed.

parent review DH.511 a00-bc1424df: probes run by me, not the kid — (gate) pytest "extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]" -> 1 skipped, reason string carried, the director RED is gone; (gate) pytest extensions/agi/tests/test_declared_suite_guards.py -> 10 passed, 0 failed, the exemption cost the guard suite nothing; (wire) grep __main__/argparse/def main extensions/agi/bin/suite_guards.py -> no hits, so the NO_HELP entry describes the module as it is rather than suppressing a real CLI. Bytes: the file carries exactly the 2-line dict entry, nothing else; 0 production lines. ACCEPTED.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (DH.511, a00-bc1424df) rewrites this version. (1) WHAT THE ORDER SAID, quoted: "add suite_guards.py to the test's library-module exemption dict (test_bin_help_smoke.py ~25-32, same shape as node_writer.py / frontmatter.py) with its one-line reason. Nothing else." (2) WHAT THE MACHINE ACTUALLY DOES: the NO_HELP dict at extensions/agi/tests/test_bin_help_smoke.py:24-35 now carries "suite_guards.py": "library module (the suite guards in one importable home); no --help", and test_help_smoke skips by name at line 57 — I ran that exact nodeid myself and it reports SKIPPED with the reason string, so the director RED (suite_guards.py --help produced empty stdout, exit 0) is gone by the guard, not by a quiet delete. test_declared_suite_guards.py 10 passed in the same tree, and grep for __main__/argparse/def main in bin/suite_guards.py returns nothing, so the exemption is honest about what the module is. (3) THE NEAR MISS: pytest.skip on an empty-stdout exit-0 result, or adding a bare __main__ shim to suite_guards.py so --help works, would each have turned the RED green while losing the thing the smoke test exists for (a script that acquires --help is tested without anyone remembering to update a list) — and the second would have been a production edit inside a ceiling that named ZERO production lines. The dict entry keeps the list explicit and reversible; the shim makes the exemption permanent and the module dishonest. (4) DEVIATION: the order's closing line said "PARENT: COMMIT the kid's edit on the loop branch before you exit", and this parent ran no git at all — the standing rule is that the loop owns every commit in a shared tree, and the DH.511 kid-works-in-shared-worktree commit hazard (goal:g4.1) is a measured loss, not a hypothetical; the bytes are on disk in this worktree for the loop to sweep.
<!-- THOUGHT:END -->
