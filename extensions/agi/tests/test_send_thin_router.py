"""Falsifier for goal:g7.32.4 — send's transport choice is a table, not policy.

Three clauses: (thin) send_router imports no orchestration; (extensible) a new
transport is a register() row with no edit to the module; (wire) the live
`send` verb call site actually reaches the router.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import send_router  # noqa: E402

spec = importlib.util.spec_from_file_location("send_thin", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)

ROUTER = BIN / "send_router.py"
BANNED = {"rotate", "dispatch", "send", "seatsig"}


def test_thin_router_imports_only_stdlib():
    """Clause (1): no rotate / dispatch / send / seatsig import anywhere."""
    tree = ast.parse(ROUTER.read_text())
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names
                      if a.name.split(".")[0] in BANNED]
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".")[0] in BANNED:
                found.append(node.module)
    assert found == [], f"transport router imports orchestration: {found}"


def test_new_transport_is_a_table_row():
    """Clause (2): a fresh transport is a register() row, not a new branch."""
    stub = object()
    send_router.register("stub-harness", stub, lambda a: True, verb="nudge",
                         replace=True)
    assert send_router.choose("nudge", object()).transport is stub


def test_send_verb_call_site_reaches_the_router(tmp_path, monkeypatch):
    """Clause (wire): main()'s send verb consults send_router.choose live."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / "sessions").mkdir(parents=True)
    monkeypatch.chdir(root)

    seen = []
    original = send_router.choose

    def recorder(verb, args):
        seen.append((verb, getattr(args, "room", None)))
        return original(verb, args)

    monkeypatch.setattr(send_router, "choose", recorder)
    monkeypatch.setattr(send_mod, "_kid_room_refusal", lambda *a, **k: None)
    monkeypatch.setattr(send_mod, "send_room", lambda *a, **k: Path("stub"))
    monkeypatch.setattr(send_mod.last_act, "touch_env", lambda *a, **k: None)

    rc = send_mod.main(["--from", "alive", "send", "--room", "r", "hello"])
    assert rc == 0
    assert seen == [("send", "r")], "the live call site never consulted the router"
