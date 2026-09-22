---
id: hypothesis:lm-graph-sql-mirror
mint_id: c0adbd447a414690be08cbdb63186b4a
type: hypothesis
parents:
  - goal:g5.13
next_edges: []
ceiling: $1 OpenRouter; $0 compute; file scope = .agi/context/local-maxxing/sql/{graph2sql.py, schema.sql, test_graph2sql.py, INGEST.md} + the kid experiment node + this node; no engine file (graduation to extensions/ is a later g13/g15 decision).
edited_by: belam
falsifier: Build > 300 s, or any id/edge missing or extra after a rebuild, or a standing query > 500 ms, or the DDL needs Postgres-incompatible SQLite-isms -- then the mirror is not a substitute surface and the idea stays file-only.
push_further: "Mirror is proved and live under .agi/context/local-maxxing/sql/. Next run: harden the one soft edge -- graph2sql.py query with the DEFAULT db path before build dies with sqlite3.OperationalError: no such table: nodes AND creates a zero-byte nodes.sqlite. Add a missing-db guard (clear message or auto-build) plus one regression test. Also wire the five standing queries into an actual loop surface (brief.py/zoom.py read path) if the town wants the db to earn its keep, else bank as file-only."
scaffold_hash: cbcaf32630749af3
season: 2
testable_claim: "graph2sql.py (kid-written, tests beside it) builds nodes.sqlite from .agi/nodes/**/*.md (frontmatter -> typed columns + a json column for the rest; body, thought, agent notes as text; edges table from parents/next_edges/evidence_runs; a files table with path, mint_id, sha256) in <= 60 s for the ~3.5k-node graph on this A1; (2) a round-trip check: every node id + every edge in the files appears in the db and nothing else (count and set equality, exit 0); (3) five standing queries (nodes by type+verdict+town; children of a goal; evidence_runs of a hypothesis; notes containing a term with dates; retired nodes with dangling supersedes) each < 50 ms; (4) the DDL runs unchanged on Postgres 16 (tested in a throwaway docker postgres on this box or SQL-syntax-checked with pglast if docker is unavailable, stated which); (5) an ingestion doc: how an agent reads the same graph in db form vs file form, one page."
tests: "ONE pi parent + ONE kid, A1-light class ($1 OpenRouter, $0 compute, no downloads except pip-free stdlib sqlite3; docker postgres only if already installed); the .sqlite file is gitignored (rebuilt, never committed); code + tests + DDL + the ingestion doc committed under .agi/context/local-maxxing/sql/; the parent re-runs the build + the round-trip check from a clean clone of the town branch. Owner 03:5xZ: use plain old SQL to own more of the stack; Neon key optional."
thought_session: dissolve-legacy-2026-09-19
title: A plain-SQL mirror of the graph (SQLite file, Postgres-compatible DDL) rebuilt from .agi/nodes in under 60 s answers the loop everyday questions (by type/verdict/town/parent/edge, evidence_runs, notes by date) in milliseconds and stays byte-consistent with the files; git remains the source of truth
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-graph-sql-mirror

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 04:59Z (thought-master pane), verbatim: "I was thinking we could use the DB mirror to dynamically build jev prompts since it’s basically multiple choice and graph is the choice limiting engine." APPLY (thought-master): the mirror gets its FIRST CONSUMER -- a jev prompt builder. The graph is the choice-limiting engine: for an act, the mirror enumerates the LEGAL choice set (schema-legal parents and verbs for the node type, in-scope node ids, open hypotheses under the goal, the tool roster of that kid, the six verdict words), the builder renders it as a numbered multiple-choice prompt, and jev answers with an index + confidence -- generation becomes selection, which is what a small local model does well. For TM.31 (live now): a sixth standing query, choices-for-act (children of a goal by status, allowed parents from the schema, open hypotheses under a goal, kids by round) -- added by in-node rebrief if the parent can take it, else it is the first line of the R2 brief. Measured claim for R2 (hypothesis:lm-jev-next-call-suggestion): top-1 agreement rises as the graph shrinks the choice set; choice-set size is recorded per decision as the covariate.

REVIEWED BY NAME (thought-master 05:09Z): TM.31 ACCEPTED, verdict proved stands (kid experiment:a00-ba4206b3-02af63; build 7.1 s for 3492 nodes / 5470 edges, 0 missing / 0 extra on three independent reproductions; the parent 5 adversarial probes all held, including the injected-EXTRA-id/edge drift the kid own test missed; kid suite 7/7 in 42.5 s). Director judgment call ACCEPTED: the parent a00-3533a847 died with its work staged when the 04:33-04:47Z history rewrite moved the branch under it; the director verified the bytes three ways and committed the 7 round paths itself rather than re-dispatching -- right call, no spend, recorded here. Landed on local-maxxing/season1/main (gate: base 2262f365f live, clean after the origin merge, 0 deletions, links 3472/0, anonymization clean). Soft edge on record: query-before-build raises sqlite3.OperationalError and leaves a zero-byte db. NEXT ROUND = hypothesis:lm-mirror-choices-for-act (minted 05:09Z): the hardening + the choices-for-act query family the owner line above asks for -- the mirror becomes the menu that jev chooses from.
