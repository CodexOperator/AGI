#!/usr/bin/env python3
"""graph2sql.py -- a one-way SQL mirror of the thoughtgraph.

`.agi/nodes/**/*.md` (including the `deprecated/` sibling trees) -> one SQLite
file. git stays the source of truth; this is a query surface, rebuilt not
committed. The DDL lives in schema.sql and runs unchanged on Postgres 16.

  graph2sql.py build   [--nodes DIR] [--db PATH]   # build the file (<= 60 s)
  graph2sql.py --verify [--nodes DIR] [--db PATH]  # set-equality round trip
  graph2sql.py query <name> [terms...]             # the five standing queries
  graph2sql.py ddl                                 # print schema.sql

stdlib only for the mirror itself (sqlite3); PyYAML is preferred for the
frontmatter when present, with a flat stdlib fallback so it still builds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema.sql"

#: frontmatter keys promoted to typed columns; everything else lands in `json`.
TYPED = ("id", "mint_id", "type", "title", "town", "verdict", "status",
         "confidence", "season", "supersedes")
NODE_COLS = ("id", "mint_id", "type", "title", "town", "verdict", "status",
             "confidence", "season", "supersedes", "retired", "body", "thought",
             "agent_notes", "note_dates", "json")
EDGE_KEYS = ("parents", "next_edges", "evidence_runs")
_FM_LINE = re.compile(r"^---[ \t]*\r?$")


def find_root(start: Path | None = None) -> Path:
    """Nearest enclosing dir holding `.agi/config.json`."""
    p = Path(start or HERE).resolve()
    for d in (p, *p.parents):
        if (d / ".agi" / "config.json").is_file():
            return d
    raise SystemExit(f"graph2sql: no .agi/config.json above {p}")


def split_frontmatter(text: str):
    lines = text.split("\n")
    if not lines or not _FM_LINE.match(lines[0]):
        return "", text
    for i in range(1, len(lines)):
        if _FM_LINE.match(lines[i]):
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", text


def _mini_yaml(raw: str) -> dict:
    """Flat fallback: top-level `key: value` and `- item` list entries only."""
    out: dict = {}
    key = None
    for line in raw.split("\n"):
        m = re.match(r"^([A-Za-z_][\w]*):(.*)$", line)
        if m:
            key, val = m.group(1), _scalar(m.group(2).strip())
            out[key] = val if val is not None else []
        elif key is not None and re.match(r"^\s+-\s+", line):
            if not isinstance(out.get(key), list):
                out[key] = []
            out[key].append(_scalar(re.sub(r"^\s+-\s+", "", line).strip()))
    return out


def _scalar(v: str):
    if v in ("", "~", "null"):
        return None
    if v == "[]":
        return []
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def parse_frontmatter(raw: str) -> dict:
    if not raw:
        return {}
    try:
        import yaml
        data = yaml.safe_load(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return _mini_yaml(raw)


def _as_list(v) -> list:
    if v is None:
        return []
    return list(v) if isinstance(v, list) else [v]


def _num(v):
    return v if isinstance(v, (int, float)) else None


def _int(v):
    return int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def read_node(path: Path, root: Path):
    """(row, edges, file_row) for one node file with a frontmatter `id`."""
    text = path.read_text(encoding="utf-8", errors="replace")
    raw, body = split_frontmatter(text)
    fm = parse_frontmatter(raw)
    if not fm.get("id"):
        return None
    thought = notes = ""
    m = re.search(r"<!-- THOUGHT:BEGIN.*?-->(.*?)<!-- THOUGHT:END -->", body, re.S)
    if m:
        thought = m.group(1).strip()
    m = re.search(r"^## Agent Notes[ \t]*$(.*?)(?=^## |\Z)", body, re.S | re.M)
    if m:
        notes = m.group(1).strip()
    sup = fm.get("supersedes")
    if isinstance(sup, list):
        sup = sup[0] if sup else None
    row = {
        "id": str(fm.get("id")), "mint_id": fm.get("mint_id"),
        "type": fm.get("type"), "title": fm.get("title"), "town": fm.get("town"),
        "verdict": fm.get("verdict"), "status": fm.get("status"),
        "confidence": _num(fm.get("confidence")), "season": _int(fm.get("season")),
        "supersedes": str(sup) if sup is not None else None,
        "retired": int(str(fm.get("status")) == "deprecated" or "deprecated" in path.parts),
        "body": body, "thought": thought, "agent_notes": notes,
        "note_dates": ",".join(sorted(set(re.findall(r"\d{4}-\d{2}-\d{2}", notes)))),
        "json": json.dumps({k: v for k, v in fm.items() if k not in TYPED},
                           ensure_ascii=False, default=str),
    }
    edges = [(row["id"], str(d), k) for k in EDGE_KEYS for d in _as_list(fm.get(k))]
    rel = str(path.relative_to(root))
    files = (rel, fm.get("mint_id"), hashlib.sha256(text.encode("utf-8")).hexdigest())
    return row, edges, files


def iter_files(nodes_dir: Path):
    return sorted(p for p in nodes_dir.rglob("*.md") if p.is_file())


def build(root: Path, nodes_dir: Path, db_path: Path, quiet: bool = False,
          files: list[Path] | None = None):
    """`files` freezes the file set ONCE: on a live graph other agents write nodes
    while a mirror is being built, and a re-glob afterwards compares the db against a
    tree that moved (the DH.387 `FAIL 127 passed, 1 failed` flake, cause measured in
    .agi/sessions/iter-DH.393/a00-6f88eaa5/probe_toctou.py). Pass one snapshot to
    build/verify/file_sets to compare a set with itself."""
    ddl = SCHEMA.read_text(encoding="utf-8")
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    try:
        con.executescript(ddl)
        n_nodes = n_edges = n_files = 0
        placeholders = ",".join("?" for _ in NODE_COLS)
        for path in (iter_files(nodes_dir) if files is None else files):
            parsed = read_node(path, root)
            if parsed is None:
                continue
            row, edges, files = parsed
            con.execute(f"INSERT OR REPLACE INTO nodes ({','.join(NODE_COLS)}) "
                        f"VALUES ({placeholders})", tuple(row[c] for c in NODE_COLS))
            con.executemany("INSERT OR REPLACE INTO edges (src,dst,kind) VALUES (?,?,?)", edges)
            con.execute("INSERT OR REPLACE INTO files (path,mint_id,sha256) VALUES (?,?,?)", files)
            n_nodes += 1
            n_edges += len(edges)
            n_files += 1
        con.commit()
        try:  # FTS5 is SQLite-only; it never enters schema.sql (Postgres 16)
            con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(id UNINDEXED, notes)")
            con.execute("INSERT INTO notes_fts(id,notes) SELECT id,agent_notes FROM nodes "
                        "WHERE agent_notes IS NOT NULL AND agent_notes<>''")
            con.commit()
        except sqlite3.OperationalError:
            pass  # no FTS5 in this build -> notes_with_dates falls back to LIKE
        if not quiet:
            print(f"nodes={n_nodes} edges={n_edges} files={n_files} -> {db_path}")
        return n_nodes, n_edges, n_files
    finally:
        con.close()


def file_sets(root: Path, nodes_dir: Path, files: list[Path] | None = None):
    ids, edges = set(), set()
    for path in (iter_files(nodes_dir) if files is None else files):
        parsed = read_node(path, root)
        if parsed is None:
            continue
        ids.add(parsed[0]["id"])
        edges.update(parsed[1])
    return ids, edges


def verify(root: Path, nodes_dir: Path, db_path: Path, files: list[Path] | None = None) -> int:
    """Set equality: every file id/edge is in the db and nothing else. 0 on match."""
    if not db_path.exists():
        print(f"verify: {db_path} absent -- building it first")
        build(root, nodes_dir, db_path, quiet=True, files=files)
    want_ids, want_edges = file_sets(root, nodes_dir, files=files)
    con = sqlite3.connect(db_path)
    try:
        got_ids = {r[0] for r in con.execute("SELECT id FROM nodes")}
        got_edges = set(con.execute("SELECT src,dst,kind FROM edges"))
    finally:
        con.close()
    missing_ids, extra_ids = want_ids - got_ids, got_ids - want_ids
    missing_edges, extra_edges = want_edges - got_edges, got_edges - want_edges
    for label, miss, extra in (("id", missing_ids, extra_ids), ("edge", missing_edges, extra_edges)):
        for x in sorted(miss)[:20]:
            print(f"  MISSING {label}: {x}")
        for x in sorted(extra)[:20]:
            print(f"  EXTRA {label}: {x}")
    ok = not (missing_ids or extra_ids or missing_edges or extra_edges)
    print(f"verify: ids {len(want_ids)}/{len(got_ids)} edges {len(want_edges)}/{len(got_edges)} "
          f"missing={len(missing_ids)+len(missing_edges)} extra={len(extra_ids)+len(extra_edges)} "
          f"-> {'OK' if ok else 'DRIFT'}")
    return 0 if ok else 1


#: The five standing queries. Each is (sql, param_count_hint); a query takes
#: the terms it needs from argv and returns rows. Every one is index-backed.
QUERIES = {
    "nodes_by_type_verdict_town": (
        "SELECT id,type,verdict,town,title FROM nodes WHERE "
        "(:type IS NULL OR type=:type) AND (:verdict IS NULL OR verdict=:verdict) "
        "AND (:town IS NULL OR town=:town) ORDER BY id"),
    "children_of": (
        "SELECT n.id,n.type,n.title FROM edges e JOIN nodes n ON n.id=e.src "
        "WHERE e.kind='parents' AND e.dst=:term ORDER BY n.id"),
    "evidence_runs_of": (
        "SELECT src,dst FROM edges WHERE kind='evidence_runs' "
        "AND (src=:term OR dst=:term) ORDER BY src,dst"),
    "notes_with_dates": (
        "SELECT id,title,note_dates FROM nodes "
        "WHERE agent_notes LIKE '%'||:term||'%' AND note_dates IS NOT NULL AND note_dates<>'' "
        "ORDER BY id"),
    "retired_dangling_supersedes": (
        "SELECT id,supersedes FROM nodes WHERE retired=1 AND supersedes IS NOT NULL "
        "AND supersedes<>'' AND supersedes NOT IN (SELECT id FROM nodes) ORDER BY id"),
}


#: FTS5 variant, used only when build() created the virtual table (fast path).
NOTES_FTS = (
    "SELECT id,title,note_dates FROM nodes WHERE id IN "
    "(SELECT id FROM notes_fts WHERE notes MATCH :fts) "
    "AND note_dates IS NOT NULL AND note_dates<>'' ORDER BY id")


def _has_fts(con: sqlite3.Connection) -> bool:
    return con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='notes_fts'").fetchone() is not None


def run_query(con: sqlite3.Connection, name: str, args: list):
    if name not in QUERIES:
        raise SystemExit(f"graph2sql: unknown query {name!r}; have {sorted(QUERIES)}")
    term = args[0] if args else None
    if name == "notes_with_dates" and _has_fts(con):
        fts = '"' + str(term).replace('"', '""') + '"'
        return list(con.execute(NOTES_FTS, {"term": term, "fts": fts}))
    sql = QUERIES[name]
    params = {"term": term, "type": None, "verdict": None, "town": None}
    if name == "nodes_by_type_verdict_town":
        for key, val in zip(("type", "verdict", "town"), args):
            params[key] = val
    return list(con.execute(sql, params))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", default="build", choices=("build", "query", "ddl"))
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--verify", action="store_true", help="round-trip the built file against the nodes")
    ap.add_argument("--nodes", default=None, help="nodes dir (default <root>/.agi/nodes)")
    ap.add_argument("--db", default=None, help="sqlite path (default nodes.sqlite beside schema.sql)")
    args = ap.parse_args(argv)
    root = find_root()
    nodes_dir = Path(args.nodes) if args.nodes else root / ".agi" / "nodes"
    db_path = Path(args.db) if args.db else HERE / "nodes.sqlite"
    if args.action == "ddl":
        sys.stdout.write(SCHEMA.read_text(encoding="utf-8"))
        return 0
    if args.verify:
        return verify(root, nodes_dir, db_path)
    if args.action == "build":
        build(root, nodes_dir, db_path)
        return 0
    con = sqlite3.connect(db_path)
    try:
        rows = run_query(con, args.terms[0], args.terms[1:]) if args.terms else []
    finally:
        con.close()
    for row in rows:
        print("\t".join("" if v is None else str(v) for v in row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
