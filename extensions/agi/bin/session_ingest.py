#!/usr/bin/env python3
"""Ingest a JSON/JSONL session transcript as one stable graph node."""
from __future__ import annotations
import ast, json, re, sys
from pathlib import Path

_YAML_BREAKERS = set(':#{}[],&*!|>%@`"\'\n\r\t')

def _session_slug(value: object) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("session_id must be a non-empty scalar")
    raw = str(value).strip()
    if not raw:
        raise ValueError("session_id must be a non-empty scalar")
    if raw in {".", ".."} or "/" in raw or "\\" in raw or any(c.isspace() for c in raw):
        raise ValueError("session_id contains a path separator or whitespace")
    if any(c in _YAML_BREAKERS for c in raw):
        raise ValueError("session_id contains YAML-breaking characters")
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", raw).strip("-_").lower()
    if not slug:
        raise ValueError("session_id normalizes to an empty slug")
    return slug

def _text(value: object, default: str) -> str:
    if value is None:
        return default
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)

def ingest(path: Path, root: Path) -> str:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError("empty session artifact")
    records = []
    try:
        parsed = json.loads(raw)
        records = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        records = [json.loads(line) for line in raw.splitlines()]
    records = [r for r in records if isinstance(r, dict)]
    if not records:
        raise ValueError("session artifact has no records")
    record = records[0]
    identity = record.get("session_id", record.get("id"))
    if identity is None:
        raise ValueError("session artifact has no session_id")
    sid = _session_slug(identity)
    nid = f"doc:session-{sid}"
    node_dir = (Path(root).resolve() / "nodes" / "doc")
    out = (node_dir / f"{sid}.md").resolve()
    if out.parent != node_dir.resolve():
        raise ValueError("session output escapes nodes/doc")
    previous = out.read_text(encoding="utf-8") if out.exists() else ""
    def old(name, default):
        m = re.search(rf"^{re.escape(name)}: (.*)$", previous, re.M)
        if not m:
            return default
        try:
            return json.loads(m.group(1).strip())
        except (TypeError, json.JSONDecodeError):
            try:
                return ast.literal_eval(m.group(1).strip())
            except (ValueError, SyntaxError):
                return m.group(1).strip()
    edited = _text(record.get("edited_by") or record.get("actor"), old("edited_by", "grok"))
    thought = _text(record.get("thought_session"), old("thought_session", sid))
    goal = record.get("goal") or record.get("goal_id")
    parents = [goal if isinstance(goal, str) and goal.startswith("goal:") else f"goal:{goal}"] if goal else old("parents", [])
    if not isinstance(parents, list):
        parents = []
    seat = record.get("seat", old("seat", None))
    extra = f"seat: {json.dumps(seat, ensure_ascii=False)}\n" if seat is not None else ""
    text = json.dumps(records, ensure_ascii=False, indent=2)
    out.parent.mkdir(parents=True, exist_ok=True)
    fm = {"id": nid, "mint_id": "session-" + sid, "type": "doc", "title": f"Session {sid}",
          "parents": parents, "tags": ["session"], "edited_by": edited,
          "thought_session": thought}
    yaml = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, str) else v}" for k, v in fm.items())
    out.write_text(f"---\n{yaml}\n{extra}---\n# {sid}\n\n```json\n{text}\n```\n", encoding="utf-8")
    return nid

if __name__ == "__main__":
    try:
        print(ingest(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERR: refusing session artifact: {exc}", file=sys.stderr)
        raise SystemExit(2)
