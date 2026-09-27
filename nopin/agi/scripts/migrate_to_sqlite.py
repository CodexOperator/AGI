#!/usr/bin/env python3
"""One-shot migration: filesystem node directory -> SQLite database.

Reads every .md/.json file under the source directory, skips files that
appear in .gitignore, and upserts all nodes into a SQLite database.

Usage:
    python scripts/migrate_to_sqlite.py /path/to/nodes/ /path/to/nodes.db

After migration the DB contains all nodes. Edges are NOT migrated (they live
in frontmatter parent/child fields and are reconstructed on load).
"""

from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path

# Add source tree to path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph_core.persistence.frontmatter import load_node_file
from graph_core.persistence.sqlite_backend import SQLiteBackend


def _walk_files(base: Path):
    """Sorted walk of .md/.json files, skipping gitignored ones."""
    rules: list[str] = []
    gi_path = base / ".gitignore"
    if gi_path.exists():
        for line in gi_path.read_text().splitlines():
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            rules.append(line)

    def is_ignored(p: Path) -> bool:
        if not rules:
            return False
        import fnmatch
        rel = str(p.relative_to(base))
        for rule in rules:
            neg = False
            r = rule
            if rule.startswith("!"):
                neg = True
                r = rule[1:]
            if fnmatch.fnmatch(rel, r) or fnmatch.fnmatch(p.name, r):
                return not neg
        return False

    for root, dirs, files in os.walk(base):
        dirs.sort()
        for fname in sorted(files):
            p = Path(root) / fname
            if p.suffix.lower() not in {".md", ".json"}:
                continue
            if is_ignored(p):
                continue
            yield p


def migrate(nodes_dir: Path, db_path: Path) -> None:
    files = list(_walk_files(nodes_dir))
    print(f"Found {len(files)} node files -> {db_path}")

    # Use batch inserts for speed
    BATCH = 500
    with SQLiteBackend(db_path) as backend:
        conn = backend._get_conn()
        batch: list[tuple] = []
        written = 0
        errors = 0

        for i, p in enumerate(files):
            try:
                nf = load_node_file(p)
            except Exception as e:
                warnings.warn(f"skipping {p}: {e}")
                errors += 1
                continue

            node_id = nf.frontmatter.get("id")
            if not node_id:
                node_id = p.stem
                nf.frontmatter["id"] = node_id

            parents = json.dumps(list(nf.frontmatter.get("parents", [])))
            children = json.dumps(list(nf.frontmatter.get("children", [])))
            tags = json.dumps(list(nf.frontmatter.get("tags", [])))
            batch.append((
                node_id,
                str(nf.frontmatter.get("type", "node")),
                nf.frontmatter.get("payload_ref"),
                parents,
                children,
                tags,
                nf.frontmatter.get("origin"),
                nf.body,
            ))

            if len(batch) >= BATCH:
                conn.executemany(
                    """
                    INSERT OR REPLACE INTO nodes
                    (id, type, payload_ref, parents, children, tags, origin, body)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    batch,
                )
                conn.commit()
                written += len(batch)
                batch = []
                print(f"  {written}/{len(files)} nodes written")

        # Flush remaining
        if batch:
            conn.executemany(
                """
                INSERT OR REPLACE INTO nodes
                (id, type, payload_ref, parents, children, tags, origin, body)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                batch,
            )
            conn.commit()
            written += len(batch)

        # Persist counts
        backend._update_counts(conn)

    print(f"Migration complete: {written} nodes written, {errors} errors")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: migrate_to_sqlite.py <nodes_dir> <db_path>")
        sys.exit(1)
    nodes_dir = Path(sys.argv[1]).resolve()
    db_path = Path(sys.argv[2]).resolve()
    if not nodes_dir.is_dir():
        print(f"Error: {nodes_dir} is not a directory")
        sys.exit(1)
    migrate(nodes_dir, db_path)
