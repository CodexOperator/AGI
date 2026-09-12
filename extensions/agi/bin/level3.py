#!/usr/bin/env python3
"""level3.py — one level-3 node per code file, carrying a machine-attached contract.

Reads the **engine repo** (this repo — `agi`, not the graph repo) and writes one
`type: level3` node per Python file under `extensions/agi/src/**/*.py` and
`extensions/agi/bin/*.py` into `<PROJECT_ROOT>/nodes/level3/`. See
`hyp:level3-node-anatomy` and `goal:g2.1` in the graph repo for the design
this script implements — read those before changing this file's shape.

Level 3 = one canonical node per *file* (not per class, not per symbol). The
node's frontmatter carries no new keys beyond what other generated nodes
already use: `payload_ref` is the repo-relative path to the file (the code
surface itself lives on disk exactly once — it is never inlined into the node
body), `origin` marks harness provenance (`level3-scan`). The interesting
content — the contract / IO map — lives in the node **body**, inside
harness-owned markers, one entry per input and output:
`{name, how, why, perf, security}`.

`how` is mechanically derived with the standard library `ast` module:
  - imports                              -> inputs
  - `sys.argv` / `argparse` / env / stdin -> inputs
  - detected file-read call sites         -> inputs
  - top-level function/class definitions -> outputs
  - detected file-write call sites        -> outputs
  - `print()` call sites                  -> outputs (stdout)
A call site whose read/write *direction* cannot be statically resolved (e.g.
`open(path, mode)` where `mode` is not a string literal) is not guessed into
either bucket — it goes into a third `uncovered` list with `how` explaining
why. A file that fails to parse gets `parse_ok: false` and an empty contract,
not an invented one.

Every code fragment quoted in a `how` (and every entry `name` derived from an
expression) is a **literal slice of the payload's own source**, taken with
`ast.get_source_segment` and collapsed to one line — never re-rendered with
`ast.unparse`. `ast.unparse` is a function of the payload *and* the CPython
version that ran the scan (PEP 701 changed f-string rendering in 3.12), and a
derivation that is not a function of the payload alone leaves the graph dirty
for whoever scans next. See `_render` and `goal:s19`.

`why`, `perf`, `security` are never mechanically derivable — they are emitted
as explicit `TODO(model)` placeholders. The harness owns the block's shape
(field names, ordering, which entries exist); a later model pass may only
fill those three free-text slots per entry, never invent or drop a field.

Parent linkage: a level-3 node's `parents:` points at the `idea:engine-*`
census node (written by `decompose-engine.py`) whose `unit_path` covers this
file — exact match for a `bin_script` unit, directory-prefix match for a
`src_package` unit. Read from `nodes/idea/*.md` in the project, never
inferred from the file tree itself. A file matching no census unit is
emitted **parentless** and printed as `NO_PARENT` — never guessed.

Scope is deliberately narrow: `extensions/agi/src/**/*.py` and
`extensions/agi/bin/*.py` only (~70 files). Shell scripts
(`driver.sh`, `find-root.sh`, `cc-session-start.sh`) and the TypeScript
bridge (`extensions/agi-bridge/index.ts`) are out of scope for this first
pass — no ast-equivalent mechanical `how` derivation is implemented for them
here, so scanning them would force a choice between silently skipping their
contract or fabricating one. Neither is acceptable; they are just not
discovered.

Three safety properties this script must hold (see decompose-engine.py's
precedent, and TODO.md's H0e-g/H0i entries for why these are non-negotiable
for this shape of generator):

1. Field erasure — reuses `write_frontmatter(..., preserve=existing_fm)` from
   snapshot-goals.py verbatim (imported by file path, not re-implemented).
2. Prune reach — stamps `origin: level3-scan` and prunes *only* nodes
   carrying that exact stamp. A missing/unreadable engine tree is a no-op:
   nothing is written and nothing is pruned.
3. The override door — this script has no project-local lookup. It is
   invoked directly; wiring it into `driver.sh` (if ever) must stay
   plugin-only.

Run: `python3 bin/level3.py [--dry-run] [--project PATH] [--engine-root PATH]`
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

import yaml

ORIGIN = "build-scan"

#: Sibling of the per-type node directories, holding retired nodes under the
#: same per-type split: `nodes/deprecated/build/`, `nodes/deprecated/goal/`, …
#:
#: A retired node is kept, never deleted — deleting one would orphan its grid
#: ref, which outlives the file, so removal decouples durable structure rather
#: than removing it (goal:g2.10). Moving it changes only its **address**, which
#: is derived and expected to change on regroup; its **mint id** is untouched,
#: so every grid ref and every provenance link keeps resolving (goal:g2.5).
#:
#: Readers that walk `nodes/` with `rglob` need no change. The few that glob a
#: single type directory do, and they call `node_type_dirs()` below rather than
#: hardcoding one path — a reader that silently stops seeing retired nodes is
#: how a deprecation becomes a deletion nobody authorised.
DEPRECATED_DIRNAME = "deprecated"


def node_type_dirs(project_root: Path, type_name: str,
                   legacy: str | None = None) -> list[Path]:
    """Every directory holding nodes of one type: live first, then retired.

    Order matters and is live-first: callers that take the first hit (id
    lookup, path resolution) must find the live node, not a retired namesake.
    Only directories that exist are returned, so a project with no retired
    nodes yields exactly what it did before this existed.
    """
    nodes_root = Path(project_root) / "nodes"
    names = [type_name] + ([legacy] if legacy else [])
    out: list[Path] = []
    for name in names:
        for d in (nodes_root / name,
                  nodes_root / DEPRECATED_DIRNAME / name):
            if d.is_dir() and d not in out:
                out.append(d)
    return out


def iter_type_nodes(project_root: Path, type_name: str,
                    legacy: str | None = None):
    """`*.md` under every directory for one type, live first, sorted per dir."""
    for d in node_type_dirs(project_root, type_name, legacy):
        yield from sorted(d.glob("*.md"))

#: The pre-2026-08-27 origin stamp. Read for recognition, NEVER for pruning.
#: The asymmetry is the whole safety property: a straggler still stamped
#: `level3-scan` is left alone rather than deleted, because "this scan does
#: not recognise it" and "this node is stale" are different statements and
#: only the second licenses removal. Pruning on the legacy stamp is exactly
#: how a half-applied rename becomes H0i (S11).
LEGACY_ORIGIN = "level3-scan"

#: Payload suffixes that make a build node `build_kind: code`. Everything
#: else is `prose`. Mechanical on purpose -- G6.8's boundary is only a
#: boundary if it answers without a human adjudicating.
CODE_SUFFIXES = frozenset({".py", ".sh", ".ts", ".js"})


def build_kind_for(rel_path: str) -> str:
    """`code` or `prose`, from the payload suffix alone."""
    from pathlib import Path as _P
    return "code" if _P(rel_path).suffix.lower() in CODE_SUFFIXES else "prose"

BIN_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN_DIR.parent  # .../extensions/agi
# This script lives at <engine repo root>/extensions/agi/bin/level3.py.
# BIN_DIR is .../extensions/agi/bin, so three levels up (agi -> extensions ->
# repo root) is the engine repo we scan. Overridable with --engine-root,
# chiefly for tests. (Same convention as decompose-engine.py; that script's
# own history records this exact off-by-one as a caught bug — pinned by a
# dedicated test here too.)
DEFAULT_ENGINE_ROOT = BIN_DIR.parents[2]

#: goal:g11.1, third instance of the same residual (after snapshot-goals.py and
#: grid.py). The `os.getcwd()` fallback resolved to the REPO root under the
#: `.agi` layout, so `level3.py` wrote its build nodes to `<repo>/nodes/build`
#: instead of `<repo>/.agi/nodes/build` — creating a second, stray node tree
#: beside the real one. Combined with the boundary bug fixed in
#: `payload_boundary.is_the_graph_itself`, that stray tree then became input to
#: the next scan. Computed per-run in `main`, never at import: a module-import
#: time `project_root_from_env()`/`getcwd()` bakes the *importing* process's
#: cwd in, and tests import level3 from anywhere.
PROJECT_ROOT: Path | None = None


def resolve_project_root(path: Path) -> Path | None:
    """Resolve a `--project` value to the GRAPH ROOT, or None when it resolves
    to no graph at all (goal:g15, hypothesis:l4-stitch-and-level3-project-
    resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count).
    Never a literal `<p>/nodes`: accepts the path itself when it holds
    `nodes/` directly (legacy), else the nearest enclosing `.agi/` via
    `locations` (the one resolver), else None for the caller to refuse
    by name rather than scan an empty tree as authoritative.
    """
    p = Path(path).resolve()
    if (p / "nodes").is_dir():
        return p
    return locations.find_project_root(p)


def default_project_root() -> Path | None:
    """The graph root for a no-`--project` run, or None when there is no graph.

    Resolves through the SAME `resolve_project_root` as the `--project` flag so
    the two spells cannot disagree (goal:g15, hypothesis:l4-level3-no-flag-
    default-refuses-a-rootless-cwd-and-the-sl7-25-body-names-its-missing-and-
    orphan-counts): the env override first (it may descend into `.agi/` — see
    `locations.project_root_from_env`), else the cwd. Env-first is deliberate:
    a caller that already exported a project root is never overridden by the
    directory the run happens to start in. None reaches `main`, which refuses
    by name rather than scan a stray `<cwd>/nodes/...` tree as authoritative.
    """
    env_root = locations.project_root_from_env()
    if env_root is not None:
        return env_root
    return resolve_project_root(Path.cwd())


def _set_project_root(path: Path) -> None:
    global PROJECT_ROOT
    PROJECT_ROOT = Path(path).resolve()


# --- reuse snapshot-goals.py's write_frontmatter / load_existing_nodes -----
# Loaded by file path (not `import`) because the filename has a hyphen and is
# not a valid module name. This is the actual function, not a copy — see
# module docstring point 1 (field erasure). Same pattern decompose-engine.py
# uses for the identical reason.
_SNAPSHOT_GOALS_PATH = BIN_DIR / "snapshot-goals.py"
_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter

# --- the contract reader (goal:g2.10) --------------------------------------
# Moved here from stitch.py on 2026-08-27, because this file "owns the
# contract shape" (stitch.py's own module docstring) and, from g2.10 onward,
# has to read a stored contract back before it can rewrite one. It could not
# import stitch.py to get it: stitch.py already imports *this* file for
# `analyze_file` and `discover_files`, so the borrow was an import cycle and
# died with RecursionError on the first run. Ownership decides direction —
# stitch.py now aliases these instead.
#
# Both marker spellings. `LEVEL3-CONTRACT` was renamed to `BUILD-CONTRACT` on
# 2026-08-27; a reader that recognised only the new one would report every
# unmigrated node as having no contract at all, which `--strict` turns into
# drift and `publish-engine.sh` turns into a refusal.
_MARKER_SPAN_RE = re.compile(
    r"(?:LEVEL3|BUILD)-CONTRACT:BEGIN(.*?)(?:LEVEL3|BUILD)-CONTRACT:END", re.DOTALL)
_YAML_FENCE_OPEN = "```yaml"
_FENCE = "```"
NO_CONTRACT_BLOCK = "no BUILD-CONTRACT block found in body"


def extract_contract(body: str) -> tuple[dict | None, str | None]:
    """Pull the fenced YAML contract block out of a node body.

    Returns (contract_dict, None) on success, (None, reason) on failure. A
    node with no contract markers, or an unparsable contract, is reported —
    never silently treated as fresh (that would hide exactly the kind of
    drift this tool exists to find).

    Bounding matters more than it looks: a `how` field can (and, on the real
    corpus, does — `build:bin-heal`) contain a mechanically-unparsed call
    site whose literal text itself embeds a ``` fence, e.g. an f-string
    template being written to disk that contains a markdown code block. A
    naive "first ``` after ```yaml" search stops at that embedded fence, not
    the real closing one, and truncates the block mid-string — invalid YAML,
    not because the file is malformed but because the *parser* guessed
    wrong. So: bound first by the harness markers (which model-authored prose
    can only ever appear outside of), then take the *last* ``` inside that
    bounded span as the closing fence, not the first.
    """
    span_m = _MARKER_SPAN_RE.search(body)
    if not span_m:
        return None, NO_CONTRACT_BLOCK
    span = span_m.group(1)
    open_idx = span.find(_YAML_FENCE_OPEN)
    if open_idx == -1:
        return None, "no ```yaml fence found inside BUILD-CONTRACT block"
    after_open = span[open_idx + len(_YAML_FENCE_OPEN):]
    if after_open.startswith("\n"):
        after_open = after_open[1:]
    close_idx = after_open.rfind(_FENCE)
    if close_idx == -1:
        return None, "no closing ``` fence found inside BUILD-CONTRACT block"
    yaml_text = after_open[:close_idx]
    try:
        contract = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return None, f"contract block is not valid YAML: {exc}"
    if not isinstance(contract, dict):
        return None, "contract block did not parse to a mapping"
    return contract, None


# --- reuse payload_boundary.py's classify() (the G6.8 boundary predicate) ---
# Loaded by file path for the same reason snapshot-goals.py is above: one
# definition, never re-implemented. See `goal:g6.8` /
# `mvp:payload-boundary-predicate` for the rule.
_PAYLOAD_BOUNDARY_PATH = BIN_DIR / "payload_boundary.py"
_pb_spec = importlib.util.spec_from_file_location(
    "payload_boundary", _PAYLOAD_BOUNDARY_PATH)
payload_boundary = importlib.util.module_from_spec(_pb_spec)
_pb_spec.loader.exec_module(payload_boundary)


# grid.py, by file path — same rule, same reason: `--from-grid` resolves
# payloads out of `refs/grid/node/<mint-id>`, and grid.py is the one definition
# of how those refs are named and read (goal:g6.1).
_GRID_PATH = BIN_DIR / "grid.py"
_grid_spec = importlib.util.spec_from_file_location("grid_for_level3", _GRID_PATH)
grid = importlib.util.module_from_spec(_grid_spec)
_grid_spec.loader.exec_module(grid)


def grid_payload_for(project_root: Path, node_path: Path) -> bytes | None:
    """The payload bytes recorded in `node_path`'s grid ref, or None.

    None is returned — never a fallback to disk — for a node with no mint id,
    no ref, or no payload entry yet. The caller reports it and derives from the
    engine tree instead, saying which source it used. A silent fallback would
    make `--from-grid` a no-op that reads like a success, which is the failure
    `stitch.py --from-grid` was already written to avoid.
    """
    node_id = grid.parse_node_id(node_path)
    if node_id is None:
        return None
    ref = grid._resolve_read_ref(project_root, node_path, node_id)
    if ref is None:
        return None
    entry = grid.read_tree_entry(project_root, ref, grid.PAYLOAD_ENTRY)
    return entry[1] if entry else None


# --- file discovery -----------------------------------------------------------

# Retained for tests and for the record: the pre-G6.8 scope. Nothing reads
# these for discovery any more.
SRC_PREFIX = "extensions/agi/src/"
BIN_PREFIX = "extensions/agi/bin/"


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


def discover_files(engine_root: Path,
                   payload_root: Path | None = None) -> list[str] | None:
    """Tracked files passing the G6.8 payload-boundary predicate, or None on a
    no-op (missing/unreadable engine root, or not a git repo).

    This scanned only `extensions/agi/src/**/*.py` and `extensions/agi/bin/*.py`
    (~74 files). `goal:g6.6` named that scope as the thing blocking G6.1: the
    skill doc, the kid brief, every shell surface and every non-`.py` file were
    invisible to the graph. `payload_boundary.classify()` is the mechanical
    boundary `goal:g6.8` drew to replace it — every tracked file is `in` unless
    gitignore-declared transient, under a `tests/fixtures/` directory, or a
    `.jsonl` event stream. No per-extension allowlist.

    A non-Python file that passes the boundary still gets a node;
    `analyze_file` degrades anything `ast` cannot parse to `parse_ok: false`
    with an empty contract. That is the honest output here — see
    `verdict:noncode-coverage` for why a real prose contract is deliberately
    not attempted at this step.
    """
    if not engine_root.is_dir():
        return None
    try:
        rows = payload_boundary.classify(engine_root)
    except Exception:
        # Any failure inside classify() (missing repo, git erroring) collapses
        # to the same no-op signal the old git_ls_files() gave — never a
        # partial or guessed file list.
        return None
    found = {f for f, verdict, _reason in rows if verdict == "in"}
    found |= discover_payload_only_files(engine_root, payload_root, found)
    return sorted(found)


def discover_payload_only_files(engine_root: Path, payload_root: Path | None,
                                already: set[str]) -> set[str]:
    """Files that exist in the graph's payload checkout and nowhere else.

    **This is how a NEW file enters the graph graph-first (goal:g6.1).** Before
    it existed, discovery asked `git ls-files` on the engine and nothing else,
    so a script authored in `payloads/` was invisible to `level3.py`, never got
    a node, never got a `payload_ref`, and was therefore never committed to the
    grid or published — it lived in exactly one gitignored directory. Writing a
    new engine file still meant touching the engine repo first, which is the
    one thing the closed loop is supposed to remove.

    Same boundary predicate as the engine side (`classify_paths`), so a fixture
    or a `.jsonl` stream authored here is excluded for the same reason it is
    excluded there.
    """
    if payload_root is None or not payload_root.is_dir():
        return set()
    candidates = []
    for p in payload_root.rglob("*"):
        if p.is_dir() and not p.is_symlink():
            continue
        rel = str(p.relative_to(payload_root))
        if rel in already:
            continue
        candidates.append(rel)
    try:
        rows = payload_boundary.classify_paths(engine_root, candidates)
    except Exception:
        return set()
    new = {f for f, verdict, _reason in rows if verdict == "in"}
    for f in sorted(new):
        print(f"NEW: {f} exists only in the payload checkout — minting its node "
              f"(goal:g6.1)")
    return new


# --- ast-based contract derivation --------------------------------------------

_READ_ATTR_METHODS = {"read_text", "read_bytes"}
_WRITE_ATTR_METHODS = {"write_text", "write_bytes"}
_READ_FUNCS = {
    ("json", "load"), ("json", "loads"),
    ("yaml", "safe_load"), ("yaml", "load"), ("yaml", "full_load"),
    ("pickle", "load"),
}
_WRITE_FUNCS = {
    ("json", "dump"), ("json", "dumps"),
    ("yaml", "safe_dump"), ("yaml", "dump"),
    ("pickle", "dump"),
}


_CAP_LEN = 240


def _cap(s: str | None, limit: int = _CAP_LEN) -> str | None:
    """Bound a mechanically-derived text fragment to `limit` chars.

    A rendered call site reproduces the full source of that call — including a
    multi-line string literal argument (e.g. a template being written to disk),
    verbatim. Left uncapped, one such call can dominate the whole contract
    block with hundreds of characters of literal content. Truncating says so
    explicitly rather than silently clipping, so `how` stays honest about being
    partial.

    Always applied *after* `_one_line`, never before: the cap is a budget for
    content, and a source slice indented eight levels deep would otherwise
    spend most of it on leading whitespace.
    """
    if s is None or len(s) <= limit:
        return s
    return s[:limit] + f"...[truncated, {len(s)} chars total]"


#: A run of whitespace that **contains a line break**, plus the horizontal
#: whitespace hugging it on either side. Deliberately not `\s+`.
_LINE_JOIN = re.compile(r"[^\S\r\n]*[\r\n]+[^\S\r\n]*")


def _one_line(s: str | None) -> str | None:
    """Join a source slice onto one line; leave whitespace *within* a line alone.

    `how` is a single YAML scalar. A source slice carries the file's real
    newlines and original indentation, and roughly 7% of the call sites on this
    corpus span more than one line. Emitting those raw would put multi-line
    scalars into the `BUILD-CONTRACT` block — which YAML can carry, but which
    makes `_cap`'s budget meaningless and the block far harder to read.

    **The first version of this collapsed `\\s+`, and that was wrong.** Most of
    what this engine writes is indentation-sensitive text — YAML fragments,
    markdown, node bodies — held in string literals whose escaped newlines
    (`\\n`, two characters) are followed by *real* spaces that are content, not
    layout. `\\s+` silently rewrote `f"---\\nfields:\\n  {fields}:"` to
    `...\\n {fields}:`, i.e. it reported an indentation the payload does not
    have. A contract that quietly alters what it quotes is worse than one that
    quotes too much. Caught by
    `test_how_quotes_the_payload_source_rather_than_re_rendering_it`, which
    asserts the quoted fragment is a verbatim substring of the payload.

    So: only runs containing `\\r`/`\\n` collapse, which is exactly the set that
    would otherwise break the scalar across lines. Every remaining character
    inside a line is the payload's own. A triple-quoted template holding *real*
    newlines is still flattened — unavoidable if `how` is one line, and the same
    information `ast.unparse` used to escape to `\\n`.

    Collapsing is a pure function of its input, so it costs nothing against the
    property this whole path exists to hold (goal:s19). It is not free of all
    cost: 38 of 10,099 call sites here span lines *and* carry a `#` comment, and
    joining those puts the comment text inline, where it reads as if it
    swallowed the rest of the call. That is cosmetic and deterministic;
    stripping comments would mean re-rendering from tokens, i.e. building a
    second renderer — the interpreter-dependent thing being removed.
    """
    if s is None:
        return None
    return _LINE_JOIN.sub(" ", s).strip()


def _unparse_safe(node: ast.AST | None) -> str | None:
    """`ast.unparse`, or None. **The fallback, not the derivation** — see `_render`."""
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def _render(source: str | None, node: ast.AST | None) -> str | None:
    """One line of literal source for `node`. The single chokepoint every
    `how` and every derived entry `name` passes through (goal:s19).

    This used to be `ast.unparse(node)`, which re-renders the AST rather than
    quoting the file — and `ast.unparse` is **not** a function of the AST
    alone. PEP 701 rewrote f-string parsing in 3.12, so the same node renders
    differently under 3.11 and 3.12:

        3.11.15  ->  (d / name).write_text(f"---\\nfields:\\n  {fields}: ...
        3.12.3   ->  (d / name).write_text(f'---\\nfields:\\n  {fields}: ...

    A stored contract the next scan does not reproduce leaves the graph
    permanently dirty and shuts `publish-engine.sh`'s first gate (goal:g6.5).
    Here it was worse than permanent — it was *intermittent*: the `:37` cron
    runs 3.12 and an interactive shell picks up 3.11 from a venv, so the node
    flapped back and forth, each flap burning a real grid version on a file
    nobody edited.

    `ast.get_source_segment` returns the literal slice of the file, so it is
    interpreter-independent by construction and strictly more faithful — it
    shows what is written rather than a normalisation of it.

    **The fallback is reachable for exactly one node type: `ast.arguments`.**
    `get_source_segment` needs `lineno`/`col_offset`, and `arguments` is
    neither a `stmt` nor an `expr` and carries none — it returns None for all
    1,241 top-level signatures in this engine. Slicing it out by hand is not
    available either: `vararg`'s own position starts at the *name*, so a span
    built from the child nodes silently drops the `*` in `*args`, and the `/`
    in a positional-only list has no node at all. Matching parentheses in the
    text would need a tokenizer, i.e. a second renderer.

    So signatures keep `ast.unparse`, and the justification is measured, not
    assumed: the only construct known to render differently across these
    versions is an f-string, `ast.unparse(node.args)` is byte-identical under
    3.11.15 and 3.12.3 for all 1,241 of them, and zero signatures in this
    corpus contain an f-string at all (a default or an annotation would be the
    only way in). `test_signature_fallback_is_the_only_unparse_path` pins that
    this fallback stays a single named case rather than a quiet default.
    """
    if node is None:
        return None
    seg = None
    if source is not None:
        try:
            seg = ast.get_source_segment(source, node)
        except Exception:
            seg = None
    if seg is None:
        seg = _unparse_safe(node)
    return _one_line(seg)


def _scan_imports(tree: ast.Module) -> list[dict]:
    inputs = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                disp = alias.asname or alias.name
                stmt = f"import {alias.name}"
                if alias.asname:
                    stmt += f" as {alias.asname}"
                inputs.append({"name": disp, "how": f"`{stmt}` at line {node.lineno}"})
        elif isinstance(node, ast.ImportFrom):
            mod_prefix = "." * node.level + (node.module or "")
            for alias in node.names:
                disp = f"{mod_prefix}.{alias.name}" if mod_prefix else alias.name
                stmt = f"from {mod_prefix} import {alias.name}"
                if alias.asname:
                    stmt += f" as {alias.asname}"
                inputs.append({"name": disp, "how": f"`{stmt}` at line {node.lineno}"})
    return inputs


def _scan_top_level_defs(tree: ast.Module, source: str) -> list[dict]:
    """`source` is required, not defaulted, on purpose: a caller that forgot it
    would fall back to `ast.unparse` for every entry and reintroduce goal:s19
    silently. A missing argument is a TypeError; a silent default is a flap."""
    outputs = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if isinstance(node, ast.AsyncFunctionDef):
                kind = "async function"
            elif isinstance(node, ast.FunctionDef):
                kind = "function"
            else:
                kind = "class"
            vis = "private" if node.name.startswith("_") else "public"
            sig = ""
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # `node.args` is the one node with no position — `_render`
                # falls back to `ast.unparse` here and only here. See its
                # docstring for the measurement that licenses that.
                sig = _cap(_render(source, node.args)) or ""
            how = f"defines {vis} {kind} `{node.name}` at line {node.lineno}"
            if sig:
                how += f", signature: ({sig})"
            outputs.append({"name": node.name, "how": how})
    return outputs


def _scan_io_calls(tree: ast.Module,
                   source: str) -> tuple[list[dict], list[dict], list[dict]]:
    """Detected filesystem-shaped read/write call sites.

    `source` is required, not defaulted — see `_scan_top_level_defs`.

    Scope is deliberately bounded: `open()`, `pathlib.Path`'s `.read_text` /
    `.write_text` / `.read_bytes` / `.write_bytes`, and `json`/`yaml`/`pickle`
    load/dump. Subprocess, socket, and generic `.read()`/`.write()` (which
    could be a file, a pipe, a StringIO, ...) are not attempted — classifying
    those would require type inference this pass does not do, and a wrong
    guess is worse than not attempting it.
    """
    reads: list[dict] = []
    writes: list[dict] = []
    uncovered: list[dict] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func

        if isinstance(func, ast.Name) and func.id == "open":
            mode_node = node.args[1] if len(node.args) >= 2 else None
            for kw in node.keywords:
                if kw.arg == "mode":
                    mode_node = kw.value
            call_src = _cap(_render(source, node)) or f"open(...) at line {node.lineno}"
            if mode_node is None:
                mode = "r"  # open()'s documented default — not a guess
            elif isinstance(mode_node, ast.Constant) and isinstance(mode_node.value, str):
                mode = mode_node.value
            else:
                uncovered.append({
                    "name": (_cap(_render(source, node.args[0]), 80) if node.args
                             else f"open() at line {node.lineno}"),
                    "how": (f"uncovered — `{call_src}` at line {node.lineno}: mode is a "
                            f"non-literal expression, read/write direction cannot be "
                            f"statically resolved"),
                })
                continue
            target = _cap(_render(source, node.args[0]), 80) if node.args else None
            entry_name = target or f"open() call at line {node.lineno}"
            entry = {"name": entry_name,
                      "how": f"`{call_src}` at line {node.lineno} (mode={mode!r})"}
            (writes if any(c in mode for c in "wax") else reads).append(entry)
            continue

        if isinstance(func, ast.Attribute) and func.attr in (_READ_ATTR_METHODS | _WRITE_ATTR_METHODS):
            target = _cap(_render(source, func.value), 80)
            call_src = _cap(_render(source, node)) or f"{func.attr}(...) at line {node.lineno}"
            entry_name = target or f"{func.attr}() call at line {node.lineno}"
            entry = {"name": entry_name, "how": f"`{call_src}` at line {node.lineno}"}
            (reads if func.attr in _READ_ATTR_METHODS else writes).append(entry)
            continue

        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            key = (func.value.id, func.attr)
            call_src = _cap(_render(source, node)) or f"{func.value.id}.{func.attr}(...) at line {node.lineno}"
            entry = {"name": f"{func.value.id}.{func.attr}",
                      "how": f"`{call_src}` at line {node.lineno}"}
            if key in _READ_FUNCS:
                reads.append(entry)
            elif key in _WRITE_FUNCS:
                writes.append(entry)
    return reads, writes, uncovered


def _scan_cli_and_env(tree: ast.Module) -> list[dict]:
    inputs = []
    seen_argv = False
    seen_argparse = False
    seen_stdin = False
    env_vars: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "argv":
            if isinstance(node.value, ast.Name) and node.value.id == "sys":
                seen_argv = True
        if isinstance(node, ast.Attribute) and node.attr == "stdin":
            if isinstance(node.value, ast.Name) and node.value.id == "sys":
                seen_stdin = True
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and f.attr == "ArgumentParser":
                seen_argparse = True
            if (isinstance(f, ast.Attribute) and f.attr in ("getenv", "get")
                    and isinstance(f.value, ast.Name) and f.value.id == "os"):
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    env_vars.add(node.args[0].value)
            if isinstance(f, ast.Name) and f.id == "input":
                seen_stdin = True
        if isinstance(node, ast.Subscript):
            val = node.value
            if (isinstance(val, ast.Attribute) and val.attr == "environ"
                    and isinstance(val.value, ast.Name) and val.value.id == "os"):
                sl = node.slice
                key_node = sl.value if isinstance(sl, ast.Index) else sl  # py<3.9 vs 3.9+
                if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                    env_vars.add(key_node.value)
    if seen_argv or seen_argparse:
        how = "reads `sys.argv`" if seen_argv else ""
        if seen_argparse:
            how = (how + " / " if how else "") + "builds an `argparse.ArgumentParser`"
        inputs.append({"name": "cli-args", "how": how + " (module-wide, no single call site)"})
    for var in sorted(env_vars):
        inputs.append({"name": f"env:{var}",
                        "how": f"reads `os.environ`/`os.getenv` for literal key {var!r}"})
    if seen_stdin:
        inputs.append({"name": "stdin", "how": "reads `sys.stdin` / calls `input()`"})
    return inputs


def _scan_stdout(tree: ast.Module) -> list[dict]:
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            lines.append(node.lineno)
    if not lines:
        return []
    return [{"name": "stdout",
             "how": f"{len(lines)} `print()` call(s) at line(s) {sorted(set(lines))}"}]


def _content_sha256(abs_path: Path) -> str:
    """sha256 of the payload's raw bytes, or `unreadable` if it cannot be read.

    Bytes, not decoded text: a fingerprint that depends on an encoding guess is
    not a fingerprint. Returns a string either way so the contract's shape stays
    fixed — a missing key would read as drift on every subsequent scan.
    """
    try:
        return hashlib.sha256(abs_path.read_bytes()).hexdigest()
    except Exception:
        return "unreadable"


def analyze_file(abs_path: Path) -> dict:
    """Mechanically derive the contract's `how` half from a file **on disk**.

    Thin wrapper over `analyze_source`, which is the real derivation. Kept as
    the disk-facing entry point because that is what every caller has used
    since this script existed, and because a file that cannot be *read* is a
    distinguishable failure from one that cannot be *parsed*.
    """
    try:
        data = abs_path.read_bytes()
    except Exception as exc:
        return {"parse_ok": False, "parse_error": f"unreadable: {exc}",
                "inputs": [], "outputs": [], "uncovered": []}
    return analyze_source(data, abs_path.suffix, str(abs_path))


def analyze_source(data: bytes, suffix: str, name: str = "<payload>") -> dict:
    """Mechanically derive the contract's `how` half from bytes.

    **goal:g6.1** — the derivation takes *bytes*, not a path, so it can run
    against a payload read out of a node's grid ref exactly as it runs against
    a file on disk. That is the read direction the write direction already has:
    until this existed, the graph could write the engine but could only learn
    about it by reading the engine, so a payload edited only in the graph
    carried a stale contract until it was published and rescanned.

    One derivation, two sources. Re-implementing it per source is the drift
    `stitch.py` exists to catch in the nodes, so it is not allowed to happen
    between these two entry points either.

    Returns {"parse_ok", "parse_error", "inputs", "outputs", "uncovered"}.
    Anything that cannot be read or parsed gets `parse_ok: false` and an empty
    contract — never an invented one.
    """
    # `ast` is a *Python* parser, so gate on the suffix before using it. JSON
    # is a dict literal and TOML's `key = "value"` is an assignment, so both
    # parse clean and would report `parse_ok: true` with an empty contract —
    # a file claiming it was analysed when nothing analysed it, which
    # `stitch.py --verify` would then read as no drift. An honest
    # `not-python` is the correct answer for every non-`.py` payload until
    # G6.6's extracted-claims contract exists.
    if suffix != ".py":
        # Still record a content fingerprint. Without it a non-`.py` node's body
        # is byte-identical no matter what its payload says, so editing a doc
        # produces no node change and therefore no grid version — the payload's
        # history exists only in ordinary git and is invisible to
        # `refs/grid/node/*`. Measured 2026-08-25: editing README.md and
        # agent-prompt.md left both nodes at their prior version counts and
        # `commit --all` reported 0 new versions. The hash is not a contract and
        # is not claimed to be one; it is the minimum that makes a prose change
        # *visible* to node history until G6.6's extracted-claims contract lands.
        return {"parse_ok": False,
                "parse_error": f"not-python: {suffix or 'no suffix'} "
                               "(no mechanical contract derivation for this "
                               "file type yet — see goal:g6.6)",
                "content_sha256": hashlib.sha256(data).hexdigest(),
                "inputs": [], "outputs": [], "uncovered": []}
    try:
        source = data.decode("utf-8")
    except Exception as exc:
        return {"parse_ok": False, "parse_error": f"unreadable: {exc}",
                "inputs": [], "outputs": [], "uncovered": []}
    try:
        tree = ast.parse(source, filename=name)
    except SyntaxError as exc:
        return {"parse_ok": False, "parse_error": f"SyntaxError: {exc}",
                "inputs": [], "outputs": [], "uncovered": []}

    io_reads, io_writes, io_uncovered = _scan_io_calls(tree, source)

    inputs = _scan_imports(tree) + io_reads + _scan_cli_and_env(tree)
    outputs = _scan_top_level_defs(tree, source) + io_writes + _scan_stdout(tree)

    return {"parse_ok": True, "parse_error": None,
            "inputs": inputs, "outputs": outputs, "uncovered": io_uncovered}


# --- census parent matching (read, never guessed) -----------------------------


def load_census_units(existing: dict) -> list[dict]:
    """`idea:engine-*` census units whose scope overlaps `src/**/*.py` + `bin/*.py`.

    Read from already-loaded nodes (any `type: idea` node carrying
    `unit_kind`/`unit_path`, written by decompose-engine.py) — never
    re-derived from the file tree, per the "never guessed" rule in the
    anatomy node.
    """
    units = []
    for node_id, rec in existing.items():
        fm = rec["fm"]
        if fm.get("type") != "idea":
            continue
        kind = fm.get("unit_kind")
        # `entry_point` was silently dropped here. Five such units already
        # existed and were correct — driver.sh, find-root.sh,
        # cc-session-start.sh, agi-bridge/index.ts, migrate_to_sqlite.py —
        # so those files reported NO_PARENT while their census unit sat in
        # the graph unread. They are exactly the highest-leverage surfaces
        # goal:g6.6 names, and the filter that hid them was invisible
        # because a missing parent looks identical to a missing unit.
        if kind not in ("src_package", "bin_script", "entry_point"):
            continue
        unit_path = fm.get("unit_path")
        if not unit_path:
            continue
        units.append({"node_id": node_id, "unit_path": str(unit_path), "unit_kind": kind})
    return units


def find_parent(rel_path: str, units: list[dict]) -> str | None:
    """Longest-match census unit covering `rel_path`, or None (flag, don't guess)."""
    best_id = None
    best_len = -1
    for u in units:
        # `entry_point` needs the same exact-match semantics as `bin_script`:
        # it names one file, and the prefix branch below can never match a
        # single path. Admitting the kind above without this is a silent
        # no-op, which is the shape that hid it in the first place.
        if u["unit_kind"] in ("bin_script", "entry_point"):
            if rel_path == u["unit_path"] and len(u["unit_path"]) > best_len:
                best_id, best_len = u["node_id"], len(u["unit_path"])
        else:  # src_package
            prefix = u["unit_path"].rstrip("/") + "/"
            if rel_path.startswith(prefix) and len(prefix) > best_len:
                best_id, best_len = u["node_id"], len(prefix)
    return best_id


# --- id / slug minting ---------------------------------------------------


def read_mvp_map(path: Path | None) -> list[tuple[str, str]]:
    """Goal:s29 parent map, as declared DATA: rel-path-prefix -> mvp:<id>.

    A NEW build node needs `parents: [mvp:<id>]` (goal:s29) — an mvp states the
    minimum a subsequent build must satisfy, so a file with one is argued for
    rather than just written. `--mint-missing-only` attaches that parent by
    subsystem (one mvp per subsystem — bin/, tests/, workflows/, ... — because
    72 per-file mvps would be bookkeeping, not thought). The map lives in a
    data file, never an if-statement, one `prefix | mvp:<id>` line per
    subsystem. Longest-prefix wins so a specific subsystem overrides a general
    one. A missing file is an empty map — the mint then falls back to the census
    parent, then parentless; the parent is provenance, not a gate.
    """
    mapping: list[tuple[str, str]] = []
    if path is None or not Path(path).is_file():
        return mapping
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        prefix, mvp_id = (p.strip() for p in line.split("|", 1))
        if prefix and mvp_id.startswith("mvp:"):
            mapping.append((prefix, mvp_id))
    return mapping


def mvp_parent_for(rel_path: str, mapping: list[tuple[str, str]]) -> str | None:
    """Longest-matching `prefix | mvp:<id>` for `rel_path`, or None (flag, don't
    guess — same shape as find_parent)."""
    best_id, best_len = None, -1
    for prefix, mvp_id in mapping:
        if rel_path.startswith(prefix) and len(prefix) > best_len:
            best_id, best_len = mvp_id, len(prefix)
    return best_id


# --- mint-missing-only: the ADDITIVE pass (trap 0i) -------------------------


def mint_missing(files, existing, units, project_root, engine_root,
                 level3_dir, args, mvp_map) -> int:
    """`--mint-missing-only`: mint a build node + payload_ref ONLY for a tracked
    file that has none. This mode is the trap-0i escape: default level3.py is
    destructive (it prunes stale build-scan nodes), so the fix is a mode that
    CANNOT be destructive by construction rather than a promise to be careful.

    Additivity is structural, not a promise:
      - a file already declared by ANY payload_ref is skipped — that includes a
        deprecated build node that still claims the file, because a deprecated
        node whose file still exists is a DELIBERATE state and reviving it would
        destroy a decision (deprecate-never-delete);
      - a slug-id already owned by an existing node is skipped — a duplicate id
        under two paths is the one shape every id-keyed reader disagrees on;
      - minted nodes are written FRESH at the live build address only; a
        deprecated node is never moved, re-stamped, or un-deprecated;
      - there is no prune branch and no rewrite branch anywhere in this mode.
    """
    declared_refs: set[str] = set()
    for node in existing.values():
        ref = (node.get("fm") or {}).get("payload_ref")
        if ref:
            declared_refs.add(str(ref))

    # Scope is the CHECKER's boundary (grid_coverage_check.py): tracked CODE
    # files under extensions/skills/src/bin only — the universe the grid-cover
    # invariant enumerates and the 65-file backlog was measured in. Prose
    # (briefs, docs, manifests), the `.claude/workflows/*.js` SYMLINKS (trap
    # 0i — the real file each points at already has its own node) and any
    # stray extension-less file are deliberately OUT: none of them is a node
    # the invariant demands, so minting them would over-reach the parent's one
    # job. This guard keeps mint and checker agreeing by construction.
    candidates = [
        f for f in files
        if f.startswith(("extensions/", "skills/", "src/", "bin/"))
        and (f.endswith(".py") or f.endswith(".sh") or f.endswith(".js"))
    ]
    missing = sorted(f for f in candidates if f not in declared_refs)
    print(f"--mint-missing-only: {len(missing)} un-noded code file(s) of "
          f"{len(candidates)} tracked-code ({len(files)} boundary-admitted)")
    if not missing:
        print("nothing to mint — every tracked file already has a payload_ref")
        return 0

    minted: list[str] = []
    skipped_collision: list[str] = []
    for rel_path in missing:
        node_id = f"build:{slug_for(rel_path)}"
        if node_id in existing:
            skipped_collision.append(rel_path)
            print(f"SKIP (id collision — existing node owns {node_id}): {rel_path}",
                  file=sys.stderr)
            continue
        abs_path = engine_root / rel_path
        if not (abs_path.is_symlink() or abs_path.exists()):
            # Tracked means present; a graph-authored pre-publish file lands in
            # the payload checkout (goal:g6.1). Same fallback as the main pass.
            abs_path = project_root / grid.PAYLOAD_DIR / rel_path
        # goal:s29 — a NEW build node is parented by the mvp that specified its
        # subsystem; fall back to the census parent, then parentless; never guessed.
        parent_id = (mvp_parent_for(rel_path, mvp_map)
                     or find_parent(rel_path, units))
        _id, fm, body, analysis = build_node(rel_path, abs_path, parent_id,
                                             prior_body=None)
        slug_part = node_id.split(":", 1)[-1]
        out_path = level3_dir / f"{slug_part}.md"
        parent_note = f", parent {parent_id}" if parent_id else ", parentless"
        if args.dry_run:
            print(f"DRY-RUN: would mint {out_path} ({node_id}{parent_note})")
            continue
        write_frontmatter(out_path, fm, body, origin=ORIGIN,
                          preserve=None, preserve_body=None)
        print(f"MINTED: {node_id} ({rel_path}{parent_note})")
        minted.append(rel_path)

    verb = "would mint" if args.dry_run else "minted"
    print(f"level-3 nodes {verb} (mint-missing-only): {len(minted)}")
    print(f"  skipped (id collision): {len(skipped_collision)}")
    print("stale pruned (mint-missing-only): 0 — this mode is ADDITIVE ONLY")
    print(f"target dir: {level3_dir}")
    return 0


def slug_for(rel_path: str) -> str:
    trimmed = rel_path
    if trimmed.startswith("extensions/agi/"):
        trimmed = trimmed[len("extensions/agi/"):]
    if trimmed.endswith(".py"):
        trimmed = trimmed[:-3]
    parts = ["init" if p == "__init__" else p for p in trimmed.split("/")]
    slug = "-".join(parts).replace("_", "-")
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "root"


# --- node construction ---------------------------------------------------

_CONTRACT_BEGIN = ("<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model "
                    "may only fill why/perf/security, never add/remove/reorder "
                    "fields or entries -->")
_CONTRACT_END = "<!-- BUILD-CONTRACT:END -->"


_AUTHORED_FIELDS = ("why", "perf", "security")
_TODO = "TODO(model)"


def _prior_index(prior_contract: dict | None, section: str) -> dict[str, list[dict]]:
    """`name` -> the stored entries under `section`, in file order.

    Keyed on `name` and *not* on `how`, deliberately. `how` embeds the line
    number ("... at line 18"), so keying on it would drop a model's `why` the
    first time anything above that call site shifted by a line — the rationale
    for a call is not invalidated by the call moving. Duplicate names within a
    section are matched positionally, which is why the value is a list.
    """
    out: dict[str, list[dict]] = {}
    if not prior_contract:
        return out
    for e in prior_contract.get(section) or []:
        if isinstance(e, dict) and e.get("name") is not None:
            out.setdefault(str(e["name"]), []).append(e)
    return out


def _fill_entries(entries: list[dict], prior: dict[str, list[dict]] | None = None) -> list[dict]:
    """Derive `how` afresh; carry `why`/`perf`/`security` over (goal:g2.10).

    `how` is mechanical and must be re-derived every run — that is what makes
    it trustworthy and what `stale_contracts` polices. The other three are
    authored, and until 2026-08-27 this function overwrote them with
    `TODO(model)` on every scan. The corpus read exactly as that predicts:
    8,034 such fields across 190 build nodes, 8,034 still `TODO(model)`, zero
    ever filled — not neglect, but a permission the schema granted and the
    code revoked on the next run.

    Idempotent by construction: with nothing filled in, every lookup returns
    `TODO(model)` and the output is byte-identical to the old behaviour. That
    matters more than it sounds — a derivation that does not reproduce its own
    stored value leaves the graph permanently dirty and shuts the publish
    cron's first gate silently (goal:g6.5).
    """
    pending = {k: list(v) for k, v in (prior or {}).items()}
    filled = []
    for e in entries:
        stored = pending.get(str(e["name"]))
        carried = stored.pop(0) if stored else {}
        entry = {"name": e["name"], "how": e["how"]}
        for field in _AUTHORED_FIELDS:
            value = carried.get(field)
            entry[field] = _TODO if value in (None, "") else value
        filled.append(entry)
    return filled


def build_node(rel_path: str, abs_path: Path, parent_id: str | None,
               payload: bytes | None = None,
               prior_body: str | None = None) -> tuple[str, dict, str, dict]:
    """Returns (node_id, frontmatter, body, analysis) for one file.

    `payload`, when given, is the file's bytes read from somewhere other than
    `abs_path` — in practice the node's own grid ref under `--from-grid`
    (goal:g6.1). `abs_path` is still used for nothing but its suffix in that
    case, so a node whose payload exists only in the graph derives correctly
    even if the engine tree no longer has the file.
    """
    node_id = f"build:{slug_for(rel_path)}"
    analysis = (analyze_source(payload, Path(rel_path).suffix, rel_path)
                if payload is not None else analyze_file(abs_path))

    fm = {
        "id": node_id,
        "type": "build",
        "build_kind": build_kind_for(rel_path),
        "title": f"Build: {rel_path}",
        "payload_ref": rel_path,
        "tags": ["build", build_kind_for(rel_path), "g2.1"],
        "confidence": 1.0,
    }
    if parent_id:
        fm["parents"] = [parent_id]

    contract: dict = {"payload_ref": rel_path, "parse_ok": analysis["parse_ok"]}
    if not analysis["parse_ok"]:
        contract["parse_error"] = analysis["parse_error"]
    # Emitted only when `analyze_file` produced one (today: non-`.py` payloads).
    # Without it a prose node's body never changes when its payload does, so the
    # doc's history is invisible to `refs/grid/node/*` — see the comment in
    # `analyze_file` for the measurement that established this.
    if analysis.get("content_sha256"):
        contract["content_sha256"] = analysis["content_sha256"]
    # The node's own stored contract, so authored fields survive this rewrite.
    # A body that cannot be parsed is treated as "nothing to carry" rather than
    # as an error: this writer's job is to emit a correct contract, and
    # refusing to write one because the *previous* one was malformed would
    # strand the node in exactly the broken state it is trying to leave.
    prior_contract, _ = extract_contract(prior_body) if prior_body else (None, None)
    contract["inputs"] = _fill_entries(
        analysis["inputs"], _prior_index(prior_contract, "inputs"))
    contract["outputs"] = _fill_entries(
        analysis["outputs"], _prior_index(prior_contract, "outputs"))
    if analysis["uncovered"]:
        contract["uncovered"] = _fill_entries(
            analysis["uncovered"], _prior_index(prior_contract, "uncovered"))

    yaml_text = yaml.safe_dump(contract, sort_keys=False, default_flow_style=False,
                                allow_unicode=True).rstrip("\n")

    body_lines = [f"`{rel_path}` — level-3 code node (one file, one canonical node).", ""]
    if parent_id:
        body_lines.append(f"Census parent: `{parent_id}`.")
    else:
        body_lines.append(
            "Census parent: none — **flagged**. No `idea:engine-*` census unit's "
            "`unit_path` (see `decompose-engine.py`, `nodes/idea/engine-*.md`) "
            "covers this file. Left parentless rather than guessed."
        )
    body_lines += [
        "",
        _CONTRACT_BEGIN,
        "```yaml",
        yaml_text,
        "```",
        _CONTRACT_END,
        "",
        "Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph "
        "repo for the design). `how` fields above are derived mechanically via "
        "the standard library `ast` module; `why`/`perf`/`security` are "
        "placeholders for a later model pass — never fabricated by this "
        "generator.",
    ]
    return node_id, fm, "\n".join(body_lines), analysis


# --- main ----------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="One level-3 node per code file (with a contract block) -> nodes/level3/")
    ap.add_argument("--project", default=None,
                    help="override PROJECT_ROOT (graph repo; default: env or cwd)")
    ap.add_argument("--engine-root", default=None,
                    help="override the engine repo root (default: this script's own repo)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would happen; write nothing")
    ap.add_argument("--from-grid", action="store_true",
                    help="goal:g6.1 — derive each existing node's contract from "
                         "the payload in its own grid ref instead of from the "
                         "engine tree. Discovery still reads the engine tree "
                         "(a file with no node yet can only be found there); "
                         "derivation stops depending on it.")
    ap.add_argument("--mint-missing-only", action="store_true",
                    help="ADDITIVE ONLY (trap 0i). Mint a build node + payload_ref "
                         "ONLY for a tracked file that has none. By construction "
                         "incapable of destruction: never prunes, never resurrects "
                         "a deprecated node, never touches an existing node. The "
                         "default mode stays forbidden without --dry-run.")
    ap.add_argument("--mvp-map", default=None,
                    help="goal:s29 parent data for --mint-missing-only: a file "
                         "mapping a rel-path prefix to the mvp:<id> that specified "
                         "its subsystem. One '%s' per line, longest-prefix wins; a "
                         "minted node gets parents: [mvp:<id>] (else falls back to "
                         "the census parent, then parentless). Never an in-code if."
                         % 'prefix | mvp:<id>')
    args = ap.parse_args(argv)

    resolved: Path | None
    if args.project:
        resolved = resolve_project_root(args.project)
        if resolved is None:
            print(f"ERR: no graph root at or above "
                  f"{Path(args.project).resolve()}"
                  f" (no .agi/ and no nodes/)", file=sys.stderr)
            return 2
        _set_project_root(resolved)
    else:
        # No `--project`: resolve through the SAME resolver as the flag, and
        # refuse by name when it finds no graph — never scan the raw cwd's
        # `<cwd>/nodes` tree as authoritative (goal:g15).
        resolved = default_project_root()
        if resolved is None:
            print(f"ERR: no graph root at or above "
                  f"{Path.cwd().resolve()}"
                  f" (no .agi/ and no nodes/)", file=sys.stderr)
            return 2
        _set_project_root(resolved)
    project_root = PROJECT_ROOT
    engine_root = Path(args.engine_root).resolve() if args.engine_root else DEFAULT_ENGINE_ROOT

    payload_root = project_root / grid.PAYLOAD_DIR
    files = discover_files(engine_root, payload_root)
    if files is None:
        # A missing/unreadable engine tree is a no-op: nothing written, nothing pruned.
        print(f"WARN: engine root {engine_root} is missing or unreadable "
              f"(not a git repo?) — no-op, nothing written or pruned",
              file=sys.stderr)
        return 0

    if not files:
        # H0/H0i guard. An empty scope is never "prune everything". Before
        # G6.8 this case could not arise — the two-prefix scan had no external
        # classification step that could return "everything excluded" short of
        # git itself failing, which already returns None above. Now it can, so
        # a zero-length result means the predicate resolved against the wrong
        # tree rather than a genuine empty scope. Fail loud and return before
        # `written_paths`/`stale_generated` are touched at all; a silent exit-0
        # here is precisely the shape that cost this project 29k nodes twice.
        print(f"ERROR: discover_files returned zero files for engine root "
              f"{engine_root} — refusing to treat this as authoritative "
              f"scope; no-op, nothing written or pruned", file=sys.stderr)
        return 1

    snapshot_goals._set_project_root(project_root)
    existing = snapshot_goals.load_existing_nodes()
    units = load_census_units(existing)

    level3_dir = project_root / "nodes" / "build"

    if args.mint_missing_only:
        # trap 0i — the ADDITIVE mode, chosen deliberately; the destructive path
        # below is never reached in this mode, so there is no primal branch to
        # accidentally trip. `--from-grid` is ignored: a file with no node has no
        # grid ref to derive from, so discovery is the only possible source.
        mvp_map = read_mvp_map(
            Path(args.mvp_map).resolve() if args.mvp_map else None)
        return mint_missing(files, existing, units, project_root, engine_root,
                            level3_dir, args, mvp_map)

    written_paths: set[Path] = set()
    used_ids: dict[str, str] = {}
    n_with_parent = 0
    n_no_parent = 0
    n_derivable = 0
    n_uncovered = 0
    n_parse_fail = 0

    n_from_grid = 0
    n_from_engine = 0

    for rel_path in files:
        abs_path = engine_root / rel_path
        if not (abs_path.is_symlink() or abs_path.exists()):
            # A file authored in the graph and not yet published has no engine
            # copy. The payload checkout is its only source; that is not a
            # policy choice about which source wins, it is the only one there is.
            abs_path = payload_root / rel_path
        parent_id = find_parent(rel_path, units)
        payload = None
        if args.from_grid:
            probe_id = f"build:{slug_for(rel_path)}"
            node_path = existing.get(probe_id, {}).get("path")
            payload = grid_payload_for(project_root, node_path) if node_path else None
            if payload is None:
                n_from_engine += 1
            else:
                n_from_grid += 1
        prior_body = existing.get(f"build:{slug_for(rel_path)}", {}).get("body")
        node_id, fm, body, analysis = build_node(
            rel_path, abs_path, parent_id, payload, prior_body=prior_body)

        if node_id in used_ids:
            disambiguated = f"{node_id}-{len(used_ids)}"
            print(f"WARN: slug collision for {rel_path} vs {used_ids[node_id]}; "
                  f"disambiguated id to {disambiguated}", file=sys.stderr)
            node_id = disambiguated
            fm["id"] = node_id
        used_ids[node_id] = rel_path

        if parent_id:
            n_with_parent += 1
        else:
            n_no_parent += 1
            print(f"NO_PARENT: {rel_path} — no matching engine census unit "
                  f"(emitted parentless)")

        n_derivable += len(analysis["inputs"]) + len(analysis["outputs"])
        n_uncovered += len(analysis["uncovered"])
        if not analysis["parse_ok"]:
            n_parse_fail += 1

        slug_part = node_id.split(":", 1)[-1]
        # Rewrite a node where it actually lives, not where a fresh mint would
        # put it. `load_existing_nodes()` rglobs, so it finds a node that has
        # been regrouped — e.g. retired into `nodes/deprecated/build/`. Without
        # this, a scan would write a *second* file at the default address and
        # the graph would carry one id in two places, which is the duplicate
        # every id-keyed reader resolves differently.
        existing_path = existing.get(node_id, {}).get("path")
        out_path = (Path(existing_path) if existing_path
                    else level3_dir / f"{slug_part}.md")
        written_paths.add(out_path.resolve())

        if args.dry_run:
            verb = "would update" if existing_path else "would create"
            print(f"DRY-RUN: {verb} {out_path} ({node_id})")
            continue

        write_frontmatter(
            out_path, fm, body, origin=ORIGIN,
            preserve=existing.get(node_id, {}).get("fm"),
            # The body half of the same contract (goal:g2.10). Frontmatter has
            # been carried forward since `next_edges` was being severed; the
            # body was not, so a build node could be *cited* by a thought but
            # never *contain* one — which is half of goal:g6.8's argument for
            # admitting build nodes at all, and it was false.
            preserve_body=existing.get(node_id, {}).get("body"),
        )

    # Prune only nodes stamped with our own origin that we did not write this
    # run. Never touches unstamped or other-origin nodes (build-site,
    # goals-doc, engine-decomp, ...).
    stale_generated = []
    kept_by_grid = 0
    for node_id, node in existing.items():
        if node["origin"] != ORIGIN or node["path"].resolve() in written_paths:
            continue
        # H0-class guard, added with payload-only discovery (goal:g6.1). A node
        # whose payload is in its own grid ref is backed by the graph, so
        # "discovery did not find it this run" is a statement about the two
        # source trees, not about whether the node is real. Deleting it would
        # be the H0i shape with a new door: run `level3.py` on a machine where
        # `payloads/` was never checked out and every graph-authored file's
        # node disappears. The grid is what makes that recoverable, so the grid
        # is what gets asked.
        if grid_payload_for(project_root, node["path"]) is not None:
            kept_by_grid += 1
            print(f"KEEP: {node_id} was not discovered this run but its payload "
                  f"is in the grid — not pruning (goal:g6.1)", file=sys.stderr)
            continue
        stale_generated.append(node["path"])
    for path in sorted(stale_generated):
        if args.dry_run:
            print(f"DRY-RUN: would prune stale {path}")
        else:
            path.unlink(missing_ok=True)
            print(f"removed stale: {path}")

    print(f"engine root: {engine_root}")
    print(f"files scanned: {len(files)}")
    verb = "would write" if args.dry_run else "wrote"
    print(f"level-3 nodes {verb}: {len(files)}")
    print(f"  with census parent: {n_with_parent}")
    print(f"  flagged NO_PARENT (parentless): {n_no_parent}")
    if args.from_grid:
        print(f"payload source: {n_from_grid} from the grid, {n_from_engine} "
              "from the engine tree (no node or no payload in its ref yet)")
    print(f"contract entries: {n_derivable} derivable, {n_uncovered} uncovered, "
          f"{n_parse_fail} file(s) failed to parse")
    prune_verb = "would prune" if args.dry_run else "pruned"
    print(f"stale {ORIGIN} nodes {prune_verb}: {len(stale_generated)}")
    print(f"target dir: {level3_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
