"""success_metrics.py — shared, not forked (hypothesis:l4-residue-that-is-
recorded-is-still-residue, SITE A).

`record_path` is "The ONE recorded place for a season's success metrics"
(docstring), and the write-log it reads is the same shared room. The
falsifier is PATH EQUALITY: a seat's graph root and the main checkout's graph
root must resolve the SAME success-metrics record path — not merely that each
read succeeds. A seat in a linked git worktree must read/write the season's
durable record on the MAIN checkout, never a per-worktree fork.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import success_metrics  # noqa: E402


def _git(cwd: Path, *args: str):
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)


def _make_project_repo(tmp_path: Path) -> Path:
    """A real git repo with a committed `.agi/` graph dir, on `master`."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    graph = repo / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (graph / "nodes").mkdir()
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir")
    return repo


def test_record_path_is_the_same_room_for_seat_and_main(tmp_path):
    """FALSIFIER (SITE A): a seat's groot and the main groot resolve the SAME
    success-metrics record path — path EQUALITY. Under the pre-fix plain
    `Path(root) / "sessions"` join these diverged; through
    `locations.shared_sessions_dir` they meet on the main checkout."""
    repo = _make_project_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    wt_graph = (wt / ".agi").resolve()       # the fork a seat edits
    main_graph = (repo / ".agi").resolve()   # the one shared body
    assert wt_graph != main_graph            # the fork is real

    from locations import find_project_root  # noqa: E402

    assert find_project_root(wt) == wt_graph
    assert find_project_root(repo) == main_graph

    season = 3
    seat_path = success_metrics.record_path(wt_graph, season)
    main_path = success_metrics.record_path(main_graph, season)
    assert seat_path == main_path            # THE falsifier: one room, one path
    # The unified path is the MAIN checkout's room, not the seat's fork.
    assert str(seat_path) == str(main_graph / "sessions" / f"success-metrics-{season}.json")
    assert seat_path != wt_graph / "sessions" / f"success-metrics-{season}.json"

# --- goal:g7.16.1.11.46.9: the p1 segment reads the REPO whether it is given the repo or the `.agi` graph dir ------

REPO_ROOT = Path(__file__).resolve().parents[3]
P1_CFG = json.loads((REPO_ROOT / ".agi" / "config.json").read_text())
P1_RESULTS = {"base": P1_CFG["p1"]["base"], "arms": [
    {"arm": "glm", "model": "z-ai/glm-5.3-flash", "kids": [
        {"leaf": P1_CFG["p1"]["leaves"][0], "landed": True, "usd": 0.1, "secs": 100.0, "red": False, "reviewed": "gate-1"}]}]}


def _p1_repo(tmp_path: Path, *, config=True, p1=True, results=False) -> Path:
    repo = tmp_path / "repo"
    (repo / ".agi").mkdir(parents=True)
    if config:
        cfg = dict(P1_CFG) if p1 else {k: v for k, v in P1_CFG.items() if k != "p1"}
        (repo / ".agi" / "config.json").write_text(json.dumps(cfg))
    if results is not False:
        path = repo / P1_CFG["p1"]["results"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(results if isinstance(results, str) else json.dumps(results))
    return repo


def _stub_line(monkeypatch):
    """make_line without the minute-long metrics.py run and without a real graph."""
    monkeypatch.setattr(success_metrics, "_run_metrics_once", lambda root: ({}, "stub"))
    monkeypatch.setattr(success_metrics, "SOURCE_FUNCS", [])


def test_no_results_file_means_no_p1_segment_from_either_root(tmp_path, monkeypatch):
    _stub_line(monkeypatch)
    repo = _p1_repo(tmp_path)
    for root in (repo, repo / ".agi"):
        line = success_metrics.make_line(root)
        assert "p1:" not in line and "No such file" not in line, root
        assert success_metrics.p1_segment(root) == ""


def test_a_committed_results_file_renders_the_segment_from_either_root(tmp_path, monkeypatch):
    _stub_line(monkeypatch)
    repo = _p1_repo(tmp_path, results=P1_RESULTS)
    want = "| p1: z-ai/glm-5.3-flash $/landed=0.1000 s/landed=100 red=0/5 ran=1/5 rss=unmeasured"
    for root in (repo, repo / ".agi"):
        # a board line's segments are counted by their KEY and content, never by position (council 04:23Z)
        line = success_metrics.make_line(root)
        assert line.count("| p1:") == 1 and want in line, root


def test_the_cli_root_is_the_graph_dir_and_the_line_has_no_false_red(tmp_path, monkeypatch, capsys):
    """The live red: main() resolves the root with find_project_root(), which returns `<repo>/.agi`."""
    _stub_line(monkeypatch)
    repo = _p1_repo(tmp_path)
    monkeypatch.chdir(repo)
    assert success_metrics.main(["--line"]) == 0
    out = capsys.readouterr().out
    assert "UNMEASURED(results unreadable" not in out and "p1:" not in out
    (repo / P1_CFG["p1"]["results"]).parent.mkdir(parents=True)
    (repo / P1_CFG["p1"]["results"]).write_text(json.dumps(P1_RESULTS))
    assert success_metrics.main(["--line"]) == 0
    assert "| p1: z-ai/glm-5.3-flash" in capsys.readouterr().out


def test_a_project_without_a_p1_cell_or_without_a_config_has_no_segment(tmp_path, monkeypatch):
    _stub_line(monkeypatch)
    for kw in (dict(p1=False), dict(config=False)):
        repo = _p1_repo(tmp_path / ("a" if "p1" in kw else "b"), **kw)
        for root in (repo, repo / ".agi"):
            assert success_metrics.p1_segment(root) == "", (kw, root)


def test_a_results_file_that_exists_but_is_broken_is_named_not_dropped(tmp_path, monkeypatch):
    _stub_line(monkeypatch)
    repo = _p1_repo(tmp_path, results="{broken")
    for root in (repo, repo / ".agi"):
        seg = success_metrics.p1_segment(root)
        assert seg.startswith("| p1: UNMEASURED(results unreadable"), root
        assert "/" not in seg.split("(", 1)[1], "no path may ride the board line"


# --- the council's final form: _reason is a fixed code (A2), the CLI is a SUBPROCESS row (A3) ----------------------

def test_reason_is_a_fixed_code_never_exception_text():
    r = success_metrics._reason
    assert r(OSError(2, "No such file or directory", "/data/work/secret/x.json")) == "FileNotFoundError 2"
    assert r(PermissionError(13, "denied", "/data/work/y")) == "PermissionError 13"
    assert r(ValueError("/abs/path/in/the/message")) == "ValueError"
    assert r(SystemExit(3)) == "SystemExit 3" and r(SystemExit("/a/b")) == "SystemExit"
    assert r("/a/b/c") == "unknown" and r(None) == "unknown"
    for e in (OSError(2, "m", "/p/q"), KeyError("/k/l"), RuntimeError("see /var/lib/x")):
        assert "/" not in r(e)


def test_every_unmeasured_in_the_line_is_free_of_a_box_path(tmp_path, monkeypatch):
    """Mutant: an exception whose message holds an absolute path must give a metrics_line with no '/'."""
    monkeypatch.setattr(success_metrics, "_run_metrics_once", lambda root: ({}, None))
    boom = lambda root: (_ for _ in ()).throw(OSError(2, "No such file or directory", "/data/work/secret/x.json"))
    monkeypatch.setattr(success_metrics, "SOURCE_FUNCS", [("src_a", boom), ("src_b", lambda root: (_ for _ in ()).throw(SystemExit("/var/lib/agi/x")))])
    repo = _p1_repo(tmp_path, results="{broken")
    for root in (repo, repo / ".agi"):
        line = success_metrics.make_line(root)
        assert "src_a=UNMEASURED(source failed: FileNotFoundError 2)" in line, line
        assert "src_b=UNMEASURED(source failed: SystemExit)" in line
        assert "| p1: UNMEASURED(results unreadable: P1Refused)" in line
        assert "/" not in line, line


def test_a_metrics_py_that_cannot_run_names_the_class_not_the_path(monkeypatch, tmp_path):
    def nope(*a, **k):
        raise OSError(2, "No such file or directory", "/usr/bin/python3-not-here")
    monkeypatch.setattr(success_metrics.subprocess, "run", nope)
    found, dead = success_metrics._run_metrics_once(tmp_path)
    assert dead == "metrics.py unrunnable FileNotFoundError 2" and "/" not in dead


def _scratch_project(tmp_path: Path, results=None) -> Path:
    repo = tmp_path / "scratch"
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text(json.dumps(P1_CFG))
    if results is not None:
        path = repo / P1_CFG["p1"]["results"]
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(results))
    return repo


def _cli_line(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(BIN_DIR / "success_metrics.py"), "--line"], cwd=repo,
                          capture_output=True, text=True, timeout=300)


def test_the_cli_as_a_subprocess_has_no_p1_text_without_a_results_file(tmp_path):
    """The live red, end to end: the real entry point, its own root resolution (find_project_root -> the .agi dir)."""
    r = _cli_line(_scratch_project(tmp_path))
    assert r.returncode == 0, r.stderr
    assert "p1:" not in r.stdout and "No such file" not in r.stdout and len(r.stdout.strip().splitlines()) == 1


def test_the_cli_as_a_subprocess_renders_the_segment_once_results_exist(tmp_path):
    r = _cli_line(_scratch_project(tmp_path, P1_RESULTS))
    assert r.returncode == 0, r.stderr
    out = r.stdout.strip()
    assert out.count("| p1:") == 1 and "| p1: z-ai/glm-5.3-flash $/landed=0.1000 s/landed=100 red=0/5 ran=1/5 rss=unmeasured" in out, out
