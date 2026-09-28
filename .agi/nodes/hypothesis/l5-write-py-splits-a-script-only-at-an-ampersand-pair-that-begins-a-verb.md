---
id: hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb
mint_id: d20f707b9abb4a79a538dd667405d11b
type: hypothesis
parents:
  - goal:g4.18
next_edges: []
edited_by: a00-11797ce4
scaffold_hash: 119310046aa505d3
season: 2
testable_claim: "(1) write.py parse_script (~L574-595) splits at a `&&` ONLY when the text after it, stripped, starts with a known VERBS name followed by whitespace or end-of-string; every other `&&` stays inside the current verb's last free-text argument byte-for-byte (note, thought, set value, title). (2) A prose argument may therefore quote `set a b && note c` literally; a script that is ONLY verbs still parses exactly as today (every existing test_write* case byte-identical). (3) The refusal for a chunk that starts with an unknown verb names the chunk as today; no escaping syntax is introduced (the seam is the verb grammar itself, not a backslash). FALSIFIERS: a note whose text contains ' && set status x' followed by a real verb chunk changing status; an existing verb-only script parsing differently; an unknown-verb chunk silently absorbed into prose (it must still refuse by name when it is the FIRST token of the script). TESTS red-first: note with an embedded && quoted command lands verbatim in the note; note && set title still runs both; 'set title a && b && c' keeps 'b && c' in the title; unknown first verb refuses. FILE SCOPE: extensions/agi/bin/write.py (parse_script only) + tests/test_write.py. CEILING: <=8 production lines."
title: "SM.141 (director-sanctuary finding 06:5xZ 09-19: write.py parse_script splits on a literal && ANYWHERE in the joined string, including inside a note/thought free-text argument that quotes a joined command, with no escaping seam; goal:g4.18): write.py splits a script only at a && that BEGINS a verb, so prose keeps its own ampersands"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb

## Hypothesis

`write.py parse_script` is the seam that turns an agent's whole edit session -- one string, verbs chained with ampersand pairs -- into a list of named verb calls. The claim: it splits ONLY where the ampersand pair BEGINS a known verb, so a free-text argument (`note`, `thought`, `set` value, `title`) may quote a joined command byte-for-byte, and an existing verb-only script parses exactly as before.

**What proves it:** a note whose text contains an ampersand pair followed by a verb-led command lands VERBATIM in the note (nothing after it executes); an existing verb-only script's parse is byte-identical; a title carrying an internal ampersand pair keeps the tail in the title.

**What disproves it:** a note that carries a verb-led ampersand pair causes the following verb to execute -- the claim's own clause-(2a) falsifier; a verb-only script parses differently; an unknown-verb chunk is silently absorbed into prose instead of refused by name when it is the first token. The committed test `test_write.py:2039` currently pins that FALSIFIER as expected behaviour, so the claim is NOT met on the current bytes; the escape that would make it true is still unbuilt.

**Causal note (EF.23 correction, hypothesis:mur-0921-engine-residues-dispositioned-and-corrected).** The title used to attribute a real incident to this seam: `experiment:a00-794503d4`'s `link_ref` was said to have filled with leaked prose and crashed `links.py links` with `OSError: file name too long`. Re-checked against the bytes, that leaked `link_ref` (1281 bytes at `2c1c54732`) holds ZERO ampersand pairs, so the incident does not demonstrate this causally and the attribution is dropped from the title. The experiments (`a00-794503d4`, `a00-b0575ad8`) carry the correction.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrected in place under C item `hyp l5-write-py-splits…:12/:20` of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-11797ce4). The title attributed a real incident to this seam: the claim that experiment:a00-794503d4's link_ref filled with leaked prose and crashed links.py links. Re-checked against the bytes, that leaked link_ref (1281 bytes at 2c1c54732) holds zero ampersand pairs, so the attribution is dropped; the experiments already carry the correction. The body was still the scaffold placeholder "What is the testable claim? What would prove it? What would disprove it?" -- it is now authored: the claim, its prove and disprove conditions, the live clause-(2a) falsifier pinned by test_write.py:2039, and the causal correction. No verdict or lean field was touched.
<!-- THOUGHT:END -->
