"""goal:g1.31.4.2.1 (DG5 lane of the PASS B3 residues): #45 `rotate.py status`
lists the post session's windows; #32 the copilot post-spawn line names its
shipped --remote mode. tmux is faked; no live pane is touched."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import rotate  # noqa: E402


def test_status_lists_windows_in_post_session(monkeypatch, capsys):
    calls = []

    def fake_run(argv, **kw):
        calls.append(argv)
        if argv[:2] == ["tmux", "list-sessions"]:
            return subprocess.CompletedProcess(argv, 0, f"{rotate.DEFAULT_TMUX_SESSION}\nother\n", "")
        return subprocess.CompletedProcess(argv, 0, "belam-S2\t1\t0\n", "")

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    rotate.cmd_status(NS(record=None, seats=False, post=None, seat=None), None)
    listed = [a[a.index("-t") + 1] for a in calls if a[:2] == ["tmux", "list-windows"]]
    assert listed == [rotate.DEFAULT_TMUX_SESSION]
    assert "belam-S2" in capsys.readouterr().out


def test_copilot_spawn_line_names_its_remote_mode():
    src = Path(rotate.__file__).read_text(encoding="utf-8")
    assert "copilot has no remote-control" not in src
    assert "(copilot runs in its --remote mode, not claude.ai)" in src
    toml = (Path(rotate.__file__).resolve().parents[1] / "templates" / "harness"
            / "copilot-cli.toml").read_text(encoding="utf-8")
    assert 'const = "--remote"' in toml
