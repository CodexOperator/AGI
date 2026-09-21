---
id: hypothesis:l3w4-seat-push-further
mint_id: 543ee356159948559515a23646e8b320
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 3b865451f76e9549
season: 2
testable_claim: "rotate.py's cmd_loop gains an optional --push-further TEXT flag plus a new _seat_job_metric(root, seat_row) that returns ('alignment_rate', aligned/(aligned+adjust)) tallied from fm.get('alignment') on this season's outcome/bigger_outcome/overview nodes whose parents directly name the seat's config:seats row owning_goal when that field is set, else ('generation', the seat's last handoff generation); given the flag, the seat's handoff is stamped push_further/job_metric and, only when owning_goal is set, write.py create idea additionally mints one idea node under it carrying the same text and metric, except when the seat is belam or its row's personality_ref is non-empty (the three advisors), in which case no idea is minted and send.py send_room posts the note to room tier3-quorum instead; and the successor inherits the note because spawn_window's existing extra parameter -- already used for the ROTATION CONTINUATION line -- gets a 'PUSH FURTHER (left by <seat>): <text> (<metric>=<value>)' line appended whenever the predecessor supplied one."
thought_session: L3.26
title: Give every seat a push-further loop
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-push-further

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`rotate.py` gains optional `--push-further TEXT` on `cmd_loop`'s successor
path, plus `_seat_job_metric(root, seat_row)`: when `owning_goal` is set,
returns `("alignment_rate", aligned/(aligned+adjust))` tallied from
`fm.get("alignment")` on this season's outcome/bigger_outcome/overview
nodes whose `parents` name that goal directly; else `("generation", <the
seat's last handoff generation>)`. Given the flag, the seat's handoff
gains `push_further`/`job_metric`; when `owning_goal` is set,
`write.py create idea` also mints under it, carrying text and metric;
when the seat is `belam`, or its row's `personality_ref` is non-empty
(the three advisors, no new field), neither happens — `send.py send_room`
posts to `tier3-quorum` instead. Generic over any `config:seats` row;
the Masters and drafter inherit it once seated. The successor inherits
it via the `extra` param `spawn_window`/`_successor_command` use for the
ROTATION CONTINUATION line: `"PUSH FURTHER (left by <seat>): <text>
(<metric>=<value>)"` appends whenever the predecessor supplied one.

## WHY

Owner (9): "all staffers and seats aim to get better and better at their
respective jobs... Improvements to standard seats are automatic, but
modifications to Belam or his advisors require owner approval." Owner
(8): "atomic, recursive, reusable" — reuses `extra` and `push_further`
from `l3w4-push-further-loops`, not a second mechanism.

## FILES

- extensions/agi/bin/rotate.py :: _successor_command L653 (`extra`),
  spawn_window L793, cmd_loop L906 — EDIT
- extensions/agi/bin/spawn_gate.py :: read_seat_registry L588 — reused
- extensions/agi/bin/season.py :: _season_nodes L641, cmd_judge
  `alignment` — reused
- extensions/agi/bin/send.py :: send_room L455 — reused
- extensions/agi/bin/write.py :: create L444 — reused
- .agi/nodes/.geometry/seats.md :: owning_goal, personality_ref, name
- .agi/context/schemas/[idea].md :: allowed_parents [goal, vision]
- extensions/agi/tests/test_rotate.py — EDIT, one new test

## DESIGN

Metric scope is first-order: a report's `parents` must name `owning_goal`
directly — deeper chains are unscoped. `alignment: unknown` counts on
neither side. No flag given leaves `cmd_loop` exactly as today — opt-in,
never forced. Mint: `write.py create idea seat-push-<name>-s<season>
--parent <owning_goal> --set authors=["<name>"] --set scale=small`, then
`write.py <id> "note <TEXT> (<metric>=<value>)"`. `personality_ref` (the
existing per-advisor vision field) is non-empty on exactly the three
advisor rows — no schema change.

## TESTS (red-first)

One: `test_push_further_banks_idea_for_goal_seat_quorum_only_for_belam` —
a fixture director row (`owning_goal: goal:g1`) with `--push-further
"widen the retry window"` calls `write.py create idea` under `goal:g1`,
never `send_room`; the fixture `belam` row, same flag, calls
`send_room(..., "tier3-quorum", ...)` and mints no idea.

## GATE

Test green. `rotate.py loop --role director --push-further "text"
--dry-run` prints the metric and, for a goal-owning seat, the `write.py
create idea` it would run; for `belam`/an advisor, the `send_room` post
instead. Suite green; no live spawn.

## NOT IN SCOPE

`rotate-self`, the handoff file, window rename/kill
(`l3w4-seat-rotation-loops`); registry rows (`l3w4-seat-registry`);
quorum vote tally (`l3w4-quorum-reviews`); the Masters' own seats
(`l3w4-sanctuary-master`, `l3w4-bug-master-seat`, `l3w4-plan-master`,
`l3w4-training-master`); seat-status render
(`l3w4-telemetry-seat-status`); the report-node chain itself
(`l3w4-push-further-loops`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07...
Masters of the Sanctuary" — owner verbatim (9), with (7)/(7b)/(8) as
prior context.

OWNER QUOTE (12), 2026-09-07 ~17:55 UTC (verbatim in doc:l3-command-ladder-brief): the Training Master of quote (9) is renamed MASTER SENSEI — the one seat looking over the Masters themselves (the Sanctuary Master included); the Sanctuary Master owns seat assignments, model selection and seat-structure changes. Read "Training Master" in this body as Master Sensei; his brief is hypothesis:l3w4-master-sensei.
