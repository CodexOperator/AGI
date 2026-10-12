"""sysctl-check.sh (goal:g7.16.1.11.40.1.1 target 3a ii): the stopgap is bytes in /etc/sysctl.d AND live, else RED."""
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "extensions" / "agi" / "guard" / "sysctl-check.sh"
sys.path.insert(0, str(REPO / "extensions" / "agi" / "bin"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture
def box(tmp_path):
    import test_boxkit_templates as T
    d = tmp_path / "sysctl.d"; d.mkdir()
    rendered = T.R.rendered(T.BY_NAME["agi-vm-sysctl"], T._vs())
    (d / "60-agi-vm.conf").write_text(rendered)
    stub = tmp_path / "sysctl"
    stub.write_text('#!/bin/sh\n[ "$1" = -n ] || exit 2\ncase "$2" in vm.vfs_cache_pressure) echo "$LIVE_VFS";; *) exit 1;; esac\n'); stub.chmod(stub.stat().st_mode | stat.S_IXUSR)
    exp = tmp_path / "expected"; exp.write_text(rendered)
    return {"PATH": os.environ["PATH"], "SYSCTL_D": str(d), "SYSCTL": str(stub), "EXPECTED": str(exp), "LIVE_VFS": T._vs()["VFS_CACHE_PRESSURE"]}, d, exp


def _run(env, **over):
    return subprocess.run(["sh", str(SCRIPT)], env={**env, **over}, capture_output=True, text=True, timeout=60)


def test_the_installed_bytes_equal_the_render_and_the_kernel_has_the_value(box):
    env, *_ = box
    r = _run(env)
    assert r.returncode == 0 and "ok bytes:" in r.stdout and "ok vm.vfs_cache_pressure = 200 (live)" in r.stdout, r.stdout


def test_a_dropped_file_is_red_not_silence(box):
    env, d, _ = box
    (d / "60-agi-vm.conf").unlink()                                                     # a box move that left /etc/sysctl.d behind
    r = _run(env)
    assert r.returncode == 1 and "is missing" in r.stdout, r.stdout


def test_a_live_value_that_differs_is_red_and_names_both(box):
    env, *_ = box
    r = _run(env, LIVE_VFS="100")                                                        # the file is there but sysctl --system never ran
    assert r.returncode == 1 and "says '200', the kernel has '100'" in r.stdout, r.stdout


def test_bytes_that_differ_from_the_render_are_red(box):
    env, d, _ = box
    (d / "60-agi-vm.conf").write_text((d / "60-agi-vm.conf").read_text().replace("= 200", "= 201"))
    r = _run(env, LIVE_VFS="201")
    assert r.returncode == 1 and "RED bytes:" in r.stdout, r.stdout


def test_an_empty_conf_and_an_unreadable_key_are_red(box):
    env, d, _ = box
    (d / "60-agi-vm.conf").write_text("# only a comment\n")
    assert _run(env, EXPECTED="").returncode == 1
    (d / "60-agi-vm.conf").write_text("vm.no_such_key = 5\n")
    r = _run(env, EXPECTED="")
    assert r.returncode == 1 and "<unreadable>" in r.stdout, r.stdout


def test_an_unset_expected_says_the_bytes_were_not_checked_and_is_not_a_full_pass(box):
    env, d, _ = box
    for over in ({"EXPECTED": ""}, {}):
        e = {k: v for k, v in env.items() if k != "EXPECTED"}; e.update(over)
        r = _run(e)
        assert r.returncode == 0 and "bytes: not checked (EXPECTED unset)" in r.stdout and "equals the rendered row" not in r.stdout, r.stdout
    r = _run(env)                                                    # EXPECTED named: the line is absent and the bytes are compared
    assert "not checked" not in r.stdout and "equals the rendered row" in r.stdout, r.stdout
