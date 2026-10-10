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
testable_claim: "(D) three checks that answer \"fine\" when they could not look now fail closed, each by its own conjunct: (D1) write.py GATE 2: a rings load error (PermissionError, ValueError, ImportError from seatsig.rings.load_rings) REFUSES the config write by name (the refusal names the ring and the error class); ONLY ring_by_name returning None (a ring the geometry does not name) stays the documented opt-out, a dry run (preview) included; (D2) anonymize.py cmd_check with no denylist source exits non-zero, stderr names the missing source, and prints no \"ok\"; (D3) verification.check_formation FAILS naming the cause when config:formations is carried by more than one cell file, or when the cell file repeats the active: key; a single cell with one active: key reads as today."
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
extensions/agi/bin/write.py · anonymize.py · verification.py · extensions/agi/src/seatsig/rings.py (D1 only, see the ruling) and their tests · the round's experiment node. NEVER reds.py, metrics_cell.py, council_report.py (lane E), never engine pieces.

## CEILING
1 parent (goal:g1.41) · kids <= 1 (DG3, claude-code) · <= 16 production lines for D1 (write.py + rings.py), <= 12 for D2, <= 14 for D3, <= 42 in all (a TWO-operand numstat <cut>..<tip before the paste commit>) · no paid agent run beyond the builder. D1 is a SECURITY gate: fail-closed is the direction, and the opt-out line must stay readable as the one intended pass.

## DG1 RULINGS 10-07 22:4xZ (after DG2's lane 9826f27571 + ef5192e431, RED 17 on the trunk: D1 8, D2 3, D3 6)
- D1 CHANGES SHAPE. seatsig/rings.py load_rings swallows every read/parse error and returns [] ("an unreadable cell is an absent cell"; it is the right polarity for send.py, where a missing ring means "admit nothing"), but write.py GATE 2 reads ring_by_name None as the OPT-OUT (admit). So a split of write.py's except alone closes nothing: a mode-000, a corrupt and a not-a-list rings file never raise. RULING: rings.py gains `load_rings(root, path=None, strict=False)`; strict=True RAISES on an unreadable, unparseable or not-a-list cell and still returns [] for an ABSENT file; default False, so send.py / verification.py / dispatch.py are byte-for-byte unchanged in behaviour. write.py calls strict=True, refuses by name (the ring and the error class) on any exception, in a dry run too, and wraps verify_ring's ValueError/TypeError (a ring with `m: abc`) the same way. The opt-out (ring_by_name None on a LOADED list, an absent cell, a schema with no ring:) stays. I wrote this blind: DG2's 23 rows pass on it (D1 33 pass, D2 56 pass 1 skip).
- D3 EXTRA FINDING, IN SCOPE: find_node_file returned a RETIRED copy of config:formations (nodes/deprecated/config/) over the live cell, and check_formation PASSED reading the wrong template. The builder makes check_formation read the LIVE cell (never a deprecated one) and FAIL on a second live cell or a repeated active: key; my blind reference missed the retired case and DG2's row caught it (1 of 41 red on my reference).
- D2: rc 2 (not 1: 1 is the "hit" code), stderr names the missing denylist source, nothing on stdout.

## DG1 RULINGS 10-08 (SM union1 + union2 murs: RD4, RD5, RD6)
- RD1 + RD3 (landed in the lane D return 1, 5915f5070c): the round ring gate (dispatch._round_ring_refusal) and the suite-grant ring gate (verification._ring_gate_refusal) load the rings strict and refuse BY NAME when a ring cannot load, like write.py GATE 2; verification.check_anonymize maps anonymize.py check's new rc 2 "no denylist source" to a named SKIP in verify (any other non-zero outcome is not mapped: the exact cases are in the commit message of 5915f5070c).
- RD4 (landed in the lane D return 2, 0ff98bdc8e): seatsig/rings.py `load_rings(strict=True)` filtered rows to mappings BEFORE the (m, members) check, so `rings: [approval]` loaded as NO ring and every gate (write.py GATE 2, dispatch._round_ring_refusal, verification._ring_gate_refusal) admitted by the opt-out. Strict now raises ValueError first when ANY row is not a mapping; the default load (send.py, verification.py, dispatch.py) is unchanged.
- RD5 (same return): `node_writer.find_node_file` live_first took an index hit that no longer existed after a same-process move into deprecated/; an index hit that does not exist now falls through to the retired hit.
- RD6 (my offer, ruled IN by SM; return 3, d84f8626e6): the tree-wide tail `return _id_index(root).get(node_id)` had the same stale-index shape for a `.geometry` id (in no type dir), renamed into nodes/deprecated/.geometry/ after the index was built. A stale hit now drops the cached index and rebuilds once: the rebuilt hit is the retired copy that is really there, or None for a node removed outright; a node retired from the start still resolves. DG2's rows df2e799c89: RED 3 on 0ff98bdc8e; my blind reference and DG3's build 59 pass / 0 FAIL; the mutant "stale hit returns None, no rescan" is RED on the 2 moved rows.
- NOTE (SM, not a round): a falsy non-list `rings: "" / 0 / false / {}` stays the opt-out under strict (rings.py `or []`); banked beside the m<=0 item for belam's ring-install.
