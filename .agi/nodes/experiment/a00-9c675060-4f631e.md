---
id: experiment:a00-9c675060-4f631e
mint_id: 7ebc65b7aba74b8ba2c778ec89815c00
type: experiment
parents:
  - hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write
next_edges: []
confidence: 0.9
edited_by: a00-085283ea
evidence_runs:
  - experiment:a00-9c675060-4f631e
loop: hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3569ae4de3912801
season: 2
title: A00 9c675060 4f631e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9c675060-4f631e

## Experiment

FIX-ONLY round on `hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write` (RUNG 2b, residue c, mur-48 by name). Implemented clauses 1, 2, 3, 5(4b) of the owner's claim and proved them on the built bytes.

### What changed (pre-state measured at anchors @61311b2c2)
1. **Clause 1 (`_fresh` collision)** — `extensions/agi/bin/write.py::_config_write_fields` previously OVERWROTE a caller-supplied `_fresh` via `fresh_fields` (the docs admitted it), leaving the caller's written value uncovered by the signed bytes. Now a `set_fm` OR `unset_fm` key named `_fresh` (`seatsig.rings.FRESH_KEY`) is REFUSED **by name** with an `EditError` BEFORE `fresh_fields`, so the freshness field is never displaced and no such write is ever signed.
2. **Clause 2 (set/unset overlap)** — a key present in BOTH `set_fm` and `unset_fm` previously signed `<unset>` while the write applied the set value. Now refused **by name** (`EditError` naming the key) before signing.
3. **Clause 3 (nonce never spent silently)** — `seatsig/rings.py::nonce_ledger.remember()` ended in `except Exception: pass`, swallowing write failures (an admitted replayed record became possible after a failed ledger write). Defined `LedgerWriteError` (naming the ledger path + underlying error) and `remember()` now RAISES it. The write gate (`write.py::_enforce_written_by`) catches it and converts it to an `EditError` naming the ledger path. `dispatch.py::_round_ring_gate` and `verification.py::_ring_gate` also call `freshness_refusal(..., remember=...)` and would have leaked `LedgerWriteError` as a traceback — both touched MINIMALLY to return a by-name refusal string (`round ... refused: <le>` / `merge grant refused: <le>`).
4. **Clause 5/4b (ledger under shared sessions dir)** — `NONCE_LEDGER_FILE` was `nodes/.geometry/ring-nonces.json` (committed graph content, would churn commits once a ring is live). Now `NONCE_LEDGER_FILE = "ring-nonces.json"` (filename only), resolved at call time through `locations.shared_sessions_dir(root)` (imported lazily/defensively; falls back to `<root>/sessions` if the import fails). No migration needed: the live tree has no ledger (`rings.load_rings(live) == []`, no `.geometry/ring-nonces.json` existed).

### Reasoned deviations / notes
- `FRESH_KEY == "_fresh"` is defined identically in both `rings.py` and (pre-existing) as a literal in tests; the write.py refusal uses `_rings.FRESH_KEY` so there is no second constant to drift.
- The existing `test_fresh_fields_reserved_key_cannot_be_spoofed` (direct `fresh_fields` call) is UNAFFECTED — it tests `fresh_fields`'s overwrite behaviour, which is deliberate at that level; only the config-write REFUSAL path changed.
- `veto.py::freshness_refusal` passes no `remember`, so no ledger write and no `LedgerWriteError` can arise there — left untouched.

## Evidence

Tests added (all fail pre-fix, pass post-fix):
- `test_rings.py::test_nonce_ledger_round_trip` — UPDATED from the old path: asserts the ledger is NOT under `nodes/.geometry/ring-nonces.json` AND IS under `sessions/ring-nonces.json`.
- `test_rings.py::test_nonce_ledger_remember_raises_when_unwritable` — sessions dir is a FILE; `remember()` raises `LedgerWriteError` naming the ledger path; nonce NOT remembered.
- `test_write_ring_cli.py::test_H_fresh_key_refused_as_set_field`, `::test_H2_fresh_key_refused_as_unset_key`, `::test_H3_set_unset_overlap_refused_by_name`, `::test_H4_gate_refuses_by_name_when_ledger_unwritable`.
- `test_ring_cli_seam.py::_ledger` helper re-pointed `nodes/.geometry/ring-nonces.json` → `sessions/ring-nonces.json` (its three seam tests re-pin the new path).

Commands + results (all touched suites):
```
$ python3 -m pytest extensions/agi/tests/test_rings.py extensions/agi/tests/test_write_ring_cli.py extensions/agi/tests/test_ring_cli_seam.py -q
66 passed in 0.58s

$ python3 -m pytest extensions/agi/tests/test_rings.py extensions/agi/tests/test_write_ring_cli.py extensions/agi/tests/test_ring_cli_seam.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_verification.py -q
211 passed in 9.17s
```

Live verification: `rings.load_rings('/home/ubuntu/work/agi/.agi') == []` (unchanged, no live ring); no `.geometry/ring-nonces.json` nor `sessions/ring-nonces.json` in the real graph; NO schema cell edited.

## Notes

`test_H4` monkeypatches `rings.nonce_ledger` to a remember that raises `LedgerWriteError`, then drives `_enforce_written_by` with real valid fixture signatures (`ring_fresh` pinned) and asserts the resulting `EditError` names the nonce ledger path.

## Agent Notes
RUNG2b clauses 1,2,3,4b: refuse _fresh colliding key + set/unset overlap by name; nonce_ledger.remember raises LedgerWriteError; gate + dispatch + verification refuse by name; ledger moved to shared_sessions_dir. 66+211 tests green; live tree clean (load_rings==[], no ledger created).

PARENT REVIEW (a00-085283ea, L4.337): ACCEPTED, verdict proved kept. Artifact read, not the report: write.py::_config_write_fields now refuses _fresh as a set key (L1131) and an unset key (L1167), and a set/unset overlap (L1141), all before fresh_fields signs; rings.py::LedgerWriteError raised from remember() (L511) with write/dispatch/verification converting it to a by-name refusal; ledger resolved via _ledger_path() through locations.shared_sessions_dir (L457). Re-ran 211 tests green in the worktree. Every claim in the node is true of the bytes. CAVEAT left for the round: nonce_ledger._read() still swallows read errors and returns [] -- an unreadable ledger reads as no nonces seen, so a previously-admitted nonce can be re-admitted (and remember would then overwrite the file, dropping the old entries). Clause 3 covered the WRITE half only; the READ half is a replay hole the next round should name.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review at L4.337 read the artifacts (rings.py, write.py, the five touched suites) rather than the kid report. Kept proved: each of clauses 1,2,3,5 is implemented in bytes and pinned by a test that fails pre-fix. Added the parent note above with one caveat the kid did not name: _read() swallows ledger read errors, so the read half of the nonce ledger is still replay-prone.
<!-- THOUGHT:END -->
