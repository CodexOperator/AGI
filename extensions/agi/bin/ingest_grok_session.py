#!/usr/bin/env python3
"""ingest_grok_session.py — a grok session artifact -> a graph node
(`goal:g7.32.1`). One artifact by path, or a whole directory with `--scan`.

JSONL: first line `{"session_id": ...}`, then `{role, content, ts}` turns.
Idempotent by `source_session` (mint_ids are random, so the session key is the
only key). Malformed or empty input, missing provenance, and a bad `--scan`
directory are refused BY NAME with no node written: every minted node carries
non-empty `edited_by` and `thought_session` from the flags or
`AGI_ACTOR`/`AGI_AGENT_ID` and `AGI_THOUGHT_SESSION`.

`--scan DIR` ingests every `*.jsonl` in DIR in stable sorted order, one node id
(or `refused:` line) per artifact; one refusal does not abort the batch, and
the exit code is non-zero iff ZERO artifacts ingested.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path[:0] = [str(BIN), str(BIN.parent / "src")]
import locations  # noqa: E402
import node_writer  # noqa: E402 -- the ONE node-writing routine
from graph_core.persistence import frontmatter as fm_reader  # noqa: E402

INGEST_SOURCE, SESSION_KEY = "grok-session", "source_session"
# A refusal writes nothing and names its reason on stdout: ValueError carries it.
Refused = ValueError


def resolve_provenance(actor, thought_session):
    """Required, not best-effort: flag, then env, then refuse BY NAME."""
    actor = (actor or os.environ.get("AGI_ACTOR") or os.environ.get("AGI_AGENT_ID") or "").strip()
    session = (thought_session or os.environ.get("AGI_THOUGHT_SESSION") or "").strip()
    if not actor or not session:
        raise Refused("no actor" if not actor else "no thought_session")
    return actor, session


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


def ingest_one(root, path, parent, ntype, actor, thought_session, label=""):
    """Mint or resolve ONE artifact: prints the node id, or a `refused:` line
    and returns None. Never raises, so a batch keeps going."""
    try:
        sid, turns = parse_session(path)
    except Refused as exc:
        print(f"refused: {label}{exc}")
        return None
    if (hit := find_existing(root, sid)):
        print(hit)
        return hit
    cleaned = re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-") or "session"
    slug = cleaned if cleaned.startswith("grok-") else "grok-" + cleaned
    claim = f"Grok session {sid} lands as graph residue."
    fm = {SESSION_KEY: sid, "ingest_source": INGEST_SOURCE, "testable_claim": claim,
          "title": f"Grok session {sid}", "edited_by": actor, "thought_session": thought_session}
    res = node_writer.write_node(root, ntype, slug, [parent], extra_fm=fm, announce=False,
                                 body=f"Ingested Grok session `{sid}` ({len(turns)} turns).\n\nTestable claim: {claim}\n")
    if res.rejected or not res.written:
        print(f"refused: {label}{res.reason}")
        return None
    print(res.node_id)
    return res.node_id


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact", nargs="?", help="one session artifact; omit with --scan")
    ap.add_argument("--scan", help="ingest every *.jsonl in this directory")
    ap.add_argument("--root", help="graph root or repo root (default: nearest .agi)")
    ap.add_argument("--parent", default="goal:g7.32.1")
    ap.add_argument("--type", default="hypothesis")
    ap.add_argument("--actor", default="")
    ap.add_argument("--thought-session", default="")
    a = ap.parse_args(argv)
    if bool(a.artifact) == bool(a.scan):
        print("refused: exactly one of ARTIFACT or --scan is required")
        return 2
    root = Path(a.root).resolve() if a.root else locations.find_project_root()
    if root is None:
        print("refused: no agi project graph root")
        return 2
    if (root / ".agi").is_dir():
        root = root / ".agi"
    try:
        actor, thought_session = resolve_provenance(a.actor, a.thought_session)
    except Refused as exc:
        print(f"refused: {exc}")
        return 2
    if not a.scan:
        return 0 if ingest_one(root, a.artifact, a.parent, a.type, actor, thought_session) else 2
    d = Path(a.scan)
    if not d.is_dir():
        print(f"refused: not a directory: {d}")
        return 2
    files = sorted(p for p in d.iterdir() if p.suffix == ".jsonl")
    got = sum(ingest_one(root, p, a.parent, a.type, actor, thought_session, label=f"{p.name}: ") is not None
              for p in files)
    return 0 if got else 2


if __name__ == "__main__":
    sys.exit(main())
