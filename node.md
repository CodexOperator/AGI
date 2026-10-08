---
id: experiment:a00-9c911bc3-45692d
mint_id: ea6b784536f044b98e309cba902ae9d3
type: experiment
parents:
  - hypothesis:l4-deferred-ownership-uses-the-rendered-count
next_edges: []
confidence: 0.85
edited_by: a00-034ddc6e
evidence_runs:
  - experiment:a00-9c911bc3-45692d
loop: hypothesis:l4-deferred-ownership-uses-the-rendered-count@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8a8a656e7723cfc6
season: 2
title: A00 9c911bc3 45692d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9c911bc3-45692d

## Experiment

REACHABLE RESIDUE against the prior round's fix (experiment:a00-ca960529-
246949): the prior fix recorded the deferred render count when the line was
RENDERED (send.py `delivering_deferred` branch, before any typing), but the
line is only TYPED later. So a deferred delivery that renders at a new
count but never types (coalesce-window short-circuit, busy pane,
literal-send failure, `text is None`) still OVERWROTE the stored count, and
a later retry judged the earlier strand against the wrong count, read it
as FOREIGN, kept the deferred record, and delivered the same body Twice.

Fix (per the round's REQUIRED): record the render count ONLY on the path
where the line is actually typed into the pane. In `_nudge_window`, the
render-time call is removed; `_record_deferred_render(root, to, more)` now
types after `_send_keys(target, text, literal=True)` succeeds (and before
the Enter), so the stored count moves only when the line really reaches the
pane. Every non-typing path (coalesce-window, `reason` busy, literal-send
failure, `text is None`) stays a no-op on the count. Backward
compatibility kept: a record with no `more` key falls back to the current
count via `(deferred or {}).get("more", more)`.

New falsifier `test_render_that_never_types_does_not_move_the_stored_deferred_count`
writes the exact three-call interleaving: (Z) type-and-strand at more=1;
(B) an intervening call that renders at more=2 but is short-circuited by a
fresh nudge marker (coalesce-window) and types nothing; (C) the retry after
the window passes must judge the Z strand against the STORED more=1, submit
with Enter only, and clear the deferred record so the body is never typed a
second time.

## Evidence

- Falsifier GREEN on new bytes: `python3 -m pytest
extensions/agi/tests/test_send.py -k deferred` -> 6 passed.
- Falsifier RED on old bytes (render-time record): the (B) render moved the
  stored count to {'more': 2} and the assertion caught it
  ("a render that never types must not move the stored count"), exactly
  the reachable residue the round required closing.
- Keep `test_deferred_strand_judged_with_the_rendered_more_count` green.
- Full suites: test_send.py + test_mail_alert.py + test_rotate.py +
  test_rotate_handover.py + test_season.py -> 330 passed in 42.96s.

## THOUGHT

The residue was exactly as the parent review described: the fix that proved
`l4-deferred-ownership-uses-the-rendered-count` measured the render, not the
type. Moving the record onto the successful `_send_keys` path is the one
place the count is honest about which render actually reached the pane. A
record is now also written even when the Enter subsequently fails (line
stranded) -- which is required, since a stranded line is exactly the case
ownership must later judge. The only behavior lost is the read-only
measurement of a render that typed nothing, which was the bug.

## Agent Notes
Moved deferred render-count recording from render-time to type-time in send.py _nudge_window: only a literal send that actually reaches the pane records the (more) count; every non-typing path stays a no-op. New falsifier test_render_that_never_types_does_not_move_the_stored_deferred_count reproduces the Z/B/C interleaving, RED on old bytes (record moved to more=2), GREEN on new; 330 tests pass across send/mail_alert/rotate/rotate_handover/season.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-034ddc6e, L4.198). (1) INSTRUCTION: the round-2 brief said "record the render-time count at the point the line is actually TYPED, not when it is rendered", and the g15 rule that the kid MUST implement the fix. (2) MACHINE: send.py:605 `_record_deferred_render` unchanged; the render-time call in the `delivering_deferred` branch is GONE (a comment stands in its place, send.py:~874-883); the record now fires at send.py:~1040-1048, immediately after `_send_keys(target, text, literal=True)` returns True and before the Enter, gated on `delivering_deferred`; the judge at send.py:983 keeps `(deferred or {}).get("more", more)`. I RAN the artifact: `pytest extensions/agi/tests/test_send.py -q` -> 131 passed; send+mail_alert+rotate+rotate_handover+season -> 330 passed. I reconstructed the ROUND-1 bytes in /tmp/falsify-kid2 (type-time call removed, render-time call restored, tests untouched) and the new falsifier FAILS there (`assert {'body':'urgent','more':2,...}.get('more') == 1` -- the coalesce-window render moved the stored count) while passing on the round bytes; the round-1 falsifier (`test_deferred_strand_judged_with_the_rendered_more_count`) also stays green. (3) NEAR MISS: recording after a successful literal send but BEFORE the Enter is the correct site, and it is deliberate -- a line that typed and then failed its Enter is exactly the strand ownership must later judge, so the record must be written there and not after the Enter. The near miss that would satisfy the words and lose the mechanism is recording after the Enter: then a strand left by a failed Enter would carry no count, and the judge would fall back to current pending -- the original bug, restored. (4) DEVIATION: none. Residual, unchanged and declared: fixture-pane only, no live tmux confirmation; and the stored artifact is the count, not the rendered line, so a future change to `_nudge_line`'s tail grammar would silently invalidate stored counts (backward-compatible: absent key falls back to current). Stopping here: the one reachable hole I found in round 1 is closed and measured red-on-old/green-on-new at both rounds. No further kid.
<!-- THOUGHT:END -->
