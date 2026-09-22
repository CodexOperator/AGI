#!/usr/bin/env python3
"""ingest_grok_session.py — one grok session artifact -> one graph node
(`goal:g7.32.1`). Fixture: JSONL, first line `{"session_id": ...}`, then turns
`{"role","content","ts"}`. Idempotent by `source_session` (mint_ids are
random, so a re-run finds the same node instead of forking one). Malformed or
empty input is refused BY NAME and no node is written.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
BIN = Path(__file__).resolve().parent
sys.path[:0] = [str(BIN), str(BIN.parent / "src")]
import locations  # noqa: E402
import node_writer  # noqa: E402 -- the ONE node-writing routine
from graph_core.persistence import frontmatter as fm_reader  # noqa: E402
INGEST_SOURCE, SESSION_KEY = "grok-session", "source_session"
# A refusal writes nothing and names its reason on stdout: ValueError carries it.
Refused = ValueError
def parse_session(path):
    try:
        rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    except json.JSONDecodeError as exc:
        raise Refused(f"unparseable JSON: {exc}") from exc
    head = next((r for r in rows if r.get("session_id")), None)
    sid = str((head or {}).get("session_id") or "").strip()
    turns = [r for r in rows if r is not head]
    for bad, why in ((not rows, "empty session artifact"), (not sid, "no session_id"),
                     (not turns, "session has no turns")):
        if bad:
            raise Refused(why)
    return sid, turns
def find_existing(root, sid):
    """A random mint_id cannot be recomputed, so the session key is the key."""
    for nf in sorted((root / "nodes").rglob("*.md")):
        try:
            fm = fm_reader.load_node_file(nf, body=False).frontmatter
        except Exception:  # noqa: BLE001 -- an unreadable node is not this session
            continue
        if isinstance(fm, dict) and fm.get(SESSION_KEY) == sid and fm.get("ingest_source") == INGEST_SOURCE:
            return str(fm.get("id") or nf.stem)
    return None
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact")
    ap.add_argument("--root", help="graph root or repo root (default: nearest .agi)")
    ap.add_argument("--parent", default="goal:g7.32.1")
    ap.add_argument("--type", default="hypothesis")
    ap.add_argument("--actor", default="")
    ap.add_argument("--thought-session", default="")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else locations.find_project_root()
    if root is None:
        print("refused: no agi project graph root")
        return 2
    if (root / ".agi").is_dir():
        root = root / ".agi"
    try:
        sid, turns = parse_session(a.artifact)
    except Refused as exc:
        print(f"refused: {exc}")
        return 2
    if (hit := find_existing(root, sid)):
        print(hit)
        return 0
    slug = "grok-" + (re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-") or "session")
    claim = f"Grok session {sid} lands as graph residue."
    fm = {SESSION_KEY: sid, "ingest_source": INGEST_SOURCE, "testable_claim": claim, "title": f"Grok session {sid}"}
    # announce=False: the SPAWN-GATE line goes to STDOUT; stdout carries the id.
    res = node_writer.write_node(root, a.type, slug, [a.parent], extra_fm=fm, announce=False,
                                 body=f"Ingested Grok session `{sid}` ({len(turns)} turns).\n\nTestable claim: {claim}\n")
    if res.rejected or not res.written:
        print(f"refused: {res.reason}")
        return 2
    prov = {k: v for k, v in (("edited_by", a.actor), ("thought_session", a.thought_session)) if v}
    if prov:
        node_writer.update_node(root, res.node_id, set_fm=prov)
    print(res.node_id)
    return 0
if __name__ == "__main__":
    sys.exit(main())
