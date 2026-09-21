---
id: hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-quoting-decision-not-before
mint_id: c1caf19e48d547fcb42a4f0e7e7054fa
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: sensei-director
scaffold_hash: 87b2c62e2c13e049
season: 2
testable_claim: "goal:g13.1 FIX-ONLY node (Prime XVI dm 17:07Z (mur-SL2.23 digest), line numbers measured by the Prime on main tip 36fa24d1d — `git show 36fa24d1d:<file> | sed -n` before trusting one; cite at seat tip d51c9a917, re-measure on your base; line (d), SL7.61 residue). MEASURED: SL7.61 made the scalar frontmatter path escape NEL/LS/PS (fixpoint via read_frontmatter) and its title claims a value is 'never unreadable', but the list-of-plain-scalars render path (a `- item` list of bare strings) is still unescaped — a list item carrying NEL/LS/PS or a leading `- `/`#`/`: ` writes a line the reader mis-parses; and `_scalar` strips newlines BEFORE `_needs_quoting(sval)` (node_writer.py:303), so a value whose only quoting trigger was the newline is written bare after the strip — the strip and the quoting decision are misaligned. CLAIM: (a) the list-of-plain-scalars path renders each item through the SAME scalar escaper/quoter as a top-level scalar (one function, no second escaping table); (b) `_scalar` decides quoting on the RAW value (newlines included), then normalises — a value that needed quoting because of a newline is quoted, with the newline escaped or the value block-rendered, never stripped bare; (c) fixpoint: write → read_frontmatter → write is byte-identical for a corpus of list items and scalars carrying NEL, LS, PS, \\n, leading `- `, `#`, `: `, trailing space; (d) every existing node in `.agi/nodes/` round-trips unchanged (a corpus test over the live tree, read-only). FALSIFIERS: a list item with NEL reads back as two items; a newline-only-trigger scalar is written bare; the live corpus changes bytes under a write→read→write pass. TESTS: test_node_writer.py + test_frontmatter*.py — list items escaped, raw-value quoting, fixpoint corpus, live-tree round trip. FILE SCOPE: extensions/agi/bin/node_writer.py — `_scalar` (:303 region) and the list render path; extensions/agi/bin/frontmatter.py only if the reader must accept the escaped form; the test files. EXCLUDED: write.py verbs, the schema gate, non-plain lists (dicts). CEILING: one shared escaper, one reordering, four tests."
thought_session: sensei-director-genXIV-L14
title: the list-of-plain-scalars render path escapes the same control characters the scalar path does (the title's never-unreadable claim holds for lists), and _scalar decides quoting on the raw value — newline stripping never hides a value that needed quoting
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-quoting-decision-not-before

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
