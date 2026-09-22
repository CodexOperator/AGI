#!/usr/bin/env python3
"""profile_sync.py — graph -> profile projection (goal:g7.31.5.1).

A node with `profile_ref: <path>` is LINKED to a projection artifact holding
its body (frontmatter and THOUGHT stripped); the graph is the SoT. It is NOT
`link_ref`, which resolves the other way. Refs resolve against the repo root
(the directory enclosing `.agi/`); an outside-repo ref, or one under
`.agi/nodes/`, is refused by name and never written.
"""
from __future__ import annotations
import argparse, hashlib, os, re, sys
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

def validate_ref(root, ref):
    """Resolve `ref` and refuse it BY NAME without writing anything.

    write.py calls this BEFORE `node_writer.update_node` so a refused
    `profile_ref` cannot leave a partial write (the node body landing while
    the projection refuses). Returns the resolved artifact path.
    """
    if root is None:
        raise Refused("no project root — no enclosing .agi/config.json")
    return artifact_path(root, ref)


def _projected_bytes(nf):
    """A node-file's projection payload: body with THOUGHT stripped."""
    t = node_writer.extract_thought(nf.body)
    body = nf.body.replace(t, "") if t else nf.body
    return (body.strip("\n") + "\n").encode()

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
    return artifact_path(root, str(ref)), _projected_bytes(nf)


def _raw_profile_ref(text):
    """Best-effort `profile_ref` from raw bytes, for a file YAML cannot parse."""
    m = re.search(r"^profile_ref:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def check_all(root):
    """Sweep every node with `profile_ref` under `nodes/**` (the retired
    sibling included, goal:g2.10). Returns a dict per linked node with
    status ok|drift|missing|refused|unreadable; an unlinked node is not
    swept. An unparseable file never raises: if its raw bytes carry no
    `profile_ref:` hint it is not a profile-linked node and is skipped;
    if they do, it cannot be proven in sync and is named `unreadable`.
    """
    if root is None:
        raise Refused("no project root — no enclosing .agi/config.json")
    out = []
    for f in sorted((Path(root) / "nodes").rglob("*.md")):
        try:
            nf = fmr.load_node_file(f)
        except Exception as e:
            raw = f.read_text(encoding="utf-8", errors="replace")
            if "profile_ref:" not in raw:
                continue  # unparseable but not profile-linked: not ours
            out.append({"node_id": f.stem, "artifact": _raw_profile_ref(raw),
                        "actual": None, "expected": None, "path": str(f),
                        "status": "unreadable",
                        "detail": f"{type(e).__name__}: {e}"})
            continue
        ref = nf.frontmatter.get("profile_ref")
        if not ref:
            continue
        r = {"node_id": str(nf.frontmatter.get("id") or f.stem),
             "artifact": str(ref), "actual": None,
             "expected": hashlib.sha256(_projected_bytes(nf)).hexdigest()}
        try:
            dest = artifact_path(root, str(ref))
        except Refused as e:
            r.update(status="refused", detail=str(e))
        else:
            if not dest.exists():
                r["status"] = "missing"
            else:
                r["actual"] = hashlib.sha256(dest.read_bytes()).hexdigest()
                r["status"] = "ok" if r["actual"] == r["expected"] else "drift"
        out.append(r)
    return out

def sync_node(root, node_id):
    """Write the artifact atomically. Returns (path, bytes, sha256)."""
    dest, payload = project(root, node_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp"); tmp.write_bytes(payload)
    os.replace(tmp, dest)
    return dest, len(payload), hashlib.sha256(payload).hexdigest()

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("node_id", nargs="?")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--all", dest="all_", action="store_true")
    a = ap.parse_args(argv); root = locations.find_project_root()
    if a.all_:
        try:
            rows = check_all(root)
        except Refused as e:
            print(f"REFUSED: {e}", file=sys.stderr); return 2
        bad = [r for r in rows if r["status"] != "ok"]
        for r in rows:
            where = r.get("path") or r["node_id"]
            print(f"{r['status'].upper()} {where} {r['artifact']} "
                  f"sha256={r['expected'] or 'unavailable'}")
        print(f"{len(rows)} linked, {len(bad)} not ok")
        return 1 if bad else 0
    if not a.node_id:
        ap.error("a node_id or --all is required")
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