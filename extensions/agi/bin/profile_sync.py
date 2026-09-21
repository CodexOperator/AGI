#!/usr/bin/env python3
"""profile_sync.py — graph -> profile projection (goal:g7.31.5.1).

A node with `profile_ref: <path>` is LINKED to a projection artifact holding
its body (frontmatter and THOUGHT stripped); the graph is the SoT. It is NOT
`link_ref`, which resolves the other way. Refs resolve against the repo root
(the directory enclosing `.agi/`); an outside-repo ref, or one under
`.agi/nodes/`, is refused by name and never written.
"""
from __future__ import annotations
import argparse, hashlib, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations, node_writer  # noqa: E402
from graph_core.persistence import frontmatter as fmr  # noqa: E402

class Refused(Exception): pass
class NoRef(Exception): pass

def artifact_path(root, ref):
    """Resolve `ref`; refuse outside-repo and .agi/nodes/ by name."""
    repo, nodes = Path(root).resolve().parent, Path(root).resolve() / "nodes"
    p = Path(ref); p = (p if p.is_absolute() else repo / p).resolve()
    if p.is_relative_to(nodes):
        raise Refused(f"profile_ref {ref!r} resolves under .agi/nodes/")
    if not p.is_relative_to(repo):
        raise Refused(f"profile_ref {ref!r} resolves outside the repo root")
    if p.is_dir():
        raise Refused(
            f"profile_ref {ref!r} resolves to a directory, not a file")
    return p

def project(root, node_id):
    """(artifact path, normalized body bytes) for a linked node."""
    if root is None:
        # locations.find_project_root() returns None outside any project.
        # Refuse BY NAME here rather than letting Path(None) raise a bare
        # TypeError from inside node_writer.find_node_file.
        raise Refused("no project root — no enclosing .agi/config.json")
    f = node_writer.find_node_file(root, node_id)
    if f is None:
        raise FileNotFoundError(node_id)
    nf = fmr.load_node_file(f); ref = nf.frontmatter.get("profile_ref")
    if not ref:
        raise NoRef(node_id)
    t = node_writer.extract_thought(nf.body)
    payload = (nf.body.replace(t, "") if t else nf.body).strip("\n") + "\n"
    return artifact_path(root, str(ref)), payload.encode()

def sync_node(root, node_id):
    """Write the artifact atomically. Returns (path, bytes, sha256)."""
    dest, payload = project(root, node_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp"); tmp.write_bytes(payload)
    os.replace(tmp, dest)
    return dest, len(payload), hashlib.sha256(payload).hexdigest()

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("node_id"); ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv); root = locations.find_project_root()
    try:
        dest, payload = project(root, a.node_id)
    except NoRef as e:
        print(f"{e}: no profile_ref"); return 0
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr); return 2
    sha = hashlib.sha256(payload).hexdigest()
    if a.check:
        have = dest.read_bytes() if dest.exists() else b""
        print(f"{'OK' if have == payload else 'DRIFT'} {dest} "
              f"bytes={len(payload)} sha256={sha}")
        return 0 if have == payload else 1
    dest, n, sha = sync_node(root, a.node_id)
    print(f"synced {dest} bytes={n} sha256={sha}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())