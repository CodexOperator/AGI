"""Tests for the L4-tier full-suite gate (hypothesis:l4-full-suite-tier-gate).

The testable claim: a conftest.py in extensions/agi/tests/ REFUSES a bare
whole-directory pytest run when AGI_TIER=kid, names a one-line reason with the
variable and the fix, and is invisible at every other tier (and when unset).

These tests exercise BOTH branches directly:
  - decision unit test: _is_bare_directory_run() on the three invocation shapes
  - hook integration test: subprocess runs of the real conftest under
    AGI_TIER=kid (bare dir refused, named file / -k passed) and AGI_TIER unset
    / parent (bare dir passed unchanged).
"""
import copy
import os
import subprocess
import sys

from extensions.agi.tests import conftest as gate

CONFTEST = os.path.join(os.path.dirname(__file__), "conftest.py")

TEST_SRC = 'def test_ok():\n    assert True\n'


class _Opt:
    def __init__(self, keyword=""):
        self.keyword = keyword
        self.kw = None


class _Cfg:
    def __init__(self, args, keyword=""):
        self.args = list(args)
        self.option = _Opt(keyword)


def test_decision_bare_directory_kid_refuses():
    assert gate._is_bare_directory_run(_Cfg(["extensions/agi/tests/"])) is True
    assert gate._is_bare_directory_run(_Cfg([])) is True


def test_decision_named_file_passes():
    assert gate._is_bare_directory_run(
        _Cfg(["extensions/agi/tests/test_send.py"])
    ) is False


def test_decision_k_filter_passes_even_on_directory():
    assert gate._is_bare_directory_run(
        _Cfg(["extensions/agi/tests/"], keyword="send")
    ) is False


def _run_pytest(path_args, env_extra, named_file=False):
    """Run pytest against a throwaway dir that symlinks the real conftest."""
    import tempfile

    d = tempfile.mkdtemp()
    try:
        os.symlink(CONFTEST, os.path.join(d, "conftest.py"))
        with open(os.path.join(d, "test_a.py"), "w") as f:
            f.write(TEST_SRC)
        target = os.path.join(d, "test_a.py") if named_file else d
        env = dict(os.environ)
        if env_extra is None:
            env.pop("AGI_TIER", None)
        else:
            env["AGI_TIER"] = env_extra
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", target, "-q"],
            capture_output=True, text=True, env=env,
        )
        return proc.returncode, proc.stderr
    finally:
        import shutil
        shutil.rmtree(d)


def test_hook_bare_directory_kid_refused():
    code, err = _run_pytest([], "kid")
    assert code == 4  # pytest.UsageError
    assert "AGI_TIER=kid" in err
    assert "specific test file or a -k filter" in err


def test_hook_named_file_kid_passes():
    code, _ = _run_pytest([], "kid", named_file=True)
    assert code == 0


def test_hook_unset_bare_dir_invisible():
    code, _ = _run_pytest([], None)
    assert code == 0


def test_hook_parent_bare_dir_invisible():
    code, _ = _run_pytest([], "parent")
    assert code == 0
