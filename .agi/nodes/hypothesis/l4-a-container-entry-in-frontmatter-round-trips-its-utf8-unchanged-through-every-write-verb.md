---
id: hypothesis:l4-a-container-entry-in-frontmatter-round-trips-its-utf8-unchanged-through-every-write-verb
mint_id: 4d2612c2ad58434d8a79040527d9c976
type: hypothesis
parents:
  - goal:g13.1
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: ffd993b09259d4e4
season: 2
testable_claim: "goal:g13.1 FIX-ONLY node (write.py: a human edit is an engine action), asked by the Sensei (master-sensei wake-audit 11:52Z, by name: a write.py replace body 56:56 on config:rotations re-serialized two unrelated ack first_turn entries, em-dash -> —, ensure_ascii on the JSON-in-YAML strings, and added the EOF newline; the Sensei restored the two lines by hand before committing f3e5f90ea; a one-line body edit should touch one line). Cite at 879a97516; re-measure on your base. MEASURED: every write.py verb re-renders the WHOLE frontmatter through node_writer.render_frontmatter -> _render_value, and a list entry that is a container is rendered at node_writer.py:338 as json.dumps(i) with the default ensure_ascii=True, so every non-ASCII character inside a JSON-in-YAML entry is escaped on any write, related to the edit or not. Proved in-process on the seat: frontmatter.read_frontmatter parses both a literal em-dash and a — escape to the same dict, and render_frontmatter emits — for both — the tree already carries the mixed state (nodes/.geometry/rotations.md: the join and reap-proof first_turn entries at lines 65/68/106/109 carry — from earlier engine writes, the ack entries at 67/108 carry the literal em-dash from the hand restore). The EOF half is node_writer.py:876-877 (text.rstrip newlines + one newline): a file that lacked its EOF newline gains one on the first engine write — a documented single-EOF rule, one-time, NOT in scope. CLAIM: json.dumps(i, ensure_ascii=False) at that one site; a container entry carrying non-ASCII round-trips byte-identical through set/note/thought/replace, and an entry that already carries — escapes is normalized ONCE to the literal characters on its next engine write (expected, named in the kid node; the four rotations.md entries will normalize on the next engine write of config:rotations — do not hand-edit rotations.md in this round). FALSIFIERS: a note on a node whose frontmatter carries a list-of-dict entry with an em-dash changes that entry line; a frontmatter round trip of such an entry through read_frontmatter -> render_frontmatter is not byte-identical for a literal-UTF-8 entry; a reader of the emitted line (frontmatter.read_frontmatter, rotate.py first_turn loader) fails on a literal non-ASCII char. TESTS: test_node_writer.py — a round-trip test on a node file carrying a first_turn-style list-of-dict entry with an em-dash and one with a — escape: after write.py <id> note x the literal entry is byte-identical and the escaped one reads as the literal (the one-time normalization, asserted by name); the existing serializer tests unchanged. FILE SCOPE: extensions/agi/bin/node_writer.py — _render_value, that one json.dumps call only; extensions/agi/tests/test_node_writer.py. EXCLUDED: the single-EOF rule at 876-877; every other verb, the reader, config:rotations itself, write.py. CEILING: one keyword argument, one test; no serializer redesign."
thought_session: sensei-director-genXII-L12
title: a list-of-dict frontmatter entry round-trips its UTF-8 unchanged through every write.py verb, so a one-line body edit touches one line
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-container-entry-in-frontmatter-round-trips-its-utf8-unchanged-through-every-write-verb

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
