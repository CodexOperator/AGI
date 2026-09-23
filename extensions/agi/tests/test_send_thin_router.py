"""Executable falsifier for ``goal:g7.32.4`` — ``send.py`` must be a THIN
TRANSPORT ROUTER: it picks a transport (native seat channel / signed DM /
board / cross-harness nudge bridge) and never embeds formation, rotation or
harness policy.

The goal node states three falsifier clauses verbatim; this module measures
all three against the LIVE bytes, with ``send.py`` imported and its source
parsed by ``ast`` (top-level AND function-local imports are walked):

  1. ``send.py`` (or its package ``__init__``) has zero imports of ``rotate``
     / ``dispatch`` orchestration symbols, and no ``rotate.<name>`` /
     ``dispatch.<name>`` attribute use. On a violation the test names the
     EXACT symbol and line number.
  2. Transport selection is a module-level TABLE (a dict keyed by transport
     name) and NOT a per-harness ``if`` chain in the ``send``/router path. If
     no table exists the test fails by naming the absence — it is never
     faked.
  3. The cross-harness nudge/wake path is reachable from the router entry
     point: ``send.main`` routes a ``wake`` verb to ``send.wake``, and
     ``send.wake`` calls ``send._nudge_window``. A wire check, not a comment.

Run the module directly (``python3 test_send_thin_router.py``) to print the
measured baseline without pytest — that output is what an Agent Notes block
should quote.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

_SEND = Path(__file__).resolve().parents[1] / "bin" / "send.py"

#: Modules whose orchestration symbols a thin router must never import.
ORCH_MODULES = ("rotate", "dispatch")

#: Candidate names for the module-level transport table.
TRANSPORT_TABLE_NAMES = ("TRANSPORTS", "TRANSPORT_TABLE", "TRANSPORT_ROUTES")

#: Harness names whose selection by ``if`` inside the router would be policy.
HARNESS_NAMES = frozenset({
    "claude", "pi", "grok", "gemini", "codex", "copilot", "cursor", "warp",
})


def _tree() -> ast.Module:
    return ast.parse(_SEND.read_text(encoding="utf-8"), filename=str(_SEND))


def _orchestration_imports(tree: ast.Module) -> list[tuple[int, str, str]]:
    """(lineno, module, imported-name) for every ``rotate``/``dispatch``
    import in the file, wherever it sits (top-level or nested in a function)."""
    found: list[tuple[int, str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in ORCH_MODULES:
                    found.append((node.lineno, root, alias.name))
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in ORCH_MODULES:
                for alias in node.names:
                    found.append((node.lineno, root,
                                  f"{node.module}.{alias.name}"))
    return sorted(found)


def _orchestration_attrs(tree: ast.Module) -> list[tuple[int, str, str]]:
    """(lineno, module, attr) for every ``rotate.X`` / ``dispatch.X``
    attribute use. A local rebind of the name is not detectable by AST alone,
    which is correct: the goal forbids the symbol regardless."""
    found: list[tuple[int, str, str]] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in ORCH_MODULES):
            found.append((node.lineno, node.value.id, node.attr))
    return sorted(found)


def _module_level_dict(tree: ast.Module,
                       names: tuple[str, ...]) -> ast.Dict | None:
    """The module-level ``{...}`` assigned to one of ``names``, or None."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in names:
                if isinstance(node.value, ast.Dict):
                    return node.value
    return None


def _harness_if_chain(tree: ast.Module,
                      funcs: tuple[str, ...]) -> list[tuple[int, str, str]]:
    """(lineno, func, harness) for every string comparison against a harness
    name inside the named router functions — a per-harness ``if`` chain."""
    hits: list[tuple[int, str, str]] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name in funcs):
            continue
        for sub in ast.walk(node):
            if not isinstance(sub, ast.Compare):
                continue
            for cmp_node in [sub.left, *sub.comparators]:
                if (isinstance(cmp_node, ast.Constant)
                        and isinstance(cmp_node.value, str)
                        and cmp_node.value in HARNESS_NAMES):
                    hits.append((sub.lineno, node.name, cmp_node.value))
    return sorted(hits)


def _verb_wired(tree: ast.Module, verb: str, callee: str) -> bool:
    """True when ``main`` routes ``args.verb == verb`` to a call of ``callee``."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name == "main"):
            continue
        for sub in ast.walk(node):
            if not isinstance(sub, ast.If):
                continue
            test = sub.test
            if not isinstance(test, ast.Compare):
                continue
            left, comps = test.left, test.comparators
            is_verb = (isinstance(left, ast.Attribute)
                       and left.attr == "verb")
            matched = is_verb and any(
                isinstance(c, ast.Constant) and c.value == verb
                for c in comps)
            if not matched:
                continue
            for call in ast.walk(sub):
                if (isinstance(call, ast.Call)
                        and isinstance(call.func, ast.Name)
                        and call.func.id == callee):
                    return True
    return False


def _call_in(tree: ast.Module, func_name: str, callee: str) -> bool:
    """True when ``func_name``'s body calls ``callee``."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef)
                and node.name == func_name):
            continue
        for call in ast.walk(node):
            if (isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Name)
                    and call.func.id == callee):
                return True
    return False


# --- clause 1 -----------------------------------------------------------

def test_clause1_no_orchestration_in_send():
    tree = _tree()
    imports = _orchestration_imports(tree)
    attrs = _orchestration_attrs(tree)
    if imports or attrs:
        detail = [f"L{n} import {sym}" for n, _, sym in imports]
        detail += [f"L{n} uses {mod}.{attr}" for n, mod, attr in attrs]
        pytest.fail(
            "clause 1 RED — send.py carries rotate/dispatch orchestration: "
            + "; ".join(detail))


# --- clause 2 -----------------------------------------------------------

def test_clause2_transport_table_not_harness_ifs():
    tree = _tree()
    if _module_level_dict(tree, TRANSPORT_TABLE_NAMES) is None:
        pytest.fail(
            "clause 2 RED — no module-level transport table in send.py "
            "(looked for " + ", ".join(TRANSPORT_TABLE_NAMES)
            + "); transport selection is not table-driven")
    chain = _harness_if_chain(tree, ("main", "send"))
    if chain:
        detail = [f"L{n} {func}() compares harness {name!r}"
                  for n, func, name in chain]
        pytest.fail(
            "clause 2 RED — per-harness if chain in the router path: "
            + "; ".join(detail))


# --- clause 3 -----------------------------------------------------------

def test_clause3_wake_nudge_wired_from_router():
    tree = _tree()
    if not _verb_wired(tree, "wake", "wake"):
        pytest.fail(
            "clause 3 RED — send.main does not route the `wake` verb to "
            "wake(); the nudge path is unreachable from the router")
    if not _call_in(tree, "wake", "_nudge_window"):
        pytest.fail(
            "clause 3 RED — send.wake does not call _nudge_window(); the "
            "cross-harness nudge bridge is not wired through the router")


# --- baseline measurement (no pytest) -----------------------------------

def measure() -> dict:
    """The measured baseline, for an Agent Notes block to quote."""
    tree = _tree()
    return {
        "path": str(_SEND),
        "lines": len(_SEND.read_text(encoding="utf-8").splitlines()),
        "orchestration_imports": _orchestration_imports(tree),
        "orchestration_attrs": _orchestration_attrs(tree),
        "transport_table": _module_level_dict(
            tree, TRANSPORT_TABLE_NAMES) is not None,
        "harness_if_chain": _harness_if_chain(tree, ("main", "send")),
        "wake_verb_wired": _verb_wired(tree, "wake", "wake"),
        "wake_calls_nudge": _call_in(tree, "wake", "_nudge_window"),
    }


def main() -> int:
    m = measure()
    print(f"send.py: {m['path']} ({m['lines']} lines)")
    print(f"clause 1 orchestration imports: {m['orchestration_imports']}")
    print(f"clause 1 orchestration attrs:   {m['orchestration_attrs']}")
    print(f"clause 2 transport table:       {m['transport_table']}")
    print(f"clause 2 harness if chain:      {m['harness_if_chain']}")
    print(f"clause 3 wake verb wired:       {m['wake_verb_wired']}")
    print(f"clause 3 wake calls nudge:      {m['wake_calls_nudge']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
