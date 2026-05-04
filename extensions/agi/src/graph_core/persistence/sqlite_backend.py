"""SQLite persistence backend (T-015 / R8 alternative).

Stores all node data in a single SQLite database file.
Nodes are serialised with their frontmatter fields + body.
Edges stored separately with a unique constraint on (source_id, target_id, relation).
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterator

from .backend import PersistenceBackend
from .frontmatter import NodeFile


class SQLiteBackend:
    """SQLite backend for graph-core nodes.

    Schema
    ------
    nodes: id PK, type, payload_ref, parents JSON, children JSON,
           tags JSON, origin, body TEXT
    edges: id PK autoincrement, source_id, target_id, relation, tags JSON
           UNIQUE(source_id, target_id, relation)
    metadata: key PK, value
    Indexes on edges(source_id) and edges(target_id) for fast traversal.
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS nodes (
        id          TEXT PRIMARY KEY,
        type        TEXT NOT NULL,
        payload_ref TEXT,
        parents     TEXT NOT NULL DEFAULT '[]',
        children    TEXT NOT NULL DEFAULT '[]',
        tags        TEXT NOT NULL DEFAULT '[]',
        origin      TEXT,
        body        TEXT NOT NULL DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS edges (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id  TEXT NOT NULL,
        target_id  TEXT NOT NULL,
        relation   TEXT NOT NULL,
        tags       TEXT NOT NULL DEFAULT '[]',
        UNIQUE(source_id, target_id, relation)
    );

    CREATE INDEX IF NOT EXISTS idx_edges_out ON edges(source_id);
    CREATE INDEX IF NOT EXISTS idx_edges_in  ON edges(target_id);

    CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT);
    """

    CURRENT_VERSION = 1

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._conn: sqlite3.Connection | None = None
        self._last_mtime: float | None = None
        self._ensure_db()

    # --- Connection management ---

    def _ensure_db(self) -> None:
        if self._db_path.exists():
            return
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self._connect()
        conn.executescript(self.SCHEMA)
        conn.execute(
            "INSERT OR IGNORE INTO metadata (key, value) VALUES (?, ?)",
            ("version", str(self.CURRENT_VERSION)),
        )
        conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = self._connect()
        return self._conn

    def _close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # --- PersistenceBackend surface ---

    def load(self, path: str | Path) -> NodeFile:
        """Load a node by id (path is treated as the node id).

        Returns NodeFile(frontmatter, body, suffix='.json').
        The frontmatter contains all node fields EXCEPT 'body';
        body is returned separately in NodeFile.body.
        """
        conn = self._get_conn()
        row = conn.execute(
            "SELECT id, type, payload_ref, parents, children, tags, origin, body FROM nodes WHERE id = ?",
            (str(path),),
        ).fetchone()
        if row is None:
            from .frontmatter import FrontmatterError

            raise FrontmatterError(f"node not found in DB: {path}")
        fm: dict[str, Any] = {
            "id": row["id"],
            "type": row["type"],
            "payload_ref": row["payload_ref"],
            "parents": json.loads(row["parents"]),
            "children": json.loads(row["children"]),
            "tags": json.loads(row["tags"]),
            "origin": row["origin"],
        }
        return NodeFile(frontmatter=fm, body=row["body"], suffix=".json")

    def save(self, path: str | Path, nf: NodeFile) -> None:
        """Upsert a node. Extracts 'body' from frontmatter, stores rest as JSON columns."""
        conn = self._get_conn()
        fm = dict(nf.frontmatter)
        body = fm.pop("body", nf.body)
        node_id = str(path)
        parents = json.dumps(list(fm.get("parents", [])))
        children = json.dumps(list(fm.get("children", [])))
        tags = json.dumps(list(fm.get("tags", [])))
        conn.execute(
            """
            INSERT INTO nodes (id, type, payload_ref, parents, children, tags, origin, body)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                type        = excluded.type,
                payload_ref = excluded.payload_ref,
                parents     = excluded.parents,
                children    = excluded.children,
                tags        = excluded.tags,
                origin      = excluded.origin,
                body        = excluded.body
            """,
            (
                node_id,
                str(fm.get("type", "node")),
                fm.get("payload_ref"),
                parents,
                children,
                tags,
                fm.get("origin"),
                body,
            ),
        )
        conn.commit()
        self._update_counts(conn)

    def list(self, directory: str | Path) -> Iterator[Path]:
        """Return an iterator of all node ids as Path objects."""
        conn = self._get_conn()
        rows = conn.execute("SELECT id FROM nodes ORDER BY id").fetchall()
        for row in rows:
            yield Path(row["id"])

    def watch(self, directory: str | Path) -> Iterator[Path]:
        """Poll-based watcher. Yields all node paths if DB mtime changed since last call."""
        try:
            mtime = os.stat(self._db_path).st_mtime
        except OSError:
            return
        if self._last_mtime is not None and mtime == self._last_mtime:
            return
        self._last_mtime = mtime
        yield from self.list(directory)

    # --- Edge helpers (used by Graph persistence layer) ---

    def load_edges(self) -> list[dict[str, Any]]:
        """Return all edges as dicts."""
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT source_id, target_id, relation, tags FROM edges"
        ).fetchall()
        return [
            {
                "source_id": r["source_id"],
                "target_id": r["target_id"],
                "relation": r["relation"],
                "tags": json.loads(r["tags"]),
            }
            for r in rows
        ]

    def save_edge(self, source_id: str, target_id: str, relation: str, tags: set[str]) -> None:
        """Insert or ignore an edge."""
        conn = self._get_conn()
        tags_json = json.dumps(list(tags))
        conn.execute(
            """
            INSERT OR IGNORE INTO edges (source_id, target_id, relation, tags)
            VALUES (?, ?, ?, ?)
            """,
            (source_id, target_id, relation, tags_json),
        )
        conn.commit()
        self._update_counts(conn)

    def remove_edge(self, source_id: str, target_id: str, relation: str) -> bool:
        """Remove an edge. Returns True if removed."""
        conn = self._get_conn()
        cur = conn.execute(
            "DELETE FROM edges WHERE source_id = ? AND target_id = ? AND relation = ?",
            (source_id, target_id, relation),
        )
        conn.commit()
        self._update_counts(conn)
        return cur.rowcount > 0

    def clear_edges(self) -> None:
        """Remove all edges."""
        conn = self._get_conn()
        conn.execute("DELETE FROM edges")
        conn.commit()
        self._update_counts(conn)

    def node_count(self) -> int:
        """Cached node count; falls back to live COUNT if metadata missing."""
        conn = self._get_conn()
        row = conn.execute(
            "SELECT value FROM metadata WHERE key = 'node_count'"
        ).fetchone()
        if row and row["value"] not in (None, "", "0"):
            return int(row["value"])
        # Fallback: live count from table
        return conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]

    def edge_count(self) -> int:
        """Cached edge count; falls back to live COUNT if metadata missing."""
        conn = self._get_conn()
        row = conn.execute(
            "SELECT value FROM metadata WHERE key = 'edge_count'"
        ).fetchone()
        if row and row["value"] not in (None, "", "0"):
            return int(row["value"])
        # Fallback: live count from table
        return conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]

    def _update_counts(self, conn: sqlite3.Connection) -> None:
        n = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        e = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES ('node_count', ?)",
            (str(n),),
        )
        conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES ('edge_count', ?)",
            (str(e),),
        )
        conn.commit()

    # --- Context manager ---

    def __enter__(self) -> "SQLiteBackend":
        return self

    def __exit__(self, *args: Any) -> None:
        self._close()

    # --- Protocol check (static) ---

    def _protocol_check() -> None:
        b: PersistenceBackend = SQLiteBackend(":memory:")
        _ = b
