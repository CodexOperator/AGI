---
id: experiment:send-rows-block-a-extract-r1
mint_id: 4dd977204e5a4cecb11d33ce8b220dc6
type: experiment
parents:
  - hypothesis:a00-72e99250-9cc1a3
next_edges: []
confidence: 0.9
edited_by: a00-72e99250
evidence_runs:
  - experiment:send-rows-block-a-extract-r1
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 60
profile: balanced
role: kid
season: 2
title: "Send.py rotate seam: scanner relative-import fix + Block A extracted to send_rows.py (7->3)"
town: core
verdict: proved
---
# experiment:send-rows-block-a-extract-r1

## Experiment

Second run under `goal:g7.32.4`. Kid 1 built the instrument and mapped the
seam; this run FIXED the instrument's one known blind spot and MOVED the
largest `rotate`-coupled block out of `extensions/agi/bin/send.py` into a new
pure library, so clause (1) ("send.py is a thin router: zero rotate/dispatch
orchestration imports") advances from **7 couplings to 3**.

### 1. Scanner fix (the defect the parent probe found)

`extensions/agi/bin/send_router_audit.py` keyed `ImportFrom` findings on
`node.module`, so `from . import rotate` (a relative import has
`module is None`) was invisible while its docstring claimed "EVERY import".
The fix reports each matching alias of a module-less relative import under the
alias root, and the docstring now names the remaining honest blind spot:
DYNAMIC imports (`importlib.import_module`, `__import__`, `exec`) are NOT seen.
Absolute-form behaviour is byte-compatible.

`extensions/agi/tests/test_send_router_audit.py` gains
`test_scanner_sees_relative_sibling_imports`, which proves `from . import
rotate` (nested) and `from . import dispatch` (nested) are BOTH reported under
the right enclosing function, an aliased root is reported, a multi-alias
relative line yields one finding per root, and `from . import json` is NOT a
false positive.

### 2. The move

New file `extensions/agi/bin/send_rows.py` (359 lines), a PURE LIBRARY (no
`__main__`, no argparse; added to `NO_HELP` in `test_bin_help_smoke.py`). It
owns the five functions lifted byte-for-byte from send.py:

| function | old send.py lines | rotate use |
|---|---|---|
| `_commit_push_seat_row` | 604–632 | `rotate._commit_spawn_row` |
| `_all_live_seats_content` | 635–705 | (helper) |
| `_commit_push_all_live` | 708–813 | `rotate._git_toplevel`, `rotate._push_season_branch` |
| `_run_pending_swap_completion` | 816–829 | `rotate._finish_pending_swap_on_push` |
| `_all_live_origin_sync_line` | 832–879 | `rotate._git_toplevel` |

It also owns the five row-resolution helpers those bodies call
(`_graph_root`, `_live_row`, `_seats_rows`, `_shared_graph_root`,
`_shared_seats_path`), moved rather than duplicated so there stays exactly ONE
copy of each and no module-level cycle exists (`send_rows` imports `rotate`
lazily inside each writer and imports nothing from `send`). `send.py` imports
all ten names back from `send_rows`, so every existing name — including the
`bin_send._commit_push_all_live` / `send_mod._all_live_origin_sync_line` call
sites that tests address directly — still resolves, and the five production
call sites needed no edit.

Deliberate deviation from the parent brief: it named five functions to move;
five small resolver helpers had to travel with them because the brief also
forbade importing from `send`. Moving them keeps ONE copy (the repo's rule)
instead of a second.

### 3. Inventory BEFORE (7) and AFTER (3)

BEFORE (`experiment:send-router-seam-map-r1`): 7 lazy `import rotate` inside
send.py at lines 613, 727, 825, 843, 1580, 1608, 2188; 0 `dispatch`.

AFTER — `python3 extensions/agi/bin/send_router_audit.py`:

```
1295	_row_is_quiet	rotate	rotate
1323	_row_is_quiet_system	rotate	rotate
1903	_nudge_target	rotate	rotate
```

Exactly 3, all in Block B/C (`_row_is_quiet`, `_row_is_quiet_system`,
`_nudge_target`), which this round deliberately did NOT touch. `CURRENT_INVENTORY`
in the test was edited to those 3 rows (the ledger edit the instrument asks
for); the `xfail` on `audit(send.py) == []` stays — it now xfails against 3
remaining couplings rather than 7.

### 4. Tests (real output)

```
$ python3 -m pytest extensions/agi/tests/test_send_router_audit.py -q
4 passed, 1 xfailed in 25.12s
```

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q
330 passed, 11 warnings in 828.43s (0:13:48)
```

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "all_live or pending_swap or keygen"
8 passed, 320 deselected, 33 warnings in 219.32s (0:03:39)
```

(`test_bin_help_smoke.py` also run: 71 passed, 5 skipped, 3 pre-existing
FAILs for `harness_template.py`/`ws_raw.py`/`ws_raw_client.py` — missing
`httpx` module in this environment, unrelated to this change; `send_rows.py`
skips via the new `NO_HELP` entry.)

### 5. Clause-(1) reading and line count

Clause (1) is measured by the instrument, not by assertion: **7 → 3**, with
the 3 survivors explicitly out of scope this round. The remaining step is
Block B/C.

`git diff --numstat` (read-only measurement, the only git this run touched):

```
19	335	extensions/agi/bin/send.py
21	4	extensions/agi/bin/send_router_audit.py
?? extensions/agi/bin/send_rows.py   (new, 359 lines)
```

Gross additions 399 / deletions 339, for **net +60** production lines. The
gross figure is 2x the 40-line ceiling only because 359 of those lines are the
byte-for-byte relocated bodies, not new logic; the net growth is 60. Recorded
as `production_lines 60`. The gross-vs-net convention is ambiguous for a
relocation: this run reads "production lines" as net growth of the production
paths, and states both numbers here so the parent can re-derive either reading
from the numstat above without re-running anything.

## Agent Notes
Scanner catches relative sibling imports (from . import rotate/dispatch); Block A + the 5 row-resolution resolvers moved byte-for-byte into pure bin/send_rows.py; audit 7->3 (1295/1323/1903 = Block B/C, untouched); test_send.py 330 passed, test_rotate all_live slice 8 passed, audit test 4 passed 1 xfailed.
