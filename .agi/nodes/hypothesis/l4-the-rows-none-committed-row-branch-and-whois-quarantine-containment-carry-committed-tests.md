---
id: hypothesis:l4-the-rows-none-committed-row-branch-and-whois-quarantine-containment-carry-committed-tests
mint_id: 5e5732ff0896473cbf196d9bd1b4b941
type: hypothesis
parents:
  - goal:g15.26
  - hypothesis:l4-an-absent-pushed-row-reads-unverifiable-never-forged-whois-sig-gets-the-seam-and-all-live-stages-only-the-keyed-rows
next_edges: []
edited_by: sensei-director
scaffold_hash: 7c48b7c2a3d4e5d5
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node, mur-SL2.16 (Prime XV 08:06Z, by name) line (5) — SL7.14 residue. Cite lines at 2451606d0; re-measure on your base. MEASURED: `_row_for_label` (send.py 2404-2440): the `rows is None` (pushed set unreadable) + committed-row-present branch (2422-2432) — the case where origin cannot be read at all but MAIN's committed seats.md carries the keyed row — has NO committed test (SL7.14's two-tree test uses a non-empty pushed set); and the quarantine containment of an unresolvable `--sig` ref is exercised ONLY by the unit test `test_sanitize_ref_accepts_and_refuses_bounds`, never through `whois` (SL7.14 rewrote the three SL7.02 quarantine tests to assert UNVERIFIABLE with resolvable refs). CLAIM: (a) a committed test where the pushed rows read `None` (a fixture whose origin ref is absent / `_pushed_rows` returns None) and MAIN's committed row is keyed: `_verify_block` labels the envelope `VERIFIED <seat> (ed25519, main-committed)` — never FORGED, never UNVERIFIABLE; and the sibling case (rows None AND no committed row) reads `UNVERIFIABLE (no row: <seat>)`; (b) ONE integration test drives `whois --sig <block>` with an UNRESOLVABLE ref that carries path-traversal bytes (`../`, NUL, a 300-char name) and asserts: UNVERIFIABLE printed, NO file written anywhere under the quarantine dir or outside it (list the sessions tree before/after), exit code as SL7.02 specifies; (c) no production code change unless (a) or (b) exposes a defect — then record the measured line and fix it in the same round, naming it in the node. FALSIFIERS: the rows-None + committed branch reads FORGED or UNVERIFIABLE; a traversal ref writes a file; any existing send/seatsig test changes assertion. TESTS: test_send.py test_seatsig.py test_sensei.py test_bin_help_smoke.py with neighbours; every path under tmp_path with the conftest live-inbox guard active. RULES: merge, never rebase; TESTS-FIRST — production edits only for a defect the new tests expose. FILE SCOPE: tests (test_send.py or a new test module); send.py `_row_for_label`/`_verify_block`/`_quarantine_whois` ONLY on an exposed defect. EXCLUDED: rotate.py, heal.py, the signer preference (SL7.22 landed), hooks. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: the rows-None + committed-row branch of _row_for_label and the whois --sig quarantine containment of an unresolvable traversal ref carry committed tests
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-rows-none-committed-row-branch-and-whois-quarantine-containment-carry-committed-tests

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
