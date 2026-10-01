"""agi-run's strace line stops only on %file syscalls (--seccomp-bpf) and still sees a grandchild's open."""
import re, shlex, shutil, subprocess
from pathlib import Path
import pytest

WRAP = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry/engine-wrap.md"
pytestmark = pytest.mark.skipif(not shutil.which("strace"), reason="strace absent")


def _line():
    m = re.search(r"^exec strace .*$", WRAP.read_text(), re.M)
    assert m, "agi-run strace line not found"
    return m.group(0)


def test_f1_line_carries_seccomp_bpf():
    assert "--seccomp-bpf" in shlex.split(_line())


def test_f2_grandchild_open_in_stream(tmp_path):
    flags = []
    for t in shlex.split(_line())[1:]:  # strace flags up to the -o sink
        if t.startswith("-o"):
            break
        flags.append(t)
    target = tmp_path / "gc-target.txt"
    target.write_text("x")
    out = tmp_path / "trace"
    cmd = f'sh -c "cat {target} >/dev/null"; :'
    argv = ["strace", *flags, "-o", str(out), "sh", "-c", cmd]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    hits = [l for l in out.read_text().splitlines() if re.search(r"open(at)?\(", l) and str(target) in l]
    assert hits, out.read_text()
