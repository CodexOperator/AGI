#!/usr/bin/env python3
"""session_ingest.py — a session artifact lands as a graph node, or is refused.

`goal:g7.32.1`. A finished harness session is currently only a file under
`sessions/`: unaddressable and lost the moment that directory is rotated. This
is the one narrow door between the two — read a BOUNDED window of the
artifact, mint ONE node naming it, print the node id. A refusal is a named
reason on stderr and exit 2, never a silent drop.

## Idempotency: the same-node shape, not supersession

The node id is DERIVED from content, `doc:session-<sha256(window)[:12]>`, so a
re-ingest asks for a node that already exists and `write_node` returns
`SKIPPED` — same id, same `mint_id`, no fork. A session that GREW hashes
differently and gets a second node; that case wants an explicit supersession
edge and is named as unbuilt in the body rather than half-done.

The hash covers the window read, not the whole file: naming a node must not
cost a multi-hundred-MB read, and the node states how much it saw.

Provenance is stamped through `write.create` (`edited_by`, `thought_session`),
so an ingested node is not a node with a weaker record than a dispatched one.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import node_writer  # noqa: E402
import write as write_api  # noqa: E402

#: The window read off the tail of a session artifact. A session log is
#: append-only, so the tail is the part that changed and the part a summary
#: is about.
TAIL_BYTES = 256 * 1024

#: `doc` is the one ACTIVE schema whose spawn rule takes a single goal parent
#: and whose `link_ref` is optional (body-is-data). A session residue has no
#: source file of its own — the session log IS the file, and it is named in
#: the body instead. The inactive `agent_session` schema is deliberately NOT
#: used: it is not auto-discovered and its required fields were derived from a
#: design document rather than from any node.
NODE_TYPE = "doc"

EXIT_OK = 0
EXIT_REFUSED = 2


class Refusal(Exception):
    """A named reason this artifact is not becoming a node. Never silent."""

    def __init__(self, name: str, detail: str):
        super().__init__(f"{name}: {detail}")
        self.name = name


def read_window(path: Path, max_bytes: int) -> tuple[str, int, bool]:
    """The last `max_bytes` of `path`, as text. Never the whole tree."""
    size = path.stat().st_size
    with open(path, "rb") as fh:
        if size > max_bytes:
            fh.seek(size - max_bytes)
        raw = fh.read()
    return raw.decode("utf-8", errors="replace"), size, size > max_bytes


def events(text: str) -> list[dict]:
    """Every parseable JSON line. A malformed line is a foreign artifact, not
    a reason to drop the lines that ARE parseable."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def role_of(rec: dict) -> str:
    for key in ("role", "type", "event", "author", "tool"):
        val = rec.get(key)
        if isinstance(val, str) and val:
            return val
    return "unknown"


def first_text(rec: dict, limit: int = 200) -> str:
    """A one-line excerpt of the first thing a human said, when there is one."""
    for key in ("text", "content", "message", "prompt"):
        val = rec.get(key)
        if isinstance(val, str) and val.strip():
            flat = " ".join(val.split())
            return flat[:limit]
        if isinstance(val, dict):
            inner = val.get("text") or val.get("content")
            if isinstance(inner, str) and inner.strip():
                return " ".join(inner.split())[:limit]
    return ""


def summarise(path: Path, max_bytes: int) -> dict:
    """Everything the node body needs, or a named refusal."""
    if not path.exists():
        raise Refusal("missing-artifact", f"{path} does not exist")
    if not path.is_file():
        raise Refusal("not-an-artifact", f"{path} is not a regular file")
    try:
        text, size, truncated = read_window(path, max_bytes)
    except OSError as exc:
        raise Refusal("unreadable-artifact", f"{path}: {exc}") from exc

    recs = events(text)
    if not recs:
        raise Refusal(
            "no-parseable-events",
            f"{path} yielded no JSON object in its last {max_bytes} bytes — "
            "this is not a session log, or the window missed its content")
    digest = hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()
    roles: dict[str, int] = {}
    opener = ""
    for rec in recs:
        role = role_of(rec)
        roles[role] = roles.get(role, 0) + 1
        if not opener:
            opener = first_text(rec)
    return {
        "path": path, "sha": digest, "size": size, "truncated": truncated,
        "events": len(recs), "roles": roles, "opener": opener,
        "window": min(max_bytes, size),
    }


def slug_for(digest: str) -> str:
    """The content address. This IS the idempotency mechanism."""
    return f"session-{digest[:12]}"


def body_for(node_id: str, meta: dict) -> str:
    roles = ", ".join(f"{k}×{v}" for k, v in sorted(meta["roles"].items()))
    window = f"last {meta['window']} bytes"
    if meta["truncated"]:
        window += f" of {meta['size']} (truncated)"
    return (
        f"# {node_id}\n\n"
        f"## Session residue\n\n"
        f"Minted by `session_ingest.py` from a harness session artifact — the "
        f"transcript was a file under `sessions/`, and this node is the "
        f"addressable residue of it (`goal:g7.32.1`).\n\n"
        f"- artifact: `{meta['path']}`\n"
        f"- content sha256: `{meta['sha']}`\n"
        f"- read window: {window}\n"
        f"- events: {meta['events']}\n"
        f"- roles: {roles}\n\n"
        + (f"Opener: {meta['opener']}\n\n" if meta["opener"] else "")
        + "Re-ingesting the same window resolves to THIS node id, so a repeat "
        "run mints nothing. A session that grew between runs hashes "
        "differently and needs an explicit supersession edge — not "
        "implemented, and said here rather than half-done.\n"
    )


def ingest(artifact: str, parent: str, max_bytes: int, *,
           root: Path | None = None, actor: str = "session_ingest",
           session: str = "session_ingest") -> dict:
    """Mint (or re-find) the node for one artifact. Raises `Refusal`."""
    meta = summarise(Path(artifact), max_bytes)
    start = Path(root) if root is not None else Path(artifact).resolve().parent
    # Both paths need the GRAPH root, not the project dir: `write.create`
    # resolves descend-only, and `node_writer.update_node` looks under
    # `<root>/nodes/`. Normalising once here is what keeps the two calls
    # pointing at the same tree.
    root = locations.find_project_root(start)
    if root is None:
        raise Refusal("no-project-root",
                      f"no enclosing .agi/ with a config.json for {artifact}; "
                      "pass --root to name the graph this session belongs to")

    slug = slug_for(meta["sha"])
    node_id = f"{NODE_TYPE}:{slug}"
    # The spawn gate announces to stdout. This script's stdout IS its result
    # (one node id, or nothing on refusal), so the gate's chatter is moved to
    # stderr where a human reads it and `$(...)` never swallows it.
    with contextlib.redirect_stdout(sys.stderr):
        res, _ = write_api.create(
            root, NODE_TYPE, slug, [parent],
            set_fm={
                "title": f"Session residue {slug}",
                "tags": ["session", "ingest", "grok-bot"],
                "thought_session": session,
                "ingest_source": meta["path"].name,
                "ingest_sha256": meta["sha"],
            },
            actor=actor, session=session,
        )
        if res.rejected:
            raise Refusal("spawn-gate-refused", f"{node_id}: {res.reason}")
        # Only a FRESH mint writes a body: a SKIPPED node is already the
        # record, and rewriting it would make a re-ingest mutate what it
        # claims to verify.
        if res.written:
            upd = node_writer.update_node(root, node_id,
                                          body=body_for(node_id, meta))
            if upd.rejected:
                raise Refusal("body-write-refused", f"{node_id}: {upd.reason}")
    return {"node_id": node_id, "status": res.status, "sha256": meta["sha"],
            "events": meta["events"], "path": str(root), "type": NODE_TYPE}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="session_ingest.py",
        description="Turn one session artifact into one graph node.")
    ap.add_argument("artifact", help=".jsonl session transcript, or a session dir")
    ap.add_argument("--parent", default="goal:g7.32.1",
                    help="the goal this residue hangs from (default: %(default)s)")
    ap.add_argument("--max-bytes", type=int, default=TAIL_BYTES,
                    help="tail window to read (default: %(default)s)")
    ap.add_argument("--root", default=None, help="graph root override")
    ap.add_argument("--json", action="store_true", help="print the result as json")
    args = ap.parse_args(argv)

    artifact = Path(args.artifact)
    if artifact.is_dir():
        logs = sorted(artifact.glob("*.jsonl"))
        if not logs:
            print(f"no-jsonl-in-dir: {artifact} holds no .jsonl session log",
                  file=sys.stderr)
            return EXIT_REFUSED
        artifact = logs[-1]  # a dir names its latest checkpoint
    try:
        out = ingest(str(artifact), args.parent, args.max_bytes,
                     root=Path(args.root).resolve() if args.root else None,
                     actor=os.environ.get("AGENT_ID", "session_ingest"))
    except Refusal as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_REFUSED
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(out["node_id"])
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
