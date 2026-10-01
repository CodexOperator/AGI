"""F1-F11 of hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit: a stage
runs in a NAMED scope and stops it on EVERY exit path, so no orphan outlives it.
FAKES ONLY: `systemd-run`/`systemctl` are tmp scripts FIRST ON PATH, `_stops` proves
every stop resolved inside that dir and WRAPS the conftest guard (F10)."""
import contextlib, json, os, shutil, subprocess, sys, time  # noqa: E401
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import mem_cap  # noqa: E402
import workflow as _wf  # noqa: E402

#: the conftest import fence's run wrapper, NOT the stdlib original (`_stops` only)
_TRUE_RUN = subprocess.run
WF = Path(__file__).resolve().parents[1] / "workflows"


def _fake_bin(tmp_path, monkeypatch, *, stop_rc=0, no_systemctl=False,
              stop_body="") -> Path:
    """PATH-first fakes: systemd-run logs, execs; systemctl logs, REFUSES (rc 5, as the
    real one: a bare name is `X.service`) a stop not named `*.scope`, `stop_body`, `stop_rc`."""
    d = tmp_path / "bin"; d.mkdir()
    log = tmp_path / "calls.log"
    (d / "systemd-run").write_text(
        "#!/bin/bash\n" f'echo "run $*" >> "{log}"\n'
        'while [ "${1#-}" != "$1" ]; do shift; done\n'
        '[ "$1" = "--" ] && shift\n' 'exec "$@"\n')
    os.chmod(d / "systemd-run", 0o755)
    if not no_systemctl:
        (d / "systemctl").write_text(
            "#!/bin/bash\n" f'echo "ctl $*" >> "{log}"\n' '[[ "$3" == *.scope ]] || exit 5\n'
            f'{stop_body}exit {stop_rc}\n')
        os.chmod(d / "systemctl", 0o755)
    monkeypatch.setenv("PATH", f"{d}:{os.environ['PATH']}")
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    return d


def _unit_of(tmp_path: Path) -> str:
    """The `--unit=` the fake systemd-run ACTUALLY received."""
    run = next(ln for ln in (tmp_path / "calls.log").read_text().splitlines()
               if ln.startswith("run "))
    return next(a.split("=", 1)[1] for a in run.split() if a.startswith("--unit="))


def _stop_of(tmp_path: Path) -> list:
    """The ONE stop argv expected: the unit the wrap got, as `mem_cap.scope_unit` names it."""
    return ["systemctl", "--user", "stop", mem_cap.scope_unit(_unit_of(tmp_path))]


def _stops(monkeypatch, fake_dir: Path) -> list[list]:
    """Every `systemctl` argv, in order, PROVEN inside `fake_dir` (only that tmp
    script runs; all else hits the WRAPPED guard); declared `_wf._REAL_RUN`."""
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


def _env(d: Path) -> dict:
    """The stage's env: the tmp fakes FIRST on PATH, every process TAGGED."""
    return {"PATH": f"{d}:{os.environ['PATH']}", "AGI_ROW": f"{d}/"}


@pytest.fixture(autouse=True)
def _no_process_left(tmp_path):
    """h60c item 2: after EVERY row, no process a stage of it started (tagged by
    `_env`) is alive; a leftover is killed, then the row FAILS."""
    yield
    tag, left = f"AGI_ROW={tmp_path}/".encode(), []
    for _ in range(60):
        left = []
        for p in Path("/proc").glob("[0-9]*"):
            with contextlib.suppress(OSError):
                if tag in (p / "environ").read_bytes():
                    left.append(int(p.name))
        if not left:
            return
        time.sleep(0.05)
    for pid in left:
        with contextlib.suppress(OSError): os.kill(pid, 9)
    assert not left, f"processes left behind: {left}"


def _stage(args, d: Path, *, budget=1.0, label="verify"):
    """One capped, NAMED-scope stage launch through the seam under test."""
    return _wf._run_stage_proc(args, budget=budget,
                               stage={"label": label, "max_extensions": 0},
                               spawn_env=_env(d), view=None, cap="64M", cfg={},
                               run_key="mur-39")


def test_F1_normal_return_stops_the_scope_it_wrapped(tmp_path, monkeypatch):
    """A stage that backgrounds a child and exits 0 stops the unit the wrap
    USED exactly once; the fake stop kills that child, as a real scope stop does."""
    pids = tmp_path / "pids"
    d = _fake_bin(tmp_path, monkeypatch, stop_body=f"kill -9 $(cat {pids})\n")
    stops = _stops(monkeypatch, d)
    (tmp_path / "stage.sh").write_text(
        f"#!/bin/bash\nsleep 30 >/dev/null 2>&1 &\necho $! > {pids}\nexit 0\n")
    assert _stage(["bash", str(tmp_path / "stage.sh")], d, budget=10,
                  label="review").returncode == 0
    assert (unit := _unit_of(tmp_path)).startswith("agi-stage-mur-39_review-")
    assert stops == [_stop_of(tmp_path)] and unit + ".scope" in stops[0]   # never silence


def test_F2_wall_kill_and_exception_still_stop(tmp_path, monkeypatch):
    """F2: the wall-kill and the exception paths stop the scope too."""
    d = _fake_bin(tmp_path, monkeypatch)
    stops = _stops(monkeypatch, d)
    (tmp_path / "slow.sh").write_text("#!/bin/bash\nexec sleep 30\n")
    with pytest.raises(subprocess.TimeoutExpired):
        _stage(["bash", str(tmp_path / "slow.sh")], d, budget=0.2)
    assert stops == [_stop_of(tmp_path)]

    boom = tmp_path / "boom"; boom.mkdir()
    d2 = _fake_bin(boom, monkeypatch)
    stops2 = _stops(monkeypatch, d2)
    monkeypatch.setattr(mem_cap, "wrap_argv", lambda *a, **k:  # after the mint
                        (_ for _ in ()).throw(OSError("wrap failed")))
    with pytest.raises(OSError):
        _stage(["true"], d2, budget=5, label="review")
    assert len(stops2) == 1


def test_F3_a_failing_stop_is_one_stderr_line_and_never_a_raise(tmp_path,
        monkeypatch, capsys):
    """F3: a failing stop never raises; it is ONE stderr line naming the unit --
    the fake's rc 1, and no systemctl on PATH at all (the guard answers rc 1)."""
    script = tmp_path / "s.sh"; script.write_text("#!/bin/bash\nexit 3\n")
    for kwargs in (dict(stop_rc=1), dict(no_systemctl=True)):
        root = tmp_path / next(iter(kwargs)); root.mkdir()
        d = _fake_bin(root, monkeypatch, **kwargs)
        monkeypatch.setenv("PATH", str(d))   # the REAL systemctl unreachable
        seen = _stops(monkeypatch, d)
        r = _stage(["/bin/bash", str(script)], d, budget=10, label="review")
        assert (r.returncode, len(seen)) == (3, 1), kwargs   # attempted either way
        err = capsys.readouterr().err
        assert err.count("could not stop stage scope") == 1, kwargs
        assert _unit_of(root) in err, kwargs                # the line NAMES it


def test_F12_a_bare_name_stop_is_refused_and_the_orphan_survives(tmp_path, monkeypatch):
    """F12: a bare-name stop (what `scope_unit` replaced) is refused rc 5 by the
    manager: the stage's rc is unchanged and the orphan stays ALIVE (the old bug)."""
    pids = tmp_path / "pids"
    d = _fake_bin(tmp_path, monkeypatch, stop_body=f"kill -9 $(cat {pids})\n")
    seen = _stops(monkeypatch, d)
    monkeypatch.setattr(mem_cap, "scope_unit", lambda u: u)
    (tmp_path / "s.sh").write_text(
        f"#!/bin/bash\nsleep 30 >/dev/null 2>&1 &\necho $! > {pids}\nexit 3\n")
    assert _stage(["bash", str(tmp_path / "s.sh")], d, budget=10).returncode == 3
    assert seen == [["systemctl", "--user", "stop", _unit_of(tmp_path)]]
    os.kill(int(pids.read_text()), 9)   # still alive: raises if the stop had worked


def test_F13_an_already_collected_scope_rc5_stop_is_silent(tmp_path, monkeypatch, capsys):
    """F13: rc 5 (unit not loaded: the scope emptied and was collected) is a finished
    scope, not a failure: the `.scope` stop IS attempted, stderr stays empty."""
    d = _fake_bin(tmp_path, monkeypatch, stop_rc=5)
    seen = _stops(monkeypatch, d)
    assert _stage(["/bin/bash", "-c", "exit 3"], d, budget=10,
                  label="review").returncode == 3
    assert seen == [_stop_of(tmp_path)]
    assert "could not stop" not in capsys.readouterr().err


def test_F4_wrap_argv_without_a_unit_is_byte_unchanged(monkeypatch):
    """F4: the new `unit=` kwarg changes NO existing caller's argv."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    plain = mem_cap.wrap_argv(["pi", "-p"], "64M", {})
    assert "--unit=" not in " ".join(plain)
    named = mem_cap.wrap_argv(["pi", "-p"], "64M", {}, unit="agi-stage-x-1")
    assert named == plain[:4] + ["--unit=agi-stage-x-1"] + plain[4:]
    assert mem_cap.wrap_argv(["pi", "-p"], None) == ["pi", "-p"]


def test_F5_both_merge_up_review_prompts_forbid_a_recursive_grep():
    """F5: the no-grep line is in BOTH carriers: stage prompts and the .js templates."""
    want = ("never grep -r", "never `rg`", "never `find`")
    prompts = [s["prompt"] for s in
               json.loads((WF / "merge-up-review.json").read_text())["stages"]]
    assert len(prompts) >= 2
    for p in prompts + [(WF / "agi-merge-up-review.js").read_text()]:
        assert all(w in p.lower() for w in want), p[:60]


def _wait_for(pids: Path) -> None:
    for _ in range(200):
        time.sleep(0 if pids.exists() else 0.05)


def _orphan_dead(pids: Path) -> bool:
    """The recorded orphan is gone or a zombie (a missing pids file FAILS)."""
    _wait_for(pids)
    try:
        return Path(f"/proc/{pids.read_text().split()[0]}/stat").read_text().split()[2] in "ZX"
    except FileNotFoundError:
        return pids.exists()


def _held_pipe_stage(tmp_path, monkeypatch, tail="exec sleep 300\n", kills=True):
    """A stage backgrounds an orphan HOLDING its stdout pipe, records its pid, runs
    `tail`. `kills`: the fake stop kills the orphan as a REAL scope stop does (no race)."""
    monkeypatch.setattr(_wf, "_WALL_STOP_GRACE_S", 1.0)   # seconds, not 30
    pids = tmp_path / "pids"
    body = (f"for _ in $(seq 200); do [ -s {pids} ] && break; sleep 0.05; done\n"
            f"kill -9 $(cat {pids}) 2>/dev/null\n") if kills else ""
    d = _fake_bin(tmp_path, monkeypatch, stop_body=body)
    (tmp_path / "stage.sh").write_text(
        f'#!/bin/bash\nsleep 300 &\necho $! > "{pids}.w"; mv "{pids}.w" "{pids}"\n{tail}')
    return d, _stops(monkeypatch, d), pids, ["bash", str(tmp_path / "stage.sh")]


def test_F6_an_orphan_holding_the_stage_pipe_dies_with_the_scope(tmp_path, monkeypatch):
    """F6: an orphan INHERITING the stage's stdout pipe hung the wall path forever
    (the `finally` never ran). Now: a wall kill inside a bound, the ORPHAN DEAD."""
    d, stops, pids, argv = _held_pipe_stage(tmp_path, monkeypatch)
    t0 = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired):
        _stage(argv, d, budget=0.5)
    assert time.monotonic() - t0 < 20, "the wall path hung again"
    assert stops == [_stop_of(tmp_path)]
    assert _orphan_dead(pids)


@pytest.mark.parametrize("tail,rc", [("exit 7", 7), ("kill -9 $$", -9)])
def test_F7_a_stage_that_exited_with_a_held_pipe_returns_its_own_rc(
        tmp_path, monkeypatch, tail, rc):
    """item 2(a): the stage EXITED (rc 7) -- or was OOM-KILLED (-9, h60c item 3)
    -- with an orphan still holding its pipe: its own rc is the result, so a cap
    death is named 'memory-cap', never 'timed out' (what 96a7dd7173 raised)."""
    d, stops, pids, argv = _held_pipe_stage(tmp_path, monkeypatch, tail + "\n")
    r = _stage(argv, d, budget=2.0)
    assert (r.returncode, mem_cap.is_cap_death(r.returncode, "64M")) == (rc, rc < 0)
    assert stops == [_stop_of(tmp_path)]
    assert _orphan_dead(pids)


def test_F8_a_real_wall_timeout_raises_though_the_orphan_survives(tmp_path, monkeypatch):
    """item 2(b): a stage STILL RUNNING at the wall, orphan SURVIVING the stop, raises
    TimeoutExpired ('timed out'), never a bare -9 read as 'memory-cap' (96a7dd7173)."""
    d, stops, pids, argv = _held_pipe_stage(tmp_path, monkeypatch, kills=False)
    with pytest.raises(subprocess.TimeoutExpired):
        _stage(argv, d)
    assert stops == [_stop_of(tmp_path)]
    _wait_for(pids)
    os.kill(int(pids.read_text().split()[0]), 9)   # the survivor, by design


def test_F9_a_prlimit_fallback_launch_stops_nothing(tmp_path, monkeypatch):
    """item 2(c): the prlimit fallback has no scope, so NO stop is attempted."""
    d = _fake_bin(tmp_path, monkeypatch)
    stops = _stops(monkeypatch, d)
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    assert _stage(["/bin/bash", "-c", "exit 5"], d, budget=10,
                  label="review").returncode == 5
    assert stops == []


def test_F11_the_legacy_run_seam_keeps_the_anonymous_wrap_and_stops_nothing(monkeypatch):
    """C6: an injected-`subprocess.run`-only caller: ANONYMOUS wrap, launch only, NO stop."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    calls: list = []
    monkeypatch.setattr(subprocess, "run", lambda cmd, *a, **k: calls.append(cmd)
                        or subprocess.CompletedProcess(cmd, 0, "", ""))
    assert _stage(["true"], Path("/nonexistent"), label="review").returncode == 0
    assert [c[:3] for c in calls] == [["systemd-run", "--user", "--scope"]]
    assert not [a for a in calls[0] if a.startswith("--unit=")]


def test_F10_the_conftest_guard_still_stops_a_real_shaped_unit(tmp_path, monkeypatch, capsys):
    """item 4: a `systemctl --user stop` from this file with NO proven tmp fake
    is answered rc 1 by the conftest guard -- the sentinel is never written."""
    (tmp_path / "systemctl").write_text(f"#!/bin/sh\ntouch {tmp_path / 'sentinel'}\n")
    os.chmod(tmp_path / "systemctl", 0o755)
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    _wf._stop_stage_unit("agi-stage-mur-39_review-x")
    assert not (tmp_path / "sentinel").exists(), "the guard was bypassed"
    assert capsys.readouterr().err.count(
        "could not stop stage scope agi-stage-mur-39_review-x") == 1
