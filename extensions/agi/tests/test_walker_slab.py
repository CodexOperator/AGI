"""walker-slab.sh (goal:g7.16.1.11.40.1.1 target 3c): one read-only row of the per-walker table."""
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "extensions" / "agi" / "guard" / "walker-slab.sh"
MIB = 1 << 20


def _env(tmp_path):
    cg = tmp_path / "cg"; cg.mkdir()
    (cg / "memory.stat").write_text("anon 1\nslab %d\n" % (100 * MIB))
    (tmp_path / "dentry").write_text("1000\t900\t45\t0\t0\t0\n"); (tmp_path / "inode").write_text("500\t10\n")
    return {"PATH": os.environ["PATH"], "CG": str(cg), "INTERVAL": "0.1", "DENTRY": str(tmp_path / "dentry"), "INODE": str(tmp_path / "inode")}


def _run(env, *argv):
    return subprocess.run(["sh", str(SCRIPT), *argv], env=env, capture_output=True, text=True, timeout=60)


def test_the_row_carries_the_slab_before_the_peak_and_after_and_the_delta_to_the_peak(tmp_path):
    env = _env(tmp_path)
    cmd = ("printf 'slab %d\\n' %d > $CG/memory.stat; sleep 0.8; printf 'slab %d\\n' %d > $CG/memory.stat; "
           "printf '2500\\t0\\n' > %s; sleep 0.4") % (300 * MIB, 300 * MIB, 150 * MIB, 150 * MIB, tmp_path / "dentry")
    r = _run(env, "demo-walker", "sh", "-c", cmd)
    assert r.returncode == 0 and r.stderr == "", r
    f = r.stdout.rstrip("\n").split("\t")
    assert f[0] == "demo-walker" and float(f[1]) >= 1.0, f
    assert f[2:6] == ["100", "300", "150", "200"], f                                          # before, PEAK (polled mid-run), after, peak - before
    assert f[6] == "1000" and f[7] == "2500" and f[8] == f[9] == "500" and f[10] == "0", f   # dentries before/after, inodes, rc


def test_it_runs_the_command_unchanged_reports_its_rc_and_writes_nothing_but_its_row(tmp_path):
    env = _env(tmp_path)
    before = sorted(p.name for p in tmp_path.iterdir())
    r = _run(env, "fails", "sh", "-c", "exit 7")
    assert r.stdout.rstrip("\n").split("\t")[-1] == "7" and r.returncode == 0
    assert sorted(p.name for p in tmp_path.iterdir()) == before                                # no file written, memory.stat untouched
    assert "slab %d" % (100 * MIB) in (tmp_path / "cg" / "memory.stat").read_text()
    assert _run(env, "x").returncode == 2                                                       # no command = usage, rc 2


def test_it_never_drops_caches_or_needs_root():
    text = SCRIPT.read_text()
    assert "drop_caches" not in text.replace("drop_caches` (", "") .split("# Env:")[1] and "sudo" not in text and "runuser" not in text
