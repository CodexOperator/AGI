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

import yaml

ORIGIN = "level3-scan"

BIN_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN_DIR.parent  # .../extensions/agi
# This script lives at <engine repo root>/extensions/agi/bin/level3.py.
# BIN_DIR is .../extensions/agi/bin, so three levels up (agi -> extensions ->
# repo root) is the engine repo we scan. Overridable with --engine-root,
# chiefly for tests. (Same convention as decompose-engine.py; that script's
# own history records this exact off-by-one as a caught bug — pinned by a
# dedicated test here too.)
DEFAULT_ENGINE_ROOT = BIN_DIR.parents[2]

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
# Loaded by file path (not `import`) because the filename has a hyphen and is
# not a valid module name. This is the actual function, not a copy — see
# module docstring point 1 (field erasure). Same pattern decompose-engine.py
# uses for the identical reason.
_SNAPSHOT_GOALS_PATH = BIN_DIR / "snapshot-goals.py"
_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter


# --- reuse payload_boundary.py's classify() (the G6.8 boundary predicate) ---
# Loaded by file path for the same reason snapshot-goals.py is above: one
# definition, never re-implemented. See `goal:g6.8` /
# `mvp:payload-boundary-predicate` for the rule.
_PAYLOAD_BOUNDARY_PATH = BIN_DIR / "payload_boundary.py"
_pb_spec = importlib.util.spec_from_file_location(
    "payload_boundary", _PAYLOAD_BOUNDARY_PATH)
payload_boundary = importlib.util.module_from_spec(_pb_spec)
_pb_spec.loader.exec_module(payload_boundary)


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


def discover_files(engine_root: Path) -> list[str] | None:
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
    return sorted(f for f, verdict, _reason in rows if verdict == "in")


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

    `ast.unparse` faithfully reproduces the full source of a call — including
    a multi-line string literal argument (e.g. a template being written to
    disk), verbatim, with embedded newlines escaped to `\\n`. Left uncapped,
    one such call can dominate the whole contract block with hundreds of
    characters of literal content. Truncating says so explicitly rather than
    silently clipping, so `how` stays honest about being partial.
    """
    if s is None or len(s) <= limit:
        return s
    return s[:limit] + f"...[truncated, {len(s)} chars total]"


def _unparse_safe(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


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


def _scan_top_level_defs(tree: ast.Module) -> list[dict]:
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
                sig = _cap(_unparse_safe(node.args)) or ""
            how = f"defines {vis} {kind} `{node.name}` at line {node.lineno}"
            if sig:
                how += f", signature: ({sig})"
            outputs.append({"name": node.name, "how": how})
    return outputs


def _scan_io_calls(tree: ast.Module) -> tuple[list[dict], list[dict], list[dict]]:
    """Detected filesystem-shaped read/write call sites.

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
            call_src = _cap(_unparse_safe(node)) or f"open(...) at line {node.lineno}"
            if mode_node is None:
                mode = "r"  # open()'s documented default — not a guess
            elif isinstance(mode_node, ast.Constant) and isinstance(mode_node.value, str):
                mode = mode_node.value
            else:
                uncovered.append({
                    "name": (_cap(_unparse_safe(node.args[0]), 80) if node.args
                             else f"open() at line {node.lineno}"),
                    "how": (f"uncovered — `{call_src}` at line {node.lineno}: mode is a "
                            f"non-literal expression, read/write direction cannot be "
                            f"statically resolved"),
                })
                continue
            target = _cap(_unparse_safe(node.args[0]), 80) if node.args else None
            entry_name = target or f"open() call at line {node.lineno}"
            entry = {"name": entry_name,
                      "how": f"`{call_src}` at line {node.lineno} (mode={mode!r})"}
            (writes if any(c in mode for c in "wax") else reads).append(entry)
            continue

        if isinstance(func, ast.Attribute) and func.attr in (_READ_ATTR_METHODS | _WRITE_ATTR_METHODS):
            target = _cap(_unparse_safe(func.value), 80)
            call_src = _cap(_unparse_safe(node)) or f"{func.attr}(...) at line {node.lineno}"
            entry_name = target or f"{func.attr}() call at line {node.lineno}"
            entry = {"name": entry_name, "how": f"`{call_src}` at line {node.lineno}"}
            (reads if func.attr in _READ_ATTR_METHODS else writes).append(entry)
            continue

        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            key = (func.value.id, func.attr)
            call_src = _cap(_unparse_safe(node)) or f"{func.value.id}.{func.attr}(...) at line {node.lineno}"
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
    """Mechanically derive the contract's `how` half from a Python file via `ast`.

    Returns {"parse_ok", "parse_error", "inputs", "outputs", "uncovered"}.
    A file that cannot be read or parsed gets `parse_ok: false` and an empty
    contract — never an invented one.
    """
    # `ast` is a *Python* parser, so gate on the suffix before using it. JSON
    # is a dict literal and TOML's `key = "value"` is an assignment, so both
    # parse clean and would report `parse_ok: true` with an empty contract —
    # a file claiming it was analysed when nothing analysed it, which
    # `stitch.py --verify` would then read as no drift. An honest
    # `not-python` is the correct answer for every non-`.py` payload until
    # G6.6's extracted-claims contract exists.
    if abs_path.suffix != ".py":
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
                "parse_error": f"not-python: {abs_path.suffix or 'no suffix'} "
                               "(no mechanical contract derivation for this "
                               "file type yet — see goal:g6.6)",
                "content_sha256": _content_sha256(abs_path),
                "inputs": [], "outputs": [], "uncovered": []}
    try:
        source = abs_path.read_text(encoding="utf-8")
    except Exception as exc:
        return {"parse_ok": False, "parse_error": f"unreadable: {exc}",
                "inputs": [], "outputs": [], "uncovered": []}
    try:
        tree = ast.parse(source, filename=str(abs_path))
    except SyntaxError as exc:
        return {"parse_ok": False, "parse_error": f"SyntaxError: {exc}",
                "inputs": [], "outputs": [], "uncovered": []}

    io_reads, io_writes, io_uncovered = _scan_io_calls(tree)

    inputs = _scan_imports(tree) + io_reads + _scan_cli_and_env(tree)
    outputs = _scan_top_level_defs(tree) + io_writes + _scan_stdout(tree)

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

_CONTRACT_BEGIN = ("<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model "
                    "may only fill why/perf/security, never add/remove/reorder "
                    "fields or entries -->")
_CONTRACT_END = "<!-- LEVEL3-CONTRACT:END -->"


def _fill_entries(entries: list[dict]) -> list[dict]:
    return [
        {"name": e["name"], "how": e["how"],
         "why": "TODO(model)", "perf": "TODO(model)", "security": "TODO(model)"}
        for e in entries
    ]


def build_node(rel_path: str, abs_path: Path, parent_id: str | None) -> tuple[str, dict, str, dict]:
    """Returns (node_id, frontmatter, body, analysis) for one file."""
    node_id = f"level3:{slug_for(rel_path)}"
    analysis = analyze_file(abs_path)

    fm = {
        "id": node_id,
        "type": "level3",
        "title": f"Level-3: {rel_path}",
        "payload_ref": rel_path,
        "tags": ["level3", "g2.1"],
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
    contract["inputs"] = _fill_entries(analysis["inputs"])
    contract["outputs"] = _fill_entries(analysis["outputs"])
    if analysis["uncovered"]:
        contract["uncovered"] = _fill_entries(analysis["uncovered"])

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
    args = ap.parse_args(argv)

    if args.project:
        _set_project_root(Path(args.project))
    project_root = PROJECT_ROOT
    engine_root = Path(args.engine_root).resolve() if args.engine_root else DEFAULT_ENGINE_ROOT

    files = discover_files(engine_root)
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

    level3_dir = project_root / "nodes" / "level3"

    written_paths: set[Path] = set()
    used_ids: dict[str, str] = {}
    n_with_parent = 0
    n_no_parent = 0
    n_derivable = 0
    n_uncovered = 0
    n_parse_fail = 0

    for rel_path in files:
        abs_path = engine_root / rel_path
        parent_id = find_parent(rel_path, units)
        node_id, fm, body, analysis = build_node(rel_path, abs_path, parent_id)

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
        out_path = level3_dir / f"{slug_part}.md"
        written_paths.add(out_path.resolve())

        if args.dry_run:
            verb = "would create" if slug_part not in {
                p.stem for p in level3_dir.glob("*.md")
            } else "would update"
            print(f"DRY-RUN: {verb} {out_path} ({node_id})")
            continue

        write_frontmatter(
            out_path, fm, body, origin=ORIGIN,
            preserve=existing.get(node_id, {}).get("fm"),
        )

    # Prune only nodes stamped with our own origin that we did not write this
    # run. Never touches unstamped or other-origin nodes (build-site,
    # goals-doc, engine-decomp, ...).
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

    print(f"engine root: {engine_root}")
    print(f"files scanned: {len(files)}")
    verb = "would write" if args.dry_run else "wrote"
    print(f"level-3 nodes {verb}: {len(files)}")
    print(f"  with census parent: {n_with_parent}")
    print(f"  flagged NO_PARENT (parentless): {n_no_parent}")
    print(f"contract entries: {n_derivable} derivable, {n_uncovered} uncovered, "
          f"{n_parse_fail} file(s) failed to parse")
    prune_verb = "would prune" if args.dry_run else "pruned"
    print(f"stale level3-scan nodes {prune_verb}: {len(stale_generated)}")
    print(f"target dir: {level3_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
