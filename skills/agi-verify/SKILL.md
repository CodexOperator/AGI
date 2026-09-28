---
name: agi-verify
description: >
  Verify the agi graph and engine after a landing: the one verify command and what each
  check means, the node-count floor, links, GOALS.md round trip, the suite lock and the
  engine test suite. Use after any merge, node migration, retag or engine edit, and before
  claiming a landing is clean.
---

# agi-verify — every landing verified

## 1 · The one command
```bash
python3 extensions/agi/bin/commands.py run verify
```
| check | green means |
|---|---|
| links | `broken=0` (`links.py links`) |
| goals-check | `GOALS.md` ⇄ goal nodes byte-identical (`snapshot-goals.py --render --check`) |
| smoke / node-count | active + deprecated never dropped (`driver.sh --smoke --max-iters 1`); stamped only on the integration branch |
| viewport-verify | one render, two readers (goal:g2.19) |
| write-guard · dispatch-help · budget · anonymize · seat-model · node-dirs | each tool's own invariant |
| bin-suite-fresh | a bin/*.py is newer than the last suite run → the SUITE is owed (known FAIL until a suite window runs) |

## 2 · The suite
```bash
python3 extensions/agi/bin/verification.py window      # lock free? tip? baseline?
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/<file>.py -q   # one committed file, never a rotate test from a pane
```
- The lock is `.agi/sessions/verify-suite.lock`; "free" = absent in MAIN AND every post worktree (F7).
- Never merge into a tree while a suite runs in it: getsource tests read the moved file (2 false reds, measured).
- local-maxxing context tests: `PYTHONPATH=` the cell `paths.local_maxxing.osc_test_pythonpath` + system python3 (the venv has no pytest).
- The Prime grants ONE suite window at a time; a probe never calls rotate/heal/send/dispatch functions (a probe
  once TERM'd the Prime's pane from inside it).

## 3 · Also
`links.py schema` (which nodes violate their type's required list, dry) · `snapshot-goals.py --render --check` ·
`envfile.py --check` (presence, not validity) · `provisioning.py status` · `spawn_budget.py status` ·
`crons.py show` · guard: `~/work/.sanctuary/guard/guard-init.sh --status` + `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-` (drop column 2: every line carries the host name, TM [red] 02:36Z 09-27).
Report outcomes faithfully: a FAIL is quoted with its line, never summarised away.
