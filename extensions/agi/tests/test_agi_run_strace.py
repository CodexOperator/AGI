"""agi-run's strace line detaches at each child exec (-b execve): the harness's own opens are traced, exec'd compute children run untraced."""
import re, shlex, shutil, subprocess
from pathlib import Path
import pytest

WRAP = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry/engine-wrap.md"
needs_strace = pytest.mark.skipif(not shutil.which("strace"), reason="strace absent")  # only the rows that run strace; the F1 text guard always runs


def _line():
    m = re.search(r"^exec strace .*$", WRAP.read_text(), re.M)
    assert m, "agi-run strace line not found"
    return m.group(0)


def _stream(tmp_path):
    """Run the line's flags on a command that opens file A itself, then forks+execs `cat B`; return (A, B, stream)."""
    flags = []
    for t in shlex.split(_line())[1:]:  # strace flags up to the -o sink
        if t.startswith("-o"):
            break
        flags.append(t)
    a, b = tmp_path / "direct-a.txt", tmp_path / "exec-child-b.txt"
    a.write_text("x"), b.write_text("x")
    out = tmp_path / "trace"
    cmd = f": <{a}; cat {b} >/dev/null; :"  # the trailing ':' keeps sh forking cat, not exec'ing it
    r = subprocess.run(["strace", *flags, "-o", str(out), "sh", "-c", cmd], capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    return a, b, out.read_text()


def _opened(path, stream):
    return [l for l in stream.splitlines() if re.search(r"open(at)?\(", l) and str(path) in l]


def test_f1_line_detaches_at_exec_not_seccomp():
    t = shlex.split(_line())
    assert "-b execve" in " ".join(t) and "--seccomp-bpf" not in t


@needs_strace
def test_f2_direct_command_open_in_stream(tmp_path):
    a, _, s = _stream(tmp_path)
    assert _opened(a, s), s


@needs_strace
def test_execd_grandchild_open_not_in_stream(tmp_path):  # the designed loss of -b execve
    a, b, s = _stream(tmp_path)
    assert _opened(a, s) and not _opened(b, s), s
