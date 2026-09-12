---
id: hypothesis:l4-the-config-posts-note-is-silent-until-posts-md-exists-or-posts-md-is-minted-with-seats-as-its-alias
mint_id: c4273dc4ead7470893ccb2c6d93a7bd9
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: e984b579f42d9c92
season: 2
testable_claim: "goal:g15 FIX-ONLY node (owner order 15:4xZ relayed by master-sensei gen 4 (15:41Z; verbatim at doc:l4-owner-decisions latest note); cite at seat tip 290644b2b, re-measure on your base. line (1)). MEASURED: geometry_config.py:48-52 _FILE_DEP_MSG prints 'note: config:seats is deprecated; use config:posts (nodes/.geometry/posts.md with a posts: list). Falling back to the old seats.md layout this season.' on EVERY seats read by every bin, and nodes/.geometry/posts.md does NOT exist (ls .agi/nodes/.geometry: commands.md crons.md ladder.md rotations.md seats.md secrets.md workflows.md) — a note pointing at a file that is not there trains every model that reads a STARTUP to copy stale --post/--seat arguments; the Sensei already swapped the template's five first_turn '--seat' sites to '--post' (848fa20fd). CLAIM: the kid picks ONE of two and names it: (A) the note is printed only when posts.md exists and seats.md is still the one being read (a real migration hint), silent otherwise; or (B) posts.md is minted from the current seats.md rows (a posts: list, same cells) and seats.md becomes the alias the reader falls back to, the note then true. Either way: zero occurrences of the note in a fresh STARTUP on this tree, every reader of seats rows unchanged in behaviour, the schema test for config nodes green. FALSIFIERS: a bin invocation on this tree still prints the note while posts.md is absent (A) or posts.md exists but a reader still reads seats.md first without the alias (B); any seat-row read changes result. TESTS: test_geometry_config.py (or the reader's test file) — note silent when posts.md absent / present-and-primary when it exists; a row read equality test across the two layouts. FILE SCOPE: extensions/agi/bin/geometry_config.py — the note gate (A) or the posts reader + alias (B); nodes/.geometry/posts.md only under (B); the reader's test file. EXCLUDED: rotations.md templates, send.py, rotate.py. CEILING: one gate or one file + one alias, two tests."
thought_session: sensei-director-genXIII-L13
title: the 'config:seats is deprecated; use config:posts' note is not printed while nodes/.geometry/posts.md does not exist — or posts.md is minted from the seats.md rows with seats.md as the alias — so no post copies a stale argument at spawn
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-config-posts-note-is-silent-until-posts-md-exists-or-posts-md-is-minted-with-seats-as-its-alias

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
