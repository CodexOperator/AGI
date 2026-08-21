#!/usr/bin/env python3
"""snapshot-goals.py — convert GOALS.md into first-class nodes under nodes/goal/.

Reads `<PROJECT_ROOT>/GOALS.md` (human-authored prose) and writes one frontmatter
file per goal heading of the form:

    ## G1 — Playable dungeon crawler (sandbox ladder) — status: active

Output: `nodes/goal/<gid-lower>-<slug-of-title>.md`, node id `goal:g1`.

Linkage is parent-pointing: a node joins a goal by listing the goal node id in
its own `parents:` list (e.g. `parents: [goal:g2]`). render-context.py already
turns `parents` into `spawns` edges, so goals traverse and render for free.
This script only *reads* those parent pointers to compute each goal's `seeds:`
list — it never emits `next_edges` and never touches chain shape.

Pruning is H0-safe: only files stamped `origin: goals-doc` that were not written
this run are removed. A missing GOALS.md is a no-op (prunes nothing).

Run: `python3 bin/snapshot-goals.py [--strict] [--project PATH]`
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import yaml
from pathlib import Path

ORIGIN = "goals-doc"
KNOWN_STATUSES = {"active", "phasing-out", "complete"}
BODY_CAP = 4000

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(
    os.environ.get("AGI_TREE_PROJECT_ROOT")
    or os.environ.get("AUTORESEARCH_TREE_PROJECT_ROOT")  # legacy, rename window
    or os.environ.get("PROJECT_ROOT")
    or os.getcwd()
).resolve()

# Canonical name first; the legacy name stays accepted during the rename window.
CONFIG_NAMES = ("agi-tree.config.json", "autoresearch-tree.config.json")


def config_path(root: Path) -> Path | None:
    """First existing config file in `root`, or None if it is not a project."""
    for name in CONFIG_NAMES:
        p = root / name
        if p.exists():
            return p
    return None

GOALS_MD = PROJECT_ROOT / "GOALS.md"
NODES_DIR = PROJECT_ROOT / "nodes"

# `## G1 — Title — status: active`
GOAL_RE = re.compile(r"^##\s*(G\d+)\b(.*)$")
HEADING_RE = re.compile(r"^##\s")
STATUS_RE = re.compile(r"[—\-]?\s*status\s*:\s*(.+?)\s*$", re.IGNORECASE)
GOAL_ID_RE = re.compile(r"^goal:")


def _set_project_root(path: Path) -> None:
    """Re-point the module-level path globals (used by --project in tests)."""
    global PROJECT_ROOT, GOALS_MD, NODES_DIR
    PROJECT_ROOT = Path(path).resolve()
    GOALS_MD = PROJECT_ROOT / "GOALS.md"
    NODES_DIR = PROJECT_ROOT / "nodes"


# --- helpers copied from snapshot-build-site.py (kept in sync deliberately;
#     snapshot-build-site.py is load-bearing and is not refactored here) ------


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9\- ]", "", s.lower())
    s = re.sub(r"\s+", "-", s.strip())
    parts = s.split("-")[:6]
    return "-".join(p for p in parts if p) or "untitled"


def _upsert_node_to_db(node_id: str, fm: dict, body: str, origin: str) -> None:
    """Upsert a node into SQLite if persistence.type=sqlite."""
    if not hasattr(_upsert_node_to_db, "_backend"):
        cfg_path = config_path(PROJECT_ROOT)
        _upsert_node_to_db._backend = None
        if cfg_path is not None:
            cfg = json.loads(cfg_path.read_text())
            if cfg.get("persistence", {}).get("type") == "sqlite":
                db_path = PROJECT_ROOT / cfg["persistence"]["path"]
                from graph_core.persistence.sqlite_backend import SQLiteBackend
                _upsert_node_to_db._backend = SQLiteBackend(db_path)
    if _upsert_node_to_db._backend is None:
        return
    from graph_core.persistence.frontmatter import NodeFile
    fm = dict(fm)
    fm["id"] = node_id
    fm["origin"] = origin
    nf = NodeFile(frontmatter={**fm, "body": body}, body=body, suffix=".json")
    _upsert_node_to_db._backend.save(node_id, nf)


def write_frontmatter(path: Path, fm: dict, body: str, origin: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if origin:
        fm = dict(fm)  # copy so we don't mutate caller's dict
        fm["origin"] = origin
    lines = ["---"]
    for k in sorted(fm.keys()):
        v = fm[k]
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        else:
            sval = str(v).replace("\n", " ").strip()
            if any(c in sval for c in ":#'\""):
                sval = '"' + sval.replace('"', "'") + '"'
            lines.append(f"{k}: {sval}")
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def load_existing_nodes() -> dict:
    """Load all existing nodes. Returns dict keyed by node id.
    Each value: {path: Path, origin: str, fm: dict}
    """
    nodes = {}
    if not NODES_DIR.exists():
        return nodes
    for md_path in sorted(NODES_DIR.rglob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
            if text.strip().startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1]) or {}
                    node_id = fm.get("id", "")
                    if node_id:
                        nodes[node_id] = {
                            "path": md_path,
                            "origin": fm.get("origin", ""),
                            "fm": fm,
                        }
        except Exception:
            pass
    return nodes


# --- GOALS.md parsing ------------------------------------------------------


def _strip_separators(s: str) -> str:
    return s.strip().strip("—-").strip()


def parse_goals(text: str) -> list[dict]:
    """Parse GOALS.md text into an ordered list of goal dicts.

    Text before the first `## G` heading (the preamble) is ignored.
    """
    goals: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        m = GOAL_RE.match(line)
        if m:
            if current is not None:
                goals.append(current)
            gid = m.group(1)
            rest = m.group(2)
            status = "active"
            m_status = STATUS_RE.search(rest)
            if m_status:
                status = m_status.group(1).strip()
                rest = rest[: m_status.start()]
            title = _strip_separators(rest)
            current = {
                "gid": gid,
                "title": title or gid,
                "status": status or "active",
                "body": [],
            }
            continue
        if HEADING_RE.match(line):
            # A non-goal `## ` heading terminates the current goal body.
            if current is not None:
                goals.append(current)
                current = None
            continue
        if current is not None:
            current["body"].append(line)
    if current is not None:
        goals.append(current)
    for g in goals:
        g["body"] = "\n".join(g["body"]).strip()[:BODY_CAP]
    return goals


def collect_parent_refs(existing: dict) -> dict:
    """Map goal-id -> sorted list of node ids whose `parents` reference it."""
    refs: dict[str, list[str]] = {}
    for node_id, node in existing.items():
        parents = node["fm"].get("parents") or []
        if isinstance(parents, str):
            parents = [parents]
        for p in parents:
            p = str(p).strip()
            if GOAL_ID_RE.match(p):
                refs.setdefault(p, []).append(node_id)
    for k in refs:
        refs[k] = sorted(set(refs[k]))
    return refs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Derive nodes/goal/ from GOALS.md")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if a node references an unknown goal id")
    ap.add_argument("--project", default=None,
                    help="override PROJECT_ROOT (default: env or cwd)")
    args = ap.parse_args(argv)
    if args.project:
        _set_project_root(Path(args.project))

    if not GOALS_MD.exists():
        # Never prune on a missing/renamed GOALS.md — that would wipe goal nodes.
        print(f"no GOALS.md at {GOALS_MD} — skipping")
        return 0

    goals = parse_goals(GOALS_MD.read_text(encoding="utf-8"))
    existing = load_existing_nodes()
    refs = collect_parent_refs(existing)

    goal_ids = {f"goal:{g['gid'].lower()}" for g in goals}
    written: set[str] = set()
    written_paths: set[Path] = set()

    for g in goals:
        if g["status"] not in KNOWN_STATUSES:
            print(f"WARN: goal {g['gid']} has unrecognized status '{g['status']}'",
                  file=sys.stderr)
        node_id = f"goal:{g['gid'].lower()}"
        title = f"{g['gid']}: {g['title']}"
        fm = {
            "id": node_id,
            "type": "goal",
            "goal_id": g["gid"],
            "title": title,
            "status": g["status"],
            "seeds": refs.get(node_id, []),
            "tags": ["goal", "root"],
            "confidence": 1.0,
        }
        slug = f"{g['gid'].lower()}-{slugify(g['title'])}"
        out_path = NODES_DIR / "goal" / f"{slug}.md"
        write_frontmatter(out_path, fm, g["body"], origin=ORIGIN)
        _upsert_node_to_db(node_id, fm, g["body"], origin=ORIGIN)
        written.add(node_id)
        written_paths.add(out_path.resolve())

    # Referential integrity: `goal:` parents that no goal in GOALS.md resolves.
    unresolved = 0
    for goal_ref in sorted(refs):
        if goal_ref in goal_ids:
            continue
        for node_id in refs[goal_ref]:
            unresolved += 1
            path = existing[node_id]["path"]
            print(f"INTEGRITY: {path} references unknown goal '{goal_ref}'",
                  file=sys.stderr)

    # Prune only nodes stamped with our origin that we did not write this run
    # (covers both removed goals and goals whose title/slug changed).
    stale = [
        node["path"]
        for node_id, node in existing.items()
        if node["origin"] == ORIGIN and node["path"].resolve() not in written_paths
    ]
    for path in sorted(stale):
        path.unlink(missing_ok=True)
        print(f"removed stale: {path}")

    print(f"wrote: {len(goals)} goal nodes")
    print(f"target dir: {NODES_DIR / 'goal'}")
    if unresolved and args.strict:
        print(f"ERR: {unresolved} unresolved goal reference(s) (--strict)",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
