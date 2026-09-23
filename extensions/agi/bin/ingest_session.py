#!/usr/bin/env python3
"""ingest_session.py — grok session artifact -> graph node (goal:g7.32.1).
Slug = grok-session-<session_id>-<sha256(bytes)[:12]>: same bytes -> same id, write_node(on_exists=SKIP) -> SKIPPED never a re-mint; a goal parent takes hypothesis."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import locations  # noqa: E402
import node_writer  # noqa: E402
from graph_core.persistence import frontmatter as fm_reader  # noqa: E402
GOAL_CHILD_TYPE = "hypothesis"
#: parent type -> the type an ingest may mint under it.
CHILD_OF = {"goal": "hypothesis", "idea": "hypothesis", "hypothesis": "experiment"}
def _refuse(reason):  # by name on stderr; no silent drop
    print(f"refused: {reason}", file=sys.stderr)
    return 2
def load_artifact(path):
    """Read a grok artifact or raise ValueError naming the defect."""
    p = Path(path)
    if not p.is_file():
        raise ValueError(f"artifact not found: {p}")
    raw = p.read_bytes()
    if not raw.strip():
        raise ValueError(f"artifact is empty: {p}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"artifact is malformed JSON: {p}: {exc}")
    if not isinstance(data, dict) or not str(data.get("session_id", "")).strip():
        raise ValueError(f"artifact is not a JSON object with session_id: {p}")
    return data, raw
def _body(data, raw, artifact):
    prov = "\n".join(f"- {k}: `{v}`" for k, v in [
        ("harness", data.get("harness")), ("agent_id", data.get("agent_id")),
        ("iter", data.get("iter")), ("final_status", data.get("final_status")),
        ("transcript_ref", data.get("transcript_ref")), ("artifact", artifact),
        ("artifact_sha256", hashlib.sha256(raw).hexdigest())])
    return (f"\n# {data.get('session_id')}\n\n## Testable claim\n\n"
            f"A grok session (`{data.get('session_id')}`) can land as a graph node "
            "with provenance preserved.\n\n"
            f"## Session\n\n- window: {data.get('started_at')} -> {data.get('ended_at')}\n"
            f"{prov}\n- summary: {data.get('summary')}\n")
def main(argv=None):
    ap = argparse.ArgumentParser(prog="ingest_session.py")
    ap.add_argument("artifact")
    ap.add_argument("--parent", required=True)
    ap.add_argument("--root", default=None)
    ap.add_argument("--type", dest="node_type", default=None)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else locations.find_project_root()
    if root is None:
        return _refuse("no graph root found; pass --root")
    try:
        data, raw = load_artifact(args.artifact)
    except ValueError as exc:
        return _refuse(str(exc))
    nf = node_writer.find_node_file(root, args.parent)
    ptype = ""
    if nf is not None:
        try:
            ptype = str((fm_reader.load_node_file(nf, body=False).frontmatter or {}).get("type", ""))
        except Exception:
            ptype = ""
    ntype = args.node_type or CHILD_OF.get(ptype, GOAL_CHILD_TYPE)
    slug = f"grok-session-{data['session_id']}-{hashlib.sha256(raw).hexdigest()[:12]}"
    res = node_writer.write_node(
        root, ntype, slug, parents=[args.parent],
        extra_fm={"edited_by": str(data.get("agent_id", "")),
                  "thought_session": str(data.get("thought_session", "")),
                  "title": f"Grok session {data['session_id']}",
                  "testable_claim": str(data.get("summary", "")).strip() or data["session_id"]},
        body=_body(data, raw, args.artifact), announce=False)
    if res.rejected:
        return _refuse(f"{res.node_id}: {res.reason}")
    tail = "" if res.written else " (already exists; mint_id unchanged)"
    print(f"{'written' if res.written else 'skipped'} {res.node_id}{tail}")
    return 0
if __name__ == "__main__":
    sys.exit(main())
