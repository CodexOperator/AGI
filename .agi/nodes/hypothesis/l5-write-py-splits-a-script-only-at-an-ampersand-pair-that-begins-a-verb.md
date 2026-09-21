---
id: hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb
mint_id: d20f707b9abb4a79a538dd667405d11b
type: hypothesis
parents:
  - goal:g4.18
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 119310046aa505d3
season: 2
testable_claim: "(1) write.py parse_script (~L574-595) splits at a `&&` ONLY when the text after it, stripped, starts with a known VERBS name followed by whitespace or end-of-string; every other `&&` stays inside the current verb's last free-text argument byte-for-byte (note, thought, set value, title). (2) A prose argument may therefore quote `set a b && note c` literally; a script that is ONLY verbs still parses exactly as today (every existing test_write* case byte-identical). (3) The refusal for a chunk that starts with an unknown verb names the chunk as today; no escaping syntax is introduced (the seam is the verb grammar itself, not a backslash). FALSIFIERS: a note whose text contains ' && set status x' followed by a real verb chunk changing status; an existing verb-only script parsing differently; an unknown-verb chunk silently absorbed into prose (it must still refuse by name when it is the FIRST token of the script). TESTS red-first: note with an embedded && quoted command lands verbatim in the note; note && set title still runs both; 'set title a && b && c' keeps 'b && c' in the title; unknown first verb refuses. FILE SCOPE: extensions/agi/bin/write.py (parse_script only) + tests/test_write.py. CEILING: <=8 production lines."
title: "SM.141 (director-sanctuary finding 06:5xZ 09-19: write.py parse_script splits on a literal && ANYWHERE in the joined string, including inside a note/thought free-text argument that quotes a joined command, with no escaping seam -- the measured way experiment:a00-794503d4's link_ref filled with leaked prose and crashed links.py links (OSError: file name too long) on the trunk until hand-fixed; goal:g4.18): write.py splits a script only at a && that BEGINS a verb, so prose keeps its own ampersands"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
