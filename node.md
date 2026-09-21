---
id: hypothesis:l3w4-belam-predecessor-chain
mint_id: 211bd8e822b94a088d64a6a5a3fb2253
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 2d882a2940d72e48
season: 2
testable_claim: "rotate.py status --chain lists every live belam-prefixed tmux window newest-first as an arrow chain with each row marked active or idle, using the existing _existing_windows() helper rather than cmd_status's own session-name filter (confirmed broken against the live server: tmux list-sessions returns agi-rc and fantasia-dev, matching neither the agi-master nor belam prefix check it applies); cmd_loop writes a new one-line sibling file .agi/sessions/<successor>.predecessor (never a second line inside the single-line .meter pin) naming the window it just rotated out of; send.py ask-predecessor <question> --as <own-window> dms the nearest live predecessor, walking exactly one link further per gone window and never blocking; and a guard test confirms no non-prime brief under extensions/agi/briefs/ carries the predecessor-chain rule that prime-director-successor.md alone states."
thought_session: L3.27
title: Wire the Belam predecessor chain
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-belam-predecessor-chain

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`rotate.py` gains one pure helper, `_predecessor_name(name, prefix="belam") -> str | None` (Roman-decrement, symmetric with `_derive_successor_name`), reused three ways: (1) `status --chain` prints the live belam-window chain newest-first, arrow-joined (`V←IV←III←II←belam-S1-L3`), each row active/idle — via `_existing_windows()`, not `cmd_status`'s own session filter, confirmed broken (WHY); (2) `cmd_loop`, after `spawn_window` succeeds, writes a sibling `.agi/sessions/<successor>.predecessor` (one line: the prior window's name), never a second line inside the single-line `.meter` pin; (3) `send.py ask-predecessor "<question>" --as <own-window>` dms the nearest *live* predecessor, falling back one link per gone window, never blocking.

## WHY

Owner, verbatim (11), Belam-only: "...may ask their predecessor for input... and so on... only available to Belam." Belam V: "a rotated Belam idles in its window and never exits." Already in `extensions/agi/briefs/prime-director-successor.md` (checked, not duplicated) — two defects: the prior bullet runs on with no line break (`never rebase.- **Predecessor chain`), and the command drops `--to`: `text` (nargs="*") greedily swallows both words, `target` stays `None`, so it errors (`ERR: send needs a target`, exit 1, confirmed) instead of writing the comms-root dm `comms/season-2/dm/belam-S1-L3-IV--belam-S1-L3-V.md` (and two siblings) use.

## FILES

- `extensions/agi/briefs/prime-director-successor.md` — fix formatting + `--to`
- `extensions/agi/bin/rotate.py :: _split_roman_suffix`(601), `_derive_successor_name`(618), `_existing_windows`(538), `cmd_loop`(961), `cmd_status`(1033) — NEW `_predecessor_name`, `--chain`
- `extensions/agi/bin/send.py :: send_dm`(459), `_nudge_window`(324), `main`(605) — NEW `ask-predecessor`
- `extensions/agi/tests/test_rotate.py`, `test_send.py` — NEW cases
- `.agi/nodes/.geometry/seats.md`, `[config].md` — considered, unused (DESIGN)

## DESIGN

`seats.md`'s `belam` row is per-seat class config, not per-rotation state — no field goes there. `.meter` is one line, a transcript path (`_read_pin_target` strips the file as one path); a second line breaks it silently. `.predecessor` is a new sibling, same family as `.log`/`.head.md`/`.seed.md`. `--chain`'s live enumeration is authoritative and free; `.predecessor` is a durability record for once a link's window is gone. `ask-predecessor` requires `--as` — no reliable identity exists for a remote-control prime today (`AGI_SEAT`/`AGI_AGENT_ID` are never exported into the tmux launch line). Recursion needs no new code: every Belam reads this same rule at spawn, so an idling IV can `ask-predecessor` III on V's behalf.

## TESTS (red-first)

`test_predecessor_name_decrements_and_roots_at_none`; `test_status_chain_orders_newest_first_and_marks_active`; `test_status_chain_marks_gone_window_when_not_live`; `test_loop_writes_predecessor_sibling_file_not_meter`; `test_ask_predecessor_falls_back_one_link_when_window_gone`; `test_ask_predecessor_requires_as_flag`; `test_generic_seat_briefs_carry_no_predecessor_rule` (globs `briefs/*.md` minus this one — 0 files today, vacuous now, a real guard once a seat brief lands).

## GATE

`status --chain --window-path <fixture V,IV,III,II,belam-S1-L3>` prints the arrow chain; one `.predecessor` file lands per rotation, naming the prior window; `ask-predecessor` on a fixture missing the direct link still delivers one dm, exit 0; brief-glob guard passes; suite green.

## NOT IN SCOPE

Non-prime `rotate-self` / window-kill (`l3w4-seat-rotation-loops`); its "revoke predecessor git verbs" ADDENDUM (banked, unresolved); nudge/transport internals (`l3w4-seat-transport`); fixing `cmd_status`'s legacy default dump (confirmed broken — CLAIM) is separate.

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07 ... perpetual seats" — owner quote (11), Belam V's reading (not owner text).

Belam V 18:56 UTC: fold in the unbuilt fix shape of hypothesis:l3-remote-control-desktop-disconnect — rotate.py status --chain shows, per Belam window, active | idle | remote-control attached (the claude-code debug log's heartbeats stop on a GUI detach, system code 4090; measured by experiment:a00-773d0fd5-68fd10).
