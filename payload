"""T-011 tests: directory walk determinism (graph-core/R6)."""

from pathlib import Path

from graph_core.loader import load_directory, walk_node_files

WALK_FIXTURE = Path(__file__).parent.parent / "fixtures" / "walk_test"


def test_walk_returns_files_sorted() -> None:
    """R6.4: deterministic walk — sorted within and across directories."""
    paths = walk_node_files(WALK_FIXTURE)
    names = [p.name for p in paths]
    # Within-dir sort: file_b.md before file_c.md
    b_idx = names.index("file_b.md")
    c_idx = names.index("file_c.md")
    assert b_idx < c_idx


def test_walk_byte_equal_across_runs() -> None:
    """R6.4: two walks of the same fixture yield the SAME ordered path list."""
    p1 = walk_node_files(WALK_FIXTURE)
    p2 = walk_node_files(WALK_FIXTURE)
    assert p1 == p2


def test_walk_picks_up_md_only(tmp_path: Path) -> None:
    """Only .md/.json files are walked; .txt etc skipped."""
    (tmp_path / "n.md").write_text("---\nid: x\n---\n")
    (tmp_path / "n.txt").write_text("not a node")
    (tmp_path / "n.json").write_text('{"frontmatter": {"id": "y"}, "body": "z"}')
    paths = walk_node_files(tmp_path)
    suffixes = {p.suffix for p in paths}
    assert suffixes == {".md", ".json"}


def test_load_directory_id_sequence_stable() -> None:
    """R6.1 + R6.4: loading same dir twice yields identical id sequences."""
    g1, loaded1 = load_directory(WALK_FIXTURE)
    g2, loaded2 = load_directory(WALK_FIXTURE)
    seq1 = [ln.node.id for ln in loaded1]
    seq2 = [ln.node.id for ln in loaded2]
    assert seq1 == seq2


def test_load_directory_node_count_matches_files() -> None:
    """R6.1: node count == file count for the fixture (4 files)."""
    g, loaded = load_directory(WALK_FIXTURE)
    # 4 files in fixture = 4 nodes minimum
    assert len(loaded) == 4
