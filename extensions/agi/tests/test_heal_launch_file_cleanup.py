"""hypothesis:heal-never-reseats-a-worktree-post-into-main, defect (3).

A recovery launch that FAILS before the pane's `sh` ever runs the launch file
leaves the file — and the whole startup PROMPT it carries — in the temp dir
forever, readable by any process, one per failed recovery. The only unlink
used to be the `rm -f "$0"` line INSIDE the file, which by construction never
runs on a failed launch.

So: the WRITER owns the failure paths. `_unlink_launch_file` removes the file
when (a) the write failed mid-way, (b) `tmux new-window` raised (tmux absent
/ down / timeout), (c) `tmux new-window` returned non-zero. The SUCCESS path
still leaves the file for the pane's own shell to unlink — unlinking it here
would race the shell that is about to run it.

Never launches anything: `subprocess.run` is stubbed, and the tmux-absent probe
runs the real `subprocess.run` with `PATH` pointing at an empty dir, so tmux
cannot resolve (a real failure path on a real box). The temp dir is the test's
own `tmp_path`, set on `tempfile.tempdir` — the real `/tmp/agi-recover-*` files
on the box are never read or written.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")

PROMPT = "read the card and start\n" * 200


def _mine_tmpdir(monkeypatch, tmp_path: Path) -> Path:
    """Point tempfile at a dir this test owns. No new config cell: the code
    already honours the stdlib temp root, so this only sets it."""
    d = tmp_path / "mytmpshim"
    d.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(tempfile, "tempdir", str(d))
    return d


def _orphans(d: Path) -> list[Path]:
    return sorted(d.glob("agi-recover-*"))


def test_tmux_nonzero_leaves_no_launch_file(monkeypatch, tmp_path):
    d = _mine_tmpdir(monkeypatch, tmp_path)
    monkeypatch.setattr(heal.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(
                            a[0], 1, "", "can't find session"))
    pid, wid = heal._launch_recovered(tmp_path, "wt", PROMPT,
                                      cwd=tmp_path)
    assert (pid, wid) == (0, "")
    assert _orphans(d) == []


def test_tmux_absent_leaves_no_launch_file(monkeypatch, tmp_path):
    """THE REAL SHAPE: real subprocess.run, tmux not on PATH → FileNotFound
    → the `except Exception` failure path."""
    d = _mine_tmpdir(monkeypatch, tmp_path)
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    pid, wid = heal._launch_recovered(tmp_path, "wt", PROMPT,
                                      cwd=tmp_path)
    assert (pid, wid) == (0, "")
    assert _orphans(d) == []


def test_tmux_timeout_leaves_no_launch_file(monkeypatch, tmp_path):
    d = _mine_tmpdir(monkeypatch, tmp_path)

    def _boom(*a, **k):
        raise subprocess.TimeoutExpired(cmd="tmux", timeout=10)

    monkeypatch.setattr(heal.subprocess, "run", _boom)
    pid, wid = heal._launch_recovered(tmp_path, "wt", PROMPT,
                                      cwd=tmp_path)
    assert (pid, wid) == (0, "")
    assert _orphans(d) == []


def test_write_failure_leaves_no_launch_file(monkeypatch, tmp_path):
    d = _mine_tmpdir(monkeypatch, tmp_path)

    class _FailWrite:
        def __init__(self, fd):
            self.fd = fd

        def write(self, _s):
            raise OSError("disk full")

        def __enter__(self):
            return self

        def __exit__(self, *e):
            import os as _os
            _os.close(self.fd)
            return False

    monkeypatch.setattr(heal.os, "fdopen",
                        lambda fd, *a, **k: _FailWrite(fd))
    pid, wid = heal._launch_recovered(tmp_path, "wt", PROMPT,
                                      cwd=tmp_path)
    assert (pid, wid) == (0, "")
    assert _orphans(d) == []


def test_non_oserror_write_neither_raises_nor_orphans(monkeypatch, tmp_path):
    """The LIFETIME bug: a NON-OSError out of the write used to escape
    `_launch_recovered` (its docstring promises "Never raises into the watch
    pass" — a dead watch pass kills heal for every seat) AND leave the prompt
    on disk, because the orphan unlink hung off an `except OSError` list."""
    d = _mine_tmpdir(monkeypatch, tmp_path)

    class _GremlinWrite:
        def __init__(self, fd):
            self.fd = fd

        def write(self, _s):
            raise ValueError("disk gremlin, not an OSError")

        def __enter__(self):
            return self

        def __exit__(self, *e):
            import os as _os
            _os.close(self.fd)
            return False

    monkeypatch.setattr(heal.os, "fdopen",
                        lambda fd, *a, **k: _GremlinWrite(fd))
    pid, wid = heal._launch_recovered(tmp_path, "wt", PROMPT, cwd=tmp_path)
    assert (pid, wid) == (0, "")
    assert _orphans(d) == []


def test_success_leaves_the_file_for_the_pane(monkeypatch, tmp_path):
    """The `rm -f "$0"` self-unlink still owns the success case: the file must
    SURVIVE here, or the pane's own `sh` would race the writer."""
    d = _mine_tmpdir(monkeypatch, tmp_path)
    monkeypatch.setattr(heal.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(
                            a[0], 0, "@9\n", ""))
    pid, wid = heal._launch_recovered(tmp_path, "wt", PROMPT,
                                      cwd=tmp_path)
    assert pid is None and wid == "@9"
    left = _orphans(d)
    assert len(left) == 1
    assert 'rm -f "$0"' in left[0].read_text(encoding="utf-8")
