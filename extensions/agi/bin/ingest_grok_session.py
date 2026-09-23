#!/usr/bin/env python3
"""ingest_grok_session.py -- Grok session artifact -> agent_session node (goal:g7.32.1)."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import node_writer  # noqa: E402
DEFAULT_PARENT = "goal:g7.32.1"
TAGS = ["agent-session", "grok", "session-ingest"]

class Refusal(Exception):
    """A fixture that cannot be ingested, refused by name."""
def parse_session(path):
    """(header, turns), or a named Refusal for what a session must carry."""
    try:
        lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    except OSError as exc:
        raise Refusal(f"unreadable-fixture: {exc}") from exc
    if not lines:
        raise Refusal(f"empty-fixture: {path} has no JSONL records")
    try:
        header = json.loads(lines[0])
    except ValueError as exc:
        raise Refusal(f"bad-header-json: {exc}") from exc
    for key in ("session_id", "agent_id"):
        if not isinstance(header.get(key), str) or not header[key].strip():
            raise Refusal(f"missing-{key}: header carries no usable {key!r}")
    turns = []
    for i, line in enumerate(lines[1:], start=2):
        try:
            turns.append(json.loads(line))
        except ValueError as exc:
            raise Refusal(f"bad-turn-json line {i}: {exc}") from exc
    return header, turns
def ingest(root, fixture, parent=DEFAULT_PARENT):
    """Mint (or reuse) the agent_session node for `fixture` under `root`."""
    header, turns = parse_session(fixture)
    sid = header["session_id"]
    slug = re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-")
    if not slug:
        raise Refusal(f"empty-slug: session_id {sid!r} yields no slug")
    slug = f"grok-{slug[:60]}-{hashlib.sha1(sid.encode()).hexdigest()[:8]}"
    body = (f"\nIngested Grok session `{sid}` "
            f"(agent `{header['agent_id']}`), {len(turns)} turns.\n\n"
            f"Source artifact: `{fixture}`.\n")
    res = node_writer.write_node(
        root, "agent_session", slug, parents=[parent],
        extra_fm={"title": f"Grok session: {sid}", "tags": list(TAGS),
                  "agent_id": header["agent_id"], "session_id": sid,
                  "started_at": str(header.get("started_at", "")),
                  "thought_session": str(header.get("thought_session") or sid),
                  "edited_by": header["agent_id"],
                  "source_artifact": str(fixture), "turn_count": len(turns)},
        body=body)
    return {"status": res.status, "node_id": res.node_id, "reason": res.reason}

def iter_sessions(sessions_dir, last=None):
    """`*.jsonl` under `sessions_dir`, OLDEST-FIRST by (mtime, name); `--last N` keeps the N most recent by mtime, ties by name."""
    paths = sorted(Path(sessions_dir).glob("*.jsonl"),
                   key=lambda p: (p.stat().st_mtime, p.name))
    return paths[-last:] if last is not None and last > 0 else (
        [] if last is not None else paths)
def ingest_dir(root, sessions_dir, parent=DEFAULT_PARENT, last=None):
    """Ingest every member; return (node_ids, refusals). A refusal names its member and never aborts its siblings."""
    sessions_dir = Path(sessions_dir)
    if not sessions_dir.is_dir():
        return [], [(str(sessions_dir), f"not-a-directory: {sessions_dir}")]
    node_ids, refusals = [], []
    for path in iter_sessions(sessions_dir, last):
        try:
            res = ingest(root, path, parent)
        except Refusal as exc:
            refusals.append((path.name, str(exc)))
            continue
        if res["status"] == node_writer.REJECTED:
            refusals.append((path.name, f"gate-rejected: {res['reason']}"))
            continue
        node_ids.append(res["node_id"])
    return node_ids, refusals
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--fixture")
    mode.add_argument("--sessions-dir")
    ap.add_argument("--last", type=int, default=None,
                    help="batch: keep the N most recent *.jsonl by mtime")
    ap.add_argument("--root", default=None)
    ap.add_argument("--parent", default=DEFAULT_PARENT)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else locations.find_project_root()
    if root is None:
        print("refused: no-project-root: pass --root")
        return 2
    if args.sessions_dir:
        # Exit rule: 0 iff every member yielded a node id; 2 if any was
        # refused. Ids go to stdout (one per line); refusals to stderr by name.
        ids, refusals = ingest_dir(root, args.sessions_dir, args.parent, args.last)
        for name, reason in refusals:
            print(f"refused: {name}: {reason}", file=sys.stderr)
        for node_id in ids:
            print(node_id)
        return 2 if refusals else 0
    try:
        result = ingest(root, Path(args.fixture), args.parent)
    except Refusal as exc:
        print(f"refused: {exc}")
        return 2
    if result["status"] == node_writer.REJECTED:
        print(f"refused: gate-rejected: {result['reason']}")
        return 2
    print(result["node_id"])
    return 0
if __name__ == "__main__":
    sys.exit(main())
