---
id: hypothesis:l4-rendered-line-ownership-tolerates-the-wrap
mint_id: 2e58b26bfdf549c29ea85d0740c6ad8c
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 6d60aef04bde29e7
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.180) send.py:907 compares the rendered line against the captured pane region verbatim, but tmux WRAPS a 95-char line at the pane width (the measured sanctuary-director pane is 104 columns; a fixture pane is 80), so an own stranded line that wrapped never matches and is re-deferred. CLAIM: the comparison collapses the wrap on the region side (join the captured lines, strip the wrap-inserted line breaks and trailing spaces) before testing `own_line in region`; tests render a stranded line at fixture width 80 AND at the measured 104 and assert ownership under both. FALSIFIER: an own line that wraps reported as not ours. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (the ownership region only) + test_send.py."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: send.py's rendered-line ownership test compares against a wrap-collapsed pane region, at fixture width 80 and the measured 104
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rendered-line-ownership-tolerates-the-wrap

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.180) send.py:907 compares the rendered line against the captured pane region verbatim, but tmux WRAPS a 95-char line at the pane width (the measured sanctuary-director pane is 104 columns; a fixture pane is 80), so an own stranded line that wrapped never matches and is re-deferred. CLAIM: the comparison collapses the wrap on the region side (join the captured lines, strip the wrap-inserted line breaks and trailing spaces) before testing `own_line in region`; tests render a stranded line at fixture width 80 AND at the measured 104 and assert ownership under both. FALSIFIER: an own line that wraps reported as not ours. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (the ownership region only) + test_send.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.188, 2026-09-11 12:09Z). Kid demoted proved -> lean_proved:70 (see experiment:a00-e04043eb-cb6a8a): the join-with-a-space reconstruction recognises a WORD-boundary wrap but not the CELL wrap a real tmux pane performs; reproduced on the round bytes (word-wrap True, cell-wrap at 80 False, no wrap at the measured 104). tmux 3.4 on this box supports `capture-pane -J` (join wrapped lines). FIX-ONLY #2 (L4.192) CLAIM (what is done: _region_join_wrap + the word-wrap fixture): the ownership capture at send.py:662 passes `-J` (`tmux capture-pane -p -J -t <target>`) so the region carries no soft-wrap at all, and `_region_join_wrap` keeps working as the fallback for a region captured without `-J` by trying BOTH joins (one space, and empty) so a cell-wrapped own line is recognised too; the fixture models the CELL wrap (`line[:W-2] + "\n" + line[W-2:]`, mid-word) at 80 AND 104 alongside the existing word-wrap case, and a test asserts the capture argv contains `-J`. FALSIFIER: an own line cell-wrapped at 80 reported as not ours. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (the capture call + _region_join_wrap + the ownership line) + test_send.py.

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.192, 2026-09-11 12:28Z). Kept the kid's proved (0.8) and the parent's accept (experiment:a00-e98c3185-4c6b69). Ran myself on the round bytes (a00-2ff9f5de): the REAL `_nudge_line` render (95 chars, `[nudge: a00-e98c3185]: iter=L4.192 ...  (read sanctuary-director)`) cell-wrapped at 78 (`an`) and at 80 (`ct`) is recognised by `any(own in r for r in _region_join_wrap(...))` = True while the space-only join = False (the L4.188 defect, reproduced then closed); no wrap at the measured 104 (ncands=1, both True); word-wrap@75 True under both. `_capture_pane("agi-rc","@278")` with a fake `subprocess.run` records argv `['tmux','capture-pane','-p','-J','-t','@278']`. 159 passed with neighbours (test_send/test_mail_alert/test_rotate_handover). REAL-PANE MEASUREMENT the round did not make: `tmux capture-pane -p` vs `-p -J` on the four live Claude Code panes (@278 mine, @277 prime, @248 helper, @272) at 104x89 returns 89 rows both ways and zero joined rows wider than the pane -- the claude-code TUI draws its own rows, so a tmux SOFT-wrap never exists on a live target and `-J` is neutral there; the both-join fallback is the load-bearing half for the TUI-drawn wrap. Not a demotion (the falsifier is measured false through that exact path), a scoping: `-J` earns its keep only on a raw-shell pane. Parent's residual stands and is real: the empty join also erases HARD row boundaries in the fallback, so two genuinely separate logical lines could concatenate into our rendered line; bounded by the `[nudge: <sender>]:` head + our body having to appear in order, so a different body still does not match. Queue for send.py after this: `l4-deferred-ownership-uses-the-rendered-count`.
