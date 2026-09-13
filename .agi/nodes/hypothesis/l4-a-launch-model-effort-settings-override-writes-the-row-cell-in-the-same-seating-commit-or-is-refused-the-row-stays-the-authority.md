---
id: hypothesis:l4-a-launch-model-effort-settings-override-writes-the-row-cell-in-the-same-seating-commit-or-is-refused-the-row-stays-the-authority
mint_id: 8f7ea7488d7044f0b4d821d4fe35a00a
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 77c441c5d48dad5b
season: 2
testable_claim: "goal:g15.25 SM.15 (intake: master-sensei 07:25Z: sanctuary-director 25, pid 2277285, launched claude-opus-5 by --model while its row says claude-sonnet-5 — the Prime 01:13Z boundary set directors to sonnet-5 max by ROW). MEASURED on season2/main @340d051b6: rotate-self builds the launch with `model=args.model or row.model` (rotate.py:15467; cmd_spawn :1783 the same shape; :2523 the plain launch) — the flag WINS over the row and nothing writes it back; the model-confirm poll compares the live transcript model against `row.model or args.model` (:16029 expected_model) so a flag that disagrees with the row is confirmed against the ROW and reads as a mismatch or is skipped — measure which on the 25 record; the seating row write (SL5.01) already commits session_id/generation/window/pid in one pathspec commit. CLAIM: (1) at rotate-self and cmd_spawn, when an explicit --model/--effort/--settings differs from the row cell, the launch uses the flag AND the seating row write carries the new cell(s) — same commit, and the commit message + the record name `row_override: model claude-sonnet-5 -> claude-opus-5 (flag)`; (2) `--no-row-write` (a new flag) refuses such an override by name (`--model differs from the row; pass without --no-row-write to write it, or drop the flag`) — there is no silent path; (3) a flag EQUAL to the row is a no-op (no cell write, no line); (4) the model-confirm expected_model :16029 reads the row AFTER the write (one source); (5) the bare keyed rotate verb (SL7.115) inherits — its flag-set is the same definition; TEMPLATE-FIRST note: the row stays the authority; the Prime moves models by row edits at boundaries as today. FALSIFIERS: a launch whose argv model differs from the row cell after the seating commit; a row write outside the seating commit; an override without a record line; a --dry-run that writes the row. TESTS (test_rotate.py / test_spawn_name.py <= 4, fixture row model sonnet): --model opus -> launch argv opus AND the committed row cell opus AND record row_override; --model sonnet -> no write, no line; --no-row-write --model opus -> refusal by name, nothing launched; --dry-run -> prints the would-write line, row untouched. FILE SCOPE: rotate.py (the two launch sites + the seating row write + record), the two test files. CEILING: <= 45 lines net, <= 4 tests."
title: a --model / --effort / --settings passed to rotate-self or spawn that differs from the row is written INTO the row cell in the same seating-row commit (one write, visible, named in the record) — never a silent launch that disagrees with the row (sanctuary-director 25 runs claude-opus-5 while its row says claude-sonnet-5; master-sensei 07:3xZ)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-launch-model-effort-settings-override-writes-the-row-cell-in-the-same-seating-commit-or-is-refused-the-row-stays-the-authority

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
