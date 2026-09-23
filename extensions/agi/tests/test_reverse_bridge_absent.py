"""goal:g7.31.5.2 — the ABSENCE of a reverse harness-doc bridge is EXECUTABLE.

The goal node records, from `experiment:a00-fcd60995-reverse-bridge-absent`
and `hypothesis:a00-ce81c047-f9185d`, that no reverse bridge exists: editing
the artifact named by a node's `profile_ref` must NOT reconverge into the
node. Until 2026-09-23 that record was PROSE ONLY — nothing in the suite
would turn RED if a reverse bridge landed tomorrow.

This test is that red path. On a throwaway repo it:
  1. forward-projects the node (`profile_sync.sync_node`) and records the NODE
     file's sha256;
  2. mutates the ARTIFACT bytes on disk (`HARNESS EDITED LINE`);
  3. runs every candidate reconverging surface — `profile_sync.py <node>
     --check`, `profile_sync.py <node>`, `profile_sync.py --all`, and a
     `write.py <node> 'note ...'`;
  4. asserts the node never absorbs the artifact bytes and that `write.py`
     exposes no reverse/import/artifact verb.

If a reverse bridge is ever added, at least one surface below will bring
`HARNESS EDITED LINE` into the node (or move a read-only surface's node file
that must not move) and this test FAILS. That failure is the signal that
`goal:g7.31.5.2`'s absence record must be updated: the falsifier has landed
and the goal body may no longer say "reverse bridge absent".
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import profile_sync  # noqa: E402

NODE = "hypothesis:h1"
MUTATION = "HARNESS EDITED LINE\n"
BODY = "# standing\n\nrule one\n"
THOUGHT = ("<!-- THOUGHT:BEGIN — authored, not derived -->\n"
           "why this version\n<!-- THOUGHT:END -->\n")


def _repo(tmp_path: Path, ref: str | None = "profile/h1.md") -> Path:
    """A throwaway repo: `.agi/nodes/hypothesis/h1.md`, optionally linked."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    fm = ('---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
          'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
          'status: pending\n')
    if ref is not None:
        fm += f'profile_ref: "{ref}"\n'
    fm += "---\n\n"
    (graph / "nodes" / "hypothesis" / "h1.md").write_text(
        fm + BODY + "\n" + THOUGHT)
    return tmp_path


def _node_bytes(repo: Path) -> bytes:
    return (repo / ".agi" / "nodes" / "hypothesis" / "h1.md").read_bytes()


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _run(argv, repo: Path):
    return subprocess.run(
        [sys.executable, str(BIN / argv[0])] + argv[1:], cwd=repo,
        capture_output=True, text=True)


@pytest.mark.parametrize("name,argv", [
    ("check", ["profile_sync.py", NODE, "--check"]),
    ("forward_sync", ["profile_sync.py", NODE]),
    ("sweep_all", ["profile_sync.py", "--all"]),
])
def test_no_read_side_surface_reconverges_the_node(tmp_path, name, argv):
    """The node file is byte-identical after every surface, mutation or not.

    `--check` and `--all` are read-only by contract; the forward sync writes
    only the ARTIFACT. None of them may move the node file — so a reverse
    bridge showing up here fails the sha256 identity below.
    """
    repo = _repo(tmp_path)
    artifact, _n, _s = profile_sync.sync_node(repo / ".agi", NODE)
    before = _sha(_node_bytes(repo))
    # Re-mutate per surface so each one independently faces the edit.
    artifact.write_text(MUTATION)
    r = _run(argv, repo)
    after = _sha(_node_bytes(repo))
    assert after == before, (
        f"{name} moved the node file: a reverse bridge may have landed; "
        f"update goal:g7.31.5.2's absence record. rc={r.returncode} "
        f"stdout={r.stdout!r} stderr={r.stderr!r}")
    assert b"HARNESS EDITED LINE" not in _node_bytes(repo), (
        f"{name} pulled the artifact edit into the node — reverse bridge "
        f"present; goal:g7.31.5.2's absence record is now false")
    # Non-vacuity: --check/--all do not write the artifact; forward sync does,
    # and re-projects it FROM the node (the forward direction).
    if name == "forward_sync":
        assert artifact.read_bytes() != MUTATION.encode()
        _p, projected = profile_sync.project(repo / ".agi", NODE)
        assert artifact.read_bytes() == projected
    else:
        assert artifact.read_bytes() == MUTATION.encode(), (
            f"{name} is read-only and must not write the artifact")


def test_write_cli_note_does_not_import_the_artifact(tmp_path):
    """A `write.py` note advances the node forward; it never imports bytes."""
    repo = _repo(tmp_path)
    artifact, _n, _s = profile_sync.sync_node(repo / ".agi", NODE)
    artifact.write_text(MUTATION)
    r = _run(["write.py", NODE, "note round-check"], repo)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    after = _node_bytes(repo)
    assert b"HARNESS EDITED LINE" not in after, (
        "write.py imported the artifact edit into the node — reverse bridge "
        "present; goal:g7.31.5.2's absence record is now false")
    assert b"round-check" in after, "the declared forward note did not land"
    # The artifact was re-projected FROM the node (forward), graph as SoT.
    _p, projected = profile_sync.project(repo / ".agi", NODE)
    assert artifact.read_bytes() == projected
    assert b"HARNESS EDITED LINE" not in artifact.read_bytes()


@pytest.mark.parametrize("verb", ["reverse", "import", "artifact"])
def test_write_py_exposes_no_reverse_verb(tmp_path, verb):
    """No named verb would reconverge an artifact into the node."""
    repo = _repo(tmp_path)
    before = _node_bytes(repo)
    r = _run(["write.py", NODE, verb], repo)
    assert r.returncode != 0, f"write.py grew a {verb!r} verb: {r.stdout!r}"
    assert "no verb" in (r.stdout + r.stderr)
    assert _node_bytes(repo) == before