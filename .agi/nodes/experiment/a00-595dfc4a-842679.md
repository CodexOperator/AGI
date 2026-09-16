---
id: experiment:a00-595dfc4a-842679
mint_id: bb0ef41056474b269846511e0c1e9d62
type: experiment
parents:
  - hypothesis:l4-a-present-but-unreadable-nonce-ledger-is-never-read-as-empty
next_edges: []
confidence: 0.85
edited_by: a00-d1c2e7b5
evidence_runs:
  - experiment:a00-595dfc4a-842679
line_ceiling: 40
loop: hypothesis:l4-a-present-but-unreadable-nonce-ledger-is-never-read-as-empty@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probe_kidA.py (P1) -- fixture root, ring-nonces.json holds a valid prior entry then garbage; remember('NEW')", "expected": "LedgerReadError naming lpath; file byte-identical after", "observed": "raised=True file_untouched=True path_in_msg=True: 'could not read the nonce ledger at .../ring-nonces.json: Expecting property name...'", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "(P2) fixture root, valid 5-entry list + trailing NUL+marker byte; remember('n_new')", "expected": "LedgerReadError -- never a folded LedgerWriteError, never a write", "observed": "kind=LedgerReadError file_untouched=True (a folded write would have dropped the 5 entries)", "result": "refused"}
  - {"conjunct": 3, "class": "gate", "cmd": "(P3) fixture root, malformed ledger holding an admitted nonce; `'SPENT_ONE' in seen`", "expected": "LedgerReadError -- never False, which would re-admit a spent nonce", "observed": "LedgerReadError", "result": "refused"}
  - {"conjunct": 5, "class": "wire", "cmd": "(P4) fixture root with NO ledger; `'anything' in seen` then remember('first')", "expected": "absent reads empty; remember() creates the file with exactly one entry", "observed": "absent_reads_empty=True remember_created=['first']", "result": "admitted"}
  - {"conjunct": 1, "class": "gate", "cmd": "(P5, DEVIATION) fixture root whose sessions path is a regular FILE; read half and write half", "expected": "read answers empty (nothing could have been recorded) AND the write still refuses by name", "observed": "read=ANSWERED False write=LedgerWriteError -- matches pre-existing test_rings.py:874 `'n_fail' not in seen`", "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "(P6, BOUNDARY) ledger path holds valid JSON of the WRONG SHAPE (an object); read + remember", "expected": "observed boundary: it PARSES, so it is not the read-failure case; still reads []", "observed": "read=ANSWERED False and remember() overwrote it -- a separate hypothesis, recorded not claimed", "result": "admitted"}
production_lines: 35
profile: balanced
role: kid
scaffold_hash: f54f9c262cab988f
season: 2
title: "nonce ledger read: present-but-unreadable raises LedgerReadError, absent still reads empty"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-595dfc4a-842679

Slice A (conjuncts 1,2,3,5) of the parent: a PRESENT-but-unreadable nonce
ledger must never read as an empty one. BUILT, not just measured.

Production change -- `extensions/agi/src/seatsig/rings.py` only (35 added /
3 removed lines, `git diff --numstat`):

1. `LedgerReadError(Exception)` defined beside `LedgerWriteError`, same
   voice: an unreadable-but-present ledger is NOT an empty one.
2. `_ABSENT_LEDGER_ERRORS = (FileNotFoundError, NotADirectoryError)` is the
   ONE "the ledger provably cannot exist" set. `_read()` returns `[]` for
   exactly those two; ANY other exception raises `LedgerReadError` naming
   `lpath` and the underlying `exc`, `from exc`.
3. `remember()` and `_Seen.__contains__` needed NO edit: `_read()` is called
   before the write `try:` block, and `__contains__` has no try/except at
   all -- both propagate by construction. Verified by reading, then pinned
   by test.

JUDGEMENT CALL (documented): `NotADirectoryError` is folded into the ABSENT
set rather than raising. A parent path that is not a directory means the
ledger file provably cannot exist, so reading it as empty drops nothing --
and it is exactly the state the pre-existing
`test_nonce_ledger_remember_raises_when_unwritable` uses to reach the WRITE
failure. Raising there would have changed that LedgerWriteError test, which
the parent's own DISPROOF clause forbids. Non-list JSON stays `[]` for the
same minimal-scope reason (a shape miss, not a read failure) -- see caveat.

## Evidence

Baseline before the change: `test_rings.py` 42 passed.
After: `python3 -m pytest extensions/agi/tests/test_rings.py -q`
-> **48 passed** (42 + 6 new).
Callers unaffected: `test_verification.py test_write.py` -> 139 passed;
`test_dispatch.py` -> 125 passed.

FALSIFIER, run for real: I copied the fixed `rings.py` aside, patched the
two `except` arms back to the old bare `except Exception: return []`, and
reran the three new read-failure tests. On the OLD bytes:
`test_nonce_ledger_malformed_json_read_raises`,
`test_nonce_ledger_remember_unreadable_leaves_file_unchanged` and
`test_nonce_ledger_membership_on_unreadable_ledger_raises` all FAILED with
`DID NOT RAISE <class 'seatsig.rings.LedgerReadError'>` -- and the
unchanged-bytes test showed remember() had in fact overwritten the
malformed ledger (the defect). Restored from the copy, `cmp` byte-identical,
suite green again.

LIVE INVARIANT: `PYTHONPATH=src python3 -c "from seatsig import rings;
print(rings.load_rings('/home/ubuntu/work/agi/.agi'))"` -> `[]`.
No ring decision made live; every test ran on `tmp_path` fixture roots.

New tests (test_rings.py, appended): malformed-JSON read raises naming the
path; chmod-000 present ledger raises (permission bit ASSERTED to deny
first; skipped under root); a directory at the ledger path
(IsADirectoryError) raises; `remember()` on an unreadable ledger leaves the
file byte-for-byte unchanged; `nonce in seen` raises; absent-file regression
(empty read, clean create, second append drops neither).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-d1c2e7b5, SD.09). Previous version: the kid's slice-A report + its own 6 tests. This version differs because the PARENT ran its own adversarial probes and recorded them as `probes:` (6 entries, conjuncts 1/2/3/5), plus a `note` with the review. Three things the kid did not claim and the parent had to establish independently: (1) the deviation probe P5 -- the kid broadened the empty-read set to (FileNotFoundError, NotADirectoryError) against the parent brief's literal "ONLY FileNotFoundError"; I confirmed from the bytes that the pre-existing test_rings.py:863-874 walks through exactly that state and :874 requires `"n_fail" not in seen` to be False rather than raise, so the broadening is FORCED by the parent DISPROOF clause and not a lazy widening. (2) P1/P2/P3 exercised real malformed bytes rather than a stub, and P2 checked that the raise is LedgerReadError and NOT a folded LedgerWriteError -- the kid asserted only "raises LedgerReadError". (3) P6 recorded the one remaining path where a present file reads empty -- valid JSON of the wrong SHAPE -- as an observed boundary and a separate hypothesis, not as a hole in this claim. The claim is BUILD-ORDER satisfied: the fix exists in rings.py and every conjunct has a parent-run negative probe.
<!-- THOUGHT:END -->

## Agent Notes
Slice A clauses 1,2,3,5 BUILT: LedgerReadError beside LedgerWriteError in seatsig/rings.py; _read() returns [] only for the path-provably-cannot-exist set (FileNotFoundError, NotADirectoryError) and raises LedgerReadError naming lpath+exc otherwise; remember()/_Seen propagate by construction (no edit needed) and are pinned by test. 35/40 production lines. 48 passed in test_rings.py (42 baseline + 6 new); 139 passed test_verification+test_write; 125 passed test_dispatch. Falsifier run for real: reverting _read() to the bare swallow makes 3 new tests fail with DID NOT RAISE and shows remember() overwriting the malformed ledger. Live invariant rings.load_rings(/home/ubuntu/work/agi/.agi) still [].

PARENT REVIEW (a00-d1c2e7b5, SD.09): ACCEPTED, verdict proved. Bytes read, not the result file. Slice A conjuncts 1,2,3,5 built in extensions/agi/src/seatsig/rings.py only (35/-3): LedgerReadError beside LedgerWriteError; _read() returns [] for exactly _ABSENT_LEDGER_ERRORS=(FileNotFoundError, NotADirectoryError) and raises LedgerReadError naming lpath+exc otherwise; remember()/_Seen propagate by construction (no edit needed). PARENT-RUN NEGATIVE PROBES (6, fixture roots only, none live): P1 gate/conj1 real malformed ledger with a prior admitted nonce -- remember() RAISES LedgerReadError, path in message, file BYTE-IDENTICAL after (an empty read would have dropped 5 old entries). P2 gate/conj2 -- the raise is LedgerReadError, NOT a folded LedgerWriteError; file untouched. P3 gate/conj3 -- `nonce in seen` RAISES, never answers False (False would re-admit a spent nonce). P4 wire/conj5 -- absent ledger reads empty, remember() creates it, one entry. P5 gate/conj1 DEVIATION PROBE -- where the sessions dir is a regular FILE, read answers False and the WRITE still refuses by name as LedgerWriteError; this is the state the pre-existing test_nonce_ledger_remember_raises_when_unwritable (test_rings.py:863-874) walks through, and :874 requires `"n_fail" not in seen` to be False rather than raise, so broadening to NotADirectoryError is FORCED by the parent DISPROOF clause (no existing LedgerWriteError behaviour may change) and not a lazy widening. P6 recorded boundary, not a disproof. Suites: test_rings+test_write_ring_cli+test_ring_cli_seam 82 passed; test_verification+test_dispatch+test_write 264 passed. LIVE INVARIANT rings.load_rings(/home/ubuntu/work/agi/.agi) == [] and no live ring-nonces.json exists. CAVEATS: (a) a PRESENT ledger holding valid JSON of the WRONG SHAPE (an object, not a list) still reads as [] and remember() overwrites it -- my P6 shows it; it PARSES, so it is not the read-failure case this claim names, but it is the one remaining path where a present file reads empty. It is a separate hypothesis, not this round. (b) _ABSENT_LEDGER_ERRORS is broader than the target claim literally states ("FileNotFoundError -> returns []"); the broadening is mechanism-forced as shown in P5.
