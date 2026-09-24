#!/usr/bin/env python3
"""Ingest a JSON/JSONL session transcript as one stable graph node."""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

from node_writer import WRITTEN, find_node_file, update_node, write_node

_YAML_BREAKERS = set(':#{}[],&*!|>%@`"\'\n\r\t')

def _session_identity(value: object) -> tuple[str, str, str]:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("session_id must be a non-empty scalar")
    raw = str(value).strip()
    if not raw:
        raise ValueError("session_id must be a non-empty scalar")
    if raw in {".", ".."} or "/" in raw or "\\" in raw or any(c.isspace() for c in raw):
        raise ValueError("session_id contains a path separator or whitespace")
    if any(c in _YAML_BREAKERS for c in raw):
        raise ValueError("session_id contains YAML-breaking characters")
    canonical = json.dumps([type(value).__name__, raw], ensure_ascii=False,
                           separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    readable = re.sub(r"[^A-Za-z0-9_-]+", "-", raw).strip("-_").lower() or "session"
    return f"session-{readable}-{digest}", canonical, raw

def _text(value: object, default: str) -> str:
    if value is None:
        return default
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)

def _live_goal(root: Path, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("session artifact has no live goal parent")
    gid = value.strip() if value.startswith("goal:") else f"goal:{value}"
    path = find_node_file(root, gid)
    if path is None:
        raise ValueError(f"goal parent does not resolve: {gid}")
    from graph_core.persistence import frontmatter
    fm = frontmatter.load_node_file(path, body=False).frontmatter
    if fm.get("type") != "goal" or fm.get("status") in {"retired", "deprecated"}:
        raise ValueError(f"goal parent is not live: {gid}")
    return gid

def ingest(path: Path, root: Path, *, session_id: object = None,
            goal: object = None) -> str:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError("empty session artifact")
    records = []
    try:
        parsed = json.loads(raw)
        records = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        records = [json.loads(line) for line in raw.splitlines()]
    control_records = [r for r in records if isinstance(r, dict)]
    if not control_records:
        raise ValueError("session artifact has no object records")
    record = control_records[0]
    for name, supplied, keys in (("session_id", session_id, ("session_id", "id")),
                                 ("goal", goal, ("goal", "goal_id"))):
        present = next((record[key] for key in keys if record.get(key) is not None), None)
        if supplied is not None and present is not None and supplied != present:
            raise ValueError(f"conflicting CLI {name} and artifact {name}")
    identity = session_id if session_id is not None else record.get("session_id", record.get("id"))
    if identity is None:
        raise ValueError("session artifact has no session_id")
    root = Path(root).resolve()
    slug, canonical, display_id = _session_identity(identity)
    nid = f"doc:{slug}"
    previous = find_node_file(root, nid)
    prior_fm = {}
    if previous is not None:
        from graph_core.persistence import frontmatter
        prior_fm = frontmatter.load_node_file(previous, body=False).frontmatter
    goal_value = goal if goal is not None else (record.get("goal") or record.get("goal_id"))
    if goal_value is None and prior_fm:
        prior_parents = prior_fm.get("parents") or []
        goal_value = prior_parents[0] if len(prior_parents) == 1 else None
    goal = _live_goal(root, goal_value)
    edited = _text(record.get("edited_by") or record.get("actor"),
                   prior_fm.get("edited_by", "grok"))
    thought = _text(record.get("thought_session"),
                    prior_fm.get("thought_session", display_id))
    seat = record.get("seat", prior_fm.get("seat"))
    text = json.dumps(records, ensure_ascii=False, indent=2)
    body = f"\n# {display_id}\n\nCanonical session identity: `{canonical}`\n\n```json\n{text}\n```\n"
    set_fm = {"parents": [goal], "tags": ["session"], "edited_by": edited,
              "thought_session": thought, "session_id_canonical": canonical}
    if seat is not None:
        set_fm["seat"] = seat
    result = (update_node(root, nid, set_fm=set_fm, body=body)
              if previous is not None else
              write_node(root, "doc", slug, [goal], extra_fm={
                  "title": f"Session {display_id}", **set_fm},
                  body=body, announce=False))
    if result.status not in {WRITTEN, "updated", "unchanged"}:
        raise ValueError(f"node writer refused session artifact: {result.reason}")
    return nid

if __name__ == "__main__":
    try:
        print(ingest(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERR: refusing session artifact: {exc}", file=sys.stderr)
        raise SystemExit(2)
