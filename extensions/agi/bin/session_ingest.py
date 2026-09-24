#!/usr/bin/env python3
"""Ingest one Grok session artifact into the graph (goal:g7.32.1)."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations, node_writer

def session_key(path: Path) -> str:
    """Return a stable identity, preferring the artifact's own session id."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("session_id", "sessionId", "id"):
                if data.get(key):
                    return str(data[key])
    except (OSError, ValueError):
        pass
    return path.stem

def slug_for(key: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_.-]+", "-", key).strip("-")
    return "grok-session-" + (value or "session")

def ingest(root: Path, artifact: Path, parent: str = "goal:g7.32.1", actor: str = ""):
    key = session_key(artifact)
    slug = slug_for(key)
    text = artifact.read_text(encoding="utf-8")
    try:
        text = json.dumps(json.loads(text), indent=2, sort_keys=True)
    except ValueError:
        pass
    fm = {"source_session": key, "ingest_path": str(artifact),
          "source_kind": "grok-session", "edited_by": actor or "grok-session-ingest",
          "thought_session": key}
    body = (f"# Grok session `{key}`\n\n"
            "Ingested from a completed or checkpointed Grok session artifact.\n\n"
            "## Artifact\n\n```json\n" + text + "\n```\n")
    return node_writer.write_node(root, "experiment", slug, [parent], extra_fm=fm,
                                  body=body, heading=False)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("--parent", default="goal:g7.32.1")
    p.add_argument("--actor", default="")
    p.add_argument("--root", type=Path, default=None)
    a = p.parse_args(argv)
    root = a.root or locations.find_project_root()
    if root is None:
        p.error("no agi project root")
    try:
        r = ingest(root, a.artifact, a.parent, a.actor)
    except OSError as e:
        print(f"REFUSED {a.artifact}: {e}", file=sys.stderr)
        return 2
    print(f"{r.status} {r.node_id} {r.path or '-'} reason={r.reason or '-'}")
    return 0 if r.status in (node_writer.WRITTEN, node_writer.SKIPPED) else 1

if __name__ == "__main__":
    raise SystemExit(main())
