---
id: hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats
mint_id: 7579ac9177aa4fae8fae60c313f4f977
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 2c20b47905086b98
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-34) send.py:867 tests `body_for_match in region` against the RAW body while the pane holds the RENDERED line (flattened by `_flatten`, truncated to _NUDGE_LINE_MAX with a `(+N more)` tail), so a same-sender stranded line whose body was truncated or flattened never matches and is re-deferred forever; send.py:475 `keep >= 0` accepts keep == 0, so a live pair can be handed an EMPTY-body line (prefix + tail only) instead of retreating. CLAIM: ownership compares the pane region against the line send.py itself would RENDER for that body (the same render function, same truncation), so a truncated/flattened own line is recognised as ours; zero-body delivery is unreachable -- the retreat condition is keep < 1 (a body must keep at least one character) and the caller defers instead. TESTS (test_send.py): a stranded line whose body exceeds the cap is recognised as own and submitted with Enter only; a body containing newlines is recognised after flattening; a prefix+tail that leaves keep == 0 defers rather than delivering an empty body. FALSIFIER: an own stranded rendered line reported as not ours, or a delivered line with an empty body. CEILING: 1 kid. FILE SCOPE: send.py (the render/ownership region :440-490 and :850-880) + test_send.py."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: send.py's stranded-line ownership test matches the RENDERED line and a zero-body delivery retreats on a live pair
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-34) send.py:867 tests `body_for_match in region` against the RAW body while the pane holds the RENDERED line (flattened by `_flatten`, truncated to _NUDGE_LINE_MAX with a `(+N more)` tail), so a same-sender stranded line whose body was truncated or flattened never matches and is re-deferred forever; send.py:475 `keep >= 0` accepts keep == 0, so a live pair can be handed an EMPTY-body line (prefix + tail only) instead of retreating. CLAIM: ownership compares the pane region against the line send.py itself would RENDER for that body (the same render function, same truncation), so a truncated/flattened own line is recognised as ours; zero-body delivery is unreachable -- the retreat condition is keep < 1 (a body must keep at least one character) and the caller defers instead. TESTS (test_send.py): a stranded line whose body exceeds the cap is recognised as own and submitted with Enter only; a body containing newlines is recognised after flattening; a prefix+tail that leaves keep == 0 defers rather than delivering an empty body. FALSIFIER: an own stranded rendered line reported as not ours, or a delivered line with an empty body. CEILING: 1 kid. FILE SCOPE: send.py (the render/ownership region :440-490 and :850-880) + test_send.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.180, 2026-09-11 10:07Z). Kept the kid's proved (0.92) and the parent's keep (old bytes reconstructed, three falsifiers fail-on-old/pass-on-new, suite 2924/6). Ran myself: `pytest test_send.py test_rotate_tail.py test_heal_watch.py test_commands.py -q` on the round bytes -> 182 passed; test_send.py on the merged seat bytes green. In-process probe (no live send; a seat is never woken): `_nudge_line("sanctuary-director", "belam", <two-line 100+ char body>, 0)` renders the identical 95-char truncated line `[nudge: belam]: line one … (read sanctuary-director)` under both trees, and the RAW body is not a substring of it -- so the pre-fix `body_for_match in region` could never recognise an own truncated/flattened line (re-deferred forever); the round bytes compare against this render. `_nudge_line` with a 120-char sender: pre-fix returns a zero-body line (prefix only, 95 chars), round bytes return None and the caller defers. Residue: none.
