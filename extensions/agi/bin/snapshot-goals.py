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
# `horizon` = declared and committed to, but deliberately not being worked yet.
# It is what lets L5 goal rotation distinguish queued goals from active ones
# when `cc_dispatch.max_goals_active` is below the number of declared goals.
KNOWN_STATUSES = {"active", "horizon", "phasing-out", "complete"}
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

# `## G1 — Title — status: active`             long-term goal
# `### G1.2 — Title — status: active`          sub-goal, nested under G1
# `## S3 — Title — status: active`             standalone short-term goal
#
# Sub-goals and short-term goals exist so that work small enough to be a TODO
# item still lands in the graph instead of in a second document. A sub-goal
# parent-points at its long-term goal exactly the way a seed idea does; a
# short-term goal is its own root and needs no parent to be legitimate.
GOAL_RE = re.compile(r"^##\s*([GS]\d+)\b(.*)$")
SUBGOAL_RE = re.compile(r"^###\s*(G\d+\.\d+)\b(.*)$")
HEADING_RE = re.compile(r"^##\s")
STATUS_RE = re.compile(r"[—\-]?\s*status\s*:\s*(.+?)\s*$", re.IGNORECASE)
GOAL_ID_RE = re.compile(r"^goal:")


def _id_rest(node_id: str) -> str:
    """Everything after the first ``:`` in an id, or the whole id if there is none.

    Used to spot G7.1's common real cause: a typo'd type prefix (a node writes
    ``hypothesis:chain-engine-r1`` when the real id is ``hyp:chain-engine-r1``).
    Two ids with the same "rest" but different prefixes are almost certainly
    the same node referenced under the wrong prefix, not two unrelated ids.
    """
    return node_id.split(":", 1)[1] if ":" in node_id else node_id


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


def _add_graph_core_to_path() -> None:
    """Put graph_core on sys.path, plugin src last so a project can override.

    Mirrors driver.sh's convention and zoom.py's `_add_graph_core_to_path`.
    Without this the sqlite branch below raised ModuleNotFoundError *mid-run*,
    after some goal files had already been written — a project with
    `persistence.type: sqlite` could not snapshot its goals at all.
    """
    plugin_src = PLUGIN_ROOT / "src"
    if plugin_src.is_dir() and str(plugin_src) not in sys.path:
        sys.path.insert(0, str(plugin_src))
    proj_src = PROJECT_ROOT / "src"
    if (proj_src / "graph_core").is_dir() and str(proj_src) not in sys.path:
        sys.path.insert(0, str(proj_src))


def _upsert_node_to_db(node_id: str, fm: dict, body: str, origin: str) -> None:
    """Upsert a node into SQLite if persistence.type=sqlite."""
    if not hasattr(_upsert_node_to_db, "_backend"):
        cfg_path = config_path(PROJECT_ROOT)
        _upsert_node_to_db._backend = None
        if cfg_path is not None:
            cfg = json.loads(cfg_path.read_text())
            if cfg.get("persistence", {}).get("type") == "sqlite":
                db_path = PROJECT_ROOT / cfg["persistence"]["path"]
                _add_graph_core_to_path()
                # The DB is a mirror of the files just written, so an
                # unavailable backend must degrade to a warning. Raising here
                # aborts mid-corpus and leaves a partially-snapshotted graph —
                # a project shadowing graph_core with a stale copy that predates
                # sqlite_backend hit exactly that.
                try:
                    from graph_core.persistence.sqlite_backend import SQLiteBackend
                    _upsert_node_to_db._backend = SQLiteBackend(db_path)
                except Exception as exc:
                    print(f"WARN: sqlite persistence unavailable ({exc}); "
                          f"nodes written to files only", file=sys.stderr)
    if _upsert_node_to_db._backend is None:
        return
    from graph_core.persistence.frontmatter import NodeFile
    fm = dict(fm)
    fm["id"] = node_id
    fm["origin"] = origin
    nf = NodeFile(frontmatter={**fm, "body": body}, body=body, suffix=".json")
    _upsert_node_to_db._backend.save(node_id, nf)


def write_frontmatter(path: Path, fm: dict, body: str, origin: str = "",
                      preserve: dict | None = None) -> None:
    """Write a node file.  `preserve` carries forward fields we do not own.

    Kept in sync with snapshot-build-site.py, where rebuilding frontmatter from
    scratch silently severed `next_edges` on every re-snapshot.  Snapshot-owned
    keys win; anything a later writer added survives.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if preserve:
        merged = {k: v for k, v in preserve.items() if k not in fm}
        if merged:
            fm = {**merged, **fm}
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

    def _start(gid: str, rest: str) -> dict:
        status = "active"
        m_status = STATUS_RE.search(rest)
        if m_status:
            status = m_status.group(1).strip()
            rest = rest[: m_status.start()]
        title = _strip_separators(rest)
        return {
            "gid": gid,
            "title": title or gid,
            "status": status or "active",
            # A sub-goal carries its long-term goal as a parent; a top-level
            # goal (G or S) is a root and carries none.
            "parent_gid": gid.split(".")[0] if "." in gid else None,
            "body": [],
        }

    for line in text.splitlines():
        m = GOAL_RE.match(line)
        if m:
            if current is not None:
                goals.append(current)
            current = _start(m.group(1), m.group(2))
            continue
        m_sub = SUBGOAL_RE.match(line)
        if m_sub:
            if current is not None:
                goals.append(current)
            current = _start(m_sub.group(1), m_sub.group(2))
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
    """Map any referenced id -> sorted list of node ids whose `parents` reference it.

    G7.1: this used to filter down to `goal:`-prefixed refs only, because the
    only consumer was goal-seed population and the goal integrity check. Both
    still work off this same dict — seed lookups key on `goal:` ids, which are
    still in here — but now every prefix is collected so the integrity check
    below can validate ALL parent references, not just goals.
    """
    refs: dict[str, list[str]] = {}
    empty_parent_entries: dict[str, int] = {}
    for node_id, node in existing.items():
        parents = node["fm"].get("parents") or []
        if isinstance(parents, str):
            parents = [parents]
        for p in parents:
            # An empty YAML list item (`parents:\n  - `) parses to None. That is
            # malformed frontmatter, not a reference to a node called "None" —
            # reporting it as a dangling ref sent readers looking for a missing
            # node that never existed. Skipped here and counted separately below.
            if p is None or not str(p).strip():
                empty_parent_entries.setdefault(node_id, 0)
                empty_parent_entries[node_id] += 1
                continue
            refs.setdefault(str(p).strip(), []).append(node_id)
    for k in refs:
        refs[k] = sorted(set(refs[k]))
    for node_id, n in sorted(empty_parent_entries.items()):
        print(f"INTEGRITY: {node_id} has {n} empty entry/entries under `parents:` "
              f"(malformed frontmatter, not a missing node)", file=sys.stderr)
    return refs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Derive nodes/goal/ from GOALS.md")
    # The help text used to say "unknown goal id" while the check below tested
    # every unresolved parent reference — 81 of them on the live tree against 0
    # unresolved goals. A flag whose documentation is narrower than its
    # behaviour is worse than no flag: it reads as safe to enable and is not.
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if a node references ANY unknown parent id")
    ap.add_argument("--strict-goals", action="store_true",
                    help="exit 1 only if a node references an unknown goal id "
                         "(goal:g5 — the check driver.sh can actually enable)")
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
        parent_gid = g.get("parent_gid")
        if parent_gid:
            kind, tags = "subgoal", ["goal", "subgoal"]
        elif g["gid"].startswith("S"):
            kind, tags = "short-term", ["goal", "root", "short-term"]
        else:
            kind, tags = "long-term", ["goal", "root"]
        fm = {
            "id": node_id,
            "type": "goal",
            "goal_id": g["gid"],
            "title": title,
            "status": g["status"],
            "goal_kind": kind,
            "seeds": refs.get(node_id, []),
            "tags": tags,
            "confidence": 1.0,
        }
        if parent_gid:
            # Same parent-pointing convention seed ideas use, so a sub-goal
            # renders and traverses under its long-term goal for free.
            fm["parents"] = [f"goal:{parent_gid.lower()}"]
        slug = f"{g['gid'].lower()}-{slugify(g['title'])}"
        out_path = NODES_DIR / "goal" / f"{slug}.md"
        write_frontmatter(out_path, fm, g["body"], origin=ORIGIN,
                          preserve=existing.get(node_id, {}).get("fm"))
        _upsert_node_to_db(node_id, fm, g["body"], origin=ORIGIN)
        written.add(node_id)
        written_paths.add(out_path.resolve())

    # Referential integrity (G7.1): every parent reference must resolve to a
    # known node id — not just `goal:`-prefixed ones. This used to check goal
    # refs only; the mechanism (warn by default, --strict to fail) is unchanged,
    # only its scope. `goal_ids` is the fresh set this run computed from
    # GOALS.md (a goal's file may not exist on disk yet this run); `existing`
    # is every id already on disk. Together they're the full universe a
    # `parents:` entry may legitimately point at.
    known_ids = set(existing.keys()) | goal_ids
    rest_index: dict[str, list[str]] = {}
    for kid in known_ids:
        rest_index.setdefault(_id_rest(kid), []).append(kid)

    unresolved = 0
    unresolved_goals = 0
    prefix_mismatches = 0
    genuinely_missing = 0
    for ref in sorted(refs):
        if ref in known_ids:
            continue
        for node_id in refs[ref]:
            unresolved += 1
            path = existing[node_id]["path"]
            if GOAL_ID_RE.match(ref):
                # Preserve the original message verbatim for `goal:` refs.
                unresolved_goals += 1
                print(f"INTEGRITY: {path} references unknown goal '{ref}'",
                      file=sys.stderr)
                continue
            candidates = sorted(c for c in rest_index.get(_id_rest(ref), []) if c != ref)
            if candidates:
                prefix_mismatches += 1
                print(f"INTEGRITY: {path} references unknown parent '{ref}' "
                      f"(possible prefix typo — did you mean '{candidates[0]}'?)",
                      file=sys.stderr)
            else:
                genuinely_missing += 1
                print(f"INTEGRITY: {path} references unknown parent '{ref}'",
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
    if unresolved:
        print(f"unresolved parent references: {unresolved} "
              f"({prefix_mismatches} prefix-mismatch, {genuinely_missing} missing)")
    if unresolved and args.strict:
        print(f"ERR: {unresolved} unresolved parent reference(s) (--strict)",
              file=sys.stderr)
        return 1
    # goal:g5 — "fail loudly when a seed node points at a goal id that does not
    # exist." Narrower than --strict on purpose: the loop carries 81 unresolved
    # *parent* references (mostly `hypothesis:`/`hyp:` prefix drift), so
    # enabling --strict in driver.sh would abort every run on day one and be
    # reverted within the hour. A dangling goal reference is the different,
    # rarer failure this goal cares about, and it currently stands at 0 — which
    # is exactly when to start enforcing it, before the first one appears.
    if unresolved_goals and args.strict_goals:
        print(f"ERR: {unresolved_goals} unresolved goal reference(s) "
              "(--strict-goals)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
