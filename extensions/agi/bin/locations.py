#!/usr/bin/env python3
"""locations.py — the one place a path is resolved.

**goal:g11.** Every entry point under `bin/` used to carry its own copy of
"walk up from cwd looking for `agi-tree.config.json`" — twelve of them, byte
for byte, plus a thirteenth in `lib/find-root.sh` written in bash. That is the
sprawl G11 has to remove before the layout can change at all: a resolver
duplicated thirteen times cannot be given a new rule, only thirteen new rules
that drift.

This module is the Python half of that single rule. `lib/find-root.sh` is the
bash half and implements the *same* phase order deliberately; the two are
verified against each other in `tests/test_locations.py::test_bash_and_python_agree`.

## The three questions, and why they are three

| Question | Answer |
|---|---|
| Where is the graph? | `find_project_root()` — nodes, context, config |
| Where is the source the graph describes? | `source_root()` — where `payload_ref` resolves |
| Where does the rendered goal document go? | `goals_path()` |

They used to be one question with one answer because the graph repo and the
source repo were the same directory in the only layout that existed. They are
separated here because **G11's whole point is that the graph moves inside the
thing it builds**, at which point the graph root (`<repo>/.agi`) and the source
root (`<repo>`) are different directories and the goal document belongs at
neither's default.

## Layout discovery, in phase order

Phase 0 is new and wins outright; phases 1 and 2 are exactly today's rule, kept
so that every existing project keeps resolving with no config change.

    0. GRAPH DIR   <d>/.agi/ holding a config          -> <d>/.agi
    1. UP          <d>/agi-tree.config.json            -> <d>
    2. DOWN        <start>/*-tree/ holding a config    -> that dir

**Nearest enclosing wins, and that is the feature.** Under G11 an engine clone
carries its own graph, so a project checkout holds two:

    fantasia/.agi          <- run from fantasia/,    you get fantasia's graph
    fantasia/agi/.agi      <- run from fantasia/agi/, you get the engine's

Neither needs a flag and neither needs the engine to know which project it is
running (**goal:g8.2**) — the answer falls out of where you are standing. This
is also why phase 0 checks `.agi/` *before* the legacy marker in the same
directory: during the migration a repo carries both, and the new layout is the
one that should win.

## Nothing here is agi-tree-specific

No project name appears in this file and none may be added. Phase 2 derives its
candidate from the starting directory's own basename, phases 0 and 1 from
literal marker names that every project shares. **goal:g8.2**'s invariant is
that no `if project == "agi-tree"` branch exists anywhere; a resolver is the
most tempting place to put one, which is why the rule is restated here.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# --- markers ---------------------------------------------------------------

#: Canonical first; the legacy name stays accepted during the rename window.
#: `config_path()` returns the first that exists, so a project carrying both
#: resolves to the canonical one.
CONFIG_NAMES = ("agi-tree.config.json", "autoresearch-tree.config.json")

#: The graph directory G11 moves the tree into. A dot name on purpose: it puts
#: the graph with `.git`, `.github` and `.claude` — the tooling a repo carries
#: but does not itself run — rather than in the middle of the source tree.
GRAPH_DIR_NAME = ".agi"

#: Inside `.agi/` the config needs no project prefix; the directory already
#: says what it is. The prefixed names stay accepted so a tree that is moved
#: into `.agi/` without being renamed still resolves.
GRAPH_DIR_CONFIG_NAMES = ("config.json",) + CONFIG_NAMES

#: Overridable per project via `goals_file` (see `goals_path`).
DEFAULT_GOALS_FILE = "GOALS.md"

#: Canonical first; the legacy spelling is still read and still set.
PROJECT_ROOT_ENV_VARS = (
    "AGI_TREE_PROJECT_ROOT",
    "AUTORESEARCH_TREE_PROJECT_ROOT",
    "PROJECT_ROOT",
)


# --- layout ----------------------------------------------------------------


def is_graph_dir(root: Path) -> bool:
    """True if `root` is a `.agi/` graph directory rather than a bare tree.

    Checked by name rather than by content because it is a question about the
    *layout*, not about what happens to be inside: a `.agi/` that has lost its
    nodes is still a `.agi/` and should report the G11 layout, so the caller
    fails on the missing nodes rather than silently resolving paths as legacy.
    """
    return Path(root).name == GRAPH_DIR_NAME


def repo_root(root: Path) -> Path:
    """The enclosing repository root for graph root `root`.

    Under G11 that is the parent of `.agi/`. Under the legacy layout the graph
    root *is* the repo root, so this is the identity — which is what lets every
    caller ask for the repo root unconditionally instead of branching on layout.
    """
    root = Path(root).resolve()
    return root.parent if is_graph_dir(root) else root


def config_path(root: Path) -> Path | None:
    """First existing config file in `root`, or None if it is not a project.

    Accepts the bare `config.json` only inside a `.agi/` directory. Outside one
    that name is far too generic to be a project marker — a stray `config.json`
    in someone's repo root must never make it look like a graph.
    """
    root = Path(root)
    names = GRAPH_DIR_CONFIG_NAMES if is_graph_dir(root) else CONFIG_NAMES
    for name in names:
        p = root / name
        if p.exists():
            return p
    return None


def load_config(root: Path) -> dict:
    """Parse the project config, or `{}` if absent or unreadable.

    Never raises. A malformed config must not take down a resolver that half
    the engine imports at module scope; callers that need the config to be
    valid check for the keys they need and say so themselves.
    """
    p = config_path(root)
    if p is None:
        return {}
    try:
        with open(p, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


# --- discovery -------------------------------------------------------------


def _graph_dir_in(d: Path) -> Path | None:
    """`d/.agi` if it exists and holds a config, else None."""
    cand = d / GRAPH_DIR_NAME
    if cand.is_dir() and config_path(cand) is not None:
        return cand
    return None


def _descend(start: Path) -> Path | None:
    """Phase 2: find a tree at `<start>/*-tree/`.

    Preferred, unambiguous match first (`<start>/<basename>-tree`), then a glob.
    Exactly one match wins. **More than one is None, never a guess** — the bash
    half prints the candidates and fails; here the caller decides how loud to
    be, because this module is imported at module scope by scripts that must
    not die on import.
    """
    preferred = start / f"{start.name}-tree"
    if preferred.is_dir() and config_path(preferred) is not None:
        return preferred

    candidates = [
        d for d in sorted(start.glob("*-tree"))
        if d.is_dir() and config_path(d) is not None
    ]
    return candidates[0] if len(candidates) == 1 else None


def find_project_root(start: Path | str | None = None) -> Path | None:
    """Resolve the graph root from `start` (default: cwd), or None.

    Phases 0 and 1 are interleaved in a single upward walk rather than run as
    two separate walks. That matters: two walks would let a distant `.agi/`
    outrank a legacy config sitting right next to you, which inverts "nearest
    enclosing wins" exactly when a repo is half migrated.
    """
    d = Path(start).resolve() if start is not None else Path.cwd().resolve()

    cur = d
    while True:
        # Phase 0 before phase 1 within each directory: during migration a repo
        # holds both markers and the new layout is the one that should win.
        found = _graph_dir_in(cur)
        if found is not None:
            return found
        if config_path(cur) is not None:
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent

    return _descend(d)


def project_root_from_env(start: Path | str | None = None) -> Path | None:
    """`find_project_root`, but an explicit environment override wins.

    Kept separate so that a caller which already has a root (a `--project`
    flag, say) is never silently overridden by an env var set for a different
    project in the same shell.
    """
    for var in PROJECT_ROOT_ENV_VARS:
        val = os.environ.get(var)
        if val:
            return Path(val).resolve()
    return find_project_root(start)


# --- the two derived roots -------------------------------------------------


def source_root(root: Path, config: dict | None = None) -> Path:
    """Where the source the graph describes lives — `payload_ref`'s base.

    Resolution order, and the default is the interesting one:

    1. **`locations.source_root` in the config.** Absolute is used as-is;
       relative is resolved against the *graph* root, so `".."` means the
       enclosing repo and `"agi"` means a clone beside the tree. This is the
       explicit override — the "run against a custom source location" dial —
       and it is what makes both layouts expressible from one binary.
    2. **G11 layout** (`root` is `.agi/`): the enclosing repo. The graph sits
       inside what it builds, so the source is simply one level up and there is
       no staging copy at all.
    3. **Legacy, engine beside the tree** (`root/agi` exists): that directory.
       This is today's `agi-tree/agi` symlink and today's `fantasia/agi` clone,
       and it is why existing projects need no config change.
    4. **Otherwise** the graph root itself.

    Note what case 2 deletes: under G11 a `payload_ref` names a tracked file in
    the same worktree, so `payloads/` — the staged checkout that exists only
    because the bytes lived in one repo and had to be written into another —
    stops having a reason to exist.
    """
    root = Path(root).resolve()
    cfg = load_config(root) if config is None else config

    declared = (cfg.get("locations") or {}).get("source_root")
    if isinstance(declared, str) and declared.strip():
        p = Path(declared.strip()).expanduser()
        return p.resolve() if p.is_absolute() else (root / p).resolve()

    if is_graph_dir(root):
        return root.parent

    beside = root / "agi"
    if beside.exists():
        return beside.resolve()

    return root


def goals_path(root: Path, config: dict | None = None) -> Path:
    """Where the rendered goal document belongs.

    The value of `goals_file` decides how it is read, and the three forms exist
    for three real situations:

    - **Absolute** — used as-is. Escape hatch; no rules applied.
    - **Contains a separator** (`docs/GOALS.md`) — relative to the graph root.
      Full control for a project that wants the document filed somewhere
      specific.
    - **A bare filename** (the default, `GOALS.md`) — placed at the layout's
      natural home: the *repo* root under G11, the graph root under the legacy
      layout.

    The bare-name case is the one that matters and it is why this is not simply
    `root / "GOALS.md"`. Under G11 the graph lives at `<repo>/.agi`, and a goal
    document rendered to `<repo>/.agi/GOALS.md` would be invisible in a file
    listing and on GitHub — for the one document in the project that a human is
    most likely to open first. It renders to `<repo>/GOALS.md` instead.

    `goals_file` also settles the collision G11 creates: dropping the engine
    into a repo that already ships its own `GOALS.md` would otherwise have the
    renderer overwrite it. Such a project sets `goals_file` and keeps both.
    """
    root = Path(root).resolve()
    cfg = load_config(root) if config is None else config

    raw = cfg.get("goals_file")
    name = raw.strip() if isinstance(raw, str) and raw.strip() else DEFAULT_GOALS_FILE

    p = Path(name).expanduser()
    if p.is_absolute():
        return p.resolve()
    if len(p.parts) > 1:
        return (root / p).resolve()
    return repo_root(root) / p.name


# --- cli -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Print resolved locations. `--json` for machine use, plain for humans.

    Exists so the bash half and the shell can ask the same question this module
    answers, rather than reimplementing it a fourteenth time.
    """
    import argparse

    ap = argparse.ArgumentParser(description="Resolve agi project locations.")
    ap.add_argument("start", nargs="?", default=None,
                    help="directory to resolve from (default: cwd)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--what", choices=["root", "source", "goals", "repo"],
                    help="print one path and nothing else")
    args = ap.parse_args(argv)

    root = find_project_root(args.start)
    if root is None:
        start = args.start or os.getcwd()
        print(f"ERR: no agi project found from {start} — looked for "
              f"{GRAPH_DIR_NAME}/ or {CONFIG_NAMES[0]} walking up, then "
              f"<dir>/*-tree/ below", flush=True)
        return 1

    cfg = load_config(root)
    resolved = {
        "root": str(root),
        "repo": str(repo_root(root)),
        "source": str(source_root(root, cfg)),
        "goals": str(goals_path(root, cfg)),
        "layout": "graph_dir" if is_graph_dir(root) else "legacy",
    }

    if args.what:
        print(resolved[args.what])
    elif args.json:
        print(json.dumps(resolved, indent=2))
    else:
        for k in ("layout", "root", "repo", "source", "goals"):
            print(f"{k}: {resolved[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
