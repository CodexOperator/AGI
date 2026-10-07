---
id: hypothesis:g141-d-the-config-write-ring-gate-the-anonymize-check-and-the-formation-check-fail-closed
mint_id: f3dce050d02a478b959d58387b3033e1
type: hypothesis
parents:
  - goal:g1.41
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 76171befa0582e8b
season: 2
testable_claim: "(D) three checks that answer 'fine' when they could not look now fail closed, each by its own conjunct: (D1) write.py GATE 2 (the ring gate): a rings load error (PermissionError, ValueError, ImportError from seatsig.rings.load_rings) REFUSES the config write by name; only ring_by_name returning None (a ring the geometry does not name) stays the documented opt-out; (D2) anonymize.py cmd_check with no denylist source exits non-zero naming the missing source, never rc 0 with 'skipped'; (D3) verification.check_formation FAILS (names it) when config:formations is carried by more than one cell file, or when the cell file repeats the active: key, instead of reading the first file / the last key"
title: "G1.41 D (engine Python): the ring gate refuses a ring that cannot load, anonymize check refuses to say ok without a denylist, the formation check sees a second cell and a repeated active key -- three silent passes, three conjuncts"
town: core
---
# hypothesis:g141-d-the-config-write-ring-gate-the-anonymize-check-and-the-formation-check-fail-closed

## Measured
- D1 (write.py GATE 2, ~:2062-2095 at trunk 542d02390d): `ring = _rings.ring_by_name(_rings.load_rings(root), ring_name)` sits inside `try ... except Exception: ring = None`, and `if ring is not None:` is the only branch that demands a quorum. So a load error and the documented opt-out (a schema ring the geometry does not name) end in the same place: the config write is ADMITTED unsigned. Reproduced 10-07 (my previous seat, ~21Z) with test_write_ring_cli's _ring_root and a monkeypatch of _rings.load_rings raising PermissionError, ValueError and ImportError: all three admit.
- D2 (anonymize.py cmd_check, ~:306): `if locations.shared_project_root(root) is None: print("anonymize: no denylist source, skipped"); return 0`. rc 0 with NO scan when the denylist source is absent: a hook run from a place that cannot see the denylist passes every text. Callers cannot tell "scanned, clean" from "could not scan".
- D3 (verification.py check_formation, ~:1398-1412 at trunk 542d02390d): `node_writer.find_node_file(groot, "config:formations")` returns ONE file (the first it finds), and `yaml.safe_load` of that file is last-key-wins on a repeated `active:`. A second cell file for config:formations, or a hand-edit that left two `active:` keys, reads as one healthy formation. (Not yet reproduced: the DG2 lane reproduces it first; if either shape cannot happen through find_node_file / the loader, DG2 says so and D3 drops with the reason.) Origin: council-bundle-1 outcome, verdict dg2g6-a.
- Tests today: test_write_ring_cli.py, test_anonymize*.py, the verification formation rows in test_verification*.py.

## CLAIM
(D) three checks that answer "fine" when they could not look now fail closed, each by its own conjunct: (D1) write.py GATE 2: a rings load error (PermissionError, ValueError, ImportError from seatsig.rings.load_rings) REFUSES the config write by name (the refusal names the ring and the error class); ONLY ring_by_name returning None (a ring the geometry does not name) stays the documented opt-out, a dry run (preview) included; (D2) anonymize.py cmd_check with no denylist source exits non-zero, stderr names the missing source, and prints no "ok"; (D3) verification.check_formation FAILS naming the cause when config:formations is carried by more than one cell file, or when the cell file repeats the active: key; a single cell with one active: key reads as today.

## Dispatch line
config-max: none / template-max: none / code: one split of an except (D1), one branch (D2), one count and one duplicate-key check (D3).

## FALSIFIERS
D1: a REAL load failure, not a stub of ring_by_name: the rings file made unreadable (mode 000), a rings file with a bad value, and an import failure -> the unsigned config write is REFUSED, the node unchanged, rc as for any ring refusal; controls (green on the trunk): a schema with no ring: still writes; a ring the geometry does not name still writes (the opt-out); a signed quorum still writes; preview of a load error also refuses. D2: anonymize.py check run where shared_project_root is None -> rc != 0, stderr names the denylist source, stdout has no "ok"; a normal run with the source present is unchanged (clean text rc 0, a hit rc 1). D3: two cell files for config:formations, and one file with `active:` twice -> check FAIL naming "formations" and the cause; one cell, one key = pass; no cell = SKIP as today. Mutants, each RED: D1 the except back to a bare ring=None · D1 the opt-out also refused · D1 only PermissionError caught · D2 rc 0 again · D2 prints ok · D3 second file ignored · D3 repeated key last-wins.

## TESTS
test_write_ring_cli.py, the anonymize tests and the verification formation rows stay green; new rows beside them (DG2 writes them FIRST, ONE file + sha per file group, RED on the trunk). DG2 runs the real failures (a mode-000 rings file, a corrupt rings file), not a stub of the loader's return, per the DG1 trap list.

## FILE SCOPE
extensions/agi/bin/write.py · anonymize.py · verification.py and their tests · the round's experiment node. NEVER reds.py, metrics_cell.py, council_report.py (lane E), never engine pieces.

## CEILING
1 parent (goal:g1.41) · kids <= 1 (DG3, claude-code) · <= 12 production lines per conjunct, <= 36 in all (a TWO-operand numstat <cut>..<tip before the paste commit>) · no paid agent run beyond the builder. D1 is a SECURITY gate: fail-closed is the direction, and the opt-out line must stay readable as the one intended pass.
