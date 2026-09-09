---
id: hypothesis:l3w4-liaison-seat
mint_id: 5bec84402ac04d04aeb33a4d7cf3bc60
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: d788664b350959b3
season: 2
testable_claim: "brief.py gains a new tier, assemble(tier=\"liaison\"), that carries exactly one constitution head (reusing the director's read_order via _LIAISON_HEAD_TIER), and DUTIES naming the seat the owner's primary contact with a tier3-quorum room channel for relaying quorum questions and a write.py instruction for banking owner decisions, and states plainly that the quorum — not the seat itself — performs its rotation; the ladder's roles: table resolves a new {tier:1, role:liaison} row to model claude-sonnet-5 and effort high via load_role(); and rotate.py spawn --tier liaison --name liaison sources its successor body from that assembled brief (joined segments) rather than the static prime-director prompt file, without double-inserting the constitution head that both assemble() and the old successor_prompt() wrapper would otherwise each prepend."
thought_session: L3.21
title: Spawn the owner-liaison seat
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-liaison-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM

`rotate.py spawn --tier liaison --name liaison` launches the owner-liaison seat as a `claude --remote-control` tmux session built from a new `brief.py` tier, `liaison`: one constitution head, `claude-sonnet-5` at effort `high` from one new ladder `roles:` row, and DUTIES naming it the owner's primary contact via a `tier3-quorum` channel that relays quorum questions and banks owner decisions through `write.py` — rotated by the quorum, never itself.

WHY

Owner (2): "Add one more director-kid always on rotated by quorum that is the owner liaison so Belam is no longer my primary point of contact either but rather another director-kid answering to the quorum." Owner (3): "the owner-liaison director kid should be a sonnet model on high... liaison is under a long term goal of his own the seat system."

FILES

.agi/nodes/.geometry/ladder.md :: roles
.agi/nodes/goal/g17.md :: parent — verified active, perpetual, "The seat system"
extensions/agi/bin/brief.py :: TIERS/_ADVISOR_HEAD_TIER/assemble()/closing_line()
extensions/agi/bin/rotate.py :: cmd_spawn/_successor_command/load_role
extensions/agi/bin/adapters/claude_code_adapter.py, .agi/config.json :: effort dial low|medium|high|xhigh|max + "claude-sonnet-5" spelling (grounding)
extensions/agi/tests/test_rotate.py :: test_spawn_resolves_role_model_effort_settings (pattern)
extensions/agi/tests/test_brief.py :: test_advisor_is_a_known_tier/test_advisor_closing_line_is_distinct (pattern)

DESIGN

Ladder row via `write.py ladder:ladder "set roles <array>"` (proven JSON-list coercion): `{"tier":1,"role":"liaison","harness":"claude-code","model":"claude-sonnet-5","effort":"high","settings":""}`. `load_role()` matches by `role` name alone.

brief.py: `"liaison"` joins `TIERS`; `_LIAISON_HEAD_TIER="director"` reuses the director `read_order` (mirrors `_ADVISOR_HEAD_TIER`; no ladder edit). New `_liaison(...)` (modeled on `_director()`), three duties: sit/read room `tier3-quorum` (never Belam directly — owner 4), relaying quorum questions; bank owner decisions via `write.py <node-id> "thought <decision>"` or an `idea` node under `goal:g17` (SKILL.md ideas-as-memos); state the quorum rotates it, not itself — no self-rotate line. `assemble()` adds `if tier=="liaison"` inserting the head; `closing_line` for it: "Begin your watch as OWNER LIAISON agent {agent_id}" — no "iteration N" (a perpetual seat).

rotate.py `cmd_spawn`: when `tier!="prime_director"` and `--prompt-file` is absent, body comes from `brief.assemble(tier=args.tier,agent_id=name,iter_n=0,dispatch_py=dispatch_path)` joined — skip `brief.successor_prompt()` here, since `assemble()` already added the head and calling both doubles it. The prime's static-file path is untouched.

TESTS (red-first)

test_ladder_roles_table_has_a_liaison_row · test_liaison_is_a_known_tier · test_liaison_brief_names_owner_primary_contact_and_banking_duty · test_liaison_brief_seats_the_room_tier3_quorum · test_liaison_closing_line_has_no_iteration_language · test_spawn_tier_liaison_resolves_sonnet_high_from_the_new_row · test_spawn_liaison_prompt_has_exactly_one_constitution_head · test_spawn_prime_director_path_is_unchanged (regression)

GATE

One experiment node under this hypothesis; verdict with `evidence_runs>=1` (`--evidence-runs`); every VERIFY command's real output in the body, incl. live `rotate.py spawn --tier liaison --name liaison --dry-run` showing `--model claude-sonnet-5 --effort high` and exactly one `CONSTITUTION HEAD` marker; suite green via `commands.py run tests`. No commit/push/grid.py commit; report unexpected files, never touch them.

NOT IN SCOPE

The seat registry (session-kind/personality/handoff/rotated-by/owning-goal; config nodes) and the `send.py send --to <seat>` tmux-nudge transport — sequencing (1; `l3w4-seat-registry`/`l3w4-seat-transport`). `rotate.py loop`/alarm rotation for the liaison — sequencing (3; `l3w4-seat-rotation-loops`). Quorum-as-reviewer voting (aligned/adjust, 3-0/2-1/1-1-1) — sequencing (4; `l3w4-quorum-reviews`). Director-kid Opus rows — already built, wave 3.

SOURCE

.agi/context/l3-command-ladder-brief.md, section "Owner text 2026-09-07 (04:40–06:40 UTC, to Belam II after rotation)", owner verbatim (2) and (3); director gloss, "Sequencing," item (2).
