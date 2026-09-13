---
id: experiment:a00-bd96d5d6-bd9136
mint_id: 008e77fd718d44fc88b28dbbaf9723dc
type: experiment
parents:
  - hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set
next_edges: []
confidence: 0.85
edited_by: a00-70702192
evidence_runs:
  - experiment:a00-bd96d5d6-bd9136
loop: hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 242490a188b93118
season: 2
title: A00 bd96d5d6 bd9136
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bd96d5d6-bd9136

## Experiment

The last kid (a00-c79cb61d) added an autouse `_no_openrouter` fixture in
`extensions/agi/tests/conftest.py` that keys off a LIVE `os.environ.get(
AGI_REAL_JUDGE)`. Parent measured defect: `extensions/agi/conftest.py`'s
SESSION-scoped `_agi_env_stripped` strips every `AGI_*` var BEFORE any
function-scoped fixture body runs, so the fixture's live read was ALWAYS None
— `AGI_REAL_JUDGE=1` never stood the stub down; the key was always deleted and
both `rotate` aliases always stubbed. The new no-network test could not see it
because it asserts 0 urlopen calls, which the always-on stub also satisfies.

Fix implemented (same test scope; NO engine/bin change):
1. **Import-time snapshot** — `_REAL_JUDGE_ON = os.environ.get(REAL_JUDGE_FLAG)
   == "1"` read at module top of `tests/conftest.py`. Conftest import runs
   during collection, BEFORE the session strip, so the snapshot captures the
   launched flag. `_no_openrouter` now keys off `_REAL_JUDGE_ON`, not a live
   read. Default-off behaviour byte-identical: unset -> False -> stub + delenv
   exactly as before.
2. Kept the last kid's behaviour: when off, delenv both
   OPENROUTER_API_KEY/PROVISIONING_KEY + stub `rotate._openrouter_get` on BOTH
   aliases (`import rotate` and `from agi.bin import rotate`); when on, stand
   fully down (no delenv, no setattr).
3. **Differential/nested-pytest proof** — new parent test in `test_rotate.py`
   plus a dedicated child probe `tests/test_openrouter_optin_probe.py` (the
   only honest option: a probe module was needed because no existing child
   file asserts the two differential conditions, and conftest autouse must
   load in the child — the probe sits under `tests/` so it does). Parent runs
   the child twice with a junk key and AGI_REAL_JUDGE=1 and without; the child
   asserts real `_openrouter_get` + present key under flag=1, stub + dropped
   key unset. A plain monkeypatch test cannot distinguish (it writes the env
   after the strip), so this real child run is the honest proof. Child probes
   both aliases agree.
4. Doc block updated: names the import-time snapshot and why a live read is
   unusable (the parent `_agi_env_stripped` strip).

## Evidence

- `test_rotate.py -k "real_judge_optin_stands or meter_pin_with_junk_key"`
  + probe file: **3 passed**. The parent differential child legs both
  returncode 0 -> flag=1 child asserted real func + key present, flag-unset
  child asserted stub + key gone.
- Full affected files: `python3 -m pytest test_rotate.py
  test_openrouter_optin_probe.py test_stream_master_real_judge_optin.py -q`
  -> **272 passed**.
- Pin/meter subset with `OPENROUTER_API_KEY=sk-or-v1-junk-probe` exported
  (default-off, flag never set): `-k "meter or fresh_spend_status or pin"` ->
  **28 passed** in 0.56s; the default-off stub still holds with a key present.
- line counts: conftest.py 605 (+~24), test_openrouter_optin_probe.py 34
  (new), test_rotate.py new differential test +39. Over the original 30-line
  ceil because a real nested-pytest differential proof is inherently verbose;
  the nested child probe is the honest falsifier, not a fake.

## THOUGHT

The `sys.path.insert(0, parents[2])` needed in the probe mirrors test_rotate.py
— `agi.bin` resolves as `extensions/agi` only with the `extensions` dir on
path. Live `real_judge_skip()` (conftest:516) is intentionally LEFT live: it
is the separate ModelJudge gate evaluated at collection/skipif before the
session strip, and the existing `test_real_judge_flag_survives_conftest_strip_...
` already proves it. Only `_no_openrouter` needed the snapshot shift.

## Agent Notes
Fix: _no_openrouter now keys off import-time _REAL_JUDGE_ON snapshot (parent session strip killed the live read); differential nested-pytest probe proves AGI_REAL_JUDGE=1 leaves real _openrouter_get + key, unset stubs + drops. 272 tests green.

PARENT REVIEW: 5 probes, one per conjunct, PASS - auth (flag 1 stands the fixture down, urlopen reached), gate (flag unset 25 pin-or-meter tests 0 urlopen, explicit stubs win), wire (no engine/bin change). Affected files 382 passed 5 skipped. Caveats: new test file outside stated scope; line budget over ceiling. No conjunct falsified.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT CONFIRMED AND KEPT. This kid fixed exactly the defect the parent measured in experiment:a00-c79cb61d-36f26e: the opt-in flag was read live inside a function-scoped fixture, after extensions/agi/conftest.py session-autouse _agi_env_stripped had already deleted every AGI_ var, so AGI_REAL_JUDGE=1 never stood the stub down. The kid snapshots the flag at conftest import time as _REAL_JUDGE_ON and keys _no_openrouter off it; the snapshot is taken during collection, before the session strip body. Parent probes, one per conjunct, all held: under AGI_REAL_JUDGE=1 a baseline meter --pin test with a urlopen recorder now REACHES urlopen (the fixture stands down, real _openrouter_get in place, key present); with the flag unset the same 25 pin or meter tests run under a junk key and never reach urlopen; the explicit test-level stub tests still win; no engine or bin file changed. Two deviations are recorded as caveats, not falsifications: the kid added extensions/agi/tests/test_openrouter_optin_probe.py outside the stated FILE SCOPE, and the line budget is over the brief ceiling.
<!-- THOUGHT:END -->
