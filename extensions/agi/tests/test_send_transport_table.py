"""goal:g7.32.4 falsifier 2 — adding a transport is a TABLE ROW, not a new
harness `if` inside `send.py:main()`.

The router contract (goal:g7.32.4): transport selection is one lookup over a
module-scope table. This module pins three things on the built bytes:

  (a) `TRANSPORTS` exists at module scope and maps the three modes to the
      three handlers, keyed by the CLI flag that selects each one;
  (b) the REAL `send.main()` selects the matching handler for `send --room`,
      `send --to`, and plain inbox -- asserted by patching the HANDLERS
      (`send_room` / `send_dm` / `send`), never the table. A patched handler
      that runs proves SELECTION, which is the correct seam for a router
      claim; it says nothing about the handler's own behaviour;
  (c) a NEW row is reachable through the same lookup with no edit to `main()`:
      a 4th (key, flag, handler) row is injected and selected -- and driven
      through the real `main()` when its flag is set.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


class _Sent:
    """The shape `send_room`/`send_dm` return: a result with `.resolve()`."""

    def resolve(self) -> str:
        return "TRANSPORT-SENT"


@pytest.fixture
def project(tmp_path: Path, monkeypatch):
    """A tmp project + the isolation main()'s send path needs.

    `_project_root` is pinned to the tmp project so nothing resolves live;
    the identity env vars are cleared so the kid/prime dm gates (which are
    the subject of other tests, not this one) do not fire; the seat last-act
    stamp is recorded, never written.
    """
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"}))
    (root / "sessions" / "inbox").mkdir(parents=True)
    monkeypatch.setattr(send_mod, "_project_root", lambda: root)
    for key in ("AGI_TIER", "AGI_AGENT_ID", "AGI_SEAT", "AGI_ACTOR"):
        monkeypatch.delenv(key, raising=False)
    stamped: list = []
    monkeypatch.setattr(send_mod.last_act, "touch_env",
                        lambda r, s: stamped.append((r, s)))
    return root, stamped


def _argv(root: Path, *rest: str) -> list[str]:
    return ["--comms-root", str(root / "comms"), *rest]


# ───────────────────────── (a) the table ─────────────────────────


def test_transports_table_maps_three_modes_to_three_handlers():
    assert set(send_mod.TRANSPORTS) == {"room", "dm", "inbox"}
    assert send_mod.TRANSPORTS["room"] == ("room", send_mod._send_room_transport)
    assert send_mod.TRANSPORTS["dm"] == ("dm_to", send_mod._send_dm_transport)
    assert send_mod.TRANSPORTS["inbox"] == (None, send_mod._send_inbox_transport)


# ──────────────────── (b) main() selects by handler ────────────────────


def test_main_selects_room_handler(project, monkeypatch, capsys):
    root, stamped = project
    calls: list = []
    monkeypatch.setattr(send_mod, "send_room",
                        lambda *a, **k: calls.append("room") or _Sent())
    rc = send_mod.main(_argv(root, "send", "--room", "quorum", "hello"))
    capsys.readouterr()
    assert rc == 0
    assert calls == ["room"], "send --room did not reach send_room"


def test_main_selects_dm_handler(project, monkeypatch, capsys):
    root, stamped = project
    calls: list = []
    monkeypatch.setattr(send_mod, "send_dm",
                        lambda *a, **k: calls.append("dm") or _Sent())
    rc = send_mod.main(_argv(root, "send", "--to", "peer", "hello"))
    capsys.readouterr()
    assert rc == 0
    assert calls == ["dm"], "send --to did not reach send_dm"


def test_main_selects_inbox_handler(project, monkeypatch, capsys):
    root, stamped = project
    calls: list = []
    monkeypatch.setattr(send_mod, "send",
                        lambda *a, **k: calls.append("inbox"))
    rc = send_mod.main(_argv(root, "send", "peer", "hello"))
    capsys.readouterr()
    assert rc == 0
    assert calls == ["inbox"], "plain send did not reach send"


# ───────────── (c) a NEW row through the SAME lookup, main() untouched ─────────


def test_new_table_row_is_selected_by_the_same_lookup(monkeypatch):
    calls: list = []

    def fake_handler(args, root, croot, sender) -> int:
        calls.append("smoke")
        return 0

    # a 4th row with a flag the selector can key on -- no edit to main().
    monkeypatch.setitem(send_mod.TRANSPORTS, "smoke", ("smoke_flag", fake_handler))
    args = SimpleNamespace(room=None, dm_to=None, smoke_flag="on")
    key = send_mod._select_transport(args)
    assert key == "smoke"
    assert send_mod.TRANSPORTS[key][1] is fake_handler
    assert send_mod.TRANSPORTS[key][1](args, None, None, None) == 0
    assert calls == ["smoke"]


def test_new_row_is_reachable_through_real_main_without_editing_it(
        project, monkeypatch, capsys):
    """A 4th row that claims an EXISTING flag, placed first, changes real
    dispatch: `send --room` reaches the new handler and NOT `send_room`.
    `main()` is not edited -- only the table is."""
    root, stamped = project
    calls: list = []

    def fake_handler(args, root_, croot, sender) -> int:
        calls.append("new-row")
        return 0

    monkeypatch.setattr(send_mod, "TRANSPORTS",
                        {"newrow": ("room", fake_handler),
                         **send_mod.TRANSPORTS})
    monkeypatch.setattr(send_mod, "send_room",
                        lambda *a, **k: calls.append("send_room") or _Sent())
    rc = send_mod.main(_argv(root, "send", "--room", "quorum", "hello"))
    capsys.readouterr()
    assert rc == 0
    assert calls == ["new-row"], f"new row not selected through main(): {calls}"