---
id: hypothesis:l3w4-bug-master-seat
mint_id: e2eea49560724e84b816faaa9ef81732
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 6d45c0c92be55616
season: 2
testable_claim: dispatch.py --seat bug-master --tier director --role director --ladder-tier 1 --dry-run resolves claude-opus-5 at effort xhigh with CLAUDE_CODE_WORKFLOWS=1 exported and Workflow present in --tools, and new bug_master.py format-record, given agi-round-review.js's returned JSON for N targets plus one global check, writes that JSON verbatim to .agi/sessions/iter-<id>/review/results.json and prints exactly N REVIEW lines plus one GLOBAL line shaped for send.py send --room tier3-quorum.
thought_session: L3.27
title: Seat the Glitch Master reviewer
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-bug-master-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`config:seats` gains one row, `bug-master` (director, tier 1, claude-code, opus-5, xhigh), rotated by the not-yet-seated Sanctuary Master. A round-landing DM `send.py send --to bug-master '{"iter":I,"targets":[{"hyp":H,"window":W}]}'` wakes it; it runs `agi-round-review.js`, turns the JSON into one REVIEW line per target plus one GLOBAL line via new `bug_master.py format-record`, posted to `tier3-quorum`.

## WHY

Owner (7): "Just create a seat for a 'reviewer' on opus xhigh that runs a bunch of sonnet max minion seats, and they get called anytime it's time to review." Owner (7b): "...the Bug Master who does the ephemeral review parent/kid minion coordination" (ephemeral — minions get no seat rows) and "Sanctuary Master...takes care of rotating...the Bug Master" (`rotated_by`). `idea:push-further`: "runs the review minions on every landing" — the trigger this brief designs.

## FILES

- extensions/agi/workflows/agi-round-review.js :: TARGET_SCHEMA, GLOBAL_SCHEMA — prototype, untouched
- .agi/nodes/.geometry/seats.md :: seats — NEW row bug-master
- extensions/agi/bin/dispatch.py :: resolve_seat_spec L340, --seat L597
- extensions/agi/bin/adapters/claude_code_adapter.py :: _is_privileged_tool_seat L420, ULTRA_TOOLS L114, _tier_is_ultracode L320
- extensions/agi/bin/spawn_gate.py :: read_seat_registry L588
- extensions/agi/bin/send.py :: send_dm L441, send_room L455
- .agi/config.json :: workflows.review — NEW (l3w4-workflows-config-maxxed)
- extensions/agi/briefs/bug-master-duties.md, extensions/agi/bin/bug_master.py, extensions/agi/tests/test_bug_master.py — all NEW

## DESIGN

Row: `{"name":"bug-master","role":"director","tier":1,"harness":"claude-code","model":"claude-opus-5","effort":"xhigh","settings":"ultracode","session_kind":"tty","personality_ref":"","handoff_file":"","pin_ref":".agi/sessions/bug-master.meter","rotated_by":"sanctuary-master","owning_goal":""}`. `settings:"ultracode"` exports `CLAUDE_CODE_WORKFLOWS=1` (`_tier_is_ultracode`); role/tier reuse `_is_privileged_tool_seat`'s director-at-1 gate for `Workflow`+dispatch.py — that gate keys off `--role`/`--ladder-tier`, not the seat row: spawn as `--seat bug-master --tier director --role director --ladder-tier 1 [--dry-run]`.

Summon (existing verb): whichever seat's round just landed (a director's loop step, or driver.sh) runs `send.py send --to bug-master --from <caller> '{"iter":"<id>","targets":[{"hyp":"hypothesis:<id>","window":"<agent-id>"}]}'`.

Duty text (`bug-master-duties.md`): read the DM (`peek --dm <caller> --me bug-master`); on claude-code call `Workflow({name:"agi-round-review", args:{iter,targets}})`, off it `workflow.py run review --harness pi --args {iter,targets}` (l3w4-workflows-config-maxxed's runner) — model/effort come from config `workflows.review` (sonnet-max), never hardcoded; pipe the JSON to `bug_master.py format-record --iter <id>` (new, pure): writes it verbatim to `.agi/sessions/iter-<id>/review/results.json`, prints one `REVIEW iter=<id> target=<hyp> verdict=<v> overclaims=<n> open_gaps=<n> files_changed=<n> summary="…"` per target plus one `GLOBAL iter=<id> links_broken=<n> suite=<p>/<f>/<s> guard=<clean|WARN:n> summary="…"`; posts each via `send.py send --room tier3-quorum --from bug-master`.

## TESTS (red-first)

test_format_record_writes_results_json_verbatim; test_format_record_prints_one_review_line_per_target; test_format_record_prints_one_global_line; test_seat_row_bug_master_resolves_opus_xhigh_via_seat_plus_role_flags; test_dm_payload_roundtrips_iter_and_targets.

## GATE

The DESIGN invocation with `--dry-run` prints model=claude-opus-5, effort=xhigh, `CLAUDE_CODE_WORKFLOWS=1` exported, `Workflow` in `--tools`. A 2-target-plus-global fixture piped to `bug_master.py format-record --iter L3.99` prints exactly 3 lines and writes byte-identical JSON under `.agi/sessions/iter-L3.99/review/`. `send.py send --to bug-master '{...}' --from fixture` then `peek --dm fixture --me bug-master` round-trips it. Suite green; no live Workflow call or spawn.

## NOT IN SCOPE

`agi-round-review.js`'s prompts/schemas; its runner + `workflows.review` row (`l3w4-workflows-config-maxxed`); `send.py vote`/`season.py judge --quorum` (`l3w4-quorum-reviews`); rotation-loop alarms (`l3w4-seat-rotation-loops`); tmux transport (`l3w4-seat-transport`); the Sanctuary Master seat (`l3w4-sanctuary-master`); the drafter seat (`l3w4-drafter-seat`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, section "Owner text 2026-09-07... perpetual seats..." (owner verbatim 7, 7b) and its Director note placing Bug Master under `goal:g17`. `.agi/nodes/idea/push-further.md`, Agent Notes.

OWNER RENAME 2026-09-07 16:20 UTC (verbatim): "lets rename Bug Master to Glitch Master. Sounds more badass and lines up with the vibe of the Master layer." — the seat is glitch-master everywhere new (seats.md row, bug_master.py becomes glitch_master.py, the duties brief, room posts); this brief's slug keeps its address. The owner's layer 8 (doc quote 9, HANDOFF §6 item 24) makes it the Master that runs the strict graph-submission review loops under the Sanctuary Master, reports back to the director that asked, and joins season rollovers with the Training Master.

Belam V 2026-09-07 18:40 UTC: owner layer 8 (HANDOFF section 6 item 24, doc quote 9) puts every Master under the Sanctuary Master with its own workflow — this seat (Glitch Master) owns agi-round-review.js, the strict submission review loop. Sibling briefs now minted: hypothesis:l3w4-plan-master (owns agi-brief-drafting.js), hypothesis:l3w4-master-sensei (improves the Masters, reads hypothesis:l3w4-agent-failure-ledger), hypothesis:l3w4-masters-comms-and-escalation, hypothesis:l3w4-seat-push-further, hypothesis:l3w4-masters-rollover (Glitch + Sensei + Sanctuary Masters run season.py rollover).
