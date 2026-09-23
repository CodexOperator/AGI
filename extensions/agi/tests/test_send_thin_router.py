"""goal:g7.32.4 -- census of send.py's coupling to rotate/dispatch.

Measures, from the source BYTES via AST (never by grepping prose):

  (1) every `import rotate` / `import dispatch` site, module-level or lazy;
  (2) every `rotate.<symbol>` / `dispatch.<symbol>` attribute the file
      actually references (comments and docstrings are not references);
  (3) each referenced symbol classified against the explicit ORCHESTRATION
      set below -- spawn / rotation / push / pending-swap / formation -- with
      everything else named UTILITY;
  (4) Falsifier 2's substrate: is transport choice a table, or inline
      harness branching? Reported statically.

The assertions now pin the TARGET INVARIANT: send.py references ZERO
orchestration symbols (goal:g7.32.4 Falsifier 1). The three orchestration
acts send.py still needs from rotate (spawn-row commit, season-branch push,
deferred pending-swap completion) go through the ONE seam module
`extensions/agi/bin/seat_registry_commit.py`, so the `rotate.X` attribute
set is UTILITY-only. A later edit that reintroduces direct orchestration
coupling turns this file red on purpose.
"""
from __future__ import annotations

import ast
from pathlib import Path

SEND_PY = Path(__file__).resolve().parents[1] / "bin" / "send.py"

#: The census's explicit, named classification. Any rotate/dispatch symbol
#: that is an orchestration act -- minting a spawn row, rotating/pushing a
#: season branch, completing a deferred pending swap, formation edits -- goes
#: here. Everything else (constants, generic git/settings helpers, registry
#: reads) is UTILITY and must be named in UTILITY_SYMBOLS.
ORCHESTRATION_SYMBOLS = {
    "_commit_spawn_row",             # spawn row mint (rotate orchestration)
    "_push_season_branch",           # season-branch push
    "_finish_pending_swap_on_push",  # deferred pending-key swap completion
}

#: Referenced rotate/dispatch symbols that are NOT orchestration acts.
UTILITY_SYMBOLS = {
    "DEFAULT_TMUX_SESSION",   # constant
    "_git_toplevel",          # generic git helper
    "_normalize_settings",    # settings normaliser (registry read shape)
}

#: The exact import sites measured on the current bytes (line, statement).
#: The three rotate imports that used to sit beside `rotate._commit_spawn_row`
#: and `rotate._finish_pending_swap_on_push` are GONE -- those acts now go
#: through the seat_registry_commit seam, which needs no `import rotate` here.
EXPECTED_IMPORT_SITES = {
    (727, "import rotate"),
    (845, "import rotate"),
    (1582, "import rotate"),
    (1610, "import rotate"),
    (2190, "import rotate"),
}

#: The exact referenced-symbol set measured on the current bytes:
#: UTILITY only -- the target invariant (Falsifier 1) is that no orchestration
#: symbol is referenced.
EXPECTED_REFERENCED = set(UTILITY_SYMBOLS)

#: Caller-facing bodies Falsifier 2 asks about.
CALLER_BODIES = {"send", "send_dm", "send_room", "_nudge_target", "_nudge_window"}


def _module():
    return ast.parse(SEND_PY.read_text(encoding="utf-8"))


def _import_sites(tree) -> set[tuple[int, str]]:
    """Every import of `rotate`/`dispatch`, module-level or lazy."""
    sites: set[tuple[int, str]] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in ("rotate", "dispatch"):
                    sites.add((node.lineno, f"import {alias.name}"))
        elif isinstance(node, ast.ImportFrom):
            mod = (node.module or "").split(".")[0]
            if mod in ("rotate", "dispatch"):
                names = ",".join(a.name for a in node.names)
                sites.add((node.lineno, f"from {node.module} import {names}"))
    return sites


def _referenced_attrs(tree) -> dict[str, set[str]]:
    """Every `rotate.X` / `dispatch.X` attribute ACTUALLY referenced.

    Comments and docstrings are not AST nodes, so this cannot be fooled by
    prose that merely names a symbol.
    """
    out: dict[str, set[str]] = {"rotate": set(), "dispatch": set()}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in out):
            out[node.value.id].add(node.attr)
    return out


def test_import_sites_are_the_measured_five_rotate_sites():
    tree = _module()
    sites = _import_sites(tree)
    print("send.py rotate/dispatch import sites:")
    for lineno, stmt in sorted(sites):
        print(f"  L{lineno}: {stmt}")
    assert sites == EXPECTED_IMPORT_SITES, (
        "send.py import sites changed; re-census before trusting thinness")
    assert not {s for s in sites if s[1].startswith("import dispatch")}, (
        "unexpected `import dispatch` in send.py")


def test_referenced_symbols_are_characterized():
    refs = _referenced_attrs(_module())
    print("send.py referenced rotate symbols:", sorted(refs["rotate"]))
    print("send.py referenced dispatch symbols:", sorted(refs["dispatch"]))
    assert refs["dispatch"] == set(), "send.py references dispatch symbols"
    assert refs["rotate"] == EXPECTED_REFERENCED, (
        "referenced rotate symbol set changed; re-classify each new symbol")


def test_orchestration_symbol_set_is_empty():
    """TARGET INVARIANT (goal:g7.32.4 Falsifier 1): no orchestration symbol.

    send.py reaches rotate's spawn/push/pending-swap internals only through
    the seat_registry_commit seam, never as `rotate.<orchestration>`.
    """
    refs = _referenced_attrs(_module())
    offenders = refs["rotate"] & ORCHESTRATION_SYMBOLS
    print("orchestration symbols referenced by send.py:", sorted(offenders))
    assert offenders == set(), (
        "send.py reaches rotate orchestration directly again -- route it "
        "through seat_registry_commit (goal:g7.32.4)")
    # every referenced symbol is classified, nothing falls through
    assert refs["rotate"] <= (ORCHESTRATION_SYMBOLS | UTILITY_SYMBOLS)
    assert not (ORCHESTRATION_SYMBOLS & UTILITY_SYMBOLS)


def test_transport_is_not_a_table_and_no_inline_harness_branching_in_callers():
    """Falsifier 2 substrate: table vs inline harness `if`.

    Measured: send.py defines NO module-level TRANSPORTS/dispatch table, and
    the caller-facing bodies carry no `"grok"` literal and no `harness ==`
    comparison. Transport choice is therefore not (yet) table-driven.
    """
    tree = _module()
    table_names = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (isinstance(target, ast.Name)
                        and ("TRANSPORT" in target.id.upper()
                             or "DISPATCH" in target.id.upper())):
                    table_names.append(target.id)
    print("module-level transport tables:", table_names)

    offenders: list[tuple[str, int, str]] = []
    for node in ast.walk(tree):
        if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in CALLER_BODIES):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and sub.value == "grok":
                    offenders.append((node.name, sub.lineno, "grok literal"))
                if isinstance(sub, ast.Compare):
                    for side in [sub.left, *sub.comparators]:
                        if (isinstance(side, ast.Name)
                                and "harness" in side.id.lower()):
                            offenders.append(
                                (node.name, sub.lineno, "harness comparison"))
    print("caller-body harness literals/comparisons:", offenders)

    assert table_names == [], "send.py grew a transport table -- update node"
    assert offenders == [], (
        "inline harness branching appeared in a caller-facing body")
