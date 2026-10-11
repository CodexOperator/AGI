"""goal:g7.16.1.11.13.1 re-cut (SM's 21:4xZ return A1-A3, DG1's rulings): the
residues of the two flip successors.

A1  `evidence_gate.py enforce` takes ONE non-blocking exclusive flock inside the
    verb (cron AND the manual verb share it): a second run prints
    `[busy] evidence enforce already running`, exits 0, demotes nothing;
    `--dry-run` takes no lock; a lock that cannot be taken fails closed.
A2  `grid.grid_retired()` in a project WITHOUT a crons node is SILENT; an INVALID
    node is still NAMED; the other readers (`crons.load_crons_node`) still raise
    for a missing file.
A3  the manual verb's docstring says what it does: it defers, and has no override.

Fixture roots only, never the live tree. Bare subprocesses with the harness env
stripped, like test_grid_evidence_gate_defer.py.
"""

import fcntl
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
EG = str(BIN / "evidence_gate.py")
MINT = "e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1"
STRIP = {
    "AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT",
    "AUTORESEARCH_TREE_PROJECT_ROOT", "PROJECT_ROOT", "AGI_TIER",
    "GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0",
}
BUSY = "[busy] evidence enforce already running"

sys.path.insert(0, str(BIN))


def _env():
    return {k: v for k, v in os.environ.items() if k not in STRIP}


def _build(root: Path) -> Path:
    """A legacy fixture root (graph root = root): one unevidenced `proved` experiment node."""
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    (root / "agi-tree.config.json").write_text("{}")
    d = root / "nodes" / "experiment"
    d.mkdir(parents=True)
    node = d / "h.md"
    node.write_text(
        f'---\nid: "experiment:h"\nmint_id: {MINT}\ntype: experiment\n'
        f"verdict: proved\n---\n\nbody\n")
    return node


def _enforce(root: Path, *extra):
    return subprocess.run([sys.executable, EG, "enforce", "--root", str(root), *extra],
                          env=_env(), capture_output=True, text=True, timeout=120)


def _lock_file(root: Path) -> Path:
    return root / "sessions" / ".evidence-enforce.lock"


def _hold(root: Path):
    """Hold the enforce lock the way a running enforce does (the test process is the foreign holder)."""
    p = _lock_file(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = open(p, "a")
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return fd


# ==== A1 ====


def test_a1_a_held_enforce_lock_prints_one_busy_line_demotes_nothing_and_the_next_run_demotes(tmp_path):
    node = _build(tmp_path)
    before = node.read_bytes()
    fd = _hold(tmp_path)
    try:
        r = _enforce(tmp_path)
        assert r.returncode == 0, (r.returncode, r.stderr[-300:])
        assert r.stdout.splitlines() == [BUSY], r.stdout
        assert node.read_bytes() == before, "a node was rewritten while another enforce held the lock"
    finally:
        fd.close()
    r2 = _enforce(tmp_path)
    assert r2.returncode == 0 and BUSY not in r2.stdout, (r2.stdout, r2.stderr[-300:])
    assert "demoted_from: proved" in node.read_text(), "the run after the holder left must demote"
    assert _lock_file(tmp_path).exists(), "the lock file is left behind (harmless): the flock, not the file, is the lock"


def test_a1b_two_enforces_at_once_exactly_one_runs_and_the_other_says_busy(tmp_path):
    """A REAL overlap: process A is slowed inside enforce_on_disk (after it took the lock); B starts once A holds it."""
    node = _build(tmp_path)
    slow = (
        "import sys,time;sys.path.insert(0,%r);import evidence_gate as g;o=g.enforce_on_disk;"
        "g.enforce_on_disk=lambda *a,**k:(time.sleep(3),o(*a,**k))[1];"
        "sys.exit(g.main(['enforce','--root',%r]))" % (str(BIN), str(tmp_path)))
    a = subprocess.Popen([sys.executable, "-c", slow], env=_env(), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True)
    try:
        deadline = time.time() + 30
        held = False
        while time.time() < deadline and not held:       # wait until A really holds the flock
            time.sleep(0.1)
            if not _lock_file(tmp_path).exists():
                continue
            probe = open(_lock_file(tmp_path), "a")
            try:
                fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(probe, fcntl.LOCK_UN)
            except BlockingIOError:
                held = True
            finally:
                probe.close()
        assert held, "process A never took the enforce lock"
        b = _enforce(tmp_path)
        out_a, err_a = a.communicate(timeout=60)
    finally:
        if a.poll() is None:
            a.kill()
            a.wait()
    assert b.returncode == 0 and b.stdout.splitlines() == [BUSY], (b.returncode, b.stdout, b.stderr[-200:])
    assert a.returncode == 0 and "evidence-gate enforce:" in out_a, (a.returncode, out_a, err_a[-300:])
    runs = [x for x in (out_a, b.stdout) if "evidence-gate enforce:" in x]
    busies = [x for x in (out_a, b.stdout) if BUSY in x]
    assert len(runs) == 1 and len(busies) == 1, (out_a, b.stdout)
    assert "demoted_from: proved" in node.read_text()


def test_a1c_dry_run_takes_no_lock_and_is_not_blocked_by_one(tmp_path):
    node = _build(tmp_path)
    before = node.read_bytes()
    fd = _hold(tmp_path)
    try:
        r = _enforce(tmp_path, "--dry-run")
    finally:
        fd.close()
    assert r.returncode == 0 and BUSY not in r.stdout, (r.stdout, r.stderr[-300:])
    assert "would demote" in r.stdout, r.stdout
    assert node.read_bytes() == before, "--dry-run must write nothing"


def test_a1d_a_lock_that_cannot_be_taken_fails_closed_naming_the_path(tmp_path):
    node = _build(tmp_path)
    before = node.read_bytes()
    (tmp_path / "sessions").write_text("a file where the lock directory should be\n")
    r = _enforce(tmp_path)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr[-300:])
    assert ".evidence-enforce.lock" in r.stderr and "cannot take its lock" in r.stderr, r.stderr
    assert node.read_bytes() == before, "nothing may be demoted when the lock cannot be taken"


def test_a1e_the_lock_file_is_in_the_git_ignored_sessions_dir_of_the_real_tree():
    r = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", ".agi/sessions/.evidence-enforce.lock"])
    assert r.returncode == 0, "the enforce lock file would show up as an untracked file in MAIN"


# ==== A2 ====


def _project(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text("{}")
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    return repo / ".agi"


def test_a2_grid_retired_with_no_crons_node_is_false_and_silent(tmp_path, capsys):
    import grid
    graph = _project(tmp_path)
    assert not (graph / "nodes" / ".geometry" / "crons.md").exists()
    capsys.readouterr()
    assert grid.grid_retired(graph) is False
    got = capsys.readouterr()
    assert got.err == "" and got.out == "", (got.err, got.out)


def test_a2b_an_invalid_crons_node_is_still_named_once_per_call(tmp_path, capsys):
    import grid
    graph = _project(tmp_path)
    (graph / "nodes" / ".geometry" / "crons.md").write_text("no frontmatter at all\n")
    capsys.readouterr()
    assert grid.grid_retired(graph) is False
    err = capsys.readouterr().err
    lines = err.splitlines()
    assert len(lines) == 1 and lines[0].startswith("grid: crons node invalid (") and lines[0].endswith("); grid NOT retired"), err


def test_a2c_the_other_readers_still_refuse_a_missing_node(tmp_path):
    """Control: A2 changed the CALL SITE, not crons.py: load_crons_node still raises CronsError for a missing file."""
    import crons
    graph = _project(tmp_path)
    with pytest.raises(crons.CronsError, match="missing node file"):
        crons.load_crons_node(graph)


# ==== A3 ====


def test_a3_the_manual_verbs_docstring_says_it_defers_and_has_no_override():
    import evidence_gate
    doc = evidence_gate.main.__doc__
    assert "demote now" not in doc, "the old promise ('or to demote now') is false: the verb defers"
    assert "NO override" in doc and "defers" in doc.lower(), doc
    assert "evidence gate deferred: suite lock held by pid" in doc, "the docstring must name the deferral line"
    assert BUSY in doc, "the docstring must name the busy line"
