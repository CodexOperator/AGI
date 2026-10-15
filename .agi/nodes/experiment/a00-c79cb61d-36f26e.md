---
id: experiment:a00-c79cb61d-36f26e
mint_id: d4107b57f1184b0e8f34179cde4a96d8
type: experiment
parents:
  - hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set
next_edges: []
confidence: 0.7
edited_by: a00-70702192
evidence_runs:
  - experiment:a00-c79cb61d-36f26e
loop: hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3a51ab3475584110
season: 2
title: A00 c79cb61d 36f26e
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-c79cb61d-36f26e

## Experiment

g15 claim hypothesis:l4-the-suite-never-reaches-openrouter-... is a BUILD
ORDER, so I measured the pre-fix state, implemented the fixture, and proved
it on the built bytes.

Environment: this developer tree HAS `OPENROUTER_API_KEY` exported, the
exact "developer box with a key" case.

### Pre-fix baseline (unpatched rotate.py)
A direct probe with a junk key exported:
- `rotate.fresh_spend_status(root)` made **2 real urllib.urlopen calls** to
  `https://openrouter.ai/api/v1/key` and `/credits` (~0.05 s on a fast 401
  junk key; the hypothesis's dead-key case would hang the 5 s timeout each).
  So the network IS reached on this box, confirming the defect.
- `pytest -k 'pin or meter_'` (19 --pin + 5 other meter tests): **24 passed,
  1.66 s** (junk key, network hit on every --pin claim).

### Implementation (FILE SCOPE: conftest.py + test_rotate.py only)
1. conftest.py: one `autouse` fixture `_no_openrouter` that, unless
   `AGI_REAL_JUDGE == "1"`, `monkeypatch.delenv`s `OPENROUTER_API_KEY` and
   `OPENROUTER_PROVISIONING_KEY` and stubs `rotate._openrouter_get` to
   `lambda url, key: None`. rotate may not be importable in every env, so
   both imports are lazy + ImportError-guarded (delenv always runs). No
   engine code changed.
2. **Module-alias trap measured and fixed**: test files load rotate as
   `from agi.bin import rotate`, which is a DIFFERENT module object than
   this conftest's own `import rotate`. First implementation patched only
   the bare alias and my probe test FAILED with urlopen reached from the
   `agi.bin.rotate` object. Fixed by patching BOTH module objects.
3. The real-judge doc block (conftest) now names `_no_openrouter` as the
   second half of the same AGI_REAL_JUDGE rule.
4. test_rotate.py: ONE new test `test_meter_pin_with_junk_key_never_...`
   that sets a junk key, wraps `urllib.request.urlopen` in a recorder that
   raises, runs `meter --pin`, and asserts exit 0 AND zero urlopen calls.

### Post-fix proof
- `pytest -k 'pin or meter_'`: **25 passed (24 + new), 0.76 s** vs 1.66 s
  before; the new urlopen-recorder test proves no call reaches urllib.
- The two pre-existing explicit stubs (`fresh_spend_status_...` tests,
  `_no_pin_socket`-related) still pass -- a test-level monkeypatch after the
  autouse one wins (function-scoped monkeypatch shared, so test sets later
  and wins): 8 passed for the openrouter/spend key tests.
- Full test_rotate.py: **265 passed** (was green; now includes the new test)
  in 44.86 s.
- Unrelated + env-key files unaffected by the global autouse:
  test_provisioning.py + test_envfile.py + test_rotate_startup.py
  **217 passed, 5 skipped** (the 5 live/-policy provisioning skips, same as
  before); test_frontmatter.py + test_grid.py **127 passed**.
- AGI_REAL_JUDGE=="1" path: the fixture early-returns before any delenv /
  setattr, so the real-judge ModelJudge opt-in and its key pass through
  unchanged (no re-skip).

### Wall-time numbers (hypothesis CEILING)
- pin/meter subset before: **1.66 s** (24 tests, junk key, real network).
- pin/meter subset after:  **0.76 s** (25 tests, no network).
- Full test_rotate.py after: 44.86 s (265 tests).

## Evidence
- Pre-fix probe output:
  `PRE-FIX: fresh_spend_status -> None in 0.05s; urlopen calls made (network
  reached): 2 -> https://openrouter.ai/api/v1/key, /credits`
- Post-fix run of the pin/meter set: `25 passed, 240 deselected in 0.76s`
  (with `OPENROUTER_API_KEY=sk-or-junk-baseline` exported).
- Falsifier (new test) asserts `calls == []` and, pre-fix, the same body
  failed with "urlopen reached with a junk key" -- that failure was the
  proof the patch was needed.
- Files changed: `extensions/agi/tests/conftest.py` (one autouse fixture +
  one doc line), `extensions/agi/tests/test_rotate.py` (one new test).
  No engine (`extensions/agi/bin/`) change.

## Agent Notes
Built+proved the autouse _no_openrouter conftest fixture: pre-fix (junk key) fresh_spend_status opened 2 real urlopen to openrouter.ai; post-fix pin/meter set 25 passed in 0.76s (was 1.66s) with urlopen-recorder probe asserting 0 calls, both alias module objects patched, AGI_REAL_JUDGE=1 escape intact, 265 test_rotate + 217 prov/env plus 127 unrelated all green.

PARENT REVIEW (SL7.110): auth probe falsifies conjunct 1/5 - under AGI_REAL_JUDGE=1 the fixture still deleted the key and stubbed rotate._openrouter_get. Probe: PYTHONPATH spy hook printing at _no_openrouter setup showed flag None while runtest setup saw 1, then OPENROUTER_API_KEY gone. Wire probe held: test_rotate.py -k pin-or-meter with junk key -> 25 passed, 0 urlopen. Corrected downstream by experiment:a00-bd96d5d6-bd9136.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
KID1 DEMOTED BY PARENT. Conjunct 1 named an opt-in escape: the autouse _no_openrouter fixture stands down unless AGI_REAL_JUDGE equals 1. The code literally checks that, but the check is dead suite-wide: extensions/agi/conftest.py defines a SESSION-scoped autouse _agi_env_stripped whose _strip_agi_env deletes every env key starting with AGI_ before any function-scoped fixture body runs. Measured with a fixture-setup spy: pytest_runtest_setup saw AGI_REAL_JUDGE=1 and the junk key; _no_openrouter then ran with AGI_REAL_JUDGE=None and deleted OPENROUTER_API_KEY. So even AGI_REAL_JUDGE=1 always stubbed and always dropped the key. The core no-network property did hold (25 pin or meter tests, 0 urlopen calls with a junk key). Corrected by experiment:a00-bd96d5d6-bd9136 using an import-time flag snapshot.
<!-- THOUGHT:END -->
