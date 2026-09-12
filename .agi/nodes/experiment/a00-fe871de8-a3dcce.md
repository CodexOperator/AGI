---
id: experiment:a00-fe871de8-a3dcce
mint_id: ba4dde169d4644deaa86f8082cf6cd46
type: experiment
parents:
  - hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write
confidence: 0.9
edited_by: a00-085283ea
evidence_runs:
  - experiment:a00-fe871de8-a3dcce
scaffold_hash: 7cc167501483fbb8
title: A00 fe871de8 a3dcce
verdict: proved
---
# experiment:a00-fe871de8-a3dcce

## Experiment

Kid B on hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write, clauses (4) and (6). Built on kid A (kid-a clauses 1,2,3,5 landed in this worktree). Implemented both clauses in `extensions/agi/bin/write.py` + tests in `extensions/agi/tests/test_write_ring_cli.py`.

### Clause 4 — empty-but-declared `written_by` refuses BY NAME
`_enforce_written_by` gate 1: a declared-but-EMPTY `written_by` (`[]` or `""`) previously parsed to `admitted == set()`, so `resolved not in admitted` was always true and the final refusal read `admitted roles ;` — a misleading "as if roles were admitted" line. Added an explicit refusal after `admitted = links.parse_written_by(written_by)` / `_resolve_role(...)`:

```
if admitted is not None and not admitted:
    ... f"{node_type} nodes ({where}): the schema declares `written_by:` but
        the declared list is EMPTY, so no role may hand-edit them. (goal:g12)"
```

Refuses BEFORE the self_row / master_sensei carve-outs (an empty gate admits nobody). An ABSENT `written_by` (`admitted is None`) is unchanged — gates nothing.

### Clause 6 — `--dry-run` previews the ring/freshness refusal
The `--dry-run` branch of `main()` printed set/unset and returned 0 BEFORE `submit`/`_enforce_written_by` ran, so a write the ring would refuse printed as success. Added:

- `_preview_dry_run_gate(root, edit, args)` — after the edit is resolved, calls `_enforce_written_by(..., preview=True)` with the SAME fields as the real gate: `edit.set_fm or None`, `edit.unset_fm or None`, `allow_self_row=True`, `has_body` from apply, `signatures=args.ring_sigs`, `ring_fresh=parse_ring_fresh(args.ring_fresh)`. Prints `RING-GATE PREVIEW: <refusal>` or `RING-GATE PREVIEW: admitted (written_by + ring quorum + freshness satisfied); dry-run writes nothing`.
- `_refuse(out_decision, preview, msg)` — ONE message shared by both paths: raises `EditError(msg)` in a real gate; records `out_decision["refusal"]` and returns True in preview (caller returns). So the preview prints the EXACT text the real gate raises.
- Every gate raise site (rung-3 veto, empty written_by, master_sensei, self_row, final written_by, ring quorum, freshness) routes through `_refuse`.
- **Pure no-op**: preview passes `remember=None` so `freshness_refusal` only reads the seen set and never records the nonce; nothing written, no `edited_by` stamp.

### Live schema scan (clause 4 deliverable)
Over `.agi/context/schemas/*.md` via `load_schemas_from_dir`:

```
schema scan: 21 schemas, 4 declare written_by, 17 undeclared, 0 empty-but-declared
```

Only `[moral].md` (owner), `[config].md`, `[town].md`, `[vision].md` (owner/prime_director) declare a real `written_by`. The 17 bare `written_by:` lines parse to `None` (undeclared => gates nothing), NOT to an empty list/string. **No live schema declares an empty-but-declared `written_by`** — clause 4's new refusal is currently dead code in production but the correct behavior for a fixture/type that declares one. No schema cell was edited.

### Sanity
- `rings.load_rings('.agi')` on the live tree → `[]` (unchanged).
- No live schema edited (git status: only write.py + the test file touched by me; kid A's dispatch/verification/rings/tests changes are inherited-uncommitted).

## Evidence

Pre-fix (would-be) gate-1 message for `written_by: []` was `admitted roles ; ...` (empty admitted set). Post-fix:

```
$ REPRO (clause 4): _enforce_written_by on a fixture schema `written_by: []`
REFUSAL: config nodes (config:seats): the schema declares `written_by:` but the declared list is EMPTY, so no role may hand-edit them. (goal:g12)
```

```
$ REPRO (clause 6, --dry-run, m=2 ring, no sigs):
config:seats:
  set    seats = 'x'
  RING-GATE PREVIEW: config nodes (config:seats): record needs 2 valid ring signature(s) from 'approval' (m-of-n), got 0; <none checked>. (rung 2 multisig ring)
```

```
$ pytest test_write_ring_cli.py -k "empty or absent or dry_run or live_schema" -v
test_empty_declared_written_by_refuses_by_name PASSED
test_absent_written_by_still_gates_nothing PASSED
test_dry_run_previews_ring_refusal_naming_quorum PASSED
test_dry_run_admits_without_spending_nonce PASSED
test_dry_run_previews_freshness_refusal_for_stale PASSED
test_live_schema_scan_reports_empty_written_by PASSED
6 passed, 13 deselected
```

Full engine files I touched, clean:
```
$ pytest extensions/agi/tests/test_write_ring_cli.py test_write.py test_write_self_row.py
  test_write_guard.py test_write_master_sensei.py -q
165 passed in 3.33s
```

The `test_dry_run_admits_without_spending_nonce` proves nonce not spent: the identical dry-run a second time (same fresh fields + valid quorum) still prints ADMITTED — a spent nonce would refuse the second as `replayed nonce`.

### Agent Notes
Clauses (4) and (6) of hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write are implemented and tested. Clauses (1),(2),(3),(5) were landed by kid A (experiment:a00-9c675060-4f631e) and preserved untouched.

## Agent Notes
Clauses 4 (empty declared written_by refuses BY NAME) and 6 (--dry-run previews the ring/freshness refusal, no-op: no nonce spent, nothing written) implemented+tested; 6 new tests pass, 165 in suite

PARENT REVIEW (a00-085283ea, L4.337): ACCEPTED, verdict proved kept. Artifact read: write.py::_enforce_written_by now refuses a declared-but-empty written_by before the carve-outs (msg names the type and says the list is EMPTY); _preview_dry_run_gate() runs the SAME _enforce_written_by with preview=True, and the dry-run branch of main() returns through it (write.py:~2362). _refuse() shares one message string between raise and preview. preview forces remember=None so no nonce is spent. Re-ran the broad write/ring/dispatch/verification/veto set: 825 passed, 1 skipped. Live schema scan confirmed here: 21 schemas, 4 declare written_by, 0 empty-but-declared. CAVEATS: (a) _preview_dry_run_gate wraps the enforce call in a broad except Exception and prints the exception as a refusal, so a genuine bug in the gate would read as a preview refusal rather than a crash -- acceptable for a preview, worth tightening if a preview ever feeds a decision; (b) the empty-written_by refusal is dead code on today's live tree (no schema declares one) -- correct behavior, exercised only by fixtures. Residue left on the parent node: the nonce ledger READ half (_read() swallows read errors -> an unreadable ledger reads as empty seen, so a nonce can be replayed and remember() would then overwrite the file).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review at L4.337 read write.py and the new tests, not the kid report. Kept proved: both clauses are in the bytes and the preview is a real no-op (no write, no editor stamp, no nonce spent -- proven by the two-dry-run test). Added the caveats above: the broad except could mask a gate bug as a refusal, and clause 4 is fixture-only on the live tree.
<!-- THOUGHT:END -->
