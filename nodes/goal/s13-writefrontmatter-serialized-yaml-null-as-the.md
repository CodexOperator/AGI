---
confidence: 1.0
goal_id: S13
goal_kind: short-term
heading_level: 2
id: "goal:s13"
mint_id: 199d522645cc4f84957fd23fda49dfc7
order: 61
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
title: "S13: `write_frontmatter` serialized YAML null as the string \"None\""
type: goal
---

Fixed 2026-08-25. `write_frontmatter` in `bin/snapshot-goals.py` — the **shared**
serializer that `level3.py` and `decompose-engine.py` import by file path
specifically so there is one writer and no field erasure — turned a real YAML
`null` into the four-character string `None` on re-serialize.

Silent, and invisible at small scale: it only surfaced when the mint-id backfill
wrote every node in the corpus at once. **10 nodes were already damaged.** In at
least one, an empty `parents:` entry became a dangling reference to a node
literally named `None` — a fabricated edge, which is the G7.1 referential-
integrity failure produced by the writer rather than by an author.

Fixed additively with 3 regression tests; the 10 damaged files were repaired in
the same pass and the corpus verified clean (`grep` for the pattern returns
nothing).

Recorded because the *class* matters more than the instance: the one function
guaranteed to touch every node on every generator run is the one place a silent
serialization bug scales to the whole corpus before anyone notices. It was found
only because an unrelated task happened to write all 832 files at once. **Any
future change to a shared writer deserves a corpus-wide round-trip test, not a
unit test on one node.**

Open, deliberately not claimed as done: nodes damaged and committed *before*
2026-08-25 were repaired in the working tree, but no audit was run over git
history to find earlier instances that may have been overwritten since.
