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
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: send.py's rendered-line ownership test compares against a wrap-collapsed pane region, at fixture width 80 and the measured 104
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rendered-line-ownership-tolerates-the-wrap

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.180) send.py:907 compares the rendered line against the captured pane region verbatim, but tmux WRAPS a 95-char line at the pane width (the measured sanctuary-director pane is 104 columns; a fixture pane is 80), so an own stranded line that wrapped never matches and is re-deferred. CLAIM: the comparison collapses the wrap on the region side (join the captured lines, strip the wrap-inserted line breaks and trailing spaces) before testing `own_line in region`; tests render a stranded line at fixture width 80 AND at the measured 104 and assert ownership under both. FALSIFIER: an own line that wraps reported as not ours. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (the ownership region only) + test_send.py.
