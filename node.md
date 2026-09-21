---
id: experiment:a00-c9653f38-22dafb
mint_id: c96d9787f091412a9b56f19d7200e5e5
type: experiment
parents:
  - hypothesis:l4-the-rows-none-committed-row-branch-and-whois-quarantine-containment-carry-committed-tests
next_edges: []
confidence: 0.9
edited_by: a00-78779a46
evidence_runs:
  - experiment:a00-c9653f38-22dafb
loop: hypothesis:l4-the-rows-none-committed-row-branch-and-whois-quarantine-containment-carry-committed-tests@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4b9908f778595184
season: 2
title: A00 c9653f38 22dafb
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c9653f38-22dafb

## Experiment

Committed three tests to `extensions/agi/tests/test_send.py` (no production
change — the code already met the claim, TESTS-FIRST carried it):

(a) `test_rows_none_committed_row_keyed_verifies_main_committed` (:5080) —
the `rows is None` positive branch: `_stub_pushed(monkeypatch, ([], ...))`
makes `_load_rows` (send.py:2332) return None, so `read` runs
`_verify_block(root, None, ...)` → `_row_for_label(root, None, "seat-a")`
(send.py:2443) falls through to `_seats_committed_rows` and returns the
committed row tagged `_main_committed`; envelope reads
`VERIFIED seat-a (ed25519, main-committed)`, never FORGED/UNVERIFIABLE.
`test_rows_none_and_no_committed_row_reads_unverifiable` (:5109) — the
sibling: rows None AND no committed row → `UNVERIFIABLE (no row: seat-a)`.
Both real-git `_git_project` fixtures. Prior tests only drove a NON-EMPTY
pushed set into this branch.

(b) `test_whois_sig_unresolvable_path_traversal_refs_write_nothing_recursive`
(:5149) — ONE integration test driving `whois --sig` with unresolvable refs
`"../../x"`, `"z\x00ploit"` (NUL byte), and `"x"*300` under
comms.verify=enforcing: each reads `UNVERIFIABLE (no row: <ref>)`, never
FORGED, never REFUSED, `rc != 2`; and a RECURSIVE before/after snapshot of
the whole `.agi/sessions` tree (`_recursive_session_snapshot`, :5130, walks
`rglob("*")` collecting path→bytes) is EMPTY — closes the SL7.14
`inbox.iterdir()` (non-recursive) gap: a file written one level down under
`inbox/quarantine/` would now be caught. All under tmp_path, live-inbox
conftest guard active.

(c) No defect exposed → no send.py edit needed.

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py test_seatsig.py
 test_sensei.py test_bin_help_smoke.py -q` → **367 passed, 3 skipped (all
pre-existing)** in 29.37s. New-tests-only run (k rows_none/traversal):
**3 passed**. Line refs measured against this checkout.

## Agent Notes
Three committed tests carry the rows-is-None branch (VERIFIED main-committed + UNVERIFIABLE sibling, both real-git) and recursive whois quarantine containment for ../, NUL, 300-char refs. 367 passed, 3 pre-existing skips; no send.py change needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-78779a46, SL7.26) — accepted, verdict proved stands.

(1) INSTRUCTION SAID (target testable_claim): "(a) a committed test where the pushed rows read None ... and MAIN's committed row is keyed: _verify_block labels the envelope VERIFIED <seat> (ed25519, main-committed) ... and the sibling case (rows None AND no committed row) reads UNVERIFIABLE (no row: <seat>); (b) ONE integration test drives whois --sig <block> with an UNRESOLVABLE ref that carries path-traversal bytes (../, NUL, a 300-char name) and ... NO file written anywhere under the quarantine dir or outside it (list the sessions tree before/after) ... (c) no production code change unless (a) or (b) exposes a defect".

(2) WHAT THE MACHINE ACTUALLY DOES (measured, not read): I read the artifact and ran it. _load_rows (extensions/agi/bin/send.py:2332) returns None on an EMPTY pushed set (the explicit `return None` after the rows truthiness test), so _stub_pushed(monkeypatch, ([], "deadbeef")) genuinely drives the rows-is-None arm of _row_for_label (send.py:2443-2470), which then returns the committed row tagged _main_committed — not a synthetic direct call. I confirmed the arm was uncovered before: every prior test stubs a NON-EMPTY pushed list (test_absent_pushed_row_verifies_main_committed:5946 stubs [{"name": "seat-other"}]; two-tree :5999; whois :6037), so the untested-arm claim is correct. I ran python3 -m pytest test_send.py test_seatsig.py test_sensei.py test_bin_help_smoke.py -q myself: 367 passed, 3 skipped, reproducing the numbers in this node exactly; the three new tests alone: 3 passed.

(3) NEAR MISS: the plausible test that satisfies the words and loses the mechanism is stubbing _pushed_seats to None directly — that fakes the sentinel instead of reaching it. The kid went through ([], sha), so _load_rows' own truthiness test produces the None and the production branch is the one under test. Same near miss on (b): an inbox.iterdir() diff (the SL7.14 shape) satisfies "no file written" while missing inbox/quarantine/<safe>.md one level down, so a writing bug would pass. The kid added _recursive_session_snapshot (rglob over the whole sessions tree, path -> bytes), which catches it; fixtures are real-git (_git_project), not mocked authority.

(4) DEVIATION: none from a standing rule. _stub_seat_rows on the whois test keeps the traversal refs unresolvable so the UNVERIFIABLE path (not FORGED) is exercised — that is the claim, not a shortcut. No send.py edit was needed and none was made; the three existing SL7.14 tests were left untouched.

CAVEAT recorded honestly: clause (c) is an ABSENCE ("no defect exposed") and is not itself falsifiable by this run; it is evidenced only by the suite staying green.
<!-- THOUGHT:END -->
