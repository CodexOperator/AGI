---
id: hypothesis:l3w4-master-sensei
mint_id: 7c7fc65605a643e8b8748340d49191c4
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 4dfeda184df78b84
season: 2
testable_claim: "dispatch.py --seat master-sensei --tier director --role director --ladder-tier 1 --dry-run resolves claude-opus-5 at effort high, and new sensei.py's apply --since TS calls write.py <node> \"note SENSEI: ...\" exactly once, and only once a reply after TS exists on every required dm/room thread (the target role's own dm plus its rotated_by-resolved supervisor dm/room, or the supervisor thread alone for a target absent from config:seats), while the identical apply against belam or a tier-3 parent (an advisor) never calls write.py without an explicit --owner-approved flag and instead writes a draft file under .agi/sessions/sensei/drafts/ and dms liaison."
thought_session: L3.27
title: Seat the Master Sensei
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-master-sensei

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`config:seats` gains `master-sensei` (director, tier 1, claude-opus-5,
high, no ultracode, `rotated_by: sanctuary-master`,
`owning_goal: goal:g17` — matches
sanctuary-master/plan-master; training-master's draft left it empty).
New `sensei.py`: `pick_worst()` reads the ledger's rows
(`hypothesis:l3w4-agent-failure-ledger`), not cached, for the
worst seat/model/role. `propose --target S --change TEXT` dms the seat
plus `rotated_by`, prints a timestamp; `apply --since TS`, once every
required thread shows a reply after it, shells `write.py <node> "note
SENSEI: TEXT"` on the role's build node — a protected target (Belam, a
tier-3 parent) also needs `--owner-approved`, else it drafts a file
and dms `liaison`.

## WHY

Owner (12): "always by talking to the respective role and their direct
supervisor... For ephemeral roles... only talk to that role's
supervisor... keep track of where agents fail and... eliminate why...
'training' them... propose harness updates and staffing/seat
modifications." Owner (9): "Improvements to standard seats are
automatic, but modifications to Belam or his advisors require owner
approval."

## FILES

- .agi/nodes/.geometry/seats.md :: seats — EDIT, rename+correct row
- .agi/nodes/goal/g17.md — parent
- extensions/agi/bin/sensei.py — NEW
- extensions/agi/briefs/master-sensei-duties.md — NEW
- extensions/agi/bin/spawn_gate.py :: read_seat_registry L588
- extensions/agi/bin/dispatch.py :: resolve_seat_spec L436, --seat L693
- extensions/agi/bin/node_writer.py :: find_node_file L184
- extensions/agi/bin/send.py :: send_dm L441, send_room L455, peek_dm L485
- extensions/agi/bin/write.py :: parse_script L308 (the "note" verb)
- extensions/agi/tests/test_sensei.py — NEW

## DESIGN

Two axes, non-circular: sanctuary-master rotates every Master
including Sensei; Sensei improves every Master including
sanctuary-master (safe: sanctuary-master's own `rotated_by` is
`quorum`, not Sensei). `_direct_supervisor(row)`: `rotated_by` in
`{quorum,advisor,prime}`→room `tier3-quorum` (owner 4: no seat but
the quorum reaches Belam); else dm that name; no row (ephemeral)
needs `--supervisor SEAT`, skips the role dm. `pick_worst(rows)`: pure,
groups ledger rows by `(seat_or_role, model)`, worst rate, ties by
count. `propose` posts one `[sensei #propose] TEXT` to the role dm
(skipped if ephemeral) and the supervisor dm/room; stateless, the
printed `ts` is the handle. `apply --since TS` re-derives the
supervisor, needs a reply after `TS` on each required thread
(`peek_dm`/`peek_room`), then `find_node_file` plus `write.py note`.
Protected, no `--owner-approved`: skips `write.py`, drafts a file, dms
`liaison` instead — the owner gate only adds a step.

## TESTS (red-first)

`test_direct_supervisor_room_for_quorum_advisor_prime_dm_for_named_seat`;
`test_pick_worst_returns_highest_rate_row_ties_broken_by_count`;
`test_apply_refuses_without_a_reply_after_since_on_every_thread`;
`test_apply_protected_target_never_calls_write_py_without_owner_approved`;
`test_apply_ephemeral_target_checks_only_the_supervisor_thread`.

## GATE

`dispatch.py --seat master-sensei --tier director --role director
--ladder-tier 1 --dry-run` prints `claude-opus-5`/`effort=high`.
Fixture: `propose --target dir-g1`, a reply on each dm, `apply --since
<ts>` — one `write.py note`; the same on `belam` with no
`--owner-approved` drafts+dms `liaison` instead, zero `write.py`
calls. Suite green.

## NOT IN SCOPE

Ledger file/schema/writer (`l3w4-agent-failure-ledger`); tagged
ask/report/escalate comms (`l3w4-masters-comms-and-escalation`) —
`sensei.py` uses only plain `send_dm`/`send_room`/`peek_dm`. Sanctuary
Master's row, seat add/remove, `hierarchy_state`
(`l3w4-sanctuary-master`). Rotation alarms (`l3w4-seat-rotation-loops`).
Plan/Glitch Master seats. Sensei's own push-further (`l3w4-seat-push-further`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, owner quote (12) (2026-09-07
~17:55 UTC, to Belam V), renaming/scoping the Sensei; quote (9), the
automatic/owner-approval split.

BUILD IT — OWNER PRIORITY, 2026-09-07 23:1x UTC, verbatim: 'We also could use that Master Sensei asap for sure'. Your artefact is a DIFF. The L3.34 round on this brief returned a faithful red-first baseline with zero lines of code and its own caveat said so: 'experiment records absence-of-build only'. That is not what is wanted here. The claim is FALSE today and you are the one who makes it true; if git diff --stat is empty you are not done, and a fix you find impossible is a real result only if you say which part and why. WHY THE SENSEI IS URGENT RATHER THAN NICE, in this loop's own measured terms — this is the evidence he would be reading on day one. The same kid-side failures keep recurring and nobody owns them: a parent's first cli.py done lacking --evidence-runs happened three rounds running; kids minting nodes with their own tool instead of write.py happened repeatedly until a guard caught it; brief.py's kid template taught EVERY kid a broken write.py call (L3.31) and then, in a second and unrelated way, taught every kid to measure instead of build (L3.34, four parents at once). Each was found by accident, by one parent's struggles: line or one director's eye, and each cost a round. That is exactly the job the owner described for this seat: keep track of where agents fail, figure out why, and eliminate the cause by working with the role and its supervisor. hypothesis:l3w4-agent-failure-ledger is the table he reads and its mvp now exists (mvp:g16-failure-ledger, minted 2026-09-07 22:1x UTC) along with build:failures.py, so the blocked payload path is open — the Sensei is no longer waiting on it. REMEMBER THE OWNER'S BOUNDARIES, quote (12): the Sensei improves the MASTERS, including the Sanctuary Master, while the Sanctuary Master owns seat assignments, model selection and seat-structure changes. He works by talking to the role AND its direct supervisor, and for an ephemeral role only to the supervisor. Improvements to standard seats are automatic; anything touching Belam or his advisors needs owner approval or a finalized draft, never a direct edit. And correction (4) stands: the quorum IS Belam to everyone else, so the Sensei never DMs Belam for an advisor's thread.
