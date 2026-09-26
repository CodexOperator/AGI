---
id: hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched
mint_id: 10552e3357e9427f8459ade0ee1eeb04
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 7cdc7cfac0397865
season: 2
testable_claim: "rotation_alert.py _force_capture never prepends into the card path or its symlink target (a captured card node still parses, first line ---); the backgrounded handoff && rotate-self --force chain logs to a declared path instead of DEVNULL and a capture latches once per seating; the chain failure is reproduced on a symlinked fixture card and fixed if the unflattened symlink is the cause, else recorded as MEASURED (lean)."
title: The captive capture never writes into the live card, and a failed forced rotation is logged and latched
town: core
---
# hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched

# hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched

## Measured
- TMM.190 (thought-master, traced on the bytes, 2026-09-26): `extensions/agi/hooks/rotation_alert.py:832` `_force_capture` does `card.write_text("AUTO-CAPTURED\n" + card.read_text())` on the LIVE card path. A quorum card is a symlink into `.agi/nodes/doc/card-<seat>.md` (restored by director-engine gen 22), so the write lands ABOVE the node's `---` -> FrontmatterError. Hit director-engine's card 3x (f 0.41/0.42/0.43) and director-thought's quorum card 5x (13:58:36Z; thought-master restored main's copy before 8732c4dc8e).
- Trigger: `_captive_rotate` fires at f >= captive_rotate_ratio (ladder.md:16 = 0.85) x the line = 0.3995 for a director; `rotation_alert.py:840-844` backgrounds ONE `bash -c` chain `handoff --driven ... && rotate-self --force` with stdout+stderr -> DEVNULL.
- Loop: 3 captures and NO rotation record after director-engine.20260925T223509Z = the forced chain failed silently each time, and nothing latches the capture -> one more corrupting prepend per prompt.
- Lead (NOT proved): the chain's first step `cmd_handoff` does not flatten a symlinked card (PASS 7 follow-up row; `rotate.py:18013` `_flatten_card_symlink` exists but the handoff path may not call it); with `&&`, a failed handoff means rotate-self never runs.

## CLAIM
(1) `_force_capture` never writes into the card path or its symlink target -- the AUTO-CAPTURED marker goes to a sibling state file (or rides the s3/s6 fields the handoff already carries), and a card node read after a capture parses (first line `---`); (2) the backgrounded chain's stdout+stderr go to a DECLARED log path (a config cell, never DEVNULL) and a capture latches once per seating (a second prompt past the ratio with the same seating writes no second capture); (3) WHY `handoff --driven && rotate-self --force` failed is REPRODUCED in a scratch fixture (symlinked card), and if the cause is the unflattened symlink, the handoff path flattens via `_flatten_card_symlink` or writes through the symlink target correctly -- else the node records the measured cause and (3) is a lean.

## Dispatch line
config-max: the capture log path is a cell (paths.<town>.* or the hook's config), never a literal / template-max: none / code: the sibling marker, the latch, the logged chain, the handoff symlink step.

## FALSIFIERS
- a fixture card symlinked into a fixture node, captured once: the node's first line is not `---` -> (1) false
- two consecutive captive prompts for one seating produce two captures -> (2) false
- the chain's failure reproduces with a REGULAR (non-symlink) card too -> the symlink lead is wrong; say so
- any test touching a real pane, pid, seat card, `.agi/sessions/quorum/*` of the live tree, or spawning a real rotate-self -> demote (fixtures + `AGI_HOOK_NO_SPAWN` / `_Popen` seams only)

## TESTS
`extensions/agi/tests/test_rotation_alert*.py` + `test_rotate*handoff*` neighbourhoods (read them first); new: symlinked-card capture keeps frontmatter; latch once per seating; chain output lands in the declared log.

## FILE SCOPE
`extensions/agi/hooks/rotation_alert.py`, `extensions/agi/bin/rotate.py` (`cmd_handoff`'s card-write path only), their tests, one config cell. Nothing else. Never run the hook against a live seat.

## CEILING
ONE pi-free parent (tier 0), <= 3 kids, 10-12 production lines per conjunct, cap $1.
