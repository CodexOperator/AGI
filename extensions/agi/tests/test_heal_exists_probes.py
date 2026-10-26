"""goal:g7.16.1.11.45.5 -- heal.py's `Path.exists()` probes never raise on EACCES and never read
"cannot see" as "gone".

On Python 3.12 `Path.exists()` RAISES PermissionError behind an unreadable (0o000) parent, while
`os.path.exists()` returns False there. Three probes were left raw by goal:g7.16.1.11.45.4:

  1. `_sweep_orphan`      the gitfile's `gitdir:` target       -> `[sweep] <wt> gitdir unreadable (EACCES): kept`
  2. the RAM-link branch  `(ent / "locked")`                    -> outcome `left (lock state unread)`
  3. `_heal`              the hung agent's `log_file`           -> `(log unread (EACCES))` in the healer's context

R1 one tri-state probe (`heal._exists3`: True / False / None) at all three; R2 never `os.path.exists`
and never `except OSError: False`; R3 a mutant per site, each RED on the bytes (a False wrap prints a
FALSE `orphan: gitdir gone` line and loses the kept-line: a mutant that only asks "was the worktree
removed" can never go red, because today the orphan branch REFUSES); R4 a census of every `.exists()`
call in heal.py against an allowlist, so a new raw probe reads RED.

The rows need a non-root uid (root stats a 0o000 dir). The skip says so; `pytest -rs` prints it.
"""
from __future__ import annotations

import ast
import errno
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
import locations  # noqa: E402

NOT_ROOT = pytest.mark.skipif(
    os.geteuid() == 0,
    reason="root can stat a 0o000 dir: the falsifier needs a non-root uid (uid %d)" % os.geteuid())


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.setattr(heal, "_sweep_pressure_ok", lambda root: (True, "test"))
    heal._SWEEP_SKIP.clear()
    heal._SWEEP_ORPHAN.clear()
    yield
    heal._SWEEP_SKIP.clear()
    heal._SWEEP_ORPHAN.clear()


def _sh(*args: str) -> str:
    out = subprocess.run(list(args), capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"{args}: {out.stderr}")
    return out.stdout


@pytest.fixture
def scratch(tmp_path: Path, monkeypatch):
    """A real MAIN with one merged-clean kid worktree (the sibling the pass must still sweep)."""
    repo = tmp_path / "repo"
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({"reaper": {"worktree_grace_min": 0}}))
    _sh("git", "init", "-b", "season/s2", str(repo))
    _sh("git", "-C", str(repo), "config", "user.email", "t@example.com")
    _sh("git", "-C", str(repo), "config", "user.name", "t")
    (repo / ".gitignore").write_text(".agi/sessions/\n.agi/worktrees/\n")
    (repo / "base.txt").write_text("base\n")
    _sh("git", "-C", str(repo), "add", "-A")
    _sh("git", "-C", str(repo), "commit", "-q", "-m", "init")
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph / "reaper.log"))
    return {"repo": repo, "graph": graph, "tmp": tmp_path, "log": graph / "reaper.log"}


def _kid(scratch, name="a00-zdead1"):
    wt = scratch["graph"] / "worktrees" / name
    _sh("git", "-C", str(scratch["repo"]), "worktree", "add", "-b", f"loop/{name}@2", str(wt),
        "season/s2")
    return wt


def _text(scratch) -> str:
    return scratch["log"].read_text() if scratch["log"].exists() else ""


def _registered(repo: Path) -> set[str]:
    adm = Path(_sh("git", "-C", str(repo), "rev-parse", "--path-format=absolute",
                   "--git-common-dir").strip()) / "worktrees"
    return {p.name for p in adm.iterdir()} if adm.is_dir() else set()


class closed_dir:
    """A directory that is 0o000 for the duration of the block (restored on exit)."""

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.path.chmod(0o000)
        return self.path

    def __exit__(self, *exc):
        self.path.chmod(0o700)


# ---- the probe itself (R1/R2) ---------------------------------------------------------------------
@NOT_ROOT
def test_the_probe_is_tri_state_and_never_raises(tmp_path):
    here = tmp_path / "here"
    here.write_text("x")
    closed = tmp_path / "closed"
    (closed / "inner").mkdir(parents=True)
    with closed_dir(closed):
        assert heal._exists3(here) is True
        assert heal._exists3(tmp_path / "nope") is False
        assert heal._exists3(closed / "inner") is None, "unreadable is UNKNOWN, not gone"
        assert heal._errno_name(closed / "inner") == "EACCES"
        with pytest.raises(PermissionError):
            (closed / "inner").exists()          # the premise: the stdlib probe raises here
        assert os.path.exists(closed / "inner") is False, "the premise: os.path reads it as gone (R2)"


# ---- site 1: the orphan probe -----------------------------------------------------------------------
def _gitfile_tree(scratch, name: str, gitdir: Path) -> Path:
    wt = scratch["graph"] / "worktrees" / name
    wt.mkdir(parents=True)
    (wt / ".git").write_text(f"gitdir: {gitdir}\n")
    (wt / "stray.txt").write_text("bytes\n")
    return wt


def _orphan_pass(scratch, monkeypatch, probe=None):
    """Three trees in ONE pass: an orphan whose gitdir sits under a 0o000 parent (unknown), an orphan whose
    gitdir is provably gone, and a merged-clean kid. `probe` swaps `heal._exists3` (the mutants)."""
    closed = scratch["tmp"] / "closed"
    (closed / "inner").mkdir(parents=True)
    unk = _gitfile_tree(scratch, "a00-aorphe", closed / "inner" / "gd-eacces")
    gone = _gitfile_tree(scratch, "a00-borphg", scratch["tmp"] / "nowhere" / "gd-gone")
    kid = _kid(scratch)
    if probe is not None:
        monkeypatch.setattr(heal, "_exists3", probe)
    exc = None
    res = None
    with closed_dir(closed):
        try:
            res = heal._sweep_finished_worktrees(scratch["graph"])
        except Exception as e:  # noqa: BLE001 -- the mutant raises; the verdict reads it
            exc = e
    return {"exc": exc, "res": res, "unk": unk, "gone": gone, "kid": kid, "text": _text(scratch)}


def _orphan_failures(o) -> list[str]:
    """Every way the orphan-site contract can be broken; empty = the contract holds."""
    bad = []
    if o["exc"] is not None:
        bad.append(f"the pass raised {type(o['exc']).__name__}")
        return bad
    t = o["text"]
    if "[sweep] a00-aorphe gitdir unreadable (EACCES): kept" not in t:
        bad.append("no kept-line for the unreadable gitdir")
    if "refused a00-aorphe: orphan: gitdir gone" in t:
        bad.append("a FALSE `orphan: gitdir gone` line for a gitdir that is only unreadable")
    if not any("refused a00-aorphe: git rev-parse HEAD failed" in l for l in t.splitlines()):
        bad.append("the unreadable orphan did not fall to the existing rev-parse refusal")
    if "refused a00-borphg: orphan: gitdir gone" not in t:
        bad.append("the provably-gone orphan lost its DG2.C1 refusal")
    if o["kid"].exists():
        bad.append("the sibling merged-clean kid after the unreadable orphan was not swept")
    if not (o["unk"] / "stray.txt").exists():
        bad.append("the unreadable orphan's bytes were touched")
    return bad


def _bare(site):
    """A mutant probe: the raw `Path.exists()` at ONE site (a path whose name contains `site`)."""
    real = heal._exists3
    return lambda p: p.exists() if site in p.name else real(p)


def _false_wrap(site):
    """A mutant probe: `except OSError: False` at ONE site -- reads "cannot see" as "gone" (R2)."""
    real = heal._exists3

    def probe(p):
        if site in p.name:
            try:
                return p.exists()
            except OSError:
                return False
        return real(p)
    return probe


@NOT_ROOT
def test_orphan_unreadable_gitdir_is_kept_named_and_the_pass_completes(scratch, monkeypatch):
    assert _orphan_failures(_orphan_pass(scratch, monkeypatch)) == []


@NOT_ROOT
def test_mutant_orphan_probe_bare_exists_kills_the_pass_and_is_red(scratch, monkeypatch):
    bad = _orphan_failures(_orphan_pass(scratch, monkeypatch, _bare("gd-eacces")))
    assert any("raised PermissionError" in b for b in bad), bad


@NOT_ROOT
def test_mutant_orphan_probe_false_wrap_prints_a_false_orphan_line_and_is_red(scratch, monkeypatch):
    """Today the orphan branch REFUSES, so the False wrap deletes nothing: the worktree-still-there check
    stays green. The RED is the FALSE `orphan: gitdir gone` line plus the missing kept-line."""
    bad = _orphan_failures(_orphan_pass(scratch, monkeypatch, _false_wrap("gd-eacces")))
    assert any("FALSE `orphan: gitdir gone`" in b for b in bad), bad
    assert any("no kept-line" in b for b in bad), bad
    assert not any("bytes were touched" in b for b in bad), "the vacuous check would have stayed green"


# ---- site 2: the RAM-link lock file -------------------------------------------------------------------
def _ram(scratch, name):
    ram = scratch["tmp"] / "ram" / name
    _sh("git", "-C", str(scratch["repo"]), "worktree", "add", "-b", f"loop/{name}", str(ram), "season/s2")
    (scratch["graph"] / "worktrees").mkdir(parents=True, exist_ok=True)
    (scratch["graph"] / "worktrees" / name).symlink_to(ram)
    return ram


def _locked_pass(scratch, monkeypatch, probe=None):
    """Two gone RAM links in ONE pass. The first one's admin entry sits behind a 0o000 parent (the lookup is
    stubbed to hand it back; the drop is stubbed to fail), so its `locked` stat is EACCES."""
    _ram(scratch, "a00-ram1")
    _ram(scratch, "a00-ram2")
    shutil.rmtree(scratch["tmp"] / "ram")
    closed = scratch["tmp"] / "closedadm"
    (closed / "adm").mkdir(parents=True)
    real_entry = locations.worktree_admin_entry
    real_drop = locations.drop_dead_worktree_admin
    monkeypatch.setattr(locations, "worktree_admin_entry",
                        lambda mc, target: closed / "adm" if Path(target).name == "a00-ram1"
                        else real_entry(mc, target))
    monkeypatch.setattr(locations, "drop_dead_worktree_admin",
                        lambda mc, target: False if Path(target).name == "a00-ram1"
                        else real_drop(mc, target))
    if probe is not None:
        monkeypatch.setattr(heal, "_exists3", probe)
    exc = res = None
    with closed_dir(closed):
        try:
            res = heal._sweep_finished_worktrees(scratch["graph"])
        except Exception as e:  # noqa: BLE001
            exc = e
    return {"exc": exc, "res": res, "text": _text(scratch)}


def _locked_failures(o) -> list[str]:
    bad = []
    if o["exc"] is not None:
        return [f"the pass raised {type(o['exc']).__name__}"]
    t = o["text"]
    if "[sweep] unlinked a00-ram1: RAM target gone; left (lock state unread)" not in t:
        bad.append("no `left (lock state unread)` outcome for the unreadable lock state")
    if "unlinked a00-ram1: RAM target gone; left (not provably gone, or drop failed)" in t:
        bad.append("the unread lock state was reported as a plain failed drop")
    if "[sweep] unlinked a00-ram2: RAM target gone; registration dropped" not in t:
        bad.append("the SECOND link was not swept after the unread one")
    return bad


@NOT_ROOT
def test_locked_unreadable_is_named_and_the_next_link_is_still_swept(scratch, monkeypatch):
    assert _locked_failures(_locked_pass(scratch, monkeypatch)) == []
    assert "a00-ram2" not in _registered(scratch["repo"])


@NOT_ROOT
def test_mutant_locked_probe_bare_exists_kills_the_pass_and_is_red(scratch, monkeypatch):
    bad = _locked_failures(_locked_pass(scratch, monkeypatch, _bare("locked")))
    assert any("raised PermissionError" in b for b in bad), bad


@NOT_ROOT
def test_mutant_locked_probe_false_wrap_reads_unread_as_a_plain_drop_failure_and_is_red(scratch, monkeypatch):
    bad = _locked_failures(_locked_pass(scratch, monkeypatch, _false_wrap("locked")))
    assert any("plain failed drop" in b for b in bad) and any("lock state unread" in b for b in bad), bad


# ---- site 3: the healer's log ---------------------------------------------------------------------------
class _FakeProc:
    pid = 4242


def _heal_pass(tmp_path, monkeypatch, log_file: Path, probe=None, closed: Path | None = None):
    graph = tmp_path / "repo" / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage", "spawn": {"memory_max": "1G"}}))
    it = graph / "sessions" / "iter-L1.07"
    (it / "agent-h").mkdir(parents=True, exist_ok=True)
    rec = {"id": "agent-h", "status": "running", "pid": 0, "log_file": str(log_file), "iter_n": "C"}
    (it / "agent-h" / "agent.json").write_text(json.dumps(rec))
    spawned: list = []
    monkeypatch.setattr(heal.subprocess, "Popen", lambda argv, **k: spawned.append(list(argv)) or _FakeProc())
    monkeypatch.setattr(heal.time, "sleep", lambda *_a, **_k: None)
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "1")
    if probe is not None:
        monkeypatch.setattr(heal, "_exists3", probe)
    exc = None
    try:
        if closed is not None:
            with closed_dir(closed):
                heal._heal(graph, "L1.07", "agent-h", rec)
        else:
            heal._heal(graph, "L1.07", "agent-h", rec)
    except Exception as e:  # noqa: BLE001
        exc = e
    ctxs = list((it / "agent-h").glob("heal-*/context.md"))
    return {"exc": exc, "spawned": spawned, "ctx": ctxs[0].read_text() if ctxs else ""}


def _closed_log(tmp_path) -> tuple[Path, Path]:
    closed = tmp_path / "closedlog"
    (closed / "d").mkdir(parents=True)
    (closed / "d" / "output.log").write_text("stuck\n")
    return closed, closed / "d" / "output.log"


def _log_failures(o) -> list[str]:
    if o["exc"] is not None:
        return [f"the healer raised {type(o['exc']).__name__}"]
    bad = []
    if len(o["spawned"]) != 1:
        bad.append("the healer was not spawned")
    if "(log unread (EACCES))" not in o["ctx"]:
        bad.append("the healer's record has no `log unread (EACCES)` tail")
    return bad


@NOT_ROOT
def test_unreadable_log_gives_a_named_unread_tail_and_the_healer_still_spawns(tmp_path, monkeypatch):
    closed, log = _closed_log(tmp_path)
    assert _log_failures(_heal_pass(tmp_path, monkeypatch, log, closed=closed)) == []


@NOT_ROOT
def test_mutant_log_probe_bare_exists_raises_out_of_the_healer_and_is_red(tmp_path, monkeypatch):
    closed, log = _closed_log(tmp_path)
    bad = _log_failures(_heal_pass(tmp_path, monkeypatch, log, probe=_bare("output.log"), closed=closed))
    assert any("raised PermissionError" in b for b in bad), bad


@NOT_ROOT
def test_mutant_log_probe_false_wrap_gives_an_empty_tail_and_is_red(tmp_path, monkeypatch):
    closed, log = _closed_log(tmp_path)
    bad = _log_failures(_heal_pass(tmp_path, monkeypatch, log, probe=_false_wrap("output.log"), closed=closed))
    assert any("no `log unread" in b for b in bad), bad


def test_an_absent_log_keeps_the_empty_tail_and_a_present_one_its_tail(tmp_path, monkeypatch):
    absent = _heal_pass(tmp_path / "a", monkeypatch, tmp_path / "a" / "no" / "output.log")
    assert absent["exc"] is None and len(absent["spawned"]) == 1
    assert "log unread" not in absent["ctx"] and "```\n\n```" in absent["ctx"]
    here = tmp_path / "b" / "output.log"
    here.parent.mkdir(parents=True)
    here.write_text("stuck here\n")
    present = _heal_pass(tmp_path / "b", monkeypatch, here)
    assert "stuck here" in present["ctx"]


# ---- the other routed probes: unknown is never gone --------------------------------------------------------
@NOT_ROOT
def test_an_unreadable_session_dir_is_not_home_and_an_unreadable_link_is_not_created(tmp_path, monkeypatch):
    closed = tmp_path / "closed"
    (closed / "iter-9").mkdir(parents=True)
    target = tmp_path / "main" / "iter-9"
    target.mkdir(parents=True)
    with closed_dir(closed):
        assert heal._sweep_iter_home(closed / "iter-9", target) is False, "unreadable source != home (fail closed)"
        monkeypatch.setattr(locations, "guard_cell", lambda root, name: str(tmp_path / "cold"))
        assert heal._sweep_cold_link(tmp_path, closed, "iter-9") is None, "an entry we cannot see is not created over"


@NOT_ROOT
def test_the_window_seams_answer_unknown_not_a_raise_on_an_unreadable_file(tmp_path):
    closed = tmp_path / "closed"
    closed.mkdir()
    w = closed / "windows"
    w.write_text("@1 main\n")
    with closed_dir(closed):
        assert heal._all_windows(str(w)) == []
        assert heal._pane_pid_of("@1", str(w)) == 0
        assert heal._pane_pid_map(str(w)) == {}


# ---- R4: the census of every `.exists()` call in heal.py ---------------------------------------------------------
#: (enclosing function, stripped source line) -> why this raw probe is safe. Everything else is routed
#: through `_exists3`. A NEW raw probe, or a stale entry, reads RED.
ALLOW = {
    ("_exists3", "return p.exists()"):
        "the probe itself: it is inside the try that turns every OSError into None",
    ("_main_heal", "if not manifest_path.exists():"):
        "a CLI path that must fail LOUD: the heal command's own iteration manifest, same uid; a raise is the "
        "right answer, a quiet 'no manifest' would hide a broken session dir",
    ("_main_heal", "if not ap_file.exists():"):
        "the same CLI loop over the manifest's own agent dirs (same uid, written by the driver this iteration); "
        "a raise surfaces a broken session dir loudly, and skipping would let the loop declare the round finished",
    ("_read_seat_log_tail", "if p.exists():"):
        "inside `try: ... except Exception: continue` -- a raise is swallowed to the next candidate and never "
        "read as 'absent'",
}


def _exists_calls(src: str) -> set[tuple[str, str]]:
    tree = ast.parse(src)
    lines = src.splitlines()
    out: set[tuple[str, str]] = set()

    class V(ast.NodeVisitor):
        def __init__(self):
            self.stack: list[str] = []

        def visit_FunctionDef(self, n):
            self.stack.append(n.name)
            self.generic_visit(n)
            self.stack.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, n):
            f = n.func
            if isinstance(f, ast.Attribute) and f.attr == "exists":
                out.add((self.stack[-1] if self.stack else "<module>", lines[n.lineno - 1].strip()))
            self.generic_visit(n)

    V().visit(tree)
    return out


def test_census_every_exists_call_in_heal_py_is_routed_or_named_safe():
    found = _exists_calls((BIN / "heal.py").read_text())
    assert found == set(ALLOW), (
        f"unlisted raw .exists() probe(s): {sorted(found - set(ALLOW))}; "
        f"stale allowlist entr(ies): {sorted(set(ALLOW) - found)}")


def test_mutant_a_new_raw_exists_probe_reads_red():
    src = (BIN / "heal.py").read_text() + "\n\ndef _new_probe(p):\n    return p.exists()\n"
    assert _exists_calls(src) != set(ALLOW)


def test_the_census_ignores_comments_and_docstrings():
    src = 'def f(p):\n    """p.exists() in prose"""\n    # p.exists() in a comment\n    return 1\n'
    assert _exists_calls(src) == set()


def test_no_os_path_exists_in_heal_py():
    """R2: os.path.exists reads 'cannot see' as 'gone' (an AST walk: prose may name it)."""
    tree = ast.parse((BIN / "heal.py").read_text())
    hits = [n.lineno for n in ast.walk(tree)
            if isinstance(n, ast.Attribute) and n.attr in ("exists", "lexists", "isdir", "isfile")
            and isinstance(n.value, ast.Attribute) and n.value.attr == "path"
            and isinstance(n.value.value, ast.Name) and n.value.value.id == "os"]
    assert hits == [], f"os.path probe(s) at line(s) {hits}"
