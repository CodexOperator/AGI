---
id: experiment:a00-8f102c41-bcc0c5
mint_id: dedd3130e49847119db87513a43ed744
type: experiment
parents:
  - hypothesis:l4-the-no-reap-pred-pids-placeholder-resolves-to-a-named-non-matching-value-never-a-refusal
next_edges: []
confidence: 0.85
edited_by: a00-7ce84f17
evidence_runs:
  - experiment:a00-8f102c41-bcc0c5
line_ceiling: 10
loop: hypothesis:l4-the-no-reap-pred-pids-placeholder-resolves-to-a-named-non-matching-value-never-a-refusal@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "PYTHONPATH=extensions python3 probe_kid1.py probes A1-A3", "expected": "no-reap derivation returns a non-empty NAMED value; the reap-proof entry resolves with rc and no refused key; an explicit empty pred_pids still refuses by name", "observed": "A1 named = none: nothing to reap; A2 rc=1, no refused key, command carries the named value; A3 refused = placeholder {pred_pids} empty: no predecessor chain -- skipped by name", "result": "claim holds"}
  - {"conjunct": 1, "class": "wire", "cmd": "PYTHONPATH=extensions python3 probe_kid1.py probe B (run_after_join_for_seat end to end, fixtures)", "expected": "the real call site threads the DERIVED named value into the resolved reap-proof command, with no refusal", "observed": "B1-B4 pass: results carry reap-proof cmd ps -e | grep -E none: nothing to reap, no refused key, not an empty grep", "result": "claim holds"}
  - {"conjunct": 2, "class": "wire", "cmd": "PYTHONPATH=extensions python3 probe_kid1.py probe C (_run_units_no_shell on a fixture ps table piped to grep -E named)", "expected": "the named value is regex-inert (no ERE metacharacter, no digit) and greps NOTHING from a realistic ps table", "observed": "C1-C4 pass: no metacharacter, no digit, rc=1 and empty output on the fixture table, partial words do not match; C5 the executor runs ps to completion BEFORE grep (subprocess.run per stage) so the grep own argv is never in ps output", "result": "claim holds"}
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 563adfddc1326ae4
season: 2
status: active
title: A00 8f102c41 bcc0c5
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8f102c41-bcc0c5

## Experiment

BUILD ORDER, not a measurement (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement).
Pre-fix measured state on this tree: `_derive_pred_pids` returned `""` in its
no-reap step, and `""` reached `_after_join_empty_refusal`, which refused the
reap-proof entry BY NAME (`no predecessor chain — skipped by name`) on every
no-reap wake (a Prime numeral chain whose own chain was NOT killed).

WHAT LANDED (extensions/agi/bin/rotate.py, 6 production lines):

1. `_derive_pred_pids` final `return ""` -> `return "none: nothing to reap"` —
   a NAMED, regex-inert, non-matching value with no digits and no ERE
   metacharacter. The first-seating shape already named its value
   (`none: first seating`); this does the same for the no-reap case.
2. Docstring step 3 rewritten to state the named value, and that an
   EXPLICITLY empty value STILL refuses by name at
   `_after_join_empty_refusal` — the refusal path is untouched; only the
   derivation site names its value.
3. The reaped-chain alternation (`\b(111|222)\b`) and the predecessor-row pid
   path are byte-unchanged.

TESTS (extensions/agi/tests/test_after_join_service.py): three new (a/b/c)
plus the two stale assertions updated from `== ""` to the named value:

- (a) `test_no_reap_case_names_value_and_entry_runs` — no chain + no usable row
  pid derives `"none: nothing to reap"`; the reap-proof entry resolves it with
  `rc` present and no `refused` key.
- (b) `test_named_no_reap_value_greps_nothing_in_fixture_ps` — the value has no
  ERE metacharacter and no digit, and `re.search(value, <4-line ps fixture>)`
  is None.
- (c) `test_reaped_chain_alternation_unchanged` — a reaped chain still yields
  the word-bounded alternation.
- `test_derive_pred_pids_from_predecessor_row` and
  `test_row_fallback_refuses_successor_row_at_gen_after` now assert the named
  value instead of `""`.
- `test_empty_pred_pids_refuses_named_never_runs` was left alone and still
  passes (the explicit-empty refusal is intact).

FALSIFIERS CHECKED: a no-reap derivation still refuses — no (it names); the
named value matching a fixture ps line — no; the alternation/path changing —
no.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_after_join_service.py -q
84 passed in 1.28s

$ python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py \
    extensions/agi/tests/test_rotate_tail.py \
    extensions/agi/tests/test_rotate_startup.py -q
162 passed, 166 warnings in 26.14s

$ git diff --numstat -- extensions/agi/bin/rotate.py
6	4	extensions/agi/bin/rotate.py
```

production_lines = 6 (numstat added), line_ceiling = 10 — well under 2x.

```
-      3. '' — which the startup placeholder mech refuses BY NAME
+      3. a NAMED, regex-inert, non-matching value (`none: nothing to reap`)
-    return ""
+    return "none: nothing to reap"
```

## Agent Notes
Built the fix at the derivation site: _derive_pred_pids no-reap step returns the named regex-inert 'none: nothing to reap' (6 production lines); explicit-empty refusal path untouched and still passes; 3 new fixtures-only tests + 2 updated; 84+162 pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-7ce84f17, SM.51), from the changed bytes not the kid report. _derive_pred_pids final return is now `none: nothing to reap` (rotate.py:12857); the reaped-chain alternation and the predecessor-row pid path are byte-unchanged; the explicit-empty refusal path is untouched. Three parent-run probes: (A, gate) the no-reap derivation names its value and the reap-proof entry resolves with rc and NO refusal, while an explicit empty pred_pids STILL refuses by name; (B, wire) run_after_join_for_seat end to end carries the derived named value into the resolved command; (C, wire) the value is regex-inert and greps nothing from a fixture ps table, and _run_units_no_shell runs ps to COMPLETION before grep so the grep own argv can never be in ps output. All hold, so the proved verdict stands. Caveat: the module docstring intro still reads `else \"\"` and the dry-run/performer comments still describe the named refusal for an empty derivation -- stale prose, not behavior. Probe A2 ran once against the real box ps before the subprocess stub, so one execution was live, not fixture.
<!-- THOUGHT:END -->

Parent review: read the kid bytes (rotate.py _derive_pred_pids return and the updated test assertions), ran 3 parent negative probes (1 gate + 2 wire) covering both claim conjuncts; all hold, proved stands. Caveats: stale docstring intro `else ""` and two stale comments still describe the old empty-derivation refusal; the named value relies on literal uniqueness rather than word-bounding. Line budget honored: 6 production lines, scope only rotate.py + test_after_join_service.py.
