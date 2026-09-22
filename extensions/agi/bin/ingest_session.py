#!/usr/bin/env python3
"""ingest_session.py -- goal:g7.32.1: one Grok session transcript -> one node.

Idempotent: the slug derives from the session id, so re-ingest returns the SAME
node id (`write_node(..., on_exists=SKIP)`) with no new mint. A malformed,
empty or non-session input exits 2 with a NAMED reason on stderr -- never a
silent drop."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import node_writer  # noqa: E402


def read_session(path):
    """(session_id, facts) or a ValueError whose message names the refusal."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"unreadable-input: {exc}")
    records = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed-jsonl: line {lineno}: {exc.msg}")
    session = next((r for r in records if r.get("type") == "session"), None)
    if session is None:
        raise ValueError('no-session-record: no {"type":"session"} line')
    sid = str(session.get("id") or "").strip()
    if not sid:
        raise ValueError("no-session-id: the session record has no id")
    msgs = [r for r in records if r.get("type") == "message"]
    texts = [b.get("text", "") for m in msgs
             for b in (m.get("message") or {}).get("content") or []
             if b.get("type") == "text" and b.get("text")]
    return sid, {"messages": len(msgs), "cwd": str(session.get("cwd") or ""),
                 "first": " ".join(" ".join(texts).split())[:280]}


#: A canonical UUID, the shape every id in the repo-root `sessions/` corpus has.
#: Case is NOT significant for a UUID, so `sid.lower()` is applied first: an
#: upper-cased UUID is the SAME session, and must stay idempotent, not fork.
_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def slug_for(sid):
    """Injective over the accepted domain (goal:g7.32.1, no-silent-drop).

    Sanitizing alone is lossy: `Probe-aaaa-1111` and `probe_aaaa_1111` both
    collapse to `probe-aaaa-1111`, so the second session hit an existing path
    and was skipped with exit 0 -- a silent drop. Two disjoint cases close it:
    a canonical UUID keeps its BARE slug (the whole real corpus, so the node
    already minted at `grok-session-<uuid>` stays idempotent and is never
    duplicated); EVERY other id gets a short `sha256(raw_id)` suffix, so two
    raw ids that sanitize alike address different files.
    """
    canon = re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-")
    if _UUID.match(sid.lower()):
        return "grok-session-" + canon
    digest = hashlib.sha256(sid.encode("utf-8")).hexdigest()[:8]
    return f"grok-session-{canon}-{digest}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("session", help="path to a JSONL session transcript")
    ap.add_argument("--parent", default="goal:g7.32.1")
    ap.add_argument("--out-root", default=None, help="graph root (holds nodes/)")
    args = ap.parse_args(argv)
    try:
        sid, facts = read_session(args.session)
    except ValueError as exc:
        print(f"INGEST refuse {exc}", file=sys.stderr)
        return 2
    src = str(Path(args.session))
    body = ("Ingested Grok session artifact (goal:g7.32.1).\n\n"
            f"- source_session: {sid}\n- source_path: {src}\n"
            f"- cwd: {facts['cwd']}\n- messages: {facts['messages']}\n\n"
            f"## First text\n\n{facts['first'] or '(none)'}\n")
    root = Path(args.out_root) if args.out_root else locations.find_project_root()
    if root is None:
        print("INGEST refuse no-project-root: pass --out-root", file=sys.stderr)
        return 2
    res = node_writer.write_node(
        root, "doc", slug_for(sid), parents=[args.parent], announce=False,
        extra_fm={"title": f"Grok session {sid}", "source_session": sid,
                  "edited_by": "ingest_session.py", "thought_session": src,
                  "tags": ["grok-session", "ingest"]}, body=body)
    if res.rejected:
        print(f"INGEST refuse gate: {res.reason}", file=sys.stderr)
        return 2
    print(f"INGEST {'ok' if res.written else 'skip'} {res.node_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())