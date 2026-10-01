"""F1-F10 of hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit: a
workflow stage runs in a NAMED scope and stops it on EVERY exit path, so no
orphan (a repo-wide grep the stage left behind) outlives its stage.
FAKES ONLY. `systemd-run` / `systemctl` are tmp scripts put FIRST ON PATH, and
`_stops` asserts every stop resolved INSIDE that tmp dir. The recorder WRAPS the
conftest autouse guard (never the stdlib original) and runs the proven tmp fake
itself, so the guard still fires for what the fake does not cover (F10).
"""
import contextlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import mem_cap  # noqa: E402
import workflow as _wf  # noqa: E402

#: the TRUE stdlib subprocess.run, for the proven tmp fake only (see `_stops`)
_TRUE_RUN = subprocess.run
WF = Path(__file__).resolve().parents[1] / "workflows"


def _fake_bin(tmp_path, monkeypatch, *, stop_rc=0, no_systemctl=False,
              stop_body="") -> Path:
    """PATH-first tmp fakes: systemd-run logs then execs; systemctl logs, runs
    `stop_body`, exits `stop_rc`."""
    d = tmp_path / "bin"
    d.mkdir()
    log = tmp_path / "calls.log"
    (d / "systemd-run").write_text(
        "#!/bin/bash\n" f'echo "run $*" >> "{log}"\n'
        'while [ "${1#-}" != "$1" ]; do shift; done\n'
        '[ "$1" = "--" ] && shift\n' 'exec "$@"\n')
    os.chmod(d / "systemd-run", 0o755)
    if not no_systemctl:
        (d / "systemctl").write_text(
            "#!/bin/bash\n" f'echo "ctl $*" >> "{log}"\n' f'{stop_body}exit {stop_rc}\n')
        os.chmod(d / "systemctl", 0o755)
    monkeypatch.setenv("PATH", f"{d}:{os.environ['PATH']}")
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    return d


def _unit_of(tmp_path: Path) -> str:
    """The `--unit=` the fake systemd-run ACTUALLY received."""
    log = tmp_path / "calls.log"
    run = next(ln for ln in (log.read_text().splitlines() if log.exists() else [])
               if ln.startswith("run "))
    return next(a.split("=", 1)[1] for a in run.split() if a.startswith("--unit="))


def _stops(monkeypatch, fake_dir: Path) -> list[list]:
    """Every `systemctl` argv issued, in order, each PROVEN to resolve inside
    `fake_dir`, declared `_wf._REAL_RUN` so the seam takes its real-launch path.

    Item 4: the spy WRAPS whatever `subprocess.run` is CURRENT when the test
    starts (the conftest guard), never the stdlib original. The guard answers
    rc 1 to every `systemctl stop`, which would leave the fake unrun -- so for a
    stop PROVEN inside `fake_dir` the spy runs that tmp script itself. F10
    shows the guard firing untouched for what the fake does not cover."""
    stops: list[list] = []
    chained = subprocess.run

    def _run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["systemctl"]:
            found = shutil.which(cmd[0])
            assert found is None or Path(found).parent == fake_dir, cmd
            stops.append(list(cmd))
            if found:
                return _TRUE_RUN([str(found), *cmd[1:]], *a, **k)
        return chained(cmd, *a, **k)
    monkeypatch.setattr(subprocess, "run", _run)
    monkeypatch.setattr(_wf, "_REAL_RUN", _run)
    return stops


def _env(d: Path, *, bare: bool = False) -> dict:
    """The stage's env; `bare=True` hides every REAL binary."""
    return {"PATH": str(d) if bare else f"{d}:{os.environ['PATH']}"}


@pytest.fixture
def fakes(tmp_path, monkeypatch):
    _fake_bin(tmp_path, monkeypatch)
    return tmp_path


def test_F1_normal_return_stops_the_scope_it_wrapped(fakes, monkeypatch):
    """A stage that backgrounds a child and exits 0 stops the unit the wrap
    USED exactly once; `_stops` asserts no real systemctl was reachable."""
    stops = _stops(monkeypatch, fakes / "bin")
    (fakes / "stage.sh").write_text("#!/bin/bash\nsleep 30 >/dev/null 2>&1 &\nexit 0\n")
    r = _wf._run_stage_proc(["bash", str(fakes / "stage.sh")], budget=10,
                            stage={"label": "review"}, spawn_env=_env(fakes / "bin"),
                            view=None, cap="64M", cfg={}, run_key="mur-39")
    assert r.returncode == 0
    unit = _unit_of(fakes)
    assert unit.startswith("agi-stage-mur-39_review-")
    assert stops == [["systemctl", "--user", "stop", unit]]   # never silence


def test_F2_wall_kill_and_exception_still_stop(tmp_path, monkeypatch):
    """F2: the wall-kill and the exception paths stop the scope too."""
    d = _fake_bin(tmp_path, monkeypatch)
    stops = _stops(monkeypatch, d)
    (tmp_path / "slow.sh").write_text("#!/bin/bash\nexec sleep 30\n")
    with pytest.raises(subprocess.TimeoutExpired):
        _stage(["bash", str(tmp_path / "slow.sh")], d, budget=0.2)
    assert stops == [["systemctl", "--user", "stop", _unit_of(tmp_path)]]

    boom = tmp_path / "boom"; boom.mkdir()
    d2 = _fake_bin(boom, monkeypatch)
    stops2 = _stops(monkeypatch, d2)
    monkeypatch.setattr(mem_cap, "wrap_argv", lambda *a, **k:  # after the mint
                        (_ for _ in ()).throw(OSError("wrap failed")))
    with pytest.raises(OSError):
        _wf._run_stage_proc(["true"], budget=5, stage={"label": "review"},
                            spawn_env=_env(d2), view=None, cap="64M", cfg={},
                            run_key="mur-39")
    assert len(stops2) == 1


def test_F3_a_failing_stop_is_one_stderr_line_and_never_a_raise(tmp_path,
        monkeypatch, capsys):
    """F3: a failing stop never raises -- NON-ZERO and cannot-RUN are ONE line."""
    script = tmp_path / "s.sh"
    script.write_text("#!/bin/bash\nexit 3\n")
    for kwargs in (dict(stop_rc=1), dict(no_systemctl=True)):
        root = tmp_path / f"case{sorted(kwargs)}{kwargs.get('stop_rc', '')}"
        root.mkdir()
        bare = "no_systemctl" in kwargs
        d = _fake_bin(root, monkeypatch, **kwargs)
        if bare:
            monkeypatch.setenv("PATH", str(d))   # the REAL systemctl unreachable
        seen = _stops(monkeypatch, d)
        r = _wf._run_stage_proc(["/bin/bash", str(script)], budget=10,
                                stage={"label": "review"}, spawn_env=_env(d, bare=bare),
                                view=None, cap="64M", cfg={}, run_key="mur-39")
        assert (r.returncode, len(seen)) == (3, 1), kwargs   # attempted either way
        err = capsys.readouterr().err
        assert err.count("could not stop stage scope") == 1, kwargs
        assert _unit_of(root) in err, kwargs                # the line NAMES it


def test_F4_wrap_argv_without_a_unit_is_byte_unchanged(monkeypatch):
    """F4: the new `unit=` kwarg changes NO existing caller's argv."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    plain = mem_cap.wrap_argv(["pi", "-p"], "64M", {})
    assert "--unit=" not in " ".join(plain)
    named = mem_cap.wrap_argv(["pi", "-p"], "64M", {}, unit="agi-stage-x-1")
    assert named == plain[:4] + ["--unit=agi-stage-x-1"] + plain[4:]
    assert mem_cap.wrap_argv(["pi", "-p"], None) == ["pi", "-p"]


def test_F5_both_merge_up_review_prompts_forbid_a_recursive_grep():
    """F5: the no-grep line is in BOTH carriers -- the workflow's stage prompts
    and the script's own REVIEW/VERIFY templates."""
    want = ("never grep -r", "never `rg`", "never `find`")
    prompts = [s["prompt"] for s in
               json.loads((WF / "merge-up-review.json").read_text())["stages"]]
    assert len(prompts) >= 2
    for p in prompts + [(WF / "agi-merge-up-review.js").read_text()]:
        assert all(w in p.lower() for w in want), p[:60]


def _fast_wall(monkeypatch):
    """Bound the post-stop pipe grace so a wall row costs seconds, not 30."""
    monkeypatch.setattr(_wf, "_WALL_STOP_GRACE_S", 1.0)


@contextlib.contextmanager
def _reaped(pids: Path):
    """Never leave a 300 s sleeper behind, pass or fail."""
    try:
        yield
    finally:
        for p in (pids.read_text().split() if pids.exists() else []):
            with contextlib.suppress(OSError, ValueError):
                os.kill(int(p), 9)


def _kill_scope(pids: Path) -> str:
    """A fake stop modelling a REAL scope stop (every pid in the scope goes),
    WAITING for the pids file instead of racing the budget (item 3)."""
    return (f"for _ in $(seq 100); do [ -s {pids} ] && break; sleep 0.05; done\n"
            f"kill -9 $(cat {pids}) 2>/dev/null\n")


def _orphan_dead(pids: Path) -> bool:
    for p in (pids.read_text().split() if pids.exists() else []):
        try:
            return Path(f"/proc/{int(p)}/stat").read_text().split()[2] in "ZX"
        except (OSError, ValueError):
            return True
    return True


def _fake_stage(tmp_path, body: str) -> list[str]:
    """A bash stage script that records its orphan's pid, plus the argv for it."""
    p = tmp_path / "stage.sh"
    p.write_text(f'#!/bin/bash\nsleep 300 &\n'
                 f'echo $! >> "{tmp_path / "pids"}"\n{body}')
    return ["bash", str(p)]


def _stage(args, d: Path, *, budget=1.0, label="verify", ext=0):
    """One capped, NAMED-scope stage launch through the seam under test."""
    return _wf._run_stage_proc(args, budget=budget,
                               stage={"label": label, "max_extensions": ext},
                               spawn_env=_env(d), view=None, cap="64M", cfg={},
                               run_key="mur-39")


def test_F6_an_orphan_holding_the_stage_pipe_dies_with_the_scope(tmp_path, monkeypatch):
    """F6: a stage whose backgrounded child INHERITS its stdout pipe hung the
    wall path forever (the orphan held the pipe, so the `finally` that stops the
    unit never ran). Now: a wall kill inside a bound, and the ORPHAN DEAD."""
    _fast_wall(monkeypatch)
    pids = tmp_path / "pids"
    d = _fake_bin(tmp_path, monkeypatch, stop_body=_kill_scope(pids))
    stops = _stops(monkeypatch, d)
    with _reaped(pids):
        t0 = time.monotonic()
        with pytest.raises(subprocess.TimeoutExpired):
            _stage(_fake_stage(tmp_path, "exec sleep 300\n"), d, budget=0.5)
        assert time.monotonic() - t0 < 20, "the wall path hung again"
        assert stops == [["systemctl", "--user", "stop", _unit_of(tmp_path)]]
        assert _orphan_dead(pids)


def test_F7_a_stage_that_exited_with_a_held_pipe_returns_its_own_rc(tmp_path, monkeypatch):
    """item 2(a): the stage EXITED (rc 7) with an orphan still holding its pipe:
    its own rc is the result, the unit IS stopped, nothing is left alive."""
    _fast_wall(monkeypatch)
    pids = tmp_path / "pids"
    d = _fake_bin(tmp_path, monkeypatch, stop_body=_kill_scope(pids))
    stops = _stops(monkeypatch, d)
    with _reaped(pids):
        r = _stage(_fake_stage(tmp_path, "exit 7\n"), d)
        assert r.returncode == 7
        assert stops == [["systemctl", "--user", "stop", _unit_of(tmp_path)]]
        assert _orphan_dead(pids)


def test_F8_a_real_wall_timeout_raises_though_the_orphan_survives(tmp_path, monkeypatch, capsys):
    """item 2(b): a stage STILL RUNNING at the wall whose orphan SURVIVES the
    stop must raise TimeoutExpired, so the caller reports 'timed out after N s'
    (workflow.py:2035-2043); pre-fix it returned a bare negative rc instead."""
    _fast_wall(monkeypatch)
    pids = tmp_path / "pids"
    d = _fake_bin(tmp_path, monkeypatch)   # the stop does NOT reach the orphan
    stops = _stops(monkeypatch, d)
    with _reaped(pids):
        with pytest.raises(subprocess.TimeoutExpired):
            _stage(_fake_stage(tmp_path, "exec sleep 300\n"), d)
        assert stops, "the unit must still be stopped on a real wall kill"
        err = capsys.readouterr().err.lower()
        assert "memory" not in err and "timed out after" not in err
        assert _wf._result_file_value({"label": "verify"}, {}, None) is None


def test_F9_a_prlimit_fallback_launch_stops_nothing(tmp_path, monkeypatch):
    """item 2(c): the prlimit fallback wraps in `prlimit`, not `systemd-run`, so
    no scope exists and NO stop is attempted."""
    d = _fake_bin(tmp_path, monkeypatch)
    stops = _stops(monkeypatch, d)
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    assert _stage(["/bin/bash", "-c", "exit 5"], d, budget=10,
                  label="review").returncode == 5
    assert stops == []


def test_F10_the_conftest_guard_still_stops_a_real_shaped_unit(tmp_path, monkeypatch, capsys):
    """item 4: a `systemctl --user stop` from this file with NO proven tmp fake
    is still answered rc 1 by the guard -- the sentinel is never written."""
    bin_ = tmp_path / "real"
    bin_.mkdir()
    sentinel = tmp_path / "sentinel"
    (bin_ / "systemctl").write_text(f"#!/bin/sh\ntouch {sentinel}\n")
    os.chmod(bin_ / "systemctl", 0o755)
    monkeypatch.setenv("PATH", f"{bin_}:{os.environ['PATH']}")
    _wf._stop_stage_unit("agi-stage-mur-39_review-x")
    assert not sentinel.exists(), "the real user manager was reached"
    assert capsys.readouterr().err.count(
        "could not stop stage scope agi-stage-mur-39_review-x") == 1
