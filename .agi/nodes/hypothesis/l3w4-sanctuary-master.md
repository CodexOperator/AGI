---
id: hypothesis:l3w4-sanctuary-master
mint_id: f6ff0aff9af0437e8c19a06489fcb423
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: 4968cdf1bdafda08
season: 2
testable_claim: "config:seats gains a sanctuary-master row (director, tier 1, claude-opus-5, effort high, rotated_by: quorum, owning_goal: goal:g17) that is the only row whose rotated_by is quorum; every row for a seat she oversees (liaison, dir-g1, dir-g15, dir-g16, the future Bug Master) has rotated_by repointed to sanctuary-master; and rotate.py master --as <seat> --kind {rotate|add-seat|remove-seat|expand|collapse} forwards exactly one send_dm to sanctuary-master when --as names any other seat, but enacts the request directly (a rotate-now DM, a config:seats rewrite, or a new ladder hierarchy_state write) only when --as sanctuary-master, adding no sanctuary-master key to ladder:ladder's mantles."
thought_session: L3.25
title: Stand up the Sanctuary Master seat
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-sanctuary-master

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`config:seats` gains a `sanctuary-master` row (director, tier 1, claude-opus-5, effort high, `rotated_by: quorum`, `owning_goal: goal:g17`) — the only row so rotated. Every seat she oversees (`liaison`, `dir-g1`, `dir-g15`, `dir-g16`, the Bug Master) gets `rotated_by: sanctuary-master` instead. One entry point every seat calls: `rotate.py master --as <seat> --kind {rotate|add-seat|remove-seat|expand|collapse} [--target T] [--dry-run]` — `--as` anyone else forwards one `send_dm` to her, `--as sanctuary-master` enacts. Her mantle is banked, not invented: `personality_ref` stays empty, no `sanctuary-master` key lands on `ladder:ladder`'s `mantles`.

## WHY

Owner (7): "...a 'Chief-of-Staff' director-kid... responsible for the 'House' that has all our seats." Owner (7b): "...anyone the Master oversees gets rotated by the Master... The Master is the only one who gets rotated by the quorum. Any seat modifications also go through the Master who also helps expand or collapse hierarchy or... add/remove seats... also oversees the owner liaison... and... the Bug Master." Owner (4) sets her row's model ("director-kids are opus on high effort") and the collapsed/expanded comms split `hierarchy_state` stores.

## FILES

- `.agi/nodes/.geometry/seats.md` :: `seats`, `rotated_by` — EDIT
- `.agi/nodes/.geometry/ladder.md` :: `mantles` — EDIT, NEW `hierarchy_state`
- `.agi/context/schemas/[ladder].md` :: `fields`, `validation.types` — EDIT
- `extensions/agi/bin/rotate.py` :: `spawn_window` L793, `main` L1033 — NEW `cmd_master`
- `extensions/agi/bin/send.py` :: `send_dm` L441
- `extensions/agi/bin/spawn_gate.py` :: `read_seat_registry` L588
- `extensions/agi/bin/write.py` :: `verb_set` L229
- `extensions/agi/tests/test_rotate.py` — NEW tests
- `.agi/nodes/goal/g17.md` — parent

## DESIGN

Row (mirrors `dir-*`): `{"name":"sanctuary-master","role":"director","tier":1,"harness":"claude-code","model":"claude-opus-5","effort":"high","settings":"","session_kind":"tty","personality_ref":"","handoff_file":"","pin_ref":".agi/sessions/sanctuary-master.meter","rotated_by":"quorum","owning_goal":"goal:g17"}`. `session_kind: tty` matches the other director-kids (director proposal, owner silent on hers). Delegation to `l3w4-seat-rotation-loops`'s `alarms --holder S` is pure data, no new rotation code: once every row she oversees reads `rotated_by: sanctuary-master`, her own `alarms --holder sanctuary-master` (same code, different holder) nudges each past `director_rotate_at`. `master`'s `--as` gate is one call, two behaviors by caller identity: `rotate` sends the identical `"rotate now"` DM the alarm loop sends; `add-seat`/`remove-seat` rewrite `config:seats` via `verb_set`; `expand`/`collapse` set new `hierarchy_state: collapsed|expanded` on `ladder:ladder` (default `collapsed`) — owner (4): collapsed=no free director-Belam comms; expanded adds director-to-director lateral+limited-vertical only; Belam is quorum-only regardless; enforcement unbuilt, see NOT IN SCOPE.

## TESTS

`test_sanctuary_master_row_is_only_rotated_by_quorum`; `test_probe_and_liaison_rows_rotated_by_sanctuary_master`; `test_master_as_non_master_forwards_dm_never_enacts`; `test_master_as_sanctuary_master_kind_rotate_sends_rotate_now`; `test_master_seat_add_and_remove_rewrite_registry`; `test_master_kind_expand_sets_hierarchy_state`; `test_ladder_mantles_has_no_fabricated_sanctuary_master_entry`.

## GATE

`rotate.py master --as dir-g1 --kind rotate --target dir-g1 --dry-run` prints one forwarded dm to `sanctuary-master`, nothing written; `--as sanctuary-master --kind expand --dry-run` prints the `hierarchy_state` write, nothing live; `seats.md` carries the new row plus every repointed `rotated_by`; `links.py schema` no new violation; suite green.

## NOT IN SCOPE

Rotation-loop mechanics (`l3w4-seat-rotation-loops`); tmux nudge internals (`l3w4-seat-transport`); the Bug Master's own row (`l3w4-bug-master-seat`); the quorum vote rotating HER (`l3w4-quorum-reviews`); the send.py comms-gate enforcing owner (4) via `hierarchy_state`; the Sanctuary viewport theme (`l3w4-sanctuary-theme`); her mantle prose.

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07... perpetual seats, the quorum as reviewer, the owner liaison" — owner verbatim (4), (7), (7b).

OWNER RENAME 2026-09-07 16:20 UTC: the Bug Master seat is the GLITCH MASTER (glitch-master). Layer 8 (doc quote 9): the Masters under her are the Plan Master (drafting), the Glitch Master (review loops) and the Training Master (audits, role improvement); director-kids consult any Master and Masters report back to the asker.
