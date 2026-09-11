"""Tests for the synthetic-root in-repo basetemp guard
(hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures).

The testable claim: the Prime's cross-worktree race advice runs a round's
tests with `--basetemp` under its own .agi/sessions/. That is safe ONLY for
tests whose fixtures do NOT build a synthetic `.agi/` ROOT. A synthetic-root
test builds groot = tmp_path/".agi" and resolves it through `locations.*`;
under an in-repo basetemp, tmp_path lands INSIDE the real repo, so locations
resolves the REAL graph instead of the synthetic root and the test silently
runs against the wrong tree (measured: 4 of 8 test_verification_seat_model.py
failing; all 8 passing on the default out-of-repo basetemp).

The guard in conftest.py REFUSES an in-repo `--basetemp` ONLY when a named
module is a synthetic-root module (a module-NAME ALLOWLIST, the sanctioned
detection). The critical near-miss it must NOT become: "refuse every in-repo
basetemp", which would re-break the Prime's race fix. So a non-synthetic
module must pass through unchanged even under an in-repo basetemp.

Decision (unit) + hook (integration) both branches, mirroring
test_tier_gate.py's split.
"""
import importlib.util
import os
import subprocess
import sys

import pytest

CONFTEST = os.path.join(os.path.dirname(__file__), "conftest.py")

_spec = importlib.util.spec_from_file_location("_agi_basetemp_conftest", CONFTEST)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

# The in-repo basetemp the Prime's advice points at. Resolved lazily so the
# test works from any cwd.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
IN_REPO_BT = os.path.join(
    REPO_ROOT, ".agi", "sessions", "pytest-basetemp")

SYNTH_MODULE = "test_verification_seat_model.py"
PLAIN_MODULE = "test_send.py"


class _Opt:
    def __init__(self, basetemp=None):
        self.basetemp = basetemp


class _Cfg:
    def __init__(self, args, basetemp=None):
        self.args = list(args)
        self.option = _Opt(basetemp)


def test_in_repo_basetemp_detected():
    assert gate._in_repo_basetemp(_Cfg(["x"], IN_REPO_BT)) is True


def test_default_basetemp_not_in_repo():
    assert gate._in_repo_basetemp(_Cfg(["x"], None)) is False


def test_out_of_repo_basetemp_not_in_repo(tmp_path):
    assert gate._in_repo_basetemp(
        _Cfg(["x"], str(tmp_path / "out-of-repo"))) is False


def test_refuse_synthetic_root_module_with_in_repo_basetemp():
    cfg = _Cfg(["extensions/agi/tests/" + SYNTH_MODULE], IN_REPO_BT)
    try:
        gate._refuse_in_repo_basetemp_on_synthetic_root(cfg)
    except pytest.UsageError as exc:
        assert "synthetic" in str(exc)
        assert "in-repo basetemp" in str(exc)
        return
    raise AssertionError("in-repo basetemp + synthetic-root module was NOT refused")


def test_plain_module_not_refused_even_with_in_repo_basetemp():
    """The near-miss rejection: a non-synthetic module must pass through
    unchanged under an in-repo basetemp, or we re-break the Prime's race fix."""
    cfg = _Cfg(["extensions/agi/tests/" + PLAIN_MODULE], IN_REPO_BT)
    gate._refuse_in_repo_basetemp_on_synthetic_root(cfg)  # must not raise


def test_synthetic_root_module_with_default_basetemp_not_refused():
    cfg = _Cfg(["extensions/agi/tests/" + SYNTH_MODULE], None)
    gate._refuse_in_repo_basetemp_on_synthetic_root(cfg)  # must not raise


def test_hook_refuses_in_repo_basetemp_on_synthetic_root():
    """Integration: the REAL conftest, run inside the real worktree, refuses
    the advised --basetemp for the measured synthetic-root module, naming a
    reason. This is the falsifier-control turned mechanical guard: where the
    advice previously made 4 of 8 tests fail, it now refuses up front."""
    import pytest as _pytest
    env = dict(os.environ)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest",
         "extensions/agi/tests/" + SYNTH_MODULE, "-q",
         "--basetemp", IN_REPO_BT],
        capture_output=True, text=True, env=env,
        cwd=REPO_ROOT, timeout=300)
    err = proc.stdout + proc.stderr
    assert proc.returncode == 4, err  # pytest.UsageError
    assert "synthetic" in err
    assert "in-repo basetemp" in err


def test_hook_default_basetemp_on_synthetic_root_passes():
    """Integration: the same synthetic-root module with the DEFAULT basetemp
    (None) runs and PASSES — the guard must not fire when the invocation did
    not take the advised flag at all."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest",
         "extensions/agi/tests/" + SYNTH_MODULE, "-q"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=300)
    err = proc.stdout + proc.stderr
    assert proc.returncode == 0, err
    assert "passed" in proc.stdout