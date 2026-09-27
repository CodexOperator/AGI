#!/usr/bin/env python3
"""decompose-engine.py — census of the engine's changeable surfaces -> nodes/idea/.

Reads the **engine repo** (this repo — `agi`, not the graph repo) and writes one
`type: idea` node per "unit" into `<PROJECT_ROOT>/nodes/idea/`. A unit is a
top-level `src/` package or an executable entry point (`bin/*.py`, `driver.sh`,
the session-start hook, `find-root.sh`, the sqlite migration script, the
agi-bridge extension) — never a file, never a symbol. See
`idea:engine-self-decomposition` in the graph repo for why that grain was
chosen and what would falsify it.

Seed source is deliberately `git ls-files` plus grouping of those paths by
directory, **not GitNexus**: a fresh index of this repo has zero symbol
coverage of any `bin/*.py` file (GitNexus appears to exclude `bin/` dirs by
default), which is exactly the half of the engine that changes most.

Three failure modes this script is built to avoid (see engine-self-decomposition
§4 in the graph repo):

1. Field erasure — reuses `write_frontmatter(..., preserve=existing_fm)` from
   snapshot-goals.py verbatim (imported, not re-implemented) so foreign fields
   a human or another writer added to a generated node survive a re-run.
2. Prune reach — stamps `origin: engine-decomp` and prunes *only* nodes
   carrying that exact stamp. A missing/unreadable engine tree is a no-op:
   nothing is written and nothing is pruned.
3. The override door — this script has no project-local lookup. It is invoked
   directly; wiring it into `driver.sh` (if ever) must stay plugin-only.

The unit -> goal `parents:` mapping is **not derived** from the file tree or
guessed from names. It is read from a declared table in
`decompose-engine.goalmap.json` (next to this script, override with
`--goal-map`). A unit absent from that table is emitted with no `parents:`
field and reported as `NO_GOAL:` on stdout — a human or a verdict decides the
mapping, the generator never does.

Pre-existing hand-written `idea:domain-*` nodes that no longer name a live
surface are never touched, re-pointed, or pruned — this script only prints a
`STALE:` line per one it cannot match to a current unit, using a coarse
token-overlap heuristic. That heuristic is advisory only; read the printed
line, don't trust it blindly.

Run: `python3 bin/decompose-engine.py [--dry-run] [--project PATH]
        [--engine-root PATH] [--goal-map PATH]`
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ORIGIN = "engine-decomp"

BIN_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN_DIR.parent  # .../extensions/agi
# This script lives at <engine repo root>/extensions/agi/bin/decompose-engine.py.
# BIN_DIR is .../extensions/agi/bin, so three levels up from BIN_DIR
# (agi -> extensions -> repo root) is the engine repo we census.
# Overridable with --engine-root, chiefly for tests.
DEFAULT_ENGINE_ROOT = BIN_DIR.parents[2]
DEFAULT_GOAL_MAP_PATH = BIN_DIR / "decompose-engine.goalmap.json"

PROJECT_ROOT = Path(
    os.environ.get("AGI_TREE_PROJECT_ROOT")
    or os.environ.get("AUTORESEARCH_TREE_PROJECT_ROOT")  # legacy, rename window
    or os.environ.get("PROJECT_ROOT")
    or os.getcwd()
).resolve()


def _set_project_root(path: Path) -> None:
    global PROJECT_ROOT
    PROJECT_ROOT = Path(path).resolve()


# --- reuse snapshot-goals.py's write_frontmatter / load_existing_nodes -----
# Loaded by file path (not `import`) because the filename has a hyphen and
# is not a valid module name. This is the actual function, not a copy — see
# module docstring point 1 (field erasure).
_SNAPSHOT_GOALS_PATH = BIN_DIR / "snapshot-goals.py"
_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter


# --- unit discovery ----------------------------------------------------------

SRC_PREFIX = "extensions/agi/src/"
BIN_PREFIX = "extensions/agi/bin/"

# Non-code subsystem directories (goal:g6.8 census widening). level3.py's scan
# widened to the G6.8 payload boundary; this script's discovery did not move
# with it, so every file below was left parentless. Each directory here is ONE
# unit — unlike SRC_PREFIX, which groups by the next path segment — because
# each holds a handful of files that are one coherent body of material.
# Subdividing further would be one-unit-per-file for a directory this small.
DIR_SUBSYSTEM_PREFIXES = [
    # context/impl, kits, plans retired 2026-09-06 (Hermes/cavekit era);
    # their build nodes live under nodes/deprecated/build/.
    ("context/refs/", "context-refs"),
]

# tests/ gets the src/ treatment, not the DIR_SUBSYSTEM treatment: one unit per
# immediate subdirectory (a tests/<pkg>/ dir is that package's suite), plus one
# catch-all for what sits directly under tests/. The catch-all is deliberate:
# those flat test_*.py files each test a bin_script unit, and find_parent()
# exact-matches a bin_script rather than matching by directory, so they cannot
# nest under the script they test the way tests/graph_core/ nests under
# src/graph_core. Twelve near-empty units would be the "too fine" failure.
TESTS_PREFIX = "extensions/agi/tests/"

# Single-file entry points named explicitly rather than discovered by a generic
# "every file in this dir" walk, because most directories holding one also hold
# files that should not become units merely by co-location.
#
# agent-prompt.md was the original worked example of exactly that — a file that
# must never become a unit by co-location (engine-self-decomposition §1, pinned
# by a regression test). That call predates goal:g6.6/g6.8, which later named
# agent-prompt.md and SKILL.md as the two highest-leverage prose surfaces the
# census must cover. It is listed below as its own deliberate entry, which does
# not loosen the rule: every entry here is still an individually-decided tuple,
# never a directory listing.
#
# Each entry is (rel_path from engine root, slug, kind). Presence is still
# checked against git ls-files: a removed entry point silently drops out.
NAMED_ENTRY_POINTS = [
    ("extensions/agi/driver.sh", "driver-sh", "entry_point"),
    ("extensions/agi/hooks/cc-session-start.sh", "cc-session-start", "entry_point"),
    ("extensions/agi/lib/find-root.sh", "find-root", "entry_point"),
    ("extensions/agi/scripts/migrate_to_sqlite.py", "migrate-to-sqlite", "entry_point"),
    ("extensions/agi-bridge/index.ts", "agi-bridge-index", "entry_point"),
    ("extensions/agi-bridge/README.md", "agi-bridge-readme", "entry_point"),
    ("extensions/agi/lib/agent-prompt.md", "agent-prompt", "entry_point"),
    ("extensions/agi/bin/decompose-engine.goalmap.json", "decompose-engine-goalmap", "entry_point"),
    ("extensions/agi/conftest.py", "conftest", "entry_point"),
    ("skills/agi/SKILL.md", "skill-doc", "entry_point"),
    ("README.md", "readme", "entry_point"),
    ("TODO.md", "todo", "entry_point"),
    ("HANDOFF.md", "handoff", "entry_point"),
    (".gitignore", "gitignore", "entry_point"),
    ("package.json", "package-json", "entry_point"),
    # schema.sql, run-loop.sh, start.sh, autoresearch.* retired 2026-09-06 --
    # pre-agi entry points; nodes deprecated, files gone, grid keeps them.
]

KIND_LABEL = {
    "src_package": "source package",
    "bin_script": "bin entry-point script",
    "entry_point": "entry point",
}


def git_ls_files(engine_root: Path) -> list[str] | None:
    """Tracked files under `engine_root`, or None if unreadable (no-op signal)."""
    if not engine_root.is_dir():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(engine_root), "ls-files"],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return [line for line in result.stdout.splitlines() if line]


def discover_units(engine_root: Path) -> list[dict] | None:
    """Census of changeable surfaces, seeded from `git ls-files`.

    Returns None (never [] for this case) if the engine tree could not be
    read at all — callers must treat that as a hard no-op, not "zero units".
    """
    files = git_ls_files(engine_root)
    if files is None:
        return None
    files_set = set(files)

    # src/ packages: group tracked files by their top-level dir under src/.
    pkg_files: dict[str, list[str]] = {}
    for f in files:
        if not f.startswith(SRC_PREFIX):
            continue
        rest = f[len(SRC_PREFIX):]
        if "/" not in rest:
            continue  # a stray file directly in src/ (e.g. __init__.py), not a package
        pkg = rest.split("/", 1)[0]
        if pkg.startswith("__"):
            continue
        pkg_files.setdefault(pkg, []).append(f)

    units: list[dict] = []
    for pkg in sorted(pkg_files):
        rel_path = f"{SRC_PREFIX}{pkg}"
        doc_source = f"{rel_path}/__init__.py"
        units.append({
            "rel_path": rel_path,
            "slug": pkg.replace("_", "-"),
            "kind": "src_package",
            "doc_source": doc_source if doc_source in files_set else None,
        })

    # Directory-subsystem units (goal:g6.8 widening): everything under each
    # prefix is one unit. Discovery only mints it; level3.py's existing
    # longest-prefix-wins find_parent() is what lets a more specific prefix
    # (a tests/ subdirectory below) beat a broader one, so this script does
    # not need to know about that resolution.
    for prefix, slug in DIR_SUBSYSTEM_PREFIXES:
        if any(f.startswith(prefix) for f in files):
            units.append({
                "rel_path": prefix.rstrip("/"),
                "slug": slug,
                "kind": "src_package",
                "doc_source": None,
            })

    # tests/: one unit per immediate subdirectory, plus one catch-all for what
    # sits directly under tests/ itself.
    test_subdirs: set[str] = set()
    has_flat_test_file = False
    for f in files:
        if not f.startswith(TESTS_PREFIX):
            continue
        rest = f[len(TESTS_PREFIX):]
        if "/" in rest:
            test_subdirs.add(rest.split("/", 1)[0])
        else:
            has_flat_test_file = True
    for sub in sorted(test_subdirs):
        if sub == "fixtures":
            # Mirrors payload_boundary.is_test_fixture(): every file under
            # tests/fixtures/ is *out* of the G6.8 boundary, so level3.py
            # never emits a node for one. A unit here would have zero
            # possible children forever. Not minted, on purpose.
            continue
        units.append({
            "rel_path": f"{TESTS_PREFIX}{sub}",
            "slug": f"tests-{sub.replace('_', '-')}",
            "kind": "src_package",
            "doc_source": None,
        })
    if test_subdirs or has_flat_test_file:
        units.append({
            "rel_path": TESTS_PREFIX.rstrip("/"),
            "slug": "tests",
            "kind": "src_package",
            "doc_source": None,
        })

    # bin/*.py: direct children of bin/ only, not nested, not __pycache__.
    bin_files = sorted(
        f for f in files
        if f.startswith(BIN_PREFIX) and f.endswith(".py")
        and "/" not in f[len(BIN_PREFIX):]
    )
    for f in bin_files:
        stem = Path(f).stem
        units.append({
            "rel_path": f,
            "slug": stem.replace("_", "-"),
            "kind": "bin_script",
            "doc_source": f,
        })

    # Named single-file entry points.
    for rel_path, slug, kind in NAMED_ENTRY_POINTS:
        if rel_path in files_set:
            units.append({
                "rel_path": rel_path,
                "slug": slug,
                "kind": kind,
                "doc_source": rel_path,
            })

    return units


# --- docstring / header extraction -------------------------------------------


def _extract_py_docstring(text: str) -> str | None:
    import ast
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    doc = ast.get_docstring(tree)
    return doc.strip() if doc else None


def _extract_sh_header(text: str) -> str | None:
    out: list[str] = []
    started = False
    for line in text.splitlines():
        if not started:
            if line.startswith("#!"):
                continue
            if line.startswith("#"):
                started = True
                out.append(line[1:].strip())
                continue
            break  # code before any comment header: nothing to extract
        if line.startswith("#"):
            out.append(line[1:].strip())
        else:
            break
    joined = "\n".join(out).strip()
    return joined or None


def _extract_block_comment(text: str) -> str | None:
    m = re.search(r"/\*\*(.*?)\*/", text, re.DOTALL)
    if not m:
        return None
    lines = [re.sub(r"^\s*\*\s?", "", ln) for ln in m.group(1).splitlines()]
    joined = "\n".join(lines).strip()
    return joined or None


def extract_doc(engine_root: Path, doc_source: str | None) -> str | None:
    if not doc_source:
        return None
    p = engine_root / doc_source
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return None
    if doc_source.endswith(".py"):
        return _extract_py_docstring(text)
    if doc_source.endswith(".sh"):
        return _extract_sh_header(text)
    if doc_source.endswith((".ts", ".js")):
        return _extract_block_comment(text)
    return None


# --- goal map (declared, never guessed) --------------------------------------


def load_goal_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"WARN: unreadable goal-map {path} ({exc}); treating as empty",
              file=sys.stderr)
        return {}
    mapping = data.get("mappings", {})
    if not isinstance(mapping, dict):
        print(f"WARN: goal-map {path} 'mappings' is not an object; treating as empty",
              file=sys.stderr)
        return {}
    return {str(k): str(v) for k, v in mapping.items()}


# --- node construction ---------------------------------------------------


def build_node(unit: dict, doc: str | None, goal_id: str | None) -> tuple[str, dict, str]:
    """Returns (node_id, frontmatter, body) for one unit."""
    node_id = f"idea:engine-{unit['slug']}"
    kind_label = KIND_LABEL[unit["kind"]]
    title = f"Engine surface: {unit['rel_path']}"
    scale = "big" if unit["kind"] == "src_package" else "small"

    fm = {
        "id": node_id,
        "type": "idea",
        "title": title,
        "unit_path": unit["rel_path"],
        "unit_kind": unit["kind"],
        "status": "open",
        "scale": scale,
        "tags": ["engine", "census", "l19"],
        "confidence": 1.0,
    }
    if goal_id:
        fm["parents"] = [goal_id]

    body_lines = [f"`{unit['rel_path']}` — an engine {kind_label}.", ""]
    if doc:
        body_lines.append(doc)
    else:
        body_lines.append(
            "No module docstring or header comment was found for this surface."
        )
    body_lines += [
        "",
        "Generated by `decompose-engine.py` (see `idea:engine-self-decomposition` "
        "in the graph repo for the census design). This node records that the "
        "surface exists; it is not itself a design argument.",
    ]
    return node_id, fm, "\n".join(body_lines)


# --- STALE detection (advisory only, never mutates) --------------------------


def _tokens(s: str) -> list[str]:
    s = re.sub(r"[-_]", " ", s.lower())
    return [t for t in s.split() if len(t) > 2]


def _overlaps(a_tokens: list[str], b_tokens: list[str]) -> bool:
    return any(a in b or b in a for a in a_tokens for b in b_tokens)


def report_stale_domain_nodes(existing: dict, units: list[dict]) -> int:
    """Print STALE: for `idea:domain-*` nodes with no matching current unit.

    Advisory only — matched by coarse token overlap against unit slugs and
    rel_paths, never by exact identity. Does not read or write anything.
    """
    unit_token_sets = [_tokens(u["slug"]) for u in units]
    count = 0
    for node_id in sorted(existing):
        if not node_id.startswith("idea:domain-"):
            continue
        node = existing[node_id]
        fm = node["fm"]
        candidate = fm.get("domain") or node_id.split(":", 1)[-1][len("domain-"):]
        cand_tokens = _tokens(str(candidate))
        if any(_overlaps(cand_tokens, ut) for ut in unit_token_sets):
            continue
        print(f"STALE: {node['path']} ({node_id}) — no matching engine surface "
              f"found for '{candidate}' (advisory, human/verdict decides)")
        count += 1
    return count


# --- main ----------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Census the engine's changeable surfaces into nodes/idea/")
    ap.add_argument("--project", default=None,
                    help="override PROJECT_ROOT (graph repo; default: env or cwd)")
    ap.add_argument("--engine-root", default=None,
                    help="override the engine repo root (default: this script's own repo)")
    ap.add_argument("--goal-map", default=None,
                    help="override the declared unit->goal mapping file")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would happen; write nothing")
    args = ap.parse_args(argv)

    if args.project:
        _set_project_root(Path(args.project))
    project_root = PROJECT_ROOT
    engine_root = Path(args.engine_root).resolve() if args.engine_root else DEFAULT_ENGINE_ROOT
    goal_map_path = Path(args.goal_map).resolve() if args.goal_map else DEFAULT_GOAL_MAP_PATH

    units = discover_units(engine_root)
    if units is None:
        # engine-self-decomposition failure mode #2: an unreadable/missing
        # engine tree is a no-op. Nothing is written, nothing is pruned.
        print(f"WARN: engine root {engine_root} is missing or unreadable "
              f"(not a git repo?) — no-op, nothing written or pruned",
              file=sys.stderr)
        return 0

    if not units:
        # H0/H0i guard, matching the one in level3.py. A readable engine repo
        # always yields units, so an empty list means discovery resolved
        # against the wrong tree rather than a genuine empty scope. Fail loud
        # and return before the origin-scoped prune can run; a silent exit-0
        # here would unlink every `idea:engine-*` node in the project.
        print(f"ERROR: discover_units returned zero units for engine root "
              f"{engine_root} — refusing to treat this as authoritative "
              f"scope; no-op, nothing written or pruned", file=sys.stderr)
        return 1

    goal_map = load_goal_map(goal_map_path)

    snapshot_goals._set_project_root(project_root)
    existing = snapshot_goals.load_existing_nodes()

    idea_dir = project_root / "nodes" / "idea"

    written_paths: set[Path] = set()
    used_ids: dict[str, str] = {}
    n_with_goal = 0
    n_no_goal = 0
    n_by_kind: dict[str, int] = {}

    for unit in units:
        n_by_kind[unit["kind"]] = n_by_kind.get(unit["kind"], 0) + 1
        doc = extract_doc(engine_root, unit["doc_source"])
        goal_id = goal_map.get(unit["rel_path"])
        node_id, fm, body = build_node(unit, doc, goal_id)

        if node_id in used_ids:
            disambiguated = f"{node_id}-{unit['kind']}"
            print(f"WARN: slug collision for {unit['rel_path']} vs "
                  f"{used_ids[node_id]}; disambiguated id to {disambiguated}",
                  file=sys.stderr)
            node_id = disambiguated
            fm["id"] = node_id
        used_ids[node_id] = unit["rel_path"]

        if goal_id:
            n_with_goal += 1
        else:
            n_no_goal += 1
            print(f"NO_GOAL: {unit['rel_path']} — no declared goal mapping "
                  f"(emitted parentless)")

        slug_part = node_id.split(":", 1)[-1]
        out_path = idea_dir / f"{slug_part}.md"
        written_paths.add(out_path.resolve())

        if args.dry_run:
            verb = "would create" if slug_part not in {
                p.stem for p in idea_dir.glob("*.md")
            } else "would update"
            print(f"DRY-RUN: {verb} {out_path} ({node_id})")
            continue

        write_frontmatter(
            out_path, fm, body, origin=ORIGIN,
            preserve=existing.get(node_id, {}).get("fm"),
        )

    # Prune only nodes stamped with our own origin that we did not write
    # this run. Never touches unstamped or build-site-origin nodes.
    stale_generated = [
        node["path"]
        for node_id, node in existing.items()
        if node["origin"] == ORIGIN and node["path"].resolve() not in written_paths
    ]
    for path in sorted(stale_generated):
        if args.dry_run:
            print(f"DRY-RUN: would prune stale {path}")
        else:
            path.unlink(missing_ok=True)
            print(f"removed stale: {path}")

    n_stale_flags = report_stale_domain_nodes(existing, units)

    print(f"engine root: {engine_root}")
    print(f"units discovered: {len(units)}")
    for kind in sorted(n_by_kind):
        print(f"  {kind}: {n_by_kind[kind]}")
    verb = "would write" if args.dry_run else "wrote"
    print(f"nodes {verb}: {len(units)}")
    print(f"  with declared goal parent: {n_with_goal}")
    print(f"  flagged NO_GOAL (parentless): {n_no_goal}")
    prune_verb = "would prune" if args.dry_run else "pruned"
    print(f"stale engine-decomp nodes {prune_verb}: {len(stale_generated)}")
    print(f"STALE flags against pre-existing idea:domain-* nodes: {n_stale_flags}")
    print(f"target dir: {idea_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
