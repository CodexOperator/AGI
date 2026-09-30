"""F1-F5 of hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit.

A workflow stage runs in a NAMED scope and stops it on EVERY exit path, so
no orphan (a repo-wide grep the stage left behind) outlives its stage.

FAKES ONLY: `systemd-run` / `systemctl` are tmp scripts on PATH which append
their argv to a log; the real user manager, a real unit and the live RAM dir
are never touched (the fake systemd-run `exec`s the stage, so no bus is
contacted at all). The suite's own autouse systemd guard (conftest: no test
stops a REAL unit) is stood down for the FAKE by routing `subprocess.run`
through the true implementation captured at import, before any fixture
patched it -- the only thing that ever reaches it is a tmp script.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import mem_cap  # noqa: E402
import workflow as _wf  # noqa: E402

#: the TRUE subprocess.run, captured before conftest's autouse guard patches
#: the module attribute (that guard refuses `systemctl stop` outright, which
#: would hide the very call under test).
_TRUE_RUN = subprocess.run


def _fake_bin(tmp_path: Path, *, stop_rc: int = 0,
              no_systemctl: bool = False) -> Path:
    """A tmp dir holding a fake systemd-run (logs, then execs the stage
    after the `--`) and a fake systemctl (logs, then exits `stop_rc`)."""
    d = tmp_path / "bin"
    d.mkdir()
    log = tmp_path / "calls.log"
    (d / "systemd-run").write_text(
        "#!/bin/bash\n"
        f'echo "run $*" >> "{log}"\n'
        'while [ "${1#-}" != "$1" ]; do shift; done\n'
        '[ "$1" = "--" ] && shift\n'
        'exec "$@"\n')
    os.chmod(d / "systemd-run", 0o755)
    if not no_systemctl:
        (d / "systemctl").write_text(
            "#!/bin/bash\n"
            f'echo "ctl $*" >> "{log}"\n'
            f'exit {stop_rc}\n')
        os.chmod(d / "systemctl", 0o755)
    return d


def _calls(tmp_path: Path) -> list[str]:
    f = tmp_path / "calls.log"
    return f.read_text().splitlines() if f.exists() else []


def _stops(monkeypatch) -> list[list]:
    """Every `systemctl` argv the stage seam actually issued, in order.

    The recorder is also declared to be the engine's OWN `_REAL_RUN`, so the
    seam takes its real-launch path (a merely-substituted `subprocess.run`
    reads as the legacy dispatch seam, which mints no unit at all)."""
    stops: list[list] = []

    def _run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["systemctl"]:
            stops.append(list(cmd))
        return _TRUE_RUN(cmd, *a, **k)
    monkeypatch.setattr(subprocess, "run", _run)
    monkeypatch.setattr(_wf, "_REAL_RUN", _run)
    return stops


def _env(d: Path, *, bare: bool = False) -> dict:
    """The stage's env. `bare=True` hides every REAL binary (the fake dir
    only), which is how the 'no systemctl at all' case is spelled."""
    return {"PATH": str(d) if bare else f"{d}:{os.environ['PATH']}"}


@pytest.fixture
def fakes(tmp_path, monkeypatch):
    d = _fake_bin(tmp_path)
    monkeypatch.setenv("PATH", f"{d}:{os.environ['PATH']}")
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    return tmp_path


def test_F1_normal_return_stops_the_scope_it_wrapped(fakes, monkeypatch):
    """A stage that backgrounds a child and exits 0 still leaves NO live
    process in its scope: the unit the wrap used is stopped exactly once."""
    stops = _stops(monkeypatch)
    script = fakes / "stage.sh"
    script.write_text("#!/bin/bash\nsleep 30 >/dev/null 2>&1 &\nexit 0\n")
    r = _wf._run_stage_proc(["bash", str(script)], budget=10,
                            stage={"label": "review"},
                            spawn_env=_env(fakes / "bin"), view=None,
                            cap="64M", cfg={}, run_key="mur-39")
    assert r.returncode == 0
    ran = [ln for ln in _calls(fakes) if ln.startswith("run ")]
    unit = next(a.split("=", 1)[1] for a in ran[0].split()
                if a.startswith("--unit="))
    assert unit.startswith("agi-stage-mur-39_review-")
    assert stops == [["systemctl", "--user", "stop", unit]]


def test_F2_wall_kill_and_exception_still_stop(tmp_path, monkeypatch):
    """F2: the wall-kill path and an exception path stop the scope too."""
    d = _fake_bin(tmp_path)
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    stops = _stops(monkeypatch)
    script = tmp_path / "slow.sh"
    script.write_text("#!/bin/bash\nexec sleep 30\n")
    with pytest.raises(subprocess.TimeoutExpired):
        _wf._run_stage_proc(["bash", str(script)], budget=0.2,
                            stage={"label": "verify", "max_extensions": 0},
                            spawn_env=_env(d), view=None, cap="64M", cfg={},
                            run_key="mur-39")
    assert len(stops) == 1
    assert stops[0][1:] == ["--user", "stop", stops[0][3]] and stops[0][3]

    boom = tmp_path / "boom"
    boom.mkdir()
    d2 = _fake_bin(boom)
    stops2 = _stops(monkeypatch)
    # The exception path on a REAL launch: the wrap itself blows up AFTER
    # the unit was minted -- exactly the shape a partially-built scope has.
    def _wrap(*a, **k):
        raise OSError("wrap failed")
    monkeypatch.setattr(mem_cap, "wrap_argv", _wrap)
    with pytest.raises(OSError):
        _wf._run_stage_proc(["true"], budget=5,
                            stage={"label": "review"},
                            spawn_env=_env(d2), view=None, cap="64M", cfg={},
                            run_key="mur-39")
    assert len(stops2) == 1


def test_F3_a_failing_stop_never_raises_and_costs_one_line(
        tmp_path, monkeypatch, capsys):
    """F3: a stop that fails changes nothing and never raises -- a non-zero
    stop is silent, a stop that cannot RUN is exactly one stderr line."""
    script = tmp_path / "s.sh"
    script.write_text("#!/bin/bash\nexit 3\n")
    for kwargs, err_lines in ((dict(stop_rc=1), 0),
                              (dict(no_systemctl=True), 1)):
        root = tmp_path / f"case{sorted(kwargs)}{kwargs.get('stop_rc', '')}"
        root.mkdir()
        d = _fake_bin(root, **kwargs)
        bare = "no_systemctl" in kwargs
        monkeypatch.setenv("PATH", str(d) if bare
                           else f"{d}:{os.environ['PATH']}")
        monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
        seen = _stops(monkeypatch)
        r = _wf._run_stage_proc(["/bin/bash", str(script)], budget=10,
                                stage={"label": "review"},
                                spawn_env=_env(d, bare=bare),
                                view=None, cap="64M", cfg={}, run_key="mur-39")
        assert r.returncode == 3, kwargs
        assert len(seen) == 1, kwargs        # the stop is ATTEMPTED either way
        assert capsys.readouterr().err.count(
            "could not stop stage scope") == err_lines, kwargs


def test_F4_wrap_argv_without_a_unit_is_byte_unchanged(monkeypatch):
    """F4: the new `unit=` kwarg changes NO existing caller's argv."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    plain = mem_cap.wrap_argv(["pi", "-p"], "64M", {})
    assert "--unit=" not in " ".join(plain)
    named = mem_cap.wrap_argv(["pi", "-p"], "64M", {}, unit="agi-stage-x-1")
    assert named == plain[:4] + ["--unit=agi-stage-x-1"] + plain[4:]
    assert mem_cap.wrap_argv(["pi", "-p"], None) == ["pi", "-p"]


def test_F5_both_merge_up_review_prompts_forbid_a_recursive_grep():
    """F5: TEMPLATE-MAX -- both stage prompts carry the line."""
    mf = Path(__file__).resolve().parents[1] / "workflows" / "merge-up-review.json"
    d = json.loads(mf.read_text())
    prompts = [s["prompt"] for s in d["stages"]]
    assert len(prompts) >= 2
    for p in prompts:
        low = p.lower()
        assert ("never grep -r" in low and "never `rg`" in low
                and "never `find`" in low)