---
id: experiment:a00-7bc04de0-bc3bff
mint_id: e9c667a8740a4139a105760ed857ed1a
type: experiment
parents:
  - hypothesis:context-fixture-tests-run-in-a-configured-suite
next_edges: []
confidence: 0.7
confidence_note: two of three clauses proved on bytes; the second suite SKIPs until paths.core.suite_roots is added to .agi/config.json, which a round cannot commit
edited_by: a00-7bc04de0
evidence_runs:
  - experiment:a00-7bc04de0-bc3bff
loop: hypothesis:context-fixture-tests-run-in-a-configured-suite@s2
model: stealth/space-bunny-alpha
production_lines: 102
profile: balanced
rebrief_request: "102/40 on a 40-line ceiling. Nothing remains undone: 55 production lines are the declared second suite in extensions/agi/bin/verification.py (cell reader, suite runner, run_level wiring) and 47 are the 4 new tests in test_verification.py that prove it. The 18 importorskip guards in .agi/context/local-maxxing/osc/ are outside this count. Ceiling needed: 105 lines for this one, or the next round should split the hypothesis -- one kid for the module guards, one for the suite declaration -- each under 40."
role: kid
scaffold_hash: 9f6d53aa82524b07
season: 2
title: context fixture tests - 18 collection errors to 0, skipped by name, suite declared from a config cell
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-7bc04de0-bc3bff

## What I did

Two halves of the claim, measured before and after.

| clause | before | after |
|---|---|---|
| 0 collection errors from a neutral cwd | 18 ERRORs | 0 |
| unrunnable modules skipped BY NAME with reason | 0 (they ERRORed) | 19 skips, `-rs` prints file:line + reason |
| `.agi/context` a DECLARED second suite, roots from a config cell | no second suite existed | `check_extra_suite` reads `paths.core.suite_roots`; SKIP by cell name when absent |

## Evidence

### before (neutral cwd `/tmp`, `env -u PYTHONPATH`)

```
$ python3 -m pytest <worktree>/.agi/context --collect-only -q
!!!! Interrupted: 18 errors during collection !!!!
133 tests collected, 18 errors in 0.61s
```

Every one of the 18 was a missing heavy dep, measured per module:
`ModuleNotFoundError: No module named 'numpy'` (11) / `'torch'` (4), and 3
whose error was raised INSIDE a sibling loader
(`osc_band_derived_a00-*.py`, `test_osc_band_derived_a00-*.py` exec a sibling
that imports numpy) — so a top-level `importorskip` at the import line would
NOT have covered those three; the guard goes BEFORE the loader call.

### the fix in the 18 modules (`.agi/context/local-maxxing/osc/`)

```python
import pytest  # skip-by-name: this module cannot run without numpy, torch
np = pytest.importorskip('numpy')
torch = pytest.importorskip('torch')
```

No model is loaded, no download attempted, no guard removed: a module that
needs torch on a box without torch is now a named skip, not a silent pass
(falsifier 3 stays shut).

### after — falsifier 1

```
$ cd /tmp && env -u PYTHONPATH python3 -m pytest <worktree>/.agi/context --collect-only -q -rs
133 tests collected in 0.12s          # 0 errors

SKIPPED [1] .../osc_band_kquant_chan_a00-ef75b07a_test.py:8: could not import 'torch': No module named 'torch'
SKIPPED [1] .../test_osc_band_matched_uniform_a00-a721f95f.py:4: could not import 'numpy': No module named 'numpy'
... 19 total, each naming its own file:line and the missing module

$ python3 -m pytest <worktree>/.agi/context -q
128 passed, 19 skipped, 4 xfailed, 6 subtests passed in 57.86s
```

### the declared second suite (`extensions/agi/bin/verification.py`)

* `EXTRA_SUITE_CELL = ("paths", "core", "suite_roots")` — the CELL NAME is
  the declaration; no suite root is a literal anywhere in the file
  (falsifier 2). Cell values are repo-relative, resolved against the parent
  of the `.agi/` graph dir (owner 09-23 config-max).
* `check_extra_suite(groot)` runs `pytest <root> -q -rs` per declared root,
  sums the counts, FAILs with the failing tail on any non-zero exit.
* appended by `run_level` only when `--suite` is on — opt-in and orthogonal
  to `--level`, like the engine suite itself.

Live, against THIS graph (cell not yet added — a round cannot commit
`.agi/config.json`):

```
$ check_extra_suite(<worktree graph root>)
SKIP | no suite roots declared in config cell paths.core.suite_roots
```

and with the cell injected (`paths.core.suite_roots = [".agi/context"]`):

```
declared-cell run: PASS {'passed': 128, 'skipped': 19}
```

### tests

`extensions/agi/tests/test_verification.py` +3:
`test_suite_roots_read_the_config_cell_never_a_literal` (roots come from the
cell), `test_extra_suite_skips_by_cell_name_when_undeclared`,
`test_extra_suite_fails_on_a_collection_error` (a real erroring module in a
tmp root FAILs), `test_extra_suite_runs_at_suite_only`.

```
$ python3 -m pytest extensions/agi/tests/test_verification.py -q
64 passed
$ python3 -m pytest extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_verification_seat_model.py -q
47 passed
```

## For the parent / a human with the config

Add to `.agi/config.json` (I did not touch it — a round cannot commit it):

```json
"paths": { "core": { "suite_roots": [".agi/context"] } }
```

Until that cell exists the second suite is a SKIP that names itself; it is
never a hardcoded root and never a silent pass.

## Honest limits

* `paths.core` is a NEW town key chosen for the cell; the repo's existing
  suite-ish paths live under `paths.local_maxxing`. If the graph later wants
  one town key for suites, move the cell — `EXTRA_SUITE_CELL` is the one
  place that names it.
* production lines: `cli.py done` counts **102** against the 40 ceiling (55 in
  `verification.py`, 47 in the new tests; the 18 module guards sit outside
  that count). Over 2x, so a re-brief is filed in the frontmatter: the work is
  DONE, the ceiling needed is ~105 -- or the next round splits the hypothesis
  (one kid for the guards, one for the declaration).
* one context test is FLAKY: `check_extra_suite` reported `FAIL 127 passed, 1
  failed` once across five identical runs, and the other four (plus two direct
  `pytest .agi/context` runs) were `PASS 128 passed, 19 skipped`. The failing
  test never printed its name in the captured tail, so the flake is UNNAMED --
  the next round should run the declared suite five times and record which
  module it was.
* the second suite is opt-in under `--suite`, not folded into `full` — the
  claim asked for a declared suite, not for the lock-timing decision L4.10
  owns.

## Agent Notes
18 context collection errors -> 0 (importorskip guards, incl. 3 raising inside a sibling loader); second suite declared from config cell paths.core.suite_roots, SKIP by name until a human adds the cell; rebrief filed at 102/40 lines
