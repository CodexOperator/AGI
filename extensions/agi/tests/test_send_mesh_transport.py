"""goal:g7.31.4 — one transport resolver behind an unchanged send/wake surface.

`send.py send <to> <text>` must produce the SAME caller-facing result whether
the recipient's `config:posts` row is on this box or another one. The branch on
transport (local / mesh / no-mesh) lives ONLY in `_nudge_transport`; every
tmux call keeps ONE shape and only the argv PREFIX changes.

Falsifiers, each named below:
  (1) local seat: inbox block AND a `send-keys` typing the wake token;
  (2) foreign seat with a mesh alias: the SAME args succeed, the fake ssh sees
      the token and never the body;
  (3) foreign seat with no mesh transport: success, inbox present, no ssh, one
      named "mail_poll" line -- never a silent refusal;
  (4) wire probe: the resolver is invoked from the `send` call site;
  (5) `_nudge_target` (the local address resolver) is untouched: a foreign row
      still has no local address.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import send as send_mod  # noqa: E402


@pytest.fixture(autouse=True)
def _box_env(monkeypatch):
    monkeypatch.setenv("AGI_BOX", "core-town")


def _rows(rows):
    lines = ["---", "id: config:posts", "type: config", "default_box: core-town",
             "posts:"]
    # the town's `council` cell must name a real posts row (towns._validate)
    for r in [{"name": "council-local"}, *rows]:
        lines.append("  - " + json.dumps(r))
    lines.append("---")
    return "\n".join(lines) + "\n"


def _graph(tmp: Path, rows, town_location: str | None = "local-town",
           town_name: str = "local-maxxing") -> Path:
    """A minimal graph root with a posts node, one town and one vision."""
    root = tmp / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text("{}")
    geom = root / "nodes" / ".geometry"
    geom.mkdir(parents=True)
    (geom / "posts.md").write_text(_rows(rows))
    (root / "nodes" / "vision").mkdir(parents=True)
    (root / "nodes" / "vision" / "v1.md").write_text(
        "---\nid: vision:v1\ntype: vision\n---\n")
    (root / "nodes" / "town").mkdir(parents=True)
    loc = f"location: {town_location}\n" if town_location else ""
    (root / "nodes" / "town" / f"{town_name}.md").write_text(
        f"---\nid: town:{town_name}\ntype: town\nvisions: [vision:v1]\n"
        f"council: council-local\nseason: 1\n{loc}---\n")
    return root


def _fake_run(monkeypatch, window_names=("@246", "director")):
    """Record EVERY subprocess argv; tmux calls succeed, ssh calls are the
    recorded remote transport. Never touches a live pane or a real host."""
    calls = []

    def fake_run(cmd, capture_output=True, text=True, timeout=5):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(cmd, 0,
                                               stdout="\n".join(window_names),
                                               stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: None)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    return calls


FOREIGN = {"name": "director", "role": "director", "window": "@246",
           "pid": 424242, "box": "local-town", "town": "local-maxxing"}
LOCAL = {"name": "director", "role": "director", "window": "@246",
         "pid": 424242, "box": "core-town", "town": "core"}


# ── (1) local seat: the resolver says local, bytes are today's ───────────

def test_local_seat_types_with_bare_tmux_and_resolver_says_local(tmp_path,
                                                                 monkeypatch):
    root = _graph(tmp_path, [LOCAL])
    calls = _fake_run(monkeypatch)
    assert send_mod._nudge_transport(root, "director") == ("local", [])
    body = "an inbox body that must never be typed"
    send_mod.send(root, "director", body, "a00-xxxx")
    inbox = root / ".agi" / "sessions" / "inbox" / "director.md"
    assert "an inbox body that must never be typed" in inbox.read_text()
    typed = [c for c in calls if c[:3] == ["tmux", "send-keys", "-l"]]
    assert typed, "a local send must type the wake token"
    assert "director" in typed[-1][-1], "the token names the seat"
    assert body not in typed[-1][-1], "the body is never typed"


# ── (2) foreign seat WITH a mesh alias: same args, remote transport ───────

def test_foreign_seat_with_mesh_alias_types_on_the_remote_box(tmp_path,
                                                              monkeypatch):
    root = _graph(tmp_path, [FOREIGN])
    calls = _fake_run(monkeypatch)
    kind, prefix = send_mod._nudge_transport(root, "director")
    assert (kind, prefix) == ("mesh", ["ssh", "local-town"]), \
        "the alias is READ from the town's `location` cell"
    body = "the body must never reach the remote transport"
    send_mod.send(root, "director", body, "a00-xxxx")
    inbox = root / ".agi" / "sessions" / "inbox" / "director.md"
    assert "the body must never reach the remote transport" in inbox.read_text()
    ssh = [c for c in calls if c[:2] == ["ssh", "local-town"]]
    assert ssh, "a foreign mesh seat must be typed through the ssh alias"
    assert ssh[0][2:5] == ["tmux", "send-keys", "-l"]
    assert "director" in ssh[0][-1], "the token names the remote seat"
    assert body not in " ".join(ssh[0]), "the body never reaches the transport"


# ── (3) foreign seat with NO mesh: honest fallback, never a silent refusal ─

def test_foreign_seat_without_mesh_names_mail_poll_and_types_nothing(tmp_path,
                                                                    monkeypatch,
                                                                    capsys):
    root = _graph(tmp_path, [FOREIGN], town_location=None)
    calls = _fake_run(monkeypatch)
    assert send_mod._nudge_transport(root, "director") == ("none", [])
    send_mod.send(root, "director", "kept in the inbox", "a00-xxxx")
    err = capsys.readouterr().err
    assert "mail_poll delivers the inbox" in err, \
        "the missing transport is named, never a silent refusal"
    assert not [c for c in calls if c and c[0] == "ssh"], \
        "no mesh transport must attempt no ssh"
    assert not [c for c in calls if c[:2] == ["tmux", "send-keys"]], \
        "no wake is typed without a transport"
    inbox = root / ".agi" / "sessions" / "inbox" / "director.md"
    assert "kept in the inbox" in inbox.read_text()


# ── (4) wire probe: the resolver is reached from the send call site ───────

def test_send_call_site_reaches_the_one_resolver(tmp_path, monkeypatch):
    root = _graph(tmp_path, [FOREIGN])
    _fake_run(monkeypatch)
    seen = []
    real = send_mod._nudge_transport

    def spy(r, to):
        out = real(r, to)
        seen.append((to, out))
        return out

    monkeypatch.setattr(send_mod, "_nudge_transport", spy)
    send_mod.send(root, "director", "hi", "a00-xxxx")
    assert seen, "`_nudge_window` must reach `_nudge_transport`, not a stub"


# ── (5) the local address resolver keeps refusing foreign rows ────────────

def test_foreign_row_still_has_no_local_address(tmp_path, monkeypatch):
    root = _graph(tmp_path, [FOREIGN])
    monkeypatch.setattr(send_mod, "_window_id_listed", lambda *a, **k: True)
    assert send_mod._nudge_target(root, "director", None) is None