"""crons._systemd_bus_env: a post unit sets DBUS_SESSION_BUS_ADDRESS=disabled: (agi-post@ drop-in
51-no-session-bus.conf), which names NO bus -- it must fall through to the socket probe, never read as
"bus reachable" (DG1 09:04Z 10-10). A real address still means reachable; no address + no socket = None."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import crons  # noqa: E402


def test_a_real_address_is_reachable(monkeypatch):
    monkeypatch.setenv("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")
    assert crons._systemd_bus_env() == {}


def test_disabled_with_no_socket_is_the_named_skip(monkeypatch, tmp_path):
    monkeypatch.setenv("DBUS_SESSION_BUS_ADDRESS", "disabled:")
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))
    assert crons._systemd_bus_env() is None


def test_disabled_with_a_socket_hands_the_socket_over(monkeypatch, tmp_path):
    monkeypatch.setenv("DBUS_SESSION_BUS_ADDRESS", "disabled:")
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))
    (tmp_path / "bus").touch()
    assert crons._systemd_bus_env() == {"XDG_RUNTIME_DIR": str(tmp_path),
                                     "DBUS_SESSION_BUS_ADDRESS": f"unix:path={tmp_path}/bus"}


def test_no_address_and_no_socket_is_the_named_skip(monkeypatch, tmp_path):
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))
    assert crons._systemd_bus_env() is None
