"""goal:g7.16.1.11.46.23 V8a 3a: node_commit, the by-exact-path commit of a node a runtime job wrote.

Council decision alive 23:28:02Z 10-25 (3/3): MINIMAL, KEEPING the already-dirty refusal. One test per promise, each
with the mutant that must be REFUSED: a hand edit in the target path (bytes untouched, caller non-zero), a held
suite lock, index.lock held past the bound, an unknown git state (fail closed), a clean path (committed under the
caller's subject, nothing else swept in).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_BIN))

import node_commit as nc  # noqa: E402
import node_writer  # noqa: E402

NODE = "doc:board-x"


def _git(d, *a):
    return subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture()
def proj(tmp_path):
    d = tmp_path / "proj"
    (d / ".agi" / "nodes" / "doc").mkdir(parents=True)
    (d / ".agi" / "config.json").write_text(json.dumps({}))
    (d / ".agi" / "nodes" / "doc" / "board-x.md").write_text(
        "---\nid: doc:board-x\ntitle: board x\ncell: old\n---\n# board x\n")
    (d / "other.txt").write_text("o\n")
    _git(d, "init", "-q", "-b", "main")
    for k, v in (("user.name", "t"), ("user.email", "t@t"), ("commit.gpgsign", "false")):
        _git(d, "config", k, v)
    _git(d, "add", "-A")
    _git(d, "commit", "-q", "-m", "base")
    return d


def _set(root, **fm):
    return lambda: node_writer.update_node(root, NODE, set_fm=fm)


def test_a_clean_path_is_committed_under_the_callers_subject_and_nothing_else_rides(proj):
    root = proj / ".agi"
    (proj / "other.txt").write_text("a peer's unstaged edit\n")          # not ours: must stay out of the commit
    _git(proj, "add", "other.txt")                                         # ... even STAGED by a peer
    nc.land(root, NODE, "board: doc:board-x (belam)", _set(root, cell="new"))
    assert _git(proj, "log", "-1", "--format=%s") == "board: doc:board-x (belam)"
    assert _git(proj, "show", "--name-only", "--format=", "HEAD") == ".agi/nodes/doc/board-x.md"
    assert "cell: new" in (proj / ".agi/nodes/doc/board-x.md").read_text()
    assert _git(proj, "diff", "--cached", "--name-only") == "other.txt"   # the peer's staged file is still staged


def test_mutant_a_hand_edit_in_the_target_path_is_refused_before_any_write(proj):
    root = proj / ".agi"
    f = proj / ".agi/nodes/doc/board-x.md"
    f.write_text(f.read_text() + "\nbelam's hand edit\n")
    before, head = f.read_text(), _git(proj, "rev-parse", "HEAD")
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(root, NODE, "board: x", _set(root, cell="new"))
    assert "already dirty: refused, nothing written" in exc.value.line and not exc.value.written
    assert f.read_text() == before and _git(proj, "rev-parse", "HEAD") == head   # bytes untouched, no commit


def test_mutant_an_unknown_git_state_fails_closed_and_names_itself(proj, monkeypatch, capsys):
    root = proj / ".agi"
    real = nc._git

    def fake(r, *a):
        if "diff" in a:
            return subprocess.CompletedProcess(a, 128, "", "fatal: broken")
        return real(r, *a)

    monkeypatch.setattr(nc, "_git", fake)
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(root, NODE, "board: x", _set(root, cell="new"))
    assert "already dirty: refused" in exc.value.line
    assert "state unknown, path refused" in capsys.readouterr().err
    assert "cell: new" not in (proj / ".agi/nodes/doc/board-x.md").read_text()


def test_mutant_a_held_suite_lock_refuses_by_name_with_the_bytes_on_disk(proj, monkeypatch):
    import verification
    root = proj / ".agi"
    monkeypatch.setattr(verification, "suite_lock_holder", lambda r: 4242)
    monkeypatch.setattr(verification, "suite_lock_policy", lambda r: {"hold_wait_s": 0.2, "write_commit_wait_s": 1, "file": "verify-suite.lock"})
    head = _git(proj, "rev-parse", "HEAD")
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(root, NODE, "board: x", _set(root, cell="new"))
    assert "held by live pid 4242" in exc.value.line and exc.value.written and "recover once released: git -C" in exc.value.line
    assert _git(proj, "rev-parse", "HEAD") == head
    assert _git(proj, "diff", "--cached", "--name-only") == ""            # never left staged


def test_mutant_index_lock_held_past_the_bound_is_a_named_line_not_a_skipped_hour(proj, monkeypatch):
    root = proj / ".agi"
    monkeypatch.setattr(nc, "_commit_wait_s", lambda r: 0.3)
    (proj / ".git" / "index.lock").write_text("")
    head = _git(proj, "rev-parse", "HEAD")
    try:
        with pytest.raises(nc.CommitRefused) as exc:
            nc.land(root, NODE, "board: x", _set(root, cell="new"))
    finally:
        (proj / ".git" / "index.lock").unlink()
    assert "commit failed after" in exc.value.line and "UNCOMMITTED" in exc.value.line and exc.value.written
    assert _git(proj, "rev-parse", "HEAD") == head
    assert "cell: new" in (proj / ".agi/nodes/doc/board-x.md").read_text()   # on disk, named, recoverable


def test_mutant_a_hand_edit_landing_during_the_lock_wait_is_never_swept_into_the_commit(proj, monkeypatch):
    root = proj / ".agi"
    f = proj / ".agi/nodes/doc/board-x.md"
    real = nc._held

    def held_then_a_human_edits(r, recover):
        out = real(r, recover)
        f.write_text(f.read_text() + "\nbelam edits while we waited\n")
        return out

    monkeypatch.setattr(nc, "_held", held_then_a_human_edits)
    head = _git(proj, "rev-parse", "HEAD")
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(root, NODE, "board: x", _set(root, cell="new"))
    assert "changed since this job wrote it" in exc.value.line and exc.value.written
    assert _git(proj, "rev-parse", "HEAD") == head and _git(proj, "diff", "--cached", "--name-only") == ""
    assert "belam edits while we waited" in f.read_text() and "cell: new" in f.read_text()


def test_an_index_lock_that_clears_inside_the_bound_commits(proj, monkeypatch):
    root = proj / ".agi"
    monkeypatch.setattr(nc, "_commit_wait_s", lambda r: 5)
    lock = proj / ".git" / "index.lock"
    lock.write_text("")
    real, n = nc._git, {"i": 0}

    def fake(r, *a):
        if a and a[0] == "add":
            n["i"] += 1
            if n["i"] == 2 and lock.exists():
                lock.unlink()
        return real(r, *a)

    monkeypatch.setattr(nc, "_git", fake)
    nc.land(root, NODE, "board: x", _set(root, cell="new"))
    assert _git(proj, "log", "-1", "--format=%s") == "board: x" and n["i"] >= 2


def test_a_rejected_write_is_refused_by_name_and_nothing_is_committed(proj):
    root = proj / ".agi"
    head = _git(proj, "rev-parse", "HEAD")
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(root, "doc:no-such-node", "board: x", _set(root, cell="new"))
    assert "no node file for doc:no-such-node" in exc.value.line
    assert _git(proj, "rev-parse", "HEAD") == head


def test_not_a_git_checkout_is_said_aloud_never_a_silent_nothing(tmp_path, capsys):
    d = tmp_path / "plain"
    (d / ".agi/nodes/doc").mkdir(parents=True)
    (d / ".agi/config.json").write_text("{}")
    (d / ".agi/nodes/doc/board-x.md").write_text("---\nid: doc:board-x\ntitle: t\n---\n# t\n")
    nc.land(d / ".agi", NODE, "board: x", _set(d / ".agi", cell="new"))
    assert "cell: new" in (d / ".agi/nodes/doc/board-x.md").read_text()
    assert f"node_commit: {d / '.agi'} is not a git checkout: written, not committed" in capsys.readouterr().err
    # the direct call returns the same NOTE (never "")
    assert nc.commit_paths(d / ".agi", [d / ".agi/nodes/doc/board-x.md"], "x").endswith("written, not committed")


def test_mutant_a_git_dir_git_cannot_read_is_refused_before_any_write_and_non_zero(proj, monkeypatch):
    """.git present + rev-parse rc 128 (dubious ownership / a broken .git / no git): the write would land and nothing
    would commit, the hourly job exiting 0 every hour. land refuses BEFORE writing; commit_paths refuses too."""
    root = proj / ".agi"
    real = nc._git

    def fake(r, *a):
        if a[:2] == ("rev-parse", "--is-inside-work-tree"):
            return subprocess.CompletedProcess(a, 128, "", "fatal: detected dubious ownership in repository")
        return real(r, *a)

    monkeypatch.setattr(nc, "_git", fake)
    before = (proj / ".agi/nodes/doc/board-x.md").read_text()
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(root, NODE, "board: x", _set(root, cell="new"))
    assert "git cannot read" in exc.value.line and "dubious ownership" in exc.value.line and not exc.value.written
    assert (proj / ".agi/nodes/doc/board-x.md").read_text() == before          # nothing written
    with pytest.raises(nc.CommitRefused) as exc2:                                  # the direct call: refused, written
        nc.commit_paths(root, [proj / ".agi/nodes/doc/board-x.md"], "x")
    assert "dubious ownership" in exc2.value.line and exc2.value.written


def test_mutant_a_broken_dot_git_in_an_ancestor_is_refused_not_a_plain_directory(tmp_path):
    d = tmp_path / "proj"
    (d / ".agi/nodes/doc").mkdir(parents=True)
    (d / ".agi/config.json").write_text("{}")
    (d / ".agi/nodes/doc/board-x.md").write_text("---\nid: doc:board-x\ntitle: t\n---\n# t\n")
    (d / ".git").write_text("gitdir: /nonexistent/nowhere\n")                   # a .git git cannot use
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(d / ".agi", NODE, "board: x", _set(d / ".agi", cell="new"))
    assert "git cannot read" in exc.value.line and "cell: new" not in (d / ".agi/nodes/doc/board-x.md").read_text()


def test_wait_lock_waits_the_bound_once_and_names_the_holder_past_it(proj, monkeypatch):
    """The ONE bounded loop (the job's start check and the commit both use it): free -> (None, bound); released
    inside the bound -> (None, bound); still held past it -> the live pid."""
    import threading
    import time
    import verification
    root = proj / ".agi"
    monkeypatch.setattr(verification, "suite_lock_policy", lambda r: {"hold_wait_s": 1.0, "file": "verify-suite.lock"})
    state = {"pid": None}
    monkeypatch.setattr(verification, "suite_lock_holder", lambda r: state["pid"])
    assert nc.wait_lock(root) == (None, 1.0)
    state["pid"] = 4242
    threading.Timer(0.4, lambda: state.update(pid=None)).start()
    t0 = time.monotonic()
    assert nc.wait_lock(root) == (None, 1.0) and 0.3 < time.monotonic() - t0 < 1.0     # released inside the bound
    state["pid"] = 4242
    t0 = time.monotonic()
    assert nc.wait_lock(root) == (4242, 1.0) and time.monotonic() - t0 >= 0.9           # held past it: the pid


def test_wait_lock_an_unreadable_policy_raises_so_callers_fail_closed(proj, monkeypatch):
    import verification
    monkeypatch.setattr(verification, "suite_lock_policy", lambda r: (_ for _ in ()).throw(RuntimeError("policy unreadable")))
    monkeypatch.setattr(verification, "suite_lock_holder", lambda r: None)
    with pytest.raises(RuntimeError):
        nc.wait_lock(proj / ".agi")


def test_mutant_a_dangling_dot_git_symlink_is_refused_lexists_not_exists(tmp_path):
    d = tmp_path / "proj"
    (d / ".agi/nodes/doc").mkdir(parents=True)
    (d / ".agi/config.json").write_text("{}")
    (d / ".agi/nodes/doc/board-x.md").write_text("---\nid: doc:board-x\ntitle: t\n---\n# t\n")
    (d / ".git").symlink_to(tmp_path / "nowhere")                                  # a link to nothing: exists() is False
    assert not (d / ".git").exists()
    with pytest.raises(nc.CommitRefused) as exc:
        nc.land(d / ".agi", NODE, "board: x", _set(d / ".agi", cell="new"))
    assert "git cannot read" in exc.value.line


def test_append_note_goes_under_the_one_heading_and_never_twice():
    b = nc.append_note("# t\n", "first")
    assert b.endswith("## Agent Notes\nfirst\n")
    b2 = nc.append_note(b, "second")
    assert b2.count("## Agent Notes") == 1 and b2.endswith("first\n\nsecond\n")
    assert nc.append_note(b2, "first") == b2 and nc.append_note(b2, "  ") == b2


def test_help_is_non_empty_and_rc_0():
    r = subprocess.run([sys.executable, str(_BIN / "node_commit.py"), "--help"], capture_output=True, text=True)
    assert r.returncode == 0 and "by-exact-path commit" in " ".join(r.stdout.split()) and "land(" in r.stdout
