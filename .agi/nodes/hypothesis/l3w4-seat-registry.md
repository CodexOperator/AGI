---
id: hypothesis:l3w4-seat-registry
mint_id: b0465f909cfa486da1626cf343aea725
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: 4c4597b0c2997a8b
season: 2
testable_claim: A new config:seats node (.agi/nodes/.geometry/seats.md, parent goal:g17) declares one row per seat -- name, role, tier, harness, model, effort, settings, session_kind, personality_ref, handoff_file, pin_ref, rotated_by, owning_goal -- such that `dispatch.py --seat <name>` dry-prints that row's harness/model/effort/settings overriding the ladder's (tier,role) class table, and `rotate.py meter --seat <name>` reads a seat-stable `.agi/sessions/<name>.meter` pin instead of the newest-mtime one; proved by rows for belam (fable-5.1/max/ultracode), the three advisors (opus-5/max, no ultracode), liaison owning goal:g17 (sonnet-5/high), and one director per other goal_kind:perpetual goal (opus-5/high).
thought_session: L3.22
title: Register perpetual seats
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-registry

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

A new `config:seats` node (`.agi/nodes/.geometry/seats.md`, parent `goal:g17`) declares one row per seat — name, role, tier, harness, model, effort, settings, session_kind, personality_ref, handoff_file, pin_ref, rotated_by, owning_goal. `dispatch.py --seat <name>` dry-prints that row, its harness/model/effort/settings overriding the ladder's (tier,role) class table; `rotate.py meter --seat <name>` reads a seat-stable `.agi/sessions/<name>.meter` pin instead of the newest-mtime one.

## WHY

Owner (2): "create a system for storing roles and active seats... by extending our current model assignment config for dispatch... session kind like tty or fire and forget." Owner (3): liaison "under a long term goal of his own the seat system... occupies its own slot in the seats," "sonnet... high effort." Owner (4) CORRECTS (3): "quorum is opus on max, director-kids are opus on high effort. Then parents and kids as they are now."

## FILES

- `.agi/nodes/.geometry/ladder.md :: roles` (unchanged)
- `.agi/nodes/.geometry/secrets.md` :: config-type precedent
- `.agi/nodes/goal/g17.md` :: parent
- `.agi/context/schemas/[config].md :: fields` — add `seats: list`
- `.agi/nodes/.geometry/seats.md` — NEW, `config:seats`
- `extensions/agi/bin/dispatch.py :: resolve_role_spec` L295, `main()` L549 — NEW `resolve_seat_spec`, `--seat`
- `extensions/agi/bin/spawn_gate.py :: read_ladder_roles` L607 — NEW `read_seat_registry`
- `extensions/agi/bin/rotate.py :: load_role` L443, `resolve_transcript` L251 — NEW `--seat`
- `extensions/agi/bin/adapters/claude_code_adapter.py :: record_session_pin` L192 — seat-keyed `pin_key`
- `extensions/agi/tests/test_dispatch.py`, `test_rotate.py`, `test_spawn_gate.py`

## DESIGN (director proposal; model values are owner data)

Priority for `--seat NAME`: the row's own harness/model/effort/settings win over `resolve_role_spec`'s (tier,role) lookup — how liaison diverges from its class while keeping tool privilege (`_is_privileged_tool_seat` still matches `role=director, tier=1`). `pin_ref` = `.agi/sessions/<name>.meter`, written by the code that already writes `<agent_id>.meter`, keyed off `AGI_SEAT` instead — no graph write, no race on `seats.md`. Rows (owner 4 overrides 3; pi unchanged): `belam` fable-5.1/max/ultracode, tier 3, `remote-control`, `rotated_by: quorum`. Three advisors (`adv-self-perpetuating`/`adv-all-is-one`/`adv-alive`) opus-5/max/— (no ultracode), tier 3, `remote-control`, `rotated_by: prime`, `personality_ref` = the vision embodied. `dir-<goal>` opus-5/high/—, tier 1, `tty`, `rotated_by: advisor`, one per `goal_kind: perpetual` goal via `brief.py:_resolve_perpetual_goals`, except g17. `liaison` sonnet-5/high/—, tier 1, `remote-control`, `rotated_by: quorum`, `owning_goal: goal:g17` — its own slot, not a `dir-g17` row (owner 3).

## TESTS (red-first)

`test_resolve_seat_spec_liaison_returns_sonnet_high_not_opus`; `test_dispatch_seat_flag_overrides_role_and_ladder_tier`; `test_seat_pin_stable_across_two_rotations_same_name`; `test_read_seat_registry_none_when_node_absent_fails_open`; `test_list_rows_seats_prints_every_declared_row`.

## GATE

`dispatch.py --seat liaison --dry-run` prints `claude-sonnet-5`/`--effort high`, no `--settings`; `rotate.py meter --seat belam` resolves `.agi/sessions/belam.meter` over a newer foreign pin; `seats.md` has a row for `belam`, all 3 advisors, `liaison`, and one director per perpetual goal besides g17; suite green; `links.py schema` adds no new violation.

## NOT IN SCOPE

Transport switch (tmux launch, `send.py` nudge-typing) and `spawn_budget.py` charging a tty/remote-control seat's PID-liveness lease forever; the liaison's brief template and personality doc; quorum-as-reviewer, audience routing, comms restrictions (owner 4, `l3w4-quorum-reviews`); the drafter role (owner 5).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07 ... perpetual seats" — quotes (2), (3), (4) CORRECTS (3); Director gloss (proposal) for `session_kind` and `config` placement.

RE-RUN AS BUILD (Belam III, L3.22): experiment:a00-34185da7-a0d50b (lean-proved:60) validated the override-resolution mechanism with a hardcoded row and built nothing — no config:seats node, no --seat in dispatch.py or rotate.py, no seat-keyed meter pin. The next kid builds all three exactly as the CLAIM states (seats.md rows for belam, the three advisors, the liaison, one director per perpetual goal; dispatch.py --seat dry-prints the row; rotate.py meter --seat reads the seat pin) with red-first tests; verdict proved requires the dry-run output and the tests.
