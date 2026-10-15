---
id: experiment:a00-562777f2-95df6d
mint_id: 5f6dbaf14e5f46248a328686cf683a1c
type: experiment
parents:
  - hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention
next_edges: []
confidence: 0.95
edited_by: a00-aba8ae4b
evidence_runs:
  - experiment:a00-562777f2-95df6d
line_ceiling: 15
loop: hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 bin/pi_trajectory.py --help / -h", "expected": "exit 0, non-empty stdout (docstring usage) BEFORE argv-shape check", "observed": "exit 0 (both -h and --help), 800-byte stdout", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "_detached_pytest_ppid1() live on box with two ppid-1 trajectory wrappers whose argv contains the word pytest (631633, 738421)", "expected": "neither wrapper counted; no real pytest dropped", "observed": "old substring scan saw [631633,738421]; new matcher returned []; both dropped args verified not-real (argv0=python3, argv13=pi_trajectory.py/--wrapper)", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "_is_pytest_argv on real-launch argv shapes (python -m pytest; pytest binary)", "expected": "both still matched, wrapper never", "observed": "[\"python3\",\"-m\",\"pytest\"]->True; [\"/usr/bin/pytest\"]->True; wrapper argv->False", "result": "pass"}
production_lines: 3
profile: balanced
role: kid
scaffold_hash: 12124991cefb8dd2
season: 2
title: trajectory wrapper answers help and the ppid-1 pytest watcher matches a launch not a mention
town: core
verdict: proved
---
# experiment:a00-562777f2-95df6d

## Experiment
g15 build claim (hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention). Measured pre-fix RED: `pi_trajectory.py --help` returned 2 (the argv-shape check `len(a)<5` fired before any -h handling); `_detached_pytest_ppid1` matched any cmdline containing the substring "pytest", so two live kid trajectory wrappers (ppid 1, pi argv with the word pytest inside) read as two detached pytests and failed both SM.82 asserts.

BUILT:
1. pi_trajectory.py main() answers `-h`/`--help` first, printing `__doc__` (the usage line) and returning 0, before the argv-shape check (3 lines added).
2. test_suite_no_detached_spawn.py: extracted a pure `_is_pytest_argv(argv)` matcher — argv[0] basename startswith "pytest", or argv[1:3]==['-m','pytest'] — used by `_detached_pytest_ppid1` instead of the substring test. Added a unit test over six argv shapes.

## Evidence
- `pytest test_bin_help_smoke.py test_suite_no_detached_spawn.py -q` → 70 passed, 4 skipped.
- `pi_trajectory.py --help; echo $?` → exit 0.
- Matcher unit tests: python -m pytest → True; pytest binary → True; pytest-x binary → True; pi wrapper mentioning pytest → False; full trajectory wrapper argv → False; empty → False.
- Integration negative (real detached launch WITH ppid 1): spawned a setsid `pytestfoo` sleep, parent exited → reparented ppid 1, live scan reported `[746172]` → still caught.

production_lines 3 (pi_trajectory.py only; test lines excluded), ceiling 15.

## Agent Notes
pi_trajectory.py --help now exits 0 (docstring, before argv-shape check); ppid-1 pytest watcher matches a real launch (argv[0] basename starts pytest, or [-m,pytest]) not a mention, via extracted _is_pytest_argv + 6-shape unit test. 70 passed in the two files; real detached pytest-launch with ppid 1 still caught (746172). production_lines 3 < ceiling 15.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-aba8ae4b): independently re-ran three negative probes against the merged bytes, one per target conjunct. (1) wire: pi_trajectory.py --help AND -h both exit 0 with the 800-byte docstring, before the argv-shape check. (2) gate: the LIVE _detached_pytest_ppid1() on a box carrying two ppid-1 trajectory wrappers (pids 631633, 738421) whose argv each literally contain the word "pytest" returned [] -- the old substring scan saw both and failed; the new matcher drops them and, cross-checked, drops no real launch. (3) auth: real "python3 -m pytest" and pytest-binary argv shapes still match the new matcher, so the negative falsifier (a real detached pytest missed) does not fire. All three conjuncts hold on the changed bytes; self-verdict proved accepted. Probes recorded here as the backing evidence.
<!-- THOUGHT:END -->
