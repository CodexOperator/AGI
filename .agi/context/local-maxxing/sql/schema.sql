-- schema.sql -- the graph mirror's DDL. It runs UNCHANGED on SQLite (stdlib
-- sqlite3) and on PostgreSQL 16: no AUTOINCREMENT, no PRAGMA, no WITHOUT ROWID,
-- no SQLite-only type names. Verified against postgres:16 in docker.
--
-- git is the source of truth; this file only describes the query mirror that
-- graph2sql.py rebuilds from .agi/nodes/**/*.md.

CREATE TABLE IF NOT EXISTS nodes (
    id           TEXT PRIMARY KEY,   -- frontmatter `id` (mint-address, e.g. goal:g14)
    mint_id      TEXT,               -- stable mint id, never changes
    type         TEXT NOT NULL,      -- goal | hypothesis | experiment | verdict | ...
    title        TEXT,
    town         TEXT,
    verdict      TEXT,               -- the enum, when the node carries one
    status       TEXT,               -- active | deprecated | ...
    confidence   REAL,
    season       INTEGER,
    supersedes   TEXT,               -- typed so the dangling-ref query is a join
    retired      INTEGER NOT NULL DEFAULT 0,  -- status=deprecated or /deprecated/ path
    body         TEXT,               -- node body after the closing ---
    thought      TEXT,               -- the THOUGHT:BEGIN region, if any
    agent_notes  TEXT,               -- the `## Agent Notes` section, if any
    note_dates   TEXT,               -- comma-joined YYYY-MM-DD found in agent_notes
    json         JSON                -- every remaining frontmatter key
);

CREATE TABLE IF NOT EXISTS edges (
    src  TEXT NOT NULL,              -- the node the edge leaves
    dst  TEXT NOT NULL,              -- its target (may dangle)
    kind TEXT NOT NULL,              -- parents | next_edges | evidence_runs
    PRIMARY KEY (src, dst, kind)
);

CREATE TABLE IF NOT EXISTS files (
    path    TEXT PRIMARY KEY,        -- repo-relative, e.g. .agi/nodes/goal/g14.md
    mint_id TEXT,
    sha256  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_nodes_type_verdict_town ON nodes(type, verdict, town);
CREATE INDEX IF NOT EXISTS idx_nodes_retired ON nodes(retired);
CREATE INDEX IF NOT EXISTS idx_edges_src_kind ON edges(src, kind);
CREATE INDEX IF NOT EXISTS idx_edges_dst_kind ON edges(dst, kind);
