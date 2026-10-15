---
id: experiment:a00-1a213326-063f90
mint_id: c95cc9c63c304ef1ab25017be0204ea8
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.9
edited_by: a00-efb7f2a8
evidence_runs:
  - experiment:a00-1a213326-063f90
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: stealth/space-bunny-alpha
production_lines: 26
profile: balanced
role: kid
scaffold_hash: d3d38bd684bff91a
season: 2
title: A foreign row is refused once per row and cause, and never typed into
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1a213326-063f90

## Claim (3) — built, not measured

The foreign-row refusal in `extensions/agi/bin/send.py::_nudge_target`:

| clause | meaning | where |
|---|---|---|
| (3a) | said ONCE per (row, cause) — a second sweep over the same foreign row is silent | module memo `_FOREIGN_REFUSALS` |
| (3b) | it NAMES the box: the row's own `box` cell, `(unset)` when it has none | unchanged string |
| (3c) | NO send-keys ever reaches that row's window | `return None` (unchanged), proven with a fake tmux that raises on `send-keys` |

## The design, and the near-miss it is built against

```
sweep 1  far-seat box=sanctuary   -> print "FOREIGN box row (box sanctuary)"   memo {far-seat,sanctuary}
sweep 2  far-seat box=sanctuary   -> SILENT (same row, same cause)
sweep 3  far-seat box=local-town  -> addressable, so the memo FORGETS far-seat
sweep 4  far-seat box=sanctuary   -> named AGAIN (a clean sweep is a new cause)
sweep 5  far-seat box=streaming-suite -> named AGAIN with the new label
```

Keying the memo on the ROW ALONE gives sweep 2 (the ask) but SILENCES sweeps 4
and 5 — a genuine change of cause swallowed. The key is therefore
`(row, cause)` where cause is the box label, and `_nudge_target` forgets a row's
entries the moment that row is addressable again. `_forget_refusals(to=None)`
clears the whole memo (used by tests, and available to a `rotate` sweep).

Production cost: `git diff --numstat` over the production paths in scope
= `30 4 extensions/agi/bin/send.py` — 26 added lines net, of which 8 are the
memo helper and 2 the docstring that names the hypothesis. Under the 40-line
ceiling for this round.

## Falsifiers run (CLAIM, not evidence — these are the tests that had to fail first)

All in `extensions/agi/tests/test_box_identity.py`; temp graphs, monkeypatched
`AGI_BOX`, a FAKE tmux runner only (`_FakeTmux` raises `AssertionError` on any
`send-keys` argv and records every call).

| # | test | fails on |
|---|---|---|
| 4 | `test_falsifier_two_sweeps_print_the_refusal_once` | pre-fix bytes (2 lines, not 1) |
| — | `test_falsifier_refusal_names_an_unset_box_as_unset` | a dropped `(unset)` label |
| 5 | `test_falsifier_cause_change_on_one_row_is_named_again` | a memo that never forgets |
| 6 | `test_falsifier_two_foreign_causes_on_one_row_both_named` | a memo keyed on the ROW ALONE |
| — | `test_falsifier_no_send_keys_reaches_the_foreign_window` | any key typed at `@9` (3c) |

### Commands and actual output

```
# pre-fix bytes (memo condition removed) -- falsifier 4 fires, the rest hold
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_box_identity.py -q
FAILED test_falsifier_two_sweeps_print_the_refusal_once
1 failed, 16 passed

# the near-miss: memo keyed on the row alone -- falsifier 6 fires
FAILED test_falsifier_two_foreign_causes_on_one_row_both_named
1 failed, 16 passed

# as landed
$ ... test_box_identity.py -q            -> 17 passed
$ ... test_send.py test_seatsig.py test_heal.py test_bin_help_smoke.py \
         test_write_self_row.py -q       -> 449 passed, 6 skipped
```

## Reported, not fixed (outside my file scope)

`extensions/agi/tests/test_box_guard.py::test_no_box_cell_is_default_box_and_local`
and `::test_this_box_reads_agi_box_env` fail on arrival (2 failed, 4 passed) —
they pin the `default_box` fallback kid A removed. Out of scope for me; the
director owns the decision to re-pin or retire them.

## Caveats I would flag

- The memo is process-local and unbounded in principle. It is drained for every
  row that becomes addressable, so a permanently-foreign row set is bounded by
  the row set; a row that is foreign and never swept again is one small set
  entry. Acceptable, not free.
- A row that changes box WITHOUT an intervening addressable sweep is still
  silent under the old cause label... except it is not: the label is part of the
  key, so a new label prints. The only silent case is the same label repeated,
  which is the ask.

## Agent Notes
foreign-row refusal now memoised per (row, box label) and a row that becomes addressable forgets itself, so a second sweep is silent while a genuine cause change is named again; fake-tmux proves no send-keys reaches the foreign window

PARENT REVIEW (a00-efb7f2a8, DH.498) — the DIFF holds and three parent probes pass; verdict `proved` STANDS for conjunct (3) alone, not for the whole hypothesis.

BYTES, not the report: `send.py:2176 _FOREIGN_REFUSALS: set[tuple[str,str]]`, `send.py:2179 _forget_refusals(to=None)`, and the refusal block at :2212-2224 — the print is now inside `if (to, label) not in _FOREIGN_REFUSALS:`, the tuple is added, and the `return None` is UNCHANGED. The forget call sits at :2229-2230, on the addressable path. Two files moved in the whole round (send.py, test_box_identity.py) plus the two experiment nodes — nothing outside the director FILE SCOPE, verified by mtime sweep, not by reading the report.

probes (run by the parent, script at .agi/sessions/iter-DH.498/a00-efb7f2a8/parent_probes_b.py — drives the REAL _nudge_target with a fake tmux runner that records every argv, temp graphs, never the live pane):
- P1 GATE: sweep 1 over a foreign row returns None and prints `nudge: director-belam is a FOREIGN box row (box sanctuary); refusing as a target`; sweep 2 over the SAME row and cause is SILENT. ONCE per row+cause holds.
- P2 WIRE: the fake runner argv log is EMPTY across both foreign sweeps — not one `send-keys` argv was constructed, so (3c) is a measured absence, not an inference from the return value.
- P3 AUTH (wrong-state): a LOCAL row on this box still resolves `agi-fake:@9` and still gets its keys — the memo does not swallow a legitimate delivery. A CHANGE of box on one row (sanctuary -> core-town) is named AGAIN. A row that went local and then foreign again is named AGAIN. A boxless row is refused naming `(unset)` with no send-keys.
All three classes pass. My first run showed P3a failing; that was a defect in MY fake (it listed only @7, so the pre-existing stale-@id repair path fired), not in the kid — the probe was corrected and re-run. Recording that because a probe that fails for its own reason is worth a turn for whoever reads this next.

CAVEAT I accept, named rather than dropped: `_FOREIGN_REFUSALS` is process-local and never expires on its own. It is drained whenever a row becomes addressable, so the steady-state size is bounded by the permanently-foreign row set — acceptable here, but a long-lived box cron that never makes a row addressable again would carry those entries for the life of the process. A future round may want a sweep to drain it.

STILL OPEN AT THE HYPOTHESIS (not this kid): `extensions/agi/tests/test_box_guard.py::test_no_box_cell_is_default_box_and_local` and `::test_this_box_reads_agi_box_env` remain RED — they pin the `default_box` fallback conjunct (2) removes, and that file is outside the director FILE SCOPE for this round. The tree is red until a round is granted test scope. Nothing about that residue is this kid fault: it was already red when it started and it reported it rather than reaching outside its scope.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, first version: accepted on the diff and on three parent-run probes, not on the kid own 17 tests. (1) What the instruction said: read the changed bytes, a kid suite is its CLAIM, and one negative probe per conjunct run by me. (2) What the machine does: the refusal print at send.py:2212-2224 is now guarded by a module-level (row, box-label) memo, and the `return None` — the whole of (3c) — is byte-identical to before, so the once-only memo could not have opened a send-keys path; the fake-runner argv log in P2 is empty, which is the measurement that says so. (3) The near miss this review had to refuse: a memo keyed on the row NAME alone satisfies "once per row" and silences a genuine change of cause forever — the kid built against that and my P3b is the independent kill shot for it. The second near miss: a memo so eager to re-print that it re-prints every sweep, which is the original belam complaint wearing a new hat; P1 sweep 2 is what catches it. (4) Deviation from a standing rule: I did not demote `proved` to a lean. A tier-parent is told to demote overclaims, but this kid cited real evidence_runs, the diff is inside scope, and the three probe classes all pass on the real function — so the honest verdict for conjunct (3) is proved. It is proved for conjunct (3) ONLY: conjuncts (1) and (2) carry kid A lean_proved:85, and the hypothesis as a whole is not proved while two legacy tests still pin the contract it removes.
<!-- THOUGHT:END -->
