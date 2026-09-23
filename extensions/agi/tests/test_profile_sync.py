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


# ---- goal:g7.31.5.3 residue B: the wire probe is BEHAVIOURAL, not a grep ----


def _linked_loop_root(tmp_path: Path):
    """A minimal `.agi`-shaped root with ONE linked hypothesis node, in sync.

    Shaped like the rotate harness (`_proj` in test_rotate.py): the passed
    root IS the graph dir, so `profile_ref` resolves against its parent.
    """
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\nclosed: false\n---\n")
    (root / "config.json").write_text("{}")
    (root / "nodes" / "hypothesis").mkdir(parents=True)
    fm = ('---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
          'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
          'status: pending\nprofile_ref: "profile/h1.md"\n---\n\n')
    (root / "nodes" / "hypothesis" / "h1.md").write_text(
        fm + BODY + "\n" + THOUGHT)
    dest, _n, _sha = profile_sync.sync_node(root, "hypothesis:h1")
    return root, dest


def _loop_args():
    from types import SimpleNamespace  # noqa: E402
    return SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1)


def test_loop_refuses_drift_before_any_spawn(monkeypatch, tmp_path, capsys):
    """Residue-B wire probe: a DELIBERATE desync makes cmd_loop refuse
    non-zero and NEVER reach spawn_window. This fails if the `cmd_loop` call
    site is removed -- a byte-grep of the file would not (it only saw
    cmd_rotate_self)."""
    import rotate  # noqa: E402
    root, dest = _linked_loop_root(tmp_path)
    dest.write_text("mutated\n")
    called = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: called.append(kw) or (0, ""))
    code = rotate.cmd_loop(_loop_args(), root)
    err = capsys.readouterr().err
    assert code == 1, (code, err)
    assert "profile drift" in err and "hypothesis:h1" in err
    assert called == [], "spawn_window must not be reached on drift"


def test_loop_passes_clean_graph_through_to_spawn(monkeypatch, tmp_path):
    """Symmetric clean case: an in-sync graph lets the loop proceed past the
    guard to spawn_window (the guard is a refusal, not a blanket stop)."""
    import rotate  # noqa: E402
    root, _dest = _linked_loop_root(tmp_path)
    called = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: called.append(kw) or (0, ""))
    code = rotate.cmd_loop(_loop_args(), root)
    assert code == 0
    assert len(called) == 1


def test_loop_reaches_the_live_guard_call_site(monkeypatch, tmp_path):
    """The wire is LIVE, not a string in the file: replacing the guard
    function itself changes what cmd_loop does, and it receives `root`."""
    import rotate  # noqa: E402
    root, _dest = _linked_loop_root(tmp_path)
    seen = []
    monkeypatch.setattr(rotate, "_check_profile_drift",
                        lambda r: seen.append(r) or None)
    called = []
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: called.append(kw) or (0, ""))
    code = rotate.cmd_loop(_loop_args(), root)
    assert code == 0
    assert seen == [root], "cmd_loop must call _check_profile_drift(root)"
    assert len(called) == 1


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


def _broken_prose(graph: Path, name: str, *, in_frontmatter: bool) -> Path:
    """A malformed node whose ONLY `profile_ref:` mention is in the body
    prose (in_frontmatter=False) or inside the unterminated-ish frontmatter
    block (True). No valid YAML, so it can only be judged by the heuristic."""
    prose = 'body prose mentions profile_ref: "profile/prose.md" here\n'
    extra = 'profile_ref: "profile/b.md"\n' if in_frontmatter else ""
    p = graph / "nodes" / "hypothesis" / name
    p.write_text("---\nid: hypothesis:broken\n: : : not valid yaml [[[\n"
                 + extra + "---\n\n" + prose)
    return p


def test_p7_prose_profile_ref_in_a_malformed_unlinked_node_is_a_noop(tmp_path):
    """Residue D: the heuristic must read FRONTMATTER only. Eight live nodes
    mention `profile_ref:` in prose; a malformed one is not a linked node and
    must not make --all (or the rotate guard) refuse a clean rotation."""
    import rotate  # noqa: E402
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    _broken_prose(repo / ".agi", "prose.md", in_frontmatter=False)
    r = _cli_all(repo)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "1 linked, 0 not ok" in r.stdout
    assert "prose" not in r.stdout
    assert rotate._check_profile_drift(repo / ".agi") is None


def test_frontmatter_profile_ref_still_flags_unreadable(tmp_path):
    """The symmetric half of Residue D: the SAME prose, plus a frontmatter
    `profile_ref:`, is a linked node that cannot be proven in sync -- named
    `unreadable` by path, refusal by the rotate guard."""
    import rotate  # noqa: E402
    repo = _repo(tmp_path)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    _broken_prose(repo / ".agi", "broken.md", in_frontmatter=True)
    r = _cli_all(repo)
    assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
    assert "UNREADABLE" in r.stdout and "broken.md" in r.stdout
    msg = rotate._check_profile_drift(repo / ".agi")
    assert msg and "profile drift" in msg and "broken.md" in msg


def test_check_all_survives_a_read_error_in_the_except_branch(
        tmp_path, monkeypatch):
    """Residue E: the recovery read_text can itself raise OSError. That must
    become a named `unreadable` row, never escape check_all (which the rotate
    guard would surface as a crash message, blocking a clean rotation)."""
    from pathlib import Path as _P
    import rotate  # noqa: E402
    repo = _repo(tmp_path)
    bad = _broken(repo / ".agi", "broken.md")
    real = _P.read_text
    calls = {"n": 0}

    def fake(self, *a, **k):
        if self == bad:
            calls["n"] += 1
            if calls["n"] >= 2:      # first read parses-and-fails, second dies
                raise OSError(13, "Permission denied")
        return real(self, *a, **k)

    monkeypatch.setattr(_P, "read_text", fake)
    rows = profile_sync.check_all(repo / ".agi")   # must not raise
    row = [x for x in rows if x.get("path") == str(bad)]
    assert len(row) == 1 and row[0]["status"] == "unreadable"
    assert "PermissionError" in row[0]["detail"] and "Permission denied" in row[0]["detail"]
    msg = rotate._check_profile_drift(repo / ".agi")
    assert msg and "broken.md" in msg and "unreadable" in msg
