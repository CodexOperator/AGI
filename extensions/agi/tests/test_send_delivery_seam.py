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

# ── R1 (goal:g7.32.4 residue): dm and room file appends route through the
# SAME delivery table as the inbox append. Before this fix only `send()`
# consulted it; a `kind="file"` row never saw a dm or a room block.

def test_dm_file_append_routes_through_a_runtime_file_transport(
        tmp_path, registry):
    """A `kind="file"` row is handed the dm block, and the dm file is NOT
    written when the row claims it -- the thinness contract (R1, part a)."""
    seen = []

    def carrier(root, kind, path, payload, **kw):
        if kind in ("file", "nudge"):
            seen.append((kind, Path(path).name, payload))
            return True
        return False

    send_mod.register_delivery("carrier-pigeon", carrier, priority=1)
    send_mod.send_dm(tmp_path, "alice", "bob", "hello bob", "alice")

    files = [s for s in seen if s[0] == "file"]
    assert len(files) == 1, seen
    assert files[0][1] == "alice--bob.md"
    assert files[0][2].startswith("---\nts: ")
    assert files[0][2].endswith("\nhello bob\n")
    assert not send_mod._dm_path(tmp_path, "alice", "bob").exists()


def test_room_file_append_routes_through_a_runtime_file_transport(
        tmp_path, registry):
    """The room leg is not a bypass: a `kind="file"` row sees the room block
    and the room file is not written when the row claims it (R1, part a)."""
    seen = []

    def carrier(root, kind, path, payload, **kw):
        if kind == "file":
            seen.append((Path(path).name, payload))
            return True
        return False

    send_mod.register_delivery("carrier-pigeon", carrier, priority=1)
    send_mod.send_room(tmp_path, "lab", "hello room", "alice")

    assert len(seen) == 1, seen
    assert seen[0][0] == "lab.md"
    assert seen[0][1].endswith("\nhello room\n")
    assert not send_mod._room_path(tmp_path, "lab").exists()


def test_default_dm_and_room_bytes_are_unchanged(tmp_path, registry):
    """With no extra row the dm/room bytes are the old inline write,
    byte-for-byte: `---\nts: ...` .. `\nbody\n` (R1, part b)."""
    send_mod.send_dm(tmp_path, "alice", "bob", "hello bob", "alice")
    send_mod.send_room(tmp_path, "lab", "hello room", "alice")

    dm = send_mod._dm_path(tmp_path, "alice", "bob").read_text()
    room = send_mod._room_path(tmp_path, "lab").read_text()
    assert dm.startswith("---\nts: ") and dm.endswith("\nhello bob\n")
    assert "from: alice\n" in dm and "to: bob\n" in dm
    assert room.startswith("---\nts: ") and room.endswith("\nhello room\n")
    assert "from: alice\n" in room and "to: lab\n" in room
