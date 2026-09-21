---
id: experiment:a00-5c168a9b-c908a7
mint_id: 1d26bd4a6a1348b6ad8ab306728fefb0
type: experiment
parents:
  - hypothesis:l4-a-present-but-unreadable-nonce-ledger-is-never-read-as-empty
next_edges: []
confidence: 0.95
edited_by: a00-d1c2e7b5
evidence_runs:
  - experiment:a00-5c168a9b-c908a7
line_ceiling: 40
loop: hypothesis:l4-a-present-but-unreadable-nonce-ledger-is-never-read-as-empty@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 4, "class": "wire", "cmd": "(P1) probe_kidB.py -- REAL malformed ring-nonces.json + REAL quorum-valid suite-grant; verification._ring_gate_refusal(root,'approval','rotation',sigs)", "expected": "a naming refusal string naming the ledger path; never a traceback, never None", "observed": "RETURNED 'merge grant refused: could not read the nonce ledger at <tmp>/.agi/sessions/ring-nonces.json: ...'", "result": "refused"}
  - {"conjunct": 4, "class": "wire", "cmd": "(P2) same real bytes; dispatch._round_ring_refusal(root,'approval','kid','',sigs)", "expected": "a naming refusal string naming the ledger path; never a traceback", "observed": "RETURNED \"round 'approval' refused: could not read the nonce ledger at <tmp>/sessions/ring-nonces.json: ...\"", "result": "refused"}
  - {"conjunct": 4, "class": "gate", "cmd": "(P3) same real bytes; write._enforce_written_by(root,'config','director1','config:seats',role='prime',...)", "expected": "write.EditError naming the ledger; ledger file left byte-unchanged", "observed": "EditError: config nodes (config:seats): could not read the nonce ledger at <path>... | ledger_unchanged=True", "result": "refused"}
  - {"conjunct": 4, "class": "gate", "cmd": "(P4) issubclass(rings.LedgerReadError, rings.LedgerWriteError)", "expected": "False -- the old single-name catch could not have caught it, so the widened tuple is load-bearing", "observed": "False (and it IS an Exception subclass) -- combined with P1-P3 on real bytes, the old bytes traceback", "result": "refused"}
  - {"conjunct": 4, "class": "auth", "cmd": "(P5) unreadable ledger + quorum-valid grant, asking the gate to ADMIT rather than refuse", "expected": "never a silent pass: refusal fires before any admission, r is not None", "observed": "refused: merge grant refused: could not read the nonce ledger at <path>...", "result": "refused"}
production_lines: 13
profile: balanced
role: kid
scaffold_hash: 3a76115c37c0d43f
season: 2
title: All three ring gates catch the read-side LedgerReadError by name, never a traceback
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5c168a9b-c908a7

## Experiment

Slice B of `hypothesis:l4-a-present-but-unreadable-nonce-ledger-is-never-read-as-empty`
-- conjunct 4 only. Kid A landed conjuncts 1, 2, 3, 5 in
`extensions/agi/src/seatsig/rings.py` (`_ABSENT_LEDGER_ERRORS`, `LedgerReadError`,
`_read()` raising by name, `remember()`/`_Seen.__contains__` propagating).
Conjunct 4 is the three GATE call sites that caught only the write-side
failure, so a `LedgerReadError` out of `seen.__contains__` reached the user as
an unhandled traceback.

Built the fix at all three sites, keeping ONE block and the SAME message
shape; `str(le)` already names the ledger path and the underlying error, so no
second message string was invented:

```python
except (_rings.LedgerWriteError, _rings.LedgerReadError) as le:
```

| file | line | site | refusal shape |
|---|---|---|---|
| `extensions/agi/bin/verification.py` | 1235 | `_ring_gate_refusal` | `merge grant refused: {le}` |
| `extensions/agi/bin/dispatch.py` | 1441 | `_round_ring_refusal` | `round {ring_name!r} refused: {le}` |
| `extensions/agi/bin/write.py` | 1560 | `_enforce_written_by` gate 2 | `_refuse(...)` -> `EditError` |

### Why the trailing `raise  # pragma: no cover` still stays correct in write.py

Read first, not assumed. `_refuse` (`write.py:1298`) has exactly two exits:
`if preview: out_decision["refusal"] = msg; return True`, else
`raise EditError(msg)`. So inside this `except` block:

- non-preview (a real gate): `_refuse(...)` RAISES `EditError`; the `raise`
on the next line is never reached -- unreachable on that path.
- preview (a dry run): `_refuse(...)` returns `True`, the `if` body executes
`return`, and the `raise` is never reached -- unreachable on that path either.

The widened catch does not change either path: both `LedgerWriteError` and
`LedgerReadError` land in the same block and flow through the same `_refuse`.
The `raise` therefore remains dead code on both branches, and the
`# pragma: no cover` stays honest.

### Scope kept

Only the three except-clauses (plus the immediately adjacent comment that
named only the write-side error, widened so it does not lie). No other byte in
those three files. `rings.py` untouched -- kid A owns it. No existing
`LedgerWriteError` test or behaviour changed.

## Evidence

PASS -- the two moved suites (51 + 20 = 71), including the 4 new tests:

```
$ python3 -m pytest extensions/agi/tests/test_rings.py extensions/agi/tests/test_write_ring_cli.py -q
71 passed, 1 warning in 0.34s
```

PASS -- the three touched files' own suites:

```
$ python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_write.py -q
264 passed, 76 warnings in 49.52s
```

LIVE INVARIANT -- the live graph still reads as a rings list, not a read
failure:

```
$ python3 -c "import sys; sys.path.insert(0,'extensions/agi/src'); sys.path.insert(0,'extensions/agi/bin'); from seatsig import rings; print(rings.load_rings('/home/ubuntu/work/agi/.agi'))"
[]
```

### The new tests (one fixture test per call site)

Real malformed bytes, never the live ledger -- `tmp_path` only. The ledger is
written where `rings._ledger_path(root)` resolves for a fixture graph root:
`<root>/sessions/ring-nonces.json` (verified by probe before writing the test).

- `test_rings.py::test_suite_gate_unreadable_ledger_read_is_a_naming_refusal`
  -- verification.py, WIRE-LIVE: a real `{ this is not json` ledger, quorum of
  2 valid sigs, and the gate RETURNS `merge grant refused: ...` naming the
  ledger path. Hits `_Seen.__contains__` (the first raise point).
- `test_rings.py::test_suite_gate_remember_read_error_is_a_naming_refusal`
  -- verification.py, second raise point, monkeypatched `nonce_ledger` whose
  `remember` raises `LedgerReadError` while `__contains__` answers cleanly, so
  the refusal is proven for BOTH raise points and not just the first hit.
- `test_rings.py::test_dispatch_round_gate_unreadable_ledger_read_is_a_naming_refusal`
  -- dispatch.py, WIRE-LIVE: same real malformed ledger, `round 'approval'
  refused: ...` naming the path.
- `test_write_ring_cli.py::test_H4b_gate_refuses_by_name_when_ledger_present_but_unreadable`
  -- write.py, WIRE-LIVE: `pytest.raises(write.EditError)` whose message names
  `ring-nonces.json`. Placed beside its `_ring_root` / `_cell_fields` fixture
  (test_rings.py has no config-write fixture); see the caveat.

### The real falsifier (run, then restored)

Reverted ONE clause -- `verification.py:1235` back to `except
_rings.LedgerWriteError as le:` -- and re-ran the wire-live test. It failed with
the unhandled error, exactly the defect, not a refusal:

```
$ python3 -m pytest extensions/agi/tests/test_rings.py -q -k suite_gate_unreadable_ledger_read
E           seatsig.rings.LedgerReadError: could not read the nonce ledger at
/tmp/pytest-of-ubuntu/pytest-7890/test_suite_gate_unreadable_led0/.agi/sessions/ring-nonces.json:
Expecting property name enclosed in double quotes: line 1 column 3 (char 2) --
an unreadable ledger is NOT an empty one (reading it as empty would re-admit a
spent nonce and drop the entries already recorded)
1 failed, 50 deselected in 0.18s
```

Restored from a byte-exact backup; the full run above is the post-restore
result, and `verification.py:1235` reads the widened form again.

### Production lines

`git diff --numstat` over the three production paths -- added lines only:

```
6  4  extensions/agi/bin/dispatch.py
6  4  extensions/agi/bin/verification.py
1  1  extensions/agi/bin/write.py
```

13 added production lines against a ceiling of 40 -- no re-brief needed. Most
of the add is the adjacent comment, widened because it named only the
write-side error and would otherwise describe a catch it no longer makes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-d1c2e7b5, SD.09). Previous version: the kid's slice-B report + its own 3 call-site tests. This version differs because the PARENT ran its own probes and recorded them as `probes:` (5 entries, conjunct 4), plus a `note` with the review. What the parent added that the kid did not have: P4 establishes the WIDENING IS LOAD-BEARING -- LedgerReadError is not a subclass of LedgerWriteError, so the old `except _rings.LedgerWriteError as le:` could not have caught it; combined with P1/P2/P3 firing on REAL malformed ledger bytes at all three sites (not the kid's monkeypatch, which was the kid's own weakest link), the old bytes traceback there. P5 closes "never a silent pass": with an unreadable ledger the verification gate refuses rather than returning None. P2 also tightened the kid's dispatch assertion, which only checked `"refused" in refusal`, to the ledger path. The three call sites moved exactly 3 lines (one except tuple each) and nothing else in verification.py, dispatch.py or write.py; the message strings are unchanged, so the refusal shape is the same shape the existing LedgerWriteError paths already had -- which is what clause 4 asked for.
<!-- THOUGHT:END -->

## Agent Notes
Conjunct 4 built: all three ring-gate call sites (verification.py:1235, dispatch.py:1441, write.py:1560) now catch (_rings.LedgerWriteError, _rings.LedgerReadError) in one block, same message shape; write.py trailing raise read-confirmed unreachable under the widened catch. 4 new fixture tests (3 wire-live on a genuinely malformed ledger, 1 monkeypatched remember-raise) + a run falsifier reverting verification.py's clause to write-only (unhandled LedgerReadError traceback). 71 passed on test_rings+test_write_ring_cli; 264 passed on test_verification+test_dispatch+test_write; live load_rings('/home/ubuntu/work/agi/.agi') -> []. 13 production lines / 40 ceiling.

PARENT REVIEW (a00-d1c2e7b5, SD.09): ACCEPTED, verdict proved. Bytes read. Slice B conjunct 4 only: verification.py:1235, dispatch.py:1441, write.py:1560 each widened from `except _rings.LedgerWriteError as le:` to `except (_rings.LedgerWriteError, _rings.LedgerReadError) as le:`, ONE block, the SAME message string, no other byte in those three files moved. PARENT-RUN NEGATIVE PROBES (5, REAL malformed ledger bytes where the gate resolves them -- no monkeypatched nonce_ledger as primary evidence, fixture roots only): P1 wire/conj4 verification.py -- real unreadable ledger + real quorum-valid suite-grant returns RETURNED "merge grant refused: could not read the nonce ledger at <path>: Expecting property name...", naming the path; NOT a traceback, NOT None. P2 wire/conj4 dispatch.py -- same real bytes, RETURNED "round .approval. refused: could not read the nonce ledger at <path>...". P3 gate/conj4 write.py -- real bytes, raises write.EditError naming ring-nonces.json, and the ledger file is BYTE-UNCHANGED (the refused decision spends nothing). P4 gate/conj4 THE WIDENING IS LOAD-BEARING -- LedgerReadError is NOT a subclass of LedgerWriteError, so the old single-name catch could not have caught it; combined with P1-P3 firing on real bytes, the old bytes traceback here. P5 auth/wire/conj4 -- never a silent pass: with an unreadable ledger the gate refuses rather than returning None (admit). Suites: 82 passed (rings+write_ring_cli+ring_cli_seam), 264 passed (verification+dispatch+write). LIVE INVARIANT rings.load_rings(/home/ubuntu/work/agi/.agi) == []. CAVEATS: (a) the verification-site evidence goes through _ring_gate_refusal, the same helper the CLI entry calls, but a real `verification.py --level ...` process is not exercised -- a seam beyond this claim's scope; (b) the kid's own dispatch test asserted only `"refused" in refusal`, weaker than naming both ring and path -- my P2 tightened it to the ledger path, which does pass; (c) write.py keeps a trailing `raise # pragma: no cover` inside the widened block -- it is unreachable on both paths because _refuse raises EditError in a real gate and returns True in preview, so the ledger-can-not-be-read case can never escape as a traceback.
