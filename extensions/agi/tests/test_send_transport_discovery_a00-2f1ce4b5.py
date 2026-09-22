"""goal:g7.32.4 falsifier 2, module+discovery leg -- a transport module is
sufficient ON ITS OWN. Dropping a file that defines
``register(register_delivery, helpers)`` into the transport directory is the
whole registration: no edit to send.py's selection loop and no import added
to send.py. send_transports.discover() scans the directory at startup.

The falsifier: a NEW module in a temp dir, pointed at by the loader, makes
``send()`` deliver through it -- and the built-in file/nudge transports now
live in their own module too, not inside send.py.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import send_transports  # noqa: E402

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)

NEW_TRANSPORT = '''
"""A new transport, dropped in with no edit to send.py."""
from pathlib import Path


def register(register_delivery, helpers):
    calls = helpers.setdefault("calls", [])

    def deliver(root, kind, path, payload, **kw):
        if kind != "file":
            return False
        calls.append((Path(path).name, payload))
        Path(path).write_text("INTERCEPTED\\n")
        return True

    register_delivery("carrier-pigeon", deliver, priority=1)
'''


@pytest.fixture
def registry():
    """Snapshot/restore the delivery table (and the loader's seen-set) so a
    test cannot leak into another."""
    saved = list(send_mod.DELIVERY_TRANSPORTS)
    seen = send_mod.register_delivery.__dict__.get("_discovered_paths")
    yield
    send_mod.DELIVERY_TRANSPORTS[:] = saved
    if seen is None:
        send_mod.register_delivery.__dict__.pop("_discovered_paths", None)
    else:
        send_mod.register_delivery.__dict__["_discovered_paths"] = seen


def _repo_send_source() -> str:
    return (BIN / "send.py").read_text()


def test_dropped_module_registers_with_no_edit_to_send(tmp_path, registry):
    """The falsifier: a new file alone is sufficient -- discovered, selected
    by the generic loop, and used by send()."""
    (tmp_path / "carrier_pigeon.py").write_text(NEW_TRANSPORT)
    helpers: dict = {}
    loaded = send_transports.discover(send_mod.register_delivery, helpers,
                                      directory=tmp_path)
    assert loaded == ["carrier_pigeon"]
    assert [name for name, _h in send_mod.DELIVERY_TRANSPORTS][0] == \
        "carrier-pigeon"

    send_mod.send(tmp_path, "someone", "hello", "me", nudge=False)

    inbox = send_mod._inbox_path(tmp_path, "someone")
    assert inbox.read_text() == "INTERCEPTED\n"
    assert helpers["calls"] and helpers["calls"][0][0] == "someone.md"

    # No import of the new module was added to send.py, and the loader is the
    # only admission point -- the literal "new module, never a new if" claim.
    src = _repo_send_source()
    assert "carrier_pigeon" not in src
    assert "carrier-pigeon" not in src


def test_discover_is_idempotent_per_registry(tmp_path, registry):
    """Re-running the scan (import/reload) must not double-register."""
    marker = tmp_path / "once.py"
    marker.write_text(NEW_TRANSPORT.replace("carrier-pigeon", "one-shot"))
    helpers: dict = {}
    first = send_transports.discover(send_mod.register_delivery, helpers,
                                     directory=tmp_path)
    second = send_transports.discover(send_mod.register_delivery, helpers,
                                      directory=tmp_path)
    assert first == ["once"]
    assert second == []
    assert [n for n, _h in send_mod.DELIVERY_TRANSPORTS].count("one-shot") == 1


def test_builtin_delivery_lives_in_its_own_module(tmp_path, registry):
    """The file/nudge transports are module+row, not code in send.py: the
    real directory is discovered at import and its row is present."""
    rows = {name: h for name, h in send_mod.DELIVERY_TRANSPORTS}
    assert "default" in rows
    src = _repo_send_source()
    assert "def _deliver_default" not in src
    assert (BIN / "send_transports" / "default_delivery.py").is_file()

    # ...and with nothing extra registered the bytes are the old append.
    send_mod.send(tmp_path, "someone", "hello", "me", nudge=False)
    inbox = send_mod._inbox_path(tmp_path, "someone")
    assert inbox.read_text().startswith("---\nts: ")
    assert inbox.read_text().endswith("\nhello\n")