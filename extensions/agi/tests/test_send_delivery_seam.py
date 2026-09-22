"""goal:g7.32.4 falsifier 2, DELIVERY leg -- `send()` and `send_dm()` choose
where the bytes finally land from a runtime-extensible table
(`DELIVERY_TRANSPORTS` + `register_delivery`), so a new delivery transport is
a new module + a table row, never a new `if` in send.py.

The testable claim: a delivery transport registered at run time is chosen by
the generic first-match loop -- `send()` appends through IT instead of the
built-in inbox write -- while with no transport registered every byte is
unchanged (the default row is the old inline write, verbatim).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

spec = importlib.util.spec_from_file_location("send", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)


@pytest.fixture
def registry():
    """Snapshot/restore the delivery table (module-global state)."""
    saved = list(send_mod.DELIVERY_TRANSPORTS)
    yield
    send_mod.DELIVERY_TRANSPORTS[:] = saved


def test_send_delivers_through_a_runtime_registered_transport(tmp_path, registry):
    """The falsifier: `send()` hands the block to a NEW transport, with no
    edit to send.py's selection logic, and nothing hits the inbox file."""
    seen = []

    def carrier(root, kind, path, payload, **kw):
        if kind != "file":
            return False
        seen.append((kind, Path(path).name, payload))
        return True

    send_mod.register_delivery("carrier-pigeon", carrier, priority=1)

    sender, signed = send_mod.send(tmp_path, "someone", "hello", "me")

    assert len(seen) == 1
    assert seen[0][0] == "file"
    assert seen[0][1] == "someone.md"
    assert seen[0][2].endswith("\nhello\n")
    assert "from: me\n" in seen[0][2]
    # It replaced the default write -- the inbox file was never created.
    assert not send_mod._inbox_path(tmp_path, "someone").exists()
    assert (sender, signed) == ("me", False)


def test_no_transport_registered_is_the_old_inline_write(tmp_path, registry):
    """Byte-identical default: the built-in row appends the block to the
    inbox, exactly as the inline `open(inbox, "a")` did."""
    send_mod.send(tmp_path, "someone", "hello", "me")
    inbox = send_mod._inbox_path(tmp_path, "someone")
    assert inbox.is_file()
    assert inbox.read_text().startswith("---\nts: ")
    assert inbox.read_text().endswith("\nhello\n")


def test_declining_transport_falls_through_to_the_default(tmp_path, registry):
    """A row that returns False does not claim the delivery; the next row
    (the built-in) still handles it."""
    calls = []

    def polite(root, kind, path, payload, **kw):
        calls.append(kind)
        return False

    send_mod.register_delivery("polite", polite, priority=1)
    send_mod.send(tmp_path, "someone", "hello", "me")

    inbox = send_mod._inbox_path(tmp_path, "someone")
    assert inbox.is_file()
    assert inbox.read_text().endswith("\nhello\n")
    assert calls and calls[0] == "file"


def test_send_dm_nudge_leg_is_routable(tmp_path, registry):
    """The dm wake leg consults the same table: a registered transport can
    claim kind='nudge' and observe the dm body without a pane call."""
    seen = []

    def paneless(root, kind, path, payload, **kw):
        if kind != "nudge":
            return False
        seen.append((Path(path).name, payload))
        return True

    send_mod.register_delivery("paneless", paneless, priority=1)
    send_mod.send_dm(tmp_path, "alice", "bob", "hello bob", "alice")

    assert seen == [("bob", "hello bob")]
    # The dm FILE is still the durable record, untouched by the nudge table.
    assert send_mod._dm_path(tmp_path, "alice", "bob").is_file()