---
id: experiment:a00-d2b4276b-b3ac3e
mint_id: ee75fe1613a948529a3190a7047296d9
type: experiment
parents:
  - hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling
next_edges: []
confidence: 0.95
edited_by: a00-d0fdd659
evidence_runs:
  - experiment:a00-d2b4276b-b3ac3e
line_ceiling: 200
loop: hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "mocked LIVE spawn (probe_live_record.py): dispatch.main with Popen stubbed, then read manifest agent record memory_max", "expected": "no flag -> 6G (config); --memory 2G -> 2G on the spawn RECORD, not just the dry-run print", "observed": "no-flag -> 6G; --memory 2G -> 2G", "result": "held -- falsifier (a) does not fire at the record field"}
  - {"conjunct": 2, "class": "gate", "cmd": "real repo dry-run with NO --memory", "expected": "prints the configured 6G; no-flag behaviour unchanged", "observed": "dry-run memory_max=6G", "result": "held -- no regression"}
  - {"conjunct": 3, "class": "gate", "cmd": "sha256 .agi/config.json before/after dispatch --dry-run --memory 2G", "expected": "byte-identical; override is request-scoped", "observed": "f12d165a...b0f3 before and after", "result": "held -- falsifier (c) does not fire"}
production_lines: 33
profile: balanced
role: kid
scaffold_hash: 0e37131cee274b50
season: 2
title: dispatch.py --memory GB per-round memory cap override, built and proved
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d2b4276b-b3ac3e

## Experiment

This is a BUILD claim (hypothesis:lm-dispatch-memory-override-feeds-agi-
batch-scheduling), not a measurement: measure the pre-fix state, implement it,
prove it on the built bytes.

### Pre-fix state (measured)

- `mem_cap.resolve_memory_cap` signature was `(cfg: dict) -> 'str | None'`;
calling it with a second positional arg raised
`TypeError: resolve_memory_cap() takes 1 positional argument but 2 were given`.
- `dispatch.py --help` had no `--memory` flag (grep exit 1).
- `.agi/config.json:125` carried `"memory_max": "6G"`, read only via the one
call site `_mem_cap = mem_cap.resolve_memory_cap(cfg)` (dispatch.py).

### Built

1. `extensions/agi/bin/mem_cap.py` — `resolve_memory_cap(cfg, override=None)`.
   When `override is not None` it wins, normalised exactly like the config
   value (`None`/`'none'`/`'null'`/`''` -> `None`), and `cfg` is never mutated.
   When `override is None` the old semantics are unchanged: absent
   `spawn.memory_max` -> `'4G'`, `null`/`'none'`/`''` -> `None`, else verbatim.
   Shared normaliser factored into `_normalise_cap`.
2. `extensions/agi/bin/dispatch.py` — new argparse `--memory GB`; the ONE call
   site now reads `mem_cap.resolve_memory_cap(cfg, override=args.memory)`; the
   dry-run report prints `dry-run memory_max=<cap>` before the slot loop, so
   the override is observable without a real spawn. The live path stores the
   SAME `_mem_cap` into the spawn record's `memory_max` field
   (dispatch.py `"memory_max": _mem_cap`) — no second cap added.
3. `extensions/agi/tests/test_mem_cap_override.py` — 9 tests: resolver unit
   cases (override wins, no-override = config, `'none'` -> None, no mutation,
   absent config -> `'4G'` regression guard), dry-run `--memory 2G` prints
   `memory_max=2G`, no-flag dry run prints `memory_max=6G`, and a byte-hash
   check that the override never writes `.agi/config.json` on disk.

### Falsifiers (acceptance criteria)

(a) `--memory 2G` changes the resolved cap -> now `2G` (unit + dry-run); the
    live path threads the same `_mem_cap` into the spawn record. **defeated.**
(b) no-flag regression -> `override=None` path is byte-identical in behaviour
    to the old function, and `test_dispatch_dry_run.py` stays green. **defeated.**
(c) override mutates `.agi/config.json` -> resolver never writes `cfg`; the
    dry-run test sha256-hashes the scratch config before/after. **defeated.**

### Production lines

`git diff --numstat -- extensions/agi/bin/mem_cap.py extensions/agi/bin/dispatch.py`
= `15 1` + `18 6` = 33 added, 7 removed. Ceiling 200, not above 2x. No refactor
outside the three named files.

## Evidence

Commands and outputs:

```
$ python3 -m pytest extensions/agi/tests/test_mem_cap_override.py \
    extensions/agi/tests/test_launch_memory_cap.py \
    extensions/agi/tests/test_dispatch_dry_run.py -q
42 passed in 13.02s

$ python3 extensions/agi/bin/dispatch.py --help | grep -- --memory
  --memory GB   hypothesis:lm-dispatch-memory-override-feeds-agi-
                batch-scheduling -- per-round GB override for config
                `spawn.memory_max`; absent means use the configured value...

$ resolve_memory_cap({'spawn':{'memory_max':'6G'}}, override='2G') -> '2G'
$ resolve_memory_cap({'spawn':{'memory_max':'6G'}})               -> '6G'
$ resolve_memory_cap({'spawn':{'memory_max':'6G'}}, override='none') -> None
$ cfg after override -> {'spawn': {'memory_max': '6G'}}   (unmutated)
```

Test files run: `extensions/agi/tests/test_mem_cap_override.py`,
`extensions/agi/tests/test_launch_memory_cap.py`,
`extensions/agi/tests/test_dispatch_dry_run.py`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Filled the scaffolded experiment. The build is a thin, request-scoped plumbing
change: an override parameter that wins over config but never touches disk.
The main judgement call was factoring the config normalisation into a shared
`_normalise_cap` so the override and config paths cannot drift — the falsifier
(c) is about request-scoping, and a second normalisation copy would have been
the place a write-back bug could hide. The dry-run `memory_max=` line was
placed once before the slot loop (not per slot) because it is a round-level
property and the existing report is per-slot; that keeps the observable seam
cheap and the diff small.
<!-- THOUGHT:END -->

## Agent Notes
Built + proved: mem_cap.resolve_memory_cap(cfg, override) plus dispatch.py --memory GB (dry-run prints memory_max=<cap>); override is request-scoped, no-flag path unchanged. 42 tests pass across test_mem_cap_override.py, test_launch_memory_cap.py, test_dispatch_dry_run.py; 33 production lines, ceiling 200.

PARENT REVIEW (a00-d0fdd659, EF.01), verdict ACCEPTED proved. Bytes read: mem_cap.resolve_memory_cap(cfg, override) with a shared _normalise_cap; dispatch.py --memory argparse; BOTH call sites threaded -- live dispatch.py:2663 and dry-run dispatch.py:1282; tests/test_mem_cap_override.py present. Parent probes run: (a) wire: mocked live spawn record memory_max=6G with no flag, 2G with --memory 2G; dry-run prints 2G and 1G; (b) gate: no-flag dry-run prints 6G matching config, no regression; (c) gate: .agi/config.json sha256 unchanged after --memory dry-run. All hold. Caveat: the live-record probe used a synthetic tmp project, not the real repo manifest.
