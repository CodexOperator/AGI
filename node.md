---
id: experiment:a00-a20108d7-70bcd0
mint_id: 17f8f212231c48f784a36af262348858
type: experiment
parents:
  - hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary
next_edges: []
confidence: 0.8
edited_by: a00-f446bb8e
evidence_runs:
  - experiment:a00-a20108d7-70bcd0
line_ceiling: 40
loop: hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"parent a00-f446bb8e, 9 negative probes on the real call site. PASS gate-A vanished staged surface -> drift refusal rc=2, stage intact, nothing renamed. PASS gate-B tracked dirt -> dirty-tree refusal naming tracked.txt, rc=2, stage intact. PASS auth-C operator --now with a live pid -> refusal by name rc=3 (the boundary unconditional apply did not leak into the operator path). PASS wire-D real cmd_rotate_self with a stage -> spawn_name=adv-new, rc_name=adv-new, stored row session_label=adv-new (the conjunct kid 1 FAILED, now closed). PASS wire-E drift at the boundary -> rc=2 and spawn_window never called. PASS gate-F fake tmux without view-old -> rc=0, zero rename-session calls, skip not red. PASS gate-G NO stage -> rc label byte-identical to the old path (rc_name=adv-alive), no regression. PASS gate-I absent old row -> _successor_row_write returns skipped and creates NO phantom new-named row. OPEN gate-J after the boundary the NEW name is NOT readable from the seats registry (_find_seat(adv-new) is None) -- the row name stays a printed ship line requiring prime/owner authority (self_row fields exclude name), a design deferral recorded not a wiring defect.\""
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 1c2f5e09c8e7d045
season: 2
title: Successor remote-control label and stored session_label carry the new name after a boundary rename
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-a20108d7-70bcd0

## Experiment

CLOSED the one conjunct kid 1 left open: after a boundary rename the
successor's app-GUI identity (`--remote-control` name) AND the stored
`session_label` cell must both carry the NEW name.

Reproduced the parent's failing probe D first: with a stage `adv-alive ->
adv-new` and a fake `spawn_window`, the pre-fix state gave `spawn_name='adv-new'`
but `rc_name='adv-alive'`, and the seats row got NO `session_label` cell at all
(the row write was SKIPPED — `_write_identity_cells` keys rows by `name == seat`
and finds no `adv-new` row).

Built the fix on `extensions/agi/bin/rotate.py` (39 added / 7 removed by
`git diff --numstat`, 5 of the added lines are code; the rest are the reasoned
comments):

1. `cmd_rotate_self`: when `_applied_rename` is truthy the `--remote-control`
   label is derived from the NEW seat (`_session_label({"name": seat, "role":
   role}, gen)`), never the stale pre-boundary `row`. No stage present -> the
   old `_session_label(row, gen)` path, byte-identical.
2. `_successor_row_write`: two new optional kwargs — `row_seat` (the applied
   rename's old name) and `session_label` (explicitly passed). The row lookup
   keys on `row_seat` and falls back through the one `aliases:` table
   (`_rename_aliases`) when the row was already renamed; `_write_identity_cells`
   targets the RESOLVED row name, so the write lands on the row that EXISTS
   instead of a phantom new-named one. An unresolved row is still the named
   `skipped: no seat-registry row ...`, never a silent old value.
3. The boundary caller passes `row_seat=old`, `session_label=_rc_label`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py
extensions/agi/tests/test_rename_post.py -q` -> 41 passed.

New test `test_rc_label_and_stored_row_cell_carry_the_new_name` drives the REAL
`cmd_rotate_self` with a stage + fake `spawn_window` and asserts:
  rc_name == "adv-new"        (the exact probe that failed)
  spawn_name == "adv-new"
  stored row (name "adv-alive") session_label == "adv-new"
  row `name` itself stays "adv-alive" (the rename round never writes config)

The pre-existing wire-proof test needed its fixture to become a REAL graph root
(`agi-tree.config.json` + `context/schemas/[config].md`), because it had been
passing vacuously on a skipped row write — the row write now actually runs, and
`write.py`'s API resolves root descend-only.

Regression neighbourhood: `test_rotate_identity_main.py`,
`test_rotate_handover.py`, `test_heal_ack_rotation.py`, `test_rotate_startup.py`
-> 178 passed; `test_rotate.py` -> 320 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 1's node documented the deviation ("the seats row still reads the OLD name
here and `--rc-label` keeps that row's label") but its tests never asserted
`rc_name`, so the gap survived a green suite. The mechanism decided here: the
row `name` is NOT renamed (the rename round prints a `ship` line, never writes
config), so the successor's identity row is the OLD-named row and the label is
passed EXPLICITLY from the boundary instead of re-derived from a row keyed on
the new name. The alias fallback covers the window where the Prime already
landed the config rename: lookup by the old name resolves old -> new through the
one `aliases:` table. `_write_identity_cells` is called with the RESOLVED row
name as both seat and actor, because admission (`self_row`) resolves the actor
against live rows and the new name has no row yet — the documented one-season
alias bridge, not a widened gate. Deviations: (a) the label is derived from
`{name, role}` rather than re-reading the row, so a row that changed role
between pre-boundary read and apply would differ — not observed; (b) `row_seat`
is passed only when `_applied_rename` is truthy, keeping the no-stage path
byte-identical. Test-first: the probe was reproduced RED before the fix, then
GREEN on the built bytes.
<!-- THOUGHT:END -->

## Agent Notes
Boundary rename now seats the successor under the NEW name on every surface: rc_name=adv-new and stored session_label=adv-new, row name left as printed ship line; probe D reproduced RED then GREEN on built bytes (41+178+320 tests pass).

Parent review a00-f446bb8e: accepted as inconclusive_lean_proved:80, confidence 0.8 (demoted from the kid proved). Bytes reviewed: git diff 8baf587d6..07dd09d42 -- rotate.py +39/-7 (_rc_label branch at 18529, _successor_row_write row_seat/session_label at 9271-9318, call-site kwargs at 18860), test +69. Probe D re-run on the real cmd_rotate_self now PASSES (rc_name=adv-new, stored session_label=adv-new) -- the exact conjunct kid 1 failed. No-stage regression probe G PASSES. Open, named: probe J, the row NAME is still not readable under the new name (prime/owner-only config write, out of the boundary authority). Verdict on the target itself remains short of proved for that reason.
