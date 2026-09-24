"""Boundary probes for send.py's transport-router contract."""
from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
SEND = BIN / "send.py"
spec = importlib.util.spec_from_file_location("send_router_boundary", SEND)
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


def test_send_has_no_rotate_or_dispatch_orchestration_imports():
    """Comments and prose may mention siblings; executable imports may not."""
    tree = ast.parse(SEND.read_text(), filename=str(SEND))
    forbidden = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            forbidden.add(node.module.split(".")[0])
    assert forbidden.isdisjoint({"rotate", "dispatch"}), (
        "send.py imports orchestration; transport plugins must own these seams"
    )


def test_send_selects_nudge_transport_after_writing_inbox(tmp_path, monkeypatch,
                                                          capsys):
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"})
    )
    routed = []
    monkeypatch.setattr(send_mod, "_row_is_quiet", lambda _root, _to: False)
    monkeypatch.setattr(
        send_mod, "_nudge_window",
        lambda r, to, **kwargs: routed.append((r, to, kwargs)) or True,
    )
    monkeypatch.setattr(
        send_mod, "_announce_nudge",
        lambda _r, _to, _delivered: None,
    )

    send_mod.send(root, "director", "wake route", "kid-1")

    assert (root / ".agi" / "sessions" / "inbox" / "director.md").is_file()
    assert routed == [(root, "director", {"sender": "kid-1"})]
    assert capsys.readouterr().out.strip() == str(
        (root / ".agi" / "sessions" / "inbox" / "director.md").resolve()
    )
