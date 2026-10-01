"""F1-F6 of hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit: a
workflow stage runs in a NAMED scope and stops it on EVERY exit path, so no
orphan (a repo-wide grep the stage left behind) outlives its stage.
FAKES ONLY. `systemd-run` / `systemctl` are tmp scripts put FIRST ON PATH by `_fake_bin`
(the code calls `systemctl` by bare name with no env=), and `_stops` asserts
every stop resolved INSIDE that tmp dir. HONEST CAVEAT: the suite's autouse
guard is stood down here -- it patches the very attribute under test; the
tmp-dir assert replaces it. The recorder also declares itself `_wf._REAL_RUN`
(the real-launch path) and reaches only tmp scripts.
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

#: the TRUE subprocess.run, captured before conftest's autouse guard patched it
_TRUE_RUN = subprocess.run
WF = Path(__file__).resolve().parents[1] / "workflows"


def _fake_bin(tmp_path, monkeypatch, *, stop_rc=0, no_systemctl=False,
              stop_body="") -> Path:
    """PATH-first tmp fakes: systemd-run logs then execs; systemctl logs,
    runs `stop_body`, exits `stop_rc`."""
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
    `fake_dir` (the no-real-binary property) and declared `_wf._REAL_RUN`, so
    the seam takes its real-launch path."""
    stops: list[list] = []

    def _run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["systemctl"]:
            found = shutil.which(cmd[0])
            assert found is None or Path(found).parent == fake_dir, cmd
            stops.append(list(cmd))
        return _TRUE_RUN(cmd, *a, **k)
    monkeypatch.setattr(subprocess, "run", _run)
    monkeypatch.setattr(_wf, "_REAL_RUN", _run)
    return stops


def _env(d: Path, *, bare: bool = False) -> dict:
    """The stage's env; `bare=True` hides every REAL binary."""
    return {"PATH": str(d) if bare else f"{d}:{os.environ['PATH']}"}


@pytest.fixture
def fakes(tmp_path, monkeypatch):
    return tmp_path if _fake_bin(tmp_path, monkeypatch) else None


def test_F1_normal_return_stops_the_scope_it_wrapped(fakes, monkeypatch):
    """A stage that backgrounds a child and exits 0 stops the unit the wrap
    USED (the one in the recorded argv) exactly once, via the tmp fake -- which
    also proves no real systemctl was reachable (asserted in `_stops`)."""
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
    """F2: wall-kill and exception paths stop the scope too, with the fake dir
    on PATH (round P2: built but never on PATH, so F2 hit the REAL systemctl)."""
    d = _fake_bin(tmp_path, monkeypatch)
    stops = _stops(monkeypatch, d)
    (tmp_path / "slow.sh").write_text("#!/bin/bash\nexec sleep 30\n")
    with pytest.raises(subprocess.TimeoutExpired):
        _wf._run_stage_proc(["bash", str(tmp_path / "slow.sh")], budget=0.2,
                            stage={"label": "verify", "max_extensions": 0},
                            spawn_env=_env(d), view=None, cap="64M", cfg={},
                            run_key="mur-39")
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
    """F5: TEMPLATE-MAX -- the line is in BOTH carriers: the generated
    workflow's stage prompts AND the script's own REVIEW/VERIFY templates."""
    want = ("never grep -r", "never `rg`", "never `find`")
    prompts = [s["prompt"] for s in
               json.loads((WF / "merge-up-review.json").read_text())["stages"]]
    assert len(prompts) >= 2
    for p in prompts + [(WF / "agi-merge-up-review.js").read_text()]:
        assert all(w in p.lower() for w in want), p[:60]


def test_F6_an_orphan_holding_the_stage_pipe_dies_with_the_scope(tmp_path,
                                                                monkeypatch):
    """F6 (round P1): a stage whose backgrounded child INHERITS its stdout pipe
    hung the wall path forever (kill kills the stage, the orphan holds the pipe,
    the bare `communicate()` never returns, so the `finally` that stops the unit
    never ran). Now: a wall kill inside a bound, and the ORPHAN DEAD -- a stop
    that was merely issued is not enough."""
    pids = tmp_path / "pids"
    d = _fake_bin(tmp_path, monkeypatch, stop_body=f"kill -9 $(cat {pids}) 2>/dev/null\n")
    stops = _stops(monkeypatch, d)
    (tmp_path / "stage.sh").write_text(
        f'#!/bin/bash\nsleep 300 &\necho $! >> "{pids}"\nexec sleep 300\n')
    t0 = time.monotonic()
    try:
        with pytest.raises(subprocess.TimeoutExpired):
            _wf._run_stage_proc(["bash", str(tmp_path / "stage.sh")], budget=0.5,
                                stage={"label": "verify", "max_extensions": 0},
                                spawn_env=_env(d), view=None, cap="64M", cfg={},
                                run_key="mur-39")
        assert time.monotonic() - t0 < 20, "the wall path hung again"
        assert stops == [["systemctl", "--user", "stop", _unit_of(tmp_path)]]
        stat = Path(f"/proc/{int(pids.read_text().split()[0])}/stat")
        with contextlib.suppress(OSError):        # already reaped == gone
            assert stat.read_text().split()[2] in "ZX"  # dying/zombie: no pipe
    finally:  # never leave a 300 s sleeper behind, pass or fail
        for p in (pids.read_text().split() if pids.exists() else []):
            with contextlib.suppress(OSError, ValueError):
                os.kill(int(p), 9)
