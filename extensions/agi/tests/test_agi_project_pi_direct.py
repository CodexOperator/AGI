"""G7.4: strace -b execve detaches on the harness pid's 2nd exec, so a pi row (env-shebang) must start with the interpreter."""
import os, re, shutil, subprocess, tempfile, time
import pytest
from tests import test_project_agi_box as base

ROW = '  - {"name": "t1", "engine": {"v": 4, "harness": "%s", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "harness": "%s", "box": "%%s"}\n'
needs_pty = pytest.mark.skipif(not (shutil.which("strace") and shutil.which("script")), reason="strace/script absent")


def h_of(tmp_path, monkeypatch, harness, path=None):
    monkeypatch.setattr(base, "ROW", ROW % (harness, harness))
    return base.project(tmp_path, path=path).split('Environment="H=')[1].split('" O=')[0]


def _bin(tmp_path, name, pi):
    d = tmp_path / name
    d.mkdir()
    if pi:
        (d / "pi").write_text("#!/bin/sh\n"), (d / "pi").chmod(0o755)
    return d


@pytest.fixture
def unit_path():
    try:
        m = re.search(r"(?m)^Environment=PATH=(\S+)", (base.WT / base.GEO / "engine-root.md").read_text())
    except OSError:
        pytest.skip("engine-root.md is missing: the unit's home moved")
    if not m:
        pytest.skip("engine-root.md carries no Environment=PATH= line: the geometry's unit PATH moved")
    return m[1]


def test_pi_row_is_node_exact_dir_pi_first_on_unit_path(tmp_path, monkeypatch, unit_path):
    a, b, c = _bin(tmp_path, "a", 0), _bin(tmp_path, "b", 1), _bin(tmp_path, "c", 1)
    h = h_of(tmp_path, monkeypatch, "pi-free", f"{tmp_path}/%i/bin:{a}:{b}:{c}")  # hermetic: an absent %i dir + a pi-less dir skipped; first holder wins
    assert h.startswith(f"node {b}/pi --provider openrouter --model m --thinking high "), h


UNIT = "/^### agi-post" + "@\\.service /,/^##/{/^~~~/,/^~~~/{//!p}}"  # the s function's own range


def _sect(path, expr=UNIT):
    return subprocess.run(["sed", "-n", expr, str(path)], capture_output=True, text=True, check=True).stdout


def _unit_and_section(tmp_path, engine_text=None):
    base.project(tmp_path, engine_text)  # base.ROW: a claude-only box, so no pi is needed
    return (tmp_path / "out" / ("agi-post" + "@.service")).read_text(), _sect(tmp_path / "repo" / base.GEO / "engine-root.md")


def test_projected_unit_is_the_section_byte_for_byte(tmp_path):
    unit, section = _unit_and_section(tmp_path)
    assert section and unit == section


def test_agi_project_reads_the_unit_section_once():
    assert _sect(base.WT / base.GEO / "engine.md", base.SECT).count("s agi-post" + "@.service") == 1


def _refuses(tmp_path, monkeypatch, extra="", harness="pi-free"):
    """row(s) with no pi on PATH, a seeded wants link: exit 3, no h.conf, the link survives."""
    monkeypatch.setattr(base, "ROW", ROW % ((harness,) * 2) + extra)
    w = tmp_path / "out" / "multi-user.target.wants"
    link = w / ("agi-post" + "@old.service")
    w.mkdir(parents=True), link.symlink_to("../agi-post" + "@.service")
    with pytest.raises(subprocess.CalledProcessError) as e:
        base.project(tmp_path, path=str(_bin(tmp_path, "a", 0)))
    assert e.value.returncode == 3 and not list((tmp_path / "out").glob("*/h.conf")) and os.path.islink(link)


def test_no_pi_on_unit_path_refuses_before_any_h_conf_or_wants_strip(tmp_path, monkeypatch):
    _refuses(tmp_path, monkeypatch)


def test_pi_row_then_malformed_row_refuses_rc3_no_h_conf(tmp_path, monkeypatch):
    _refuses(tmp_path, monkeypatch, "  - {oops\n")


def test_empty_unit_section_refuses_before_wants_strip(tmp_path, monkeypatch):
    fake = tmp_path / "wt"
    (fake / base.GEO).mkdir(parents=True)
    for f in (base.WT / base.GEO).glob("engine*.md"):  # a claude-only box: only the empty unit, not a pi row, can refuse
        (fake / base.GEO / f.name).write_text(re.sub(r"(?s)(### agi-post@\.service[^\n]*\n~~~ini\n).*?(~~~\n)", r"\1\2", f.read_text()))
    assert _sect(base.WT / base.GEO / "engine-root.md") and not _sect(fake / base.GEO / "engine-root.md")  # the section was real, and is now empty
    monkeypatch.setattr(base, "WT", fake)
    _refuses(tmp_path, monkeypatch, harness="claude-code")


def test_mixed_box_pi_and_claude_rows_both_project(tmp_path, monkeypatch):
    d = _bin(tmp_path, "a", 1)
    monkeypatch.setattr(base, "ROW", ROW % (("pi-free",) * 2) + ((ROW % (("claude-code",) * 2)) % "local-town").replace('"t1"', '"t2"'))
    pi = base.project(tmp_path, path=str(d))
    cl = (tmp_path / "out" / ("agi-post" + "@t2.service.d") / "h.conf").read_text()
    assert f'H=node {d}/pi --provider openrouter --model m --thinking high ' in pi
    assert 'H=claude --remote-control t2 --model m --effort high --permission-mode bypassPermissions" ' in cl


def test_claude_only_box_projects_without_pi_byte_identical(tmp_path, monkeypatch):
    monkeypatch.setattr(base, "ROW", ROW % (("claude-code",) * 2))
    (x, y), nopi = (tmp_path / "x", tmp_path / "y"), _bin(tmp_path, "n", 0)
    x.mkdir(), y.mkdir()
    assert base.project(x, path=str(nopi)).replace(str(x), "") == base.project(y).replace(str(y), "")


def test_claude_row_unchanged(tmp_path, monkeypatch):
    assert h_of(tmp_path, monkeypatch, "claude-code").startswith("claude --remote-control t1 --model m --effort high --permission-mode bypassPermissions")


def _wall(tmp_path, *argv):
    """Wall time of `agi-run's strace under a pty, stdin a never-EOF fifo; the `-o '|cmd'` sink is what makes strace exit at the detach (`-o FILE` waits)."""
    fifo = f"{tmp_path}/in{len(os.listdir(tmp_path))}"
    os.mkfifo(fifo)
    fd = os.open(fifo, os.O_RDWR)
    t = time.time()
    subprocess.run(["timeout", "4", "script", "-qfec", " ".join(["strace -qqf -b execve -e%file -o'|cat >/dev/null'", *map(str, argv)]), "/dev/null"], stdin=fd, capture_output=True)
    os.close(fd)
    return time.time() - t


@needs_pty
def test_env_shebang_under_b_execve_ends_at_once_interpreter_direct_stays(tmp_path):
    s = tmp_path / "pi"
    s.write_text("#!/usr/bin/env sh\nsleep 3\n"), s.chmod(0o755)
    fast, kept = _wall(tmp_path, s), _wall(tmp_path, "sh", s)
    assert fast < 1.5 <= 2 <= kept, (fast, kept)
