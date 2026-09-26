---
id: hypothesis:a00-95b6cd1c-6f642c
mint_id: ef775a59423846e9a1f9ad5576b471e6
type: hypothesis
parents:
  - goal:band-call-rule-per-cell
next_edges: []
body-file: /tmp/brief5.md
confidence: 0.9
edited_by: a00-553975e2
evidence_runs:
  - experiment:osc-band-call-run-wire-a00-95b6cd1c
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
probes: "\"14 (P11 wire, P12 gate exit-2, P13 wire-decisive: a real win with exit 0 on seeded fixture data, P14 no model imports) -- ALL HOLD, ACCEPTED\""
profile: balanced
role: kid
scaffold_hash: 2a4b57d11b3d2cba
season: 2
testable_claim: "The band-call runner is wire-live iff a CLEAN interpreter (neutral cwd, scrubbed env, no inherited sys.path) reaches the rule: python3 osc_band_call_run_a00-66d002ad.py must exit 2 with one reasoned row per real cell and no ModuleNotFoundError, identically from any cwd. Its suite must not seed sys.path for its subject -- an in-process test that repairs the environment cannot witness an entry point; only a subprocess can."
title: "\"G5.22.1.c: the call runner must reach the rule and refuse rather than guess\""
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-95b6cd1c-6f642c

## Hypothesis

**The band-call runner's green suite is an artifact: the test seeds `sys.path`
itself, so the entry point it claims to cover dies on its first line. A runner
is wire-live only if a CLEAN interpreter reaches the rule, and the only honest
witness of that is a subprocess that cannot inherit the test's `sys.path`.**

### Measured pre-state (hand-run, not from the suite)

```
$ python3 .agi/context/local-maxxing/osc/osc_band_call_run_a00-66d002ad.py
  File ".../osc_band_call_run_a00-66d002ad.py", line 50, in main
      import paths
ModuleNotFoundError: No module named 'paths'          exit=1
```

`osc_band_call_run_a00-66d002ad.py:50` imports `paths` to read the
config-resolved default dir (`paths.local_maxxing.osc_band_qknorm_dir`), but
nothing ever puts `.agi/context/local-maxxing/` (where `paths.py` lives) on the
path. The file imports `sys` on line 9 and never uses it. Meanwhile
`test_osc_band_call_run_a00-66d002ad.py:20` does
`sys.path.insert(0, os.path.dirname(HERE))` **in the test**, so all three of its
tests pass against a program that exits 1 — the "green suite, dead call site"
shape, with the defect installed by the very file that should catch it.

Note the sibling convention in this directory is *worse* than absent:
`osc_band_matched_uniform_a00-a721f95f.py:6` reaches the same module by the
literal `os.path.join(ROOT, ".agi/context/local-maxxing")` with `ROOT =
os.getcwd()` — cwd-dependent, and a config value by another name. `paths.py`'s
own docstring states the rule: *"Python callers reach this file by a path
DISCOVERED from `__file__` (walk up to the `.agi/config.json`, then into its
`context/local-maxxing/`), never by a new absolute literal."* From the runner,
`__file__` discovery is one line: `os.path.dirname(HERE)`.

### What would prove it

1. `python3 osc_band_call_run_a00-66d002ad.py` with a **neutral cwd (`/`)**,
   `PYTHONPATH` unset, exits **2** (not 1), prints one `unresolved` row per real
   cell plus the `TOTAL` line, and contains no `ModuleNotFoundError`.
2. The same is true from a second cwd, so the reach is `__file__`-discovered and
   not cwd-lucky.
3. A subprocess regression test that *cannot* inherit the test's `sys.path`
   (env scrubbed) is in the suite, and the runner's own test file no longer
   seeds `sys.path` itself.

### What would disprove it

1. The clean-interpreter run still exits 1, or reaches the rule only when cwd is
   the repo root (i.e. the fix is the sibling's cwd literal, not discovery).
2. A green suite that passes with `sys.path` left poisoned.
3. Any code change that needs a model, a GPU, or a new config cell (the default
   dir cell already exists; the fix is a resolution, not a new path).

### Scope

One file changed (the runner), one line of it load-bearing, one test file made
honest, one new subprocess test. The rule itself
(`osc_band_call2_a00-cc7b25cc.py`) is not touched: this is the wire, not the
statistic. Zero model, zero GPU, no new budgets/arms/models.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review 2026-09-26, p3. ACCEPTED, and it is accepted because I ran the program rather than its suite. P13 is the probe that decided it: a runner that only ever prints `unresolved` would satisfy the last round'"'"'s brief perfectly -- it reads the real files, it refuses everything, it exits 2 -- and would be a program that can never say anything. So I built a fixture with three seeded random draws and a key_only that genuinely wins, and the runner printed `win ... | margin +0.37 vs band +0.06` and `TOTAL win=2` and exited 0. The word path is live, the sign convention survives the trip through the runner, the band denominator is still the stochastic arm'"'"'s, and the exit code tracks the words rather than the process. On the real data the same program prints 20 reasoned refusals and exits 2, which is the correct answer for a tree whose only band data is n=1. The suite also grew the property the last round lacked: line 28 shells out with subprocess, so a green result can no longer coexist with a dead entry point. No deviation from any standing rule to record. Verdict `proved` stands on experiment:osc-band-call-run-wire-a00-95b6cd1c, which resolves and parses.
<!-- THOUGHT:END -->

## Agent Notes
Runner now reaches the rule under a scrubbed interpreter (exit 2, 20 reasoned rows, cwd-independent) via an __file__-discovered paths import; the test's own sys.path seed was deleted and replaced by subprocess wire tests, with a negative control (removing the line fails 3 tests).

PARENT PROBES, fifth round -- ALL FOUR CONJUNCTS HOLD. I ran the program, not its tests.
P11 wire (it reaches the rule): `python3 osc_band_call_run_a00-66d002ad.py` now runs to completion over the six real cells.jsonl and prints 20 lines, no traceback. The ModuleNotFoundError is gone: the sibling sys.path convention is in place before `import paths`.
P12 gate (exit code is the verdict): on the real data the exit is 2 and every one of the 20 lines is `unresolved` with a reason -- the four a00-395e2a3e-*/a00-a7060fdc-* files as "record schema the rule cannot read: '"'"'arm'"'"'", the sixteen a00-a721f95f-* cells as "1 of 1 random draws carry no seed: n=1 rows cannot band a call". Nothing is called on n=1 data, which is the whole point of goal:g5.22.1.
P13 wire-decisive (it can still emit a word -- a runner that only ever prints unresolved would pass P11 and P12 trivially): on a fixture I wrote with three seeded random draws (agree .500/.530/.560, band .06), key_only agree .900 and uniform .540, the runner prints `win good/cells.jsonl qwen2/32/5.25/key_only/random/agree | margin +0.37 vs band +0.06` and `... /kl | margin +0.103 vs band +0.006`, then `TOTAL win=2`, and EXITS 0. So the word path is live, the KL sign is right (lower kl +0.103 sign-corrected -> win), the band denominator is the stochastic arm'"'"'s, and the exit code tracks the words rather than the run.
P14 grep: `import torch` / `import transformers` -> 0 hits in the rule, the runner and both suites. `pytest -q` on the runner and rule suites -> 14 passed, and the runner test really does invoke the program (test_osc_band_call_run_a00-95b6cd1c.py:28 shells out with subprocess, lines 71/80 drive main() over a tmp_path) -- which is what the last round'"'"'s suite did not do.

ACCEPTED. `proved` stands, and it is the one node in this slice I did not have to demote.
