---
id: hypothesis:l3w4-drafter-seat
mint_id: 51ab4f2df2e44649b1c223d2b2b81f1a
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: b3e620cb1818abce
season: 2
testable_claim: A `drafter` row on the ladder's `roles:` table (claude-code, claude-sonnet-5, effort max, settings ultracode) is resolved by `dispatch.py --role drafter --ladder-tier 1` and a new `brief.py assemble(tier="drafter")`, whose DUTIES turn a `send.py send --to drafter` request into a scratch draft that a mechanical lint must clear before `write.py create hypothesis` mints it under the requester's own named parents and only the requester's own reply closes the acceptance gate, while the drafting workflow itself, `extensions/agi/workflows/draft-briefs.js`, exists as a `build` node under `goal:g17` (parents `[mvp:l3w4-draft-workflow, goal:g17]`) so any harness — claude-code Sonnet or a pi GLM drafter — can summon the same workflow by editing only that row's harness and model.
thought_session: L3.21
title: Stand up the drafter seat
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-drafter-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM: A `drafter` row on the ladder's `roles:` table (claude-code, claude-sonnet-5, max effort, settings ultracode), resolved by `dispatch.py --role drafter --ladder-tier 1` and a new `brief.py assemble(tier="drafter")`. Its DUTIES turn `send.py send --to drafter` requests into lint-checked scratch drafts, minted via `write.py create hypothesis` under the requester's own parents and accepted only by the requester's reply. The workflow itself, `extensions/agi/workflows/draft-briefs.js`, is a `build` node under `goal:g17`, summonable by any seat.

WHY: Owner (5): "...agent agnostic to where they can be flipped in and out using dispatch.py... a sonnet or glm flash latest 'drafter' that summons the drafting workflow and handles running it. Anyone needing to draft a brief goes through them." Owner (6): "switch the workflow agents to opus or fable again if needed via config update or single-run override."

FILES:
.agi/nodes/.geometry/ladder.md :: roles: — new drafter row
.agi/nodes/goal/g17.md :: parent
extensions/agi/bin/dispatch.py :: _default_tier_for_role, resolve_role_spec, --role/--dry-run
extensions/agi/bin/brief.py :: TIERS, _advisor (pattern), assemble()
extensions/agi/bin/adapters/claude_code_adapter.py :: _is_privileged_tool_seat, ULTRA_TOOLS, model_args
extensions/agi/bin/send.py :: send/read --to/--dm, rooms
extensions/agi/bin/write.py :: create()
.agi/context/schemas/[build].md :: parent_shapes ([mvp], [goal, mvp])
extensions/agi/tests/test_brief.py, test_dispatch.py, test_claude_code_adapter.py
extensions/agi/workflows/draft-briefs.js — NEW

DESIGN: Row: {tier:1, role:"drafter", harness:"claude-code", model:"claude-sonnet-5", effort:"max", settings:"ultracode"}. Two changes: `_is_privileged_tool_seat` gains `(role=="drafter" and lt==1)`, adding `Workflow` (in `ULTRA_TOOLS`) to its tools and dropping the dispatch.py deny; `settings:"ultracode"` separately opens `CLAUDE_CODE_WORKFLOWS` and the closing-turn keyword Workflow needs. Flip to pi's glm-flash-latest by editing this row (`--harness` already gives a same-run override; a dedicated `--model` flag is later, owner 6). Request: `send.py send --to drafter "<owner-text pointer> slug:<slug> parent:<id> scope:<line>"`, polled via `send.py rooms --me drafter` then `read --dm <requester>`. `brief.py` adds `"drafter"` to `TIERS` and `_drafter()` (head from the parent read-order, like `_ADVISOR_HEAD_TIER`): draft to scratch, lint, on pass `write.py create hypothesis <slug> --parent <ids>` plus a `write.py <id>` note recording the lint, then `send.py send --to <requester> "ready <id>"`. `draft-briefs.js` mints `mvp:l3w4-draft-workflow` under `goal:g17`, then `build:draft-briefs-js` with parents `[mvp:l3w4-draft-workflow, goal:g17]`. Both gates are director proposal: the lint (word cap, no ampersand-pair chains, FILES paths checked live) is the "critic pass"; the requester's own reply is "the requester reviews".

TESTS: test_brief_drafter_tier_in_TIERS (assemble raises today); test_dispatch_drafter_resolves_sonnet_ultracode (dry-run shows claude-sonnet-5/max/ultracode); test_adapter_drafter_is_privileged (tools include Workflow, drops dispatch.py deny); test_build_node_two_legal_parents ([mvp, goal] shape, refused otherwise); test_critic_lint_rejects_overlength_and_chaining.

GATE: `dispatch.py --list-rows` lists the drafter row; a dry run prints the resolved command and DUTIES; one full cycle — DM, draft, lint pass, `write.py create`, requester reply — writes no node by any path but `write.py`.

NOT IN SCOPE: the seat registry (l3w4-seat-registry); the remote-control transport (l3w4-seat-transport, not needed here); the liaison seat (l3w4-liaison-seat); quorum-as-reviewer (l3w4-quorum-reviews); telemetry seat-status, goal:g16 (l3w4-telemetry-seat-status); a richer adversarial critic or provider-agnostic override (owner 6, "later").

SOURCE: "Owner text 2026-09-07 ... perpetual seats, the quorum as reviewer, the owner liaison", quotes (5) and (6).

OWNER QUOTE (6), 2026-09-07 (verbatim in the brief doc): "Just make it easy to switch the workflow agents to opus or fable again if needed via config update or single-run override. And later make it model- and inference provider-agnostic completely." Requirement: the drafting workflow reads its model/effort from .agi/config.json workflows.drafting (landed) with a per-run override (landed); the seat design must make the drafter fully model- and inference-provider-agnostic — dispatch.py picks harness/provider/model from the seat row and the workflow script must not hardcode a vendor.
