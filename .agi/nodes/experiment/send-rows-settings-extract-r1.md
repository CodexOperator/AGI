---
id: experiment:send-rows-settings-extract-r1
mint_id: 9bbf6b9707d34a27b602eb8a407db195
type: experiment
parents:
  - hypothesis:a00-fd51bbd3-429f38
next_edges: []
confidence: 0.95
edited_by: a00-fd51bbd3
evidence_runs:
  - experiment:send-rows-settings-extract-r1
line_ceiling: 40
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 75
profile: balanced
role: kid
scaffold_hash: 5e3823906458b7e6
season: 2
title: "Send.py clause (1) to zero: last 3 rotate couplings moved to row_settings.py + audit FP fix"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:send-rows-settings-extract-r1

## Experiment

Third run under `goal:g7.32.4`. Kid 1 built the instrument, kid 2 moved
Block A (7 -> 3). This run (a) fixes one instrument FALSE POSITIVE and (b)
removes the LAST three `rotate` couplings from `extensions/agi/bin/send.py`,
taking clause (1), *"send.py imports no rotate/dispatch orchestration"*, from
**3 to 0**.

### 1. Instrument false positive (one-token gate fix)

`send_router_audit.py` reported `from .sub import rotate` as a coupling. That
import copies a SYMBOL named `rotate` out of module `sub`; it does not touch
the rotate module. Cause: the alias-root branch was gated
`elif child.level or not child.module:`, so EVERY relative import entered it.

**Fix:** `elif child.level or not child.module:` -> `elif not child.module:`.
The alias-root fallback now applies only when the module part is ABSENT.
`from . import rotate` still reports (module is None); `from .sub import
rotate` / `from .sub import dispatch` no longer do.

Probe on the fixed instrument (fixture: `from . import rotate`, `from .sub
import rotate`, `from .sub import dispatch`, `from .sub.rotate import x`):

```
[{'line': 1, 'function': '<module>', 'module': 'rotate', 'names': ['rotate']}]
```

Exactly one finding -- the true coupling -- down from four. Tests
`test_scanner_sees_relative_sibling_imports` now asserts the
`from .sub import rotate/dispatch` lines are NOT reported.

### 2. The move -- PREFERRED path (true decoupling, one copy each)

New **pure library** `extensions/agi/bin/row_settings.py` (54 lines, no
`__main__`, no argparse; added to `NO_HELP` in `test_bin_help_smoke.py`). It
owns, byte-for-byte from `rotate.py`:

| name | old rotate.py | new |
|---|---|---|
| `SETTINGS_ALIASES` | 140-145 | `row_settings.SETTINGS_ALIASES` |
| `_normalize_settings` | 165-190 | `row_settings.normalize_settings` |
| `DEFAULT_TMUX_SESSION` | 98 | `row_settings.DEFAULT_TMUX_SESSION` |

`rotate.py` deletes the three definitions and imports them back:

```python
from row_settings import (
    DEFAULT_TMUX_SESSION,
    SETTINGS_ALIASES,
    normalize_settings as _normalize_settings,
)
```

so every `rotate._normalize_settings` / `rotate.DEFAULT_TMUX_SESSION` /
`rotate.SETTINGS_ALIASES` reference (and `test_send_quiet.py` /
`test_send_nudge_classes.py`, which address `rotate._normalize_settings`
directly) still resolves to exactly ONE copy. `send.py` imports
`DEFAULT_TMUX_SESSION, normalize_settings` from `row_settings` and the three
lazy `import rotate` lines are gone: `_row_is_quiet` and
`_row_is_quiet_system` call `normalize_settings(...)`; `_nudge_target` uses
`DEFAULT_TMUX_SESSION`.

### 3. Clause (1) inventory BEFORE (3) -> AFTER (0)

`python3 extensions/agi/bin/send_router_audit.py` before:

```
1295	_row_is_quiet	rotate	rotate
1323	_row_is_quiet_system	rotate	rotate
1903	_nudge_target	rotate	rotate
```

After -- prints NOTHING, exit 0:

```
$ python3 extensions/agi/bin/send_router_audit.py
$ echo $?
0
```

`grep -n "import rotate" extensions/agi/bin/send.py` -> no matches.

### 4. Tests (real output)

```
$ python3 -m pytest extensions/agi/tests/test_send_router_audit.py \
    extensions/agi/tests/test_send.py extensions/agi/tests/test_send_quiet.py \
    extensions/agi/tests/test_send_nudge_classes.py -q
352 passed, 11 warnings in 833.55s (0:13:53)

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q \
    -k "settings or normalize or tmux"
4 passed, 324 deselected in 26.01s

$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
3 failed, 71 passed, 6 skipped in 379.45s
```

The 3 `test_bin_help_smoke` failures are `harness_template.py`, `ws_raw.py`,
`ws_raw_client.py` -- pre-existing (they lack `--help` handling) and
untouched by this run; `row_settings.py` is correctly skipped via NO_HELP.

### 5. Dev point of record

PREFERRED path taken, not the fallback. `rotate.py` untouched except the
move. No behaviour change: the parser and constant are the same bytes.

## Evidence

- Audit BEFORE: 3 rows (above); AFTER: 0 rows, exit 0.
- FP probe: only the true `from . import rotate` reported.
- `row_settings.py` loaded and checked: `normalize_settings("ultracode
  quiet") == {'ultracode': True, 'quiet': True}`; `DEFAULT_TMUX_SESSION ==
  'agi-rc'`; `rotate` re-exports resolve.
- Suites above: 352 passed (send + audit + quiet + nudge classes), 4 passed
  (rotate settings slice).
- Production lines (git diff --numstat, bin/ only, tests excluded): +75
  additions (row_settings 54 + rotate 6 + send 8 + audit 7), under the 2x
  ceiling (80).

## Agent Notes
Clause (1) reached: send_router_audit prints zero rows; last 3 rotate couplings (settings parser + tmux constant) moved to new pure row_settings.py and re-imported by rotate.py; audit FP gate fixed to 'not child.module'. 352 send/audit/quiet/nudge tests + 4 rotate settings tests green.
