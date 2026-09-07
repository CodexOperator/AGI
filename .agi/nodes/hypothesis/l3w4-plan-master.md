---
id: hypothesis:l3w4-plan-master
mint_id: 8dbdfa576c384be28d07f9ef98a58153
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: e5c23e9229f75373
season: 2
testable_claim: "config:seats gains a plan-master row (director, tier 1, claude-opus-5, effort high, settings ultracode, rotated_by: sanctuary-master, owning_goal: goal:g17) that dispatch.py --seat plan-master --role director --ladder-tier 1 --dry-run resolves to opus-5/high with CLAUDE_CODE_WORKFLOWS=1 exported and Workflow in --tools; the plan-master seat supersedes hypothesis:l3w4-drafter-seat's seat by answering the identical send.py send --to <name> request shape and two-stage acceptance gate (the workflow's critic pass, then the requester's own reply) under the name plan-master instead of drafter; its summon/accept cycle calls the unedited extensions/agi/workflows/agi-brief-drafting.js and mints via write.py create hypothesis only the slugs absent from the returned critic.left; and new plan_master.py record-run appends one {ts,iter,n_drafts,n_fixed,fixes_per_draft} line per summon to a seat-local log that plan_master.py trend --last N reads back to report whether fixes_per_draft is rising, falling, or flat."
thought_session: L3.26
title: Stand up the Plan Master seat
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-plan-master

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`config:seats` gains a `plan-master` row (director, tier 1, opus-5, high, ultracode, `rotated_by: sanctuary-master`, `owning_goal: goal:g17`), resolved by `dispatch.py --seat plan-master --role director --ladder-tier 1`. It supersedes `l3w4-drafter-seat`'s seat — same request (`send.py send --to plan-master`) and gate (workflow critic, then requester reply). It summons `agi-brief-drafting.js` unedited, mints only the slugs the critic clears, and reports back to the asker. `plan_master.py record-run` logs `fixes_per_draft` per summon — its push-further loop.

## WHY

Owner (9): "brief drafting needs to happen through the Plan Master"; "...any workflow becomes config-maxxed, harness-agnostic, with its own Master in the Sanctuary under SM... Masters report back to the asker"; "...seats aim to get better... at their jobs." Owner (5): "...a sonnet or glm flash latest 'drafter' that summons the drafting workflow... anyone needing to draft a brief goes through them" — seat replaced. Owner (4): "director-kids are opus on high effort" sets the row.

## FILES

- .agi/nodes/.geometry/seats.md :: seats — EDIT
- .agi/nodes/goal/g17.md — parent
- extensions/agi/workflows/agi-brief-drafting.js :: DRAFT_SCHEMA, CRITIC_SCHEMA (l3w4-workflows-config-maxxed owns it)
- .agi/config.json :: workflows.drafting
- extensions/agi/bin/dispatch.py :: resolve_seat_spec, --seat
- extensions/agi/bin/adapters/claude_code_adapter.py :: _is_privileged_tool_seat
- extensions/agi/bin/send.py :: send --to, read/rooms --me/--dm
- extensions/agi/bin/write.py :: create
- extensions/agi/bin/plan_master.py — NEW
- extensions/agi/tests/test_plan_master.py — NEW

## DESIGN

Row: `{"name":"plan-master","role":"director","tier":1,"harness":"claude-code","model":"claude-opus-5","effort":"high","settings":"ultracode","session_kind":"tty","personality_ref":"","handoff_file":"","pin_ref":".agi/sessions/plan-master.meter","rotated_by":"sanctuary-master","owning_goal":"goal:g17"}`. `ultracode` exports the Workflow-tool env; `role=director,tier=1` earns `Workflow` via `_is_privileged_tool_seat` — no adapter edit; editing `harness`/`model` flips the seat (owner 6).

Request: `send.py send --to plan-master --from <requester> "<pointer> slug:<slug> parent:<id> scope:<line>"`, polled via `rooms --me plan-master` then `read --dm <requester> --me plan-master`.

`plan_master.py summon` calls `Workflow({name:"agi-brief-drafting", args:{briefs:[{slug,parent,scope}], model, effort}})` on claude-code, or `workflow.py run drafting --harness pi` off it. `plan_master.py accept --iter I`: a draft not in `critic.left` gets `write.py create hypothesis <slug> --parent <ids> --payload <body_path>` then `"ready <id>"` DM'd back; one still `left` gets `"blocked <slug>"`, never minted; the requester's reply alone closes the loop (`l3w4-drafter-seat`).

`plan_master.py record-run`, after `accept`: `fixes_per_draft = len(critic.fixed)/len(drafts)`, appends one JSON line to `.agi/sessions/plan-master/pushfurther.jsonl` (seat-local); `trend --last N` prints rising/falling/flat.

## TESTS

One, red-first: `test_record_run_then_trend_classifies_falling_fixes_per_draft` — three fixture runs, `fixed` lengths 4, 3, 1 over 2 drafts each write 2.0, 1.5, 0.5; `trend --last 3` reports falling.

## GATE

`dispatch.py --seat plan-master --tier director --role director --ladder-tier 1 --dry-run` prints opus-5/high, `CLAUDE_CODE_WORKFLOWS=1` exported, `Workflow` in `--tools`; TESTS passes; `seats.md` carries the row; suite green, no live spawn.

## NOT IN SCOPE

`agi-brief-drafting.js` internals (`l3w4-workflows-config-maxxed`); Master-to-director-kid consult and the owner escalation ladder (`l3w4-masters-comms-and-escalation`); the every-seat push-further mechanism (`l3w4-seat-push-further` — this is only Plan Master's instance); Sanctuary Master's row and rotation (`l3w4-sanctuary-master`); rotation-loop alarms (`l3w4-seat-rotation-loops`); tmux transport (`l3w4-seat-transport`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, the 2026-09-07 owner section — verbatim (9), the Masters layer naming the Plan Master; (5)/(6), the seat superseded; (4), the director-kid model row. `HANDOFF.md` §6 item 24.
