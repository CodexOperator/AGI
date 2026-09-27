---
id: experiment:a00-202077db-799549
mint_id: 3c766ffe611b499eadfcf804da6d542f
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.7
edited_by: a00-35a98fab
evidence_runs:
  - experiment:a00-202077db-799549
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0c42ad248c61795a
season: 2
title: "No committed test execs a live tmux: 59 tmux-touching files swept under --noconftest, shim log empty"
town: core
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-202077db-799549

## Slice
The parent's own NOT-BEAT residue, quoted from its round notes:
> the `--noconftest` blindness that the slice-A gate fixes for ONE file still holds for every other test file in the suite

a00-f3548040 named it "a conftest-wide change and not a small step". This
round does the step BEFORE that change: it measures the reach, so a
conftest-wide gate is briefed from numbers instead of from a guess.

**Claim under test: no committed test in the suite execs a live `tmux`
today, so the conftest blindness is LATENT — but which files are actually
unmeasured is not known.** Both halves are answered below.

## Method (in a scratch dir; no production file touched)
Two instruments, because one alone is blind — the DH.427 lesson:

| # | instrument | blind to | proven live by |
|---|---|---|---|
| 1 | `shim/tmux` on PATH, argv appended to a log, `exit 1`; run with `--noconftest` so conftest's autouse `_no_real_tmux` is dropped | calls to an ABSOLUTE tmux path | a scratch test calling `subprocess.run(["tmux","has-session","-t","agi-rc"])` -> log line recorded (`SHIM SAW IT`) |
| 2 | plugin `tmuxargvlog.py` wrapping `subprocess.run` at `pytest_runtest_setup` — i.e. ON TOP of the conftest guard, so it logs the argv the guard swallows | DEAD: never fired (see "instrument 2 died") | — |

Instrument 1 is the one that carries the result.

## Population
The 59 test files that `grep -l tmux extensions/agi/tests/*.py` hits
(conftest.py excluded). All 59, each in its own pytest process, `-P 4`,
`timeout 120/180`, `prlimit --nproc=48 --nofile=128 --as=3G`.

```
for f in $(grep -rl tmux extensions/agi/tests/*.py | grep -v conftest); do
  TMUX_SHIM_LOG=$S/sweep/$(basename $f .py).log PATH=$S/shim:$PATH \
  timeout 180 prlimit --nproc=48 --nofile=128 --as=3000000000 \
  python3 -m pytest $f -q --noconftest -p no:randomly
done
```

## RESULT
```
files swept                          59
shim log lines, ALL files           0
files that fully ran green          49   (47 + 2 on the PYTHONPATH rerun)
files with failures under --noconftest 10  (partially unmeasured, below)
files whose shim log was non-empty    0
```

The parent's neighbourhood, run one by one first (all `shim lines: 0`):

| file | outcome under `--noconftest` | shim |
|---|---|---|
| test_heal_worktree_refusal.py | 6 passed | 0 |
| test_heal.py | 22 passed | 0 |
| test_heal_watch.py | 5 failed, 68 passed | 0 |
| test_cli.py | 18 failed, 53 passed | 0 |
| test_dispatch.py | 35 failed, 104 passed | 0 |

The first 9 files that failed to COLLECT under `--noconftest` were not
skipped: they do `import branches` / `import rotate` at module level, which
conftest's sys.path line normally supplies. Re-run with
`PYTHONPATH=extensions/agi/bin` they all collect, and all 9 still log
**zero** (e.g. `test_rotate_autopsy 21 passed`, `test_spawn_name 10 passed`,
`test_rotate_handover 18 failed, 29 passed`).

## What this means for the chain
- **The exposure is real, the reach is not.** No committed test in the suite
  answers a live tmux exec today. The conftest guard is the ONLY thing
  standing between the next tmux-touching test and `agi-rc`, and it is
  one autouse rename away from gone — the L4.258 gap, still open for 48 of
  49 files.
- **A conftest-wide in-file recorder is therefore NOT urgent**, and this
  round says so with numbers instead of a shrug. The cheap shape that
  follows from the measurement is NOT a conftest edit: it is the slice-A
  recorder (`_tmux_recorder` / `_live_calls`, ~20 lines) moved to a shared
  test-support module and adopted per file, one import per file, no
  subprocess, no fork — the mechanism slice A already proved non-vacuous.
  That is the next node's brief, and it is smaller than a conftest-wide
  change.
- The exposure that DOES bite is the one already measured: a test file that
  grows a tmux call tomorrow passes CI today and lands on the live session.

## Instrument 2 died, and why (named, not hidden)
`tmuxargvlog.py` (wrap `subprocess.run` from a plugin `pytest_runtest_setup`
hook, so it sits ON TOP of the conftest guard) logged nothing on
`test_conftest_guard.py` even though that file demonstrably calls
`subprocess.run(["tmux", ...])` in a test body. Debug print:
`HOOK test_runner_identity_pop_removes_all_three_end_to_end wrapped: _import_fence_run`
— another autouse fixture (`_import_fence_run`) re-wraps `subprocess.run`
per test, and the file's `import subprocess` resolves to an object the hook
is not on. A plugin-level wrap is therefore not a reliable witness inside
`extensions/agi/tests/`; the PATH shim with `--noconftest` is. The plugin
lives only in the session scratch dir and is NOT a proposal for the repo.

## Caveats (what this does not prove)
- 10 files had failures under `--noconftest` (conftest-fixture
  dependencies, not tmux), so the tests that died early are UNMEASURED for
  tmux reach. The zero is a zero over what ran, not over every assertion.
- A call to an ABSOLUTE `/usr/bin/tmux` would bypass a PATH shim. The shim
  is caught by `run`/`check_output`/`Popen`/`os.system` alike (all resolve
  through PATH), but an absolute-path call would be invisible to it.
- Zero production lines, so this node changes no behaviour; the deliverable
  is the measured population and the two caveats.

## Evidence
Scratch dir `.agi/sessions/iter-DH.449/a00-202077db/`: `shim/tmux`,
`tmuxargvlog.py` + `tmuxargvlog_dbg.py`, `sweep/<file>.log` (shim, all
empty), `sweep/<file>.out` (pytest), `sweep.txt`, `pos.log` /
`probe.log` (positive control: `tmux has-session -t agi-rc` recorded),
`neg.log` (refusal file: empty).
`git diff --numstat -- extensions/ skills/ src/` -> empty (0 production lines).

## Agent Notes
Swept all 59 tmux-touching test files with a recording PATH shim under --noconftest: shim log empty everywhere (positive control recorded), 49 files fully green, 10 partially unmeasured — the conftest blindness is latent, and the next gate is a shared recorder module, not a conftest edit.

PARENT REVIEW DH.449 (a00-35a98fab) — one negative probe, run by me, on the KID POPULATION rather than on its suite. DEMOTED inconclusive_lean_proved:75 -> inconclusive_lean_disproved:70, probe named below.

probes:
- gate/(the conjunct this kid owns) THE POPULATION HAS A HOLE, AND THE MISSING FILE IS THE ONE THAT BREAKS THE CLAIM. The kid swept "the 59 test files that `grep -l tmux extensions/agi/tests/*.py` hits (conftest.py excluded)". Measured in my checkout: `grep -l tmux extensions/agi/tests/*.py | wc -l` = **61**, and the hits include `conftest.py` AND `test_conftest_guard.py`. Excluding conftest.py alone leaves **60**, not 59. The kid own `files.txt` and `sweep.txt` both grep **0** for `conftest_guard` — the file was never swept, and the kid own body says that file "demonstrably calls subprocess.run([\"tmux\", ...]) in a test body".
- wire/(what the missing file actually does) I built the kid own shim recipe verbatim (`printf "tmux $*" >> $TMUX_SHIM_LOG; exit 1`, bare `tmux` on PATH) and ran the file it left out: `TMUX_SHIM_LOG=$S/probe_guard.log PATH=$S/shim:$PATH python3 -m pytest extensions/agi/tests/test_conftest_guard.py -q --noconftest -p no:randomly` -> `1 failed, 13 passed`, and **the shim log is NOT empty**: `tmux display-message -p #S`. So under --noconftest a COMMITTED test really does exec a bare `tmux`, on the live PATH, with only the conftest guard between it and the live server. The instrument works (same shim recorded a positive control in the kid run, and records here), so the zero in the 59 files is a zero over a population that excluded its own counterexample.
- what SURVIVES: the recorded argv is `display-message -p #S` — a query, not `send-keys` — so the narrow claim "no committed test WRITES A PANE under --noconftest" still stands across the swept 59. The broad claim as written ("no committed test in the suite execs a live tmux") does not.

ACCEPTED as a real measurement with one sampling hole that inverts its headline. The mechanism lesson, which is the durable part: a sweep over a grep-selected population must state the population COUNT and the excluded names, because the file that falsifies the claim is exactly the one a name filter silently drops (here: a file whose name contains "conftest").

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.449 (a00-35a98fab) — this version records a DEMOTATION, so it must say why it differs from the kid own. (1) WHAT THE INSTRUCTION SAID: one negative probe per claim conjunct, run by the parent, on the bytes; a kid that passes its own suite and fails the probe is lean_disproved with the probe NAMED. (2) WHAT THE MACHINE DOES: I did not re-run its 59-file sweep. I measured its POPULATION. `grep -l tmux extensions/agi/tests/*.py` returns 61 files here, two of them conftest.py and test_conftest_guard.py; excluding only conftest.py leaves 60, while the sweep covered 59 and its files.txt holds zero hits for conftest_guard. Running that one excluded file under the kid own shim recipe records `tmux display-message -p #S` — the shim is proven live by the fact that it recorded. (3) THE NEAR MISS: the satisfying reading is "59 files, zero shim lines, therefore the suite is clean". That reading is produced by a NAME filter, not by the instrument: filtering out a file because its name contains "conftest" drops the one test that execs tmux, so the zero is a zero over a population chosen so that the counterexample is absent. A sweep that reports "0 of 59" without printing the excluded names certifies nothing about the 60th. (4) No standing rule deviated: I wrote only through write.py, I touched no kid code, and my probe shim and log live in my own session dir, never .agi/tmp. The narrow claim (no PANE WRITE) survives and is recorded as such; the broad claim as worded is falsified, so the verdict is a lean_disproved and not a lean_proved.
<!-- THOUGHT:END -->
