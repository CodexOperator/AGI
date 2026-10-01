"""G7.4: strace -b execve detaches on the harness pid's 2nd exec, so a pi row (env-shebang) must start with the interpreter."""
import os, shutil, subprocess, tempfile, time
import pytest
from tests import test_project_agi_box as base

ROW = '  - {"name": "t1", "engine": {"v": 4, "harness": "%s", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "harness": "%s", "box": "%%s"}\n'
needs_pty = pytest.mark.skipif(not (shutil.which("strace") and shutil.which("script")), reason="strace/script absent")


def h_of(tmp_path, monkeypatch, harness, path=None):
    monkeypatch.setattr(base, "ROW", ROW % (harness, harness))
    return base.project(tmp_path, path=path).split('Environment="H=')[1].split('" O=')[0]


def _bin(tmp_path, name, pi):
    d = tmp_path / name
    d.mkdir()
    if pi:
        (d / "pi").write_text("#!/bin/sh\n"), (d / "pi").chmod(0o755)
    return d


def test_pi_row_is_node_exact_dir_pi_first_on_unit_path(tmp_path, monkeypatch):
    a, b, c = _bin(tmp_path, "a", 0), _bin(tmp_path, "b", 1), _bin(tmp_path, "c", 1)
    h = h_of(tmp_path, monkeypatch, "pi-free", f"/var/lib/agi/%i/bin:{a}:{b}:{c}")  # %i + a pi-less dir skipped; first holder wins
    assert h.startswith(f"node {b}/pi --provider openrouter --model m --thinking high "), h


def test_no_pi_on_unit_path_refuses_before_any_h_conf(tmp_path, monkeypatch):
    with pytest.raises(subprocess.CalledProcessError) as e:
        h_of(tmp_path, monkeypatch, "pi-free", str(_bin(tmp_path, "a", 0)))
    assert e.value.returncode == 3 and not list((tmp_path / "out").glob("*/h.conf"))


def test_claude_only_box_projects_without_pi_byte_identical(tmp_path, monkeypatch):
    monkeypatch.setattr(base, "ROW", ROW % (("claude-code",) * 2))
    (x, y), nopi = (tmp_path / "x", tmp_path / "y"), _bin(tmp_path, "n", 0)
    x.mkdir(), y.mkdir()
    assert base.project(x, path=str(nopi)).replace(str(x), "") == base.project(y).replace(str(y), "")


def test_claude_row_unchanged(tmp_path, monkeypatch):
    assert h_of(tmp_path, monkeypatch, "claude-code").startswith("claude --remote-control t1 --model m --effort high --permission-mode bypassPermissions")


def _wall(tmp_path, *argv):
    """Wall time of `agi-run's strace under a pty, stdin a never-EOF fifo; the `-o '|cmd'` sink is what makes strace exit at the detach (`-o FILE` waits)."""
    fifo = f"{tmp_path}/in{len(os.listdir(tmp_path))}"
    os.mkfifo(fifo)
    fd = os.open(fifo, os.O_RDWR)
    t = time.time()
    subprocess.run(["timeout", "4", "script", "-qfec", " ".join(["strace -qqf -b execve -e%file -o'|cat >/dev/null'", *map(str, argv)]), "/dev/null"], stdin=fd, capture_output=True)
    os.close(fd)
    return time.time() - t


@needs_pty
def test_env_shebang_under_b_execve_ends_at_once_interpreter_direct_stays(tmp_path):
    s = tmp_path / "pi"
    s.write_text("#!/usr/bin/env sh\nsleep 3\n"), s.chmod(0o755)
    fast, kept = _wall(tmp_path, s), _wall(tmp_path, "sh", s)
    assert fast < 1.5 <= 2 <= kept, (fast, kept)
