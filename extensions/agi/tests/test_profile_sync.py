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

# ---- goal:g7.31.5.2 — the reverse bridge's absence, made executable --------

HARNESS_EDIT = "HARNESS EDITED LINE\n"


def _node_path(repo: Path) -> Path:
    return repo / ".agi" / "nodes" / "hypothesis" / "h1.md"


def _body_bytes(repo: Path) -> bytes:
    """A linked node's normalized body bytes — the projection payload.

    The raw region after the closing `---` moves by a leading blank line when
    `write.py` re-renders a node, which is formatting, not a bridge. The
    projection (`_projected_bytes`: THOUGHT stripped, edges trimmed) is the
    body content a reverse bridge would actually overwrite, so that is what
    this detector compares.
    """
    f = profile_sync.node_writer.find_node_file(repo / ".agi", "hypothesis:h1")
    nf = profile_sync.fmr.load_node_file(f)
    return profile_sync._projected_bytes(nf)


def test_artifact_edit_never_rewrites_the_linked_node(tmp_path):
    """goal:g7.31.5.2, the prose falsifier as a committed detector.

    A reverse bridge (artifact -> node) is ABSENT on this tip. Edit the
    artifact named by a node's `profile_ref`, then run every production
    surface that reads that ref. While the bridge is absent the node's BODY
    bytes are invariant — no surface reconverges the artifact into the node.
    The day a reverse bridge lands, at least one of these assertions goes
    red, which is exactly the condition the goal node's falsifier names.

    Positive control: `write.py ... 'set title ...'` DOES move the node's
    whole-file bytes (frontmatter), so the probe demonstrably observes a
    node-file change and the invariance above is not vacuous.
    """
    repo = _repo(tmp_path)
    dest = repo / "profile" / "h1.md"
    node = _node_path(repo)
    profile_sync.sync_node(repo / ".agi", "hypothesis:h1")
    before_body = _body_bytes(repo)
    before_file = node.read_bytes()

    # (b) edit the harness-side artifact to different bytes
    dest.write_text(HARNESS_EDIT)
    assert dest.read_bytes() == HARNESS_EDIT.encode()

    # (c)+(d) every production surface that reads profile_ref leaves the
    # node body untouched — no reverse bridge reconverged the artifact.
    surfaces = [
        [sys.executable, str(BIN / "profile_sync.py"),
         "hypothesis:h1", "--check"],
        [sys.executable, str(BIN / "profile_sync.py"), "hypothesis:h1"],
        [sys.executable, str(BIN / "profile_sync.py"), "--all"],
    ]
    for argv in surfaces:
        subprocess.run(argv, cwd=repo, capture_output=True, text=True)
        assert _body_bytes(repo) == before_body, (
            f"reverse bridge detected: {argv[2:]} reconverged the artifact "
            "into the node body")
        assert node.read_bytes() == before_file, (
            f"reverse bridge detected: {argv[2:]} rewrote the node file")

    # (e) positive control — write.py reads profile_ref, re-projects the
    # GRAPH onto the artifact, and changes the node's own bytes.
    r = _cli(["hypothesis:h1", "set title control-title"], repo)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert node.read_bytes() != before_file, (
        "positive control: write.py did not change the node bytes, so this "
        "probe cannot see a node change at all")
    assert _body_bytes(repo) == before_body, (
        "a frontmatter-only write must not touch the body")
    assert "HARNESS" not in dest.read_text(), (
        "forward sync (graph -> artifact) must still overwrite the edit")


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


def test_rotate_guard_wire_reaches_the_sweep(tmp_path):
    """The call site in cmd_rotate_self must name the guard (wire probe)."""
    src = (BIN / "rotate.py").read_text()
    assert "pguard = _check_profile_drift(root)" in src


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
