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
import re
import sys
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


#: What a build node's `location:` means when it does not say. Absent is the
#: overwhelmingly common case -- 224 build nodes predate the field -- and it
#: must keep meaning exactly what it has always meant.
DEFAULT_PAYLOAD_LOCATION = "source_root"


def payload_base(root: Path, location: str | None = None,
                 config: dict | None = None) -> Path:
    """The base a `payload_ref` resolves against, by NAME rather than by path.

    `goal:g13.1`, 2026-09-05. A build node used to resolve its payload against
    `source_root()` and nothing else, which made the base a hardcoded property
    of the code rather than a stated property of the node. That is fine while
    every payload lives in one tree and wrong the moment one does not -- a doc
    set beside the repo, a second checkout, a generated tree. Naming the base
    means a tree that moves is a config edit, never a sweep over every node.

    Names, in resolution order:

    1. **`source_root`** (the default) and **`repo_root`** and **`graph_root`**
       — the three roots the engine already knows.
    2. **Anything declared under `locations:` in the project config**, resolved
       the same way `source_root` is: absolute as given, relative against the
       graph root.

    **An unknown name is an error, never a fallback.** Silently resolving to
    the default would write bytes into the wrong tree and report success, which
    is the one failure mode a payload base can have that nobody would notice.
    """
    root = Path(root).resolve()
    cfg = load_config(root) if config is None else config
    name = (location or DEFAULT_PAYLOAD_LOCATION).strip()

    if name == "source_root":
        return source_root(root, cfg)
    if name == "graph_root":
        return root
    if name == "repo_root":
        return repo_root(root)

    declared = (cfg.get("locations") or {}).get(name)
    if isinstance(declared, str) and declared.strip():
        p = Path(declared.strip()).expanduser()
        return p.resolve() if p.is_absolute() else (root / p).resolve()

    known = ["source_root", "graph_root", "repo_root"]
    known += sorted(k for k in (cfg.get("locations") or {})
                    if isinstance(k, str) and k not in known)
    raise KeyError(
        f"unknown payload location {name!r}. Declare it under `locations:` in "
        f"the project config, or use one of: {', '.join(known)}."
    )


def resolve_payload_path(root: Path, ref: str, location: str | None = None,
                         config: dict | None = None) -> Path:
    """One node's payload, as an absolute path. The single place this is done.

    An absolute `payload_ref` is used as-is and its `location` is ignored --
    naming a base for a path that already has one is a contradiction, and the
    absolute path is the more specific statement.
    """
    p = Path(ref)
    if p.is_absolute():
        return p
    return payload_base(root, location, config) / p


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


# --- iterations ------------------------------------------------------------
#
# `hypothesis:loop-scoped-iteration-ids-cannot-clobber` (goal:g7). Every entry
# point under `bin/` used to format its own `f"iter-{iter_n:03d}"` — seven
# sites — and nothing anywhere *allocated* the number: `driver.sh` counted
# `seq 1 N` from one on every invocation, so a fresh run pointed itself at
# `sessions/iter-001`, which already held a real 23-agent manifest. Only
# `dispatch._merge_manifest` (goal:s28) stood between that and data loss, and
# it guards one file, not the directory (`iter-NNN-graph.json`, the per-agent
# `sess_dir`).
#
# This section is the one parser, the one formatter and the one allocator.
#
# **Two id schemes, one type each, and they cannot collide:**
#
#   legacy numeric   7      -> `iter-007`      an `int`  (1000+ dirs on disk)
#   loop-scoped      L1.08  -> `iter-L1.08`    a `str`   (loop label + counter)
#
# A numeric id stays an `int` on purpose — it is what every legacy manifest
# holds under `"iter"`, what `brief.py` prints, what `dispatch` restarts with —
# so nothing that reads a legacy directory changes shape. A loop-scoped id is
# a `str` whose label must start with a letter, so it can never parse as a
# number and the two schemes never share a directory name. The dir keeps the
# `iter-` prefix so a reader that lists iterations by prefix (`viewport.py`)
# sees both shapes without knowing there are two.
#
# The commit-subject convention this session already uses by hand — `L1.08:`
# — is the loop-scoped id verbatim. The driver prints it at the end of an
# iteration; it does not commit.

SESSIONS_DIR_NAME = "sessions"
ITER_DIR_PREFIX = "iter-"

#: A loop label: a letter first, so it can never be mistaken for a number.
LOOP_LABEL_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
_LOOP_ID_RE = re.compile(rf"^({LOOP_LABEL_RE.pattern})\.(\d+)$")
_NUMERIC_ID_RE = re.compile(r"^\d+$")

#: Loop label resolution: `--loop` > this env var > config key > newest loop
#: already on disk > DEFAULT_LOOP.
LOOP_ENV_VAR = "AGI_LOOP"
LOOP_CONFIG_KEY = "loop"
DEFAULT_LOOP = "L1"

#: Counter width inside a loop-scoped id (`L1.08`). Widens past 99 on its own;
#: allocation compares numerically, never lexically, so nothing depends on it.
LOOP_COUNTER_WIDTH = 2


class IterationOccupied(Exception):
    """An explicit iteration id names a directory that already holds data."""


def iteration_id(text: int | str) -> int | str:
    """Parse an iteration id from any spelling a caller might hand over.

    Accepts an int, a digit string, a loop-scoped id (`L1.08`, `L1.8`), or a
    session directory name with the `iter-` prefix on either. Returns the
    canonical id: an `int` for the numeric scheme, a `str` with a zero-padded
    counter for the loop-scoped one. Raises `ValueError` on anything else, so
    it can stand directly as an argparse `type=`.
    """
    if isinstance(text, bool):
        raise ValueError(f"not an iteration id: {text!r}")
    if isinstance(text, int):
        if text < 0:
            raise ValueError(f"not an iteration id: {text!r}")
        return text
    s = str(text).strip()
    if s.startswith(ITER_DIR_PREFIX):
        s = s[len(ITER_DIR_PREFIX):]
    if _NUMERIC_ID_RE.match(s):
        return int(s)
    m = _LOOP_ID_RE.match(s)
    if m:
        return format_loop_iteration(m.group(1), int(m.group(2)))
    raise ValueError(
        f"not an iteration id: {text!r} (want a number like 1039 or a "
        f"loop-scoped id like L1.08)")


def format_loop_iteration(loop: str, counter: int) -> str:
    """`("L1", 8)` -> `"L1.08"`."""
    if not LOOP_LABEL_RE.fullmatch(loop):
        raise ValueError(f"not a loop label: {loop!r} (a letter first, then "
                         f"letters, digits, '_' or '-')")
    return f"{loop}.{int(counter):0{LOOP_COUNTER_WIDTH}d}"


def iteration_loop(iter_id: int | str) -> str | None:
    """The loop label of a loop-scoped id; None for a numeric one."""
    iid = iteration_id(iter_id)
    if isinstance(iid, int):
        return None
    return _LOOP_ID_RE.match(iid).group(1)


def _iteration_counter(iter_id: int | str) -> int:
    iid = iteration_id(iter_id)
    return iid if isinstance(iid, int) else int(_LOOP_ID_RE.match(iid).group(2))


def iteration_dirname(iter_id: int | str) -> str:
    """`7` -> `iter-007` (byte-identical to the legacy format), `L1.08` ->
    `iter-L1.08`."""
    iid = iteration_id(iter_id)
    if isinstance(iid, int):
        return f"{ITER_DIR_PREFIX}{iid:03d}"
    return f"{ITER_DIR_PREFIX}{iid}"


def sessions_dir(root: Path) -> Path:
    return Path(root) / SESSIONS_DIR_NAME


def iteration_dir(root: Path, iter_id: int | str) -> Path:
    """`<root>/sessions/<iteration_dirname>` — the one place this is spelled."""
    return sessions_dir(root) / iteration_dirname(iter_id)


def list_iterations(root: Path) -> list[int | str]:
    """Every iteration id with a directory under `sessions/`, either scheme.

    Directories that carry the `iter-` prefix but parse as neither shape
    (`iter-s31-repro`) are not iterations and are skipped, as are the ad-hoc
    hand-made dirs with no prefix (`L1.08-scale`).
    """
    sess = sessions_dir(root)
    if not sess.is_dir():
        return []
    out: list[int | str] = []
    for p in sess.iterdir():
        if not p.is_dir() or not p.name.startswith(ITER_DIR_PREFIX):
            continue
        try:
            out.append(iteration_id(p.name))
        except ValueError:
            continue
    return out


def _newest_loop_on_disk(root: Path) -> str | None:
    """The label of the loop-scoped iteration directory touched most
    recently, or None when no loop-scoped iteration exists yet."""
    newest: tuple[float, str] | None = None
    for iid in list_iterations(root):
        loop = iteration_loop(iid)
        if loop is None:
            continue
        try:
            mtime = iteration_dir(root, iid).stat().st_mtime
        except OSError:
            continue
        if newest is None or mtime > newest[0]:
            newest = (mtime, loop)
    return newest[1] if newest else None


def loop_label(root: Path, explicit: str | None = None,
               config: dict | None = None) -> str:
    """Which loop a new iteration belongs to.

    A flag wins, then `$AGI_LOOP`, then the config key `loop` (graph content —
    a director bumping the loop edits the config and commits, the same way
    crons are declared), then the loop that most recently ran on disk, then
    `DEFAULT_LOOP`. The on-disk fallback is what makes a bare `driver.sh`
    continue the loop in progress instead of starting L1 forever.
    """
    for cand in (explicit, os.environ.get(LOOP_ENV_VAR)):
        if isinstance(cand, str) and cand.strip():
            label = cand.strip()
            if not LOOP_LABEL_RE.fullmatch(label):
                raise ValueError(f"not a loop label: {label!r}")
            return label
    cfg = load_config(root) if config is None else config
    declared = cfg.get(LOOP_CONFIG_KEY)
    if isinstance(declared, str) and declared.strip():
        label = declared.strip()
        if not LOOP_LABEL_RE.fullmatch(label):
            raise ValueError(f"config {LOOP_CONFIG_KEY!r} is not a loop label: {label!r}")
        return label
    return _newest_loop_on_disk(root) or DEFAULT_LOOP


def next_free_iteration(root: Path, loop: str | None = None, *,
                        after: int | str | None = None) -> int | str:
    """The lowest id, in one scheme, that no directory on disk carries.

    `loop=None` is the numeric scheme. `after`, when given, decides the scheme
    (its own) and is a floor: the result is strictly past it even if its
    directory does not exist — which is what lets a `--smoke` pass show the
    ids a live run *would* take, one per iteration, without claiming any.
    """
    if after is not None:
        after = iteration_id(after)
        loop = iteration_loop(after)
    taken = list_iterations(root)
    if loop is None:
        floor = after if isinstance(after, int) else 0
        nums = [i for i in taken if isinstance(i, int)]
        return max([floor, *nums]) + 1
    if not LOOP_LABEL_RE.fullmatch(loop):
        raise ValueError(f"not a loop label: {loop!r}")
    floor = _iteration_counter(after) if isinstance(after, str) else 0
    counters = [_iteration_counter(i) for i in taken
                if isinstance(i, str) and iteration_loop(i) == loop]
    return format_loop_iteration(loop, max([floor, *counters]) + 1)


def _occupancy(d: Path) -> str | None:
    """What an iteration directory already holds, as a phrase, or None."""
    if not d.is_dir():
        return None
    if (d / "manifest.json").is_file():
        return "a manifest"
    try:
        n = sum(1 for _ in d.iterdir())
    except OSError:
        return "unreadable contents"
    return f"{n} entr{'y' if n == 1 else 'ies'}" if n else None


def claim_iteration(root: Path, *, loop: str | None = None,
                    explicit: int | str | None = None,
                    after: int | str | None = None,
                    dry_run: bool = False) -> int | str:
    """Allocate an iteration id and reserve its directory. Never assumes one.

    - `explicit` is honoured only if its directory is absent or empty.
      Anything already there — a manifest above all — raises
      `IterationOccupied`; this is the refusal that replaces the clobber.
    - Otherwise the next free id in the scheme (`after`'s, else `loop`'s,
      else numeric) is taken with a bare `mkdir`, which is atomic: two
      drivers racing for the same id cannot both win it. A lost race moves
      past the contested id and tries again.
    - `dry_run` returns the id it would claim and creates nothing.
    """
    root = Path(root)
    if explicit is not None:
        iid = iteration_id(explicit)
        d = iteration_dir(root, iid)
        held = _occupancy(d)
        if held:
            raise IterationOccupied(
                f"iteration {iid} already holds {held} at {d} — refusing to "
                f"reuse it. Drop --iter to allocate the next free id, or name "
                f"one whose directory is empty.")
        if not dry_run:
            d.mkdir(parents=True, exist_ok=True)
        return iid

    for _ in range(1000):
        iid = next_free_iteration(root, loop, after=after)
        if dry_run:
            return iid
        d = iteration_dir(root, iid)
        sessions_dir(root).mkdir(parents=True, exist_ok=True)
        try:
            d.mkdir()
        except FileExistsError:
            after = iid   # lost a race for this id; look strictly past it
            continue
        return iid
    raise IterationOccupied(
        f"could not claim a free iteration under {sessions_dir(root)} in "
        f"1000 attempts")


# --- cli -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Print resolved locations. `--json` for machine use, plain for humans.

    Exists so the bash half and the shell can ask the same question this module
    answers, rather than reimplementing it a fourteenth time. `--claim-iter`
    is the same idea for the allocator: `driver.sh` asks here for its next
    iteration id rather than counting in bash.
    """
    import argparse

    ap = argparse.ArgumentParser(description="Resolve agi project locations.")
    ap.add_argument("start", nargs="?", default=None,
                    help="directory to resolve from (default: cwd)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--what", choices=["root", "source", "goals", "repo"],
                    help="print one path and nothing else")
    ap.add_argument("--claim-iter", action="store_true",
                    help="allocate the next free iteration id, reserve its "
                         "sessions dir, print the id")
    ap.add_argument("--loop", default=None,
                    help=f"with --claim-iter: the loop label (default: "
                         f"${LOOP_ENV_VAR}, then config `{LOOP_CONFIG_KEY}`, "
                         f"then the newest loop on disk, then {DEFAULT_LOOP})")
    ap.add_argument("--iter", dest="explicit_iter", default=None,
                    help="with --claim-iter: use exactly this id; refused if "
                         "its directory already holds anything")
    ap.add_argument("--after", default=None,
                    help="with --claim-iter: allocate strictly past this id, "
                         "in its own scheme")
    ap.add_argument("--numeric", action="store_true",
                    help="with --claim-iter: the legacy iter-NNN scheme")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --claim-iter: print the id, create nothing")
    args = ap.parse_args(argv)

    root = find_project_root(args.start)
    if root is None:
        start = args.start or os.getcwd()
        print(f"ERR: no agi project found from {start} — looked for "
              f"{GRAPH_DIR_NAME}/ or {CONFIG_NAMES[0]} walking up, then "
              f"<dir>/*-tree/ below", flush=True)
        return 1

    if args.claim_iter:
        try:
            loop = None if args.numeric else loop_label(root, args.loop)
            iid = claim_iteration(root, loop=loop, explicit=args.explicit_iter,
                                  after=args.after, dry_run=args.dry_run)
        except (IterationOccupied, ValueError) as exc:
            print(f"ERR: {exc}", file=sys.stderr, flush=True)
            return 1
        print(iid)
        return 0

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
