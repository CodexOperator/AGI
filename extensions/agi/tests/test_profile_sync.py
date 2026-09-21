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