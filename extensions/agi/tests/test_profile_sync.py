"""goal:g7.31.5.1 — write.py -> linked profile artifact, graph as SoT.

The falsifier's first conjunct: editing a linked node through `write.py`
changes the profile bytes to match, in the same action, with no second
command. `profile_ref` is the link (not `link_ref`, which resolves the other
way), resolution is repo-root-relative, and a ref that escapes the repo or
points under `.agi/nodes/` is refused by name, never written.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import profile_sync  # noqa: E402

BODY = "# standing\n\nrule one\n"
THOUGHT = ("<!-- THOUGHT:BEGIN — authored, not derived -->\n"
           "why this version\n<!-- THOUGHT:END -->\n")


def _repo(tmp_path: Path, ref: str | None = "profile/h1.md",
          payload_ref: str | None = None) -> Path:
    """A throwaway repo: `.agi/nodes/hypothesis/h1.md`, optionally linked."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    fm = ('---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
          'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
          'status: pending\n')
    if ref is not None:
        fm += f'profile_ref: "{ref}"\n'
    if payload_ref is not None:
        fm += f'payload_ref: "{payload_ref}"\n'
    fm += "---\n\n"
    (graph / "nodes" / "hypothesis" / "h1.md").write_text(
        fm + BODY + "\n" + THOUGHT)
    return tmp_path


def _cli(argv, cwd, stdin=None):
    return subprocess.run(
        [sys.executable, str(BIN / "write.py")] + argv, cwd=cwd,
        input=stdin, capture_output=True, text=True)


def test_sync_projects_the_normalized_body(tmp_path):
    repo = _repo(tmp_path)
    dest, n, sha = profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    assert dest == repo / "profile" / "h1.md"
    assert dest.read_bytes() == BODY.encode()
    assert n == len(BODY) and len(sha) == 64
    assert b"THOUGHT" not in dest.read_bytes(), "the thought is not projection"


def test_write_cli_updates_the_linked_artifact_in_the_same_action(tmp_path):
    repo = _repo(tmp_path)
    dest = repo / "profile" / "h1.md"
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    before = dest.read_bytes()
    r = _cli(["hypothesis:h1", "replace body 1:1 -"], repo, stdin="replaced\n")
    assert r.returncode == 0, r.stderr
    after = dest.read_bytes()
    assert after != before, "the same action must move the artifact bytes"
    _p, expected = profile_sync.project(repo / ".agi", "hypothesis:h1")
    assert after == expected
    assert after.startswith(b"replaced\n")


def test_check_reports_drift_without_writing(tmp_path):
    repo = _repo(tmp_path)
    dest = repo / "profile" / "h1.md"
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    ok = subprocess.run([sys.executable, str(BIN / "profile_sync.py"),
                         "hypothesis:h1", "--check"], cwd=repo,
                        capture_output=True, text=True)
    assert ok.returncode == 0, ok.stderr
    dest.write_text("mutated\n")
    drift = subprocess.run([sys.executable, str(BIN / "profile_sync.py"),
                            "hypothesis:h1", "--check"], cwd=repo,
                           capture_output=True, text=True)
    assert drift.returncode != 0
    assert "DRIFT" in drift.stdout
    assert dest.read_text() == "mutated\n", "--check must not write"


def test_a_node_without_profile_ref_is_an_explicit_noop(tmp_path):
    repo = _repo(tmp_path, ref=None)
    r = subprocess.run([sys.executable, str(BIN / "profile_sync.py"),
                        "hypothesis:h1"], cwd=repo, capture_output=True,
                       text=True)
    assert r.returncode == 0, r.stderr
    assert "no profile_ref" in r.stdout
    assert not (repo / "profile").exists()


@pytest.mark.parametrize("ref", ["../escape.md", ".agi/nodes/evil.md"])
def test_escaping_and_node_refs_are_refused_by_name(tmp_path, ref):
    repo = _repo(tmp_path, ref=ref)
    r = subprocess.run([sys.executable, str(BIN / "profile_sync.py"),
                        "hypothesis:h1"], cwd=repo, capture_output=True,
                       text=True)
    assert r.returncode == 2
    assert "REFUSED" in r.stderr and ref in r.stderr
    assert not (repo / "profile").exists()
    assert not (tmp_path.parent / "escape.md").exists()
    assert not (repo / ".agi" / "nodes" / "evil.md").exists()


def test_no_project_root_is_refused_by_name(tmp_path):
    """cwd outside any `.agi` -> named refusal, never Path(None) TypeError."""
    bare = tmp_path / "bare"
    bare.mkdir()
    r = subprocess.run([sys.executable, str(BIN / "profile_sync.py"),
                        "hypothesis:h1"], cwd=bare, capture_output=True,
                       text=True)
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "REFUSED" in r.stderr
    assert "no project root" in r.stderr
    assert "TypeError" not in r.stderr


def test_a_directory_target_is_refused_by_name(tmp_path):
    """`dest.is_dir()` -> named refusal, never an uncaught IsADirectoryError."""
    repo = _repo(tmp_path, ref="profile_dir")
    (repo / "profile_dir").mkdir()
    r = subprocess.run([sys.executable, str(BIN / "profile_sync.py"),
                        "hypothesis:h1", "--check"], cwd=repo,
                       capture_output=True, text=True)
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "REFUSED" in r.stderr and "directory" in r.stderr
    assert "IsADirectoryError" not in r.stderr


def test_payload_failure_leaves_the_profile_artifact_unchanged(tmp_path):
    """Residue 4: the projection does not advance ahead of a failed payload."""
    repo = _repo(tmp_path, payload_ref="payloads/missing.txt")
    dest = repo / "profile" / "h1.md"
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    assert dest.read_bytes() == BODY.encode()
    src = tmp_path / "src.txt"
    src.write_text("new payload bytes\n")
    r = _cli(["hypothesis:h1", f"note changed && payload {src}"], repo)
    assert r.returncode != 0, (r.returncode, r.stdout, r.stderr)
    assert "does not exist" in r.stderr
    # The write failed; the derived projection must not have moved.
    assert dest.read_bytes() == BODY.encode()
    # Non-vacuous: the node body DID advance, so the current projection
    # differs from what the artifact still holds — the reorder is what keeps
    # the projection from running ahead of the payload.
    _p, projected = profile_sync.project(repo / ".agi", "hypothesis:h1")
    assert projected != BODY.encode()
    assert dest.read_bytes() != projected

# ---- goal:g7.31.5.3 — whole-graph sweep + pre-rotation guard ---------------

def _cli_all(cwd):
    return subprocess.run(
        [sys.executable, str(BIN / "profile_sync.py"), "--all"], cwd=cwd,
        capture_output=True, text=True)


def _deprecated_repo(tmp_path):
    repo = _repo(tmp_path, ref=None)
    d = repo / ".agi" / "nodes" / "deprecated" / "hypothesis"
    d.mkdir(parents=True)
    (d / "h2.md").write_text(
        '---\nid: "hypothesis:h2"\ntype: hypothesis\nmint_id: def456\n'
        'title: "t2"\nstatus: pending\nprofile_ref: "profile/h2.md"\n---\n\n'
        + BODY)
    return repo


def test_sweep_is_green_on_a_linked_node_in_sync(tmp_path):
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    r = _cli_all(repo)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "OK hypothesis:h1" in r.stdout and "1 linked, 0 not ok" in r.stdout


def test_sweep_exits_nonzero_and_names_a_mutated_artifact(tmp_path):
    repo = _repo(tmp_path)
    dest, _n, _sha = profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    dest.write_text("mutated\n")
    r = _cli_all(repo)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "DRIFT hypothesis:h1" in r.stdout
    assert "1 not ok" in r.stdout


def test_sweep_flags_a_missing_artifact(tmp_path):
    repo = _repo(tmp_path)
    r = _cli_all(repo)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "MISSING hypothesis:h1" in r.stdout


def test_sweep_reads_the_retired_sibling_too(tmp_path):
    repo = _deprecated_repo(tmp_path)
    dest, _n, _sha = profile_sync.sync_node(repo / ".agi", "hypothesis:h2")
    assert _cli_all(repo).returncode == 0
    dest.write_text("mutated\n")
    r = _cli_all(repo)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "hypothesis:h2" in r.stdout


def test_sweep_counts_a_refused_ref_as_a_named_failure(tmp_path):
    repo = _repo(tmp_path, ref="../escape.md")
    r = _cli_all(repo)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "REFUSED hypothesis:h1" in r.stdout


def test_rotate_guard_refuses_on_drift_and_passes_when_clean(tmp_path):
    import rotate  # noqa: E402
    none_linked = _repo(tmp_path / "none", ref=None)
    assert rotate._check_profile_drift(none_linked / ".agi") is None
    repo = _repo(tmp_path / "linked")
    dest, _n, _sha = profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    assert rotate._check_profile_drift(repo / ".agi") is None
    dest.write_text("mutated\n")
    msg = rotate._check_profile_drift(repo / ".agi")
    assert msg and "profile drift" in msg and "hypothesis:h1" in msg


def _loop_args(tmp_path: Path, **kw) -> "object":
    from types import SimpleNamespace
    wins = tmp_path / "windows.txt"
    wins.write_text("belam\n")
    a = dict(force=True, session_log=None, role="prime_director",
             tmux_session="t", window_path=str(wins), name="belam-X",
             name_prefix="belam", prompt_file="p", model=None, effort=None,
             settings=None, dry_run=True, debug_file=str(tmp_path / "d.log"),
             successor_argv=None, seat=None, harness=None, timeout=0)
    a.update(kw)
    return SimpleNamespace(**a)


def test_cmd_loop_refuses_on_drift_and_never_reaches_the_spawn(
        tmp_path, monkeypatch, capsys):
    """Residue 2: a BEHAVIOURAL wire probe, not a source grep. If `cmd_loop`
    ever drops the guard call, dry-run proceeds to the spawn and this fails."""
    import rotate  # noqa: E402
    monkeypatch.setattr(rotate, "_check_branch_guard", lambda root: None)
    repo = _repo(tmp_path)
    dest, _n, _sha = profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    dest.write_text("mutated\n")

    def _boom(*a, **k):
        raise AssertionError("spawn_window reached despite profile drift")
    monkeypatch.setattr(rotate, "spawn_window", _boom)
    rc = rotate.cmd_loop(_loop_args(tmp_path), repo / ".agi")
    err = capsys.readouterr().err
    assert rc == 1, (rc, err)
    assert "profile drift" in err and "hypothesis:h1" in err


def test_cmd_loop_proceeds_on_a_clean_repo(tmp_path, monkeypatch, capsys):
    """The guard is really invoked and does NOT block when the sweep is green."""
    import rotate  # noqa: E402
    monkeypatch.setattr(rotate, "_check_branch_guard", lambda root: None)
    calls = []
    real_guard = rotate._check_profile_drift

    def _spy(root):
        calls.append(root)
        return real_guard(root)
    monkeypatch.setattr(rotate, "_check_profile_drift", _spy)
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    reached = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **k: (reached.append(k["name"]), (0, None))[1])
    rc = rotate.cmd_loop(_loop_args(tmp_path), repo / ".agi")
    assert rc == 0, capsys.readouterr().err
    assert calls == [repo / ".agi"], "the guard was not invoked on cmd_loop"
    assert reached, "a clean repo must still reach the spawn"


def test_cmd_rotate_self_refuses_on_drift_before_the_geometry_guard(
        tmp_path, monkeypatch, capsys):
    """Same wire, the other successor primitive: drift refuses before any
    later side effect (the geometry resolution runs only after it)."""
    from types import SimpleNamespace
    import rotate  # noqa: E402
    monkeypatch.setattr(rotate, "_rotate_human_gate",
                        lambda root, name: (None, None))
    monkeypatch.setattr(rotate, "_check_branch_guard", lambda root: None)
    repo = _repo(tmp_path)
    dest, _n, _sha = profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    dest.write_text("mutated\n")

    def _boom(root):
        raise AssertionError("_geometry_resolution_root reached past drift")
    monkeypatch.setattr(rotate, "_geometry_resolution_root", _boom)
    rc = rotate.cmd_rotate_self(SimpleNamespace(name="belam-X",
                                                prepare=False),
                                repo / ".agi")
    err = capsys.readouterr().err
    assert rc == 1, (rc, err)
    assert "profile drift" in err and "hypothesis:h1" in err


# ---- goal:g7.31.5.3 corrective round 2: malformed siblings are not drift ----

def _broken(graph: Path, name: str, extra: str = "") -> Path:
    p = graph / "nodes" / "hypothesis" / name
    p.write_text("---\nid: hypothesis:broken\n: : : not valid yaml [[[\n"
                 + extra + "---\n\nbody\n")
    return p


def test_p7_malformed_unlinked_sibling_is_a_clean_noop(tmp_path):
    """P7: an in-sync linked node + an unparseable UNLINKED sibling stays
    green — the sibling does not link a profile, so it is not ours to fail."""
    import rotate  # noqa: E402
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    _broken(repo / ".agi", "broken.md")
    r = _cli_all(repo)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "1 linked, 0 not ok" in r.stdout
    assert "broken" not in r.stdout
    assert rotate._check_profile_drift(repo / ".agi") is None


def test_a_malformed_file_that_looks_linked_is_named_unreadable(tmp_path):
    """`profile_ref:` in the raw bytes means it cannot be proven in sync:
    surface it by path, never silently drop it."""
    import rotate  # noqa: E402
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    _broken(repo / ".agi", "broken.md", extra='profile_ref: "profile/b.md"\n')
    r = _cli_all(repo)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "UNREADABLE" in r.stdout and "broken.md" in r.stdout
    assert "2 linked, 1 not ok" in r.stdout
    msg = rotate._check_profile_drift(repo / ".agi")
    assert msg and "broken.md" in msg and "unreadable" in msg
    assert "profile drift" in msg


def test_body_only_profile_ref_mention_is_not_unreadable(tmp_path):
    """Residue 4.2: the heuristic reads the YAML FRONTMATTER only — prose in
    the body naming `profile_ref:` must not mark a malformed file linked."""
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    p = _broken(repo / ".agi", "body.md")
    p.write_text(p.read_text()
                 + 'prose: see profile_ref: "profile/b.md"\n')
    r = _cli_all(repo)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "1 linked, 0 not ok" in r.stdout
    assert "body.md" not in r.stdout


def test_permission_denied_file_never_raises_out_of_check_all(
        tmp_path, monkeypatch):
    """Residue 4.3: an unreadable file is named `unreadable`, never a
    traceback out of `check_all`."""
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    p = repo / ".agi" / "nodes" / "hypothesis" / "locked.md"
    p.write_text('---\nid: "hypothesis:locked"\ntype: hypothesis\n'
                 'profile_ref: "profile/locked.md"\n---\n\nbody\n')
    real = Path.read_text

    def denied(self, *a, **k):
        if self == p:
            raise PermissionError(13, "Permission denied", str(self))
        return real(self, *a, **k)
    monkeypatch.setattr(Path, "read_text", denied)
    rows = profile_sync.check_all(repo / ".agi")  # must not raise
    locked = [r for r in rows if r.get("path") == str(p)]
    assert locked and locked[0]["status"] == "unreadable", rows
