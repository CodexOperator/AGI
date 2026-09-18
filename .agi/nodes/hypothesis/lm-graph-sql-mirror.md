---
id: hypothesis:lm-graph-sql-mirror
mint_id: c0adbd447a414690be08cbdb63186b4a
type: hypothesis
parents:
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter; $0 compute; file scope = .agi/context/local-maxxing/sql/{graph2sql.py, schema.sql, test_graph2sql.py, INGEST.md} + the kid experiment node + this node; no engine file (graduation to extensions/ is a later g13/g15 decision).
edited_by: a00-3533a847
falsifier: Build > 300 s, or any id/edge missing or extra after a rebuild, or a standing query > 500 ms, or the DDL needs Postgres-incompatible SQLite-isms -- then the mirror is not a substitute surface and the idea stays file-only.
push_further: "Mirror is proved and live under .agi/context/local-maxxing/sql/. Next run: harden the one soft edge -- graph2sql.py query with the DEFAULT db path before build dies with sqlite3.OperationalError: no such table: nodes AND creates a zero-byte nodes.sqlite. Add a missing-db guard (clear message or auto-build) plus one regression test. Also wire the five standing queries into an actual loop surface (brief.py/zoom.py read path) if the town wants the db to earn its keep, else bank as file-only."
scaffold_hash: cbcaf32630749af3
season: 2
testable_claim: "graph2sql.py (kid-written, tests beside it) builds nodes.sqlite from .agi/nodes/**/*.md (frontmatter -> typed columns + a json column for the rest; body, thought, agent notes as text; edges table from parents/next_edges/evidence_runs; a files table with path, mint_id, sha256) in <= 60 s for the ~3.5k-node graph on this A1; (2) a round-trip check: every node id + every edge in the files appears in the db and nothing else (count and set equality, exit 0); (3) five standing queries (nodes by type+verdict+town; children of a goal; evidence_runs of a hypothesis; notes containing a term with dates; retired nodes with dangling supersedes) each < 50 ms; (4) the DDL runs unchanged on Postgres 16 (tested in a throwaway docker postgres on this box or SQL-syntax-checked with pglast if docker is unavailable, stated which); (5) an ingestion doc: how an agent reads the same graph in db form vs file form, one page."
tests: "ONE pi parent + ONE kid, A1-light class ($1 OpenRouter, $0 compute, no downloads except pip-free stdlib sqlite3; docker postgres only if already installed); the .sqlite file is gitignored (rebuilt, never committed); code + tests + DDL + the ingestion doc committed under .agi/context/local-maxxing/sql/; the parent re-runs the build + the round-trip check from a clean clone of the town branch. Owner 03:5xZ: use plain old SQL to own more of the stack; Neon key optional."
title: A plain-SQL mirror of the graph (SQLite file, Postgres-compatible DDL) rebuilt from .agi/nodes in under 60 s answers the loop everyday questions (by type/verdict/town/parent/edge, evidence_runs, notes by date) in milliseconds and stays byte-consistent with the files; git remains the source of truth
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-graph-sql-mirror

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
