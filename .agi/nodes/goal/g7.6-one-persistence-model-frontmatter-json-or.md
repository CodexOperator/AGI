---
id: goal:g7.6
mint_id: 8e22076aae704400b6c0271281a1aaed
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.6
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.6: One persistence model: frontmatter, JSON, or a database"
---
Three representations exist and none is authoritative. Markdown frontmatter is
what the loop actually reads and writes. A JSON/SQLite backend exists
(`graph_core/persistence/sqlite_backend.py`, `db_loader.py`, plus a one-shot
migration script) and is wired into the snapshot scripts behind a config key —
but agi-tree's own `persistence` block was removed this session because the
project's vendored `graph_core` predates the backend entirely.

The question to settle deliberately: **unify on one, support both honestly, or
migrate to a real database.** The case for a database is not tidiness — it is
that several defects this session are *schema problems wearing filesystem
clothes*: duplicate ids (G7.2, G7.4) cannot happen under a primary key; dangling
references (G7.1) are a foreign-key constraint; unresolvable `evidence_runs`
(G3.1) is a join. A store that can express those constraints removes whole
classes of bug rather than detecting them after the fact.

The case against is equally real: frontmatter is human-editable, greppable,
diffable, and it is what makes the git grid work at all — a node's version
history is a file's history. A database gives that up unless the grid is
rebuilt on top of it.

Absorbs **H1** (DB-only state migration, long carried as P0) and **H2** (import
the historical corpus). Decide before building either: H1 has sat at P0 without
the decision being made, which is why it never moved.