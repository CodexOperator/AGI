"""T-008 tests: directory-level error isolation (graph-core/R4.4)."""

from pathlib import Path

from graph_core.persistence import load_node_dir, FrontmatterError


def test_dir_load_isolates_bad_file(tmp_path: Path) -> None:
    """One valid + one malformed → 1 node + 1 error, both reported."""
    good = tmp_path / "good.md"
    good.write_text("---\nid: hyp:ok\ntype: hypothesis\n---\n\nbody\n")
    bad = tmp_path / "bad.md"
    bad.write_text("---\nid: hyp:bad\n")  # missing closing ---
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 1
    assert result.nodes[0].frontmatter["id"] == "hyp:ok"
    assert len(result.errors) == 1
    assert result.errors[0].path == bad
    assert "closing" in result.errors[0].reason.lower() or "---" in result.errors[0].reason


def test_dir_load_skips_non_node_files(tmp_path: Path) -> None:
    """Files that aren't .md/.json are silently ignored."""
    (tmp_path / "node.md").write_text("---\nid: a\n---\nb\n")
    (tmp_path / "README.txt").write_text("not a node")
    (tmp_path / "data.csv").write_text("a,b\n1,2\n")
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 1
    assert len(result.errors) == 0


def test_dir_load_mixed_md_and_json(tmp_path: Path) -> None:
    """Both .md and .json node files are picked up."""
    (tmp_path / "a.md").write_text("---\nid: a\n---\nbody-a\n")
    (tmp_path / "b.json").write_text('{"frontmatter": {"id": "b"}, "body": "body-b"}\n')
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 2
    assert len(result.errors) == 0


def test_dir_load_not_a_directory(tmp_path: Path) -> None:
    """Pointing at a file rather than a dir raises FrontmatterError."""
    f = tmp_path / "x.md"
    f.write_text("---\nid: x\n---\n")
    import pytest

    with pytest.raises(FrontmatterError):
        load_node_dir(f)


def test_dir_load_continues_after_multiple_errors(tmp_path: Path) -> None:
    """Multiple bad files → multiple LoadErrors, all good files load."""
    (tmp_path / "good1.md").write_text("---\nid: a\n---\n")
    (tmp_path / "good2.md").write_text("---\nid: b\n---\n")
    (tmp_path / "bad1.md").write_text("no frontmatter at all")
    (tmp_path / "bad2.json").write_text("{not json")
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 2
    assert len(result.errors) == 2
    assert {e.path.name for e in result.errors} == {"bad1.md", "bad2.json"}
