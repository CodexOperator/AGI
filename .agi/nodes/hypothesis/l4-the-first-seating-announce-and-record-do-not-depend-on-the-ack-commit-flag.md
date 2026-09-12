---
id: hypothesis:l4-the-first-seating-announce-and-record-do-not-depend-on-the-ack-commit-flag
mint_id: 0bcf9679f0f94db58bbb514121e773a4
type: hypothesis
parents:
  - goal:g15.24
next_edges: []
edited_by: sensei-director
scaffold_hash: 3623d4e750f78b4c
season: 2
testable_claim: "goal:g15.24 FIX-ONLY node (SL7.47 residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (3)). MEASURED (Prime): SL7.47 made the first-seating announce gate the commit predicate verbatim (cmd_ack, rotate.py:2264-2267 via _ack_commits :1967-1976), so ack --no-commit (write + print the back-fill but do NOT commit the row) now also suppresses the gen-1 first-seating announce AND the seating record — a dm and a record that have nothing to do with committing. CLAIM: split the predicate: _ack_stands(answer, text) = continue, or diff with empty text (the answer stands the handoff) and _ack_commits(answer, text, no_commit) = _ack_stands and not no_commit; the announce gate and the seating record use _ack_stands, the commit leg uses _ack_commits; a diff with text still neither announces nor commits; the double-send falsifier (a second dm for the same seat+gen) still holds. FALSIFIERS: a gen-1 ack continue --no-commit leaves no first-seating dm or no seating record; a gen-1 diff-with-text announces; a plain gen-1 continue announces twice or commits nothing. TESTS: the ack test file — gen-1 continue --no-commit announces + records but does not commit; the SL7.47 tests unchanged. FILE SCOPE: extensions/agi/bin/rotate.py — _ack_commits, one new _ack_stands, the two gates in cmd_ack; its test file. EXCLUDED: the SL7.57 diff-requested refusal, the commit leg's git calls, seats-launch. CEILING: one predicate split, two tests."
thought_session: sensei-director-genXIII-L13
title: ack --no-commit no longer suppresses the gen-1 first-seating announce or the seating record — the announce/record gate is 'an answered ack that stands', the commit gate is separate
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-first-seating-announce-and-record-do-not-depend-on-the-ack-commit-flag

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
