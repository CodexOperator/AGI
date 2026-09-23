#!/usr/bin/env python3
"""ingest_session.py — session artifact -> graph node (goal:g7.32.1).
Idempotent on `ingest_key = sha256(f"{harness}:{session_id}")[:16]` in the
minted node's frontmatter; `nodes/**/*.md` IS the registry. Malformed artifacts
are refused by name on stderr with exit 2, never a traceback.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations, node_writer, yaml
from frontmatter import split_frontmatter
PARENT, REQUIRED = "goal:g7.32.1", ("harness", "session_id")


def key_of(a):
    return hashlib.sha256(f"{a['harness']}:{a['session_id']}".encode()).hexdigest()[:16]


def find_existing(root, key):
    for p in sorted((root / "nodes").rglob("*.md")):
        sp = split_frontmatter(p.read_text(encoding="utf-8"))
        fm = (yaml.safe_load(sp[0]) if sp else None) or {}
        if fm.get("ingest_key") == key:
            return fm.get("id")


def ingest(root, a, edited_by, session):
    key = key_of(a)
    if (found := find_existing(root, key)):
        return found, "exists"
    res = node_writer.write_node(
        root, "hypothesis", f"grok-session-{key}", parents=[PARENT],
        announce=False,
        extra_fm={"ingest_key": key, "ingest_source": a.get("path", ""),
                  "ingest_harness": a["harness"], "edited_by": edited_by,
                  "thought_session": session},
        body=f"# ingested session\n\n{a.get('summary', '')}\n")
    return res.node_id, res.status


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts", nargs="+"); ap.add_argument("--root")
    ap.add_argument("--edited-by", default="ingest_session")
    ap.add_argument("--thought-session", default="")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else locations.find_project_root()
    if root is None or not ((root / "nodes").is_dir()
                            or locations.config_path(root)):
        print(f"REFUSED --root {root}: not a graph root "
              f"(no nodes/ dir and no config.json)", file=sys.stderr)
        return 2
    rc = 0
    for path in a.artifacts:
        try:
            art = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"REFUSED {path}: unreadable JSON: {type(exc).__name__}: {exc}", file=sys.stderr)
            rc = 2; continue
        if not isinstance(art, dict):
            print(f"REFUSED {path}: expected a JSON object, got {type(art).__name__}", file=sys.stderr)
            rc = 2; continue
        miss = [f for f in REQUIRED if not art.get(f)]
        if miss:
            print(f"REFUSED {path}: missing required field(s): {', '.join(miss)}", file=sys.stderr)
            rc = 2; continue
        nid, status = ingest(root, art, a.edited_by, a.thought_session)
        print(f"{nid} [{status}]")
    return rc


if __name__ == "__main__":
    sys.exit(main())