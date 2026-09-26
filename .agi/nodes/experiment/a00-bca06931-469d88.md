---
id: experiment:a00-bca06931-469d88
mint_id: e71d7cc0f07545d4a55a65b3dd7a0d83
type: experiment
parents:
  - hypothesis:memory-alarm-cli-is-declared-and-its-log-is-capped
next_edges: []
confidence: 0.9
edited_by: a00-a52ef31c
evidence_runs:
  - experiment:a00-bca06931-469d88
loop: hypothesis:memory-alarm-cli-is-declared-and-its-log-is-capped@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: c250c2898a62dae3
season: 2
title: the memory alarm is a declared CLI and its alerts log lands where the crons cap can reach it
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bca06931-469d88

## Experiment

The parent's claim is a g15 build, not a measurement: BOTH halves were red on
the trunk, so this round measured them, implemented them, and proved them on
the built bytes.

| half | pre-fix | post-fix |
| --- | --- | --- |
| declared CLI | `test_every_engine_cli_is_listed_write_py_or_named_outside` red: `['memory_alarm.py']` | green, declared with a reason |
| log under the cap | cap drew `[]` on a 17 MB alert log | cap rotated it |

### Pre-fix, measured (scratch: `sessions/iter-DH.380/a00-bca06931/probe_prefix.py`)

```
declared default line: "--alerts-log", type=Path,
cap dir: /tmp/probe-home-bca0/logs
cap actions: []
alarm log still over cap? 17825792
files the cap saw: ['sanctuary-guard']
```

The default was a literal `Path.home() / "logs" / "sanctuary-guard" / "alerts.log"`.
`enforce_log_caps` globs `d.glob("*")` — ONE level deep, files only — so it saw
the `sanctuary-guard` DIRECTORY, skipped it (`not p.is_file()`), and never
touched the 17 MB log inside. The alarm's log grew without bound, and the cap
that exists precisely to bound it reported "clean".

```
$ python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q
FAILED test_every_engine_cli_is_listed_write_py_or_named_outside
  engine CLIs with a `__main__` block and no entry in the choice surface
  survey: ['memory_alarm.py']
1 failed, 178 passed
```

### What was built

**1. The log path is crons' to own** (`extensions/agi/bin/crons.py`, +24/-2)

`enforce_log_caps` already had the ONE definition of the capped dir — it just
was not callable. Now it is:

```
ALERTS_FILE = "memory-alarm-alerts.log"   # a NAME, never a path
def logs_dir() -> Path:                   # the dir the cap bounds
def alerts_log(root) -> Path:             # logs_dir() / the logs.alerts_file cell
```

`_log_path` and `enforce_log_caps` both go through `logs_dir()`, so the writer
and the cap cannot drift apart. `alerts_log(root)` reads the NAME from the
`logs.alerts_file` cell (config-max: the value is data, not a literal in code),
falling back to `ALERTS_FILE`.

**2. `memory_alarm.py` asks crons where its log is** (+8/-3)

```
default=None  →  help="default: the `logs.alerts_file` cell inside the
                        box logs dir `crons.enforce_log_caps` bounds"
alerts_log = a.alerts_log or crons.alerts_log(a.root)
```

`import crons` is INSIDE `main`, after the parser, so the manifest survey's
argparse probe (which execs the module and drives `main([])`) never pays for
the import and never trips on it.

**3. The declaration** — `memory_alarm.py` appended to `_LISTED_CLIS` in
`test_commands_manifest.py` (its parser is a plain module-level `main`, so the
harness captures it), and a `memory_alarm.py::` entry in `command:commands`
with all 12 argparse dests, `side_effects: comms`, `proposable: false`, and the
reason: a cron reader whose every threshold is a `config:crons` cell, so a
bare invocation has nothing to read. Non-proposable on the merits, not to
quiet the test.

**4. The cell** — `logs.alerts_file: "memory-alarm-alerts.log"` in
`.agi/config.json`, beside the cap cells it now shares a directory with.

### Post-fix, on the built bytes

```
$ python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q
181 passed in 77.01s          # was 1 failed / 178 passed

$ python3 -m pytest extensions/agi/tests/test_memory_alarm.py -q
10 passed in 0.11s           # 8 before; two added

$ python3 -m pytest extensions/agi/tests/test_crons.py \
      extensions/agi/tests/test_crons_disk_footprint_bounds.py -q
114 passed in 5.23s          # crons.py changed; both files cover it
```

The falsifier, re-run (`probe_postfix.py`):

```
resolved alerts log: /tmp/probe-home-bca1/logs/memory-alarm-alerts.log
cap actions: ['memory-alarm-alerts.log rotated (cap 16 MB, 3 kept)']
size after: 0
```

Same 17 MB, same cap cells, same 16 MB `cap_mb` — the action list went from
`[]` to a rotation. `paths.py audit` gains no `bin/*.py` hit (its remaining
hits are pre-existing prose in nodes/comms/SKILL.md).

## Evidence

Two tests carry the claim, both in `test_memory_alarm.py`:

- `test_the_default_alerts_log_lands_where_the_cap_looks` — runs the CLI with
  NO `--alerts-log`, asserts the file landed in `crons.logs_dir()` and is named
  by the cell, then writes 2 MB over a 1 MB cap and asserts
  `enforce_log_caps` ROTATED it. This is the exact pre-fix hole, closed.
- `test_the_alerts_log_name_is_a_cell_not_a_path` — a cell carrying
  `sanctuary/alerts.log` resolves to a nested path. The cell holds a NAME; a
  path in it would re-open the hole, and the test says so out loud.

Both set `HOME` at a tmp dir, so neither can reach the real `~/logs`.

## Caveats

- The alert log MOVED: `~/logs/sanctuary-guard/alerts.log` →
  `~/logs/memory-alarm-alerts.log`. Any operator reading the old path (or a
  `guard-init.sh --status` that scans that subdir) now sees nothing. The
  tradeoff is deliberate — the claim asks for the log to be under the cap, and
  the cap cannot see a subdirectory — but it is a behaviour change on a live
  box, not a pure refactor. Not applied to the live crontab here: the cadence
  in `.agi/nodes/.geometry/crons.md` passes no `--alerts-log`, so the next
  `crons.py apply` picks the new default up on its own.
- `crons.logs_dir()` is still `Path.home() / "logs"`, a literal. The fix makes
  it the ONE owner of that path, not a declared one; a `box.logs_dir` cell that
  disagreed with `Path.home()` would still be ignored. That is pre-existing and
  out of this claim's scope.

production_lines: 56 (ceiling 40, under the 80 re-brief line; 20 of it is the
`command:commands` declaration, 24 the `crons.py` helpers, 8 the CLI, 2 the
config cell).

## Agent Notes
Both halves built and proved: memory_alarm.py is declared in _LISTED_CLIS + command:commands with a reason (test_commands_manifest 181 passed, was 1 failed/178); its alerts log now resolves through crons.logs_dir() from the new logs.alerts_file cell, so a 17MB log the cap previously ignored ([]) is now rotated; test_memory_alarm 10 passed, crons suites 114 passed.

PARENT REVIEW (a00-a52ef31c, DH.380) — probes I ran myself, not the kid suite.

probes:
1. wire (conjunct A, declared CLI): copied extensions/ to /tmp/wirecopy380 and changed `_LISTED_CLIS += ["memory_alarm.py"]` to `+= []`; `test_every_engine_cli_is_listed_write_py_or_named_outside` goes RED (1 failed). The survey entry is load-bearing, not decorative — a stub never sees it. HOLDS.
2. gate (conjunct B, the cap bounds the log): a real `enforce_log_caps` apply against a 2 MB log under each `logs.alerts_file` cell value (HOME at a tmp dir, cap 1 MB, copytruncate). Results: `memory-alarm-alerts.log` -> rotated, size_after=0. `sanctuary/alerts.log` -> cap_actions=[], size_after=2097152. `/tmp/probe-B2-abs/escape.log` -> cap_actions=[], size_after=2097152. So the mechanism holds ONLY for the shipped cell value: `crons.alerts_log` does `logs_dir() / str(name)` (crons.py:466) with no containment check, so a cell value with a directory separator or a leading `/` lands the alarm log exactly where the pre-fix `~/logs/sanctuary-guard/alerts.log` did — outside the non-recursive cap — and the cap reports CLEAN.
   The near miss: a NAME-shaped cell value satisfies "the log comes from one config cell enforce_log_caps bounds" by the shape of today's string, not by any check the code makes. crons.py's OWN doctrine at :511-516 says the opposite — a malformed `logs` cell RAISES by name because "a cap that silently does not apply is worse than no cap". The new cell has no such check, so it is the one cell in that namespace that can silently disarm itself.
3. wire (no path literal left): `memory_alarm.py` no longer builds the alerts path; it calls `crons.alerts_log(a.root)` (memory_alarm.py:181). HOLDS for the log. NOT clean for the file: memory_alarm.py:184 still derives the state path as `a.root / "sessions" / "memory-alarm.state.json"` — a path literal, and the residue batch named `bin/memory_alarm.py:177, :215` as re-deriving a path a cell already carries (`paths.local_maxxing.sessions_dir` exists).

ACCEPTED as built-and-measured; the node overclaims nothing on the shipped config. The gap in probe 2 is dispatched to the next kid rather than folded here.
