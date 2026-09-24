import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import durable_launch


def test_popen_fallback_is_not_creation(tmp_path):
    proc, created = durable_launch.open_round(
        [sys.executable, "-c", "pass"], tmp_path / "round.log",
        cwd=str(tmp_path), env=None, name="agi-fixed",
        wrap_argv=lambda argv: argv)
    try:
        assert created is False
        assert proc.wait(timeout=10) == 0
    finally:
        if proc.poll() is None:
            proc.kill(); proc.wait()


def test_adapter_receives_stable_name_and_provenance(tmp_path):
    seen = {}
    class Proc:
        pid = 123
    def launcher(argv, log, *, cwd, env, name):
        seen.update(name=name, argv=argv, cwd=cwd)
        return Proc(), False
    old = durable_launch.LAUNCHER
    durable_launch.LAUNCHER = launcher
    try:
        proc, created = durable_launch.open_round(
            ["agent"], tmp_path / "round.log", cwd=str(tmp_path), env={},
            name="agi-abc", wrap_argv=lambda argv: argv)
    finally:
        durable_launch.LAUNCHER = old
    assert created is False
    assert proc.pid == 123
    assert seen["name"] == "agi-abc"
