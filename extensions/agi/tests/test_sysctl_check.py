"""sysctl-check.sh (goal:g7.16.1.11.40.1.1 target 3a ii): the stopgap is bytes in /etc/sysctl.d AND live, else RED."""
import os
import shutil
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
    proc = tmp_path / "proc" / "sys" / "vm"; proc.mkdir(parents=True)
    (proc / "vfs_cache_pressure").write_text(T._vs()["VFS_CACHE_PRESSURE"] + "\n")
    exp = tmp_path / "expected"; exp.write_text(rendered)
    return {"PATH": os.environ["PATH"], "SYSCTL_D": str(d), "PROC_SYS": str(tmp_path / "proc" / "sys"), "EXPECTED": str(exp)}, d, exp


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
    (Path(env["PROC_SYS"]) / "vm" / "vfs_cache_pressure").write_text("100\n"); r = _run(env)                                                        # the file is there but sysctl --system never ran
    assert r.returncode == 1 and "says '200', the kernel has '100'" in r.stdout, r.stdout


def test_bytes_that_differ_from_the_render_are_red(box):
    env, d, _ = box
    (d / "60-agi-vm.conf").write_text((d / "60-agi-vm.conf").read_text().replace("= 200", "= 201"))
    (Path(env["PROC_SYS"]) / "vm" / "vfs_cache_pressure").write_text("201\n"); r = _run(env)
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


def test_a_path_without_usr_sbin_still_reads_the_live_value(box):
    env, d, _ = box                                                  # a post uid's PATH has no sbin dir: the check reads /proc/sys, it runs no sysctl binary
    path = ":".join(p for p in os.environ["PATH"].split(":") if "sbin" not in p)
    if shutil.which("sysctl", path=path):
        pytest.skip("sysctl is on a non-sbin PATH entry here")
    r = _run(env, PATH=path)
    assert r.returncode == 0 and "ok vm.vfs_cache_pressure" in r.stdout and "<unreadable>" not in r.stdout, r.stdout
