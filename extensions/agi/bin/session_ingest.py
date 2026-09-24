#!/usr/bin/env python3
"""Ingest a JSON/JSONL session transcript as one idempotent graph node."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

def ingest(path: Path, root: Path) -> str:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError("empty session artifact")
    records = []
    try:
        parsed = json.loads(raw)
        records = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        for line in raw.splitlines():
            records.append(json.loads(line))
    records = [r for r in records if isinstance(r, dict)]
    if not records or not any(r for r in records):
        raise ValueError("session artifact has no records")
    digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
    sid = str(records[0].get("session_id") or records[0].get("id") or digest)
    nid = f"doc:session-{sid}-{digest}"
    out = root / "nodes" / "doc" / f"session-{sid}-{digest}.md"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        edited = str(records[0].get("edited_by") or records[0].get("actor") or "grok")
        thought = str(records[0].get("thought_session") or sid)
        text = json.dumps(records, ensure_ascii=False, indent=2)
        out.write_text(f"---\nid: {nid}\ntype: doc\nedited_by: {edited}\nthought_session: {thought}\n---\n# {sid}\n\n```json\n{text}\n```\n", encoding="utf-8")
    return nid

if __name__ == "__main__":
    try:
        root = Path(sys.argv[2]).resolve()
        print(ingest(Path(sys.argv[1]).resolve(), root))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERR: refusing session artifact: {exc}", file=sys.stderr)
        raise SystemExit(2)
